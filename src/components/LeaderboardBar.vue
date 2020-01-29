<template>
  <v-toolbar
    color="white"
    :height="height"
    :min-height="height"
    :max-height="height"
    class="leaderboard-bar"
  >
    <div class="rotated-text">
      LEADER
      <br />BOARD
    </div>
    <div class="fade"></div>
    <marquee-text :duration="(items.length / 5) * 10">
      <div class="lb-item" v-for="(item, i) in items" :key="i">
        <img src="/images/shield.png" class="rank float-left" />
        <div class="rank">{{ item.rank }}</div>
        <div class="display float-left">{{ item.username }}</div>
      </div>
    </marquee-text>
  </v-toolbar>
</template>

<script>
import MarqueeText from "vue-marquee-text-component";
import * as api from "@/api";
import { shuffle } from "@/util";

export default {
  components: {
    MarqueeText
  },
  async mounted() {
    const leaders = (await api.quiz.getLeaderboard()).items;

    if (leaders.length === 0) {
      return;
    }

    while (this.items.length < 100) {
      for (const leader of leaders) {
        this.items.push({
          username: leader[0],
          rank: leader[1]
        });
      }
    }

    this.items = shuffle(this.items);
  },
  data() {
    return {
      height: 50,
      items: []
    };
  }
};
</script>
