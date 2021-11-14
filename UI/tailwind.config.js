module.exports = {
  mode: 'jit',
  purge: [
    './src/**/*.{vue,js,ts,jsx,tsx}'
  ],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      screens: {
        'xxs': '190px',
        'xs': '275px',
      },
      colors: {
        gold: {
          400: 'rgb(224, 171, 24)',
          500: 'rgb(197, 132, 11)',
          600: 'rgb(158, 114, 18)',
          700: 'rgb(143, 90, 21)',
        },
        gray: {
          900: 'rgb(28, 28, 31)',
          800: 'rgb(42, 42, 45)',
          700: '#383838',
          600: 'rgb(65, 65, 65)',
          500: 'rgb(78, 78, 78)',
          400: 'rgb(94, 94, 94)',
          300: 'rgb(124, 124, 124)',
          200: '#acacac'
        }
      },
      transitionProperty: {
        'height': 'height',
        'spacing': 'margin, padding',
      }
    },
  },
  variants: {
    
  },
  plugins: [],
}
