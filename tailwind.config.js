module.exports = {
  content: [
    "./python/templates/*.{html,js}"
  ],
  theme: {
    fontFamily: {
      sans: ["Helvetica Neue",
        'Arial',
        "Hiragino Kaku Gothic ProN",
        "Hiragino Sans",
        'Meiryo',
        'ui-sans-serif']
    },
    extend: {
      animation: {
        'bounce-slow': 'bounce 1.6s ease-in-out infinite',
      }
    },
  },
  plugins: [],
}
