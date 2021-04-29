<template>
  <v-container>
    <v-row>
      <v-col>
        <h2 class="ballot-header">
          <slot name="header">Today's Leaders</slot>
        </h2>
      </v-col>
    </v-row>
    <v-row justify="center" v-if="isLoading">
      <v-col class="text-center">
        <v-progress-circular
          class="mt-6"
          color="cwhqBlue"
          size="100"
          width="10"
          indeterminate
        />
      </v-col>
    </v-row>
    <v-row justify="center" v-else>
      <ballot-card
        v-for="(item, i) in pageData.items"
        :key="i"
        v-bind="item"
        @click="showCode(item)"
      />
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
      requestIndex: 0,
      requestCount: 0,
      showModal: false,
      item: null,
      per: 1000,
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
    this.loadPage();
  },
  methods: {
    showCode(item) {
      this.item = item;
      this.showModal = true;
    },
    async setResult(result) {
      await new Promise(resolve =>
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
          this.$emit("input", items.length);
          items.splice(10, items.length - 10);
          Vue.set(this.pageData, "items", items);
          resolve();
        }, 1000)
      );
    },
    async loadPage() {
      this.requestCount++;

      // for testing
      if (this.$route.path === "/testing/vote") {
        Vue.set(this.pageData, "items", [
          {
            display: "TedW",
            firstName: "Ted",
            id: 12345,
            lastName: "Smith",
            numVotes: 48,
            text: "Not sure what goes here?",
            username: "Ted456",
            value: "This must be where the code goes.",
            initials: "TW"
          },
          {
            display: "something",
            firstName: "Blahblahblah",
            id: 123453,
            lastName: "Smith",
            numVotes: 45,
            text: "Not sure what goes here?",
            username: "MyUserName",
            value: "Code stuff",
            initials: "TW"
          }
        ]);

        this.requestCount--;
        return;
      }
      // end for testing

      const results = await voting.getBallot(this.pageData.page, this.per);
      await this.setResult(results);

      this.requestCount--;
    }
  },
  computed: {
    isLoading() {
      return this.requestCount > 0;
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
