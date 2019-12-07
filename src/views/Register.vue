<template>
  <v-row align="center" justify="center">
    <v-col cols="12" sm="8" md="4">
      <v-card flat class="mt-12">
        <v-toolbar color="primary" dark flat>
          <v-toolbar-title>Create Your Account</v-toolbar-title>
        </v-toolbar>
        <v-form @submit.prevent="validate" ref="form">
          <v-card-text>
            <v-text-field
              v-bind="fields.email"
              v-model="fields.email.value"
              :disabled="isSubmitting"
            />

            <v-text-field
              v-bind="fields.username"
              v-model="fields.username.value"
              :disabled="isSubmitting"
            />

            <v-text-field
              v-bind="fields.name"
              v-model="fields.name.value"
              :disabled="isSubmitting"
            />

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

            <v-switch
              v-bind="fields.ageGate"
              v-model="fields.ageGate.value"
              :disabled="isSubmitting"
            />
          </v-card-text>

          <v-card-actions>
            <v-spacer />
            <v-btn color="primary" type="submit">
              Create Account
            </v-btn>
          </v-card-actions>
        </v-form>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
import { Auth } from "@/api";

export default {
  name: "register",
  methods: {
    async submit() {
      if (this.isSubmitting) {
        return;
      }
      this.isSubmitting = true;
      try {
        await Auth.createAccount(
          this.fields.username.value,
          this.fields.email.value,
          this.fields.password.value,
          this.fields.name.value,
          ""
        );
        localStorage.setItem("lastEmail", this.fields.username.value);
        this.$store.dispatch("Snackbar/showInfo", "Successfully Logged In");
        this.$router.push({ name: "home" });
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
        email: {
          label: "email",
          type: "email",
          value: "",
          rules: [v => !!v || "Please provide a email"]
        },
        username: {
          label: "Username",
          type: "text",
          value: "",
          rules: [v => !!v || "Please provide a username"]
        },
        name: {
          label: "Your Name",
          type: "text",
          value: "",
          rules: [v => !!v || "Please tells us your name"]
        },
        password: {
          label: "Password",
          type: "password",
          value: "",
          rules: [v => !!v || "Please provide a password"]
        },
        passwordConfirm: {
          label: "Confirm Passowrd",
          type: "password",
          value: "",
          rules: [
            v => v == this.fields.password.value || "Passwords do not match"
          ]
        },
        ageGate: {
          label: "I am 13 years of age or older",
          value: false,
          rules: [v => !!v || "Please confirm your age"]
        }
      }
    };
  }
};
</script>
