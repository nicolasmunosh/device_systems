# =============================================
# dependencies/database_dependency.py
# =============================================

from app.database.connection import SessionLocal


def get_db():
    """Entrega una sesión de base de datos y la cierra al terminar"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
