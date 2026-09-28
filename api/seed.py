from pathlib import Path
import json
from sqlalchemy import select
import asyncio

from app.db.database import SessionLocal
from app.models.item import Item

async def main() -> None:
    path = Path(__file__).parent / "data" / "items.json"
    items_json = json.loads(path.read_text(encoding="utf-8"))

    async with SessionLocal() as session:

        existants = set((await session.scalars(select(Item.titre))).all())

        nouveaux = [Item(**item) for item in items_json if item["titre"] not in existants]

        if nouveaux:
            session.add_all(nouveaux)
            await session.commit()

    print(f"{len(nouveaux)} items insérés, {len(existants)} déjà présents")

if __name__ == "__main__":
    asyncio.run(main())