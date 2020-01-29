<template>
	<v-toolbar class="cwhq-bar" :height="height" :max-height="height">
		<v-container>
			<v-spacer />
			<a href="#">Student Login</a>
			<a href="#">Parent Login</a>
			<a href="#">Student Center</a>
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