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
    snapshot_id: Mapped[str] = mapped_column(String, primary_key=True)              # foreign key to Snapshot.snapshot_id  
    side: Mapped[str] = mapped_column(String, primary_key=True)                     # side identifier ("friend" | "enemy")

    company: Mapped[str] = mapped_column(String, primary_key=True)                  # Company (중대) identifier (1, 2, 3, ...)
    platoon: Mapped[str] = mapped_column(String, primary_key=True)                  # Platoon (소대) identifier (i[n]: IFV, t[n]: Tank, hq[n]: headquarter, ...)
    squad: Mapped[str] = mapped_column(String, primary_key=True)                    # Squad (분대) identifier
    groupcode: Mapped[str] = mapped_column(String, primary_key=True)                # [Side]_[Company]_[Platoon]_[Squad]
    # display_name: Mapped[str | None] = mapped_column(String)                      # ???

    pos_x: Mapped[float | None] = mapped_column(Float)                              # Leader X position of the squad 
    pos_y: Mapped[float | None] = mapped_column(Float)                              # Leader Y position of the squad  
    pos_z: Mapped[float | None] = mapped_column(Float)                              # Leader Z position of the squad
    unitlist_json: Mapped[str | None] = mapped_column(Text)                         # Members belonging to each squad (json list)
    waypointpos_json: Mapped[str | None] = mapped_column(Text)                      # ??? Waypoint positions (json list)


class Unit(Base):
    __tablename__ = "units"
    snapshot_id: Mapped[str] = mapped_column(String, primary_key=True)              # foreign key to Snapshot.snapshot_id
    side: Mapped[str] = mapped_column(String, primary_key=True)                     # side identifier ("friend" | "enemy")
    unitname: Mapped[str] = mapped_column(String, primary_key=True)
    groupcode: Mapped[str] = mapped_column(String)                                  # foreign key to Group.groupcode
    unittype: Mapped[str | None] = mapped_column(String)
    pos_x: Mapped[float | None] = mapped_column(Float)                              # X position of the unit
    pos_y: Mapped[float | None] = mapped_column(Float)                              # Y position of the unit
    pos_z: Mapped[float | None] = mapped_column(Float)                              # Z position of the unit    
    damage: Mapped[float | None] = mapped_column(Float)                             # damage value between 0.0 and 1.0
    objectparent: Mapped[str | None] = mapped_column(String)                        # vehiclename if the unit is in a vehicle
    ammo_json: Mapped[str | None] = mapped_column(Text)                             # ammo (탄약) types and counts carried by the unit
    discovered: Mapped[int | None] = mapped_column(Integer)                         # only available for enemy units
    # behaviour: Mapped[str | None] = mapped_column(String)



class Vehicle(Base):
    __tablename__ = "vehicles"
    snapshot_id: Mapped[str] = mapped_column(String, primary_key=True)              # foreign key to Snapshot.snapshot_id
    side: Mapped[str] = mapped_column(String, primary_key=True)                     # side identifier ("friend" | "enemy")
    vehiclename: Mapped[str] = mapped_column(String, primary_key=True)
    groupcode: Mapped[str] = mapped_column(String)                                  # foreign key to Group.groupcode
    vehicletype: Mapped[str | None] = mapped_column(String)
    pos_x: Mapped[float | None] = mapped_column(Float)                              # X position of the vehicle
    pos_y: Mapped[float | None] = mapped_column(Float)                              # Y position of the vehicle
    pos_z: Mapped[float | None] = mapped_column(Float)                              # Z position of the vehicle
    damage: Mapped[float | None] = mapped_column(Float)                             # damage value between 0.0 and 1.0
    ammo_json: Mapped[str | None] = mapped_column(Text)                             # ammo (탄약) types and counts carried by the vehicle
    hitpoint_json: Mapped[str | None] = mapped_column(Text)                         # available hitpoints and their damage values
    discovered: Mapped[int | None] = mapped_column(Integer)                         # only available for enemy vehicles
    # group_display_name: Mapped[str | None] = mapped_column(String)                # display_name ???