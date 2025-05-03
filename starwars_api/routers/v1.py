from fastapi import APIRouter
import random

router = APIRouter()

QUOTES = [
    "Do. Or do not. There is no try.",
    "I’ve got a bad feeling about this.",
    "Never tell me the odds!",
    "It’s a trap!",
    "I find your lack of faith disturbing.",
    "The Force will be with you. Always.",
    "Help me, Obi-Wan Kenobi. You’re my only hope.",
    "Your focus determines your reality.",
    "Now, young Skywalker, you will die.",
    "This is the way."
]

@router.get("/quote", tags=["Quotes"])
def get_quote():
    return {"quote": random.choice(QUOTES)}