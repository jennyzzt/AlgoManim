from manimlib.mobject.mobject import Mobject

def test_mobject_tostring():
    obj = Mobject()
    assert str(obj) == "Mobject"

    obj = Mobject(name="dummy")
    assert str(obj) == "dummy"
