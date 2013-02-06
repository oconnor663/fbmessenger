import browser
import settings
import event
import external

def init(desktop):
  # TODO(jacko): Contain the dependency on this Qt object.
  global _desktop
  _desktop = desktop

  base_url = "http://www.facebook.com"
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
  event.subscribe(main_window.RESIZE_EVENT, main_window_moved)
  main_window.show()

  global chat_window
  chat_window = browser.BrowserWindow(base_url + "/desktop/client/chat.php")
  chat_window.set_size(420, 340)

  global toast_window
  toast_window = browser.BrowserWindow(base_url + "/desktop/client/toast.php")
  toast_window.removeframe()

def show_toast():
  width, height = toast_window.get_size()
  margin = 40
  g = _desktop.screenGeometry()
  newx = g.x() + g.width() - width - margin
  newy = g.y() + g.height() - height - margin
  toast_window.set_position(newx, newy)
  toast_window.show()
