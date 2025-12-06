import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import axios from 'axios';
import FruitCard from '../components/FruitCard';
import { DollarSign, TrendingUp, TrendingDown } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const BlackMarket = () => {
  const [fruits, setFruits] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    fetchMarketData();
  }, []);

  const fetchMarketData = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API}/black-market`);
      setFruits(response.data);
    } catch (error) {
      console.error('Erro ao carregar mercado negro:', error);
    }
    setLoading(false);
  };

  const getFilteredFruits = () => {
    if (filter === 'available') {
      return fruits.filter((f) => f.available);
    } else if (filter === 'unavailable') {
      return fruits.filter((f) => !f.available);
    }
    return fruits;
  };

  const filteredFruits = getFilteredFruits();
  const averagePrice =
    filteredFruits.length > 0
      ? filteredFruits.reduce((sum, f) => sum + f.price, 0) / filteredFruits.length
      : 0;
  const mostExpensive = [...filteredFruits].sort((a, b) => b.price - a.price)[0];
  const cheapest = [...filteredFruits].sort((a, b) => a.price - b.price)[0];

  const formatPrice = (price) => {
    return `฿${(price / 1000000).toFixed(0)}M`;
  };

  return (
    <div className="min-h-screen relative z-10">
      <div className="container mx-auto px-4 py-12">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-12"
        >
          <div className="flex items-center justify-center mb-6">
            <DollarSign className="w-12 h-12 text-brand-gold mr-4" strokeWidth={1.5} />
            <h1 className="heading-pirate text-5xl" data-testid="black-market-title">Mercado Negro</h1>
          </div>
          <p className="text-text-secondary text-center text-lg font-manrope max-w-2xl mx-auto">
            Preços e disponibilidade das Akuma no Mi em circulação
          </p>
        </motion.div>

        {!loading && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12"
          >
            <div className="bg-background-secondary/80 backdrop-blur-md border border-brand-parchment/20 rounded-xl p-6">
              <div className="flex items-center space-x-3 mb-3">
                <TrendingUp className="w-6 h-6 text-brand-gold" strokeWidth={1.5} />
                <span className="heading-wanted text-sm">Preço Médio</span>
              </div>
              <p className="text-berry text-3xl">{formatPrice(averagePrice)}</p>
            </div>

            <div className="bg-background-secondary/80 backdrop-blur-md border border-brand-parchment/20 rounded-xl p-6">
              <div className="flex items-center space-x-3 mb-3">
                <TrendingUp className="w-6 h-6 text-brand-crimson" strokeWidth={1.5} />
                <span className="heading-wanted text-sm">Mais Cara</span>
              </div>
              {mostExpensive && (
                <>
                  <p className="text-text-primary font-manrope text-sm mb-1">{mostExpensive.name}</p>
                  <p className="text-berry text-2xl">{formatPrice(mostExpensive.price)}</p>
                </>
              )}
            </div>

            <div className="bg-background-secondary/80 backdrop-blur-md border border-brand-parchment/20 rounded-xl p-6">
              <div className="flex items-center space-x-3 mb-3">
                <TrendingDown className="w-6 h-6 text-green-500" strokeWidth={1.5} />
                <span className="heading-wanted text-sm">Mais Barata</span>
              </div>
              {cheapest && (
                <>
                  <p className="text-text-primary font-manrope text-sm mb-1">{cheapest.name}</p>
                  <p className="text-berry text-2xl">{formatPrice(cheapest.price)}</p>
                </>
              )}
            </div>
          </motion.div>
        )}

        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
          className="mb-8"
        >
          <div className="flex items-center justify-center space-x-4">
            <button
              onClick={() => setFilter('all')}
              className={`px-6 py-2 rounded-lg font-cinzel text-sm transition-colors ${
                filter === 'all'
                  ? 'bg-brand-gold text-black'
                  : 'bg-background-secondary/80 text-text-secondary hover:text-brand-gold border border-brand-parchment/20'
              }`}
              data-testid="filter-all"
            >
              Todas
            </button>
            <button
              onClick={() => setFilter('available')}
              className={`px-6 py-2 rounded-lg font-cinzel text-sm transition-colors ${
                filter === 'available'
                  ? 'bg-brand-gold text-black'
                  : 'bg-background-secondary/80 text-text-secondary hover:text-brand-gold border border-brand-parchment/20'
              }`}
              data-testid="filter-available"
            >
              Disponíveis
            </button>
            <button
              onClick={() => setFilter('unavailable')}
              className={`px-6 py-2 rounded-lg font-cinzel text-sm transition-colors ${
                filter === 'unavailable'
                  ? 'bg-brand-gold text-black'
                  : 'bg-background-secondary/80 text-text-secondary hover:text-brand-gold border border-brand-parchment/20'
              }`}
              data-testid="filter-unavailable"
            >
              Indisponíveis
            </button>
          </div>
        </motion.div>

        {loading && (
          <div className="text-center py-12">
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
              className="inline-block"
            >
              <DollarSign className="w-12 h-12 text-brand-gold" strokeWidth={1.5} />
            </motion.div>
            <p className="text-text-secondary mt-4 font-manrope">Carregando mercado...</p>
          </div>
        )}

        {!loading && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.4 }}
          >
            <div className="mb-6">
              <p className="text-text-muted font-manrope text-center">{filteredFruits.length} fruta(s) no mercado</p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6" data-testid="market-results">
              {filteredFruits.map((fruit) => (
                <FruitCard key={fruit.id} fruit={fruit} />
              ))}
            </div>
          </motion.div>
        )}
      </div>
    </div>
  );
};

export default BlackMarket;