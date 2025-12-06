import React, { useState } from 'react';
import { motion } from 'framer-motion';
import axios from 'axios';
import FruitCard from '../components/FruitCard';
import { Swords, Target, Shield, Zap, Wind, Flame } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const FightingStyle = () => {
  const [fruits, setFruits] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedStyle, setSelectedStyle] = useState(null);

  const fightingStyles = [
    { id: 'range', label: 'Luta de longe', icon: Target, keyword: 'Luta de longe' },
    { id: 'mobility', label: 'Melhor mobilidade', icon: Wind, keyword: 'Melhor mobilidade' },
    { id: 'defense', label: 'Alta defesa', icon: Shield, keyword: 'Alta defesa' },
    { id: 'speed', label: 'Velocidade', icon: Zap, keyword: 'Velocidade' },
    { id: 'elemental', label: 'Controle elemental', icon: Flame, keyword: 'Controle elemental' },
    { id: 'brute', label: 'Combate bruto', icon: Swords, keyword: 'Combate bruto' },
  ];

  const handleStyleSelect = async (style) => {
    setSelectedStyle(style.id);
    setLoading(true);
    
    try {
      const response = await axios.post(`${API}/search`, {
        fighting_style: style.keyword,
      });
      setFruits(response.data);
    } catch (error) {
      console.error('Erro na busca por estilo:', error);
    }
    
    setLoading(false);
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
            <Swords className="w-12 h-12 text-brand-gold mr-4" strokeWidth={1.5} />
            <h1 className="heading-pirate text-5xl" data-testid="fighting-style-title">Estilo de Luta</h1>
          </div>
          <p className="text-text-secondary text-center text-lg font-manrope max-w-2xl mx-auto">
            Encontre a Akuma no Mi perfeita baseada no seu estilo de combate preferido
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="max-w-4xl mx-auto mb-12"
        >
          <div className="bg-background-secondary/80 backdrop-blur-md border border-brand-parchment/20 rounded-2xl p-8">
            <h2 className="heading-wanted text-xl mb-6 text-center">Escolha seu estilo de luta</h2>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
              {fightingStyles.map((style) => {
                const Icon = style.icon;
                return (
                  <motion.button
                    key={style.id}
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={() => handleStyleSelect(style)}
                    className={`flex flex-col items-center space-y-3 p-6 rounded-xl border-2 transition-all ${
                      selectedStyle === style.id
                        ? 'border-brand-gold bg-brand-gold/10'
                        : 'border-brand-parchment/20 bg-background-tertiary/50 hover:border-brand-gold/50'
                    }`}
                    data-testid={`style-${style.id}`}
                  >
                    <Icon
                      className={`w-10 h-10 ${
                        selectedStyle === style.id ? 'text-brand-gold' : 'text-text-secondary'
                      }`}
                      strokeWidth={1.5}
                    />
                    <span
                      className={`font-cinzel text-sm text-center ${
                        selectedStyle === style.id ? 'text-brand-gold' : 'text-text-secondary'
                      }`}
                    >
                      {style.label}
                    </span>
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
              <Swords className="w-12 h-12 text-brand-gold" strokeWidth={1.5} />
            </motion.div>
            <p className="text-text-secondary mt-4 font-manrope">Buscando frutas compatíveis...</p>
          </div>
        )}

        {!loading && fruits.length > 0 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5 }}
          >
            <div className="mb-6">
              <h2 className="heading-wanted text-2xl mb-2 text-center">Frutas Recomendadas</h2>
              <p className="text-text-muted font-manrope text-center">
                {fruits.length} fruta(s) compatível(is) com seu estilo
              </p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6" data-testid="style-results">
              {fruits.map((fruit) => (
                <FruitCard key={fruit.id} fruit={fruit} />
              ))}
            </div>
          </motion.div>
        )}

        {!loading && selectedStyle && fruits.length === 0 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-center py-16"
          >
            <div className="bg-background-secondary/50 border border-brand-parchment/20 rounded-2xl p-12 max-w-md mx-auto">
              <Swords className="w-16 h-16 text-brand-gold/50 mx-auto mb-4" strokeWidth={1.5} />
              <h3 className="heading-wanted text-xl mb-2">Nenhuma fruta encontrada</h3>
              <p className="text-text-muted font-manrope">
                Tente selecionar outro estilo de luta
              </p>
            </div>
          </motion.div>
        )}

        {!selectedStyle && !loading && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-center py-16"
          >
            <div className="bg-background-secondary/50 border border-brand-parchment/20 rounded-2xl p-12 max-w-md mx-auto">
              <Swords className="w-16 h-16 text-brand-gold/50 mx-auto mb-4" strokeWidth={1.5} />
              <h3 className="heading-wanted text-xl mb-2">Selecione um estilo</h3>
              <p className="text-text-muted font-manrope">
                Escolha seu estilo de luta preferido acima para ver as frutas recomendadas
              </p>
            </div>
          </motion.div>
        )}
      </div>
    </div>
  );
};

export default FightingStyle;
