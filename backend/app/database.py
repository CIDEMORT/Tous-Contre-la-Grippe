from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import get_settings

settings = get_settings()

# Créer le moteur SQLite
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False}
)

# Optimisations SQLite
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_conn, connection_record):
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA synchronous=NORMAL")
    cursor.execute("PRAGMA cache_size=-64000")
    cursor.close()

# Session locale
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour les modèles
Base = declarative_base()

# Dependency pour FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ============================================
# IMPORTANT : Importer les modèles ici pour que SQLAlchemy les trouve
# ============================================
def import_models():
    """Import tous les modèles pour que SQLAlchemy puisse créer les tables"""
    from app.models import schemas  # noqa: F401
    # Le noqa: F401 dit à Python "oui, cet import est volontaire même s'il n'est pas utilisé"

# Importer dès que ce fichier est chargé
import_models()