<template>
	<div class="mt-6" v-if="!isLoading">
		<v-row justify="center">
			<quiz-scroll>
				<template v-slot:title>Level {{ rank }}</template>
				<template v-slot:default>
					<img class="asset" :src="'/'+asset" v-if="!!asset" />
					<div class="scroll-content" v-html="question" />
				</template>
			</quiz-scroll>
			<quiz-answer :rank="rank" @next="onNext" :isLoading="isLoading" />
		</v-row>
		<quiz-need-help />
	</div>
</template>

<script>
import QuizScroll from "@/components/QuizScroll";
import QuizAnswer from "./QuizAnswer.vue";
import QuizNeedHelp from "@/components/QuizNeedHelp";
import * as api from "@/api";
import { User, Quiz } from "@/store";

export default {
	name: "quiz",
	components: {
		QuizScroll,
		QuizAnswer,
		QuizNeedHelp
	},
	data() {
		return {
			isLoading: false,
			question: "",
			rank: "",
			asset: ""
		};
	},
	async mounted() {
		// document.getElementsByTagName("html")[0].style.overflowY = "hidden";
		// window.scrollTo(0, 0);
		await this.loadQuestion();
	},
	methods: {
		async onNext() {
			await this.loadQuestion();
		},
		async loadQuestion() {
			this.isLoading = true;
			await this.$store.dispatch("Quiz/refresh");
			if (this.Quiz.awaitNextQuestion) {
				this.$router.push({ name: "quiz-countdown" });
			} else {
				this.question = this.Quiz.question;
				this.rank = this.Quiz.rank;
				this.asset = this.Quiz.asset;
			}
			this.isLoading = false;
		}
	},
	// beforeDestroy() {
	// 	// document.getElementsByTagName("html")[0].style.overflowY = "scroll";
	// },
	computed: {
		...User.mapState(),
		...Quiz.mapState()
	}
};
</script>
