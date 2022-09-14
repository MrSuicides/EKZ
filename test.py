from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
import math


class Context():

    def __init__(self, figure: Figure) -> None:
        self._figure = figure

    def do_something_logic(self, db: list) -> None:
        result = self._figure.full_info(db)

        print(f'{result[0]}:\nPerimetr {result[1]}\n'
              f'Rotation {result[2]}')


class Figure(ABC):

    @abstractmethod
    def full_info(self, data: List):
        ...


class Rectangle(Figure):

    def full_info(self, points: List) -> List:
        sides = self.search_side(points[0], points[1], points[2])
        perimetr = self.calcPerimeter(sides)
        rotation = self.rotation_figure(points)
        return ['Rectangle', perimetr, rotation]

    def search_side(self, a: List, b: List, d: List) -> List:  # [-4, -2], [4, -2], [4, 2]
        first_side = ((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** 0.5
        second_side = ((b[0] - d[0]) ** 2 + (b[1] - d[1]) ** 2) ** 0.5
        return [first_side, second_side]

    def calcPerimeter(self, sides: List) -> int:
        w, h = sides[0], sides[1]
        perimeter = w * 2 + h * 2
        return perimeter

    def rotation_figure(self, points: List) -> List:
        f = input('Grade rotation: ')
        f = int(f) * (3.14 / 180)
        result = []
        for i in points:
            x = i[0] * math.cos(f) - i[1] * math.sin(f)
            y = i[0] * math.sin(f) + i[1] * math.cos(f)
            result.append([x, y])
        return result

    # def calcSpace(self):
    #     x, y = self.search_side()
    #     space = x * y
    #     return space


if __name__ == "__main__":
    context = Context(Rectangle())
    context.do_something_logic([[-4, -2], [4, -2], [4, 2], [-4, 2]])
    #123
