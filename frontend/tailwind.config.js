/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: '#1d4ed8',
        secondary: '#3b82f6',
      },
    },
  },
  plugins: [],
}
