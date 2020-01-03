<template></template>

<template>
	<v-form @submit.prevent="validate" ref="form" v-model="isValid">
		<v-card-text>
			<v-row no-gutters>
				<v-col>
					<v-text-field
						v-bind="fields.firstName"
						v-model="fields.firstName.value"
						:disabled="isSubmitting"
					/>
				</v-col>
				<v-col>
					<v-text-field
						v-bind="fields.lastName"
						v-model="fields.lastName.value"
						:disabled="isSubmitting"
					/>
				</v-col>
			</v-row>
			<v-text-field
				v-bind="fields.studentEmail"
				v-model="fields.studentEmail.value"
				:disabled="isSubmitting"
			/>
			<v-menu
				v-model="showCalendar"
				:close-on-content-click="false"
				:nudge-right="40"
				transition="scale-transition"
				offset-y
				min-width="290px"
			>
				<template v-slot:activator="{ on }">
					<v-text-field
						v-model="fields.dateOfBirth.value"
						prepend-icon="mdi-calendar"
						readonly
						v-on="on"
						v-bind="fields.dateOfBirth"
					></v-text-field>
				</template>
				<v-date-picker v-model="fields.dateOfBirth.value" @input="showCalendar = false" />
			</v-menu>
		</v-card-text>

		<v-card-actions>
			<v-btn color="primary" @click="() => $emit('back')" :disabled="isSubmitting">Back</v-btn>
			<v-spacer />
			<v-btn color="primary" type="submit" :disabled="isSubmitting">
				Next
				<v-progress-circular size="14" class="ml-3" indeterminate v-if="isSubmitting" />
			</v-btn>
		</v-card-actions>
	</v-form>
</template>

<script>
import { auth } from "@/api";

export default {
	name: "register-step-2",
	props: ["fields"],
	methods: {
		async submit() {
			if (this.isSubmitting) {
				return;
			}
			this.isSubmitting = true;
			const cb = () => {
				this.isSubmitting = false;
			};
			this.$emit("submit", cb);
		},
		validate() {
			if (this.$refs.form.validate()) {
				this.submit();
			}
		}
	},
	data() {
		return {
			isValid: false,
			isSubmitting: false,
			showCalendar: false
		};
	}
};
</script>
