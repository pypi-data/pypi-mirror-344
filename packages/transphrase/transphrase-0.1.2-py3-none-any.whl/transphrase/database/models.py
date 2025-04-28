import datetime
from pathlib import Path

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    create_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()


class TranslationModel(Base):
    """Model information and preferences"""

    __tablename__ = "models"

    id = Column(Integer, primary_key=True)
    model_id = Column(String(128), unique=True)
    description = Column(Text)
    tokens = Column(Integer)
    pricing_input = Column(Float)
    pricing_output = Column(Float)
    capabilities = Column(String(255))
    is_favorite = Column(Boolean, default=False)
    last_used = Column(DateTime)


class TranslationJob(Base):
    """Translation job information"""

    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True)
    job_id = Column(String(36), unique=True)
    source_dir = Column(String(255))
    output_dir = Column(String(255))
    model_id = Column(String(128), ForeignKey("models.model_id"))
    system_prompt = Column(Text)
    source_language = Column(String(50), default="Chinese")  # Add this
    target_language = Column(String(50), default="English")  # Add this
    start_time = Column(DateTime, default=datetime.datetime.utcnow)
    end_time = Column(DateTime)
    status = Column(String(20), default="pending")  # pending, in_progress, completed, failed
    total_files = Column(Integer)
    completed_files = Column(Integer, default=0)

    # Relationship
    model = relationship("TranslationModel")
    translations = relationship("TranslationFile", back_populates="job")


class TranslationFile(Base):
    """Individual file translation information"""

    __tablename__ = "translation_files"

    id = Column(Integer, primary_key=True)
    job_id = Column(String(36), ForeignKey("jobs.job_id"))
    source_path = Column(String(255))
    output_path = Column(String(255))
    status = Column(String(20), default="pending")  # pending, in_progress, completed, failed
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    tokens_input = Column(Integer)
    tokens_output = Column(Integer)
    error = Column(Text)

    # Relationship
    job = relationship("TranslationJob", back_populates="translations")


class DBManager:
    """Database manager for TransPhrase tool"""

    def __init__(self, db_path: str = "~/.transphrase/transphrase.db"):
        """Initialize database manager"""
        db_file = Path(db_path).expanduser()
        db_file.parent.mkdir(parents=True, exist_ok=True)

        self.engine = create_engine(f"sqlite:///{db_file}")
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def create_session(self):
        """Create and return a new database session"""
        return self.Session()
