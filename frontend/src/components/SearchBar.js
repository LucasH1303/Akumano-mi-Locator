import React, { useState } from 'react';
import { Search } from 'lucide-react';
import { motion } from 'framer-motion';

const SearchBar = ({ onSearch, placeholder = 'Buscar por poder, descrição...' }) => {
  const [query, setQuery] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(query);
  };

  return (
    <form onSubmit={handleSubmit} className="w-full" data-testid="search-form">
      <div className="relative">
        <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-text-muted" strokeWidth={1.5} />
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder={placeholder}
          className="w-full bg-background-tertiary/50 border border-brand-parchment/30 text-text-primary placeholder:text-text-muted focus:border-brand-gold focus:ring-1 focus:ring-brand-gold rounded-lg h-14 pl-12 pr-4 font-manrope transition-all outline-none"
          data-testid="search-input"
        />
        <motion.button
          type="submit"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          className="absolute right-2 top-1/2 -translate-y-1/2 bg-brand-gold text-black px-6 py-2 rounded-lg font-bold uppercase text-sm hover:bg-brand-goldDim transition-colors"
          data-testid="search-button"
        >
          Buscar
        </motion.button>
      </div>
    </form>
  );
};

export default SearchBar;