# from deck_total import Card, Deck

"""
Cоздадим имитацию ходов в “Дурака без козырей”:

1. Создайте колоду из 52 карт. Перемешайте ее.
2. Первый игрок берет сверху 10 карт
3. Второй игрок берет сверху 10 карт.
4. Игрок-1 ходит:
    4.1. игрок-1 выкладывает самую маленькую карту по "старшенству"
    4.2. игрок-2 пытается бить карту, если у него есть такая же масть, но значением больше.
    4.3. Если игрок-2 не может побить карту, то он проигрывает/забирает себе(см. пункт 7)
    4.4. Если игрок-2 бьет карту, то игрок-1 может подкинуть карту любого значения, которое есть на столе.
5. Если Игрок-2 отбился, то Игрок-1 и Игрок-2 меняются местами. Игрок-2 ходит, Игрок-1 отбивается.
6. Выведите в консоль максимально наглядную визуализацию данных ходов (библиотека rich)
7* Реализовать возможность добрать карты из колоды после того, как один из игроков отбился/взял в руку
"""
from rich.table import Table
from rich.console import Console
from deck_total import Deck, Hand, Card
from random import shuffle


def print_deck(game_deck: Deck) -> None:
    """
    осуществляет красивый вывод колоды
    :return: None
    """
    table_deck = Table(width=150)
    table_deck.add_column("Колода", style="black", justify="center")
    table_deck.add_row(str(game_deck))
    console_output.print(table_deck)


def game(forward_player: Hand, defender_player: Hand) -> tuple[Table, bool]:
    """
    Осуществляет расчет и красивый вывод одного хода
    frwd - атакующая рука
    dfdr - обороняющаяся рука
    return: обьект Table и True если произошла смена заходящего игрока или False
    если смена не произошла
    """
    table_game = Table(title=f"Ходит {forward_player.name}", width=150)
    table_game.add_column(f"{forward_player}", style="black", justify="center")
    table_game.add_column(f"Стол", style="black", justify="center")
    table_game.add_column(f"{defender_player}", justify="center", style="black")

    change_forward = False
    attack_card = first_move(forward_player)
    cards_on_table = [attack_card]
    table_game.add_row(f'{forward_player}', f'{attack_card}', f'{defender_player}')
    defend_card = defend(attack_card, defender_player)

    if defend_card:
        cards_on_table.append(defend_card)
        table_game.add_row(f'{forward_player}', f'{defend_card}', f'{defender_player}')
    else:
        defender_player.cards += cards_on_table
        table_game.add_row(f'{forward_player}', 'Забрал', f'{defender_player}')
        return table_game, change_forward

    is_has_card = True
    while is_has_card:
        attack_card = throw_up(cards_on_table)
        if attack_card:
            table_game.add_row(f'{forward_player}', f'{attack_card}', f'{defender_player}')
            cards_on_table.append(attack_card)
            defend_card = defend(attack_card, defender_player)

            if defend_card is not None:
                cards_on_table.append(defend_card)
                table_game.add_row(f'{forward_player}', f'{defend_card}', f'{defender_player}')
            else:
                defender_player.cards += cards_on_table
                table_game.add_row(f'{forward_player}', 'Забрал', f'{defender_player}')
                is_has_card = False
        else:
            table_game.add_row(f'{forward_player}', 'Бито', f'{defender_player}')
            is_has_card = False
            change_forward = True
    return table_game, change_forward


def first_move(forward_player: Hand) -> Card:
    """
    Забирает из руки минимальные карты
    frwd: рука
    return: Минимальную карту руки
    """
    return forward_player.cards.pop(forward_player.cards.index(min(forward_player.cards)))


def defend(crd: Card, player: Hand) -> Card or None:
    """
    забирает из руки минимальную карту которой игрок может отбиться
    crd: карта с которой зашел атакующий
    player: обороняющийся игрок
    return: карту, если отбиться нечем None
    """
    res = [card for card in player if crd.eq_suits(card) and card > crd]

    if res:
        return player.cards.pop(player.cards.index(min(res)))


def throw_up(cards_on_table: list) -> Card or None:
    """
    забирает минимальную карту которую можно подкинуть
    cards_on_table: список карт на столе
    return: карту, если такой нет - None
    """
    value_on_table = [card.value for card in cards_on_table]
    cards = [card for card in forward if card.value in value_on_table]

    if cards:
        return forward.cards.pop(forward.cards.index(min(cards)))


def fill_hands(player: Hand) -> None:
    """
    если в колоде есть карты и у игрока меньше 10 карт
     пополняет количество карт до 10
     player: рука
     return: None
    """
    quantity = len(player.cards)
    length_deck = len(deck_game.cards)
    if length_deck < quantity:
        quantity = length_deck
    if quantity < 10:
        player.cards += deck_game.draw(10 - quantity)

if __name__ == "__main__":
    console_output = Console(width=150, style="black on green")
    deck_game = Deck()
    print_deck(deck_game)
    player1 = Hand(deck_game, 'Трус')
    player2 = Hand(deck_game, 'Балбес')
    players = [player1, player2]
    shuffle(players)
    forward = players[0]
    defender = players[1]
    while deck_game.cards:
        table, change = game(forward, defender)
        console_output.print(table)
        fill_hands(forward)
        fill_hands(defender)
        if change:
            forward, defender = defender, forward
    while forward.cards and defender.cards:
        table, change = game(forward, defender)
        console_output.print(table)
        if change:
            forward, defender = defender, forward
