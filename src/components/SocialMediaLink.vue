<template>
  <div class="text-center col col-6">
    <a
      :href="anchorHref"
      target="_blank"
      class="icon v-btn v-btn--is-elevated v-btn--has-bg theme--dark v-size--default"
    >
      <span class="v-btn__content"
        ><i aria-hidden="true" :class="iconClass"></i></span
    ></a>
  </div>
</template>

<script>
export default {
  name: "SocialMediaLink",
  props: {
    anchorHref: {
      type: String,
      required: true
    },
    iconClass: {
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
