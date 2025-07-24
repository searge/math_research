"""Tests for core mathematical types."""

from dataclasses import FrozenInstanceError
from types import MappingProxyType

import pytest
from src.math_research.core.types import MathElement, MathSet


class TestMathElement:
    """Test cases for MathElement."""

    def test_creation_with_value_only(self):
        """Test MathElement creation with just a value."""
        elem = MathElement(value=42)
        assert elem.value == 42
        assert elem.metadata == MappingProxyType({})

    def test_creation_with_metadata(self):
        """Test MathElement creation with metadata."""
        metadata = MappingProxyType(
            {"type": "integer", "source": "user_input"}
        )
        elem = MathElement(value=42, metadata=metadata)
        assert elem.value == 42
        assert elem.metadata == metadata

    def test_immutability(self):
        """Test that MathElement is immutable."""
        elem = MathElement(value=42)
        with pytest.raises(FrozenInstanceError):
            elem.value = 43  # type: ignore

    def test_hashability(self):
        """Test that MathElement is hashable."""
        elem1 = MathElement(value=42)
        elem2 = MathElement(value=42)
        elem3 = MathElement(value=43)

        # Same value should hash the same
        assert hash(elem1) == hash(elem2)
        # Different values should (likely) hash differently
        assert hash(elem1) != hash(elem3)

        # Can be used in sets
        element_set = {elem1, elem2, elem3}
        assert len(element_set) == 2  # elem1 and elem2 are equal

    def test_equality(self):
        """Test MathElement equality."""
        elem1 = MathElement(value=42)
        elem2 = MathElement(value=42)
        elem3 = MathElement(value=43)
        elem4 = MathElement(
            value=42, metadata=MappingProxyType({"note": "test"})
        )

        assert elem1 == elem2
        assert elem1 != elem3
        assert elem1 != elem4  # Different metadata

    def test_string_representations(self):
        """Test string representations."""
        elem1 = MathElement(value=42)
        elem2 = MathElement(
            value="x", metadata=MappingProxyType({"type": "variable"})
        )

        assert str(elem1) == "42"
        assert str(elem2) == "x"

        assert repr(elem1) == "MathElement(value=42)"
        assert "mappingproxy({'type': 'variable'})" in repr(elem2)

    def test_different_value_types(self):
        """Test MathElement with different hashable types."""
        int_elem = MathElement(value=42)
        str_elem = MathElement(value="hello")
        tuple_elem = MathElement(value=(1, 2, 3))

        assert int_elem.value == 42
        assert str_elem.value == "hello"
        assert tuple_elem.value == (1, 2, 3)


class TestMathSet:
    """Test cases for MathSet."""

    def test_empty_set_creation(self):
        """Test creation of empty MathSet."""
        empty_set = MathSet(elements=frozenset())
        assert len(empty_set) == 0
        assert not empty_set
        assert str(empty_set) == "∅"

    def test_set_creation_with_elements(self):
        """Test MathSet creation with elements."""
        elem1 = MathElement(value=1)
        elem2 = MathElement(value=2)
        mathset = MathSet(elements=frozenset([elem1, elem2]))

        assert len(mathset) == 2
        assert bool(mathset)
        assert elem1 in mathset
        assert elem2 in mathset

    def test_set_with_metadata(self):
        """Test MathSet creation with metadata."""
        elem1 = MathElement(value=1)
        metadata = MappingProxyType(
            {"type": "natural_numbers", "finite": True}
        )
        mathset = MathSet(elements=frozenset([elem1]), metadata=metadata)

        assert mathset.metadata == metadata

    def test_immutability(self):
        """Test that MathSet is immutable."""
        elem1 = MathElement(value=1)
        mathset = MathSet(elements=frozenset([elem1]))

        with pytest.raises(FrozenInstanceError):
            mathset.elements = frozenset()  # type: ignore

    def test_iteration(self):
        """Test iteration over MathSet."""
        elem1 = MathElement(value=1)
        elem2 = MathElement(value=2)
        mathset = MathSet(elements=frozenset([elem1, elem2]))

        elements = list(mathset)
        assert len(elements) == 2
        assert elem1 in elements
        assert elem2 in elements

    def test_membership(self):
        """Test membership testing."""
        elem1 = MathElement(value=1)
        elem2 = MathElement(value=2)
        elem3 = MathElement(value=3)
        mathset = MathSet(elements=frozenset([elem1, elem2]))

        assert elem1 in mathset
        assert elem2 in mathset
        assert elem3 not in mathset

    def test_string_representation(self):
        """Test string representations."""
        empty_set = MathSet(elements=frozenset())
        assert str(empty_set) == "∅"

        elem1 = MathElement(value=1)
        elem2 = MathElement(value=2)
        mathset = MathSet(elements=frozenset([elem1, elem2]))

        # Should show elements in consistent order
        str_repr = str(mathset)
        assert "1" in str_repr
        assert "2" in str_repr
        assert str_repr.startswith("{") and str_repr.endswith("}")

    def test_equality(self):
        """Test MathSet equality."""
        elem1 = MathElement(value=1)
        elem2 = MathElement(value=2)

        set1 = MathSet(elements=frozenset([elem1, elem2]))
        set2 = MathSet(elements=frozenset([elem1, elem2]))
        set3 = MathSet(elements=frozenset([elem1]))
        set4 = MathSet(
            elements=frozenset([elem1, elem2]),
            metadata=MappingProxyType({"note": "test"}),
        )

        assert set1 == set2
        assert set1 != set3
        assert set1 != set4  # Different metadata

    def test_hashability(self):
        """Test that MathSet is hashable."""
        elem1 = MathElement(value=1)
        elem2 = MathElement(value=2)

        set1 = MathSet(elements=frozenset([elem1, elem2]))
        set2 = MathSet(elements=frozenset([elem1, elem2]))

        # Should be hashable and equal sets should have same hash
        assert hash(set1) == hash(set2)

        # Can be used in sets
        set_of_sets = {set1, set2}
        assert len(set_of_sets) == 1
