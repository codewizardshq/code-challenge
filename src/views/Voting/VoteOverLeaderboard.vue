<template>
  <div class="ballot-wrapper">
    <div class="image first pb-9">
      <v-container>
        <v-row class="content">
          <v-col class="text-center">
            <div class="text-center" style="width: 100%;">
              <a href="#" @click="reload">
                <img src="/images/logo-small.png" class="mt-2" />
              </a>
            </div>

            <div style="max-width:600px; margin: auto;">
              <h2>
                Thank You All Who Participated
              </h2>
              <div>
                The CWHQ code challenge is now over. Congraulation to everyone
                below who completed every mission, including our boss question.
                The entries are in order by number of votes. We hope you'll lend
                us your aid for next year's edition!
              </div>
            </div>
          </v-col>
        </v-row>
      </v-container>
    </div>
    <div class="pt-4 pb-12">
      <VoteLeaderboardSearch :is-voting-disabled="true">
        <template slot="header">Voting Has Ended!</template>
        <template slot="content">
          The 2021 CWHQ code challenge is now over.
          <br />
          <br />
          <b>
            Behold, the final contestants who have completed 21 coding
            challenges! Congratulations to everyone, and thank you for
            participating!
            <br />
            <br />
            You can use the search bar above to find a particular entry.
          </b>
        </template>
      </VoteLeaderboardSearch>
    </div>
    <div class="footer"></div>
  </div>
</template>

<script>
// TODO: this component is largely copy pasted from Ballot - they should be consolidated at some point
import VoteLeaderboardSearch from "@/components/VoteLeaderboardSearch";

export default {
  name: "Ballot",
  components: {
    VoteLeaderboardSearch
  },
  methods: {
    reload() {
      // TODO: handle this better
      window.location = this.$route.path;
      // window.location = "/voting?page=1";
    }
  }
};
</script>

<style lang="scss" scoped>
.ballot-wrapper {
  background-color: white;
}

.first {
  margin-top: -60px;
  padding-top: 40px;
}

.image {
  $height: 550px;
  background-size: cover;
  min-height: $height;
  background-image: url("/images/website-banner-challenge-2021.png");
  &:after {
    content: "";
    display: block;
    position: absolute;
    z-index: 2;
    top: -60px;
    left: 0;
    height: $height;
    width: 100%;
    background: url("https://codewizardshq.com/wp-content/themes/codewizards/assets/images/banner-bg-2.png")
      no-repeat center top;
    background-size: cover;
  }

  .content {
    z-index: 12;
    position: relative;

    h2 {
      color: white;
      font-size: 42px;
    }
  }
}

.footer {
  background-color: #0d1d41;
  height: 150px;
}

/* bubble seems to not be used */
.bubble {
  max-width: 700px;
  border: #011e41;
  border-radius: 20px;
  padding: 30px;
  margin: auto;
}

.colored {
  display: block;
  position: relative;
  background-color: #a1c5d3;
  color: #011e41;

  background-image: url(data:image/png;base64,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),
    url(data:image/png;base64,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);
  background-position: left center, right center;
  background-repeat: no-repeat;

  a {
    small {
      color: white;
      display: block;
      padding-top: 12px;
    }
  }
}
</style>
