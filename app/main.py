from abc import ABC, abstractmethod


class Validator(ABC):
    def __set_name__(self, owner: str, name: str) -> None:
        self.protected_name = f"_{name}"

    def __get__(self, instance: object, owner: str) -> object:
        return instance.__dict__[self.protected_name]

    def __set__(self, instance: object, value: int) -> None:
        self.validate(value)
        instance.__dict__[self.protected_name] = value

    @abstractmethod
    def validate(self, value : int) -> None:
        pass


class Number(Validator):
    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        if not (self.min_value <= value <= self.max_value):
            raise ValueError(f"Quantity should be between "
                             f"{self.min_value} and {self.max_value}.")


class OneOf(Validator):
    def __init__(self, options: tuple) -> None:
        self.options = options

    def validate(self, value: str) -> None:
        if value not in self.options:
            raise ValueError(f"Expected {value} to be one of {self.options}.")


class BurgerRecipe:
    buns: int = Number(2, 3)
    cheese: int = Number(0, 2)
    tomatoes: int = Number(0, 3)
    cutlets: int = Number(1, 3)
    eggs: int = Number(0, 2)
    sauce: str = OneOf(("ketchup", "mayo", "burger"))

    def __init__(self, buns: int, cheese: int,
                 tomatoes: int, cutlets: int,
                 eggs: int, sauce: str) -> None:
        self.buns = buns
        self.cheese = cheese
        self.tomatoes = tomatoes
        self.cutlets = cutlets
        self.eggs = eggs
        self.sauce = sauce
