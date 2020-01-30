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
        secondary: "#27AE82",
        dark: "#282828",
        dark2: "#1E1E1E",
        button: "#4CAF50",
        input: "#4CAF50"
      }
    }
  }
});
