from . import application
from . import browser
from . import settings
from . import event
from PyQt4 import QtCore, QtGui

TOAST_WIDTH = 330
# Used for toast and chat window positioning
_margin = 10

def init():
    base_url = "https://www.facebook.com"
    base_url_override = settings.get_setting("BaseUrl")
    if (base_url_override):
        print("BaseUrl:", base_url_override)
        base_url = base_url_override

    global main_window
    closable_main = not settings.get_setting("SystemTray", default=False)
    main_window = browser.BrowserWindow(base_url + "/desktop/client/", closable_main)
    main_window.set_size(212, 640)
    main_window.set_title("Messenger")
    def main_window_moved_or_resized():
        settings.set_setting(
            "MainWindowRectangle", main_window.get_rectangle())
    event.subscribe(main_window.MOVE_EVENT, main_window_moved_or_resized)
    event.subscribe(main_window.RESIZE_EVENT, main_window_moved_or_resized)
    event.subscribe(main_window.HIDE_EVENT, show_or_hide_main_window)
    event.subscribe(main_window.CLOSE_EVENT, application.quit)
    init_main_window()

    global chat_window
    chat_window = browser.BrowserWindow(base_url + "/desktop/client/chat.php", False)
    chat_window.set_size(420, 340)
    def chat_window_moved_or_resized():
        settings.set_setting(
            "ChatWindowRectangle", chat_window.get_rectangle())
    event.subscribe(chat_window.MOVE_EVENT, chat_window_moved_or_resized)
    event.subscribe(chat_window.RESIZE_EVENT, chat_window_moved_or_resized)
    event.subscribe(chat_window.HIDE_EVENT, show_or_hide_chat_window)

    global toast_window
    toast_window = browser.BrowserWindow(
        base_url + "/desktop/client/toast.php", True)
    toast_window.style_toast()
    # height of one toast -- this will be overridden but just in case
    toast_window.set_size(TOAST_WIDTH, 72)
    event.subscribe(settings.AUTH_CHANGED_EVENT, toast_window.hide)

    # check if system tray should be enabled
    if settings.get_setting("SystemTray", default=False):
        create_sys_tray()

def create_sys_tray():
    global sysTray
    sysIcon = QtGui.QIcon(application.resource_path("fbmessenger.png"))
    sysTray = QtGui.QSystemTrayIcon(sysIcon, application.get_qt_application())
    sysTray.activated.connect(on_sys_tray_activated)

    sysTrayMenu = QtGui.QMenu()

    global showHide
    showHide = sysTrayMenu.addAction("Hide")
    showHide.triggered.connect(on_sys_show_hide_activated)
    quit = sysTrayMenu.addAction("Quit")
    quit.triggered.connect(application.quit)
    sysTray.setContextMenu(sysTrayMenu)
    sysTray.setVisible(True)

def on_sys_tray_activated(reason):
    if reason == QtGui.QSystemTrayIcon.Trigger or reason == QtGui.QSystemTrayIcon.DoubleClick:
        show_or_hide_main_window()

def on_sys_show_hide_activated():
    show_or_hide_main_window()

def show_or_hide_chat_window():
    if chat_window.is_visible():
        chat_window.hide()
    else:
        chat_window.show()

def show_or_hide_main_window():
    if main_window.is_visible():
        main_window.hide()
        showHide.setText("Show")
    else:
        main_window.show()
        showHide.setText("Hide")

# The main window's position is saved whenever it is moved or resized, so we
# restore it when the window is created.
def init_main_window():
    saved_rectangle = settings.get_setting("MainWindowRectangle")
    if saved_rectangle:
        main_window.set_rectangle(*saved_rectangle)
    main_window.fit_to_desktop()

    tray = settings.get_setting("SystemTray", default=False)
    minimized = settings.get_setting("MinimizedOnStart", default=False) 
    
    if not tray or not minimized:
        main_window.show()

# The chat window is initially shown adjacent to the main window, bottom
# aligned on the left (or right if not enough space). If moved or resized, the
# position is remembered while the app is still running.
def show_chat_window():
    saved_rectangle = settings.get_setting("ChatWindowRectangle")
    if saved_rectangle:
        rect = saved_rectangle
    else:
        desk_x, desk_y, desk_width, desk_height = \
            main_window.get_desktop_rectangle()
        main_x, main_y, main_width, main_height = main_window.get_rectangle()
        chat_x, chat_y, chat_width, chat_height = chat_window.get_rectangle()
        default_x = main_x - chat_width - _margin
        if default_x < desk_x:
            default_x = main_x + main_width + _margin
        default_y = main_y + main_height - chat_height
        rect = (default_x, default_y, chat_width, chat_height)
    chat_window.set_rectangle(*rect)
    chat_window.fit_to_desktop()
    chat_window.show()

# The toast shows in the bottom right of the screen.
def _position_toast():
    x, y, width, height = toast_window.get_rectangle()
    dx, dy, dwidth, dheight = main_window.get_desktop_rectangle()
    newx = dx + dwidth - width - _margin
    newy = dy + dheight - height - _margin
    toast_window.set_position(newx, newy)

# Our JS has an interesting bug where it reports the wrong value to
# setToastHeight. For some reason the layout isn't finished for several more
# milliseconds, and the height grows. This hack has us actually reaching into
# the toast and pulling out the height of a single div, several times to make
# sure it stabilizes. God help us.
def _terrible_toast_height_hack():
    def inner_hack():
        height = toast_window.evaluate_js(
                'document.getElementById("toast-frame").offsetHeight')
        if height:
            toast_window.set_size(TOAST_WIDTH, height)
            _position_toast()
        else:
            print("Failed to hack out the toast height.")
    for delay_ms in (0, 10, 100, 1000):
        event.run_on_main_thread(inner_hack, delay_ms=delay_ms)

def show_toast():
    _position_toast()
    toast_window.show()
    _terrible_toast_height_hack()
