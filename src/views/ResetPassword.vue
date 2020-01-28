<template>
  <v-row align="center" justify="center">
    <v-col cols="12" sm="8" md="4">
      <v-card flat class="mt-12">
        <v-toolbar color="secondary" dark flat>
          <v-toolbar-title>Password reset form</v-toolbar-title>
        </v-toolbar>
        <v-form @submit.prevent="validate" ref="form">
          <v-card-text>
            <p>
              Create a new password.
            </p>

            <v-text-field
              v-bind="fields.password"
              v-model="fields.password.value"
              :disabled="isSubmitting"
            />
            <v-text-field
              v-bind="fields.passwordConfirm"
              v-model="fields.passwordConfirm.value"
              :disabled="isSubmitting"
            />
          </v-card-text>

          <v-card-actions>
            <v-spacer />
            <v-btn color="secondary" type="submit" dark :disabled="isSubmitting"
            >Reset Password</v-btn
            >
          </v-card-actions>
        </v-form>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
  import {auth} from "@/api";

  export default {
    name: "reset-password",
    created() {
      if (! this.$route.params.token) {
        this.$store.dispatch(
          "Snackbar/showError",
          "Missing token from URL. Password cannot be reset."
        );
        this.$router.push({ name: "forgot-password" });
      }
    },
    methods: {
      async submit() {
        try {
          await auth.resetPassword(this.$route.params.token, this.fields.password.value);
          this.$store.dispatch(
            "Snackbar/showInfo",
            "Password reset successfully. You may now login."
          );
          this.$router.push({ name: "login" })
        } catch (e) {
          console.error(e);
          this.$store.dispatch(
            "Snackbar/showError",
            "Request failed"
          );
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
        fields: {
          password: {
            label: "Password",
            type: "password",
            autocomplete: "new-password",
            value: "",
            rules: [
              v => !!v || "Don't forget to give a password",
              v => v.length >= 8 || "Password must be at least 8 characters"
            ]
          },
          passwordConfirm: {
            label: "Confirm Password",
            type: "password",
            value: "",
            rules: [
              v => v == this.fields.password.value || "Passwords do not match"
            ]
          },
        }
      };
    }
  };
</script>
