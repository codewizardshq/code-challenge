<template>
  <v-toolbar
    :height="height"
    :min-height="height"
    :max-height="height"
    class="leaderboard-bar"
    color="#fec"
    width="100%"
    tag="footer"
  >
    <div class="rotated-text">
      LEADERBOARD
    </div>
    <div class="fade"></div>
    <marquee-text :duration="(items.length / 5) * 10" class="lb-marquee">
      <div class="lb-item" v-for="(item, i) in items" :key="i">
        <img src="/images/leaderboard-shield.svg" class="rank float-left" />
        <div class="rank">{{ item.rank }}</div>
        <div class="display float-left">{{ item.username }}</div>
      </div>
    </marquee-text>
  </v-toolbar>
</template>

<script>
import MarqueeText from "vue-marquee-text-component";
import * as api from "@/api";
// import { shuffle } from "@/util";

export default {
  components: {
    MarqueeText
  },
  async created() {
    const leaders = (await api.quiz.getLeaderboard()).items;

    if (leaders.length === 0) {
      return;
    }

    // while (this.items.length < 100) {
    for (const leader of leaders) {
      //if (leader[1] > 15) {

      this.items.push({
        username: leader.username.split("@")[0],
        rank: leader.rank + 1
      });

      //}
    }
    // }

    //this.items = shuffle(this.items);

    while (this.items.length > 100) {
      this.items.splice(this.items.length - 1, 1);
    }
  },
  data() {
    return {
      height: 50,
      items: []
    };
  }
};
</script>
