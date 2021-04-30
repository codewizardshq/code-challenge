<template>
  <div class="text-center">
    <v-dialog v-model="dialog" width="500">
      <template v-slot:activator="{ on, attrs }">
        <v-btn color="primary" dark v-bind="attrs" v-on="on" elevation="0">
          See Full Leaderboard
        </v-btn>
      </template>

      <v-card>
        <v-card-title class="headline lighten-2">
          Our Vote Leaders
        </v-card-title>

        <v-card-text>
          <v-data-table :headers="headers" :items="pageData.items"
          :items-per-page="5" class="elevation-1" width: />
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="cancel" text @click="dialog = false">
            Close
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import Vue from "vue";
import { voting } from "@/api";
export default {
  name: "Leaderboard",
  data() {
    return {
      dialog: false,
      headers: [
        { text: "Rank", sortable: true, value: "rank" },
        { text: "First Name", sortable: true, value: "firstName" },
        { text: "Last Name", sortable: true, value: "lastName" },
        { text: "Votes", sortable: true, value: "numVotes" }
      ],
      entries: [],
      pageData: {
        hasNext: false,
        hasPrev: false,
        nextNum: false,
        page: 1,
        items: [],
        prevNum: null,
        totalItems: 0,
        totalPages: 0
      }
    };
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      const results = await voting.getBallot(1, 1000);
      await this.setResult(results);
    },
    async setResult(result) {
      await new Promise(resolve => {
        setTimeout(async () => {
          for (const [key, value] of Object.entries(result)) {
            if (key !== "items") {
              Vue.set(this.pageData, key, value);
            }
          }

          const items = result.items
            .filter(i => i.disqualified === null)
            .sort((a, b) => {
              return a.numVotes < b.numVotes ? 1 : -1;
            });

          // add rank
          let counter = 1;
          for (let i = 0; i < items.length; i++) {
            items[i] = {
              ...items[i],
              rank: counter
            };
            counter++;
          }

          Vue.set(this.pageData, "items", items);
          resolve();
        }, 500);
      });
    }
  }
};
</script>

<style lang="scss" scoped>
.headline {
  background-color: #fdc743;
}
</style>
