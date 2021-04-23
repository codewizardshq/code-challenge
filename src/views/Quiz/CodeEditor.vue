<template>
  <div class="codemirror">
    <!-- codemirror -->
    <codemirror v-model="code" :options="cmOption"></codemirror>
  </div>
</template>

<script>
// language
import "codemirror/mode/vue/vue.js";
import "codemirror/mode/javascript/javascript.js";
import "codemirror/mode/python/python.js";

// theme css
import "codemirror/theme/base16-dark.css";

// active-line.js
import "codemirror/addon/selection/active-line.js";

// styleSelectedText
import "codemirror/addon/selection/mark-selection.js";
import "codemirror/addon/search/searchcursor.js";

// highlightSelectionMatches
import "codemirror/addon/scroll/annotatescrollbar.js";
import "codemirror/addon/search/matchesonscrollbar.js";
import "codemirror/addon/search/searchcursor.js";
import "codemirror/addon/search/match-highlighter.js";

// keyMap
import "codemirror/mode/clike/clike.js";
import "codemirror/addon/edit/matchbrackets.js";
import "codemirror/addon/comment/comment.js";
import "codemirror/addon/dialog/dialog.js";
import "codemirror/addon/dialog/dialog.css";
import "codemirror/addon/search/searchcursor.js";
import "codemirror/addon/search/search.js";
import "codemirror/keymap/sublime.js";

// foldGutter
import "codemirror/addon/fold/foldgutter.css";
import "codemirror/addon/fold/brace-fold.js";
import "codemirror/addon/fold/comment-fold.js";
import "codemirror/addon/fold/foldcode.js";
import "codemirror/addon/fold/foldgutter.js";
import "codemirror/addon/fold/indent-fold.js";
import "codemirror/addon/fold/markdown-fold.js";
import "codemirror/addon/fold/xml-fold.js";

export default {
  props: ["value", "language"],
  computed: {
    cmOption() {
      return {
        tabSize: 4,
        foldGutter: true,
        styleActiveLine: true,
        lineNumbers: true,
        line: true,
        keyMap: "sublime",
        mode: this.language,
        theme: "base16-dark"
      };
    }
  },
  watch: {
    value(val) {
      if (this.code !== val) {
        this.code = val;
      }
    },
    code(val) {
      if (this.value !== val) {
        this.$emit("input", val);
      }
    }
  },
  data() {
    return {
      code: this.value
    };
  }
};
</script>

<style lang="scss" scoped>
// needs to be deep to affect child component
.codemirror::v-deep .CodeMirror {
  height: 600px;
}
</style>
