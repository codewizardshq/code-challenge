<template>
  <v-form @submit.prevent="validate" ref="form" v-model.trim="isValid">
    <v-card-text>
      <v-row no-gutters>
        <v-col>
          <v-text-field
            class="mr-5"
            color="input"
            v-bind="fields.firstName"
            v-model.trim="fields.firstName.value"
            :disabled="isSubmitting"
          />
        </v-col>
        <v-col>
          <v-text-field
            color="input"
            v-bind="fields.lastName"
            v-model.trim="fields.lastName.value"
            :disabled="isSubmitting"
          />
        </v-col>
      </v-row>
      <v-text-field
        color="input"
        v-bind="fields.studentEmail"
        v-model.trim="fields.studentEmail.value"
        :disabled="isSubmitting"
      />
      <v-text-field
        color="input"
        v-model.trim="fields.schoolName.value"
        :disabled="isSubmitting"
        v-bind="fields.schoolName"
        counter="200"
      />
      <v-select
        single-line
        v-bind="fields.age"
        v-model.trim="fields.age.value"
        :disabled="isSubmitting"
      />
      <!-- <date-of-birth-field
        :label="fields.dateOfBirth.label"
        v-model.trim="fields.dateOfBirth.value"
      /> -->
    </v-card-text>

    <v-card-text v-if="needsParentConsent">
      <v-alert colored-border icon="mdi-firework">
        You are not 13 years of age.
        <p>
          In order to continue with the code challenge you must have your
          parent's permission. Have your parent or guardian complete the rest of
          this page.
        </p>
        <v-switch
          v-model.trim="hasParentConsent"
          color="button"
          class="mx-2"
          :rules="[
            v =>
              !!v ||
              'Please have your parent or guardian review this form before continuing'
          ]"
          :label="
            'I, the parent or guardian of ' +
              this.fields.firstName.value +
              ' ' +
              this.fields.lastName.value +
              ', give my consent to participate in the CodeWizardsHQ Code Challenge.'
          "
        ></v-switch>
      </v-alert>
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
  name: "register-step-2",
  props: ["fields"],
  computed: {
    needsParentConsent() {
      const ageNum = parseInt(this.fields.age.value);
      return ageNum < 13;
    }
  },
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
        if (this.needsParentConsent && !this.hasParentConsent) {
          this.showParentConsentAlert = true;
        } else {
          this.submit();
        }
      }
    }
  },
  data() {
    return {
      showParentConsentAlert: false,
      hasParentConsent: false,
      isValid: false,
      isSubmitting: false,
      showCalendar: false
    };
  }
};
</script>
