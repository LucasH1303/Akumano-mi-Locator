import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Anchor, BookOpen, TrendingUp, DollarSign, Swords } from 'lucide-react';

const Navbar = () => {
  const location = useLocation();

  const navItems = [
    { path: '/', label: 'Busca', icon: Anchor },
    { path: '/encyclopedia', label: 'Enciclopédia', icon: BookOpen },
    { path: '/black-market', label: 'Mercado Negro', icon: DollarSign },
    { path: '/rankings', label: 'Rankings', icon: TrendingUp },
    { path: '/fighting-style', label: 'Estilo de Luta', icon: Swords },
  ];

  return (
    <nav className="sticky top-0 z-50 bg-background-secondary/95 backdrop-blur-md border-b border-brand-parchment/20">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-20">
          <Link to="/" className="flex items-center space-x-3" data-testid="navbar-logo">
            <Anchor className="w-8 h-8 text-brand-gold" strokeWidth={1.5} />
            <span className="heading-pirate text-2xl">Akuma Finder</span>
          </Link>

          <div className="hidden md:flex items-center space-x-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = location.pathname === item.path;
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  data-testid={`nav-link-${item.label.toLowerCase().replace(' ', '-')}`}
                >
                  <motion.div
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors ${
                      isActive
                        ? 'bg-brand-gold/20 text-brand-gold'
                        : 'text-text-secondary hover:text-brand-gold hover:bg-brand-gold/10'
                    }`}
                  >
                    <Icon className="w-4 h-4" strokeWidth={1.5} />
                    <span className="font-manrope font-medium">{item.label}</span>
                  </motion.div>
                </Link>
              );
            })}
          </div>

          <div className="md:hidden flex space-x-2">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = location.pathname === item.path;
              return (
                <Link key={item.path} to={item.path} data-testid={`mobile-nav-${item.label.toLowerCase().replace(' ', '-')}`}>
                  <motion.div
                    whileTap={{ scale: 0.9 }}
                    className={`p-2 rounded-lg ${
                      isActive ? 'bg-brand-gold/20 text-brand-gold' : 'text-text-secondary'
                    }`}
                  >
                    <Icon className="w-5 h-5" strokeWidth={1.5} />
                  </motion.div>
                </Link>
              );
            })}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;