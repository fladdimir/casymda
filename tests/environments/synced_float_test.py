from casymda.environments.realtime_environment import SyncedFloat

synced_float = SyncedFloat._create_factor_instance(factor=2.0)


def test_right_division_float():
    result = 1.0 / synced_float
    assert result == 0.5


def test_right_division_int():
    result = 1 / synced_float
    assert result == 0.5


def test_left_division_float():
    result = synced_float / 4.0
    assert result == 0.5


def test_left_division_int():
    result = synced_float / 4
    assert result == 0.5


def test_multiplication_left_float():
    result = synced_float * 0.25
    assert result == 0.5


def test_multiplication_right_float():
    result = 0.25 * synced_float
    assert result == 0.5
