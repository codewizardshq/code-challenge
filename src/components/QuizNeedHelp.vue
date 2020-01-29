<template>
  <div>
    <v-dialog v-model="dialog" max-width="290">
      <template v-slot:activator="{ on }">
        <a class="quiz-need-help" v-on="on"></a>
        <!-- <v-btn color="primary" dark v-on="on">Open Dialog</v-btn> -->
      </template>
      <v-card class="social-pop-over">
        <v-card-text>
          <v-row no-gutters class="pt-3">
            <v-col
              v-for="(icon, i) in icons"
              :key="icon.icon"
              :cols="i == icons.length - 1 ? 12 : 6"
              class="text-center"
            >
              <v-btn>
                <v-icon>mdi-{{ icon.icon }}</v-icon>
              </v-btn>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
export default {
  name: "quizNeedHelp",
  data() {
    return {
      dialog: false,
      icons: [
        {
          icon: "twitter"
        },
        {
          icon: "facebook"
        },
        {
          icon: "whatsapp"
        },
        {
          icon: "linkedin"
        },
        {
          icon: "email"
        }
      ]
    };
  }
};
</script>

<style>
.v-menu__content,
.v-dialog {
  box-shadow: none;
}
</style>
