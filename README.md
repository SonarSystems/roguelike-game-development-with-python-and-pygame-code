# Roguelike Game Development with Python and Pygame — Companion Code

*Build a Complete Dungeon Crawler with Procedural Generation, Smart Monsters, and Permadeath*

This is the official companion code repository for **Roguelike Game Development with Python and Pygame**, published by SonarSystems. Every runnable example in the book lives here, organized by chapter, exactly as it appears in the text — clone it, follow along, and run the examples yourself instead of retyping them from the page.

## Chapters

| Chapter | Title | Code |
|---|---|---|
| 2 | Setting Up Your Workshop | [`ch02-setting-up-your-workshop/`](ch02-setting-up-your-workshop/) — 1 file |
| 3 | The Game Loop and the Grid | [`ch03-the-game-loop-and-the-grid/`](ch03-the-game-loop-and-the-grid/) — 9 files |
| 4 | Maps, Tiles and Walls | [`ch04-maps-tiles-and-walls/`](ch04-maps-tiles-and-walls/) — 12 files |
| 5 | Entities and Actions | [`ch05-entities-and-actions/`](ch05-entities-and-actions/) — 16 files |
| 6 | Procedural Dungeons I: Rooms and Corridors | [`ch06-procedural-dungeons-i-rooms-and-corridors/`](ch06-procedural-dungeons-i-rooms-and-corridors/) — 21 files |
| 7 | Procedural Dungeons II: BSP, Caves and Drunkards | [`ch07-procedural-dungeons-ii-bsp-caves-and-drunkards/`](ch07-procedural-dungeons-ii-bsp-caves-and-drunkards/) — 20 files |
| 8 | Field of View and Fog of War | [`ch08-field-of-view-and-fog-of-war/`](ch08-field-of-view-and-fog-of-war/) — 22 files |
| 9 | Monsters and Turn Order | [`ch09-monsters-and-turn-order/`](ch09-monsters-and-turn-order/) — 27 files |
| 10 | Pathfinding: A* and Dijkstra Maps | [`ch10-pathfinding-a-and-dijkstra-maps/`](ch10-pathfinding-a-and-dijkstra-maps/) — 26 files |
| 11 | Combat, Death and Permadeath | [`ch11-combat-death-and-permadeath/`](ch11-combat-death-and-permadeath/) — 29 files |
| 12 | The Interface: Health Bars, Messages and Tooltips | [`ch12-the-interface-health-bars-messages-and-tooltips/`](ch12-the-interface-health-bars-messages-and-tooltips/) — 29 files |
| 13 | Items and Inventory | [`ch13-items-and-inventory/`](ch13-items-and-inventory/) — 38 files |
| 14 | Scrolls, Targeting and Spells | [`ch14-scrolls-targeting-and-spells/`](ch14-scrolls-targeting-and-spells/) — 34 files |
| 15 | Going Deeper: Stairs, Floors and Difficulty | [`ch15-going-deeper-stairs-floors-and-difficulty/`](ch15-going-deeper-stairs-floors-and-difficulty/) — 37 files |
| 16 | Character Growth: Experience, Levels and Equipment | [`ch16-character-growth-experience-levels-and-equipment/`](ch16-character-growth-experience-levels-and-equipment/) — 36 files |
| 17 | Saving, Loading and Permadeath Done Right | [`ch17-saving-loading-and-permadeath-done-right/`](ch17-saving-loading-and-permadeath-done-right/) — 36 files |
| 18 | Game Feel: Animation, Camera and Juice | [`ch18-game-feel-animation-camera-and-juice/`](ch18-game-feel-animation-camera-and-juice/) — 41 files |
| 19 | Testing and Tuning a Procedural Game | [`ch19-testing-and-tuning-a-procedural-game/`](ch19-testing-and-tuning-a-procedural-game/) — 40 files |
| 20 | Shipping Your Roguelike | [`ch20-shipping-your-roguelike/`](ch20-shipping-your-roguelike/) — 38 files |

## The `engine/` package

Several early chapters build up a small, reusable engine — classes shared across every later chapter's examples rather than redefined each time. This repo assembles those classes into a real, importable `engine/` package at the repo root (mirroring the project layout the book itself has you build), so `from engine.game_loop import GameLoop`-style imports in later chapters resolve exactly like they do if you followed along and built the same structure yourself. Run any example that imports from `engine/` from the repo root (or add the repo root to your `PYTHONPATH`) for the import to work:

```bash
cd roguelike-game-development-with-python-and-pygame-code
python3 chNN-.../NN-example.py
```

## Prerequisites

- **Python** — Python 3.10+.

## Running the examples

**Python** — run a single example directly:

```bash
python3 chNN-.../NN-example.py
```

## Running the tests

Every example has a smoke test under `tests/` (compiles cleanly for compiled languages; runs cleanly and passes its assertions for scripted languages). From the repo root:

```bash
pip3 install pytest
pytest tests/ -v
```

## License

The code in this repository is released under the MIT License — see [`LICENSE`](LICENSE). The accompanying book text is a separate, commercial work and is **not** covered by this license.

---

This is the official companion repository for *Roguelike Game Development with Python and Pygame* (github.com/SonarSystems/roguelike-game-development-with-python-and-pygame-code), maintained by SonarSystems.
