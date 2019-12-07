<template>
	<v-app>
		<app-bar />
		<quiz-bar />
		<v-content>
			<router-view />
		</v-content>
		<snackbar />
	</v-app>
</template>

<script>
import AppBar from "@/components/AppBar";
import QuizBar from "@/components/QuizBar";
import Snackbar from "@/components/Snackbar";

export default {
	name: "App",
	components: {
		AppBar,
		QuizBar,
		Snackbar
	}
};
</script>