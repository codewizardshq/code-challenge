<template>
  <v-app-bar
    color="dark"
    flat
    dark
    :height="height"
    :max-height="height"
    class="pl-4"
  >
    <div class="text-center" style="width: 100%;">
      <router-link :to="{ name: 'home' }">
        <img src="/images/logo-small.png" class="mt-2" :height="imageHeight" />
      </router-link>
    </div>
  </v-app-bar>
</template>

<script>
import { User } from "@/store";

export default {
  name: "appBar",
  computed: {
    ...User.mapState()
  },
  data() {
    return {
      height: 60,
      imageHeight: 50
    };
  }
};
</script>
