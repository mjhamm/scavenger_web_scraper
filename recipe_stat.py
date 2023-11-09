from decimal import Decimal
from comment import Comment

class RecipeStat:
    id: int = -1
    likes: int = 0
    views: int = 0
    rating: Decimal
    comments: [Comment]
