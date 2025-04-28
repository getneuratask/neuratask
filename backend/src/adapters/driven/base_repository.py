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
    
    def _execute_query(self, query: str, params: tuple = None) -> List[dict]:
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, params)
                if cur.description:
                    return cur.fetchall()
                return []
    
    def _execute_single(self, query: str, params: tuple = None) -> Optional[dict]:
        results = self._execute_query(query, params)
        return results[0] if results else None
    
    def _create_entity(self, table: str, entity: BaseModel) -> dict:
        data = entity.model_dump()
        columns = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({values}) RETURNING *"
        return self._execute_single(query, tuple(data.values()))
    
    def _update_entity(self, table: str, entity: BaseModel) -> Optional[dict]:
        data = entity.model_dump()
        id_value = data.pop('id')
        if not data:
            return None
            
        set_clause = ', '.join([f"{k} = %s" for k in data.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE id = %s RETURNING *"
        params = tuple(data.values()) + (id_value,)
        return self._execute_single(query, params)
    
    def _delete_entity(self, table: str, id: UUID) -> bool:
        query = f"DELETE FROM {table} WHERE id = %s"
        self._execute_query(query, (str(id),))
        return True