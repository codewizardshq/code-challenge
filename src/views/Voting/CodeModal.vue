<template>
  <div>
    <v-dialog v-model="isOpen">
      <v-card
        class="ballot ballot-modal"
        height="600"
        color="white"
        light
        v-if="isOpen"
      >
        <!-- <v-row class="main-row" no-gutters> -->
        <v-col cols="3" sm="12" md="3" class="left">
          <div class="circle">
            {{ initials }}
          </div>
          <div class="username mb-2">
            {{ username }}
          </div>
          <hr />
          <v-form lazy-validation @submit.prevent="submit">
            <v-text-field
              single-line
              outlined
              solo
              v-bind="fields.email"
              v-model="fields.email.value"
              :disabled="isSubmitting || isVotingDisabled"
            />
            <v-btn
              block
              tile
              color="cwhqBlue"
              type="submit"
              :disabled="isSubmitting || isVotingDisabled"
              >{{ isVotingDisabled ? "Vote Over" : "Cast Vote" }}</v-btn
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
              <v-btn fab color="cwhqBlue" icon target="_blank" :href="mailUrl">
                <v-icon>mdi-email</v-icon>
              </v-btn>
              <v-btn fab color="cwhqBlue" icon target="_blank" :href="linkUrl">
                <v-icon>mdi-link</v-icon>
              </v-btn>
            </v-row>
          </v-form>
        </v-col>
        <v-col class="right">
          <pre v-highlightjs="sourceCode"><code :class="codeType"></code></pre>
        </v-col>
        <!-- </v-row> -->
      </v-card>
    </v-dialog>

    <SuccessModal v-model="showSuccess" />

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
import "highlight.js/styles/darcula.css";

export default {
  name: "CodeModal",
  components: {
    SuccessModal
  },
  // TODO: validate props
  props: [
    "display",
    "firstName",
    "id",
    "lastName",
    "numVotes",
    "text",
    "username",
    "value",
    "initials",
    "isVotingDisabled" //boolean, required
  ],
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
          label: this.isVotingDisabled
            ? "VOTING HAS ENDED"
            : "ENTER E-MAIL TO VOTE"
        }
      }
    };
  },
  computed: {
    ...User.mapState(),
    isPython() {
      const re = new RegExp(/print\s*\(/g);
      return re.test(this.text);
    },
    instructionComments() {
      if (this.isPython) {
        return `
# A Caeser Cipher is one of the earliest examples of cryptography. It was used to encrypt messages so that they could not be read by just anyone, only those who knew how the encryption works. Today, encryption is all around us - in our emails, over WiFi, everywhere!

# Your task is to implement the Caesar Cipher algorithm. Please review this video of how the algorithm works before beginning your code: https://www.youtube.com/watch?v=o6TPx1Co_wg.

# Please encrypt this string using this algorithm: "Glorm is defeated and the crystal has been returned by the Allsnacks Alliance!"
# *You should assume that a space will remain a space in the encrypted string.

# You must adhere to the following guidelines:
# --As defined in the video, the algorithm uses a numeric "shift" value. You should use a shift of 8 in your code.
# --You should IGNORE any characters that are not a letter (this includes symbols such as #*!$^) and they should not be in your output.
# --Your output should take into account both uppercase and lowercase letters. That is, both a lowercase ''a'' and uppercase ''A'' will have the same shift value. 
# --Your final answer should be in all capital letters.

# Your submission should be the FULL CODE you used to generate the output, not just one line that displays the output. Please submit the code you used to actually do the encryption. Good luck!

`;
      } else {
        return `
// A Caeser Cipher is one of the earliest examples of cryptography. It was used to encrypt messages so that they could not be read by just anyone, only those who knew how the encryption works. Today, encryption is all around us - in our emails, over WiFi, everywhere!

// Your task is to implement the Caesar Cipher algorithm. Please review this video of how the algorithm works before beginning your code: https://www.youtube.com/watch?v=o6TPx1Co_wg.

// Please encrypt this string using this algorithm: "Glorm is defeated and the crystal has been returned by the Allsnacks Alliance!"
// *You should assume that a space will remain a space in the encrypted string.

// You must adhere to the following guidelines:
// --As defined in the video, the algorithm uses a numeric "shift" value. You should use a shift of 8 in your code.
// --You should IGNORE any characters that are not a letter (this includes symbols such as #*!$^) and they should not be in your output.
// --Your output should take into account both uppercase and lowercase letters. That is, both a lowercase ''a'' and uppercase ''A'' will have the same shift value. 
// --Your final answer should be in all capital letters.

// Your submission should be the FULL CODE you used to generate the output, not just one line that displays the output. Please submit the code you used to actually do the encryption. Good luck!

`;
      }
    },
    sourceCode() {
      return this.instructionComments + this.text.replace(";output", ";");
    },
    codeType() {
      return this.isPython ? "python" : "javascript";
    },
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
    },
    linkUrl() {
      return (
        "https://challenge.codewizardshq.com/voting?page=1&search=" +
        this.username
      );
    }
  },
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
      if (!this.fields.email.value) {
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
