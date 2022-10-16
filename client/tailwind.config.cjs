/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        agradient: '#9769FA',
        bgradient: '#8C3494',
      }
    }
  },
  plugins: [],
}
