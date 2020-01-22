<template>
	<v-row align="center" justify="center">
		<v-col cols="12" sm="8" md="4">
			<v-card flat class="mt-12">
				<v-toolbar color="secondary" dark flat>
					<v-toolbar-title>Reset password form</v-toolbar-title>
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
						<v-spacer />
						<v-btn
							color="secondary"
							type="submit"
							dark
							:disabled="isSubmitting"
						>Send Reset Password Request</v-btn>
					</v-card-actions>
				</v-form>
			</v-card>
		</v-col>
	</v-row>
</template>

<script>
import * as api from "@/api";
export default {
	name: "reset-password",
	methods: {
		async submit() {
			try {
				await api.auth.requestPasswordReset(this.fields.username.value);
			} catch (err) {
				this.$store.dispatch("Snackbar/showError", err);
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
