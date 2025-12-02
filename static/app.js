const chatlog = document.getElementById('chatlog');
const input = document.getElementById('msg');
const sendBtn = document.getElementById('send');

function addMsg(text, who='bot'){
  const div = document.createElement('div');
  div.className = 'msg ' + who;
  div.textContent = text;
  chatlog.appendChild(div);
  chatlog.scrollTop = chatlog.scrollHeight;
}

async function send(){
  const text = input.value.trim();
  if(!text) return;
  addMsg(text, 'user');
  input.value = '';
  try {
    const res = await fetch('/chat', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({message: text})
    });
    const data = await res.json();
    addMsg(data.reply || '(no reply)', 'bot');
  } catch (e){
    addMsg('Network error. Please try again.', 'bot');
  }
}

sendBtn.addEventListener('click', send);
input.addEventListener('keydown', (e)=>{
  if(e.key === 'Enter'){ send(); }
});

// greeting
addMsg("Hello! I can help you with faculty information at MUN.\n\n" +
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
"bot");
