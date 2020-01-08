<template>
  <v-menu
    ref="menu1"
    v-model="showPicker"
    :close-on-content-click="false"
    transition="scale-transition"
    offset-y
    max-width="290px"
    min-width="290px"
    elevation="0"
    nudge-bottom
    style="margin-top:50px;"
  >
    <template v-slot:activator="{ on }">
      <v-text-field
        autocomplete="off"
        v-model="formattedDate"
        :label="label"
        hint="MM/DD/YYYY"
        placeholder="MM/DD/YYYY"
        prepend-icon="mdi-calendar"
        v-mask="mask"
        v-on="on"
      ></v-text-field>
    </template>
    <v-date-picker
      :max="new Date().toISOString().substr(0, 10)"
      v-model="date"
      @input="
        showPicker = false;
        formattedDate = formatDate(date);
      "
    ></v-date-picker>
  </v-menu>
</template>

<script>
import { mask } from "vue-the-mask";

const timeFormatRegex = /^(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/|-|\.)(?:0?[13-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$/;
export default {
  name: "date-of-birth-field",
  props: ["value", "label"],
  directives: {
    mask
  },
  data() {
    return {
      mask: "##/##/####",
      showPicker: false,
      date: null,
      formattedDate: null
    };
  },
  watch: {
    value(val) {
      if (this.date !== val) {
        this.date = val;
      }
    },
    date(val) {
      if (this.value !== val) {
        this.$emit("input", val);
      }
    },
    formattedDate(val) {
      if (timeFormatRegex.test(val)) {
        const nextDate = this.parseDate(val);
        this.date = nextDate;
      }
    }
  },
  mounted() {
    this.date = this.value;
    this.formattedDate = this.formatDate(this.date);
  },
  methods: {
    formatDate(date) {
      if (!date) return null;

      const [year, month, day] = date.split("-");
      return `${month}/${day}/${year}`;
    },
    parseDate(date) {
      if (!date) return null;

      const [month, day, year] = date.split("/");
      return `${year}-${month.padStart(2, "0")}-${day.padStart(2, "0")}`;
    }
  }
};
</script>

<style scoped>
.v-menu__content {
  box-shadow: none;
}
</style>
