<template>
  <v-row align="center" justify="center">
    <v-col cols="12" sm="8" md="4">
      <v-card flat class="mt-12">
        <v-toolbar color="secondary" dark flat>
          <v-toolbar-title>Your scores</v-toolbar-title>
        </v-toolbar>

        <v-card-text style="height: 300px"
          >This page is not implemented. You would see some stats
          here.</v-card-text
        >
        <v-card-actions>
          <v-spacer />
          <v-btn :to="{ name: 'quiz' }">Next</v-btn>
        </v-card-actions>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
export default {
  name: "home"
};
</script>
