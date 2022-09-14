from abc import ABC, abstractmethod
from enum import Enum


class ChiefMood(Enum):
    """Настроение начальника"""
    GOOD = 1
    BAD = 2
    BETTER_STAY_AWAY = 3


class Strategy(ABC):
    """Интерфейс стратегии"""

    @abstractmethod
    def check_mood_chief(self, mood: ChiefMood) -> bool:
        ...

    @abstractmethod
    def order_processing(self, money: int) -> str:
        ...


class GoodStrategy(Strategy):

    def check_mood_chief(self, mood: ChiefMood) -> bool:
        if (mood is ChiefMood.GOOD or
                mood is ChiefMood.BAD):
            return True
        return False

    def order_processing(self, money: int) -> str:
        return "Самый лучшый напиток, который возможен!"


class BadStrategy(Strategy):

    def check_mood_chief(self, mood: ChiefMood) -> bool:
        if (mood is ChiefMood.BETTER_STAY_AWAY or
                mood is ChiefMood.BAD):
            return True
        return False

    def order_processing(self, money: int) -> str:
        return "И стакан воды сойдет!"


class NormalStrategy(Strategy):

    def check_mood_chief(self, mood: ChiefMood) -> bool:
        # может у шефа и плохое настроение
        # но клиенты то тут не при чем
        return True

    def order_processing(self, money: int) -> str:
        if money < 5:
            return "Вежливо отказаться от заказа клиента"
        elif money < 10:
            return "Приготовить espresso"
        elif money < 20:
            return "Приготовить капучино"
        elif money < 50:
            return "Приготовить отменный кофе"
        else:
            return "Самый лучшый напиток, который возможен!"


class Barista:
    def __init__(self, strategy: Strategy,
                 chief_mood: ChiefMood):
        self._strategy = strategy
        self._chief_mood = chief_mood
        print(f"Изначальное настроение шефа: {chief_mood.name}")

    def get_chief_mood(self) -> ChiefMood:
        return self._chief_mood

    def set_chief_mood(self, chief_mood: ChiefMood) -> None:
        print(f"Текущее настроение шефа: {chief_mood.name}")
        self._chief_mood = chief_mood

    def set_strategy(self, strategy: Strategy) -> None:
        self._strategy = strategy

    def take_order(self, money: int) -> None:
        print(f"Клиент отдает за заказ {money} рублей")
        if self._strategy.check_mood_chief(self._chief_mood):
            print(self._strategy.order_processing(money))
        else:
            print("Сделать вид, что не заметил клиента!")


if __name__ == "__main__":
    barista = Barista(NormalStrategy(),
                      ChiefMood.BETTER_STAY_AWAY)
    barista.take_order(20)
    barista.take_order(50)
    barista.set_strategy(BadStrategy())
    barista.take_order(40)
    barista.take_order(200)
    barista.set_strategy(GoodStrategy())
    barista.take_order(40)
    barista.set_chief_mood(ChiefMood.GOOD)
    barista.take_order(0)



from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List


class Context():
    """
    Контекст определяет интерфейс, представляющий интерес для клиентов.
    """

    def __init__(self, strategy: Strategy) -> None:
        """
        Обычно Контекст принимает стратегию через конструктор, а также
        предоставляет сеттер для её изменения во время выполнения.
        """

        self._strategy = strategy

    @property
    def strategy(self) -> Strategy:
        """
        Контекст хранит ссылку на один из объектов Стратегии. Контекст не знает
        конкретного класса стратегии. Он должен работать со всеми стратегиями
        через интерфейс Стратегии.
        """

        return self._strategy

    @strategy.setter
    def strategy(self, strategy: Strategy) -> None:
        """
        Обычно Контекст позволяет заменить объект Стратегии во время выполнения.
        """

        self._strategy = strategy

    def do_some_business_logic(self, db: list) -> None:
        """
        Вместо того, чтобы самостоятельно реализовывать множественные версии
        алгоритма, Контекст делегирует некоторую работу объекту Стратегии.
        """

        # ...

        print("Context: Sorting data using the strategy (not sure how it'll do it)")
        result = self._strategy.do_algorithm(db)
        print(f' Your {result}')

        # ...


class Strategy(ABC):
    """
    Интерфейс Стратегии объявляет операции, общие для всех поддерживаемых версий
    некоторого алгоритма.

    Контекст использует этот интерфейс для вызова алгоритма, определённого
    Конкретными Стратегиями.
    """

    @abstractmethod
    def do_algorithm(self, data: List):
        pass


"""
Конкретные Стратегии реализуют алгоритм, следуя базовому интерфейсу Стратегии.
Этот интерфейс делает их взаимозаменяемыми в Контексте.
"""


class ConcreteStrategyA(Strategy):
    def do_algorithm(self, data: List) -> List:
        return sorted(data)


class ConcreteStrategyB(Strategy):
    def do_algorithm(self, data: List) -> List:
        return [1, 2, 3, 4, 5, 6, 7]


if __name__ == "__main__":
    # Клиентский код выбирает конкретную стратегию и передаёт её в контекст.
    # Клиент должен знать о различиях между стратегиями, чтобы сделать
    # правильный выбор.

    context = Context(ConcreteStrategyA())
    print("Client: Strategy is set to normal sorting.")
    context.do_some_business_logic([4, 2, 3, 1])
    print()

    print("Client: Strategy is set to reverse sorting.")
    context.strategy = ConcreteStrategyB()
    context.do_some_business_logic([4, 2, 3, 1])
