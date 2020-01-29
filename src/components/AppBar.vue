<template>
	<v-app-bar color="dark" flat dark :height="height" :max-height="height" class="pl-4">
		<div class="text-center" style="width: 100%;">
			<router-link :to="{ name: 'home' }">
				<!-- <v-img
          class="mt-2"
					alt="CodewizardsHQ Logo"
					contain
          height="80"
					src="/images/logo-small.png"
					transition="scale-transition"
				/>-->
				<img src="/images/logo-small.png" class="mt-2" :height="imageHeight" />
			</router-link>
		</div>
	</v-app-bar>
</template>

<script>
import { User } from "@/store";
import HelpPopOver from "./HelpPopOver";
export default {
	name: "appBar",
	components: {
		HelpPopOver
	},
	computed: {
		...User.mapState()
	},
	data() {
		return {
      height: 60,
      imageHeight: 50,
			buttonProps: {
				text: true,
				xLarge: true,
				class: "barrow-bold"
			}
		};
	},
	methods: {
		getHelp() {}
	}
};
</script>
