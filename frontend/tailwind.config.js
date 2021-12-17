module.exports = {
  mode: 'jit',
  content: ['./src/**/*.{html,ts}', './projects/**/*.{html,ts}'],
     // These paths are just examples, customize them to match your project structure
  purge:  ['./src/**/*.{html,ts}', './projects/**/*.{html,ts}'],

  darkMode: 'class',
  theme: {
    fontFamily: {
      display: ['Oswald', 'sans-serif'],
      body: ['Poppins', 'sans-serif'],
    },
    container: {
      center: true,
      padding: '1.5rem',

    },
    extend: {
      colors: {
        'regal-blue': '#243c5a',
        'red-fx': '#ff0000',
        'green-fx': '#006600',
      },
    },
  },
  plugins: [],
};
