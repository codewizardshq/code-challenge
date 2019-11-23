<template>
	<v-app-bar
		color="dark"
		flat
		dark
		max-height=80
	>
		<div class="d-flex align-center">
			<v-img
				alt="CodewizardsHQ Logo"
				contain
				src="~@/static/logo-small.png"
				transition="scale-transition"
			/>
		</div>

		<v-spacer></v-spacer>

		<v-btn
			:to="{name:'home'}"
			v-bind="buttonProps"
		>
			Home
		</v-btn>
		<v-btn
			:to="{name:'quiz'}"
			v-bind="buttonProps"
		>
			Quiz
		</v-btn>
		<v-btn
			:to="{name:'about'}"
			v-bind="buttonProps"
		>

			About
		</v-btn>
		<v-btn
			@click="getHelp"
			v-bind="buttonProps"
		>
			Get Help
		</v-btn>
		<v-btn
			:to="{name:'login'}"
			v-bind="buttonProps"
			v-if="!User.isAuthenticated"
		>
			Sign In
		</v-btn>
		<v-btn
			:to="{name:'register'}"
			v-bind="buttonProps"
			v-if="!User.isAuthenticated"
		>
			Create Account
		</v-btn>
		<v-btn
			:to="{name:'about'}"
			v-bind="buttonProps"
			v-if="User.isAuthenticated"
		>
			Sign Out
		</v-btn>
	</v-app-bar>
</template>

<script>
import { User } from "@/store";
export default {
  name: "appBar",
	computed: {
		...User.mapState()
	},
	data() {
		return {
			buttonProps: {
				text: true
			}
		};
	},
	methods: {
		getHelp() {}
	}
};
</script>