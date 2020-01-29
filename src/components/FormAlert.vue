<template>
	<v-alert prominent type="error" color="red darken-1" v-if="!!message">
		<v-row align="center">
			<v-col class="grow">{{ message }}</v-col>
			<v-col class="shrink">
				<v-btn color="white" light @click="$emit('dismiss')">Dismiss</v-btn>
			</v-col>
		</v-row>
	</v-alert>
</template>

<script>
export default {
	props: ["message"]
};
</script>