from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

class Database:
    """
    Singleton Database connection handler for PostgreSQL.
    """
    _instance = None

    def __new__(cls, db_uri: str):
        """
        Initialize or retrieve the existing Database instance.
        Args:
            db_uri (str): SQLAlchemy database URI string.
        Returns:
            Database: The singleton instance of the Database class.
        """
        if cls._instance is None:
            engine = create_engine(db_uri, echo=False)
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.engine = engine
            cls._instance.SessionLocal = sessionmaker(bind=engine)
        return cls._instance

    def get_session(self) -> sessionmaker:
        """
        Get a new SQLAlchemy session.

        Returns:
            Session: SQLAlchemy ORM session connected to the database.
        """
        return self.SessionLocal()

    def create_tables(self, drop_first: bool = False) -> None:
        """
        Create all tables based on ORM models.
        Args:
            drop_first (bool, optional):
                If True, drops all existing tables before recreating them. Defaults to False.
        """
        if drop_first:
            Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)
