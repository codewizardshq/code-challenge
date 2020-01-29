<template>
	<v-row align="center" justify="center">
		<v-col cols="12" lg="10">
			<page-card>
				<template #title>
					<v-toolbar-title>Create Your Account</v-toolbar-title>
				</template>

				<v-stepper v-model="stepperIndex">
					<v-stepper-header class="elevation-0">
						<v-stepper-step color="button" :complete="stepperIndex > 1" step="1">Account Details</v-stepper-step>

						<v-divider></v-divider>

						<v-stepper-step color="button" :complete="stepperIndex > 2" step="2">Student Details</v-stepper-step>

						<v-divider></v-divider>

						<v-stepper-step color="button" step="3">Terms Of Use</v-stepper-step>
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
			</page-card>
		</v-col>
	</v-row>
</template>

<script>
import PageCard from "@/components/PageCard";
import Step1 from "./Step1";
import Step2 from "./Step2";
import Step3 from "./Step3";
import { auth } from "@/api";

export default {
	components: {
		Step1,
		Step2,
		Step3,
		PageCard
	},
	methods: {
		back() {
			this.stepperIndex--;
			if (this.stepperIndex <= 0) {
				this.stepperIndex = 1;
			}
		},
		submit1(cb) {
			this.stepperIndex++;
			cb();
		},
		submit2(cb) {
			this.stepperIndex++;
			cb();
		},
		async submit3(cb) {
			if (this.isSubmitting) {
				return;
			}
			this.isSubmitting = true;
			try {
				await auth.createAccount({
					studentFirstName: this.fields.firstName.value,
					studentLastName: this.fields.lastName.value,
					username: this.fields.username.value,
					parentEmail: this.fields.parentEmail.value,
					studentEmail: this.fields.studentEmail.value,
					DOB: this.fields.dateOfBirth.value,
					password: this.fields.password.value
				});
				localStorage.setItem("lastUsername", this.fields.username.value);
				this.$store.dispatch("Snackbar/showInfo", "Successfully Logged In");
				this.isSubmitting = false;
				this.stepperIndex = 0;
				this.$router.push({ name: "quiz" });
			} catch (err) {
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
					rules: [v => !!v || "Please provide a email"]
				},
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
				dateOfBirth: {
					label: "Student's Date Of Birth",
					type: "date",
					value: new Date().toISOString().substr(0, 10),
					rules: [v => !!v || "Please enter a date of birth"]
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
