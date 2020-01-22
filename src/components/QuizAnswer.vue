<template>
	<div class="quiz-answer">
		<v-card flat>
			<img src="/images/dragon1.png" />
			<v-card-text>
				<v-form ref="form" @submit.prevent="submit">
					<div class="attempts-remaining">
						<v-avatar
							v-for="i in totalAttempts"
							:key="i"
							:color="i <= attemptsRemaining ? 'indigo' : 'red'"
							class="mx-1"
						>
							<v-icon dark>{{ (i > attemptsRemaining) ? 'mdi-close' : 'mdi-check'}}</v-icon>
						</v-avatar>
					</div>
					<div v-if="attemptsRemaining > 0">
						<v-text-field
							autocomplete="off"
							v-model="fields.answer.value"
							v-bind="fields.answer"
							:disabled="isDisabled"
							@blur="onBlur"
						/>

						<v-btn x-large color="primary" :disabled="isDisabled" type="submit">Submit</v-btn>
					</div>
					<div v-else>
						<v-alert color="warning">You are out of attempts. You can answer again in {time}</v-alert>
						<v-btn x-large color="primary" disabled type="submit">Submit</v-btn>
					</div>
				</v-form>
			</v-card-text>
		</v-card>

		<v-dialog v-model="showSuccessModal" persistent max-width="400">
			<v-card>
				<v-card-title class="headline">Your answer was correct!</v-card-title>
				<div v-if="Quiz.awaitNextQuestion">
					<v-card-text>
						Congratulations, {{ User.displayName }}!
						<br />
						You've conquered Level {{Quiz.rank}}. {{successMessage}}
						<br />
						<br />
						That's all the questions available for now. The next question unlocks {{ Quiz.nextUnlockMoment.fromNow() }}
					</v-card-text>
					<v-card-actions>
						<v-btn block color="primary darken-1" @click="next">OKAY</v-btn>
					</v-card-actions>
				</div>
				<div v-else>
					<v-card-text>
						Congratulations, {{ User.displayName }}!
						<br />
						You've conquered Level {{Quiz.rank}}. {{successMessage}}
						<br />
						<br />
					</v-card-text>
					<v-card-actions>
						<v-btn block color="primary darken-1" @click="next">NEXT QUESTION</v-btn>
					</v-card-actions>
				</div>
			</v-card>
		</v-dialog>
	</div>
</template>

<script>
import * as api from "@/api";
import { User, Quiz } from "@/store";

export default {
	name: "quizAnswer",
	props: ["isLoading", "rank"],
	computed: {
		...Quiz.mapState(),
		...User.mapState(),
		isDisabled() {
			return this.isSubmitting || this.isLoading || this.wasCorrect;
		},
		successMessage() {
			return this.successMessages[
				Math.floor(Math.random() * this.successMessages.length)
			];
		}
	},
	data() {
		return {
			successMessages: [
				"Your coding skills are quite admirable. ",
				"You really are the best. "
			],
			isSubmitting: false,
			wasCorrect: false,
			attemptsRemaining: 3,
			totalAttempts: 3,
			showSuccessModal: false,
			fields: {
				answer: {
					label: "Your Answer",
					value: "",
					rules: [v => !!v || "You forgot to include an answer!"],
					errorMessages: [],
					successMessages: [],
					success: false
				}
			}
		};
	},
	methods: {
		onBlur() {
			this.fields.answer.errorMessages = [];
			if (!this.fields.answer.value) {
				this.$refs.form.resetValidation();
			}
		},
		async next() {
			try {
				this.showSuccessModal = false;
				this.fields.answer.value = "";
				this.fields.answer.successMessages = [];
				this.fields.answer.success = false;
				this.$refs.form.resetValidation();
				this.$emit("next");
			} catch (err) {
				await this.$store.dispatch("Snackbar/showError", err);
			}
		},
		async submit() {
			if (!this.$refs.form.validate()) {
				return;
			}

			if (this.isSubmitting) {
				return false;
			}
			this.isSubmitting = true;
			try {
				const isCorrect = await api.quiz.submit(this.fields.answer.value);

				if (isCorrect) {
					await api.auth.fetchState();
					await this.$store.dispatch("Quiz/refresh");
					this.showSuccessModal = true;
					this.fields.answer.successMessages = ["Your answer was correct!"];
					this.fields.answer.success = true;
				} else {
					this.$store.dispatch(
						"Snackbar/showError",
						"That answer was not correct"
					);
					this.fields.answer.errorMessages = ["That answer was not correct"];
				}
			} catch (err) {
				this.$store.dispatch("Snackbar/showError", err);
			}
			this.isSubmitting = false;
		}
	}
};
</script>
