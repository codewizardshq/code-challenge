<template>
	<v-container>
		<v-row align="center" justify="center">
			<v-col cols="12" sm="12" md="7">
				<page-card>
					<template #title>
						<v-toolbar-title>Frequently Asked Questions</v-toolbar-title>
					</template>

					<v-card-text v-for="(item,i) in items" :key="i">
						<v-card color="dark">
							<v-card-title>{{item.title}}</v-card-title>
							<v-card-text>{{item.body}}</v-card-text>
						</v-card>
					</v-card-text>
				</page-card>
			</v-col>
		</v-row>
		<br />
		<br />
	</v-container>
</template>

<script>
import PageCard from "@/components/PageCard";
export default {
	name: "faq",
	components: {
		PageCard
	},
	mounted() {
		for (let i = 0; i < 10; i++) {
			this.items.push({
				title: "How do I do a thing?",
				body:
					"Some other text Some other text Some other text Some other text Some other text Some other text Some other text"
			});
		}
	},
	data() {
		return {
			items: []
		};
	}
};
</script>