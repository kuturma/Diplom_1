import pytest
from unittest.mock import Mock
from praktikum.burger import Burger


class TestBurger:
    def test_set_buns(self, burger, bun): # тест добавления булочки
        burger.set_buns(bun)
        assert burger.bun == bun


    def test_add_ingredient(self, burger, sauce): # тест добавления ингредиента в бургер
        burger.add_ingredient(sauce)
        assert sauce in burger.ingredients
        assert len(burger.ingredients) == 1


    def test_remove_ingredient(self, prepared_burger): # тест удаления ингредиента
        ingredient_to_remove = prepared_burger.ingredients[0]
        initial_count = len(prepared_burger.ingredients)
        prepared_burger.remove_ingredient(0)
        assert len(prepared_burger.ingredients) == initial_count - 1
        assert ingredient_to_remove not in prepared_burger.ingredients


    def test_remove_invalid_index(self, burger, sauce): # тест невалидных индексов при удалении ингредиента
        with pytest.raises(IndexError):
            burger.remove_ingredient(0)

        burger.add_ingredient(sauce)
        with pytest.raises(IndexError):
            burger.remove_ingredient(1)


    def test_move_ingredient(self, prepared_burger, sauce, filling): # тест перемещения ингредиента в бургере
        prepared_burger.move_ingredient(0, 1)
        assert prepared_burger.ingredients[0] == filling
        assert prepared_burger.ingredients[1] == sauce


    @pytest.mark.parametrize("bun_price, ingredients_prices, expected", [
        (100, [], 200),
        (200, [50], 450),
        (150, [100, 200], 600),
        (0, [0, 0], 0),
        (300, [150, 250, 100], 1100)
    ])
    def test_get_price(self, burger, bun, bun_price, ingredients_prices, expected): # тест расчета цены с использованием параметризации
        bun.get_price.return_value = bun_price
        burger.set_buns(bun)

        for price in ingredients_prices:
            ingredient = Mock()
            ingredient.get_price.return_value = price
            burger.add_ingredient(ingredient)

        assert burger.get_price() == expected


    def test_get_receipt(self, prepared_burger, bun, sauce, filling): # тест получения чека
        total_price = bun.get_price() * 2 + sauce.get_price() + filling.get_price()
        expected = (
            f"(==== {bun.get_name()} ====)\n"
            f"= {sauce.get_type().lower()} {sauce.get_name()} =\n"
            f"= {filling.get_type().lower()} {filling.get_name()} =\n"
            f"(==== {bun.get_name()} ====)\n"
            "\n"
            f"Price: {total_price}"
        )
        assert prepared_burger.get_receipt() == expected