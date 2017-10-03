"""
Tests for Variation class
"""
import itertools

from quiz_generator.input_variation import Variation

def test_sequential_variation_storage():
    """Test that variation is able to be stored in a sequentially accessible manner"""
    items = ["a", "b", "c"]
    variation = Variation(items)
    generated = variation.get()
    assert all(a == b for a, b in itertools.zip_longest(generated, items))

def test_reversed_selection():
    """Test that variation is able to be stored in a sequentially accessible manner"""

    def reversed_selection(items):
        """Yield items from an iterable in reverse order"""
        for item in reversed(items):
            yield item

    items = ["a", "b", "c"]
    variation = Variation(items, selection_method=reversed_selection)
    generated = variation.get()
    expected = ["c", "b", "a"]
    assert all(a == b for a, b in itertools.zip_longest(generated, expected))

