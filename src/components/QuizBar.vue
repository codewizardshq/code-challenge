<template>
	<v-toolbar color="dark2 quiz-bar" flat class="secondary--text" :height="60" :max-height="60">
		<div class="quiz-bar-rank" v-show="User.isAuthorized">
			<div class="level-display">Level</div>
			<div class="rank">{{ User.rank }}</div>
		</div>
		<v-container>
			<v-row>
				<v-col>
					<span v-if="User.isAuthorized" class="barrow-bold">Welcome pilgrim {{ User.displayName }}</span>

					<router-link
						v-else
						color="secondary"
						text
						x-large
						active-class="none"
						:to="{ name: 'register' }"
					>Start your journey</router-link>
				</v-col>

				<v-col class="text-right">
					<help-pop-over>
						<template v-slot:default="{ on }">
							<a v-on="on">Get Help</a>
						</template>
					</help-pop-over>

					<router-link v-if="!User.isAuthorized" :to="{name:'login'}">Sign In</router-link>

					<router-link v-if="User.isAuthorized" :to="{name:'logout'}">Sign Out</router-link>
				</v-col>
			</v-row>
		</v-container>
	</v-toolbar>
</template>

<script>
import { User } from "@/store";
import HelpPopOver from "./HelpPopOver";

export default {
	name: "quizBar",
	components: {
		HelpPopOver
	},
	computed: {
		...User.mapState()
	}
};
</script>
