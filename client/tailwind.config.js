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
      }
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
