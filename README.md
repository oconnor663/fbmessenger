##Facebook Messenger for Linux

![screenshot](https://github.com/oconnor663/linuxmessenger/raw/master/screenshot.png)

A Linux clone of [Facebook Messenger for
Windows](https://www.facebook.com/about/messenger). It gives you a chat
sidebar, chat popup windows, and notification toasts outside of the browser.

You can launch the app with `./fbmessenger`. There are packaging scripts
included: `build-debian.sh`, `build-rpm.sh`, and `PKGBUILD` for Arch. Ubuntu
users can install from a PPA by following [the instructions
here](http://www.webupd8.org/2013/04/fbmessenger-stand-alone-facebook.html)
(thanks Alin Andrei). Arch users can [install from the
AUR](https://aur.archlinux.org/packages/fbmessenger-git/).

The configuration file is `~/.fbmessenger/settings.json`. Right now the only
setting that users might want to mess with is `"Zoom"`; set a value like `1.2`
to make the fonts 20% bigger.

####Dependencies
* Python 3
* PyQt4 for Python 3
* Phonon (part of Qt4 but often packaged separately)
* setuptools for Python 3
