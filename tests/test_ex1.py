import pytest

@pytest.fixture
def test_example():
    print('pytest1')
    assert 1 == 1