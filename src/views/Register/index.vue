<template>
  <v-row align="center" justify="center">
    <v-col cols="12" sm="8" md="8">
      <v-card flat class="mt-12">
        <v-toolbar color="primary" dark flat>
          <v-toolbar-title>Create Your Account</v-toolbar-title>
        </v-toolbar>
        <v-stepper v-model="e1">
          <v-stepper-header class="elevation-0">
            <v-stepper-step :complete="e1 > 1" step="1"
              >Account Details</v-stepper-step
            >

            <v-divider></v-divider>

            <v-stepper-step :complete="e1 > 2" step="2"
              >Student Details</v-stepper-step
            >

            <v-divider></v-divider>

            <v-stepper-step step="3">Terms Of Use</v-stepper-step>
          </v-stepper-header>

          <v-stepper-items>
            <v-stepper-content step="1">
              <step-1 :fields="fields" @submit="submit1" />
            </v-stepper-content>

            <v-stepper-content step="2">
              <step-2 :fields="fields" @back="back" @submit="submit2" />
            </v-stepper-content>

            <v-stepper-content step="3">
              <step-3 :fields="fields" @back="back" @submit="submit3" />
            </v-stepper-content>
          </v-stepper-items>
        </v-stepper>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
import Step1 from "./Step1";
import Step2 from "./Step2";
import Step3 from "./Step3";
import { auth } from "@/api";

export default {
  components: {
    Step1,
    Step2,
    Step3
  },
  methods: {
    back() {
      this.e1--;
      if (this.e1 <= 0) {
        this.e1 = 1;
      }
    },
    submit1(cb) {
      this.e1++;
      cb();
    },
    submit2(cb) {
      this.e1++;
      cb();
    },
    async submit3(cb) {
      if (this.isSubmitting) {
        return;
      }
      this.isSubmitting = true;
      try {
        await auth.createAccount(
          this.fields.parentEmail.value,
          this.fields.password.value,
          this.fields.firstName.value,
          this.fields.lastName.value
        );
        localStorage.setItem("lastEmail", this.fields.parentEmail.value);
        this.$store.dispatch("Snackbar/showInfo", "Successfully Logged In");
        this.$router.push({ name: "home" });
      } catch (err) {
        this.$store.dispatch("Snackbar/showError", err);
      }
      this.isSubmitting = false;
      this.e1 = 0;
      this.$router.push({ name: "quiz" });
      cb();
    }
  },
  data() {
    return {
      isSubmitting: false,
      e1: 0,
      fields: {
        parentEmail: {
          label: "Parent's E-mail Address",
          type: "email",
          value: "",
          rules: [v => !!v || "Please provide a email"]
        },
        studentEmail: {
          label: "Student's E-mail Address (optional)",
          type: "email",
          value: ""
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
        firstName: {
          label: "Student's First Name",
          type: "text",
          value: "",
          rules: [v => !!v || "Please tells us your name"]
        },
        lastName: {
          label: "Student's Last Name",
          type: "text",
          value: "",
          rules: [v => !!v || "Please tells us your name"]
        },
        dateOfBirth: {
          label: "Student's Date Of Birth",
          type: "date",
          value: null,
          max: new Date().toISOString().substr(0, 10),
          rules: [v => !!v || "Please enter a date of birth"]
        },
        tos: {
          label: "I agree to the Terms of Use",
          value: false,
          rules: [v => !!v || "You must agree to the Terms of Use"]
        }
      }
    };
  }
};
</script>
