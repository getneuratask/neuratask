import { useEffect, useState } from "react";
import { api } from "../utils/api.ts";

export default function HomeView() {
  
  const [users, setUsers] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        setLoading(true);
        setError(null);
        const response = await api.users.getAll();
        setUsers(response.data);
      } catch (err) {
        console.error('Error fetching users:', err);
        setError('Error al cargar los usuarios');
      } finally {
        setLoading(false);
      }
    };

    fetchUsers();
  }, []);

  return (
    <>
      <div className="bg-red-500 text-4xl p-4 text-white">Usuarios desde el back!!</div>
      
      {loading && (
        <div className="mt-4 p-4 text-center">
          <span>Cargando usuarios...</span>
        </div>
      )}
      
      {error && (
        <div className="mt-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
          {error}
        </div>
      )}
      
      {!loading && !error && (
        <ul className="mt-4">
          {users.map((user, idx) => (
            <li key={user.id || idx} className="p-2 border-b">
              {JSON.stringify(user)}
            </li>
          ))}
        </ul>
      )}
    </>
  );
}
