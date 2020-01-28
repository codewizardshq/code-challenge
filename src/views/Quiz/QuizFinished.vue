<template>
	<div class="mt-6">
		<v-row justify="center">
			<quiz-scroll>
				<template v-slot:title>The Challenge Is Over</template>
				<template v-slot:default>Thank you for playing!</template>
			</quiz-scroll>
		</v-row>
	</div>
</template>

<script>
import QuizScroll from "@/components/QuizScroll";
export default {
	name: "quiz",
	components: {
		QuizScroll
	},
	mounted() {}
};
</script>
