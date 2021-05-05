<template>
  <v-container>
    <v-row>
      <v-col>
        <h2 class="ballot-header mt-8 mb-8">
          <slot name="header">Hall of Champions</slot>
        </h2>
        <SearchBar v-model="searchText" />

        <div style="color:#0d1d41" class="mb-6 mt-4 text-center">
          <slot name="content">
            Each of these amazing kid coders has used their coding skills for
            good and successfully helped Nym and the AllSnacks Alliance save the
            galaxy. Now, they have a chance to win the $100 grand prize, but
            they need your help!
            <br />
            <br />
            <b>
              View the contestants and their code, then vote for the winner of
              our 2021 Code Challenge, The Deep Space Crystal Chase. </b
            >The 10 students with the most votes will have their code
            <router-link :to="'/mission'"
              >reviewed by the Galactic Wizard Panel</router-link
            >
            and one worthy student will be our champion.
          </slot>
        </div>

        <h2
          v-if="!isLoading && pageData.items.length === 0 && searchText !== ''"
        >
          Could not find any results for "{{ searchText }}"
        </h2>
        <h2 v-else-if="searchText !== ''">
          Showing results for "{{ searchText }}"
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
        <h2 class="mt-6">
          Loading Results <small><br />Please Wait</small>
        </h2>
      </v-col>
    </v-row>
    <v-row v-else-if="pageData.items === 0">
      No results were found for "{{ searchText }}"
    </v-row>
    <v-row justify="center" v-else class="card-wrapper">
      <BallotCard
        v-for="(item, i) in pageData.items[pageData.page - 1]"
        :key="i"
        v-bind="item"
        :is-voting-disabled="isVotingDisabled"
        @click="showCode(item)"
      />
    </v-row>
    <v-row justify="center" v-if="pageData.totalPages > 1 && !isLoading">
      <v-pagination
        v-model="pageData.page"
        :length="pageData.totalPages"
        @input="nextPageOnClick"
        circle
      ></v-pagination>
    </v-row>
    <CodeModal
      v-bind="this.item"
      v-model="showModal"
      :is-voting-disabled="isVotingDisabled"
    />
  </v-container>
</template>

<script>
import Vue from "vue";
import { voting } from "@/api";
import BallotCard from "@/views/Voting/BallotCard";
import CodeModal from "@/views/Voting/CodeModal";
import SearchBar from "@/views/Voting/SearchBar";
export default {
  name: "VoteLeaderboardSearch",
  components: {
    BallotCard,
    CodeModal,
    SearchBar
  },
  props: {
    isVotingDisabled: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      totalEntries: "",
      requestIndex: 0,
      requestCount: 0,
      showModal: false,
      searchText: "",
      item: null,
      per: 10,
      pageData: {
        // hasNext: false,
        // hasPrev: false,
        // nextNum: false,
        page: -1,
        items: [],
        // prevNum: null,
        // totalItems: 0,
        totalPages: 0
      }
    };
  },
  methods: {
    showCode(item) {
      this.item = item;
      this.showModal = true;
    },
    nextPageOnClick(page) {
      Vue.set(this.pageData, "page", page);
      this.updateQueryParams();
    },
    async setResult(result) {
      await new Promise(resolve => {
        setTimeout(async () => {
          // shuffle the results if no search string given
          let shuffled;
          if (this.searchText.length > 0) {
            shuffled = result.items;
          } else {
            shuffled = this.shuffle(result.items);
          }

          // push into sub arrays
          let postShuffled = [];
          while (shuffled.length > 0) {
            postShuffled.push(shuffled.splice(0, 10));
          }

          // set data
          Vue.set(this.pageData, "items", postShuffled);
          Vue.set(this.pageData, "totalPages", this.pageData.items.length);

          // for (const [key, value] of Object.entries(result)) {
          //   if (key !== "items") {
          //     Vue.set(this.pageData, key, value);
          //   }
          // }
          // Vue.set(this.pageData, "items", shuffled);
          await this.updateQueryParams();
          resolve();
        }, 1000);
      });
    },
    async search() {
      if (this.searchText === "") {
        return this.loadPage();
      }
      // this.pageData.page = 1;
      this.requestIndex++;
      this.requestCount++;
      const requestIndex = this.requestIndex;
      const searchText = this.searchText;
      try {
        const results = await voting.search(this.searchText, 1, 10000);
        if (
          this.searchText === searchText &&
          this.requestIndex === requestIndex
        ) {
          await this.setResult(results);
        }
      } catch (err) {
        // eslint-disable-next-line no-console
        if (err.status === 404) {
          this.pageData.page = 1;
          await this.search();
        } else {
          // for testing
          // TODO: remove if later
          if (this.$router.history._startLocation !== "/testing/vote") {
            this.$router.push({ name: "redirect" });
          }
        }
      }
      this.requestCount--;
    },
    async loadPage() {
      this.requestCount++;
      try {
        const results = await voting.getBallot(1, 10000);
        await this.setResult(results);
      } catch (err) {
        if (err.status === 404) {
          this.pageData.page = 1;
          await this.loadPage();
        } else {
          // for testing
          // TODO: remove if later
          if (this.$router.history._startLocation !== "/testing/vote") {
            this.$router.push({ name: "redirect" });
          }
        }
      }
      this.requestCount--;
    },
    async updateQueryParams() {
      try {
        const query = {
          page: this.pageData.page
        };
        if (this.searchText !== "") {
          query.search = encodeURIComponent(this.searchText);
        }
        await this.$router.replace({ name: this.$route.name, query });
      } catch (err) {
        // do nothing.
      }
    },
    async refresh() {
      if (this.searchText === "") {
        this.loadPage();
      } else {
        this.search();
      }
    },
    /**
     * Shuffles array in place.
     * @param {Array} a items An array containing the items.
     */
    shuffle(a) {
      var j, x, i;
      for (i = a.length - 1; i > 0; i--) {
        j = Math.floor(Math.random() * (i + 1));
        x = a[i];
        a[i] = a[j];
        a[j] = x;
      }
      return a;
    }
  },
  computed: {
    isLoading() {
      return this.requestCount > 0;
    }
  },
  watch: {
    searchText() {
      this.search();
    }
    // ["pageData.page"]() {
    //   this.refresh();
    // },
    // ["$route.query.page"](val) {
    //   const page = parseInt(val);
    //   if (this.pageData.page === page) {
    //     return;
    //   }
    //   this.pageData.page = page;
    //   this.refresh();
    // }
  },
  async mounted() {
    this.searchText =
      this.$route.query.search === undefined ? "" : this.$route.query.search;
    this.pageData.page =
      this.$route.query.page === undefined
        ? 1
        : parseInt(this.$route.query.page);

    this.refresh();
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

.card-wrapper {
  max-width: 1250px;
  margin: 0 auto;
}
</style>
