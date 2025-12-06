import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import axios from 'axios';
import FruitCard from '../components/FruitCard';
import { Trophy, Zap, Shield, DollarSign, Sparkles } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Rankings = () => {
  const [activeRanking, setActiveRanking] = useState('expensive');
  const [fruits, setFruits] = useState([]);
  const [loading, setLoading] = useState(false);

  const rankings = [
    { id: 'expensive', label: 'Mais Caras', icon: DollarSign, endpoint: '/rankings/expensive' },
    { id: 'destructive', label: 'Mais Destrutivas', icon: Zap, endpoint: '/rankings/destructive' },
    { id: 'rare', label: 'Mais Raras', icon: Sparkles, endpoint: '/rankings/rare' },
    { id: 'defense', label: 'Melhor Defesa', icon: Shield, endpoint: '/rankings/defense' },
    { id: 'speed', label: 'Maior Velocidade', icon: Zap, endpoint: '/rankings/speed' },
  ];

  useEffect(() => {
    fetchRanking(activeRanking);
  }, [activeRanking]);

  const fetchRanking = async (rankingId) => {
    setLoading(true);
    const ranking = rankings.find((r) => r.id === rankingId);
    if (!ranking) return;

    try {
      const response = await axios.get(`${API}${ranking.endpoint}`);
      setFruits(response.data);
    } catch (error) {
      console.error('Erro ao carregar ranking:', error);
    }
    setLoading(false);
  };

  const getMedalColor = (index) => {
    if (index === 0) return 'text-yellow-400';
    if (index === 1) return 'text-gray-300';
    if (index === 2) return 'text-orange-400';
    return 'text-text-muted';
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
            <Trophy className="w-12 h-12 text-brand-gold mr-4" strokeWidth={1.5} />
            <h1 className="heading-pirate text-5xl" data-testid="rankings-title">Rankings Top 10</h1>
          </div>
          <p className="text-text-secondary text-center text-lg font-manrope max-w-2xl mx-auto">
            As melhores Akuma no Mi em diferentes categorias
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="mb-12"
        >
          <div className="bg-background-secondary/80 backdrop-blur-md border border-brand-parchment/20 rounded-2xl p-4">
            <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
              {rankings.map((ranking) => {
                const Icon = ranking.icon;
                return (
                  <motion.button
                    key={ranking.id}
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={() => setActiveRanking(ranking.id)}
                    className={`flex flex-col items-center space-y-2 p-4 rounded-xl transition-all ${
                      activeRanking === ranking.id
                        ? 'bg-brand-gold text-black'
                        : 'bg-background-tertiary/50 text-text-secondary hover:text-brand-gold'
                    }`}
                    data-testid={`ranking-${ranking.id}`}
                  >
                    <Icon className="w-6 h-6" strokeWidth={1.5} />
                    <span className="font-cinzel text-xs text-center">{ranking.label}</span>
                  </motion.button>
                );
              })}
            </div>
          </div>
        </motion.div>

        {loading && (
          <div className="text-center py-12">
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
              className="inline-block"
            >
              <Trophy className="w-12 h-12 text-brand-gold" strokeWidth={1.5} />
            </motion.div>
            <p className="text-text-secondary mt-4 font-manrope">Carregando ranking...</p>
          </div>
        )}

        {!loading && fruits.length > 0 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3 }}
          >
            <div className="mb-8">
              <h2 className="heading-wanted text-2xl text-center mb-2">
                {rankings.find((r) => r.id === activeRanking)?.label}
              </h2>
              <p className="text-text-muted text-center font-manrope">Top 10</p>
            </div>

            <div className="space-y-6" data-testid="ranking-results">
              {fruits.map((fruit, index) => (
                <motion.div
                  key={fruit.id}
                  initial={{ opacity: 0, x: -50 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="relative"
                >
                  <div className="absolute -left-12 top-1/2 -translate-y-1/2 hidden lg:flex items-center justify-center">
                    <div className={`text-4xl font-bold ${getMedalColor(index)}`}>
                      #{index + 1}
                    </div>
                  </div>
                  <div className="lg:ml-8">
                    <div className="bg-background-secondary/80 backdrop-blur-md border border-brand-parchment/20 rounded-xl p-4 hover:border-brand-gold transition-all">
                      <div className="flex items-center space-x-6">
                        <div className="lg:hidden flex items-center justify-center w-12 h-12 rounded-full bg-background-tertiary">
                          <span className={`text-xl font-bold ${getMedalColor(index)}`}>#{index + 1}</span>
                        </div>
                        <div className="w-20 h-20 rounded-lg overflow-hidden bg-background-primary/50 flex-shrink-0">
                          <img
                            src={fruit.image_url}
                            alt={fruit.name}
                            className="w-full h-full object-cover"
                            loading="lazy"
                          />
                        </div>
                        <div className="flex-1">
                          <h3 className="heading-wanted text-lg mb-1">{fruit.name}</h3>
                          <p className="text-text-muted text-sm font-manrope">{fruit.type} - {fruit.power}</p>
                        </div>
                        <div className="text-right">
                          <p className="text-berry text-xl">฿{(fruit.price / 1000000).toFixed(0)}M</p>
                          {fruit.current_user && (
                            <p className="text-text-muted text-xs mt-1">{fruit.current_user}</p>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          </motion.div>
        )}
      </div>
    </div>
  );
};

export default Rankings;