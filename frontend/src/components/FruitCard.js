import React from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { Eye, User, CircleDollarSign } from 'lucide-react';

const FruitCard = ({ fruit }) => {
  const navigate = useNavigate();

  const rarityColors = {
    'Comum': 'text-rarity-common border-rarity-common',
    'Rara': 'text-rarity-rare border-rarity-rare',
    'Muito Rara': 'text-rarity-mythical border-rarity-mythical',
    'Mítica': 'text-rarity-legendary border-rarity-legendary',
    'Única': 'text-rarity-unique border-rarity-unique',
  };

  const formatPrice = (price) => {
    return `₿${(price / 1000000).toFixed(0)}M`;
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      whileHover={{ y: -8 }}
      transition={{ duration: 0.3 }}
      className="group relative"
      data-testid={`fruit-card-${fruit.id}`}
    >
      <div className="relative overflow-hidden bg-gradient-to-b from-background-tertiary to-background-secondary border border-brand-parchment/20 rounded-xl card-glow">
        <div className="absolute top-0 right-0 w-32 h-32 bg-brand-gold/5 rounded-full blur-3xl group-hover:bg-brand-gold/10 transition-all duration-300"></div>
        
        <div className="relative p-4">
          <div className="flex items-start justify-between mb-3">
            <div className="flex-1">
              <h3 className="heading-wanted text-lg mb-1 group-hover:text-brand-gold transition-colors">
                {fruit.name}
              </h3>
              <p className="text-sm text-text-muted font-manrope">{fruit.japanese_name}</p>
            </div>
            <div className={`px-3 py-1 rounded-full border text-xs font-cinzel ${rarityColors[fruit.rarity] || rarityColors['Comum']}`}>
              {fruit.rarity}
            </div>
          </div>

          <div className="aspect-[3/4] w-full mb-4 rounded-lg overflow-hidden bg-background-primary/50">
            <img
              src={fruit.image_url}
              alt={fruit.name}
              className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
              loading="lazy"
            />
          </div>

          <div className="space-y-2 mb-4">
            <div className="flex items-center space-x-2">
              <span className="text-xs font-cinzel text-text-muted uppercase">Tipo:</span>
              <span className="text-sm font-manrope text-brand-ocean font-semibold">{fruit.type}</span>
            </div>
            <div className="flex items-center space-x-2">
              <span className="text-xs font-cinzel text-text-muted uppercase">Poder:</span>
              <span className="text-sm font-manrope text-text-primary">{fruit.power}</span>
            </div>
          </div>

          <div className="border-t border-brand-parchment/20 pt-3 space-y-2">
            {fruit.current_user && (
              <div className="flex items-center space-x-2 text-sm">
                <User className="w-4 h-4 text-brand-crimson" strokeWidth={1.5} />
                <span className="text-text-secondary">Usuário: <span className="text-text-primary font-medium">{fruit.current_user}</span></span>
              </div>
            )}
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <CircleDollarSign className="w-4 h-4 text-brand-gold" strokeWidth={1.5} />
                <span className="text-berry text-lg">{formatPrice(fruit.price)}</span>
              </div>
              {!fruit.available && (
                <span className="text-xs text-brand-crimson font-medium bg-brand-crimson/10 px-2 py-1 rounded">Indisponível</span>
              )}
            </div>
          </div>

          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={() => navigate(`/fruit/${fruit.id}`)}
            className="w-full mt-4 bg-brand-gold text-black font-bold uppercase tracking-wider py-3 rounded-lg hover:bg-brand-goldDim transition-colors flex items-center justify-center space-x-2"
            data-testid={`view-details-${fruit.id}`}
          >
            <Eye className="w-4 h-4" strokeWidth={2} />
            <span>Ver Detalhes</span>
          </motion.button>
        </div>
      </div>
    </motion.div>
  );
};

export default FruitCard;