from grapejuice_common import winectrl


def test_wine_ok():
    assert winectrl.wine_ok("wine-5.0", show_dialog=False)
    assert winectrl.wine_ok("wine-5.0-rc5", show_dialog=False)
    assert winectrl.wine_ok("Ubuntu-4.0", show_dialog=False)
    assert winectrl.wine_ok("Ubuntu-4.0-2", show_dialog=False)
    assert winectrl.wine_ok("Debian-4.0", show_dialog=False)
    assert winectrl.wine_ok("Debian-4.0-2", show_dialog=False)


def test_wine_not_ok():
    assert not winectrl.wine_ok("wine-1.0", show_dialog=False)
    assert not winectrl.wine_ok("wine-1.0-rc5", show_dialog=False)
    assert not winectrl.wine_ok("Ubuntu-3.0", show_dialog=False)
    assert not winectrl.wine_ok("Ubuntu-3.0-2", show_dialog=False)
    assert not winectrl.wine_ok("Debian-3.0", show_dialog=False)
    assert not winectrl.wine_ok("Debian-3.0-2", show_dialog=False)
