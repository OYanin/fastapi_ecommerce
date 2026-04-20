from datetime import datetime
from sqlalchemy import Boolean, Integer, DateTime, CheckConstraint, func
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
    comment: Mapped[str | None]                                                
    comment_date: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, 
        server_default=func.now()
        )
    grade: Mapped[int] = mapped_column(
        Integer, 
        CheckConstraint(sqltext='((grade>=1) AND (grade<=5))', 
                        name='CONSTRAINT_chk_grade_in_range')
        )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    user: Mapped["User"] = relationship("User",
                                        back_populates="reviews")
    product: Mapped["Product"] = relationship("Product",
                                              back_populates="reviews")
