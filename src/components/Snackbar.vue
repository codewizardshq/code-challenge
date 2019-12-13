<template>
	<v-snackbar
		v-model="isOpen"
		v-bind="Snackbar"
	>
		{{ Snackbar.text }}
	</v-snackbar>
</template>

<script>
import { Snackbar } from "@/store";

export default {
	data() {
		return {
			isOpen: false
		};
	},
	watch: {
		"Snackbar.isOpen"(value) {
			if (this.isOpen != value) {
				this.isOpen = value;
			}
		},
		isOpen(value) {
			if (this.Snackbar.isOpen != value) {
				this.$store.dispatch("Snackbar/isOpen", value);
			}
		}
	},
	computed: {
		...Snackbar.mapState()
	}
};
</script>
