import re

# Keywords
EMAIL_KW    = re.compile(r"\b(email|e-mail|contact)\b", re.IGNORECASE)
OFFICE_KW   = re.compile(r"\b(office|room|rm)\b", re.IGNORECASE)
PHONE_KW    = re.compile(r"\b(phone|telephone|call)\b", re.IGNORECASE)
POSITION_KW = re.compile(r"\b(position|title|job|role)\b", re.IGNORECASE)
FACULTY_KW  = re.compile(r"\b(faculty|department|dept|school)\b", re.IGNORECASE)
INFO_KW     = re.compile(r"\b(info|information|details|about)\b", re.IGNORECASE)

ROOM_OWNER_KW = re.compile(r"\bwho('s|se)?\b", re.IGNORECASE)
ROOM_CODE     = re.compile(r"\b([A-Za-z]{2}-\d{3,4})\b", re.IGNORECASE)


def detect_intent(text: str):
    text = text.replace("’", "'")

    if ROOM_OWNER_KW.search(text) and ROOM_CODE.search(text):
        return "PROF_BY_ROOM"

    # 2) Faculty detail intents
    if EMAIL_KW.search(text):
        return "PROF_EMAIL"
    if OFFICE_KW.search(text):
        return "PROF_OFFICE"
    if PHONE_KW.search(text):
        return "PROF_PHONE"
    if POSITION_KW.search(text):
        return "PROF_POSITION"
    if FACULTY_KW.search(text):
        return "PROF_FACULTY"
    if INFO_KW.search(text):
        return "PROF_SUMMARY"

    # 3) Basic dialogue
    low = text.lower()
    if re.search(r"\b(hi|hello|hey)\b", low):
        return "GREET"
    if "help" in low:
        return "HELP"
    if re.search(r"\b(bye|exit|quit)\b", low):
        return "EXIT"

    return "UNKNOWN"

def _normalize_name(s: str) -> str:
    return " ".join(w.capitalize() for w in s.split())

def _clean_name_candidate(s: str) -> str | None:
    """
    Strip off leading/trailing junk words like:
    - leading: what, is, about, info, tell, me, who...
    - trailing: email, office, room, phone, faculty, in...
    """
    if not s:
        return None

    lead_stops = {
        "what", "is", "about", "info", "information", "details",
        "tell", "me", "who", "who's", "whos", "whose"
    }
    trail_stops = {
        "email", "office", "room", "phone", "number", "faculty",
        "dept", "department", "school", "in", "at"
    }

    tokens = s.split()
    # Strip leading junk
    while tokens and tokens[0].lower() in lead_stops:
        tokens.pop(0)
    # Strip trailing junk
    while tokens and tokens[-1].lower() in trail_stops:
        tokens.pop()

    if not tokens:
        return None

    return _normalize_name(" ".join(tokens))

def extract_prof_name(text: str):
    """
    Extract a professor name from many styles of queries, case-insensitive:
      - Dr. Todd Wareham
      - Professor Todd Wareham
      - Wareham's email
      - info about pranjal patra
      - tell me about hatcher
      - email for Todd Wareham
    """
    txt = text.replace("’", "'")

    # Dr./Professor First Last (case-insensitive)
    m = re.search(
        r"\b(Dr\.?|Professor|Prof)\s+([a-z][a-z]+(?:\s+[a-z][a-z]+)*)",
        txt,
        re.IGNORECASE,
    )
    if m:
        cleaned = _clean_name_candidate(m.group(2))
        if cleaned:
            return cleaned

    m = re.search(
        r"\b([a-z][a-z]+(?:\s+[a-z][a-z]+)*)'s\b",
        txt,
        re.IGNORECASE,
    )
    if m:
        cleaned = _clean_name_candidate(m.group(1))
        if cleaned:
            return cleaned

    m = re.search(
        r"\b(info|information|details|about)\s+([a-z][a-z]+(?:\s+[a-z][a-z]+)*)",
        txt,
        re.IGNORECASE,
    )
    if m:
        cleaned = _clean_name_candidate(m.group(2))
        if cleaned:
            return cleaned

    # 4) for/of NAME: "email for Todd Wareham", "office of Hatcher"
    m = re.search(
        r"\b(for|of)\s+([a-z][a-z]+(?:\s+[a-z][a-z]+)*)",
        txt,
        re.IGNORECASE,
    )
    if m:
        cleaned = _clean_name_candidate(m.group(2))
        if cleaned:
            return cleaned

    # 5) fallback: last alphabetic word of length >= 3
    words = re.findall(r"[a-zA-Z]{3,}", txt)
    if words:
        cleaned = _clean_name_candidate(words[-1])
        if cleaned:
            return cleaned

    return None

def extract_office_code(text: str):
    """
    Extracts a room code like EN-2008 from text.
    """
    m = ROOM_CODE.search(text.replace("’", "'"))
    if m:
        return m.group(1).upper()
    return None
