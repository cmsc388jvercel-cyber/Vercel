/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./flask_app/templates/**/*.{html,js}"],
  theme: {
    extend: {},
  },
  plugins: [require("@tailwindcss/typography")],
};
