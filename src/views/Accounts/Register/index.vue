<template>
  <v-container>
    <v-row align="center" justify="center">
      <v-col cols="12" lg="10">
        <page-card>
          <template #title>
            <v-toolbar-title>Create Your Account</v-toolbar-title>
          </template>

          <v-stepper v-model="stepperIndex">
            <v-stepper-header class="elevation-0">
              <v-stepper-step
                color="button"
                :complete="stepperIndex > 1"
                step="1"
                >Account Details</v-stepper-step
              >

              <v-divider></v-divider>

              <v-stepper-step
                color="button"
                :complete="stepperIndex > 2"
                step="2"
                >Student Details</v-stepper-step
              >

              <v-divider></v-divider>

              <v-stepper-step
                color="button"
                :complete="stepperIndex > 3"
                step="3"
                >Parent Details</v-stepper-step
              >

              <v-divider></v-divider>

              <v-stepper-step color="button" step="4"
                >Terms Of Use</v-stepper-step
              >
            </v-stepper-header>

            <v-stepper-items>
              <v-stepper-content step="1">
                <step-1 :fields="fields" @submit="next" />
              </v-stepper-content>

              <v-stepper-content step="2">
                <step-2 :fields="fields" @back="back" @submit="next" />
              </v-stepper-content>

              <v-stepper-content step="3">
                <step-3 :fields="fields" @back="back" @submit="next" />
              </v-stepper-content>

              <v-stepper-content step="4">
                <step-4 :fields="fields" @back="back" @submit="submit" />
              </v-stepper-content>
            </v-stepper-items>
          </v-stepper>
        </page-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import PageCard from "@/components/PageCard";
import Step1 from "./Step1";
import Step2 from "./Step2";
import Step3 from "./Step3";
import Step4 from "./Step4";

import * as api from "@/api";

function validateEmail(mail) {
  return /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(mail);
}

export default {
  components: {
    Step1,
    Step2,
    Step3,
    Step4,
    PageCard
  },
  methods: {
    back() {
      this.stepperIndex--;
      if (this.stepperIndex <= 0) {
        this.stepperIndex = 1;
      }
    },
    next(cb) {
      this.stepperIndex++;
      cb();
    },
    async submit(cb) {
      if (this.isSubmitting) {
        return;
      }
      this.isSubmitting = true;
      try {
        await api.auth.createAccount({
          foundUs:
            this.fields.heardAboutUs.value === "Other"
              ? "Other - " + this.fields.heardAboutUsText.value
              : this.fields.heardAboutUs.value,
          studentFirstName: this.fields.firstName.value,
          studentLastName: this.fields.lastName.value,
          parentFirstName: this.fields.parentFirstName.value,
          parentLastName: this.fields.parentLastName.value,
          username: this.fields.username.value,
          parentEmail: this.fields.parentEmail.value,
          studentEmail: this.fields.studentEmail.value,
          DOB: parseInt(this.fields.age.value) + "",
          password: this.fields.password.value
        });
        localStorage.setItem("lastUsername", this.fields.username.value);
        this.$store.dispatch("Snackbar/showInfo", "Successfully Logged In");
        this.isSubmitting = false;
        this.stepperIndex = 0;
        this.$router.push({ name: "quiz" });
      } catch (err) {
        alert(err.message);
        // eslint-disable-next-line no-console
        console.error(err);
        this.isSubmitting = false;
        this.$store.dispatch("Snackbar/showError", err);
      }
      cb();
    }
  },
  data() {
    return {
      isSubmitting: false,
      stepperIndex: 1,
      fields: {
        username: {
          label: "Username",
          hint: "You will use this to log in",
          type: "text",
          value: "",
          rules: [
            v => !!v || "Please provide a username",
            () =>
              !this.fields.username.inUse || "This username is already in use"
          ],
          inUse: false,
          requestCount: 0,
          requestIndex: 0,
          errorMessages: []
        },
        parentEmail: {
          label: "Parent's E-mail Address",
          type: "email",
          value: "",
          rules: [v => validateEmail(v) || "Please provide a valid e-mail"]
        },
        studentEmail: {
          label: "Student's E-mail Address (optional)",
          type: "email",
          value: ""
        },
        password: {
          label: "Password",
          type: "password",
          autocomplete: "new-password",
          value: "",
          rules: [
            v => !!v || "Don't forget to give a password",
            v => v.length >= 8 || "Password must be at least 8 characters",
            v =>
              v.length < 100 || "Password must be at less than 100 characters"
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
          rules: [v => !!v || "Please tell us your name"]
        },
        lastName: {
          label: "Student's Last Name",
          type: "text",
          value: "",
          rules: [v => !!v || "Please tell us your name"]
        },
        parentFirstName: {
          label: "Parent's First Name",
          type: "text",
          value: "",
          rules: [v => !!v || "Please tell us your name"]
        },
        parentLastName: {
          label: "Parent's Last Name",
          type: "text",
          value: "",
          rules: [v => !!v || "Please tell us your name"]
        },
        heardAboutUs: {
          label: "How did you hear about the Code Challange?",
          type: "select",
          items: [
            "How did you hear about the Code Challange?",
            "I'm a CodeWizardsHQ Student",
            "CWHQ newsletter",
            "CWHQ website",
            "Facebook, Twitter, Instagram, or LinkedIn",
            "Friend or family member ",
            "Google or search engine",
            "Your school or PTA",
            "Other"
          ],
          value: "How did you hear about the Code Challange?",
          rules: [
            v =>
              v !== "How did you hear about the Code Challange?" ||
              "Please choose an option"
          ]
        },
        heardAboutUsText: {
          label: "Tell us where you heard about the Code Challenge!",
          type: "text",
          value: "",
          rules: [
            v =>
              !!v || "Please tell us where you heard about the code challenge"
          ]
        },
        dateOfBirth: {
          label: "Student's Date Of Birth",
          type: "date",
          value: new Date().toISOString().substr(0, 10),
          rules: [v => !!v || "Please enter a date of birth"]
        },
        age: {
          label: "How old is the student?",
          type: "select",
          items: [
            "How old is the student?",
            "8 years old",
            "9 years old",
            "10 years old",
            "11 years old",
            "12 years old",
            "13 years old",
            "14 years old",
            "15 years old",
            "16 years old",
            "17 years old",
            "18 years old or older"
          ],
          value: "How old is the student?",
          rules: [
            v => v !== "How old is the student?" || "Please choose an option"
          ]
        },
        tos: {
          label: "I agree to the Terms of Use and Privacy Policy",
          value: false,
          rules: [
            v => !!v || "You must agree to the Terms of Use and Privacy Policy"
          ]
        },
        tos2: {
          label:
            "I agree to receive Code Challenge related updates and offers (you may unsubscribe at any time)",
          value: false,
          rules: [v => !!v || "You must agree to recieve e-mail"]
        }
      }
    };
  }
};
</script>
