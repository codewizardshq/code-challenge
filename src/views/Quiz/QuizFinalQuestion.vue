<template>
	<div class="mt-6" v-if="!isLoading">
		<v-container>
			<v-row justify="center">
				<v-col>
					<v-card>
						<br />
						<v-card-text v-html="question"></v-card-text>
						<v-card-title>Code your answer!</v-card-title>

						<v-form ref="form" @submit.prevent="submit">
							<v-card-text v-if="!!errorMessage">
								<v-alert prominent type="error" color="red darken-4">
									<v-row align="center">
										<v-col class="grow">{{errorMessage}}</v-col>
										<v-col class="shrink">
											<v-btn color="white" light @click="errorMessage = false">Dismiss</v-btn>
										</v-col>
									</v-row>
								</v-alert>
							</v-card-text>
							<v-card-text>
								<v-select v-bind="fields.language" v-model="fields.language.value" />
								<code-editor
									v-bind="fields.code"
									v-model="fields.code.value"
									:language="fields.language.value"
								/>
							</v-card-text>
							<v-card-actions>
								<v-spacer />
								<v-btn type="submit" :disabled="isSubmitting" large color="secondary darken-2">Submit Answer</v-btn>
							</v-card-actions>
						</v-form>
					</v-card>
				</v-col>
			</v-row>
		</v-container>
		<!-- <quiz-need-help /> -->
	</div>
</template>

<script>
import QuizNeedHelp from "@/components/QuizNeedHelp";
import CodeEditor from "./CodeEditor";
import * as api from "@/api";
import { User, Quiz } from "@/store";

export default {
	name: "quiz",
	components: {
		CodeEditor,
		QuizNeedHelp
	},
	data() {
		const jsCode = `function calculateAnswer(){
  return 100;
}
var output = calculateAnswer();`;
		const pyCode = `def calculateAnswer():
  return 100

output = calculateAnswer()`;
		return {
			isLoading: false,
			isSubmitting: false,
			question: "",
			rank: "",
			asset: "",
			errorMessage: false,
			pyCode,
			jsCode,
			fields: {
				code: {
					label: "Enter your code",
					value: jsCode
				},
				language: {
					label: "Choose your language",
					value: "javascript",
					items: ["javascript", "python"]
				}
			}
		};
	},
	watch: {
		["fields.language.value"](val) {
			if (val === "javascript") {
				this.fields.code.value = this.jsCode;
			} else {
				this.fields.code.value = this.pyCode;
			}
		},
		["fields.code.value"](val) {
			if (this.fields.language.value === "javascript") {
				this.jsCode = val;
			} else {
				this.pyCode = val;
			}
		}
	},
	async mounted() {
		await this.loadQuestion();
	},
	methods: {
		async submit() {
			if (this.isSubmitting) {
				return false;
			}
			this.isSubmitting = true;
			try {
				const response = await api.quiz.submitFinal(
					this.fields.code.value,
					this.fields.language.value === "javascript" ? "js" : "py"
				);
				const isCorrect = response.correct;

				if (isCorrect) {
					// await this.$store.dispatch("Quiz/clearWrongCount");
					// await api.auth.fetchState();
					// await this.$store.dispatch("Quiz/refresh");
					// this.showSuccessModal = true;
					// this.fields.answer.successMessages = ["Your answer was correct!"];
					// this.fields.answer.success = true;
				} else {
					if (!!response.js_error) {
						this.errorMessage = response.js_error;
					} else {
						this.errorMessage =
							"Hmmm.... Your code doesn't seem to generate the correct answer. Try again.";
					}
				}
			} catch (err) {
				if (err.status === 429) {
					this.showRateLimitModal = true;
				} else {
					this.$store.dispatch("Snackbar/showError", err);
				}
			}
			this.isSubmitting = false;
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
	computed: {
		...User.mapState(),
		...Quiz.mapState()
	}
};
</script>
