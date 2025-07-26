import pytest
from unittest.mock import Mock
from praktikum.burger import Burger


def make_ingredient_mock(ingredient_type, name, price=100):
    mock_ingredient = Mock()
    mock_ingredient.get_type.return_value = ingredient_type
    mock_ingredient.get_name.return_value = name
    mock_ingredient.get_price.return_value = price
    return mock_ingredient


@pytest.fixture
def burger():
    return Burger()


@pytest.fixture
def bun():
    return make_ingredient_mock(None, "black bun")


@pytest.fixture
def sauce():
    return make_ingredient_mock("SAUCE", "hot sauce")



@pytest.fixture
def filling():
    return make_ingredient_mock("FILLING", "cutlet")


@pytest.fixture
def prepared_burger(bun, sauce, filling):
    burger = Burger()
    burger.set_buns(bun)
    burger.add_ingredient(sauce)
    burger.add_ingredient(filling)
    return burger