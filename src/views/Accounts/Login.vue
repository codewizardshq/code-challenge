<template>
  <v-container>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="12" md="7">
        <page-card>
          <template #title>
            <v-toolbar-title>Login form</v-toolbar-title>
          </template>

          <v-card-text>
            <v-alert type="info">
              Registration is closed! Thanks for playing.
            </v-alert>
            <form-alert
              :message="errorMessage"
              @dismiss="errorMessage = false"
            />
          </v-card-text>
          <v-form @submit.prevent="validate" ref="form">
            <v-card-text>
              <v-text-field
                color="input"
                v-bind="fields.username"
                v-model="fields.username.value"
                :disabled="isSubmitting"
              />

              <v-text-field
                color="input"
                v-bind="fields.password"
                v-model="fields.password.value"
                :disabled="isSubmitting"
              />
            </v-card-text>

            <v-card-text>
              <router-link :to="{ name: 'forgot-password' }"
                >Forgot your password?</router-link
              >
            </v-card-text>

            <v-card-actions>
              <v-spacer />
              <v-btn color="button" type="submit" dark :disabled="isSubmitting"
                >Sign In</v-btn
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
  name: "login",
  components: {
    PageCard,
    FormAlert
  },
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
        localStorage.setItem("lastUsername", this.fields.username.value);
        this.$router.push({ name: "quiz" });
      } catch (err) {
        this.errorMessage = err.message;
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
      errorMessage: "",
      fields: {
        username: {
          label: "Username",
          type: "text",
          value: localStorage.getItem("lastUsername"),
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
