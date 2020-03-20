<template>
  <v-container>
    <v-row>
      <v-col>
        <h2 class="ballot-header">
          Cast your vote below!
        </h2>
        <search-bar v-model="searchText" />

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
    <v-row justify="center" v-else>
      <ballot-card
        v-for="(item, i) in pageData.items"
        :key="i"
        v-bind="item"
        @click="showCode(item)"
      />
    </v-row>
    <v-row justify="center" v-if="pageData.totalPages > 1 && !isLoading">
      <v-pagination
        v-model="pageData.page"
        :length="pageData.totalPages"
        circle
      ></v-pagination>
    </v-row>
    <code-modal v-bind="this.item" v-model="showModal" />
  </v-container>
</template>

<script>
import Vue from "vue";
import { voting } from "@/api";
import BallotCard from "./BallotCard";
import CodeModal from "./CodeModal";
import SearchBar from "./SearchBar";

export default {
  components: {
    BallotCard,
    CodeModal,
    SearchBar
  },
  data() {
    return {
      requestIndex: 0,
      requestCount: 0,
      showModal: false,
      searchText: "",
      item: null,
      per: 50,
      pageData: {
        hasNext: false,
        hasPrev: false,
        nextNum: false,
        page: -1,
        items: [],
        prevNum: null,
        totalItems: 0,
        totalPages: 0
      }
    };
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
            Vue.set(this.pageData, key, value);
          }
          await this.updateQueryParams();
          resolve();
        }, 1000)
      );
    },
    async search() {
      if (this.searchText === "") {
        return this.loadPage();
      }
      this.requestIndex++;
      this.requestCount++;
      const requestIndex = this.requestIndex;
      const searchText = this.searchText;
      try {
        const results = await voting.search(
          this.searchText,
          this.pageData.page,
          this.per
        );
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
          this.$router.push({ name: "redirect" });
        }
      }
      this.requestCount--;
    },
    async loadPage() {
      this.requestCount++;
      try {
        const results = await voting.getBallot(this.pageData.page, this.per);
        await this.setResult(results);
      } catch (err) {
        if (err.status === 404) {
          this.pageData.page = 1;
          await this.loadPage();
        } else {
          this.$router.push({ name: "redirect" });
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
    },
    ["pageData.page"]() {
      this.refresh();
    },
    ["$route.query.page"](val) {
      const page = parseInt(val);
      if (this.pageData.page === page) {
        return;
      }
      this.pageData.page = page;
      this.refresh();
    }
  },
  async mounted() {
    this.searchText =
      this.$route.query.search === undefined ? "" : this.$route.query.search;
    this.pageData.page =
      this.$route.query.page === undefined
        ? 1
        : parseInt(this.$route.query.page);
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
