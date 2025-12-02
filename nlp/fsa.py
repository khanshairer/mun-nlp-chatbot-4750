class DialogueState:
    START = "START"
    ASKING = "ASKING"
    ANSWERING = "ANSWERING"
    EXIT = "EXIT"

class FSA:
    def __init__(self):
        self.state = DialogueState.START

    def transition(self, intent: str):
        if self.state == DialogueState.START:
            self.state = DialogueState.ASKING
        elif self.state == DialogueState.ASKING:
            if intent == "EXIT":
                self.state = DialogueState.EXIT
            else:
                self.state = DialogueState.ANSWERING
        elif self.state == DialogueState.ANSWERING:
            if intent == "EXIT":
                self.state = DialogueState.EXIT
            else:
                self.state = DialogueState.ASKING
        return self.state
