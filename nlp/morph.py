# Tiny lemma rules (classical style)
IRREGULAR = {
    "teaches": "teach",
    "taught": "teach",
    "professors": "professor",
    "professor's": "professor",
    "buildings": "building",
    "courses": "course",
}

def lemmatize(token: str) -> str:
    if token in IRREGULAR:
        return IRREGULAR[token]
    # plural nouns (basic)
    if token.endswith("ies") and len(token) > 3:
        return token[:-3] + "y"
    if token.endswith("s") and len(token) > 3 and not token.endswith("ss"):
        return token[:-1]
    # past tense -ed
    if token.endswith("ed") and len(token) > 3:
        return token[:-2]
    # present participle -ing (rough)
    if token.endswith("ing") and len(token) > 4:
        return token[:-3]
    return token

def normalize(tokens):
    return [lemmatize(t) for t in tokens]
