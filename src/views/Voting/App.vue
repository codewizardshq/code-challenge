<template>
  <v-app class="cwhq-app voting">
    <CWHQ-bar />
    <app-bar />
    <v-content>
      <router-view />
    </v-content>
  </v-app>
</template>

<script>
import AppBar from "@/components/Toolbars/AppBar";
import CWHQBar from "@/components/Toolbars/CWHQBar";

export default {
  name: "App",
  components: {
    AppBar,
    CWHQBar
  }
};
</script>
