import sys


def main(in_args):
    import gi
    gi.require_version("Gtk", "3.0")

    from gi.repository import Gtk
    from sparklepop.gui import MainWindow

    main_window = MainWindow()
    main_window.show()
    Gtk.main()


if __name__ == "__main__":
    main(sys.argv)
