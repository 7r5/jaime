import { useState } from 'react';

function Login({ onLogin }) {
    const [username, setUsername] = useState('admin');
    const [password, setPassword] = useState('');
    const [error, setError] = useState(null);

    const handleSubmit = async (event) => {
        event.preventDefault();
        const response = await fetch('/auth/token', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: new URLSearchParams({ username, password }),
        });
        if (response.ok) {
            const data = await response.json();
            onLogin(data.access_token);
        } else {
            setError('Usuario o contraseña incorrecta');
        }
    };

    return (
        <main>
            <h1>Login</h1>
            <form onSubmit={handleSubmit}>
                <label>
                    Usuario
                    <input value={username} onChange={(e) => setUsername(e.target.value)} />
                </label>
                <label>
                    Contraseña
                    <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
                </label>
                <button type="submit">Ingresar</button>
            </form>
            {error && <p>{error}</p>}
        </main>
    );
}

export default Login;
