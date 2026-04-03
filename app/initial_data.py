import logging

from sqlmodel import Session

from app.core.database import engine, init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    with Session(engine) as session:
        init_db(session)


def main() -> None:    
    init()
    

if __name__ == "__main__":
    main()
