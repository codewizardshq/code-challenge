<template>
	<div>
		<v-container>
			<v-row>
				<v-col cols="8">
					<quiz-scroll />
				</v-col>

				<v-col>
					<quiz-answer />
				</v-col>
			</v-row>
		</v-container>
		<quiz-need-help />
	</div>
</template>

<script>
import QuizScroll from "@/components/QuizScroll";
import QuizAnswer from "@/components/QuizAnswer";
import QuizNeedHelp from "@/components/QuizNeedHelp";

export default {
	name: "quiz",
	components: {
		QuizScroll,
		QuizAnswer,
		QuizNeedHelp
	}
};
</script>