const storageKey = "rank";

function networkDelay(func) {
  return new Promise(resolve => {
    setTimeout(async function () {
      resolve(await func());
    }, 300 + Math.random() * 1000);
  });
}

const quizes = [
  {
    question: "<center>Welcome to the CodeWizardsHQ Code Challenge.<br \> <br\> Type \"Okay!\" to get started</center>",
    answer: "Okay!"
  },
  {
    question: "What is 2 + 5",
    answer: "7"
  },
  {
    question: "<center>Thanks for taking the CodeWizardsHQ Code Challenge.<br \> <br\> Type \"Restart!\" to get restart</center>",
    answer: "Restart!"
  },
]

async function get() {
  return networkDelay(async () => {
    let rank = localStorage.getItem(storageKey);
    rank = !!rank ? parseInt(localStorage.getItem(storageKey)) : 0;
    if (rank > quizes.length - 1) {
      rank = 0;
    }
    return {
      rank: rank,
      question: quizes[rank].question
    }
  });
}

async function submit(answer) {
  return networkDelay(async () => {
    const rank = (await get()).rank;
    if (quizes[rank].answer == answer) {
      localStorage.setItem(storageKey, rank + 1);
      return true;
    }
    return false;
  });
}

export default {
  get,
  submit
}