import application
import browser
import settings
import event
import external

def init():
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
  # js doesn't listen for a separate resize event, so we use move here
  event.subscribe(main_window.RESIZE_EVENT, main_window_moved)
  def main_window_activated():
    external.arbiter_inform_all("FbDesktop.mainWindowActivated", None)
  event.subscribe(main_window.ACTIVATED_EVENT, main_window_activated)
  def main_window_deactivated():
    external.arbiter_inform_all("FbDesktop.mainWindowDeactivated", None)
  event.subscribe(main_window.DEACTIVATED_EVENT, main_window_deactivated)
  main_window.show()

  global chat_window
  chat_window = browser.BrowserWindow(base_url + "/desktop/client/chat.php")
  chat_window.set_size(420, 340)
  def chat_window_activated():
    external.arbiter_inform_all("FbDesktop.chatWindowActivated", None)
  event.subscribe(chat_window.ACTIVATED_EVENT, chat_window_activated)

  global toast_window
  toast_window = browser.BrowserWindow(base_url + "/desktop/client/toast.php")
  toast_window.remove_frame()

def show_toast():
  width, height = toast_window.get_size()
  margin = 10
  dx, dy, dwidth, dheight = application.get_desktop_geometry()
  newx = dx + dwidth - width - margin
  newy = dy + dheight - height - margin
  toast_window.set_position(newx, newy)
  toast_window.show()
