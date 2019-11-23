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
					<v-toolbar-title>Login form</v-toolbar-title>
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
							v-bind="fields.password"
							v-model="fields.password.value"
						/>

					</v-card-text>

					<v-card-actions>
						<v-spacer />
						<v-btn
							color="primary"
							type="submit"
							dark
						>Sign In Test</v-btn>
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
