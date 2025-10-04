from sqlalchemy import Column, Integer, String
from app.database import Base

class ProbeDB(Base):
    """
    Este é o modelo ORM que representa a tabela 'probes' no banco de dados.
    """
    __tablename__ = "probes"

    id = Column(String, primary_key=True, index=True)
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)
    direction = Column(String, nullable=False)
    max_x = Column(Integer, nullable=False)
    max_y = Column(Integer, nullable=False)
