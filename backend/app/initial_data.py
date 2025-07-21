import logging
from app.db.session import engine
from app.db.base import Base  # noqa

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db() -> None:
    logger.info("Creating initial data")
    # This will create all tables defined in models that inherit from Base
    Base.metadata.create_all(bind=engine)
    logger.info("Initial data created")

if __name__ == "__main__":
    init_db()