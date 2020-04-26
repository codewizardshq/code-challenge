<template>
  <v-app class="cwhq-app voting">
    <CWHQ-bar />
    <!-- <app-bar /> -->
    <v-content>
      <router-view />
    </v-content>
    <mobile-warning />
  </v-app>
</template>

<script>
// import AppBar from "@/components/Toolbars/AppBar";
import CWHQBar from "@/components/Toolbars/CWHQBar";
import MobileWarning from "@/components/MobileWarning";

export default {
  name: "App",
  components: {
    // AppBar,
    CWHQBar,
    MobileWarning
  }
};
</script>
