import re
from . import insights

def answer(question: str):
    q = question.lower()
    if "total" in q and ("month" in q or "this month" in q):
        s = insights.summary("month")
        return {"answer": f"Total spend since {s['period_start']} is {s['total_spend']}", "explain": s}
    m = re.search(r"spent on (.+?) (?:this|last)?\s*month", q)
    if m:
        cat = m.group(1)
        s = insights.summary("month")
        return {"answer": f"(Prototype) {cat} spend ≈ {s['total_spend']}", "explain": s}
    return {"answer": "Sorry, I can only answer a few prototype questions yet.",
            "explain": {"supported": ["total spend this month", "spent on <category> this month"]}}
