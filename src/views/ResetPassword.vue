<template>
  <v-container>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="12" md="7">
        <page-card flat class="mt-12">
          <template #title>
            <v-toolbar-title>Password reset form</v-toolbar-title>
          </template>
          <v-card-text>
            <form-alert
              :message="errorMessage"
              @dismiss="errorMessage = false"
            />
          </v-card-text>
          <v-form @submit.prevent="validate" ref="form">
            <v-card-text>
              <p>Create a new password.</p>

              <v-text-field
                color="input"
                v-bind="fields.password"
                v-model="fields.password.value"
                :disabled="isSubmitting"
              />
              <v-text-field
                color="input"
                v-bind="fields.passwordConfirm"
                v-model="fields.passwordConfirm.value"
                :disabled="isSubmitting"
              />
            </v-card-text>

            <v-card-actions>
              <v-spacer />
              <v-btn color="button" type="submit" dark :disabled="isSubmitting"
                >Reset Password</v-btn
              >
            </v-card-actions>
          </v-form>
        </page-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { auth } from "@/api";
import PageCard from "@/components/PageCard";
import FormAlert from "@/components/FormAlert";

export default {
  name: "reset-password",
  components: {
    PageCard,
    FormAlert
  },
  created() {
    if (!this.$route.params.token) {
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
        await auth.resetPassword(
          this.$route.params.token,
          this.fields.password.value
        );

        this.$store.dispatch(
          "Snackbar/showInfo",
          "Password reset successfully. You may now login."
        );
        this.$router.push({ name: "login" });
      } catch (e) {
        this.errorMessage = "Request Failed";
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
      errorMessage: false,
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
        }
      }
    };
  }
};
</script>
