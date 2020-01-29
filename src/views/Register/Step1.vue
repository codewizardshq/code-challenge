<template>
  <v-form @submit.prevent="validate" ref="form" v-model="isValid">
    <v-card-text>
      <p>
        Welcome to the CodeWizardsHQ Code Challenge. To begin your journey you
        must first create your account.
      </p>
      <v-text-field
        color="input"
        v-bind="fields.username"
        v-model="fields.username.value"
        :disabled="isSubmitting"
      />
      <v-text-field
        color="input"
        v-bind="fields.parentEmail"
        v-model="fields.parentEmail.value"
        :disabled="isSubmitting"
      />
      <v-text-field
        color="input"
        v-bind="fields.password"
        v-model="fields.password.value"
        :disabled="isSubmitting"
      />
      <v-text-field
        color="input"
        v-bind="fields.passwordConfirm"
        v-model="fields.passwordConfirm.value"
        :disabled="isSubmitting"
      />
    </v-card-text>

    <v-card-actions>
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
  name: "register-step-1",
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
      isSubmitting: false
    };
  }
};
</script>
