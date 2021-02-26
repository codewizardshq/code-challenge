<template>
  <v-container>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="12" md="12">
        <page-card>
          <template #title>
            <v-toolbar-title>Frequently Asked Questions</v-toolbar-title>
          </template>

          <div class="faq">
            <v-expansion-panels flat inset focusable>
              <v-expansion-panel>
                <v-expansion-panel-header color="cwhqBlue">How do I sign up for the challenge?</v-expansion-panel-header>
                <v-expansion-panel-content color="white" style="color: #333;">
                  <v-card-text>
                    Create an account anytime until April 5, 2021 at
                    <router-link :to="{ name: 'register' }">https://challenge.codewizardshq.com/create-account </router-link>. You will need a parent's email
                    address to sign up.
                  </v-card-text>
                </v-expansion-panel-content>
              </v-expansion-panel>
              <v-expansion-panel>
                <v-expansion-panel-header color="cwhqBlue">How do I play the challenge? </v-expansion-panel-header>
                <v-expansion-panel-content color="white" style="color: #333;">
                  <v-card-text>
                    Login every day between Apr 5 8:00AM CT - Apr 25 11:59PM CT to answer a challenge question. When you get the question right, you will move on to the next level.
                    You can answer questions as many times as you want until Apr 25 11:59PM CT. If you have answered all 21 questions correctly, you will move on to the boss challenge.
                    Any challengers who answer the first 21 questions correctly will win a $25 codewizardshq gift card.
                  </v-card-text>
                </v-expansion-panel-content>
              </v-expansion-panel>

              <v-expansion-panel>
                <v-expansion-panel-header color="cwhqBlue">What are the challenge prizes? </v-expansion-panel-header>
                <v-expansion-panel-content color="white" style="color: #333;">
                  <v-card-text>
                    Any challengers who complete all 21 levels will win a $25 CodeWizardsHQ gift card.
                    Place in the boss level and win the $100 CWHQ gift card plus a cash prize.
                    <ul>
                      <li>First Place $100</li>
                      <li>Second Place $50</li>
                      <li>Third Place $25</li>
                    </ul>
                    First, second, and third place winners are determined by Wizard panel review.
                  </v-card-text>
                </v-expansion-panel-content>
              </v-expansion-panel>

              <v-expansion-panel>
                <v-expansion-panel-header color="cwhqBlue">Who can participate in the code challenge? </v-expansion-panel-header>
                <v-expansion-panel-content color="white" style="color: #333;">
                  <v-card-text>
                    Challengers must be children between the ages of 8 and 18. Any challengers under the age of 13 will require parental consent.                   </v-card-text>
                </v-expansion-panel-content>
              </v-expansion-panel>

              <v-expansion-panel>
                <v-expansion-panel-header color="cwhqBlue">Can I get help with the challenge? </v-expansion-panel-header>
                <v-expansion-panel-content color="white" style="color: #333;">
                  <v-card-text>
                    You can get help with the challenge via Discord, Facebook, and our FAQ page. Please reach out to us with any technical questions through one of these sources. We will not be able to help you answer the questions in the challenge.
                  </v-card-text>
                </v-expansion-panel-content>
              </v-expansion-panel>

              <v-expansion-panel>
                <v-expansion-panel-header color="cwhqBlue">What are the questions going to cover? </v-expansion-panel-header>
                <v-expansion-panel-content color="white" style="color: #333;">
                  <v-card-text>
                    The questions will cover programming topics related to coding in Python and JavaScript. The first 21 questions are written in Python, but cover concepts across languages.
                  </v-card-text>
                </v-expansion-panel-content>
              </v-expansion-panel>

              <v-expansion-panel>
                <v-expansion-panel-header color="cwhqBlue">Are the questions differentiated by age? </v-expansion-panel-header>
                <v-expansion-panel-content color="white" style="color: #333;">
                  <v-card-text>
                    The challenge is for students 8-18 years of age. The questions are the same for all contestants and are not differentiated by age.                   </v-card-text>
                </v-expansion-panel-content>
              </v-expansion-panel>

              <v-expansion-panel>
                <v-expansion-panel-header color="cwhqBlue">How much time do you have to answer a question? </v-expansion-panel-header>
                <v-expansion-panel-content color="white" style="color: #333;">
                  <v-card-text>
                    You have until the Apr 25 11:59PM  to answer the first 21 questions. You can start anytime up until then.
                  </v-card-text>
                </v-expansion-panel-content>
              </v-expansion-panel>

              <v-expansion-panel>
                <v-expansion-panel-header color="cwhqBlue">Can I answer questions more than once? </v-expansion-panel-header>
                <v-expansion-panel-content color="white" style="color: #333;">
                  <v-card-text>
                    Yes, you have unlimited tries to answer a question correctly. However, there is a cooling off period of 30 minutes after every 3 incorrect answers.
                  </v-card-text>
                </v-expansion-panel-content>
              </v-expansion-panel>

              <v-expansion-panel>
                <v-expansion-panel-header color="cwhqBlue">What skills do I need to have to attempt the questions? </v-expansion-panel-header>
                <v-expansion-panel-content color="white" style="color: #333;">
                  <v-card-text>
                    You only need a beginner’s Python or JavaScript knowledge to participate.
                  </v-card-text>
                </v-expansion-panel-content>
              </v-expansion-panel>

              <v-expansion-panel>
                <v-expansion-panel-header color="cwhqBlue">How is the winner determined? </v-expansion-panel-header>
                <v-expansion-panel-content color="white" style="color: #333;">
                  <v-card-text>
                    he 1st, 2nd, and 3rd place winners are determined by a public vote and review by our Wizard Panel. Any challengers who complete all 21 levels and the boss level question will be eligible to win.                   </v-card-text>
                </v-expansion-panel-content>
              </v-expansion-panel>

              <v-expansion-panel>
                <v-expansion-panel-header color="cwhqBlue">What is the boss/final question? </v-expansion-panel-header>
                <v-expansion-panel-content color="white" style="color: #333;">
                  <v-card-text>
                    The final question is a test of your coding skills which requires you to submit a piece of code that gives the correct output. The programs with the correct output will be posted for public vote. The top 10 contestants with the highest number of votes will have their program reviewed and graded by the Wizard Panel. The Wizard Panel will award the top 3 places.
                  </v-card-text>
                </v-expansion-panel-content>
              </v-expansion-panel>
            </v-expansion-panels>
          </div>
        </page-card>
      </v-col>
    </v-row>
    <br />
    <br />
  </v-container>
</template>

<script>
import PageCard from '@/components/PageCard';
import FAQCard from './FAQCard';

export default {
  name: 'faq',
  components: {
    PageCard,
    FAQCard
  }
};
</script>

<style lang="scss" scoped>
.faq {
  padding-top: 12px;
  padding-bottom: 12px;
  font-family: 'Barlow', sans-serif !important;

  a {
    color: #202f50;
  }
}
</style>
