<template>
	<v-toolbar
		color="dark2"
		flat
		max-height=60
		class="secondary--text"
	>

		<quiz-bar-rank :rank="Progress.rank" />

		<span v-if="User.isAuthorized">
			Welcome pilgrim {{User.username}}
		</span>
		<v-btn
			v-else
			color="secondary"
			text
			:to="{name:'register'}"
		>
			Start your journey
		</v-btn>
		<v-spacer />
		<v-btn
			text
			color="secondary"
		>
			Get your friends in on it
			<v-icon>
				mdi-open-in-new
			</v-icon>
		</v-btn>
	</v-toolbar>
</template>

<script>
import QuizBarRank from "./QuizBarRank";
import { User, Progress } from "@/store";

export default {
	name: "quizBar",
	components: {
		QuizBarRank
	},
	computed: {
		...User.mapState(),
		...Progress.mapState()
	},
	methods: {
		getHelp() {
			// Todo
		}
	}
};
</script>
