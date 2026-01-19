from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Float, Integer, Text


class Base(DeclarativeBase):
    pass


class Snapshot(Base):
    __tablename__ = "snapshots"
    snapshot_id: Mapped[str] = mapped_column(String, primary_key=True)              # Surrogate key
    source_file: Mapped[str] = mapped_column(String, nullable=False)                # original json file name
    sha256: Mapped[str] = mapped_column(String, nullable=False, unique=True)        # content hash (to avoid duplicates)
    datetime: Mapped[str | None] = mapped_column(String)                            # ISO8601: [YYYY-MM-DD]T[HH:MM:SS.mmm]
    raw_json: Mapped[str] = mapped_column(Text, nullable=False)                     # original raw json content


class Group(Base):
    __tablename__ = "groups"
    snapshot_id: Mapped[str] = mapped_column(String, primary_key=True)
    side: Mapped[str] = mapped_column(String, primary_key=True)                     # "friend" | "enemy"
    groupcode: Mapped[str] = mapped_column(String, primary_key=True) 
    display_name: Mapped[str | None] = mapped_column(String)
    pos_x: Mapped[float | None] = mapped_column(Float)
    pos_y: Mapped[float | None] = mapped_column(Float)
    pos_z: Mapped[float | None] = mapped_column(Float)
    unitlist_json: Mapped[str | None] = mapped_column(Text)
    waypointpos_json: Mapped[str | None] = mapped_column(Text)


class Unit(Base):
    __tablename__ = "units"
    snapshot_id: Mapped[str] = mapped_column(String, primary_key=True)
    side: Mapped[str] = mapped_column(String, primary_key=True)
    unitname: Mapped[str] = mapped_column(String, primary_key=True)
    unittype: Mapped[str | None] = mapped_column(String)
    pos_x: Mapped[float | None] = mapped_column(Float)
    pos_y: Mapped[float | None] = mapped_column(Float)
    pos_z: Mapped[float | None] = mapped_column(Float)
    behaviour: Mapped[str | None] = mapped_column(String)
    damage: Mapped[float | None] = mapped_column(Float)
    objectparent: Mapped[str | None] = mapped_column(String)
    ammo_json: Mapped[str | None] = mapped_column(Text)
    discovered: Mapped[int | None] = mapped_column(Integer)


class Vehicle(Base):
    __tablename__ = "vehicles"
    snapshot_id: Mapped[str] = mapped_column(String, primary_key=True)
    side: Mapped[str] = mapped_column(String, primary_key=True)
    vehiclename: Mapped[str] = mapped_column(String, primary_key=True)
    vehicletype: Mapped[str | None] = mapped_column(String)
    group_display_name: Mapped[str | None] = mapped_column(String)
    pos_x: Mapped[float | None] = mapped_column(Float)
    pos_y: Mapped[float | None] = mapped_column(Float)
    pos_z: Mapped[float | None] = mapped_column(Float)
    damage: Mapped[float | None] = mapped_column(Float)
    ammo_json: Mapped[str | None] = mapped_column(Text)
    hitpoint_json: Mapped[str | None] = mapped_column(Text)
    discovered: Mapped[int | None] = mapped_column(Integer)
