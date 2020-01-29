<template>
	<v-toolbar class="cwhq-bar" :height="height" :max-height="height">
		<v-container>
			<v-spacer />
			<a href="https://username.codewizardshq.com/edit/">Student Login</a>
			<a href="https://username.codewizardshq.com/edit/">Parent Login</a>
			<a href="https://codewizardshq.com/students/">Student Center</a>
		</v-container>
	</v-toolbar>
</template>

<script>
export default {
	data() {
		return {
			height: 23
		};
	}
};
</script>