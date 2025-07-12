
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create SQLite engine
engine = create_engine("sqlite:///data/documents.db")  # file path where data is stored

# Base class
Base = declarative_base()

# Define Document model
class Document(Base):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True)
    source = Column(String)
    content = Column(Text)
    category = Column(String)
    is_vectorized = Column(Boolean, default=False)


# Create table
Base.metadata.create_all(engine)

# Create session (like a connection to DB)
SessionLocal = sessionmaker(bind=engine)



def insert_documents(docs, category):
    session = SessionLocal()

    try:
        for doc in docs:
            new_doc  = Document(
            source = doc.metadata.get("source",""),
            content = doc.page_content,
            category = category,
            is_vectorized = False
        )
        session.add(new_doc )
        session.commit()
        print(f"Inserted {len(docs)} documents into the database")
    except Exception as e:
        session.rollback()
        print(f"Error inserting documents: {e}")
    finally:
        session.close()




