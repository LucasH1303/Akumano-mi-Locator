import React, { useEffect } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import axios from 'axios';
import '@/App.css';
import Home from './pages/Home';
import Encyclopedia from './pages/Encyclopedia';
import FruitDetails from './pages/FruitDetails';
import BlackMarket from './pages/BlackMarket';
import Rankings from './pages/Rankings';
import FightingStyle from './pages/FightingStyle';
import Navbar from './components/Navbar';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function App() {
  useEffect(() => {
    const initDatabase = async () => {
      try {
        await axios.post(`${API}/init-database`);
      } catch (e) {
        console.error('Error initializing database:', e);
      }
    };
    initDatabase();
  }, []);

  return (
    <div className="App min-h-screen bg-background-primary">
      <BrowserRouter>
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/encyclopedia" element={<Encyclopedia />} />
          <Route path="/fruit/:id" element={<FruitDetails />} />
          <Route path="/black-market" element={<BlackMarket />} />
          <Route path="/rankings" element={<Rankings />} />
          <Route path="/fighting-style" element={<FightingStyle />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;