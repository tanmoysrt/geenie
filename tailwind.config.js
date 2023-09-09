/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/js/**/*.js",
    "./node_modules/flowbite/**/*.js",
  ],
  safelist: [
    "alert",
    "alert-success",
    "alert-danger",
    "alert-warning",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Poppins", "sans-serif"],
        poppins: ["Poppins", "sans-serif"],
      },
    },
  },
  plugins: [
    require("@tailwindcss/forms")({
      strategy: "base",
    }),
    require("flowbite/plugin"),
  ],
};
