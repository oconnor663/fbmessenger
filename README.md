##Facebook Messenger for Linux (and Mac!)
![screenshot](https://github.com/oconnor663/fbmessenger/raw/master/resources/screenshot.png)

A PyQt clone of [Facebook Messenger for
Windows](https://www.facebook.com/about/messenger). It gives you a chat
sidebar, chat popup windows, and notification toasts outside of the browser.

If you have all the dependencies, you can launch the app straight from this
repository with `./run.sh`. After you install it, you can launch it with
`fbmessenger`. There are packaging scripts included under `packaging/` for
Linux (deb, rpm, arch) and Mac (brew). See the `README` files in there for
installation instructions. You can also install with `python3 setup.py
install`. Ubuntu users can install from a PPA by following [the instructions
here](http://www.webupd8.org/2013/04/fbmessenger-stand-alone-facebook.html)
(thanks Alin Andrei). Arch users can [install from the
AUR](https://aur.archlinux.org/packages/fbmessenger-git/).

The configuration file is `~/.fbmessenger/settings.json`. Right now the only
setting that users might want to mess with is `"Zoom"`; set a value like `1.2`
to make the fonts 20% bigger.

####Dependencies
* Python 3
* PyQt4 for Python 3
* Phonon (optional, for sound on Linux)
* setuptools for Python 3
