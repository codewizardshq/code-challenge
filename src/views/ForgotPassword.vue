<template>
  <v-container>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="12" md="7">
        <page-card flat class="mt-12">
          <template #title>
            <v-toolbar-title>Forgot password form</v-toolbar-title>
          </template>
          <v-card-text>
            <form-alert
              :message="errorMessage"
              @dismiss="errorMessage = false"
            />
          </v-card-text>
          <v-form @submit.prevent="validate" ref="form">
            <v-card-text>
              <p>
                Did you forget your password? Enter your parent's e-mail address
                below. They entered this when they created your account.
              </p>
              <v-text-field
                color="input"
                v-bind="fields.username"
                v-model="fields.username.value"
                :disabled="isSubmitting"
              />
            </v-card-text>

            <v-card-actions>
              <v-spacer />
              <v-btn color="button" type="submit" dark :disabled="isSubmitting"
                >Send Reset Password Request</v-btn
              >
            </v-card-actions>
          </v-form>
        </page-card>
      </v-col>

      <v-dialog v-model="multiple" max-width="290">
        <v-card>
          <v-card-title class="headline">Multiple Accounts</v-card-title>
          <v-card-text>
            That email address is associated with multiple accounts. Password
            reset emails have been sent for each account. Double check the email
            body for the username so that you reset the intended account's
            password!
          </v-card-text>

          <v-card-actions>
            <v-spacer />
            <v-btn text color="button" @click="multiple = false">OK</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-row>
  </v-container>
</template>

<script>
import { auth } from "@/api";
import PageCard from "@/components/PageCard";
import FormAlert from "@/components/FormAlert";

export default {
  name: "forgot-password",
  components: {
    PageCard,
    FormAlert
  },
  methods: {
    async submit() {
      try {
        let res = await auth.forgotPassword(this.fields.username.value);
        this.multiple = res.multiple;
        this.$store.dispatch(
          "Snackbar/showInfo",
          "A password reset link was sent to your email."
        );
      } catch (e) {
        if (e.status === 400) {
          this.errorMessage = "No accounts associated with that email address.";
          return;
        }
        if (e.status === 429) {
          let totalSeconds = parseInt(e.headers["retry-after"]);
          let hours = Math.floor(totalSeconds / 3600);
          totalSeconds %= 3600;
          let minutes = Math.floor(totalSeconds / 60);
          let seconds = totalSeconds % 60;

          this.errorMessage = `Reset attempts exceeded. Try again in ${hours} hours ${minutes} minutes ${seconds} seconds.`;
          return;
        }
        this.errorMessage = "Request failed, please try again";
      }
    },
    validate() {
      if (this.$refs.form.validate()) {
        this.submit();
      }
    }
  },
  data() {
    return {
      isSubmitting: false,
      multiple: false,
      errorMessage: false,
      fields: {
        username: {
          label: "Parents E-mail",
          type: "email",
          rules: [v => !!v || "Please provide a valid e-mail address"]
        }
      }
    };
  }
};
</script>
