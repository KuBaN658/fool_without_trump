import random
from typing_extensions import Self

# ♥ ♦ ♣ ♠
VALUES = {'2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6,
          '8': 7, '9': 8, '10': 9, 'J': 10, 'Q': 11, 'K': 12, 'A': 13}
SUITS = {'Spades': 0.1, 'Clubs': 0.2, 'Diamonds': 0.3, 'Hearts': 0.4}
SUITS_UNI = {
    'Spades': '[black]♠[/]',
    'Clubs': '[black]♣[/]',
    'Diamonds': '[red]♦[/]',
    'Hearts': '[red]♥[/]'
}


class Card:
    def __init__(self, value, suit):
        self.value = value  # Значение карты(2, 3... 10, J, Q, K, A)
        self.suit = suit    # Масть карты
        self.point = SUITS[suit] + VALUES[value]

    def __str__(self):
        return f'{self.value}{SUITS_UNI[self.suit]}'

    def eq_suits(self, other_card: Self) -> bool:
        """
        проверяет эквивалентность мастей карт
        return: bool
        """
        if type(other_card) == Card:
            return self.suit == other_card.suit
        else:
            raise TypeError('В колоде есть что-то не похожее на карты')

    def __gt__(self, other_card: Self):
        if type(other_card) == Card:
            return self.point > other_card.point
        else:
            raise TypeError('В колоде есть что-то не похожее на карты')

    def __lt__(self, other_card: Self):
        if type(other_card) == Card:
            return self.point < other_card.point
        else:
            raise TypeError('В колоде есть что-то не похожее на карты')


class Deck:
    def __init__(self):
        self.cards = [Card(value, suit)
                      for suit in SUITS for value in VALUES]
        self.hands = []
        self.memory = -1
        self.index = -1
        self.shuffle()

    def __str__(self):
        return f'deck[{len(self.cards)}]: ' + \
               ', '.join([str(card) for card in self.cards])

    def __getitem__(self, item):
        return self.cards[item]

    def __next__(self):
        self.index += 1
        if self.index < len(self.cards):
            return self.cards[self.index]
        else:
            raise StopIteration

    def __iter__(self):
        self.index = self.memory
        return self

    def draw(self, quantity) -> list[Card]:
        """
        удаляет карты из колоды
        quantity: количество карт
        return: возвращает список удаленных карт
        """
        if quantity > len(self.cards):
            quantity = len(self.cards)
        result = [self.cards.pop(0) for _ in range(quantity)]
        return result

    def shuffle(self) -> None:
        """
        Перемешивает колоду
        return: None
        """
        random.shuffle(self.cards)


class Hand:
    def __init__(self, dck: Deck, name):
        self.cards = dck.draw(10)
        self.name = name
        self.memory = -1
        self.index = -1

    def __str__(self):
        return f'{self.name}[{len(self.cards)}]: ' + ', '.join(map(str, self.cards))

    def __getitem__(self, item):
        return self.cards[item]

    def __next__(self):
        self.index += 1
        if self.index < len(self.cards):
            return self.cards[self.index]
        else:
            raise StopIteration

    def __iter__(self):
        self.index = self.memory
        return self


if __name__ == '__main__':
    deck = Deck()
    deck.shuffle()
    hnd = Hand(deck, 'name')
    for i in hnd:
        print(i)
    print('=' * 40)
    for i in hnd:
        print(i)
    print(hnd)
    print(hnd[0])
    print('=' * 40)
    for i in deck:
        print(i)
    print('=' * 40)
    for i in deck:
        print(i)
    print(deck[-1])
# Список ВСЕХ magic-методов см. тут: http://pythonworld.ru/osnovy/peregruzka-operatorov.html
