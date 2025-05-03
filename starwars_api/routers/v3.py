from fastapi import APIRouter, Query, Request, Response
from fastapi.responses import JSONResponse, PlainTextResponse
from typing import List, Optional
from datetime import datetime

router = APIRouter()

quotes = [
    {
        "id": 1,
        "quote": "Do. Or do not. There is no try.",
        "character": "Yoda",
        "category": "wisdom",
        "episode": "The Empire Strikes Back",
        "source": {"movie": "The Empire Strikes Back", "scene_url": "https://starwars.com/empire/yoda-lesson"}
    },
    {
        "id": 2,
        "quote": "I am your father.",
        "character": "Darth Vader",
        "category": "reveal",
        "episode": "The Empire Strikes Back",
        "source": {"movie": "The Empire Strikes Back", "scene_url": "https://starwars.com/empire/reveal"}
    },
    {
        "id": 3,
        "quote": "Never tell me the odds.",
        "character": "Han Solo",
        "category": "humor",
        "episode": "The Empire Strikes Back",
        "source": {"movie": "The Empire Strikes Back", "scene_url": "https://starwars.com/empire/han-odds"}
    },
    {
        "id": 4,
        "quote": "It’s a trap!",
        "character": "Admiral Ackbar",
        "category": "alert",
        "episode": "Return of the Jedi",
        "source": {"movie": "Return of the Jedi", "scene_url": "https://starwars.com/jedi/trap"}
    },
    {
        "id": 5,
        "quote": "The Force will be with you. Always.",
        "character": "Obi-Wan Kenobi",
        "category": "wisdom",
        "episode": "A New Hope",
        "source": {"movie": "A New Hope", "scene_url": "https://starwars.com/hope/obiwan-force"}
    },
    {
        "id": 6,
        "quote": "I’ve got a bad feeling about this.",
        "character": "Multiple",
        "category": "foreshadowing",
        "episode": "All",
        "source": {"movie": "Various", "scene_url": "https://starwars.com/feeling"}
    },
    {
        "id": 7,
        "quote": "So this is how liberty dies… with thunderous applause.",
        "character": "Padmé Amidala",
        "category": "drama",
        "episode": "Revenge of the Sith",
        "source": {"movie": "Revenge of the Sith", "scene_url": "https://starwars.com/sith/liberty"}
    },
    {
        "id": 8,
        "quote": "Your focus determines your reality.",
        "character": "Qui-Gon Jinn",
        "category": "wisdom",
        "episode": "The Phantom Menace",
        "source": {"movie": "The Phantom Menace", "scene_url": "https://starwars.com/menace/focus"}
    },
    {
        "id": 9,
        "quote": "You were the chosen one!",
        "character": "Obi-Wan Kenobi",
        "category": "emotion",
        "episode": "Revenge of the Sith",
        "source": {"movie": "Revenge of the Sith", "scene_url": "https://starwars.com/sith/chosen"}
    },
    {
        "id": 10,
        "quote": "Let the past die. Kill it if you have to.",
        "character": "Kylo Ren",
        "category": "darkness",
        "episode": "The Last Jedi",
        "source": {"movie": "The Last Jedi", "scene_url": "https://starwars.com/jedi/kylo-past"}
    },
]

@router.get("/quote", summary="Get a filtered, paginated Star Wars quote", tags=["Quotes"])
def get_quotes(
    request: Request,
    character: Optional[str] = Query(None, description="Filter by character"),
    category: Optional[str] = Query(None, description="Filter by category"),
    page: int = Query(1, ge=1),
    size: int = Query(5, ge=1, le=10),
    format: Optional[str] = Query("json", description="Response format: json or text")
) -> Response:
    filtered = quotes
    if character:
        filtered = [q for q in filtered if q["character"].lower() == character.lower()]
    if category:
        filtered = [q for q in filtered if q["category"].lower() == category.lower()]

    start = (page - 1) * size
    end = start + size
    paginated = filtered[start:end]

    api_version = "v3"
    timestamp = datetime.utcnow().isoformat()

    # Add rate limiting headers
    headers = {
        "X-RateLimit-Limit": "60",
        "X-RateLimit-Remaining": "59"  # Example only
    }

    if format == "text":
        content = (
            f"API Version: {api_version}\n"
            f"Timestamp: {timestamp}\n\n" +
            "\n\n".join([f"{q['character']}: {q['quote']}" for q in paginated])
        )
        return PlainTextResponse(content, headers=headers)

    return JSONResponse(
        content={
            "version": api_version,
            "timestamp": timestamp,
            "page": page,
            "size": size,
            "total": len(filtered),
            "quotes": paginated
        },
        headers=headers
    )