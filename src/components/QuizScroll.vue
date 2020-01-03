<template>
	<div class="quiz-scroll">
		<v-card flat>
			<div class="scroll-title">{{ title }}</div>
			<div class="scroll-content">
				<slot>
					<v-img :src="asset" v-if="!!asset" />
					<v-card-text v-html="question" />
				</slot>
			</div>
		</v-card>
	</div>
</template>

<script>
export default {
	name: "quizScroll",
	props: ["title", "asset", "question"]
};
</script>
