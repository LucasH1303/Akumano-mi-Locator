const { fontFamily } = require("tailwindcss/defaultTheme");

module.exports = {
  darkMode: "class",
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html",
  ],
  theme: {
    extend: {
      colors: {
        background: {
          primary: "#050b14",
          secondary: "#0f172a",
          tertiary: "#1e293b",
        },
        text: {
          primary: "#e2e8f0",
          secondary: "#94a3b8",
          muted: "#64748b",
          accent: "#ffd700",
        },
        brand: {
          gold: "#FFD700",
          goldDim: "#C5A000",
          crimson: "#DC143C",
          ocean: "#0ea5e9",
          parchment: "#d4c5a3",
        },
        rarity: {
          common: "#94a3b8",
          rare: "#3b82f6",
          mythical: "#a855f7",
          legendary: "#FFD700",
          unique: "#DC143C",
        },
      },
      fontFamily: {
        rye: ['Rye', ...fontFamily.serif],
        cinzel: ['Cinzel', ...fontFamily.serif],
        manrope: ['Manrope', ...fontFamily.sans],
        mono: ['Space Mono', ...fontFamily.mono],
      },
      backgroundImage: {
        'gold-rush': 'linear-gradient(135deg, #FFD700 0%, #C5A000 100%)',
        'deep-sea': 'linear-gradient(to bottom, #050b14, #0f172a)',
        'wanted-poster': 'linear-gradient(to bottom right, #fef3c7, #d4c5a3)',
      },
      animation: {
        'glow-pulse': 'glow-pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
      keyframes: {
        'glow-pulse': {
          '0%, 100%': {
            boxShadow: '0 0 15px rgba(255, 215, 0, 0.3)',
          },
          '50%': {
            boxShadow: '0 0 30px rgba(255, 215, 0, 0.5)',
          },
        },
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
};