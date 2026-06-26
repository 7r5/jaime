import { useEffect, useState } from 'react';

function Dashboard({ token }) {
    const [conversations, setConversations] = useState([]);
    const [results, setResults] = useState([]);

    useEffect(() => {
        if (!token) return;
        const fetchData = async () => {
            const convResp = await fetch('/admin/conversations', {
                headers: { Authorization: `Bearer ${token}` },
            });
            const resResp = await fetch('/admin/results', {
                headers: { Authorization: `Bearer ${token}` },
            });
            if (convResp.ok) setConversations(await convResp.json());
            if (resResp.ok) setResults(await resResp.json());
        };
        fetchData();
    }, [token]);

    if (!token) return <p>Necesitas iniciar sesión.</p>;

    return (
        <main>
            <h1>Dashboard</h1>
            <section>
                <h2>Conversaciones</h2>
                <pre>{JSON.stringify(conversations, null, 2)}</pre>
            </section>
            <section>
                <h2>Resultados</h2>
                <pre>{JSON.stringify(results, null, 2)}</pre>
            </section>
        </main>
    );
}

export default Dashboard;
