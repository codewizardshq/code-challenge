import Vue from "vue";
import Vuetify from "vuetify/lib/framework";

Vue.use(Vuetify);

export default new Vuetify({
  theme: {
    dark: true,
    flat: true,
    themes: {
      dark: {
        accent: "#82B1FF",
        error: "#FF5252",
        info: "#2196F3",
        success: "#4CAF50",
        warning: "#FFC107",
        primary: "#fdc743",
        secondary: "#30395f",
        dark: "#282828",
        dark2: "#1E1E1E",
        button: "#30395f",
        input: "#4CAF50",
        cwhqBlue: "#0d1d41",
        cwhqYellow: "#fdc743"
      }
    }
  }
});
