#!/usr/bin/env python3
"""
wumpus.py

A terminal-based Python port of Gregory Yob's Hunt the Wumpus (1972), as it
appeared in More BASIC Computer Games (Ahl, 1979). The player navigates a cave
built on the topology of a dodecahedron, hunting a monster by smell and sound
while avoiding bats and bottomless pits.

Game functionality is faithful to the original with a few small adjustments:
    - If player attempts to quit (Q when prompted for move), a random message
      is shown before ending the game.
    - Wumpus cannot begin the game adjacent to the player.
    - Arrows are tracked and reported. Out of arrows also ends the game with a loss.

Usage: python wumpus.py
"""
import random
import sys
from enum import Enum

CAVE = {
    1: [2, 5, 8],
    2: [1, 3, 10],
    3: [2, 4, 12],
    4: [3, 5, 14],
    5: [1, 4, 6],
    6: [5, 7, 15],
    7: [6, 8, 17],
    8: [1, 7, 9],
    9: [8, 10, 18],
    10: [2, 9, 11],
    11: [10, 12, 19],
    12: [3, 11, 13],
    13: [12, 14, 20],
    14: [4, 13, 15],
    15: [6, 14, 16],
    16: [15, 17, 20],
    17: [7, 16, 18],
    18: [9, 17, 19],
    19: [11, 18, 20],
    20: [13, 16, 19]
}

QUIT_RESPONSES = [
    "Try as you might, you cannot escape the cave. You are lost forever.",
    "You manage to find a passage that wasn't obvious before. You're free!",
    "Turns out one of the bottomless pits actually wasn't bottomless. It's a path to the outside.",
    "The wumpus is relentless and unfortunately catches you within minutes.",
    "You somehow manage to convince the superbats to fly you home!",
    "The bats snatch you up and drop you into a bottomless pit. Better luck next time."
]


class Outcome(Enum):
    MISS = "miss"
    WUMPUS = "hit_wumpus"
    PLAYER = "hit_player"
    HAZARD = "encounter_hazard"
    BACKTRACK = "backtrack"
    NULL = "no_outcome"


class Hazard:
    def __init__(self, kind, location, warning):
        self.kind = kind
        self.location = location
        self.warning = warning


class Wumpus(Hazard):
    def __init__(self, location, warning):
        super().__init__("wumpus", location, warning)
        self.alive = True

    def bumped(self):
        rooms = CAVE[self.location] + [self.location]
        self.location = random.choice(rooms)


class Player:
    def __init__(self, location, arrows):
        self.location = location
        self.arrows = arrows
        self.alive = True


# Warnings that go with each hazard
HAZARDS = {
    "bat": "Bats nearby!",
    "pit": "I feel a draft."
}

QTY_PER_HAZARD = 2
ARROW_COUNT = 5


def cave_setup():
    rooms = list(CAVE.keys())
    hazard_list = []
    for hazard in HAZARDS:
        for _ in range(QTY_PER_HAZARD):
            hazard_list.append(Hazard(hazard, rooms.pop(random.randrange(0, len(rooms))), HAZARDS[hazard]))

    player = Player(rooms.pop(random.randrange(0, len(rooms))), ARROW_COUNT)
    # Extracts all remaining rooms that are not adjacent to the player so the Wumpus won't land there
    rooms = [room for room in rooms if room not in CAVE[player.location]]
    wumpus = Wumpus(rooms.pop(random.randrange(0, len(rooms))), "I smell a wumpus!")
    hazard_list.append(wumpus)
    return player, wumpus, hazard_list


def give_warnings(this_room, hazards):
    warnings = set()
    for hazard in hazards:
        if hazard.location in CAVE[this_room]:
            warnings.add(hazard.warning)
    for warning in sorted(warnings, reverse=True):
        print(warning)


def where_is_player(location):
    print(f"You are in room {location}")
    a, b, c = CAVE[location]
    print(f"Tunnels lead to {a}, {b}, and {c}")


def get_player_move():
    while True:
        move = input("Shoot or move (S/M)? ").upper()
        if move in ("S", "M"):
            return move
        if move == "Q":
            print(random.choice(QUIT_RESPONSES))
            sys.exit()


def check_for_hit(room, player_location, target_location):
    if room == player_location:
        return Outcome.PLAYER
    if room == target_location:
        return Outcome.WUMPUS
    return Outcome.MISS


def shoot_arrow(player, wumpus_location):
    arrow_path = []
    while True:
        rooms = input("No. of rooms (1-5)? ")
        try:
            rooms = int(rooms)
            if 1 <= rooms <= 5:
                break
        except ValueError:
            continue
    while True:
        try:
            arrow_path = [int(input(f"Room {r} > ")) for r in range(1, rooms + 1)]
            break
        except ValueError:
            print("Invalid room")
            continue
    this_room = player.location
    shot_outcome = Outcome.MISS
    for node, next_room in enumerate(arrow_path):
        if node >= 2 and next_room == arrow_path[node - 2]:
            return Outcome.BACKTRACK
        if next_room in CAVE[this_room]:
            this_room = next_room
        else:
            this_room = random.choice(CAVE[this_room])
        shot_outcome = check_for_hit(this_room, player.location, wumpus_location)
        if shot_outcome != Outcome.MISS:
            break
    player.arrows -= 1
    return shot_outcome


def move_player(player):
    new_location = player.location
    while True:
        try:
            new_location = int(input("Where to? "))
        except ValueError:
            print("Invalid room")
            continue
        if new_location in [player.location, *CAVE[player.location]]:
            break
        print("Not possible")
    player.location = new_location


def encounter_handler(player, wumpus, hazards):
    for hazard in hazards:
        if player.alive and player.location == hazard.location:
            if hazard.kind == "wumpus":
                print("... Oops! Bumped a wumpus!")
                wumpus.bumped()
                if wumpus.location == player.location:
                    print("Tsk tsk tsk - Wumpus got you!")
                    player.alive = False
                break
            elif hazard.kind == "bat":
                print("Zap - super bat snatch! Elsewhereville for you!")
                player.location = random.randint(1, 20)
                encounter_handler(player, wumpus, hazards)
                break
            elif hazard.kind == "pit":
                print("Yyyyiiiieee . . . fell in pit")
                player.alive = False
                break


def main():
    game_over = False
    first_play = True
    while not game_over:
        print("---> Hunt the Wumpus <---")
        if first_play:
            print("This is an old-style cave hunt. You are expected to learn by playing.")
            first_play = False
        # Set up initial conditions
        player, wumpus, hazards = cave_setup()

        # Main game loop
        while True:
            give_warnings(player.location, hazards)
            where_is_player(player.location)
            player_move = get_player_move()
            outcome = Outcome.NULL
            if player_move == "S":
                while True:
                    outcome = shoot_arrow(player, wumpus.location)
                    if outcome != Outcome.BACKTRACK:
                        break
                    print("Arrows aren't that crooked - try another room")
                if outcome == Outcome.MISS:
                    print("Missed.")
                    wumpus.bumped()
                elif outcome == Outcome.PLAYER:
                    print("Ouch! Arrow got you!")
                    player.alive = False
                elif outcome == Outcome.WUMPUS:
                    print("Aha! You got the wumpus!")
                    wumpus.alive = False
            elif player_move == "M":
                move_player(player)
                encounter_handler(player, wumpus, hazards)
            if not wumpus.alive:
                print("Hee hee hee - the wumpus'll getcha next time!!")
                break
            if player.arrows > 0:
                print(f"You have {player.arrows} arrows remaining.")
            else:
                print("You have no more arrows. The wumpus eventually catches up to you. You cannot defend yourself.")
                player.alive = False
            if not player.alive:
                print("Ha ha ha - you lose!")
                break

        # Continue or end
        while True:
            play_again = input("Play again (Y/N)?").upper()
            if play_again == "Y":
                break
            if play_again == "N":
                game_over = True
                break
            print("Invalid choice")

    print("---> Game Over <---")


if __name__ == "__main__":
    main()
