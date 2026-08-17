#!/usr/bin/env python3
"""Run a reproducible multi-state, reflection-isotropic 1D cellular automaton."""

from __future__ import annotations

import argparse
import itertools
import json
import math
from pathlib import Path
from typing import Iterable

import numpy as np
from PIL import Image

DEFAULT_PALETTE = [
    [0, 0, 0], [68, 68, 255], [136, 68, 255], [255, 68, 255],
    [255, 68, 136], [255, 255, 68], [68, 255, 255], [255, 255, 255],
    [136, 255, 136], [255, 160, 68], [120, 180, 255], [180, 255, 180],
]


def canonical(neighborhood: Iterable[int]) -> tuple[int, ...]:
    values = tuple(int(value) for value in neighborhood)
    return min(values, values[::-1])


def expected_isotropic_class_count(states: int, neighborhood: int) -> int:
    return (states ** neighborhood + states ** ((neighborhood + 1) // 2)) // 2


def all_canonical_neighborhoods(states: int, neighborhood: int) -> list[tuple[int, ...]]:
    classes = {canonical(values) for values in itertools.product(range(states), repeat=neighborhood)}
    return sorted(classes)


def generate_rules(states: int, neighborhood: int, lambda_value: float, rng: np.random.Generator) -> dict[tuple[int, ...], int]:
    if not 0 <= lambda_value <= 1:
        raise ValueError("lambda value must be between 0 and 1")
    rules: dict[tuple[int, ...], int] = {}
    for key in all_canonical_neighborhoods(states, neighborhood):
        if not any(key):
            rules[key] = 0
        elif rng.random() < lambda_value:
            rules[key] = int(rng.integers(1, states))
        else:
            rules[key] = 0
    return rules


def load_rules(serialized: dict[str, int]) -> dict[tuple[int, ...], int]:
    return {tuple(int(value) for value in key.split(",")): int(output) for key, output in serialized.items()}


def serialize_rules(rules: dict[tuple[int, ...], int]) -> dict[str, int]:
    return {",".join(map(str, key)): int(value) for key, value in sorted(rules.items())}


def create_initial_world(mode: str, width: int, states: int, fill: float, rng: np.random.Generator) -> np.ndarray:
    if not 0 <= fill <= 1:
        raise ValueError("fill must be between 0 and 1")
    world = np.zeros(width, dtype=np.int16)
    if mode == "single-dot":
        if width % 2 == 1:
            world[width // 2] = 1
        else:
            world[width // 2 - 1:width // 2 + 1] = 1
        return world
    if mode != "symmetric-random":
        raise ValueError(f"Unsupported initial mode: {mode}")

    left_width = width // 2
    active = rng.random(left_width) < fill
    left = np.where(active, rng.integers(1, states, left_width), 0).astype(np.int16)
    world[:left_width] = left
    world[-left_width:] = left[::-1]
    if width % 2 and rng.random() < fill:
        world[left_width] = int(rng.integers(1, states))
    return world


def evolve(initial: np.ndarray, rules: dict[tuple[int, ...], int], neighborhood: int, generations: int) -> np.ndarray:
    if generations < 1:
        raise ValueError("generations must be at least 1")
    width = len(initial)
    radius = neighborhood // 2
    history = np.empty((generations, width), dtype=np.int16)
    history[0] = initial
    for generation in range(1, generations):
        previous = history[generation - 1]
        next_world = np.empty_like(previous)
        for position in range(width):
            neighborhood_values = [previous[(position + offset) % width] for offset in range(-radius, radius + 1)]
            next_world[position] = rules[canonical(neighborhood_values)]
        history[generation] = next_world
    return history


def symmetry_score(history: np.ndarray) -> float:
    return float(np.mean(history == history[:, ::-1]))


def palette_for(states: int) -> np.ndarray:
    colors = list(DEFAULT_PALETTE)
    if states > len(colors):
        for index in range(len(colors), states):
            colors.append([int((53 * index) % 256), int((97 * index) % 256), int((193 * index) % 256)])
    return np.array(colors[:states], dtype=np.uint8)


def save_outputs(output_dir: Path, config: dict, rules: dict[tuple[int, ...], int], initial: np.ndarray, history: np.ndarray) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "config.json").write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    (output_dir / "rules.json").write_text(json.dumps(serialize_rules(rules), indent=2) + "\n", encoding="utf-8")
    (output_dir / "initial_world.json").write_text(json.dumps(initial.tolist()) + "\n", encoding="utf-8")
    np.save(output_dir / "history.npy", history)
    Image.fromarray(palette_for(config["states"])[history], "RGB").save(output_dir / "render.png")

    living_fraction = float(np.mean(history > 0))
    active_rules = sum(output > 0 for output in rules.values())
    summary = {
        "isotropic_class_count": len(rules),
        "expected_isotropic_class_count": expected_isotropic_class_count(config["states"], config["neighborhood"]),
        "active_rule_count": active_rules,
        "active_rule_fraction": active_rules / max(1, len(rules) - 1),
        "living_cell_fraction": living_fraction,
        "state_history_reflection_symmetry": symmetry_score(history),
        "exact_mirror_symmetry": bool(np.array_equal(history, history[:, ::-1])),
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")


def build_config_from_args(args: argparse.Namespace) -> dict:
    return {
        "states": args.states,
        "neighborhood": args.neighborhood,
        "width": args.width,
        "generations": args.generations,
        "lambda_value": args.lambda_value,
        "initial": args.initial,
        "fill": args.fill,
        "seed": args.seed,
        "boundary": "periodic",
        "rule_generation": "random canonical reflection-isotropic neighborhoods; all-zero neighborhood fixed to state 0",
    }


def validate_config(config: dict) -> None:
    if config["states"] < 2:
        raise ValueError("states must be at least 2")
    if config["neighborhood"] < 3 or config["neighborhood"] % 2 == 0:
        raise ValueError("neighborhood must be an odd integer of at least 3")
    if config["width"] < config["neighborhood"]:
        raise ValueError("width must be at least the neighborhood size")
    if config["generations"] < 1:
        raise ValueError("generations must be at least 1")
    if config.get("boundary", "periodic") != "periodic":
        raise ValueError("this runner currently supports periodic boundaries only")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_dir", type=Path, help="Directory for reproducible simulation outputs")
    parser.add_argument("--config", type=Path, help="Existing config.json to regenerate")
    parser.add_argument("--rules-file", type=Path, help="Optional rules.json with comma-separated canonical neighborhoods")
    parser.add_argument("--initial-world-file", type=Path, help="Optional JSON array containing the exact initial world")
    parser.add_argument("--states", type=int, default=9)
    parser.add_argument("--neighborhood", type=int, default=5)
    parser.add_argument("--width", type=int, default=800)
    parser.add_argument("--generations", type=int, default=1200)
    parser.add_argument("--lambda-value", type=float, default=0.33)
    parser.add_argument("--initial", choices=["symmetric-random", "single-dot"], default="symmetric-random")
    parser.add_argument("--fill", type=float, default=0.5)
    parser.add_argument("--seed", type=int, default=20260817)
    args = parser.parse_args()

    if args.config:
        if not args.config.is_file():
            parser.error(f"Config does not exist: {args.config}")
        config = json.loads(args.config.read_text(encoding="utf-8"))
    else:
        config = build_config_from_args(args)
    validate_config(config)

    rng = np.random.default_rng(config["seed"])
    if args.rules_file:
        if not args.rules_file.is_file():
            parser.error(f"Rules file does not exist: {args.rules_file}")
        rules = load_rules(json.loads(args.rules_file.read_text(encoding="utf-8")))
        expected_keys = set(all_canonical_neighborhoods(config["states"], config["neighborhood"]))
        if set(rules) != expected_keys:
            parser.error("Rules file must include every canonical neighborhood exactly once")
        if rules.get(tuple([0] * config["neighborhood"])) != 0:
            parser.error("Rules file must map the all-zero neighborhood to state 0")
    else:
        rules = generate_rules(config["states"], config["neighborhood"], config["lambda_value"], rng)

    if args.initial_world_file:
        if not args.initial_world_file.is_file():
            parser.error(f"Initial-world file does not exist: {args.initial_world_file}")
        initial = np.asarray(json.loads(args.initial_world_file.read_text(encoding="utf-8")), dtype=np.int16)
        if initial.shape != (config["width"],):
            parser.error("Initial world length must equal configured width")
        if np.any(initial < 0) or np.any(initial >= config["states"]):
            parser.error("Initial world contains a state outside the configured state range")
    else:
        initial = create_initial_world(config["initial"], config["width"], config["states"], config["fill"], rng)

    history = evolve(initial, rules, config["neighborhood"], config["generations"])
    save_outputs(args.output_dir, config, rules, initial, history)
    print(json.dumps(json.loads((args.output_dir / "summary.json").read_text(encoding="utf-8")), indent=2))


if __name__ == "__main__":
    main()
