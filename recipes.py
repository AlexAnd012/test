class Ingredient:
    def __init__(self, name, quantity, unit):
        self.name = name
        self.quantity = quantity
        self.unit = unit

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        value = float(value)

        if value <= 0:
            raise ValueError("количество должно быть положительным")

        self._quantity = value

    def __str__(self):
        return f"{self.name}: {self.quantity} {self.unit}"

    def __repr__(self):
        return f"Ingredient('{self.name}', {self.quantity}, '{self.unit}')"

    def __eq__(self, other):
        if not isinstance(other, Ingredient):
            return False

        return self.name == other.name and self.unit == other.unit


class Recipe:
    def __init__(self, title, ingredients):
        self.title = title
        self.ingredients = []

        for ingredient in ingredients:
            self.add_ingredient(ingredient)

    def add_ingredient(self, ingredient):
        for existing_ingredient in self.ingredients:
            if existing_ingredient == ingredient:
                existing_ingredient.quantity += ingredient.quantity
                return

        self.ingredients.append(ingredient)

    @staticmethod
    def is_valid_ratio(ratio):
        try:
            ratio = float(ratio)
        except (TypeError, ValueError):
            return False

        return ratio > 0

    def scale(self, ratio):
        if not self.is_valid_ratio(ratio):
            raise ValueError("коэффициент должен быть положительным числом")

        ratio = float(ratio)
        scaled_ingredients = []

        for ingredient in self.ingredients:
            scaled_ingredients.append(
                Ingredient(
                    ingredient.name,
                    ingredient.quantity * ratio,
                    ingredient.unit
                )
            )

        return Recipe(self.title, scaled_ingredients)

    def __len__(self):
        return len(self.ingredients)

    def __str__(self):
        result = f"{self.title}\n"

        for ingredient in self.ingredients:
            result += f"- {ingredient}\n"

        return result.strip()


class ShoppingList:
    def __init__(self):
        self._items = []

    def add_recipe(self, recipe, portions):
        portions = float(portions)

        if portions <= 0:
            raise ValueError("Количество порций должно быть положительным")

        scaled_recipe = recipe.scale(portions)

        for ingredient in scaled_recipe.ingredients:
            self._items.append((ingredient, recipe.title))

    def remove_recipe(self, title):
        self._items = [
            item for item in self._items
            if item[1] != title
        ]

    def get_list(self):
        result = {}

        for ingredient, recipe_title in self._items:
            key = (ingredient.name, ingredient.unit)

            if key in result:
                result[key] += ingredient.quantity
            else:
                result[key] = ingredient.quantity

        ingredients = []

        for (name, unit), quantity in result.items():
            ingredients.append(Ingredient(name, quantity, unit))

        ingredients.sort(key=lambda ingredient: ingredient.name)

        return ingredients

    def __add__(self, other):
        new_shopping_list = ShoppingList()

        for ingredient, recipe_title in self._items:
            copied_ingredient = Ingredient(
                ingredient.name,
                ingredient.quantity,
                ingredient.unit
            )
            new_shopping_list._items.append((copied_ingredient, recipe_title))

        for ingredient, recipe_title in other._items:
            copied_ingredient = Ingredient(
                ingredient.name,
                ingredient.quantity,
                ingredient.unit
            )
            new_shopping_list._items.append((copied_ingredient, recipe_title))

        return new_shopping_list
