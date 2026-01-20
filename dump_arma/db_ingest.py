import hashlib
from uuid import uuid4
from datetime import datetime

import orjson
from tqdm import tqdm
from sqlalchemy import select

from .db_util import make_engine, make_session_factory
from .db_schema import Base, Snapshot, Group, Unit, Vehicle


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def time_list_to_iso(t):
    y, mo, d, hh, mm, ss, ms = t
    return datetime(y, mo, d, hh, mm, ss, ms * 1000).isoformat(timespec="milliseconds")


def safe_pos3(pos):
    try:
        return float(pos[0]), float(pos[1]), float(pos[2])
    except Exception:
        return None, None, None


def dumps(raw_json_file):
    return orjson.dumps(raw_json_file).decode()


def dump_arma_into_sql(db_url: str = None, json_dir: str = None):
    engine = make_engine(db_url)
    Base.metadata.create_all(engine) # <=> CREATE TABLE IF NOT EXISTS ... (from db_schema.py!)
    Session = make_session_factory(engine)

    files = sorted(json_dir.glob("*.json"))
    if not files:
        print("💽 No JSON files")
        return

    ok, skip, fail = 0, 0, 0

    for f in tqdm(files):
        with Session() as session:
            try:
                raw = f.read_bytes()
                sha = sha256_bytes(raw)

                if session.execute(
                    select(Snapshot.snapshot_id).where(Snapshot.sha256 == sha)
                ).first():
                    skip += 1
                    continue

                raw_json_file = orjson.loads(raw)
                sid = str(uuid4())  # snapshot id

                start_iso = None
                if isinstance(raw_json_file.get("friend_info"), dict):
                    fi0 = raw_json_file["friend_info"]
                    start_iso = time_list_to_iso(fi0["start_time"]) if "start_time" in fi0 else None
                elif isinstance(raw_json_file.get("enemy_info"), dict):
                    ei0 = raw_json_file["enemy_info"]
                    start_iso = time_list_to_iso(ei0["start_time"]) if "start_time" in ei0 else None

                session.add(
                    Snapshot(
                        snapshot_id=sid,
                        source_file=f.name,
                        sha256=sha,
                        datetime=start_iso,
                        raw_json=dumps(raw_json_file),
                    )
                )

                for side, key in (("b", "friend_info"), ("r", "enemy_info")):
                    info = raw_json_file.get(key)
                    if not isinstance(info, dict):
                        continue

                    for g in info.get("groups", []):
                        x, y, z = safe_pos3(g.get("pos", []))
                        gc = g.get("groupcode")
                        if not gc:
                            continue
                        session.add(
                            Group(
                                snapshot_id=sid,
                                side=side,
                                groupcode=gc,
                                display_name=g.get("display_name"),
                                pos_x=x, pos_y=y, pos_z=z,
                                unitlist_json=dumps(g.get("unitlist", [])),
                                waypointpos_json=dumps(g.get("waypointpos", [])),
                            )
                        )

                    for u in info.get("units", []):
                        uname = u.get("unitname")
                        if not uname:
                            continue
                        x, y, z = safe_pos3(u.get("pos", []))
                        session.add(
                            Unit(
                                snapshot_id=sid,
                                side=side,
                                unitname=uname,
                                unittype=u.get("unittype"),
                                pos_x=x, pos_y=y, pos_z=z,
                                # behaviour=u.get("behaviour"),
                                damage=u.get("damage", 0.0),
                                objectparent=u.get("objectparent"),
                                ammo_json=dumps(u.get("ammo", [])),
                                discovered=u.get("discovered", 0),
                            )
                        )

                    for v in info.get("vehicles", []):
                        vname = v.get("vehiclename")
                        if not vname:
                            continue
                        x, y, z = safe_pos3(v.get("pos", []))
                        session.add(
                            Vehicle(
                                snapshot_id=sid,
                                side=side,
                                vehiclename=vname,
                                vehicletype=v.get("vehicletype"),
                                group_display_name=v.get("group"),
                                pos_x=x, pos_y=y, pos_z=z,
                                damage=v.get("damage", 0.0),
                                ammo_json=dumps(v.get("ammo", [])),
                                hitpoint_json=dumps(v.get("hitpoint", [])),
                                discovered=v.get("discovered", 0),
                            )
                        )

                session.commit()
                ok += 1

            except Exception as e:
                session.rollback()
                print(f"💽 [FAIL] {f.name}: {e}")
                fail += 1

    print(f"💽 Migrating Arma 3 metadata into SQLite3 database: Done ⭕ - ok={ok}, skipped={skip}, failed={fail}")
