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
              v-for="icon in icons"
              :key="icon.icon"
              cols="6"
              class="text-center"
            >
              <v-btn :href="icon.to" target="_blank">
                <v-icon>mdi-{{ icon.icon }}</v-icon>
              </v-btn>
            </v-col>
          </v-row>
          <a class="mt-6" href="https://github.com/codewizardshq/code-challenge"
            >Check out the source code on GitHub!</a
          >
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
          icon: "twitter",
          to:
            "https://twitter.com/intent/tweet?text=CodeWizardsHQ%20Code%20Challenge&url=https%3A%2F%2Fcodewizardshq.com%2Fchallenge%2F&original_referer="
        },
        {
          icon: "facebook",
          to:
            "https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fcodewizardshq.com%2Fchallenge%2F&amp;src=sdkpreparse"
        },
        {
          icon: "linkedin",
          to: "https://www.linkedin.com/company/codewizardshq"
        },
        {
          icon: "email",
          to:
            "mailto:?subject=Join%20me%20in%20the%20CodeWizardsHQ%20Code%20Challenge!"
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
