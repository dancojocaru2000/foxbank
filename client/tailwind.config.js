const production = !process.env.ROLLUP_WATCH;
module.exports = {
  purge: {
    content: [
      "./src/**/*.svelte",
    ],
    enabled: production,
  },
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      backgroundImage:{
        "banner":"url('/img/Banner.jpg')"
      },

      fontFamily:{
        "title":['Geo', 'sans-serif'],
        "welcome":['Rochester', 'cursive'],
        "sans":['Roboto', 'sans-serif']
      },

      colors: {
        'regal-blue': '#243c5a',
        'lime-c': '#6DE25ACC',
        'red-c': '#FB6666',
      },

      minWidth: {
        'transaction': '420px',
      },
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
  future: {
    purgeLayersByDefault: true,
    removeDeprecatedGapUtilities: true,
  },
}
