from nlp.tokenizer import tokenize
from nlp.morph import normalize
from nlp.intent import detect_intent, extract_prof_name, extract_office_code
from nlp.fsa import FSA
from db import find_prof_by_name, find_prof_by_office, find_prof_by_name_fuzzy

HELP_TEXT = (
    "I can help you with faculty information at MUN.\n\n"
    "You can ask about any professor’s:\n"
    "• Email\n"
    "• Office / Room\n"
    "• Phone Number\n"
    "• Position / Title\n"
    "• Faculty / Department\n"
    "• Full summary of all details\n\n"
    "Examples:\n"
    "• “What is Dr. Todd Wareham’s email?”\n"
    "• “Where is Professor Jane Smith’s office?”\n"
    "• “What is Dr. X’s phone number?”\n"
    "• “Which faculty is Prof. Y in?”\n"
    "• “Tell me information about Dr. Z.”"
)


class ChatEngine:
    def __init__(self):
        self.fsa = FSA()

    def respond(self, text: str):
        if not text:
            return (
                "Please type a question, e.g., 'What is Dr. Todd Wareham’s email?'.",
                self.fsa.state,
            )

        toks = tokenize(text)
        _lemmas = normalize(toks)

        intent = detect_intent(text)
        state = self.fsa.transition(intent)

        # ----- Basic dialogue intents -----
        if intent == "GREET":
            return ("Hello! " + HELP_TEXT, state)
        if intent == "HELP":
            return (HELP_TEXT, state)
        if intent == "EXIT":
            return ("Goodbye!", state)

        # If intent UNKNOWN but we can guess a name, treat as summary
        if intent == "UNKNOWN":
            guess = extract_prof_name(text)
            if guess:
                intent = "PROF_SUMMARY"

        # ----- Office → professor ("Who's room is EN-2008?") -----
        if intent == "PROF_BY_ROOM":
            code = extract_office_code(text)
            if not code:
                return ("Which room code? For example: EN-2008.", state)
            profs = find_prof_by_office(code)
            if not profs:
                return (f"I couldn't find any professor with office {code}.", state)
            if len(profs) == 1:
                p = profs[0]
                return (
                    f"{p['office']} belongs to {p['name']} "
                    f"({p['position']}, {p['faculty']}).",
                    state,
                )
            lines = [
                f"{p['office']}: {p['name']} ({p['position']}, {p['faculty']})"
                for p in profs
            ]
            return ("\n".join(lines), state)

        # ----- Professor-specific intents -----
        if intent in (
            "PROF_EMAIL",
            "PROF_OFFICE",
            "PROF_PHONE",
            "PROF_POSITION",
            "PROF_FACULTY",
            "PROF_SUMMARY",
        ):
            name = extract_prof_name(text)
            if not name:
                return ("Which professor? Please include their full name.", state)

            note = ""
            profs = find_prof_by_name(name)

            if not profs:
                # Fuzzy fallback
                profs, corrected = find_prof_by_name_fuzzy(name)
                if not profs:
                    return (
                        f"No professor matches '{name}'. Try their official name.",
                        state,
                    )
                if corrected and corrected != name:
                    note = f"(Assuming you meant {corrected}.)\n"

            if len(profs) > 1:
                names = ", ".join(p["name"] for p in profs)
                return (f"I found multiple matches: {names}. Please be more specific.", state)

            p = profs[0]

            if intent == "PROF_EMAIL":
                return (note + f"{p['name']}'s email: {p['email']}", state)

            if intent == "PROF_OFFICE":
                return (note + f"{p['name']}'s office: {p['office']}", state)

            if intent == "PROF_PHONE":
                return (note + f"{p['name']}'s phone number: {p['phone']}", state)

            if intent == "PROF_POSITION":
                return (note + f"{p['name']} is a {p['position']}", state)

            if intent == "PROF_FACULTY":
                return (note + f"{p['name']} belongs to: {p['faculty']}", state)

            if intent == "PROF_SUMMARY":
                return (
                    note
                    + f"Information about {p['name']}:\n"
                    f"- Position: {p['position']}\n"
                    f"- Email: {p['email']}\n"
                    f"- Office: {p['office']}\n"
                    f"- Phone: {p['phone']}\n"
                    f"- Faculty: {p['faculty']}",
                    state,
                )

        # ----- Fallback -----
        return ("Sorry, I didn't understand.\n" + HELP_TEXT, state)
