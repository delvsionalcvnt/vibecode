#!/usr/bin/env python3
"""Простенькое консольное казино: слоты, рулетка, монетка."""

import random
import time

START_BALANCE = 1000

SLOT_SYMBOLS = ["🍒", "🍋", "🔔", "⭐", "💎", "7️⃣"]
# множители выигрыша за три одинаковых символа
SLOT_PAYOUTS = {"🍒": 5, "🍋": 8, "🔔": 12, "⭐": 20, "💎": 50, "7️⃣": 100}

RED_NUMBERS = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}


def ask_bet(balance: int) -> int | None:
    """Спрашивает ставку. Возвращает None, если игрок хочет назад в меню."""
    while True:
        raw = input(f"Ставка (баланс {balance}, Enter — назад): ").strip()
        if not raw:
            return None
        if not raw.isdigit() or int(raw) <= 0:
            print("Введи положительное целое число.")
            continue
        bet = int(raw)
        if bet > balance:
            print("Столько у тебя нет.")
            continue
        return bet


def play_slots(balance: int) -> int:
    print("\n🎰 СЛОТЫ — три одинаковых = выигрыш, два одинаковых = возврат ставки")
    bet = ask_bet(balance)
    if bet is None:
        return balance

    balance -= bet
    reels = [random.choice(SLOT_SYMBOLS) for _ in range(3)]

    # маленькая "анимация"
    for _ in range(3):
        print("  ".join(random.choice(SLOT_SYMBOLS) for _ in range(3)), end="\r")
        time.sleep(0.3)
    print("  ".join(reels) + "   ")

    if reels[0] == reels[1] == reels[2]:
        win = bet * SLOT_PAYOUTS[reels[0]]
        print(f"ДЖЕКПОТ! x{SLOT_PAYOUTS[reels[0]]} → +{win}")
        balance += win
    elif len(set(reels)) == 2:
        print("Пара — ставка возвращается.")
        balance += bet
    else:
        print(f"Мимо. -{bet}")
    return balance


def play_roulette(balance: int) -> int:
    print("\n🎡 РУЛЕТКА (0–36)")
    print("  red / black — x2, even / odd — x2, число 0–36 — x36")
    choice = input("На что ставишь? ").strip().lower()
    valid_words = {"red", "black", "even", "odd"}
    if choice not in valid_words and not (choice.isdigit() and 0 <= int(choice) <= 36):
        print("Не понял ставку.")
        return balance

    bet = ask_bet(balance)
    if bet is None:
        return balance

    balance -= bet
    number = random.randint(0, 36)
    color = "green" if number == 0 else ("red" if number in RED_NUMBERS else "black")
    print(f"Выпало: {number} ({color})")

    won = False
    multiplier = 2
    if choice.isdigit():
        won = int(choice) == number
        multiplier = 36
    elif choice in ("red", "black"):
        won = choice == color
    elif number != 0:
        won = (choice == "even") == (number % 2 == 0)

    if won:
        win = bet * multiplier
        print(f"Победа! +{win}")
        balance += win
    else:
        print(f"Проигрыш. -{bet}")
    return balance


def play_coinflip(balance: int) -> int:
    print("\n🪙 МОНЕТКА — орёл или решка, x2")
    side = input("Орёл (o) или решка (r)? ").strip().lower()
    if side not in ("o", "r"):
        print("Нужно o или r.")
        return balance

    bet = ask_bet(balance)
    if bet is None:
        return balance

    balance -= bet
    result = random.choice(["o", "r"])
    print("Выпал " + ("орёл" if result == "o" else "решка"))
    if result == side:
        print(f"Угадал! +{bet * 2}")
        balance += bet * 2
    else:
        print(f"Не угадал. -{bet}")
    return balance


def main() -> None:
    balance = START_BALANCE
    games = {"1": play_slots, "2": play_roulette, "3": play_coinflip}

    print("=" * 36)
    print("   ДОБРО ПОЖАЛОВАТЬ В VIBE CASINO")
    print("=" * 36)

    while balance > 0:
        print(f"\n💰 Баланс: {balance}")
        print("1) Слоты   2) Рулетка   3) Монетка   0) Выйти")
        choice = input("> ").strip()

        if choice == "0":
            break
        game = games.get(choice)
        if game is None:
            print("Нет такого пункта.")
            continue
        balance = game(balance)

    if balance <= 0:
        print("\nТы всё просадил. Казино всегда в плюсе 💸")
    else:
        diff = balance - START_BALANCE
        sign = "+" if diff >= 0 else ""
        print(f"\nУходишь с {balance} ({sign}{diff}). Заходи ещё!")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nПока!")
