from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.sql import func

from app.models.products import Product as ProductModel
from app.models.users import User as UserModel
from app.models.reviews import Review as ReviewModel
from app.schemas import ReviewCreate, Review as ReviewSchema
from app.db_depends import get_async_db
from app.auth import get_current_user, get_current_seller, get_current_buyer

router = APIRouter(prefix="/reviews", tags=["reviews"])


async def update_product_rating(product_id: int,
                                db: AsyncSession = Depends(get_async_db)):
    """
    Обновляет рейтинг товара на основе оценок из отзывов
    """
    result = await db.execute(
        select(func.avg(ReviewModel.grade)).where(
            ReviewModel.product_id == product_id,
            ReviewModel.is_active == True
        )
    )
    avg_rating = result.scalar() or 0.0
    product = await db.get(ProductModel, product_id)
    product.rating = avg_rating
    await db.commit()


@router.get("/", response_model=list[ReviewSchema])
async def get_all_reviews(db: AsyncSession = Depends(get_async_db)):
    """
    Возвращает список всех активных отзывов о товарах.
    """
    result = await db.scalars(select(ReviewModel).where(ReviewModel.is_active == True))
    return result.all()


@router.post("/", response_model=ReviewSchema, status_code=status.HTTP_201_CREATED)
async def create_review(review: ReviewCreate,
                        db: AsyncSession = Depends(get_async_db),
                        current_user: UserModel = Depends(get_current_user)):
    """
    Добавляет новый отзыв покупателя о товаре
    """
    await get_current_buyer(current_user)
    result = await db.scalars(
         select(ProductModel).where(
              ProductModel.is_active, ProductModel.id == review.product_id
              )
         )
    product = result.first()
    if product:
        if 1 <= review.grade <= 5:
                new_review = ReviewModel(**review.model_dump())
                db.add(new_review)
                await db.commit()
                await update_product_rating(review.product_id, db)
                return new_review

        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
                            detail='Error: The "grade" is out of the range from 1 to 5')

    raise HTTPException(status_code=status.HTTP_404_FORBIDDEN, 
                        detail='Error: The product does not exist or is not active')


@router.delete("/{review_id}")
async def delete_review(review_id: int,
                        db: AsyncSession = Depends(get_async_db),
                        current_user: UserModel = Depends(get_current_user)):
    """
    Выполняет мягкое удаление отзыва, если он принадлежит текущему покупателю.
    """    
    result = await db.scalars(select(ReviewModel).where(ReviewModel.id == review_id, ReviewModel.is_active))
    review = result.first()

    if review:
         if current_user.role == 'admin' or current_user.id == review.user_id:
                await db.execute(update(ReviewModel)
                                 .where(ReviewModel.id == review_id)
                                 .values(is_active=False))
                await db.commit()
                #await db.refresh(review)
                await update_product_rating(review.product_id, db)
                return {"message": "Review deleted"}
    
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Error: You can't delete a review")

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Error: The review does not exist or is not active")