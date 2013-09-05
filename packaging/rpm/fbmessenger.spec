%define VERSION %(cat ../VERSION)

Name:		fbmessenger
Version:	%VERSION
Release:	1%{?dist}
Summary:	Facebook messenger client
License:	BSD
URL:		http://github.com/oconnor663/fbmessenger
Source0:	https://github.com/oconnor663/fbmessenger/archive/master.zip
BuildRequires:	git, python3, python3-setuptools
Requires:	python3, python3-PyQt4, phonon, python3-sip

%description
Facebook messenger client

%prep
%setup -n fbmessenger-master

%install
rm -rf $RPM_BUILD_ROOT
python3 setup.py install --root="$RPM_BUILD_ROOT"

%files
/usr/bin/fbmessenger
/usr/lib/python3*/site-packages/fbmessenger-%VERSION-py3*.egg-info
/usr/lib/python3*/site-packages/fbmessenger/*
/usr/share/applications/fbmessenger.desktop
/usr/share/pixmaps/fbmessenger.png
%doc README.md LICENSE

%changelog
* Thu Sep 05 2013 jacko <oconnor663@gmail.com> - 0.2.0-1
- Directory move and path changes
* Wed Apr 17 2013 shuff <shuff@fb.com> - 0.1.0-1
- RPM spec Creation!
