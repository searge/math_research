# Claude Development Instructions

## Core Principles

**Focus on single, well-defined changes**. No large code generation - implement one feature/fix at a time following functional programming principles.

## Development Style

### DO ✅

- **One feature per interaction** - implement single functions, dataclasses, or algorithms
- **Pure functions only** - no side effects, predictable inputs/outputs
- **Immutable structures** - always use `@dataclass(frozen=True)`
- **Type everything** - full type annotations with Python 3.13 syntax
- **Test mathematical properties** - property-based tests for correctness
- **NumPy-style docstrings** - complete documentation with examples
- **Small, focused commits** - clear commit messages describing exact change

### DON'T ❌

- **Generate multiple modules at once** - work incrementally
- **Add methods to dataclasses** - operations are separate functions
- **Mix concerns** - keep data structures separate from algorithms
- **Skip type hints** - strict typing prevents mathematical errors
- **Create mutable objects** - everything is immutable
- **Add dependencies without discussion** - prefer standard library + NumPy/SciPy

## Code Structure

### Dataclasses (Data Only)

```python
@dataclass(frozen=True, slots=True, kw_only=True)
class MathObject:
    value: int
    metadata: dict[str, Any] = field(default_factory=dict)
```

### Operations (Pure Functions)

```python
def combine(obj1: MathObject, obj2: MathObject) -> MathObject:
    """Combine two mathematical objects.

    Parameters
    ----------
    obj1 : MathObject
        First object to combine.
    obj2 : MathObject
        Second object to combine.

    Returns
    -------
    MathObject
        New combined object.
    """
    return MathObject(value=obj1.value + obj2.value)
```

## Implementation Workflow

1. **Understand requirement** - ask clarifying questions if needed
2. **Design types first** - what dataclasses are needed?
3. **Implement one component** - single dataclass OR single function
4. **Add comprehensive tests** - property-based for mathematical laws
5. **Document thoroughly** - NumPy-style docstrings with examples
6. **Verify types** - ensure mypy --strict passes

## Mathematical Correctness

- **Validate assumptions** - check mathematical properties hold
- **Handle edge cases** - empty sets, zero probabilities, etc.
- **Use established algorithms** - reference implementations when possible
- **Property-based testing** - test mathematical laws, not just examples

## Response Format

When implementing:

1. **Brief explanation** of what you're adding and why
2. **Single focused change** - one file, one feature
3. **Complete implementation** - types, docstrings, basic tests
4. **Next step suggestion** - what to implement next

## Current Focus

Following `PLANNING.md` roadmap:

- **Phase 1**: Core mathematical abstractions (`core/` module)
- **Sprint 1**: MathElement and MathSet implementation
- **Priority**: Mathematical correctness over performance optimization

## Questions to Ask

- Does this change follow functional principles?
- Are all types immutable and properly annotated?
- Does this feature have clear mathematical meaning?
- Can this be tested with property-based testing?
- Is the scope small and focused?

## Integration Points

- **NumPy**: Use for numerical operations, not basic data structures
- **Testing**: pytest + hypothesis for property-based testing
- **Documentation**: Always include mathematical context and examples
- **Visualization**: Separate concern, never mixed with math objects
