<template></template>

<script>
import { voting } from "@/api";

export default {
	async mounted() {
		try {
			await voting.getBallot();
		} catch (err) {
			this.$router.push({ name: "home" });
		}
	}
};
</script>