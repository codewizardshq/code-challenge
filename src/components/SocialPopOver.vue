<template>
  <v-menu
    v-model="isOpen"
    :close-on-content-click="false"
    offset-x
    offset-y
    id="test"
  >
    <template v-slot:activator="{ on }">
      <slot v-bind:on="on">Default Content</slot>
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
  </v-menu>
</template>

<script>
export default {
  data: () => ({
    isOpen: false,
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
  })
};
</script>

<style scoped>
.v-menu__content {
  box-shadow: none;
}
</style>
