from fastapi import APIRouter
from datetime import datetime
import random

router = APIRouter()

quotes = [
    "I find your lack of faith disturbing.",
    "Never tell me the odds.",
    "In my experience, there is no such thing as luck.",
    "So this is how liberty dies… with thunderous applause.",
    "Let the past die. Kill it if you have to.",
]

@router.get("/quote")
def get_quote():
    return {
        "quote": random.choice(quotes),
        "version": "v2",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }