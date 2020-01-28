<template>
  <v-row align="center" justify="center">
    <v-col cols="12" sm="8" md="4">
      <v-card flat class="mt-12">
        <v-toolbar color="secondary" dark flat>
          <v-toolbar-title>Forgot password form</v-toolbar-title>
        </v-toolbar>
        <v-form @submit.prevent="validate" ref="form">
          <v-card-text>
            <p>
              Did you forget your password? Enter your parent's e-mail address
              below. They entered this when they created your account.
            </p>
            <v-text-field
              v-bind="fields.username"
              v-model="fields.username.value"
              :disabled="isSubmitting"
            />
          </v-card-text>

          <v-card-actions>
            <v-spacer/>
            <v-btn color="secondary" type="submit" dark :disabled="isSubmitting"
            >Send Reset Password Request
            </v-btn
            >
          </v-card-actions>
        </v-form>
      </v-card>
    </v-col>

    <v-dialog
      v-model="multiple"
      max-width="290"
    >
      <v-card>
        <v-card-title class="headline">Multiple Accounts</v-card-title>
        <v-card-text>
          That email address is associated with multiple accounts.
          Password reset emails have been sent for each account.
          Double check the email body for the username so that you reset the intended account's password!
        </v-card-text>

        <v-card-actions>
          <v-spacer/>
          <v-btn text color="green" @click="multiple = false">OK</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

  </v-row>
</template>

<script>
  import {auth} from "@/api";

  export default {
    name: "forgot-password",
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
            this.$store.dispatch(
              "Snackbar/showError",
              "No accounts associated with that email address."
            );
            return;
          }
          if (e.status === 429) {
            let totalSeconds = parseInt(e.headers["retry-after"]);
            let hours = Math.floor(totalSeconds / 3600);
            totalSeconds %= 3600;
            let minutes = Math.floor(totalSeconds / 60);
            let seconds = totalSeconds % 60;

            this.$store.dispatch(
              "Snackbar/showError",
              `Reset attempts exceeded. Try again in ${hours} hours ${minutes} minutes ${seconds} seconds.`
            );
            return;
          }
          this.$store.dispatch(
            "Snackbar/showError",
            "Request failed, try again."
          );

          console.error(e);
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
