import { useEffect, useState } from "react";

export default function HomeView() {
  
  const [users, setUsers] = useState<any[]>([]);

  useEffect(() => {
    fetch("http://localhost:8000/api/v1/users")
      .then((res) => res.json())
      .then((data) => setUsers(data))
      .catch((err) => console.error(err));
  }, []);

  return (
    
    <>
      <div className="bg-red-500 text-4xl p-4 text-white">Usuarios desde el back</div>
      <ul className="mt-4">
        {users.map((user, idx) => (
          <li key={user.id || idx} className="p-2 border-b">
            {JSON.stringify(user)}
          </li>
        ))}
      </ul>
    </>
  );
}
