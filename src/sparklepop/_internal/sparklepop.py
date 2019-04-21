def main(in_args):
    import gi
    gi.require_version("Gtk", "3.0")

    from grape_reglib import snapshot
    print(snapshot.current_metadata()["id"])

    from gi.repository import Gtk
    from sparklepop._internal.gui import MainWindow

    main_window = MainWindow()
    main_window.show()
    Gtk.main()
