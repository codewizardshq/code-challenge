<template>
  <v-container>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="12" md="12">
        <page-card>
          <template #title>
            <v-toolbar-title>7 Tips and Tricks for Getting Challenge Votes</v-toolbar-title>
          </template>
          <div class="faq">
            <v-card-text>
              You’ve vanquished he evil dragon and made it to the final phase of The Dragon Quest. Now is the time to gather votes to win the grand prize! Here
              are a few easy, simple strategies to get your challenge votes. Use these 7 tips and tricks to get the most votes possible. Find and share your
              code at <a href="/voting">challenge.codewizardshq.com/voting</a>
            </v-card-text>

            <v-card-title>
              1. Ask Your Family Members to Be Your Ambassadors
            </v-card-title>

            <v-card-text>
              Your family is there to help and support you. They’re the first people you should ask to vote for you in your quest. Mom, dad, aunts, and uncles
              can all help.
            </v-card-text>
            <v-card-text>
              It’s probably pretty easy to get in touch with them too. Send an email, call, or text them and let them know you’re competing in The Dragon Quest
              and need their votes.
            </v-card-text>

            <v-card-title>
              2. Ask Friends in Groups Online and Offline
            </v-card-title>

            <v-card-text>
              You probably have friends in lots of places you haven’t thought of! Are you on a team or in a club?
            </v-card-text>
            <v-card-text>
              If you play sports, are in a dance class, scouts, or any other group, reach out to them by email, phone, or social media and ask for their vote.
              You might even reach out to other chapters in our area to help spread the word.
            </v-card-text>

            <v-card-title>
              3. Put social media to work for you
            </v-card-title>

            <v-card-text>
              Facebook, Twitter, and Instagram are great places to share your quest and connect with people while you’re at home. Post one of these graphics or
              make your own asking for votes.
            </v-card-text>
            <v-card-text class="text-center">
              <img class="mr-4" width="300" src="/images/vote-graphic-2.jpg" />
              <img width="300" src="/images/vote-graphic-1.jpg" />
            </v-card-text>
            <v-card-text>
              If you have a website or blog, you should create a post or a page and link it to the challenge voting page. If you’re playing online games, post
              about your quest in the game chat for help.
            </v-card-text>

            <v-card-title>
              4. Post a Picture or Video Sharing Your Journey
            </v-card-title>

            <v-card-text>
              Take a picture of yourself coding or a short video. Tell the audience about your coding journey over the last 21 days and why they should vote for
              you.
            </v-card-text>
            <v-card-text>
              Your friends and family are more likely to support you if they can see you! It’s also a fun way to connect while you’re apart and let them know
              what you’ve been up to.
            </v-card-text>

            <v-card-title>
              5. Make a class announcement
            </v-card-title>

            <v-card-text>
              First, ask your teacher if you can make a short announcement in class. The best time is at the beginning or end of class.
            </v-card-text>
            <v-card-text>
              If your teacher allows it, make a short announcement in each of your classes. It only takes 30 seconds, let your classmates know you’re competing
              in the dragon quest and need their votes. Your teacher might even be willing to share it in his or her other classes if you ask nicely.
            </v-card-text>

            <v-card-title>
              6. Post a Flyer
            </v-card-title>

            <v-card-text>
              Create a funny, cute, or cool flyer that includes 1) the voting page link and 2) your username. You can use
              <a href="https://www.canva.com/">Canva</a> for free to create professional flyers and download them for digital or print.
            </v-card-text>
            <v-card-text>
              Normally, anywhere in your community where people congregate and flyers are allowed would be good to post! While we are on lockdown, consider
              online message boards like NextDoor.
            </v-card-text>

            <v-card-title>
              7. Ask your friends to do #1-6
            </v-card-title>

            <v-card-text>
              After your friends and family have voted, ask them to share with their family and friends too!
            </v-card-text>
            <v-card-text>
              If they are in any groups, clubs, or classes, they can support your quest. Did you create a post or graphic? Give that to your supporters so they
              can share it. The ripple effect will mean more votes for you.
            </v-card-text>
            <v-card-text>
              These tips and tricks should boost you to the top of the challenge rankings in no time. For all the above, make sure you share the voting page at
              challenge.codewizardshq.com/voting
            </v-card-text>
            <v-card-text>
              <b>To vote, friends and family simply search for your username on the voting page and click “vote”.</b>
            </v-card-text>
            <v-card-text>
              Remember, you only have until April 30 to collect your votes.
            </v-card-text>
            <v-card-text>
              Good luck, young pilgrim!
            </v-card-text>
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
    FAQCard,
  },
};
</script>

<style lang="scss" scoped>
.faq {
  padding-top: 12px;
  padding-bottom: 12px;
  font-family: 'Barlow', sans-serif !important;
}
</style>
