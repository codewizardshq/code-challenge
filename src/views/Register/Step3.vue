<template>
  <v-form @submit.prevent="validate" ref="form" v-model="isValid">
    <v-card-text>
      <v-card max-height="500" style="overflow-y:scroll;">
        <v-card-text>
          Terms Of Service: What Is It? A Terms of Service, or TOS, is a set of
          rules that a user must agree to before they can engage in services or
          use a product. It can also serve as a disclaimer under certain
          conditions, such as for website use. A properly executed Terms of
          Service is legally binding for both parties. A Terms of Service
          agreement usually has many different sections, such as definitions,
          user rights and responsibilities, and disclaimers. Terms of Service
          can change often, and they will need to be re-accepted as changes are
          made to the agreement. It is important to any company or business to
          include as much information as possible in their Terms of Service to
          avoid problems in the future. Getting legal counsel for the Terms of
          Service can ensure no major points have been missed and that the Terms
          of Service is legally binding to users. Click here to get started now!
          Recent Reviews “I am very pleased with FormSwift products and have
          already recommended them to a number of my friends. The ease of
          creating documents has saved me countless hours.” -Carrie L. "I love
          FormSwift. There have been so many new documents added since first
          signing up. They walk you through every step. Great job and thanks for
          everything you guys do for making this happen." -John M. "FormSwift
          was very easy to use, even for someone who is not very tech savvy like
          me. Will use again." -Phil T. What Are Terms of Service? what are
          terms of service Terms of service perform two essential functions. The
          first is to educate your customers on the rules of using your products
          and services. The second is to protect your company from lawsuits .
          The TOS is a simple enough document to draw up, whether you’re using a
          free terms of service generator or working from a sample. Terms of
          service should be one of the first documents issued to your clients,
          and you should be sure to get it read and signed by each client before
          proceeding with their business. Part One - Language A TOS starts off
          by familiarizing the reader with the terms that will be used
          throughout the document. Generally these terms are fairly, well,
          general ones, such as “Terms,” “Services,” “The Company,” etc. Part
          Two – Rules of the Road. The TOS then goes on to outline the rights
          and responsibilities of the user. The key to this section is to keep
          it short and sweet while including all relevant detail. The best
          approach is to tell your client what they can’t do rather than what
          they can do. Omission is more illustrative than inclusion. Plus, it’s
          a good idea to keep the TOS as short as possible so people actually
          them. Part Three – What Is and Is Not Your Company’s Fault Limit your
          liabilities. Limit them as much as you can, and make their limits
          clear. For example: TO THE MAXIMUM EXTENT PERMITTED BY LAW,
          ARTHURMACARTHUR, INC. SHALL NOT BE LIABLE FOR AN YDIRECT, INDIRECT,
          INCIDENTAL, CONSEQUENTIAL, OR SPECIAL DAMAGES OR LOSSES, WHETHER
          TANGIBLE OR INTANGIBLE, RESULTING FROM AUTHORIZED OR UNAUTHORIZED USE
          OF OR ACCESS TO OUR PRODUCTS You also might want to include a
          disclaimer or return policy, particularly if you’re in the retail
          business. This protects you from customers blaming you for damaged
          goods: SUPERDUPER, INC. IS NOT RESPONSIBLE FOR THE CONDITIONS OF ITS
          MERCHANDISE. THE COMPANY SELLS ALL ITS MERCHANDISE ON AN “AS IS” BASIS
          AND ASSUMES NO LIABILITY OR RESPONSIBILITY FOR ANY DAMAGES INCURRED IN
          THE TRANSFER OR USE OF OUR PRODUCTS BY YOU OR ANY THIRD PARTY. Part
          Four – Verification Put a statement at the end like, “I have read and
          agreed to abide by PenDragonPencil’s Terms of Service.” If you’re
          issuing a paper TOS, follow this with a place for the user to print
          his or her name and sign and date the form provide instructions as to
          how the document should be returned to the company. If your TOS is
          online, you can just have the user insert his or her initials and hit
          the “I Agree” button.
        </v-card-text>
      </v-card>
    </v-card-text>

    <v-card-actions>
      <v-spacer />
      <v-switch v-model="fields.tos.vale" v-bind="fields.tos"></v-switch>
    </v-card-actions>

    <v-card-actions>
      <v-btn
        color="secondary darken-2"
        @click="() => $emit('back')"
        :disabled="isSubmitting"
        >Back</v-btn
      >
      <v-spacer />
      <v-btn
        color="secondary darken-2"
        type="submit"
        :disabled="
          isSubmitting ||
            !isValid ||
            fields.password.value != fields.passwordConfirm.value
        "
      >
        Create Account
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
