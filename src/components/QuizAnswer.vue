<template>
	<div class="quiz-answer">
		<v-card flat>
			<img src="~@/static/dragon1.png" />
			<v-card-text>
				<v-form>
					<v-text-field label="Your Answer" />
					<v-btn
						x-large
						color="primary"
					>
						Submit
					</v-btn>
				</v-form>
			</v-card-text>
		</v-card>
	</div>
</template>

<script>
export default {
	name: "quizAnswer"
};
</script>
