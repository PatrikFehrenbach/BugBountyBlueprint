module.exports = {
  purge: ['./src/**/*.vue'],
  // ... rest of the config
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {},
  },
  variants: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/typography'),

  ],
}
