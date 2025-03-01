import pytest
from datastructures.array import Array

class TestArray:
    
    @pytest.fixture
    def empty_array(self) -> Array[int]:
        """Fixture to provide a fresh empty Array instance for each test."""
        return Array()

    @pytest.fixture
    def filled_array(self) -> Array[int]:
        """Fixture to provide an Array instance with pre-filled values."""
        array = Array([1, 2, 3, 4])
        return array

    def test_len(self, filled_array: Array[int]):
        """Test the length of the array."""
        assert len(filled_array) == 4

    def test_get_item(self, filled_array: Array[int]):
        """Test retrieving values from the array."""
        assert filled_array[0] == 1
        assert filled_array[1] == 2
        assert filled_array[2] == 3
        assert filled_array[3] == 4

    def test_set_item(self, filled_array: Array[int]):
        """Test setting values in the array."""
        filled_array[2] = 99
        assert filled_array[2] == 99

    def test_get_invalid_index_raises_error(self, filled_array: Array[int]):
        """Test accessing an invalid index raises IndexError."""
        with pytest.raises(IndexError):
            filled_array[10]

    def test_set_invalid_index_raises_error(self, filled_array: Array[int]):
        """Test setting an invalid index raises IndexError."""
        with pytest.raises(IndexError):
            filled_array[10] = 5

    def test_append_item(self, empty_array: Array[int]):
        """Test appending items to the array."""
        empty_array.append(5)
        empty_array.append(10)
        assert empty_array[0] == 5
        assert empty_array[1] == 10

    def test_pop_item(self, filled_array: Array[int]):
        """Test popping items from the array."""
        filled_array.pop()
        assert len(filled_array) == 3
        assert filled_array[2] == 3

    def test_pop_front(self, filled_array: Array[int]):
        """Test popping from the front of the array."""
        filled_array.pop_front()
        assert len(filled_array) == 3
        assert filled_array[0] == 2

    def test_clear_array(self, filled_array: Array[int]):
        """Test clearing the array."""
        filled_array.clear()
        assert len(filled_array) == 0
