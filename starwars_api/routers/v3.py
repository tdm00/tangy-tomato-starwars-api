from fastapi import APIRouter, Query, Request
from fastapi.responses import JSONResponse, PlainTextResponse, Response
from typing import Optional
from datetime import datetime
import xml.etree.ElementTree as ET

router = APIRouter()

quotes = [
    {
        "id": 1,
        "quote": "Do. Or do not. There is no try.",
        "character": "Yoda",
        "category": "wisdom",
        "episode": "The Empire Strikes Back",
        "source": {"movie": "The Empire Strikes Back", "scene_url": "https://starwars.com/empire/yoda"}
    },
    {
        "id": 2,
        "quote": "I’ve got a bad feeling about this.",
        "character": "Various",
        "category": "humor",
        "episode": "Multiple",
        "source": {"movie": "Various", "scene_url": "https://starwars.com/recurring/badfeeling"}
    },
    {
        "id": 3,
        "quote": "The Force will be with you. Always.",
        "character": "Obi-Wan Kenobi",
        "category": "wisdom",
        "episode": "A New Hope",
        "source": {"movie": "A New Hope", "scene_url": "https://starwars.com/anewhope/obiwan"}
    },
    {
        "id": 4,
        "quote": "It's a trap!",
        "character": "Admiral Ackbar",
        "category": "humor",
        "episode": "Return of the Jedi",
        "source": {"movie": "Return of the Jedi", "scene_url": "https://starwars.com/jedi/ackbar"}
    },
    {
        "id": 5,
        "quote": "I am your father.",
        "character": "Darth Vader",
        "category": "drama",
        "episode": "The Empire Strikes Back",
        "source": {"movie": "The Empire Strikes Back", "scene_url": "https://starwars.com/empire/vader"}
    },
    {
        "id": 6,
        "quote": "Never tell me the odds!",
        "character": "Han Solo",
        "category": "humor",
        "episode": "The Empire Strikes Back",
        "source": {"movie": "The Empire Strikes Back", "scene_url": "https://starwars.com/empire/han"}
    },
    {
        "id": 7,
        "quote": "Now, young Skywalker, you will die.",
        "character": "Emperor Palpatine",
        "category": "drama",
        "episode": "Return of the Jedi",
        "source": {"movie": "Return of the Jedi", "scene_url": "https://starwars.com/jedi/palpatine"}
    },
    {
        "id": 8,
        "quote": "Chewie, we’re home.",
        "character": "Han Solo",
        "category": "nostalgia",
        "episode": "The Force Awakens",
        "source": {"movie": "The Force Awakens", "scene_url": "https://starwars.com/awakens/home"}
    },
    {
        "id": 9,
        "quote": "I will not fight you, father.",
        "character": "Luke Skywalker",
        "category": "drama",
        "episode": "Return of the Jedi",
        "source": {"movie": "Return of the Jedi", "scene_url": "https://starwars.com/jedi/luke"}
    },
    {
        "id": 10,
        "quote": "Fear is the path to the dark side.",
        "character": "Yoda",
        "category": "wisdom",
        "episode": "The Phantom Menace",
        "source": {"movie": "The Phantom Menace", "scene_url": "https://starwars.com/menace/focus"}
    },
]

def to_xml(data: dict) -> str:
    root = ET.Element("response")
    for key, value in data.items():
        if isinstance(value, list):
            list_elem = ET.SubElement(root, key)
            for item in value:
                item_elem = ET.SubElement(list_elem, "quote")
                for k, v in item.items():
                    if isinstance(v, dict):
                        dict_elem = ET.SubElement(item_elem, k)
                        for dk, dv in v.items():
                            sub_elem = ET.SubElement(dict_elem, dk)
                            sub_elem.text = str(dv)
                    else:
                        sub_elem = ET.SubElement(item_elem, k)
                        sub_elem.text = str(v)
        else:
            sub_elem = ET.SubElement(root, key)
            sub_elem.text = str(value)
    return ET.tostring(root, encoding="unicode")

@router.get("/quote")
def get_quote(
    character: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    page: int = 1,
    size: int = 5,
    format: Optional[str] = Query("json"),
    request: Request = None
):
    filtered = quotes

    if character:
        filtered = [q for q in filtered if q["character"].lower() == character.lower()]
    if category:
        filtered = [q for q in filtered if q["category"].lower() == category.lower()]

    total = len(filtered)
    start = (page - 1) * size
    end = start + size
    paginated = filtered[start:end]

    result = {
        "version": "v3",
        "timestamp": datetime.utcnow().isoformat(),
        "page": page,
        "size": size,
        "total": total,
        "quotes": paginated,
    }

    headers = {
        "X-RateLimit-Limit": "100",
        "X-RateLimit-Remaining": "99",
        "X-RateLimit-Reset": "60"
    }

    if format == "text":
        quotes_text = "\n".join([q["quote"] for q in paginated])
        return PlainTextResponse(content=quotes_text, headers=headers)
    elif format == "xml":
        return Response(content=to_xml(result), media_type="application/xml", headers=headers)
    else:
        return JSONResponse(content=result, headers=headers)