from fastapi import APIRouter, Request, Response, HTTPException, Query
from fastapi.responses import JSONResponse, PlainTextResponse
from datetime import datetime
from dicttoxml import dicttoxml

router = APIRouter()

quotes = [
    {
        "id": 1,
        "quote": "Do. Or do not. There is no try.",
        "character": "Yoda",
        "category": "wisdom",
        "episode": "The Empire Strikes Back",
        "source": {"movie": "The Empire Strikes Back", "scene_url": "https://starwars.com/empire/yoda"},
    },
    {
        "id": 2,
        "quote": "I’ve got a bad feeling about this.",
        "character": "Various",
        "category": "humor",
        "episode": "Multiple",
        "source": {"movie": "Various", "scene_url": "https://starwars.com/recurring/badfeeling"},
    },
    {
        "id": 3,
        "quote": "The Force will be with you. Always.",
        "character": "Obi-Wan Kenobi",
        "category": "wisdom",
        "episode": "A New Hope",
        "source": {"movie": "A New Hope", "scene_url": "https://starwars.com/anewhope/obiwan"},
    },
    {
        "id": 4,
        "quote": "It's a trap!",
        "character": "Admiral Ackbar",
        "category": "humor",
        "episode": "Return of the Jedi",
        "source": {"movie": "Return of the Jedi", "scene_url": "https://starwars.com/jedi/ackbar"},
    },
    {
        "id": 5,
        "quote": "I am your father.",
        "character": "Darth Vader",
        "category": "drama",
        "episode": "The Empire Strikes Back",
        "source": {"movie": "The Empire Strikes Back", "scene_url": "https://starwars.com/empire/vader"},
    },
    {
        "id": 6,
        "quote": "Never tell me the odds!",
        "character": "Han Solo",
        "category": "humor",
        "episode": "The Empire Strikes Back",
        "source": {"movie": "The Empire Strikes Back", "scene_url": "https://starwars.com/empire/han"},
    },
    {
        "id": 7,
        "quote": "Your focus determines your reality.",
        "character": "Qui-Gon Jinn",
        "category": "wisdom",
        "episode": "The Phantom Menace",
        "source": {"movie": "The Phantom Menace", "scene_url": "https://starwars.com/menace/focus"},
    },
    {
        "id": 8,
        "quote": "I find your lack of faith disturbing.",
        "character": "Darth Vader",
        "category": "drama",
        "episode": "A New Hope",
        "source": {"movie": "A New Hope", "scene_url": "https://starwars.com/anewhope/vader"},
    },
    {
        "id": 9,
        "quote": "I love you. I know.",
        "character": "Leia & Han",
        "category": "romance",
        "episode": "The Empire Strikes Back",
        "source": {"movie": "The Empire Strikes Back", "scene_url": "https://starwars.com/empire/love"},
    },
    {
        "id": 10,
        "quote": "Stay on target.",
        "character": "Gold Five",
        "category": "inspiration",
        "episode": "A New Hope",
        "source": {"movie": "A New Hope", "scene_url": "https://starwars.com/anewhope/target"},
    },
]

@router.get("/quote")
async def get_quotes(
    format: str = Query("json"),
    character: str = None,
    category: str = None,
    page: int = 1,
    size: int = 5,
):
    if format not in {"json", "text", "xml"}:
        raise HTTPException(status_code=400, detail="Unsupported format")

    filtered = quotes
    if character:
        filtered = [q for q in filtered if q["character"].lower() == character.lower()]
    if category:
        filtered = [q for q in filtered if q["category"].lower() == category.lower()]

    start = (page - 1) * size
    end = start + size
    paged_quotes = filtered[start:end]

    payload = {
        "version": "v3",
        "timestamp": datetime.utcnow().isoformat(),
        "page": page,
        "size": size,
        "total": len(filtered),
        "quotes": paged_quotes,
    }

    if format == "json":
        return JSONResponse(content=payload)
    elif format == "text":
        lines = [f"{q['quote']} – {q['character']}" for q in paged_quotes]
        return PlainTextResponse("\n".join(lines))
    elif format == "xml":
        xml_bytes = dicttoxml(payload, custom_root="response", attr_type=False)
        return Response(content=xml_bytes, media_type="application/xml")


@router.get("/quote/{quote_id}")
async def get_quote_by_id(quote_id: int, format: str = Query("json")):
    if format not in {"json", "text", "xml"}:
        raise HTTPException(status_code=400, detail="Unsupported format")

    match = next((q for q in quotes if q["id"] == quote_id), None)
    if not match:
        raise HTTPException(status_code=404, detail="Quote not found")

    payload = {
        "version": "v3",
        "timestamp": datetime.utcnow().isoformat(),
        "quote": match,
    }

    if format == "json":
        return JSONResponse(content=payload)
    elif format == "text":
        return PlainTextResponse(f"{match['quote']} – {match['character']}")
    elif format == "xml":
        xml_bytes = dicttoxml(payload, custom_root="response", attr_type=False)
        return Response(content=xml_bytes, media_type="application/xml")