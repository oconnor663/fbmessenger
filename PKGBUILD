# Maintainer: Jack O'Connor <oconnor663@gmail.com>
pkgname=fbmessenger-git
pkgver=0
pkgver() {
  cd linuxmessenger
  echo $(git rev-list --count master).$(git rev-parse --short master)
}
pkgrel=1
pkgdesc="Facebook messenger client"
arch=('any')
url="https://github.com/oconnor663/linuxmessenger"
depends=('pyqt' 'phonon')
makedepends=('git' 'python-distribute')
source=('git://github.com/oconnor663/linuxmessenger.git')
license=('BSD')
md5sums=('SKIP')

package(){
  cd "$srcdir/linuxmessenger"
  python setup.py install --root="$pkgdir"
}
