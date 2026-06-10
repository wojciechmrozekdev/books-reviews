# from fastapi import APIRouter, HTTPException
# from app.schemas.reviews import Review




# router = APIRouter(prefix="/reviews")

# @router.put("/{id}")
# async def edit_review(id: int, edited_review: Review):

#     for book_reviews in reviews.values():
#         for review in book_reviews:
#             if review["id"] == id:
#                 review["rating"] = edited_review.rating
#                 review["content"] = edited_review.content

#                 return review

#     raise HTTPException(
#         status_code=404,
#         detail="Review not found"
#     )
    
# @router.delete("/{id}")
# async def delete_rewiev(id: int):
#     for book_reviews in reviews.values():
#         for i in range(len(book_reviews)):
#             if book_reviews[i]["id"] == id:
#                 book_reviews.pop(i)
#                 return reviews
#     raise HTTPException(
#         status_code=404,
#         detail="Review not found"
#     )