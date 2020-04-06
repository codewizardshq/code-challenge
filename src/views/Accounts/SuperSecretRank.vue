<template>
  <v-container>
    <page-card>
      <template #title>
        Shhh it's a secret page
        <small style="position: absolute; right:12px;top:20px"
          >showing {{ leaders.length }} total entries</small
        >
      </template>
      <v-simple-table>
        <thead>
          <tr>
            <td>Username</td>
            <td>Rank</td>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in leaders" :key="item.username">
            <td>
              {{ item[0] }}
            </td>
            <td>
              {{ item[1] }}
            </td>
          </tr>
        </tbody>
      </v-simple-table>
    </page-card>
  </v-container>
</template>

<script>
import * as api from "@/api";
import PageCard from "@/components/PageCard.vue";
export default {
  components: {
    PageCard
  },
  name: "super-secret-rank",
  data() {
    return {
      leaders: []
    };
  },

  async mounted() {
    this.leaders = (await api.quiz.getLeaderboard()).items.sort((a, b) => {
      return a[1] < b[1];
    });
  }
};
</script>
