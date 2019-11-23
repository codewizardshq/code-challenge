<template>
	<v-app>
		<app-bar />
		<quiz-bar />
		<v-content>
			<router-view />
		</v-content>
	</v-app>
</template>

<script>
import AppBar from "@/components/AppBar";
import QuizBar from "@/components/QuizBar";

export default {
	name: "App",
	components: {
		AppBar,
		QuizBar
	}
};
</script>