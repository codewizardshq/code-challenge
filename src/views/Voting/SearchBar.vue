<template>
  <div>
    <v-text-field
      outlined
      light
      prepend-inner-icon="mdi-magnify"
      placeholder="Search by name"
      v-model="text"
    >
    </v-text-field>
  </div>
</template>

<script>
export default {
  props: ["value"],
  data() {
    return {
      text: this.value
    };
  },
  watch: {
    text(text) {
      if (this.value != text || text === "") {
        this.$emit("input", text);
      }
    },
    value(value) {
      if (this.text != value) {
        this.text = value;
      }
    }
  }
};
</script>

<style scoped></style>
