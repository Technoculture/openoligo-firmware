import openoligo.steps as steps


def test_imports():
    assert "FlowWaitPair" in globals()
    assert "FlowWaitPairs" in globals()
    assert isinstance(steps.FlowWaitPair, type)  # replace with the actual type if different
    assert isinstance(steps.FlowWaitPairs, type)  # replace with the actual type if different


def test_all():
    assert set(steps.__all__) == set(["FlowWaitPair", "FlowWaitPairs"])
