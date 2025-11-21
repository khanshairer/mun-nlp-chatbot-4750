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
addMsg("Hello! I can help with: where a building/room is, who teaches a course, and basic course info.\nTry: 'Where is EN-1051?', 'Who teaches COMP 4750?', or 'Info about CS 2000'.", 'bot');
