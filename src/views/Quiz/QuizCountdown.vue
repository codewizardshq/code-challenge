<template>
	<div class="mt-6">
		<v-row justify="center">
			<quiz-scroll v-if="Quiz.awaitNextQuestion">
				<template v-slot:title>Welcome Pilgrim</template>
				<template v-slot:default>
					<p class="text-center">Watch the video</p>
					<p class="text-center">
						<iframe
							width="400px"
							height="300px"
							src="https://www.youtube.com/embed/Fk8zykXuR5k"
							frameborder="0"
							allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"
							allowfullscreen
						></iframe>
					</p>
					<p class="text-center">
						<v-btn color="secondary darken-2" @click="onClick" x-large>Okay!</v-btn>
					</p>
				</template>
			</quiz-scroll>
			<quiz-scroll v-else-if="!Quiz.quizHasStarted">
				<template v-slot:title>Woah Slow Down!</template>
				<template v-slot:default>
					<p class="text-center">The challenge has not yet begun!</p>
					<p>Challenge begins: {{Quiz.nextUnlockMoment.fromNow()}}</p>
				</template>
			</quiz-scroll>
		</v-row>
	</div>
</template>

<script>
import QuizScroll from "@/components/QuizScroll";
import { Quiz } from "@/store";
export default {
	name: "quiz",
	components: {
		QuizScroll
	},
	computed: {
		...Quiz.mapState()
	},
	mounted() {
		console.log(this.Quiz.nextUnlockMoment.fromNow());
	},
	methods: {
		async onClick() {
			await this.$store.dispatch("Quiz/markAsSeen");
			this.$router.push({ name: "quiz" });
		}
	}
};
</script>
