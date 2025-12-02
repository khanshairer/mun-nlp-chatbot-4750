from db import find_prof_by_name

for q in ["Todd", "Wareham", "Todd Wareham"]:
    print(f"--- Searching for: {q!r}")
    rows = find_prof_by_name(q)
    for r in rows:
        print(" ", r["name"], "|", r["email"], "|", r["faculty"])
    if not rows:
        print("  (no matches)")
