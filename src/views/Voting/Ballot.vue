<template>
  <v-container>
    <v-row>
      <v-col>
        <h2 class="ballot-header">
          Lorem Ipsum is simply dummy text of the printing and typesetting
          industry. Lorem Ipsum has been the industry's standard dummy text ever
          since the 1500s, when an unknown printer took a galley of type and
          scrambled it to make a type specimen book.
        </h2></v-col
      >
    </v-row>
    <v-row justify="center">
      <ballot-card
        v-for="(item, i) in items"
        :key="i"
        v-bind="item"
        @click="showCode(item)"
      >
      </ballot-card>
    </v-row>
    <code-modal v-bind="this.item" v-model="showModal" />
  </v-container>
</template>

<script>
import Vue from "vue";
import { voting } from "@/api";
import BallotCard from "./BallotCard";
import CodeModal from "./CodeModal";

export default {
  components: {
    BallotCard,
    CodeModal
  },
  data() {
    return {
      item: null,
      showModal: false,
      hasNext: false,
      hasPrev: false,
      nextNum: false,
      page: 0,
      prevNum: null,
      totalItems: 0,
      totalPages: 0,
      items: [],
      headers: {}
    };
  },
  methods: {
    showCode(item) {
      this.item = item;
      this.showModal = true;
    }
  },
  async mounted() {
    // for (let i = 0; i < 100; i++) {
    //   this.items.push({
    //     display: "Kyle A.",
    //     firstName: "Kyle",
    //     id: 45,
    //     lastName: "Askew",
    //     numVotes: 0,
    //     text:
    //       "function calculateAnswer(){\n  return 100;\n}\nvar output = calculateAnswer();;output",
    //     username: "net8floz2"
    //   });
    // }
    try {
      const results = await voting.getBallot();
      for (const [key, value] of Object.entries(results)) {
        Vue.set(this, key, value);
      }
      // console.log(results);
    } catch (err) {
      this.$router.push({ name: "redirect" });
    }
  }
};
</script>

<style lang="scss" scoped>
h2 {
  text-align: center;
  color: #0d1d41;
  font-family: "Barlow", sans-serif;
  font-weight: bold;
  margin-bottom: 12px;
}
</style>
