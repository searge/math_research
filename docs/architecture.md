# System Architecture

## Vision & Goals

Build a research platform for exploring mathematical theories (graphs, information, games, categories) with emphasis on:

- **Mathematical Correctness**: Type safety prevents invalid operations
- **Experimentation**: Pure functions enable safe composition and testing
- **Extensibility**: New theories integrate seamlessly through shared abstractions
- **Performance**: NumPy integration for computational efficiency

## Constraints & Assumptions

- **Language Choice**: Python for broad ecosystem, Haskell for category theory
- **Target Users**: Mathematical researchers, not production systems
- **Data Scale**: Medium datasets (GB range), not big data
- **Deployment**: Local development, Jupyter notebooks, research scripts

## Architecture Principles

### Functional-First Design

- **Data & Behavior Separation**: Dataclasses hold data, functions perform operations
- **Immutability**: All structures are frozen, operations return new instances
- **Pure Functions**: No side effects, predictable testing and composition
- **Type Safety**: Compile-time prevention of mathematical errors

### Layered Architecture

| Layer              | Description                                   |
| ------------------ | --------------------------------------------- |
| Applications Layer | Jupyter notebooks, research scripts           |
| Theory Modules     | graph_theory, information_theory, game_theory |
| Core Abstractions  | Shared mathematical primitives                |
| Foundation Layer   | NumPy, SciPy, native Python types             |

## System Overview

### Core Module (`core/`)

**Purpose**: Shared mathematical abstractions used by all theories

**Key Components**:

- `types.py`: Fundamental dataclasses (MathSet, MathFunction, MathStructure)
- `functions.py`: Operations on core types (union, composition, morphisms)
- `protocols.py`: Type protocols for mathematical operations

**Design Rationale**: Mathematical theories share common concepts (sets, functions, relations). Core module prevents duplication and ensures consistent behavior.

### Theory Modules

Each theory module follows identical structure:

- `structures.py`: Theory-specific dataclasses extending core types
- `algorithms.py`: Pure functions implementing theory algorithms
- `examples.py`: Usage demonstrations and common patterns

**Interaction Pattern**: Theory modules depend on core, never on each other directly. Cross-theory connections happen through core abstractions.

### Visualization Layer (`visualization/`)

**Purpose**: Convert mathematical structures to visual representations

**Approach**: Functions that take mathematical objects and return plot objects, not methods on mathematical objects themselves.

## Module Dependencies

```txt
graph_theory ────────┐
information_theory ──┼──→ core ──→ numpy/scipy
game_theory ─────────┘                 └──→ typing protocols
category_theory ─────┘

visualization ────────→ matplotlib/plotly
```

**Dependency Rules**:

- Theory modules may only import from `core`
- `core` only imports standard library and NumPy/SciPy
- No circular dependencies between theory modules
- Visualization is separate concern, not mixed with math

## Data Flow Patterns

### Construction Pattern

```python
# 1. Create primitive structures
vertices = MathSet(elements=frozenset([...]))
edges = MathSet(elements=frozenset([...]))

# 2. Compose into complex structures
graph = Graph(vertices=vertices, edges=edges)

# 3. Apply operations
result = shortest_path(graph, source, target)
```

### Transformation Pattern

```python
# Mathematical objects flow through pure functions
graph → adjacency_matrix → eigenvalues → centrality_scores
```

### Analysis Pattern

```python
# Combine multiple views of same mathematical object
prob_dist → entropy
          → mutual_information
          → kullback_leibler
```

## Key Design Decisions

### ADR-001: Dataclasses Over Classes

**Decision**: Use `@dataclass(frozen=True)` for all mathematical objects

**Rationale**:

- Immutability prevents accidental modification
- Clear separation between data and operations
- Better performance with `slots=True`
- Matches mathematical intuition (objects don't change, we create new ones)

### ADR-002: Functions Over Methods

**Decision**: Mathematical operations as module-level functions, not class methods

**Rationale**:

- Easier testing and composition
- Follows mathematical convention (f(x), not x.f())
- Enables multiple dispatch patterns
- Reduces coupling between data and algorithms

### ADR-003: NumPy Integration Strategy

**Decision**: Optional NumPy arrays cached in dataclasses, accessed via properties

**Rationale**:

- Best of both worlds: mathematical abstraction + computational efficiency
- Lazy evaluation avoids unnecessary conversions
- Type system can still reason about abstract mathematical objects

### ADR-004: Type Protocol Approach

**Decision**: Use Protocol types for mathematical operations rather than inheritance

**Rationale**:

- Structural typing matches mathematical thinking
- No rigid inheritance hierarchies
- Easy to add new types that support existing operations
- Better IDE support and type checking

## Evolution Strategy

### Phase 1: Python Foundation

Establish core abstractions and first theory modules using functional approach with dataclasses and pure functions.

### Phase 2: Haskell Integration

When moving to category theory, leverage Haskell's advanced type system:

**Functors**: Mathematical functors naturally map to Haskell functors

```haskell
-- Category theory functor becomes Haskell Functor
instance Functor (Graph v) where
  fmap f graph = graph { vertices = fmap f (vertices graph) }
```

**Monads**: Computational contexts (probability, non-determinism, error handling)

```haskell
-- Probability monad for game theory
newtype Probability a = Probability (Distribution a)

instance Monad Probability where
  return x = Probability (pure x)
  Probability d >>= f = Probability (d >>= runProbability . f)
```

### Phase 3: Cross-Language Bridge

JSON serialization layer enabling Python-computed structures to be consumed by Haskell for category-theoretic analysis.

## Quality Attributes

### Maintainability

- Clear module boundaries prevent cascading changes
- Pure functions are easy to understand and modify
- Type annotations serve as documentation

### Testability

- Pure functions have predictable inputs/outputs
- Immutable structures prevent test pollution
- Property-based testing validates mathematical properties

### Performance

- NumPy integration for heavy computation
- Lazy evaluation of expensive properties
- Immutability enables safe parallelization

### Extensibility

- New theories integrate through core abstractions
- Protocol-based typing allows new implementations
- Functional approach enables easy algorithm composition

## Anti-Patterns to Avoid

- **God Objects**: Keep mathematical structures focused and composable
- **Mutable State**: All mathematical objects remain immutable
- **Method Chaining**: Prefer explicit function composition
- **Inheritance Hierarchies**: Use protocols and composition instead
- **Mixed Concerns**: Separate mathematical logic from visualization/IO

## Success Metrics

- **Type Coverage**: >95% with mypy strict mode
- **Module Coupling**: No circular dependencies between theory modules
- **API Consistency**: All theories follow same patterns (structures.py + algorithms.py)
- **Mathematical Correctness**: Property-based tests validate theoretical properties
- **Research Velocity**: New algorithms can be implemented and tested quickly
