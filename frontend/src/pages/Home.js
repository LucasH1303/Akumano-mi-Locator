import React, { useState } from 'react';
import { motion } from 'framer-motion';
import axios from 'axios';
import SearchBar from '../components/SearchBar';
import FruitCard from '../components/FruitCard';
import { Sparkles, DollarSign, Filter } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Home = () => {
  const [fruits, setFruits] = useState([]);
  const [loading, setLoading] = useState(false);
  const [budget, setBudget] = useState('');
  const [fruitType, setFruitType] = useState('');
  const [rarity, setRarity] = useState('');

  const handleSearch = async (query) => {
    setLoading(true);
    try {
      const response = await axios.post(`${API}/search`, {
        description: query || undefined,
        budget: budget ? parseInt(budget) : undefined,
        fruit_type: fruitType || undefined,
        rarity: rarity || undefined,
      });
      setFruits(response.data);
    } catch (error) {
      console.error('Erro na busca:', error);
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen relative z-10">
      <div className="container mx-auto px-4 py-12">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center mb-12"
        >
          <motion.div
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ duration: 0.5 }}
            className="inline-block mb-4"
          >
            <Sparkles className="w-16 h-16 text-brand-gold mx-auto" strokeWidth={1.5} />
          </motion.div>
          <h1 className="heading-pirate text-5xl md:text-7xl mb-6" data-testid="home-title">
            Akuma Finder
          </h1>
          <p className="text-text-secondary text-lg md:text-xl font-manrope max-w-2xl mx-auto">
            Encontre a Akuma no Mi perfeita baseada no seu orçamento, tipo desejado e poderes
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="max-w-4xl mx-auto mb-12"
        >
          <div className="bg-background-secondary/80 backdrop-blur-md border border-brand-parchment/20 rounded-2xl p-8">
            <div className="mb-6">
              <SearchBar onSearch={handleSearch} placeholder="Buscar por poder (ex: fogo, gelo, elástico)..." />
            </div>

            <div className="flex items-center space-x-2 mb-4">
              <Filter className="w-4 h-4 text-brand-gold" strokeWidth={1.5} />
              <span className="heading-wanted text-sm">Filtros Avançados</span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-cinzel text-text-muted mb-2">Orçamento (Berries)</label>
                <div className="relative">
                  <DollarSign className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-brand-gold" strokeWidth={1.5} />
                  <input
                    type="number"
                    value={budget}
                    onChange={(e) => setBudget(e.target.value)}
                    placeholder="Ex: 1000000000"
                    className="w-full bg-background-tertiary/50 border border-brand-parchment/30 text-text-primary placeholder:text-text-muted focus:border-brand-gold focus:ring-1 focus:ring-brand-gold rounded-lg h-12 pl-10 pr-4 font-mono transition-all outline-none"
                    data-testid="budget-input"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-cinzel text-text-muted mb-2">Tipo</label>
                <select
                  value={fruitType}
                  onChange={(e) => setFruitType(e.target.value)}
                  className="w-full bg-background-tertiary/50 border border-brand-parchment/30 text-text-primary focus:border-brand-gold focus:ring-1 focus:ring-brand-gold rounded-lg h-12 px-4 font-manrope transition-all outline-none"
                  data-testid="type-select"
                >
                  <option value="">Todos</option>
                  <option value="Logia">Logia</option>
                  <option value="Paramecia">Paramecia</option>
                  <option value="Zoan">Zoan</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-cinzel text-text-muted mb-2">Raridade</label>
                <select
                  value={rarity}
                  onChange={(e) => setRarity(e.target.value)}
                  className="w-full bg-background-tertiary/50 border border-brand-parchment/30 text-text-primary focus:border-brand-gold focus:ring-1 focus:ring-brand-gold rounded-lg h-12 px-4 font-manrope transition-all outline-none"
                  data-testid="rarity-select"
                >
                  <option value="">Todas</option>
                  <option value="Comum">Comum</option>
                  <option value="Rara">Rara</option>
                  <option value="Muito Rara">Muito Rara</option>
                  <option value="Mítica">Mítica</option>
                  <option value="Única">Única</option>
                </select>
              </div>
            </div>
          </div>
        </motion.div>

        {loading && (
          <div className="text-center py-12" data-testid="loading-indicator">
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
              className="inline-block"
            >
              <Sparkles className="w-12 h-12 text-brand-gold" strokeWidth={1.5} />
            </motion.div>
            <p className="text-text-secondary mt-4 font-manrope">Procurando frutas...</p>
          </div>
        )}

        {!loading && fruits.length > 0 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5 }}
          >
            <div className="mb-6">
              <h2 className="heading-wanted text-2xl mb-2">Resultados da Busca</h2>
              <p className="text-text-muted font-manrope">{fruits.length} fruta(s) encontrada(s)</p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6" data-testid="search-results">
              {fruits.map((fruit) => (
                <FruitCard key={fruit.id} fruit={fruit} />
              ))}
            </div>
          </motion.div>
        )}

        {!loading && fruits.length === 0 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-center py-16"
          >
            <div className="bg-background-secondary/50 border border-brand-parchment/20 rounded-2xl p-12 max-w-md mx-auto">
              <Sparkles className="w-16 h-16 text-brand-gold/50 mx-auto mb-4" strokeWidth={1.5} />
              <h3 className="heading-wanted text-xl mb-2">Comece sua busca!</h3>
              <p className="text-text-muted font-manrope">
                Use os filtros acima para encontrar a Akuma no Mi perfeita para você
              </p>
            </div>
          </motion.div>
        )}
      </div>
    </div>
  );
};

export default Home;