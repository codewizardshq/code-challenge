<template>
	<div class="mt-6" v-if="!isLoading">
		<v-row justify="center">
			<quiz-scroll>
				<template v-slot:title>Level {{ rank }}</template>
				<template v-slot:default>
					<img class="asset" :src="asset" v-if="!!asset" />
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
import QuizAnswer from "@/components/QuizAnswer";
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
			localRank: this.$store.state.User.rank + 1,
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
			this.$store.dispatch("Quiz/setScores");
			this.$router.push({ name: "quiz-scores" });
		},
		async loadQuestion() {
			this.isLoading = true;
			await this.$store.dispatch("Quiz/refresh");
			this.question = this.Quiz.question;
			this.rank = this.Quiz.rank;
			this.asset = this.Quiz.asset;
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
