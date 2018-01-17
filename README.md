### As of 13 February 2014 this app is deprecated.

This app depends on old Facebook APIs that aren't going to be around
much longer.  Thanks to all the folks who've used it, and especially
everyone who's submitted patches. If a good replacement comes along, I
will link to it here.

Update November 2015: [messenger.com](https://www.messenger.com) works
well for me as a replacement.

# Facebook Messenger for Linux (and Mac!)

![screenshot](https://github.com/oconnor663/fbmessenger/raw/master/resources/screenshot.png)

A PyQt clone of [Facebook Messenger for
Windows](https://web.archive.org/web/20130704182851/https://www.facebook.com/about/messenger).
It gives you a chat sidebar, chat popup windows, and notification toasts
outside of the browser.

If you have all the dependencies, you can launch the app straight from this
repository with `./run.sh`. After you install it, you can launch it with
`fbmessenger`. Ubuntu users can install from a PPA by following [the
instructions
here](http://www.webupd8.org/2013/04/fbmessenger-stand-alone-facebook.html)
(thanks Alin Andrei). Arch users can [install from the
AUR](https://aur.archlinux.org/packages/fbmessenger-git/).  There are packaging
scripts included under `packaging/` for Linux (Debian/Ubuntu in `deb`, Red
Hat/Fedora in `rpm`, and Arch) and OS X (using the Homebrew package manager).
See the `README` files in packaging subdirectories for more specific
instructions. You can also install with `sudo python3 setup.py install`, but
that makes it hard to uninstall, so prefer to use the packaging scripts.

The configuration file is `~/.fbmessenger/config.py`. There are a few settings
that users might want to mess with:

* Set values like `Zoom = 1.2` to make the fonts 20% bigger.
* Set `SystemTray = False` to disable the system tray icon.
* Normally the app will start minimized to the tray if it was minimized last
  time it quit. To force it to always start minimized, set `MinimizedOnStart =
  True`.

#### Dependencies

* Python 3
* PyQt4 for Python 3
* Phonon (optional, for sound on Linux)
* setuptools for Python 3
