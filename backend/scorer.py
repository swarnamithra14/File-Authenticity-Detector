def calculate_score(expected, actual, mime_type, metadata, hidden_result):
    score = 0
    reasons = []

    # ❌ Extension mismatch
    if expected != actual:
        score += 30
        reasons.append("Extension does not match actual file type")

    # ❌ MIME mismatch
    if mime_type != "Unknown" and actual not in mime_type.upper():
        score += 20
        reasons.append("MIME type mismatch")

    # ❌ Metadata warning
    if "Warning" in metadata or "Error" in metadata:
        score += 20
        reasons.append("Metadata inconsistency detected")

    # ❌ Hidden content
    if "Multiple" in hidden_result:
        score += 40
        reasons.append("Hidden or embedded file detected")

    # Cap score at 100
    score = min(score, 100)

    return score, reasons