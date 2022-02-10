const defaultTheme = require("tailwindcss/defaultTheme")

module.exports = {
  content: ["./src/components/**/*.vue", "./src/pages/**/*.vue", "./src/directives/**/*.js"],
  theme: {
    screens: {
      xxs: "190px",
      xs: "275px",
      ...defaultTheme.screens,
    },
    extend: {
      colors: {
        gold: {
          200: "rgb(255, 210, 84)",
          300: "rgb(252, 196, 40)",
          400: "rgb(224, 171, 24)",
          500: "rgb(197, 132, 11)",
          600: "rgb(158, 114, 18)",
          700: "rgb(143, 90, 21)",
        },
        gray: {
          900: "rgb(28, 28, 31)",
          800: "rgb(42, 42, 45)",
          700: "#383838",
          600: "rgb(65, 65, 65)",
          500: "rgb(78, 78, 78)",
          400: "rgb(94, 94, 94)",
          300: "rgb(124, 124, 124)",
          200: "#acacac",
        },
      },
      transitionProperty: {
        height: "height",
        spacing: "margin, padding",
        rounded: "border-radius, background-color",
      },
      height: {
        "main-electron": "calc(100vh - 45px)",
        "main-web": "100vh",
      },
      padding: {
        nav: "43px",
      },
      dropShadow: {
        dark: "0 5px 2px rgba(0, 0, 0, 0.8)",
      },
    },
  },
  plugins: [],
}
