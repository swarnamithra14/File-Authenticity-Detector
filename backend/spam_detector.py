def analyze_spam(text):
    spam_keywords = [
    # 💰 Money / Offers
    "win", "free", "offer", "deal", "limited", "bonus",
    "prize", "cash", "reward", "earn", "income", "profit",

    # 🚨 Urgency / Pressure
    "urgent", "act now", "limited time", "expires soon",
    "hurry", "immediate", "don't miss", "final notice",

    # 🔗 Click / Actions
    "click", "click here", "visit link", "open now",
    "download", "subscribe", "buy now",

    # 🔐 Sensitive Info (Phishing)
    "password", "otp", "verify account", "login",
    "bank", "credit card", "debit card", "cvv",
    "security alert", "account suspended",

    # 💸 Scam Patterns
    "lottery", "jackpot", "guaranteed", "risk-free",
    "investment", "double your money", "no risk",
    "100% free", "no cost",

    # 📧 Email Spam Style
    "congratulations", "selected", "winner",
    "claim now", "exclusive", "special offer",

    # 🧠 Social Engineering
    "trust me", "confidential", "private",
    "urgent response", "verify immediately"
]

    text_lower = text.lower()

    found = []

    for word in spam_keywords:
        if word in text_lower:
            found.append(word)

    # score logic
    score = min(len(found) * 10, 100)

    if score > 60:
        result = "🚨 High Spam Content"
    elif score > 30:
        result = "⚠️ Moderate Spam Content"
    else:
        result = "✅ Safe Content"

    return result, score, found