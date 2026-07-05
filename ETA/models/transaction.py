from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    description = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    type = Column(String, nullable=False)

    category_id = Column(Integer, ForeignKey("categories.id"))

    category = relationship(
        "Category",
        back_populates="transactions"
    )   
    
    
    