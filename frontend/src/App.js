import { Routes, Route, useNavigate } from 'react-router-dom';
import { useState } from 'react';
import Login from './Login';
import Dashboard from './Dashboard';

function App() {
    const [token, setToken] = useState(null);
    const navigate = useNavigate();

    return (
        <Routes>
            <Route path="/" element={<Login onLogin={(t) => { setToken(t); navigate('/dashboard'); }} />} />
            <Route path="/dashboard" element={<Dashboard token={token} />} />
        </Routes>
    );
}

export default App;
