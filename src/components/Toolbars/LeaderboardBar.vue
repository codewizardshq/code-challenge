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

<style lang="scss" scoped>
.leaderboard-bar {
  $lbLight: rgba(247, 228, 196, 1);
  $lbLight70: rgba(247, 228, 196, 0.7);
  $lbDark: rgba(85, 83, 94, 1);
  $opaque: rgba(1, 1, 1, 0);
  $height: 43px;

  background-color: $lbLight;

  .lb-item {
    color: $lbLight;
    display: inline-block;
    padding: 5px 4px;
    margin-left: 15px;
    margin-right: 15px;
    height: $height;
    position: relative;
    background-color: rgba(0, 0, 0, 0);

    img.rank {
      height: $height;
      display: inline-block;
      position: relative;
      margin-right: 8px;
    }

    div.rank {
      position: absolute;
      height: $height;
      width: 16px;
      text-align: center;
      top: 8px;
      left: 10px;
      color: #fec;
      font-family: "Seymour One", sans-serif;
    }

    .display {
      display: inline-block;
      height: $height;
      color: $lbDark;
      margin-top: 5px;
      font-family: "Oxygen", sans-serif;
    }
  }

  .fade {
    position: absolute;
    width: 400px;
    height: 100%;
    background-image: linear-gradient(
      to right,
      $lbDark,
      $lbDark,
      $lbLight70,
      $opaque
    );
    z-index: 1;
    top: 0;
    left: 0;
  }

  .rotated-text {
    position: absolute;
    color: honeydew;
    z-index: 999999;
    font-size: 20px;
    text-align: center;
    height: 100%;
    left: 10px;
    top: 10px;
    font-family: "Seymour One", sans-serif;
  }

  .lb-marquee {
    background-color: $lbLight;
  }
}
</style>
