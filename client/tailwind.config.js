/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        agent: {
          supervisor: '#a855f7',
          coder: '#3b82f6',
          critic: '#10b981',
          system: '#64748b',
        },
      },
    },
  },
  plugins: [],
};
