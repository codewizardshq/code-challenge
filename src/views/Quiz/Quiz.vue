<template>
	<v-container fluid>
		<v-row justify="center">
			<quiz-scroll>
				<template v-slot:title>Level {{ rank }}</template>
				<template v-slot:default>
					<img class="asset" :src="'/' + asset" v-if="!!asset" />
					<div class="scroll-content" v-html="question" />
				</template>
			</quiz-scroll>
			<quiz-answer :rank="rank" @next="onNext" />
		</v-row>
		<quiz-need-help />
	</v-container>
</template>

<script>
import QuizScroll from "@/components/QuizScroll";
import QuizAnswer from "./QuizAnswer.vue";
import QuizNeedHelp from "@/components/QuizNeedHelp";
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
			question: "",
			rank: "",
			asset: ""
		};
	},
	async created() {
		this.question = this.Quiz.question;
		this.rank = this.Quiz.rank;
		this.asset = this.Quiz.asset;
	},
	methods: {
		async onNext() {
			this.$router.go();
		}
	},
	computed: {
		...User.mapState(),
		...Quiz.mapState()
	}
};
</script>
