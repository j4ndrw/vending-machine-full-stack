from api.vendingmachine import VendingMachine

vending_machine_api = VendingMachine()


class TestDeposit:
    def test_credits_in_allowed_top_up(self):
        def validate(credits: int):
            return vending_machine_api.operation.validate_credits(
                credits,
                kind="deposit"
            )
        assert validate(1) is not None and validate(1).status_code == 400
        assert validate(2) is not None and validate(2).status_code == 400
        assert validate(4) is not None and validate(4).status_code == 400
        assert validate(15) is not None and validate(15).status_code == 400
        assert validate(5) is None
        assert validate(10) is None

    def test_depositer_is_buyer(self):
        def validate(role: str):
            return vending_machine_api.operation.validate_depositer_role(
                role
            )

        assert validate("buyer") is None
        assert validate("seller") is not None and validate(
            "seller").status_code == 403


class TestBuy:
    def test_total_sign_check(self):
        def validate(credits: int):
            return vending_machine_api.operation.validate_total(
                credits
            )
        assert validate(-1) is not None and validate(-1).status_code == 400
        assert validate(0) is not None and validate(0).status_code == 400
        assert validate(1) is None

    def test_user_is_buyer(self):
        def validate(role: str):
            return vending_machine_api.operation.validate_buyer_role(
                role
            )
        assert validate("buyer") is None
        assert validate("seller") is not None and validate(
            "seller").status_code == 403


class TestRegister:
    def test_validate_role(self):
        def validate(role: str):
            return vending_machine_api.operation.validate_role(role)

        assert validate("buyer") is None
        assert validate("seller") is None
        assert validate("something else") is not None and validate(
            "something else").status_code == 403
