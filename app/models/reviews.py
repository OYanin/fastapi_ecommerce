from datetime import datetime
from sqlalchemy import String, Boolean, Float, Integer, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from app.database import Base


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(Integer, 
                                    primary_key=True, 
                                    autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer,
                                         ForeignKey("users.id"))
    product_id: Mapped[int] = mapped_column(Integer,
                                            ForeignKey("products.id"))
    comment: Mapped[str | None] = mapped_column(None,
                                                nullable=True)
    comment_date: Mapped[datetime] = mapped_column(DateTime, 
                                                   default=datetime.now)
    grade: Mapped[int] = mapped_column(Integer)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    user: Mapped["User"] = relationship("User", back_populates="review")
    product: Mapped["Product"] = relationship("Product", back_populates="review")
