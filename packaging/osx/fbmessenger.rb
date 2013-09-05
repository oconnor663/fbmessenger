require 'formula'

class Fbmessenger < Formula
  homepage 'https://github.com/oconnor663/fbmessenger'
  url 'https://github.com/oconnor663/fbmessenger/archive/master.zip'
  version '0.2.0'

  # The build won't work without the brew version of python2
  depends_on "python"

  depends_on :python3

  # sip should be pulled in as a dependency of pyqt, but naming it explicitly
  # seems to prevent build failures
  depends_on 'sip' => 'with-python3'
  depends_on 'pyqt' => 'with-python3'

  def install
    system python3, "setup.py", "install", "--prefix=#{prefix}", "--single-version-externally-managed", "--record=installed.txt"
  end
end
