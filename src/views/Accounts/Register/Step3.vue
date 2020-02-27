<template>
  <v-form @submit.prevent="validate" ref="form" v-model="isValid">
    <v-card-text>
      <v-row no-gutters>
        <v-col>
          <v-text-field
            class="mr-5"
            color="input"
            v-bind="fields.parentFirstName"
            v-model="fields.parentFirstName.value"
            :disabled="isSubmitting"
          />
        </v-col>
        <v-col>
          <v-text-field
            color="input"
            v-bind="fields.parentLastName"
            v-model="fields.parentLastName.value"
            :disabled="isSubmitting"
          />
        </v-col>
      </v-row>
      <v-text-field
        color="input"
        v-bind="fields.parentEmail"
        v-model="fields.parentEmail.value"
        :disabled="isSubmitting"
      />
    </v-card-text>

    <v-card-actions>
      <v-btn
        color="button"
        @click="() => $emit('back')"
        :disabled="isSubmitting"
        >Back</v-btn
      >
      <v-spacer />
      <v-btn color="button" type="submit" :disabled="isSubmitting">
        Next
        <v-progress-circular
          size="14"
          class="ml-3"
          indeterminate
          v-if="isSubmitting"
        />
      </v-btn>
    </v-card-actions>
  </v-form>
</template>

<script>
export default {
  name: "register-step-3",
  props: ["fields"],
  components: {},
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
      isSubmitting: false
    };
  }
};
</script>
