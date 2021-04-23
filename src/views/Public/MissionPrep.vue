<template>
  <v-container class="rules-container">
    <v-row align="center" justify="center">
      <v-col cols="12" sm="12" md="12">
        <page-card>
          <template #title>
            <v-toolbar-title>Final Mission Prep</v-toolbar-title>
          </template>
          <div class="faq">
            <v-card-text class="top-text">
              Adventurers, it’s almost time to battle Glorm. Before you do, read
              this final mission brief from the Allsnacks Alliance with details
              on your final feat. Please read through it carefully, as it
              contains information critical to your success in returning the
              Xolcron Crystal.
            </v-card-text>

            <h2>**URGENT COMMUNICATION**</h2>

            <v-card-text>
              <p>Date: 25 Apr 2021</p>
              <p>Mission Title: CLASSIFIED</p>
              <p>
                ELECTRONICALLY SIGNED: Allsnacks Alliance for Grand Poomba Fizzy
              </p>
            </v-card-text>
            <h3>Situation Report:</h3>
            <v-card-text>
              Now that you have gathered enough fuel throughout your 21-day
              journey across the galaxy, you can successfully infiltrate Glorm’s
              Galactic Garrison. Getting there is the easy part. Then, you’ll
              come face to face with Glorm. Glorm is the only thing standing
              between you and your objective - the Xolcron Crystal.
            </v-card-text>

            <v-card-text>
              To retrieve it, you’ll need to write a program in either Python or
              JavaScript. Details about the program you must write will be
              provided to you when you reach the Garrison on 28 Apr 2021. You
              will be given an online area to write and submit your code, and
              you will also be told if your answer is correct or incorrect. You
              will have until 30 Apr 2021 at 11:59 PM Central Time to submit
              your program.
            </v-card-text>
            <v-card-text>
              After you’ve submitted your program, citizens across the galaxy
              will have an opportunity to vote for the program they like the
              best. Public voting will be available from 3 May 2021 at 8:00 AM
              Central Time to 7 May 2021 at 11:59 PM Central Time. A link will
              be provided to see how many votes you’ve obtained throughout this
              time.
            </v-card-text>

            <v-card-text>
              After public voting concludes, the Galactic Wizard Panel (GWP)
              will convene. Made up of CodeWizardsHQ teachers, the GWP will
              review the submissions of the ten (10) adventurers with the
              highest number of votes. The Galactic Wizard Panel will announce
              the winner of the 2021 CodeWizardsHQ Code Challenge on 14 May
              2021.
            </v-card-text>
            <h3>How you will be evaluated by the Galactic Wizard Panel:</h3>
            <v-card-text>
              If your code is in the top ten of vote-getters, you will be
              eligible for the grand prize. The Galactic Wizard Panel (GWP) is
              looking for the most well-rounded submission. The GWP will
              evaluate your work based on program execution time and code
              quality. Each program will be timed on how long it takes your
              program to solve the problem, and you should aim to submit a
              program that has the lowest execution time possible, while also
              following the instructions for the Boss Level. The disparity in
              program execution time between Python and JavaScript will be
              considered.. You should also conduct research online about code
              quality to make sure your submission is well-rounded and follows
              coding best practices.
            </v-card-text>

            <img
              src="https://codewizardshq.com/wp-content/uploads/2021/04/rubric-challenge.jpg"
            />

            <v-card-text>
              Good luck, adventurer!
            </v-card-text>

            <h2>**END OF MESSAGE**</h2>
          </div>
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
  name: "mission",
  components: {
    PageCard
  }
};
</script>

<style lang="scss" scoped>
.rules-container {
  margin-top: 25px;

  .top-text {
    width: 700px;
    font-family: "Oxygen";
  }

  .faq {
    display: flex;
    flex-direction: column;
    align-items: center;
    font-family: "Courier New", Courier, monospace;

    h3 {
      text-decoration: underline;
    }
  }
}
</style>
