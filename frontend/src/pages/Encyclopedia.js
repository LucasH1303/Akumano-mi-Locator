import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import axios from 'axios';
import FruitCard from '../components/FruitCard';
import SearchBar from '../components/SearchBar';
import { BookOpen, Filter } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Encyclopedia = () => {
  const [fruits, setFruits] = useState([]);
  const [filteredFruits, setFilteredFruits] = useState([]);
  const [loading, setLoading] = useState(true);
  const [typeFilter, setTypeFilter] = useState('');
  const [rarityFilter, setRarityFilter] = useState('');
  const [availableFilter, setAvailableFilter] = useState('');
  const [sortBy, setSortBy] = useState('');

  useEffect(() => {
    fetchFruits();
  }, []);

  useEffect(() => {
    applyFilters();
  }, [fruits, typeFilter, rarityFilter, availableFilter, sortBy]);

  const fetchFruits = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API}/fruits`);
      setFruits(response.data);
      setFilteredFruits(response.data);
    } catch (error) {
      console.error('Erro ao carregar frutas:', error);
    }
    setLoading(false);
  };

  const applyFilters = () => {
    let filtered = [...fruits];

    if (typeFilter) {
      filtered = filtered.filter(f => f.type === typeFilter);
    }

    if (rarityFilter) {
      filtered = filtered.filter(f => f.rarity === rarityFilter);
    }

    if (availableFilter === 'available') {
      filtered = filtered.filter(f => f.available === true);
    } else if (availableFilter === 'unavailable') {
      filtered = filtered.filter(f => f.available === false);
    }

    if (sortBy === 'name') {
      filtered.sort((a, b) => a.name.localeCompare(b.name));
    } else if (sortBy === 'price_asc') {
      filtered.sort((a, b) => a.price - b.price);
    } else if (sortBy === 'price_desc') {
      filtered.sort((a, b) => b.price - a.price);
    }

    setFilteredFruits(filtered);
  };

  const handleSearch = (query) => {
    if (!query) {
      setFilteredFruits(fruits);
      return;
    }

    const searchLower = query.toLowerCase();
    const filtered = fruits.filter(
      (fruit) =>
        fruit.name.toLowerCase().includes(searchLower) ||
        fruit.power.toLowerCase().includes(searchLower) ||
        fruit.description.toLowerCase().includes(searchLower) ||
        fruit.keywords.some((k) => k.toLowerCase().includes(searchLower))
    );
    setFilteredFruits(filtered);
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
            <BookOpen className="w-12 h-12 text-brand-gold mr-4" strokeWidth={1.5} />
            <h1 className="heading-pirate text-5xl" data-testid="encyclopedia-title">Enciclopédia</h1>
          </div>
          <p className="text-text-secondary text-center text-lg font-manrope max-w-2xl mx-auto">
            Explore todas as Akuma no Mi conhecidas no universo de One Piece
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="max-w-6xl mx-auto mb-8"
        >
          <div className="bg-background-secondary/80 backdrop-blur-md border border-brand-parchment/20 rounded-2xl p-6">
            <div className="mb-6">
              <SearchBar onSearch={handleSearch} placeholder="Buscar na enciclopédia..." />
            </div>

            <div className="flex items-center space-x-2 mb-4">
              <Filter className="w-4 h-4 text-brand-gold" strokeWidth={1.5} />
              <span className="heading-wanted text-sm">Filtros</span>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div>
                <label className="block text-xs font-cinzel text-text-muted mb-2">Tipo</label>
                <select
                  value={typeFilter}
                  onChange={(e) => setTypeFilter(e.target.value)}
                  className="w-full bg-background-tertiary/50 border border-brand-parchment/30 text-text-primary focus:border-brand-gold focus:ring-1 focus:ring-brand-gold rounded-lg h-10 px-3 text-sm font-manrope transition-all outline-none"
                  data-testid="type-filter"
                >
                  <option value="">Todos</option>
                  <option value="Logia">Logia</option>
                  <option value="Paramecia">Paramecia</option>
                  <option value="Zoan">Zoan</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-cinzel text-text-muted mb-2">Raridade</label>
                <select
                  value={rarityFilter}
                  onChange={(e) => setRarityFilter(e.target.value)}
                  className="w-full bg-background-tertiary/50 border border-brand-parchment/30 text-text-primary focus:border-brand-gold focus:ring-1 focus:ring-brand-gold rounded-lg h-10 px-3 text-sm font-manrope transition-all outline-none"
                  data-testid="rarity-filter"
                >
                  <option value="">Todas</option>
                  <option value="Comum">Comum</option>
                  <option value="Rara">Rara</option>
                  <option value="Muito Rara">Muito Rara</option>
                  <option value="Mítica">Mítica</option>
                  <option value="Única">Única</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-cinzel text-text-muted mb-2">Disponibilidade</label>
                <select
                  value={availableFilter}
                  onChange={(e) => setAvailableFilter(e.target.value)}
                  className="w-full bg-background-tertiary/50 border border-brand-parchment/30 text-text-primary focus:border-brand-gold focus:ring-1 focus:ring-brand-gold rounded-lg h-10 px-3 text-sm font-manrope transition-all outline-none"
                  data-testid="availability-filter"
                >
                  <option value="">Todas</option>
                  <option value="available">Disponíveis</option>
                  <option value="unavailable">Indisponíveis</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-cinzel text-text-muted mb-2">Ordenar por</label>
                <select
                  value={sortBy}
                  onChange={(e) => setSortBy(e.target.value)}
                  className="w-full bg-background-tertiary/50 border border-brand-parchment/30 text-text-primary focus:border-brand-gold focus:ring-1 focus:ring-brand-gold rounded-lg h-10 px-3 text-sm font-manrope transition-all outline-none"
                  data-testid="sort-select"
                >
                  <option value="">Padrão</option>
                  <option value="name">Nome</option>
                  <option value="price_asc">Preço (menor)</option>
                  <option value="price_desc">Preço (maior)</option>
                </select>
              </div>
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
              <BookOpen className="w-12 h-12 text-brand-gold" strokeWidth={1.5} />
            </motion.div>
            <p className="text-text-secondary mt-4 font-manrope">Carregando enciclopédia...</p>
          </div>
        )}

        {!loading && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3 }}
          >
            <div className="mb-6">
              <p className="text-text-muted font-manrope text-center">
                {filteredFruits.length} de {fruits.length} fruta(s)
              </p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6" data-testid="encyclopedia-results">
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

export default Encyclopedia;