import os
import pandas as pd
import logging
from sqlalchemy import create_engine, Column, Integer, Float, String, Date
from sqlalchemy.orm import declarative_base, sessionmaker

logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./portwise.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class PortModel(Base):
    __tablename__ = "ports"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    max_draft_m = Column(Float, nullable=False)
    max_loa_m = Column(Float, nullable=False)
    max_beam_m = Column(Float, nullable=False)
    handling_rate_tpd = Column(Float, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)


class VesselModel(Base):
    __tablename__ = "vessels"

    id = Column(Integer, primary_key=True, index=True)
    vessel_name = Column(String, nullable=False)
    vessel_class = Column(String, index=True, nullable=False)
    dwt = Column(Float, nullable=False)
    loa_m = Column(Float, nullable=False)
    beam_m = Column(Float, nullable=False)
    draft_m = Column(Float, nullable=False)
    built_year = Column(Integer, nullable=True)


class FreightRecordModel(Base):
    __tablename__ = "freight_records"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, index=True, nullable=False)
    origin = Column(String, index=True, nullable=False)
    destination = Column(String, index=True, nullable=False)
    vessel_class = Column(String, index=True, nullable=False)
    freight_rate = Column(Float, nullable=False)
    bdi = Column(Float, nullable=True)
    bunker = Column(Float, nullable=True)
    coal_price = Column(Float, nullable=True)
    usd_inr = Column(Float, nullable=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create database tables and seed initial data from CSV files if empty."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Seed Ports
        if db.query(PortModel).count() == 0:
            ports_csv = "backend/data/updatedpub150.csv"
            if os.path.exists(ports_csv):
                df = pd.read_csv(ports_csv)
                for _, row in df.iterrows():
                    port = PortModel(
                        name=str(row["port_name"]).strip(),
                        max_draft_m=float(row["max_draft_m"]),
                        max_loa_m=float(row["max_loa_m"]),
                        max_beam_m=float(row["max_beam_m"]),
                        handling_rate_tpd=float(row["handling_rate_tpd"]),
                        latitude=float(row.get("latitude", 0.0)),
                        longitude=float(row.get("longitude", 0.0))
                    )
                    db.add(port)
                db.commit()
                logger.info("Seeded ports table from CSV.")

        # Seed Vessels
        if db.query(VesselModel).count() == 0:
            vessels_csv = "backend/data/Cleaned_ships_data.csv"
            if os.path.exists(vessels_csv):
                df = pd.read_csv(vessels_csv)
                for _, row in df.iterrows():
                    vessel = VesselModel(
                        id=int(row["vessel_id"]),
                        vessel_name=str(row["vessel_name"]),
                        vessel_class=str(row["vessel_class"]),
                        dwt=float(row["dwt"]),
                        loa_m=float(row["loa_m"]),
                        beam_m=float(row["beam_m"]),
                        draft_m=float(row["draft_m"]),
                        built_year=int(row.get("built_year", 2020))
                    )
                    db.add(vessel)
                db.commit()
                logger.info("Seeded vessels table from CSV.")

        # Seed Freight Records
        if db.query(FreightRecordModel).count() == 0:
            freight_csv = "backend/data/freight_dataset.csv"
            if os.path.exists(freight_csv):
                df = pd.read_csv(freight_csv)
                for _, row in df.iterrows():
                    record = FreightRecordModel(
                        date=str(row["date"]),
                        origin=str(row["origin"]),
                        destination=str(row["destination"]),
                        vessel_class=str(row["vessel_class"]),
                        freight_rate=float(row["freight_rate"]),
                        bdi=float(row.get("bdi", 1800)),
                        bunker=float(row.get("bunker", 620)),
                        coal_price=float(row.get("coal_price", 135)),
                        usd_inr=float(row.get("usd_inr", 83.2))
                    )
                    db.add(record)
                db.commit()
                logger.info("Seeded freight_records table from CSV.")

    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()
