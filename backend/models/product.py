from sqlalchemy import Column, ForeignKey, Integer, String, null

from models.base import Model


class Product(Model):
    __tablename__ = 'products'
    id = Column(
        'productId',
        Integer,
        primary_key=True,
        autoincrement=True
    )
    seller_id = Column(
        "sellerId",

        # Since the seller is a user, we'll use the user's ID.
        # We'll validate on the role in the implementation
        ForeignKey("users.userId"),
        nullable=False
    )

    buyer_id = Column(
        "buyerId",
        ForeignKey("users.userId"),
        nullable=True
    )

    amount_available = Column(
        'amountAvailable',
        Integer(),
        default=0,
        nullable=False
    )

    # We'll make any financial data integers,
    # since working with integers is more precise
    # than working with floats.
    #
    # This being said, if the cost is 100, it will be
    # equivalent or 1.00 USD (or whatever the currency is).
    cost = Column("cost", Integer(), nullable=False)
    product_name = Column("productName", String(200), nullable=False)

    def __init__(
        self,
        *,
        amount_available,
        cost,
        product_name,
        seller_id,
        buyer_id
    ):
        self.amount_available = amount_available
        self.cost = cost
        self.product_name = product_name
        self.seller_id = seller_id
        self.buyer_id = buyer_id

    def to_json(self):
        return dict(
            amount_available=self.amount_available,
            cost=self.cost,
            product_name=self.product_name,
            seller_id=self.seller_id,
            buyer_id=self.buyer_id
        )
