
import Vue from 'vue'
import Vuetify from 'vuetify/lib'

// import colors from 'vuetify/lib/util/colors'

Vue.use(Vuetify)

export default new Vuetify({
  theme: {
    dark: true,
    flat: true,
    themes: {
      dark: {
        primary: '#fdc743',
        secondary: '#0fad80',
        // accent: '#82B1FF',
        // error: '#FF5252',
        // info: '#2196F3',
        // success: '#4CAF50',
        // warning: '#FFC107',
        dark: "#353535",
        dark2: "#333131"
      },
    },
  },
})
