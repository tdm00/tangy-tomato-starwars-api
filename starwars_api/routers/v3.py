from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse, Response
from typing import Optional, List
from datetime import datetime
from dicttoxml import dicttoxml

router = APIRouter()

QUOTES = [
    {
        "id": 1,
        "quote": "Do. Or do not. There is no try.",
        "character": "Yoda",
        "category": "wisdom",
        "episode": "The Empire Strikes Back",
        "source": {
            "movie": "The Empire Strikes Back",
            "scene_url": "https://starwars.com/empire/yoda"
        }
    },
    {
        "id": 2,
        "quote": "I’ve got a bad feeling about this.",
        "character": "Various",
        "category": "humor",
        "episode": "Multiple",
        "source": {
            "movie": "Various",
            "scene_url": "https://starwars.com/recurring/badfeeling"
        }
    },
    {
        "id": 3,
        "quote": "The Force will be with you. Always.",
        "character": "Obi-Wan Kenobi",
        "category": "wisdom",
        "episode": "A New Hope",
        "source": {
            "movie": "A New Hope",
            "scene_url": "https://starwars.com/anewhope/obiwan"
        }
    },
    {
        "id": 4,
        "quote": "It's a trap!",
        "character": "Admiral Ackbar",
        "category": "humor",
        "episode": "Return of the Jedi",
        "source": {
            "movie": "Return of the Jedi",
            "scene_url": "https://starwars.com/jedi/ackbar"
        }
    },
    {
        "id": 5,
        "quote": "I am your father.",
        "character": "Darth Vader",
        "category": "drama",
        "episode": "The Empire Strikes Back",
        "source": {
            "movie": "The Empire Strikes Back",
            "scene_url": "https://starwars.com/empire/vader"
        }
    },
    {
        "id": 6,
        "quote": "Your focus determines your reality.",
        "character": "Qui-Gon Jinn",
        "category": "wisdom",
        "episode": "The Phantom Menace",
        "source": {
            "movie": "The Phantom Menace",
            "scene_url": "https://starwars.com/menace/focus"
        }
    },
    {
        "id": 7,
        "quote": "This is the way.",
        "character": "The Mandalorian",
        "category": "loyalty",
        "episode": "The Mandalorian",
        "source": {
            "movie": "The Mandalorian",
            "scene_url": "https://starwars.com/mandalorian/way"
        }
    },
    {
        "id": 8,
        "quote": "Let the past die. Kill it if you have to.",
        "character": "Kylo Ren",
        "category": "drama",
        "episode": "The Last Jedi",
        "source": {
            "movie": "The Last Jedi",
            "scene_url": "https://starwars.com/lastjedi/kylo"
        }
    },
    {
        "id": 9,
        "quote": "Chewie, we’re home.",
        "character": "Han Solo",
        "category": "nostalgia",
        "episode": "The Force Awakens",
        "source": {
            "movie": "The Force Awakens",
            "scene_url": "https://starwars.com/awakens/han"
        }
    },
    {
        "id": 10,
        "quote": "Power! Unlimited power!",
        "character": "Darth Sidious",
        "category": "power",
        "episode": "Revenge of the Sith",
        "source": {
            "movie": "Revenge of the Sith",
            "scene_url": "https://starwars.com/sith/sidious"
        }
    }
]


@router.get("/quote", response_class=Response)
def get_quote(
    id: Optional[int] = Query(None),
    character: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    size: int = Query(5, ge=1),
    format: Optional[str] = Query("json")
):
    timestamp = datetime.utcnow().isoformat()

    # If ID is provided, return that specific quote
    if id is not None:
        quote = next((q for q in QUOTES if q["id"] == id), None)
        if not quote:
            raise HTTPException(status_code=404, detail="Quote not found")

        if format == "text":
            return PlainTextResponse(content=quote["quote"])
        elif format == "xml":
            xml = dicttoxml(
                {"version": "v3", "timestamp": timestamp, "quote": quote},
                custom_root="response",
                attr_type=False,
            )
            return Response(content=xml, media_type="application/xml")
        else:
            return {
                "version": "v3",
                "timestamp": timestamp,
                "quote": quote
            }

    # Filtering
    filtered = QUOTES
    if character:
        filtered = [q for q in filtered if q["character"].lower() == character.lower()]
    if category:
        filtered = [q for q in filtered if q["category"].lower() == category.lower()]

    total = len(filtered)
    start = (page - 1) * size
    end = start + size
    paginated = filtered[start:end]

    response_data = {
        "version": "v3",
        "timestamp": timestamp,
        "page": page,
        "size": size,
        "total": total,
        "quotes": paginated,
    }

    if format == "text":
        return PlainTextResponse(
            content="\n\n".join([q["quote"] for q in paginated])
        )
    elif format == "xml":
        xml = dicttoxml(response_data, custom_root="response", attr_type=False)
        return Response(content=xml, media_type="application/xml")
    else:
        return JSONResponse(content=response_data)
    
