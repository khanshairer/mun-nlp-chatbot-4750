const chatlog = document.getElementById("chatlog");
const input = document.getElementById("msg");
const sendBtn = document.getElementById("send");
const suggestionsDiv = document.getElementById("suggestions");

function addMsg(text, who = "bot") {
  const div = document.createElement("div");
  div.className = "msg " + who;
  div.textContent = text;
  chatlog.appendChild(div);
  chatlog.scrollTop = chatlog.scrollHeight;
}

async function send() {
  const text = input.value.trim();
  if (!text) return;
  addMsg(text, "user");
  input.value = "";
  clearSuggestions();
  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text })
    });
    const data = await res.json();
    addMsg(data.reply || "(no reply)", "bot");
  } catch (e) {
    addMsg("Network error. Please try again.", "bot");
  }
}

// Example buttons
document.querySelectorAll(".example-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    const q = btn.getAttribute("data-example");
    input.value = q;
    input.focus();
    send();
  });
});

// Autocomplete
let suggestTimer = null;

function clearSuggestions() {
  suggestionsDiv.innerHTML = "";
  suggestionsDiv.style.display = "none";
}

function showSuggestions(list) {
  if (!list || !list.length) {
    clearSuggestions();
    return;
  }
  suggestionsDiv.innerHTML = "";
  list.forEach(name => {
    const item = document.createElement("div");
    item.className = "suggestion-item";
    item.textContent = name;
    item.addEventListener("click", () => {
      input.value = "Tell me about " + name;
      clearSuggestions();
      input.focus();
    });
    suggestionsDiv.appendChild(item);
  });
  suggestionsDiv.style.display = "block";
}

input.addEventListener("input", () => {
  const text = input.value.trim();
  if (suggestTimer) clearTimeout(suggestTimer);
  if (text.length < 2) {
    clearSuggestions();
    return;
  }
  suggestTimer = setTimeout(async () => {
    try {
      const res = await fetch("/suggest?q=" + encodeURIComponent(text));
      if (!res.ok) {
        clearSuggestions();
        return;
      }
      const names = await res.json();
      showSuggestions(names);
    } catch (e) {
      clearSuggestions();
    }
  }, 200);
});

input.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    send();
  }
});

// initial greeting
addMsg(
  "Hello! I can help you with faculty information at MUN.\n\n" +
  "You can ask about any professor’s:\n" +
  "• Email\n" +
  "• Office / Room\n" +
  "• Phone Number\n" +
  "• Position / Title\n" +
  "• Faculty / Department\n" +
  "• Full summary of all details\n\n" +
  "Examples:\n" +
  "• “What is Dr. Todd Wareham’s email?”\n" +
  "• “Where is Professor Jane Smith’s office?”\n" +
  "• “What is Dr. X’s phone number?”\n" +
  "• “Which faculty is Prof. Y in?”\n" +
  "• “Tell me information about Dr. Z.”",
  "bot"
);

sendBtn.addEventListener("click", send);
