# Mathematical Theories Research Platform

A functional programming approach to exploring **graph theory**, **information theory**, **game theory**, and **category theory**.

## Features

- **Immutable mathematical structures** using Python dataclasses
- **Pure functions** for mathematical operations
- **Type-safe** implementations with modern Python 3.13+ features
- **NumPy integration** for computational efficiency
- **Extensible architecture** for adding new theories and algorithms

## Quick Start

```bash
# Install dependencies (requires Python 3.13+)
pip install -e .
pip install -e .[dev]

# Run quality checks
ruff check src/
mypy src/
pytest tests/
```

## Project Structure

```bash
src/math_research/
├── core/              # Shared mathematical abstractions
├── graph_theory/      # Graph algorithms and structures
├── information_theory/ # Information-theoretic measures
├── game_theory/       # Game-theoretic analysis
└── category_theory/   # Category theory (Haskell integration)

docs/                  # Architecture and coding guidelines
tests/                 # Test suite
examples/              # Usage examples and notebooks
```

## Example Usage

```python
from math_research.core.types import MathSet
from math_research.core.functions import union
from math_research.graph_theory.structures import Graph
from math_research.graph_theory.algorithms import shortest_path

# Create mathematical sets
vertices = MathSet(elements=frozenset([1, 2, 3, 4]))
edges = frozenset([(1, 2), (2, 3), (3, 4)])

# Build graph structure
graph = Graph(vertices=tuple(vertices.elements), edges=edges)

# Apply algorithms
path = shortest_path(graph, source=1, target=4)
```

## Philosophy

This project follows **functional programming principles** with emphasis on:

- **Immutability**: All mathematical objects are frozen dataclasses
- **Purity**: Operations are side-effect-free functions
- **Composability**: Simple functions combine to create complex analysis
- **Type Safety**: Prevent mathematical errors at compile time

## Documentation

- [`docs/CODING_GUIDELINES.md`](docs/CODING_GUIDELINES.md) - Development standards
- [`docs/architecture.md`](docs/architecture.md) - System design and principles

## Requirements

- **Python 3.13+**
- **NumPy 2.3.1+**
- **SciPy 1.16.0+**

## Development

```bash
# Setup pre-commit hooks
pre-commit install

# Run all checks
ruff check --fix src/
ruff format src/
mypy src/
pytest tests/ -v
```
