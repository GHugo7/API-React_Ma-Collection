from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, UniqueConstraint, ForeignKey
from datetime import datetime, timezone
from app.models.base import Base
from app.models.item import Item

class Entry(Base):
    __tablename__ = "collection_entries"
    __table_args__ = (UniqueConstraint("user_id", "item_id", name="uq_user_item"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"))

    statut: Mapped[str] = mapped_column(String(20))
    note: Mapped[int | None] = mapped_column(default=None)
    commentaire: Mapped[str | None] = mapped_column(Text, default=None)
    date_ajout: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )

    item: Mapped[Item] = relationship(lazy="selectin")