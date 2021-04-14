<template>
  <v-col cols="6" class="text-center">
    <v-btn :href="anchorHref" target="_blank" class="icon">
      <v-icon>{{ iconName }}</v-icon></v-btn
    >
  </v-col>
</template>

<script>
export default {
  name: "SocialMediaLink",
  props: {
    anchorHref: {
      type: String,
      required: true
    },
    iconName: {
      type: String,
      required: true
    }
  }
};
</script>

<style lang="scss" scoped>
.icon {
  margin: 10px;
}
</style>
