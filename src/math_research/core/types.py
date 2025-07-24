"""Core mathematical types and abstractions."""

from __future__ import annotations

from collections.abc import Hashable, Iterator
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any


@dataclass(frozen=True, slots=True, kw_only=True)
class MathElement:
    """Basic wrapper for any hashable mathematical value.

    MathElement provides a uniform interface for mathematical objects,
    ensuring immutability and hashability while preserving the underlying
    value's mathematical meaning.

    Parameters
    ----------
    value : Hashable
        The underlying mathematical value (int, str, tuple, etc.).
    metadata : dict[str, Any], optional
        Additional information about the element, by default empty dict.

    Examples
    --------
    >>> elem1 = MathElement(value=42)
    >>> elem2 = MathElement(value="x", metadata={"type": "variable"})
    >>> elem3 = MathElement(value=(1, 2, 3), metadata={"dimension": 3})

    Notes
    -----
    MathElement is immutable and hashable, making it suitable for use
    in sets, as dictionary keys, and in other mathematical structures
    that require stable identity.
    """

    value: Hashable
    metadata: MappingProxyType[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def __str__(self) -> str:
        """Return string representation of the element's value."""
        return str(self.value)

    def __repr__(self) -> str:
        """Return detailed string representation."""
        if self.metadata:
            return (
                f"MathElement(value={self.value!r}, "
                f"metadata={self.metadata!r})"
            )
        return f"MathElement(value={self.value!r})"

    def __hash__(self) -> int:
        """Return hash of the element."""
        # Hash the value and the sorted items of metadata for consistency
        metadata_items = tuple(sorted(self.metadata.items()))
        return hash((self.value, metadata_items))


@dataclass(frozen=True, slots=True, kw_only=True)
class MathSet:
    """Immutable mathematical set with optional metadata.

    MathSet provides a type-safe, immutable wrapper around frozenset,
    ensuring mathematical set semantics while supporting metadata
    for additional mathematical context.

    Parameters
    ----------
    elements : frozenset[MathElement]
        The elements contained in this set.
    metadata : dict[str, Any], optional
        Additional information about the set, by default empty dict.

    Examples
    --------
    >>> elem1 = MathElement(value=1)
    >>> elem2 = MathElement(value=2)
    >>> mathset = MathSet(elements=frozenset([elem1, elem2]))
    >>> len(mathset)
    2
    >>> elem1 in mathset
    True

    Notes
    -----
    MathSet maintains mathematical set properties: uniqueness of elements,
    unordered collection, and immutability. All operations return new
    MathSet instances rather than modifying existing ones.
    """

    elements: frozenset[MathElement]
    metadata: MappingProxyType[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def __contains__(self, element: MathElement) -> bool:
        """Check if element is in the set."""
        return element in self.elements

    def __len__(self) -> int:
        """Return the number of elements in the set."""
        return len(self.elements)

    def __iter__(self) -> Iterator[MathElement]:
        """Iterate over elements in the set."""
        return iter(self.elements)

    def __bool__(self) -> bool:
        """Return True if set is non-empty."""
        return bool(self.elements)

    def __str__(self) -> str:
        """Return string representation of the set."""
        if not self.elements:
            return "∅"
        elements_str = ", ".join(
            str(elem)
            for elem in sorted(self.elements, key=lambda x: str(x.value))
        )
        return f"{{{elements_str}}}"

    def __repr__(self) -> str:
        """Return detailed string representation."""
        if self.metadata:
            return (
                f"MathSet(elements={self.elements!r}, "
                f"metadata={self.metadata!r})"
            )
        return f"MathSet(elements={self.elements!r})"

    def __hash__(self) -> int:
        """Return hash of the set."""
        # Hash the elements and the sorted items of metadata for consistency
        metadata_items = tuple(sorted(self.metadata.items()))
        return hash((self.elements, metadata_items))
