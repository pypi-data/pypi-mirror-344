"""Web Channel Model"""

from typing import Optional, TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from bingefriend.shows.core.models.base import Base

if TYPE_CHECKING:
    from bingefriend.shows.core.models.season import Season
    from bingefriend.shows.core.models.show import Show


class WebChannel(Base):
    """Represents a web channel"""

    __tablename__ = "web_channel"

    # Attributes
    id: Mapped[int] = mapped_column(primary_key=True)
    maze_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    name: Mapped[Optional[str]] = mapped_column(String(255))
    country_name: Mapped[Optional[str]] = mapped_column(String(255))
    country_code: Mapped[Optional[str]] = mapped_column(String(255))
    country_timezone: Mapped[Optional[str]] = mapped_column(String(255))
    official_site: Mapped[Optional[str]] = mapped_column(String(255))

    # Relationships - referencing this model
    shows: Mapped[list["Show"]] = mapped_column(back_populates="web_channel")
    seasons: Mapped[list["Season"]] = mapped_column(back_populates="web_channel")
