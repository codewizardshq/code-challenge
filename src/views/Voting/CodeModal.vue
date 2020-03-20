<template>
  <div>
    <v-dialog v-model="isOpen" max-width="1000">
      <v-card
        class="ballot ballot-modal"
        height="600"
        color="white"
        light
        v-if="isOpen"
      >
        <v-row class="main-row" no-gutters>
          <v-col cols="3" sm="12" md="3" class="left">
            <div class="circle">
              {{ initials }}
            </div>
            <hr />
            <v-form lazy-validation @submit.prevent="submit">
              <v-text-field
                single-line
                outlined
                solo
                v-bind="fields.email"
                v-model="fields.email.value"
                :disabled="isSubmitting"
                v-if="!User.isAuthorized"
              />
              <v-btn
                block
                tile
                color="cwhqBlue"
                type="submit"
                :disabled="isSubmitting"
                >Confirm Vote</v-btn
              >

              <v-row no-gutters class="icons" justify="center">
                <v-btn
                  fab
                  color="cwhqBlue"
                  icon
                  target="_blank"
                  :href="facebookUrl"
                >
                  <v-icon>mdi-facebook</v-icon>
                </v-btn>
                <v-btn
                  fab
                  color="cwhqBlue"
                  icon
                  target="_blank"
                  :href="twitterUrl"
                >
                  <v-icon>mdi-twitter</v-icon>
                </v-btn>
                <v-btn
                  fab
                  color="cwhqBlue"
                  icon
                  target="_blank"
                  :href="mailUrl"
                >
                  <v-icon>mdi-email</v-icon>
                </v-btn>
              </v-row>
            </v-form>
          </v-col>
          <v-col class="right">
            <pre v-highlightjs="text"><code class="javascript"></code></pre>
          </v-col>
        </v-row>
      </v-card>
    </v-dialog>

    <success-modal v-model="showSuccess" />

    <v-dialog v-model="showError" max-width="600">
      <v-card color="white" light v-if="isOpen">
        <v-card-title>
          Uh oh something went wrong.
        </v-card-title>
        <v-card-text>
          {{ errorMessage }}
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn color="cwhqBlue" tile text @click="showError = false"
            >Okay</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import * as api from "@/api";
import SuccessModal from "./SuccessModal";
import { User } from "@/store";

export default {
  components: {
    SuccessModal
  },
  data() {
    return {
      showSuccess: false,
      showError: false,
      errorMessage: "",
      isOpen: this.value,
      sourcecode: "derp",
      isSubmitting: false,
      fields: {
        email: {
          type: "email",
          value: "",
          label: "ENTER E-MAIL TO VOTE"
        }
      }
    };
  },
  computed: {
    ...User.mapState(),
    socialText() {
      return "Vote for my code at ";
    },
    socialUrl() {
      return encodeURI(
        `https://challenge.codewizardshq.com/voting?search=${this.username}&open=true`
      );
    },
    twitterUrl() {
      return `https://twitter.com/intent/tweet?text=${encodeURIComponent(
        this.socialText
      )}&url=${this.socialUrl}&original_referer=`;
    },
    facebookUrl() {
      return `https://www.facebook.com/sharer/sharer.php?u=${this.socialUrl};src=sdkpreparse`;
    },
    mailUrl() {
      return `mailto:?subject=${encodeURIComponent(
        this.socialText
      )}!&body=${encodeURIComponent(this.socialText)} ${encodeURIComponent(
        this.socialUrl
      )}`;
    }
  },
  props: [
    "display",
    "firstName",
    "id",
    "lastName",
    "numVotes",
    "text",
    "username",
    "value",
    "initials"
  ],
  watch: {
    isOpen() {
      if (this.isOpen != this.value) {
        this.$emit("input", this.isOpen);
      }
    },
    value() {
      if (this.isOpen != this.value) {
        this.isOpen = this.value;
      }
    }
  },
  methods: {
    async submit() {
      if (this.isSubmitting) {
        return;
      }
      this.isSubmitting = true;
      if (!this.fields.email.value && !this.User.isAuthorized) {
        this.errorMessage = "You forgot to tell us your email";
        this.showError = true;
        this.isSubmitting = false;
        return;
      }

      try {
        await api.voting.cast(this.id, this.fields.email.value);
        this.showSuccess = true;
      } catch (err) {
        this.errorMessage = err.message;
        this.showError = true;
      }
      this.isSubmitting = false;
    }
  }
};
</script>
