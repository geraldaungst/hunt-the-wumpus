# Hunt the Wumpus

A terminal-based Python port of Gregory Yob's *Hunt the Wumpus* (1972), as it
appeared in *More BASIC Computer Games* (Ahl, 1979).

Navigate a cave built on the topology of a dodecahedron. Hunt a monster by smell
and sound. Avoid bottomless pits and super bats. Try not to shoot yourself.

## About This Port

This project is faithful to the original with three small adjustments:

- The Wumpus cannot start the game adjacent to the player
- Arrows are tracked and reported; running out of arrows ends the game
- Typing `Q` at the Shoot or Move prompt triggers an unannounced exit — a small
  easter egg not mentioned in the instructions

The terminal experience is intentionally retro. The code underneath tries to be
idiomatic, readable Python.

This is a learning project — part of a structured Python curriculum I'm working
through as a retired STEM educator. I'm interested in what's possible when you
bring modern programming practice to classic computing history, and in making that
journey visible to other learners and educators.

## Requirements

- Python 3.6 or higher
- No external dependencies

## Usage

```bash
python wumpus.py
```

## Background

*Hunt the Wumpus* is one of the earliest text adventure games and a landmark in
computing history. The cave topology — a dodecahedron with 20 rooms, each
connecting to exactly three others — gives the game a spatial logic that rewards
careful play. The original BASIC source is available at
[roug.org](https://www.roug.org/retrocomputing/languages/basic/morebasicgames/wumpus.bas)
if you want to compare.

## Contributing

This is a learning project, not a production codebase, but feedback and ideas are
genuinely welcome. If you spot a bug, have a suggestion, or just want to talk
Wumpus, open an issue.

Some directions I'm considering for future versions — no commitments, just
possibilities:

- Multiple cave topologies (Möbius strip, circular, procedurally generated)
- Persistent high scores
- Game replay and move logging
- Difficulty settings (arrow count, Wumpus speed, hazard density)
- A hint system based on logical deduction from known information
- A map the player builds as they explore

If something else occurs to you, open an issue and make the case. The best
additions will change the experience of playing *and* teach something interesting
to build.

## License

MIT License — see [LICENSE](LICENSE) for details.
