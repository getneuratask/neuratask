from typing import List, Optional, Type, Any
from uuid import UUID
import psycopg2
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel

class PostgresBaseRepository:
    def __init__(self, connection_params: dict):
        self.connection_params = connection_params
        
    def _get_connection(self):
        return psycopg2.connect(**self.connection_params)
    
    def _execute_query(self, query: str, params: Optional[tuple] = None) -> List[dict]:
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, params)
                if cur.description:
                    return [dict(row) for row in cur.fetchall()]
                return []
    
    def _execute_single(self, query: str, params: Optional[tuple] = None) -> Optional[dict]:
        results = self._execute_query(query, params)
        return results[0] if results else None
    
    def _prepare_data(self, entity: BaseModel) -> dict:
        """Convert entity data, handling UUID serialization"""
        data = entity.model_dump()
        for key, value in data.items():
            if isinstance(value, UUID):
                data[key] = str(value)
        return data
    
    def _create_entity(self, table: str, entity: BaseModel) -> dict:
        data = self._prepare_data(entity)
        columns = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({values}) RETURNING *"
        result = self._execute_single(query, tuple(data.values()))
        if result is None:
            raise Exception(f"Failed to create entity in {table}")
        return result
    
    def _update_entity(self, table: str, entity: BaseModel) -> Optional[dict]:
        data = self._prepare_data(entity)
        id_value = data.pop('id')
        if not data:
            return None
            
        set_clause = ', '.join([f"{k} = %s" for k in data.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE id = %s RETURNING *"
        params = tuple(data.values()) + (id_value,)
        return self._execute_single(query, params)
    
    def _delete_entity(self, table: str, id: UUID) -> bool:
        query = f"DELETE FROM {table} WHERE id = %s"
        try:
            self._execute_query(query, (str(id),))
            return True
        except Exception:
            return False