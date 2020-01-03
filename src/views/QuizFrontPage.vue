<template>
	<quiz-scroll title="Welcome Pilgrim">
		<p class="text-center">Watch the video</p>
		<p class="text-center">
			<iframe
				width="99%"
				height="300px"
				src="https://www.youtube.com/embed/Fk8zykXuR5k"
				frameborder="0"
				allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"
				allowfullscreen
			></iframe>
		</p>
		<p class="text-center">
			<v-btn color="primary" @click="() => this.$emit('next')" x-large>Continue</v-btn>
		</p>
	</quiz-scroll>
</template>

<script>
import QuizScroll from "@/components/QuizScroll";
import { quiz } from "@/api";
import { User } from "@/store";

export default {
	name: "quiz",
	components: {
		QuizScroll
	},
	async mounted() {
		document.getElementsByTagName("html")[0].style.overflowY = "hidden";
		window.scrollTo(0, 0);
	},
	beforeDestroy() {
		document.getElementsByTagName("html")[0].style.overflowY = "scroll";
	}
};
</script>
