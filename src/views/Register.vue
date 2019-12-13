<template>
  <v-row align="center" justify="center">
    <v-col cols="12" sm="8" md="4">
      <v-card flat class="mt-12">
        <v-toolbar color="primary" dark flat>
          <v-toolbar-title>Create Your Account</v-toolbar-title>
        </v-toolbar>
        <v-form lazy-validation @submit.prevent="validate" ref="form">
          <v-card-text>
            <v-text-field
              v-bind="fields.email"
              v-model="fields.email.value"
              :disabled="isSubmitting"
            />

            <v-row>
              <v-col>
                <v-text-field
                  v-bind="fields.firstName"
                  v-model="fields.firstName.value"
                  :disabled="isSubmitting"
                />
              </v-col>
              <v-col>
                <v-text-field
                  v-bind="fields.lastName"
                  v-model="fields.lastName.value"
                  :disabled="isSubmitting"
                />
              </v-col>
            </v-row>

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
import { auth } from "@/api";

export default {
  name: "register",
  methods: {
    async submit() {
      if (this.isSubmitting) {
        return;
      }
      this.isSubmitting = true;
      try {
        await auth.createAccount(
          this.fields.email.value,
          this.fields.password.value,
          this.fields.firstName.value,
          this.fields.lastName.value
        );
        localStorage.setItem("lastEmail", this.fields.email.value);
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
          label: "Your E-mail Address",
          type: "email",
          value: "",
          rules: [v => !!v || "Please provide a email"]
        },
        firstName: {
          label: "First Name",
          type: "text",
          value: "",
          rules: [v => !!v || "Please tells us your name"]
        },
        lastName: {
          label: "Last Name",
          type: "text",
          value: "",
          rules: [v => !!v || "Please tells us your name"]
        },
        password: {
          label: "Password",
          type: "password",
          value: "",
          rules: [
            v => !!v || "Don't forget to give a password",
            v => v.length >= 11 || "Password must be atleast 11 characters"
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
        ageGate: {
          label: "I am 13 years of age or older",
          value: false
        }
      }
    };
  }
};
</script>
