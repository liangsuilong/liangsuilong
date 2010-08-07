%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

Name:			ailurus
Version:		10.07.8
Release:		1%{?dist}
Summary:		A simple application installer and GNOME tweaker
Group:			Applications/System
License:		GPLv2+
URL:			http://ailurus.googlecode.com/
Source:		http://ailurus.googlecode.com/files/%{name}-%{version}.tar.gz
BuildRequires:	python2-devel python-distutils-extra intltool
BuildRequires:	desktop-file-utils
BuildArch:		noarch
# The automatic dependency consists of python and rpmlib only. It is insufficient.
Requires:		polkit pygtk2 notify-python vte rpm-python pygobject2 dbus-python wget unzip gnome-python2-gnomekeyring

%description
Ailurus is a simple application installer and GNOME tweaker.

Features:
* Help users learn some Linux skills
* Install some nice applications
* Display basic hardware information
* Clean YUM cache
* Backup and recover YUM status
* Change GNOME settings 

%prep
%setup -q -n %{name}-%{version}

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

%install
%{__python} setup.py install -O1 --root=$RPM_BUILD_ROOT
desktop-file-install \
	--delete-original \
	--dir ${RPM_BUILD_ROOT}%{_datadir}/applications \
	${RPM_BUILD_ROOT}%{_datadir}/applications/%{name}.desktop
%find_lang %{name} --with-gnome
rm -f $RPM_BUILD_ROOT%{_datadir}/PolicyKit/policy/cn.ailurus.policy


%clean
rm -rf $RPM_BUILD_ROOT

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{name}.lang
%defattr(-,root,root,-)
%{_bindir}/ailurus
%{_datadir}/applications/ailurus.desktop
%{_datadir}/ailurus/
%{_datadir}/icons/hicolor/*/apps/ailurus.png
%{_datadir}/dbus-1/system-services/cn.ailurus.service
%{_datadir}/polkit-1/actions/cn.ailurus.policy
%{_mandir}/man1/ailurus.1*
%{_sysconfdir}/dbus-1/system.d/cn.ailurus.conf
%{python_sitelib}/ailurus/
%{python_sitelib}/ailurus*.egg-info

%changelog
* Sat Jul 31 2010 Liang Suilong <liangsuilong@gmail.com> 10.07.8-1
- Upstream to 10.07.8

* Wed Jul 28 2010 Liang Suilong <liangsuilong@gmail.com> 10.07.7-1
- Upstream to 10.07.7

* Wed Jul 28 2010 Liang Suilong <liangsuilong@gmail.com> 10.07.6-2
- Fix the bug of spec

* Tue Jul 27 2010 Liang Suilong <liangsuilong@gmail.com> 10.07.6-1
- Upstream to 10.07.6

* Fri Jul 23 2010 Liang Suilong <liangsuilong@gmail.com> 10.07.4-1
- Upstream to 10.07.4

* Mon Jul 12 2010 Homer Xing <homer.xing@gmail.com> 10.06.93-0
- Initial package

