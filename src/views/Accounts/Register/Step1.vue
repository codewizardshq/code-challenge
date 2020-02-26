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

      <v-select
        single-line
        color="input"
        v-bind="fields.heardAboutUs"
        v-model="fields.heardAboutUs.value"
        :disabled="isSubmitting"
      />

      <v-textarea
        color="input"
        v-bind="fields.heardAboutUsText"
        v-model="fields.heardAboutUsText.value"
        v-if="fields.heardAboutUs.value === 'Other'"
      />
    </v-card-text>

    <v-card-actions>
      <v-spacer />
      <v-btn color="button" type="submit" :disabled="!allowSubmit">
        Next
        <v-progress-circular
          size="14"
          class="ml-3"
          indeterminate
          v-if="!allowSubmit"
        />
      </v-btn>
    </v-card-actions>
  </v-form>
</template>

<script>
import * as api from "@/api";
export default {
  name: "register-step-1",
  props: ["fields"],
  methods: {
    async submit() {
      if (!this.allowSubmit) {
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
  computed: {
    allowSubmit() {
      return !this.isSubmitting && this.fields.username.requestCount === 0;
    }
  },
  watch: {
    async "fields.username.value"() {
      this.fields.username.requestIndex++;
      const index = this.fields.username.requestIndex;
      this.fields.username.requestCount++;
      try {
        const { exists } = await api.auth.doesUsernameExist(
          this.fields.username.value
        );

        if (index !== this.fields.username.requestIndex) {
          throw new Error("Ignoring old request data");
        }

        this.fields.username.inUse = exists;
      } catch (err) {
        // eslint-disable-next-line no-console
        console.error(JSON.stringify(err));
      }
      this.fields.username.requestCount--;
    },
    "fields.username.inUse"(val) {
      this.fields.username.errorMessages = val
        ? ["This username is already in use"]
        : [];
    },
    "fields.username.requestCount"(val) {
      this.fields.username.inUse = val > 0 ? false : this.fields.username.inUse;
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
