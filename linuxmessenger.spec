%define VERSION %(cat VERSION)

Name:		linuxmessenger
Version:	%VERSION
Release:	1%{?dist}
Summary:	Facebook messenger client
License:	BSD
URL:		http://github.com/oconnor663/linuxmessenger
Source0:	https://github.com/oconnor663/linuxmessenger/archive/master.zip
BuildRequires:	git, python3
Requires:	python3, python3-PyQt4, phonon, python3-sip

%description
Facebook messenger client

%prep
%setup -n linuxmessenger-master

%install
rm -rf $RPM_BUILD_ROOT
python3 setup.py install --root="$RPM_BUILD_ROOT"

%files
/usr/bin/fbmessenger
/usr/lib/python3*/site-packages/fbmessenger-0.1.0-py3*.egg-info
/usr/lib/python3*/site-packages/fbmessengerlib/*
%doc README LICENSE

%changelog
* Wed Apr 17 2013 shuff <shuff@fb.com> - 0.1.0-1
- RPM spec Creation!
