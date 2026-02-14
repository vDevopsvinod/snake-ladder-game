#!/usr/bin/env python3
"""
Indian Snake & Ladder Game - DevOps Demo Project
"""

import random
import time

SNAKES = {
    16: 6, 47: 26, 49: 11, 56: 53, 62: 19,
    64: 60, 87: 24, 93: 73, 95: 75, 98: 79
}

LADDERS = {
    2: 38, 7: 14, 8: 31, 15: 26, 21: 42,
    28: 84, 36: 44, 51: 67, 71: 91, 78: 99
}

def roll_dice():
    return random.randint(1, 6)

def get_new_position(position, dice_value):
    new_pos = position + dice_value
    if new_pos > 100:
        return position
    if new_pos in SNAKES:
        print(f"    🐍 SNAKE! Slid from {new_pos} to {SNAKES[new_pos]}")
        return SNAKES[new_pos]
    elif new_pos in LADDERS:
        print(f"    🪜 LADDER! Climbed from {new_pos} to {LADDERS[new_pos]}")
        return LADDERS[new_pos]
    return new_pos

def play_game(players):
    positions = {player: 0 for player in players}
    winner = None
    print("\n🇮🇳 Welcome to Indian Snake & Ladder!\n")
    while not winner:
        for player in players:
            input(f"{player}'s turn (press Enter to roll)")
            dice = roll_dice()
            print(f"    Rolled: {dice}")
            old_pos = positions[player]
            new_pos = get_new_position(old_pos, dice)
            positions[player] = new_pos
            print(f"    {player} moved from {old_pos} to {new_pos}\n")
            if new_pos == 100:
                winner = player
                break
            time.sleep(0.5)
    print(f"🎉 Congratulations {winner}! You won!\n")

if __name__ == "__main__":
    play_game(["Player 1", "Player 2"])
