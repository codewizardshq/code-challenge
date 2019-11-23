<template>
	<v-row
		align="center"
		justify="center"
	>
		<v-col
			cols="12"
			sm="8"
			md="4"
		>
			<v-card flat>
				<v-toolbar
					color="primary"
					dark
					flat
				>
					<v-toolbar-title>Create Your Account</v-toolbar-title>
				</v-toolbar>
				<v-form
					@submit.prevent="validate"
					ref="form"
				>
					<v-card-text>

						<v-text-field
							v-bind="fields.username"
							v-model="fields.username.value"
						/>

						<v-text-field
							v-bind="fields.name"
							v-model="fields.name.value"
						/>

						<v-text-field
							v-bind="fields.password"
							v-model="fields.password.value"
						/>

						<v-text-field
							v-bind="fields.passwordConfirm"
							v-model="fields.passwordConfirm.value"
						/>

						<v-switch
							v-bind="fields.ageGate"
							v-model="fields.ageGate.value"
						/>

					</v-card-text>

					<v-card-actions>
						<v-spacer />
						<v-btn
							color="primary"
							type="submit"
							dark
						>Sign In</v-btn>
					</v-card-actions>
				</v-form>
			</v-card>
		</v-col>
	</v-row>
</template>

<script>
export default {
	name: "login",
	methods: {
		submit() {},
		validate() {
			if (this.$refs.form.validate()) {
				this.submit();
			}
		}
	},
	data() {
		return {
			fields: {
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
