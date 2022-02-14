from sqlalchemy import (Boolean, Column, Integer,
                        String)

from models.base import Model


class User(Model):
    __tablename__ = 'users'
    id = Column(
        "userId",
        Integer,
        primary_key=True,
        autoincrement=True
    )
    username = Column(
        "username",
        String(50),
        unique=True,
        nullable=False
    )

    # We'll only store SHA256 hashes of passwords.
    # Since those hashes are 256 bits long (so 64 hex chars),
    # We'll store them in a VARCHAR(64)
    password = Column("password", String(64), nullable=False)

    # Same idea with the cost of the product. We'll store
    # the deposit in cents.
    deposit = Column("deposit", Integer(), default=0, nullable=False)

    role = Column("role", String(6), nullable=False)

    logged_in = Column("loggedIn", Boolean(False), nullable=False)

    def __init__(
        self,
        *,
        username,
        password,
        role,
        logged_in=False,
        deposit=0,
    ):
        self.username = username
        self.password = password
        self.deposit = deposit
        self.role = role
        self.logged_in = logged_in

    def to_json(self):
        return dict(
            username=self.username,
            deposit=self.deposit,
            role=self.role,
            logged_in=self.logged_in
        )

    def __repr__(self):
        return self.to_json()
