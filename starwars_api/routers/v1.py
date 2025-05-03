from fastapi import APIRouter
import random

router = APIRouter()

quotes = [
    "Do. Or do not. There is no try.",
    "I’ve got a bad feeling about this.",
    "It’s a trap!",
    "The Force will be with you. Always.",
    "Never tell me the odds!",
    "I find your lack of faith disturbing.",
    "So this is how liberty dies… with thunderous applause.",
    "I am your father.",
    "Your focus determines your reality.",
    "Now, young Skywalker, you will die."
]

@router.get("/quote")
def get_star_wars_quote():
    return {"quote": random.choice(quotes)}
