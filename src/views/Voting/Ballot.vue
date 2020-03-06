<template>
  <v-container>
    <v-row>
      <v-col>
        <h2 class="ballot-header">
          Cast your vote below!
        </h2></v-col
      >
    </v-row>
    <v-row justify="center" v-if="isLoading">
      <v-col class="text-center">
        <v-progress-circular class="mt-6" color="cwhqBlue" size="100" width="10" indeterminate />
        <h2 class="mt-6">
          Loading Results <small><br />Please Wait</small>
        </h2>
      </v-col>
    </v-row>
    <v-row justify="center" v-else>
      <ballot-card v-for="(item, i) in items" :key="i" v-bind="item" @click="showCode(item)" />
    </v-row>
    <v-row justify="center" v-if="totalPages > 1">
      <v-pagination v-model="page" :length="totalPages" circle></v-pagination>
    </v-row>
    <code-modal v-bind="this.item" v-model="showModal" />
  </v-container>
</template>

<script>
import Vue from 'vue';
import { voting } from '@/api';
import BallotCard from './BallotCard';
import CodeModal from './CodeModal';

export default {
  components: {
    BallotCard,
    CodeModal
  },
  data() {
    return {
      isLoading: true,
      per: 16,
      item: null,
      showModal: false,
      hasNext: false,
      hasPrev: false,
      nextNum: false,
      page: 1,
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
    },
    async loadPage() {
      this.isLoading = true;
      try {
        const results = await voting.getBallot(this.page, this.per);
        for (const [key, value] of Object.entries(results)) {
          Vue.set(this, key, value);
        }
      } catch (err) {
        this.$router.push({ name: 'redirect' });
      }
      this.isLoading = false;
    }
  },
  watch: {
    page(val) {
      this.loadPage(val);
    }
  },
  async mounted() {
    this.loadPage();
  }
};
</script>

<style lang="scss" scoped>
h2 {
  text-align: center;
  color: #0d1d41;
  font-family: 'Barlow', sans-serif;
  font-weight: bold;
  margin-bottom: 12px;
}
</style>
