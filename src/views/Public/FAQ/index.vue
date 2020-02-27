<template>
  <v-container>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="12" md="7">
        <page-card>
          <template #title>
            <v-toolbar-title>Frequently Asked Questions</v-toolbar-title>
          </template>

          <FAQ-card>
            <template #title>How do I sign up for the challenge? </template>
            Create an account anytime until April 23, 2020 at
            <router-link :to="{ name: 'register' }"
              >https://challenge.codewizardshq.com/create-account </router-link
            >. You will need a parent's email address to sign up.
          </FAQ-card>

          <FAQ-card>
            <template #title>How do I play the challenge? </template>
            Login every day between Apr 3 8:00AM CT - Apr 23 11:59PM CT to answer a challenge question.
            When you get the question right, you will move on to the next level.
            You can answer questions as many times as you want until Apr 23 11:59PM CT. If you have answered all 21 questions correctly, you will
            move on to the boss challenge. Challengers who place in the boss
            challenge will win a $100 CWHQ gift card plus a cash prize.
          </FAQ-card>

          <FAQ-card>
            <template #title>What are the challenge prizes? </template>
            Any challengers who complete all 21 levels will win a $100
            CodeWizardsHQ gift card. Place in the boss level and win the $100
            CWHQ gift card plus a cash prize.
            <ul>
              <li>First Place $100</li>
              <li>Second Place $50</li>
              <li>Third Place $25</li>
            </ul>
            First, second, and third place winners are determined by public
            vote.
          </FAQ-card>

          <FAQ-card>
            <template #title
              >Who can participate in the code challenge?
            </template>
            Challengers must be children between the ages of 8 and 18. Any
            challengers under the age of 13 will require parental consent.
          </FAQ-card>

          <FAQ-card>
            <template #title>Can I get help with the challenge? </template>
            You can get help with the challenge via Discord, Facebook, and our
            FAQ page. Please reach out to us with any technical questions
            through one of these sources. We will not be able to help you answer
            the questions in the challenge.
          </FAQ-card>

          <FAQ-card>
            <template #title>What are the questions going to cover? </template>
            The questions will cover topics related to coding in Python and
            JavaScript.
          </FAQ-card>

          <FAQ-card>
            <template #title
              >Are the questions differentiated by age?
            </template>
            The challenge is for students 8-18 years of age. The questions are
            the same for all contestants and are not differentiated by age.
          </FAQ-card>

          <FAQ-card>
            <template #title>
              How much time do you have to answer a question?
            </template>
            You have until the end of the challenge to answer all questions.
          </FAQ-card>

          <FAQ-card>
            <template #title>Can I answer questions more than once? </template>
            Yes, you have unlimited tries to answer a question correctly.
            However, there is a cooling off period of 30 minutes after every 3
            incorrect answers.
          </FAQ-card>

          <FAQ-card>
            <template #title
              >What skills do I need to have to attempt the questions?
            </template>
            You only need a beginner’s Python or JavaScript knowledge to
            participate.
          </FAQ-card>

          <FAQ-card>
            <template #title>How is the winner determined? </template>
            The 1st, 2nd, and 3rd place winners are determined by a public vote.
            Any challengers who complete all 21 levels will be eligible to win.
          </FAQ-card>
        </page-card>
      </v-col>
    </v-row>
    <br />
    <br />
  </v-container>
</template>

<script>
  import PageCard from "@/components/PageCard";
  import FAQCard from "./FAQCard";

  export default {
  name: "faq",
  components: {
    PageCard,
    FAQCard
  }
};
</script>
