"""Property-based tests for core mathematical types."""

from types import MappingProxyType

from hypothesis import given
from hypothesis import strategies as st
from src.math_research.core.types import MathElement, MathSet


# Strategies for generating test data
@st.composite
def math_elements(draw, with_metadata=True):
    """Generate arbitrary MathElement instances."""
    # Use hashable types for values
    value = draw(
        st.one_of(
            st.integers(),
            st.text(),
            st.tuples(
                st.integers(), st.integers()
            ),  # Simple tuples for hashability
            st.frozensets(st.integers(), max_size=3),  # Small frozensets
        )
    )

    if with_metadata and draw(st.booleans()):
        # Generate simple metadata
        metadata_dict = draw(
            st.dictionaries(
                st.text(min_size=1, max_size=10),
                st.one_of(st.integers(), st.text(max_size=20)),
                max_size=3,
            )
        )
        metadata = MappingProxyType(metadata_dict)
    else:
        metadata = MappingProxyType({})

    return MathElement(value=value, metadata=metadata)


@st.composite
def math_sets(draw, with_metadata=True):
    """Generate arbitrary MathSet instances."""
    elements = draw(
        st.frozensets(math_elements(with_metadata=False), max_size=5)
    )

    if with_metadata and draw(st.booleans()):
        metadata_dict = draw(
            st.dictionaries(
                st.text(min_size=1, max_size=10),
                st.one_of(st.integers(), st.text(max_size=20)),
                max_size=3,
            )
        )
        metadata = MappingProxyType(metadata_dict)
    else:
        metadata = MappingProxyType({})

    return MathSet(elements=elements, metadata=metadata)


class TestMathElementProperties:
    """Property-based tests for MathElement."""

    @given(math_elements())
    def test_element_reflexivity(self, element):
        """Test that elements are equal to themselves."""
        assert element == element

    @given(math_elements(), math_elements())
    def test_element_symmetry(self, elem1, elem2):
        """Test that equality is symmetric."""
        if elem1 == elem2:
            assert elem2 == elem1

    @given(math_elements())
    def test_element_hashability_consistency(self, element):
        """Test that equal elements have the same hash."""
        # Create a copy with same data
        copy_element = MathElement(
            value=element.value, metadata=element.metadata
        )
        assert element == copy_element
        assert hash(element) == hash(copy_element)

    @given(math_elements())
    def test_element_immutability_via_operations(self, element):
        """Test that operations don't modify the original element."""
        original_value = element.value
        original_metadata = element.metadata

        # Perform various operations that should not modify the element
        str(element)
        repr(element)
        hash(element)
        assert element == element

        # Element should be unchanged
        assert element.value == original_value
        assert element.metadata == original_metadata

    @given(st.data())
    def test_element_hash_stability(self, data):
        """Test that hash values are stable for the same element."""
        element = data.draw(math_elements())
        hash1 = hash(element)
        hash2 = hash(element)
        assert hash1 == hash2


class TestMathSetProperties:
    """Property-based tests for MathSet mathematical properties."""

    @given(math_sets())
    def test_set_reflexivity(self, mathset):
        """Test that sets are equal to themselves."""
        assert mathset == mathset

    @given(math_sets(), math_sets())
    def test_set_symmetry(self, set1, set2):
        """Test that set equality is symmetric."""
        if set1 == set2:
            assert set2 == set1

    @given(math_sets())
    def test_set_length_consistency(self, mathset):
        """Test that set length is consistent with element count."""
        assert len(mathset) == len(mathset.elements)
        assert len(mathset) == len(list(mathset))

    @given(math_sets())
    def test_set_membership_consistency(self, mathset):
        """Test that membership is consistent with iteration."""
        elements_from_iteration = set(mathset)
        for element in mathset:
            assert element in mathset

        # All elements from iteration should be in the original elements
        assert elements_from_iteration == mathset.elements

    @given(math_sets())
    def test_set_boolean_consistency(self, mathset):
        """Test that boolean evaluation is consistent with length."""
        if len(mathset) == 0:
            assert not mathset
        else:
            assert bool(mathset)

    @given(math_sets())
    def test_set_hashability_consistency(self, mathset):
        """Test that equal sets have the same hash."""
        # Create a copy with same data
        copy_set = MathSet(
            elements=mathset.elements, metadata=mathset.metadata
        )
        assert mathset == copy_set
        assert hash(mathset) == hash(copy_set)

    @given(math_sets())
    def test_set_immutability_via_operations(self, mathset):
        """Test that operations don't modify the original set."""
        original_elements = mathset.elements
        original_metadata = mathset.metadata

        # Perform various operations
        len(mathset)
        bool(mathset)
        str(mathset)
        repr(mathset)
        hash(mathset)
        list(mathset)

        # Set should be unchanged
        assert mathset.elements == original_elements
        assert mathset.metadata == original_metadata

    @given(st.data())
    def test_set_hash_stability(self, data):
        """Test that hash values are stable for the same set."""
        mathset = data.draw(math_sets())
        hash1 = hash(mathset)
        hash2 = hash(mathset)
        assert hash1 == hash2

    @given(math_elements())
    def test_singleton_set_properties(self, element):
        """Test properties of sets with a single element."""
        singleton = MathSet(elements=frozenset([element]))

        assert len(singleton) == 1
        assert bool(singleton)
        assert element in singleton
        assert list(singleton) == [element]

    @given(
        st.frozensets(
            math_elements(with_metadata=False), min_size=1, max_size=10
        )
    )
    def test_set_uniqueness_property(self, elements):
        """Test that sets maintain element uniqueness."""
        mathset = MathSet(elements=elements)

        # The set should have exactly the same elements as the frozenset
        assert mathset.elements == elements
        assert len(mathset) == len(elements)

        # Each element should appear exactly once
        element_list = list(mathset)
        for element in elements:
            assert element_list.count(element) == 1
