from contextlib import contextmanager
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_path = Path(__file__).parent.parent / "sqlite" / "sqlite.db"


class Database:
    def __init__(self):
        self._db_url = f"sqlite:///{db_path}"
        self._engine = create_engine(
            self._db_url, connect_args={"check_same_thread": False}
        )
        self._Session = sessionmaker(bind=self._engine)

    def init_db(self):
        Base.metadata.create_all(bind=self._engine)

    @contextmanager
    def session(self):
        connection = self._engine.connect()
        session = self._Session()

        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
            connection.close()


database = Database()
Base = declarative_base()


def get_db():
    with database.session() as session:
        yield session
