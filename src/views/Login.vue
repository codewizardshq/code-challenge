<template>
  <v-row align="center" justify="center">
    <v-col cols="12" sm="8" md="4">
      <v-card flat class="mt-12">
        <v-toolbar color="primary" dark flat>
          <v-toolbar-title>Login form</v-toolbar-title>
        </v-toolbar>
        <v-form @submit.prevent="validate" ref="form">
          <v-card-text>
            <v-text-field
              v-bind="fields.username"
              v-model="fields.username.value"
              :disabled="isSubmitting"
            />

            <v-text-field
              v-bind="fields.password"
              v-model="fields.password.value"
              :disabled="isSubmitting"
            />
          </v-card-text>

          <v-card-actions>
            <v-spacer />
            <v-btn color="primary" type="submit" dark :disabled="isSubmitting">
              Sign In
            </v-btn>
          </v-card-actions>
        </v-form>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
import { auth } from "@/api";
export default {
  name: "login",
  methods: {
    async submit() {
      if (this.isSubmitting) {
        return;
      }
      this.isSubmitting = true;
      try {
        await auth.login(
          this.fields.username.value,
          this.fields.password.value
        );
        localStorage.setItem("lastEmail", this.fields.username.value);
        this.$store.dispatch("Snackbar/showInfo", "Successfully Logged In");
        this.$router.push({ name: "quiz" });
      } catch (err) {
        this.$store.dispatch("Snackbar/showError", err);
      }
      this.isSubmitting = false;
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
        username: {
          label: "Username",
          type: "text",
          value: localStorage.getItem("lastEmail"),
          rules: [v => !!v || "Please provide a username"]
        },
        password: {
          label: "Password",
          type: "password",
          value: "",
          rules: [v => !!v || "Please provide a password"]
        }
      }
    };
  }
};
</script>
