import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import axios from 'axios';
import {
  ArrowLeft,
  User,
  MapPin,
  Sparkles,
  Shield,
  Zap,
  Target,
  CircleDollarSign,
  Info,
} from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const FruitDetails = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [fruit, setFruit] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchFruitDetails();
  }, [id]);

  const fetchFruitDetails = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API}/fruits/${id}`);
      setFruit(response.data);
    } catch (error) {
      console.error('Erro ao carregar detalhes:', error);
    }
    setLoading(false);
  };

  const rarityColors = {
    'Comum': 'text-rarity-common',
    'Rara': 'text-rarity-rare',
    'Muito Rara': 'text-rarity-mythical',
    'Mítica': 'text-rarity-legendary',
    'Única': 'text-rarity-unique',
  };

  const formatPrice = (price) => {
    return `฿${(price / 1000000).toFixed(0)}M`;
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
        >
          <Sparkles className="w-12 h-12 text-brand-gold" strokeWidth={1.5} />
        </motion.div>
      </div>
    );
  }

  if (!fruit) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="heading-wanted text-2xl mb-4">Fruta não encontrada</h2>
          <button
            onClick={() => navigate('/')}
            className="bg-brand-gold text-black px-6 py-3 rounded-lg font-bold"
          >
            Voltar
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen relative z-10">
      <div className="container mx-auto px-4 py-12">
        <motion.button
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          whileHover={{ x: -5 }}
          onClick={() => navigate(-1)}
          className="flex items-center space-x-2 text-text-secondary hover:text-brand-gold transition-colors mb-8"
          data-testid="back-button"
        >
          <ArrowLeft className="w-5 h-5" strokeWidth={1.5} />
          <span className="font-manrope font-medium">Voltar</span>
        </motion.button>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <motion.div
            initial={{ opacity: 0, x: -50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5 }}
          >
            <div className="bg-background-secondary/80 backdrop-blur-md border border-brand-parchment/20 rounded-2xl overflow-hidden">
              <div className="aspect-square w-full bg-background-primary/50">
                <img
                  src={fruit.image_url}
                  alt={fruit.name}
                  className="w-full h-full object-cover"
                  data-testid="fruit-image"
                />
              </div>
              <div className="p-6">
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <h1 className="heading-pirate text-3xl mb-2" data-testid="fruit-name">{fruit.name}</h1>
                    <p className="text-text-muted font-manrope">{fruit.japanese_name}</p>
                  </div>
                  <div className={`px-4 py-2 rounded-full border ${rarityColors[fruit.rarity]} font-cinzel text-sm`}>
                    {fruit.rarity}
                  </div>
                </div>

                <div className="space-y-3">
                  <div className="flex items-center justify-between py-3 border-b border-brand-parchment/20">
                    <span className="text-text-muted font-cinzel text-sm uppercase">Tipo</span>
                    <span className="text-brand-ocean font-bold font-manrope">{fruit.type}</span>
                  </div>
                  <div className="flex items-center justify-between py-3 border-b border-brand-parchment/20">
                    <span className="text-text-muted font-cinzel text-sm uppercase">Poder</span>
                    <span className="text-text-primary font-manrope">{fruit.power}</span>
                  </div>
                  <div className="flex items-center justify-between py-3 border-b border-brand-parchment/20">
                    <span className="text-text-muted font-cinzel text-sm uppercase">Preço</span>
                    <span className="text-berry text-2xl">{formatPrice(fruit.price)}</span>
                  </div>
                  <div className="flex items-center justify-between py-3">
                    <span className="text-text-muted font-cinzel text-sm uppercase">Status</span>
                    <span className={`font-bold ${fruit.available ? 'text-green-500' : 'text-brand-crimson'}`}>
                      {fruit.available ? 'Disponível' : 'Indisponível'}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="space-y-6"
          >
            <div className="bg-background-secondary/80 backdrop-blur-md border border-brand-parchment/20 rounded-2xl p-6">
              <div className="flex items-center space-x-2 mb-4">
                <Info className="w-5 h-5 text-brand-gold" strokeWidth={1.5} />
                <h2 className="heading-wanted text-xl">Descrição</h2>
              </div>
              <p className="text-text-secondary font-manrope leading-relaxed">{fruit.description}</p>
            </div>

            {fruit.current_user && (
              <div className="bg-background-secondary/80 backdrop-blur-md border border-brand-parchment/20 rounded-2xl p-6">
                <div className="flex items-center space-x-2 mb-4">
                  <User className="w-5 h-5 text-brand-gold" strokeWidth={1.5} />
                  <h2 className="heading-wanted text-xl">Usuário Atual</h2>
                </div>
                <p className="text-brand-gold font-bold text-lg font-manrope">{fruit.current_user}</p>
                {fruit.previous_users && fruit.previous_users.length > 0 && (
                  <div className="mt-4">
                    <p className="text-text-muted text-sm mb-2">Usuários Anteriores:</p>
                    <ul className="space-y-1">
                      {fruit.previous_users.map((user, idx) => (
                        <li key={idx} className="text-text-secondary font-manrope text-sm">
                          • {user}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}

            <div className="bg-background-secondary/80 backdrop-blur-md border border-brand-parchment/20 rounded-2xl p-6">
              <div className="flex items-center space-x-2 mb-4">
                <Target className="w-5 h-5 text-brand-gold" strokeWidth={1.5} />
                <h2 className="heading-wanted text-xl">Estatísticas</h2>
              </div>
              <div className="space-y-4">
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center space-x-2">
                      <Zap className="w-4 h-4 text-brand-crimson" strokeWidth={1.5} />
                      <span className="text-text-muted text-sm font-cinzel">Poder Destrutivo</span>
                    </div>
                    <span className="text-text-primary font-bold">{fruit.destructive_power}/100</span>
                  </div>
                  <div className="h-2 bg-background-tertiary rounded-full overflow-hidden">
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ width: `${fruit.destructive_power}%` }}
                      transition={{ duration: 1, delay: 0.5 }}
                      className="h-full bg-brand-crimson"
                    />
                  </div>
                </div>

                <div>
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center space-x-2">
                      <Shield className="w-4 h-4 text-brand-ocean" strokeWidth={1.5} />
                      <span className="text-text-muted text-sm font-cinzel">Defesa</span>
                    </div>
                    <span className="text-text-primary font-bold">{fruit.defense_rating}/100</span>
                  </div>
                  <div className="h-2 bg-background-tertiary rounded-full overflow-hidden">
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ width: `${fruit.defense_rating}%` }}
                      transition={{ duration: 1, delay: 0.7 }}
                      className="h-full bg-brand-ocean"
                    />
                  </div>
                </div>

                <div>
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center space-x-2">
                      <Zap className="w-4 h-4 text-brand-gold" strokeWidth={1.5} />
                      <span className="text-text-muted text-sm font-cinzel">Velocidade</span>
                    </div>
                    <span className="text-text-primary font-bold">{fruit.speed_rating}/100</span>
                  </div>
                  <div className="h-2 bg-background-tertiary rounded-full overflow-hidden">
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ width: `${fruit.speed_rating}%` }}
                      transition={{ duration: 1, delay: 0.9 }}
                      className="h-full bg-brand-gold"
                    />
                  </div>
                </div>
              </div>
            </div>

            {fruit.locations && fruit.locations.length > 0 && (
              <div className="bg-background-secondary/80 backdrop-blur-md border border-brand-parchment/20 rounded-2xl p-6">
                <div className="flex items-center space-x-2 mb-4">
                  <MapPin className="w-5 h-5 text-brand-gold" strokeWidth={1.5} />
                  <h2 className="heading-wanted text-xl">Localizações</h2>
                </div>
                <ul className="space-y-2">
                  {fruit.locations.map((location, idx) => (
                    <li key={idx} className="text-text-secondary font-manrope">
                      • {location}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {fruit.lore && (
              <div className="bg-background-secondary/80 backdrop-blur-md border border-brand-parchment/20 rounded-2xl p-6">
                <div className="flex items-center space-x-2 mb-4">
                  <Sparkles className="w-5 h-5 text-brand-gold" strokeWidth={1.5} />
                  <h2 className="heading-wanted text-xl">Lore</h2>
                </div>
                <p className="text-text-secondary font-manrope leading-relaxed italic">{fruit.lore}</p>
              </div>
            )}

            {fruit.curiosities && fruit.curiosities.length > 0 && (
              <div className="bg-background-secondary/80 backdrop-blur-md border border-brand-parchment/20 rounded-2xl p-6">
                <div className="flex items-center space-x-2 mb-4">
                  <Sparkles className="w-5 h-5 text-brand-gold" strokeWidth={1.5} />
                  <h2 className="heading-wanted text-xl">Curiosidades</h2>
                </div>
                <ul className="space-y-3">
                  {fruit.curiosities.map((curiosity, idx) => (
                    <li key={idx} className="flex items-start space-x-3">
                      <span className="text-brand-gold mt-1">•</span>
                      <span className="text-text-secondary font-manrope text-sm">{curiosity}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {fruit.first_appearance && (
              <div className="bg-background-secondary/80 backdrop-blur-md border border-brand-parchment/20 rounded-2xl p-6">
                <h3 className="text-text-muted text-sm font-cinzel mb-2">Primeira Aparição</h3>
                <p className="text-text-primary font-manrope">{fruit.first_appearance}</p>
              </div>
            )}
          </motion.div>
        </div>
      </div>
    </div>
  );
};

export default FruitDetails;