import application
import browser
import settings
import event
import external

TOAST_WIDTH = 330
# Used for toast and chat window positioning
_margin = 10

# Chat position is not saved when the application closes
_chat_rectangle = None

def init():
  base_url = "https://www.facebook.com"
  base_url_override = settings.get_setting("BaseUrl")
  if (base_url_override):
    print("BaseUrl:", base_url_override)
    base_url = base_url_override

  global main_window
  main_window = browser.BrowserWindow(base_url + "/desktop/client/")
  main_window.set_size(212, 640)
  main_window.set_title("Messenger")
  def main_window_moved():
    external.arbiter_inform_all("FbDesktop.mainWindowMoved", None)
  event.subscribe(main_window.MOVE_EVENT, main_window_moved)
  # js doesn't listen for a separate resize event, so we use move here
  event.subscribe(main_window.RESIZE_EVENT, main_window_moved)
  def main_window_activated():
    external.arbiter_inform_all("FbDesktop.mainWindowActivated", None)
  event.subscribe(main_window.ACTIVATE_EVENT, main_window_activated)
  def main_window_deactivated():
    external.arbiter_inform_all("FbDesktop.mainWindowDeactivated", None)
  event.subscribe(main_window.DEACTIVATE_EVENT, main_window_deactivated)
  def main_window_moved():
    settings.set_setting("MainWindowRectangle", main_window.get_rectangle())
  event.subscribe(main_window.MOVE_EVENT, main_window_moved)
  show_main_window()

  global chat_window
  chat_window = browser.BrowserWindow(base_url + "/desktop/client/chat.php")
  chat_window.set_size(420, 340)
  def chat_window_activated():
    external.arbiter_inform_all("FbdChat.chatWindowActivated", None)
  event.subscribe(chat_window.ACTIVATE_EVENT, chat_window_activated)
  def chat_window_moved():
    global _chat_rectangle
    _chat_rectangle = chat_window.get_rectangle()
  event.subscribe(chat_window.MOVE_EVENT, chat_window_moved)

  global toast_window
  toast_window = browser.BrowserWindow(base_url + "/desktop/client/toast.php")
  toast_window.style_toast()
  # height of one toast -- this will be overridden but just in case
  toast_window.set_size(TOAST_WIDTH, 72)

def show_main_window():
  saved_rectangle = settings.get_setting("MainWindowRectangle")
  if saved_rectangle:
    main_window.set_rectangle(*_fit_rectangle_to_desktop(*saved_rectangle))
  main_window.show()

def show_chat_window(bringtofront):
  if _chat_rectangle:
    rect = _chat_rectangle
  else:
    desk_x, desk_y, desk_width, desk_height = application.get_desktop_rectangle()
    main_x, main_y, main_width, main_height = main_window.get_rectangle()
    chat_x, chat_y, chat_width, chat_height = chat_window.get_rectangle()
    default_x = main_x - chat_width - _margin
    if default_x < desk_x:
      default_x = main_x + main_width + _margin
    default_y = main_y + main_height - chat_height
    rect = (default_x, default_y, chat_width, chat_height)
  fittedrect = _fit_rectangle_to_desktop(*rect)
  chat_window.set_rectangle(*fittedrect)
  chat_window.show(bringtofront)

def _position_toast():
  x, y, width, height = toast_window.get_rectangle()
  dx, dy, dwidth, dheight = application.get_desktop_rectangle()
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

def _fit_rectangle_to_desktop(x, y, width, height):
  dx, dy, dwidth, dheight = application.get_desktop_rectangle()
  return (x, y, min(width, dwidth), min(height, dheight))
