class LatsBasketItemError(Exception):
    """Can not delete last item in basket"""

class EmptyOrderError(Exception):
    """Can make order with no books in basket"""