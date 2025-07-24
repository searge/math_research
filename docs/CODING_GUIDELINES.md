# Coding Guidelines

## Philosophy

**Functional-first approach with minimal OOP**. Dataclasses as data containers (like Go structs), pure functions for operations, immutable structures for mathematical correctness.

## Python Guidelines

### Core Toolchain

```toml
# pyproject.toml - current versions as of Dec 2024
[project]
requires-python = ">=3.13"
dependencies = ["numpy>=2.3.1", "scipy>=1.16.0"]

[dependency-groups]
dev = ["mypy>=1.17.0", "ruff>=0.12.5", "pytest>=8.3.0"]

[tool.ruff]
target-version = "py313"
line-length = 88
src = ["src", "tests"]

[tool.ruff.lint]
select = ["E", "W", "F", "I", "N", "D", "UP", "S", "B", "A", "C4", "SIM", "RUF"]
ignore = ["D203", "D213"]  # Prefer D212 over D213

[tool.ruff.lint.pydocstyle]
convention = "numpy"

[tool.mypy]
python_version = "3.13"
strict = true
```

### Data Structures (Go-style)

#### Dataclasses as pure data containers

```python
from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True, slots=True, kw_only=True)
class MathSet:
    """Mathematical set - pure data container."""
    elements: frozenset[Any]
    name: str | None = None

@dataclass(frozen=True, slots=True, kw_only=True)
class Graph:
    """Graph structure."""
    vertices: tuple[int, ...]
    edges: tuple[tuple[int, int], ...]

@dataclass(frozen=True, slots=True, kw_only=True)
class ProbabilityDistribution:
    """Probability distribution."""
    probabilities: np.ndarray
    sample_space: tuple[Any, ...]
```

#### Pure functions for operations

```python
# Operations as separate functions, not methods
def union(set_a: MathSet, set_b: MathSet) -> MathSet:
    """Union of two mathematical sets."""
    return MathSet(
        elements=set_a.elements | set_b.elements,
        name=f"({set_a.name} ∪ {set_b.name})" if all([set_a.name, set_b.name]) else None
    )

def entropy(dist: ProbabilityDistribution) -> float:
    """Shannon entropy of probability distribution."""
    probs = dist.probabilities[dist.probabilities > 0]
    return -np.sum(probs * np.log2(probs))
```

### Type Annotations

#### Modern Python 3.13 patterns

```python
# Generic types with defaults (PEP 696)
from typing import Generic, TypeVar

T = TypeVar('T', default=float)

@dataclass(frozen=True)
class Matrix[T = float]:
    data: np.ndarray

# Union types with | operator
def process_data(input_data: np.ndarray | list[float]) -> np.ndarray:
    return np.asarray(input_data)

# Protocols for mathematical operations
from typing import Protocol

class SupportsMatMul[T](Protocol):
    def __matmul__(self, other: T) -> T: ...

def matrix_multiply[T: SupportsMatMul[T]](a: T, b: T) -> T:
    return a @ b
```

### Documentation (NumPy Style)

#### Function documentation template

```python
def interpolate(x: np.ndarray, y: np.ndarray, xi: np.ndarray) -> np.ndarray:
    """Interpolate data points.

    Parameters
    ----------
    x : ndarray
        Known x-coordinates, shape (n,).
    y : ndarray
        Known y-coordinates, shape (n,).
    xi : ndarray
        Target x-coordinates for interpolation, shape (m,).

    Returns
    -------
    ndarray
        Interpolated values, shape (m,).

    Examples
    --------
    >>> x = np.array([0, 1, 2])
    >>> y = np.array([0, 1, 4])
    >>> interpolate(x, y, np.array([0.5]))
    array([0.5])
    """
```

**References**: [NumPy docstring standard](https://numpydoc.readthedocs.io/en/latest/format.html)

### Python Project Structure

```bash
src/
├── math_research/
│   ├── core/
│   │   ├── types.py          # Core dataclasses
│   │   ├── functions.py      # Pure mathematical functions
│   │   └── protocols.py      # Type protocols
│   ├── graph_theory/
│   │   ├── structures.py     # Graph dataclasses
│   │   └── algorithms.py     # Graph algorithms
│   ├── information_theory/
│   ├── game_theory/
│   └── category_theory/
tests/
docs/
```

## Haskell Guidelines

### Haskell Project Structure

```bash
src/
├── MathProject/
│   ├── Core/
│   │   ├── Types.hs         -- Core mathematical types
│   │   └── Functions.hs     -- Pure mathematical functions
│   ├── GraphTheory/
│   └── CategoryTheory/
app/
test/
math-project.cabal
```

### Functional Patterns

#### Algebraic Data Types

```haskell
-- Pure data types
data MathSet a = MathSet
  { elements :: Set a
  , name :: Maybe String
  } deriving (Eq, Show)

data Graph = Graph
  { vertices :: [Int]
  , edges :: [(Int, Int)]
  } deriving (Eq, Show)

-- Pure functions
union :: Ord a => MathSet a -> MathSet a -> MathSet a
union (MathSet s1 n1) (MathSet s2 n2) =
  MathSet (Set.union s1 s2) (combineName n1 n2)
```

#### Modern Extensions

```haskell
{-# LANGUAGE StrictData #-}           -- Strict by default
{-# LANGUAGE OverloadedRecordDot #-}   -- Record dot syntax
{-# LANGUAGE GHC2024 #-}              -- Modern language set
```

#### References

- [GHC User Guide](https://ghc.gitlab.haskell.org/ghc/doc/users_guide/),
- [Haskell Style Guide](https://kowainik.github.io/posts/2019-02-06-style-guide)

## Quality Assurance

### Development Workflow

```bash
# Python
ruff check --fix src/
ruff format src/
mypy src/
pytest tests/

# Haskell
hlint src/
cabal build --enable-tests
cabal test
```

### Pre-commit Configuration

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.12.5
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.17.0
    hooks:
      - id: mypy
```

**References**: [Ruff Documentation](https://docs.astral.sh/ruff/), [MyPy Documentation](https://mypy.readthedocs.io/)

## Key Principles

1. **Immutability**: All dataclasses `frozen=True`, pure functions only
2. **Separation**: Data structures separate from operations
3. **Type Safety**: Strict typing, protocols for mathematical operations
4. **Testability**: Pure functions easy to test and reason about
5. **Performance**: Use NumPy for numerical operations, strict evaluation in Haskell

## Quality Metrics

- **Type Coverage**: >95% (mypy --strict)
- **Linting**: 100% Ruff compliance
- **Documentation**: All public functions documented
- **Testing**: Property-based tests for mathematical correctness

**References**: [Python Developer's Guide](https://devguide.python.org/), [Effective Haskell](https://github.com/guidebooks/haskell-style-guide)
