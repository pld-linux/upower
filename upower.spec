#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	static_libs	# static library

Summary:	Power management service
Summary(pl.UTF-8):	Usługa zarządzania energią
Name:		upower
Version:	1.90.9
Release:	1
License:	GPL v2+
Group:		Libraries
#Source0Download: https://gitlab.freedesktop.org/upower/upower/-/tags
Source0:	https://gitlab.freedesktop.org/upower/upower/-/archive/v%{version}/%{name}-v%{version}.tar.bz2
# Source0-md5:	22d4f58fb54c225de7e6a7047420bb3f
URL:		https://upower.freedesktop.org/
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-tools >= 0.19.8
BuildRequires:	glib2-devel >= 1:2.66
BuildRequires:	gobject-introspection-devel >= 0.10.0
BuildRequires:	gtk-doc >= 1.11
BuildRequires:	libgudev-devel >= 238
BuildRequires:	libimobiledevice-devel >= 0.9.7
BuildRequires:	libplist-devel >= 2.2.0
BuildRequires:	libxslt-progs
BuildRequires:	meson >= 0.60.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	polkit-devel >= 0.114
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.042
BuildRequires:	sed >= 4.0
BuildRequires:	systemd-devel
Requires(post,preun,postun):	systemd-units >= 38
Requires:	libgudev >= 238
Requires:	libimobiledevice >= 0.9.7
Requires:	libplist >= 2.2.0
Requires:	systemd-units >= 38
Obsoletes:	DeviceKit-power < 015
Obsoletes:	UPower < 0.9.8-2
Obsoletes:	upower-pm-utils < 1:0.99
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
upower provides a daemon, API and command line tools for managing
power devices attached to the system.

%description -l pl.UTF-8
upower dostarcza demona, API i narzędzia linii poleceń do zarządzania
urządzeniami energii dołączonymi do systemu.

%package libs
Summary:	UPower shared library
Summary(pl.UTF-8):	Biblioteka współdzielona UPower
Group:		Libraries
Requires:	glib2 >= 1:2.66
Conflicts:	upower < 0.9.18

%description libs
UPower shared library.

%description libs -l pl.UTF-8
Biblioteka współdzielona UPower.

%package devel
Summary:	Header files for UPower library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki UPower
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2-devel >= 1:2.66
Obsoletes:	DeviceKit-power-devel < 015
Obsoletes:	UPower-devel < 0.9.8-2
Obsoletes:	upower-pm-utils-devel < 1:0.99

%description devel
Header files for UPower library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki UPower.

%package static
Summary:	Static UPower library
Summary(pl.UTF-8):	Statyczna biblioteka UPower
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Obsoletes:	upower-pm-utils-static < 1:0.99

%description static
Static UPower library.

%description static -l pl.UTF-8
Statyczna biblioteka UPower.

%package apidocs
Summary:	UPower API documentation
Summary(pl.UTF-8):	Dokumentacja API UPower
Group:		Documentation
Requires:	gtk-doc-common
Obsoletes:	DeviceKit-power-apidocs < 015
Obsoletes:	UPower-apidocs < 0.9.8-2
Obsoletes:	upower-pm-utils-apidocs < 1:0.99
BuildArch:	noarch

%description apidocs
UPower API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API UPower.

%prep
%setup -q -n %{name}-v%{version}

%if %{with static_libs}
%{__sed} -i -e '/^libupower_glib = / s/shared_library/library/' libupower-glib/meson.build
%endif

%build
%meson \
	%{!?with_apidocs:-Dgtk-doc=false} \
	-Didevice=enabled \
	-Dintrospection=enabled \
	-Dpolkit=enabled \
	-Dsystemdsystemunitdir=%{systemdunitdir} \
	-Dudevrulesdir=/lib/udev/rules.d

%meson_build

%install
rm -rf $RPM_BUILD_ROOT

%meson_install

# tests
%{__rm} $RPM_BUILD_ROOT%{_libexecdir}/upower/{integration-test,output_checker}.py
%{__rm} -r $RPM_BUILD_ROOT%{_libexecdir}/upower/tests
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/installed-tests/upower

%find_lang upower

%clean
rm -rf $RPM_BUILD_ROOT

%post
%systemd_post upower.service

%preun
%systemd_preun upower.service

%postun
%systemd_reload

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f upower.lang
%defattr(644,root,root,755)
%doc AUTHORS COMMITMENT NEWS README.md
%attr(755,root,root) %{_bindir}/upower
%attr(755,root,root) %{_libexecdir}/upowerd
%dir %{_sysconfdir}/UPower
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/UPower/UPower.conf
%{_datadir}/dbus-1/system-services/org.freedesktop.UPower.service
%{_datadir}/dbus-1/system.d/org.freedesktop.UPower.conf
%{_datadir}/polkit-1/actions/org.freedesktop.upower.policy
%{systemdunitdir}/upower.service
/lib/udev/hwdb.d/60-upower-battery.hwdb
/lib/udev/hwdb.d/95-upower-hid.hwdb
/lib/udev/rules.d/60-upower-battery.rules
/lib/udev/rules.d/95-upower-hid.rules
/lib/udev/rules.d/95-upower-wup.rules
%{zsh_compdir}/_upower
%{_mandir}/man1/upower.1*
%{_mandir}/man7/UPower.7*
%{_mandir}/man8/upowerd.8*
%dir /var/lib/upower

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libupower-glib.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libupower-glib.so.3
%{_libdir}/girepository-1.0/UPowerGlib-1.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libupower-glib.so
%{_datadir}/dbus-1/interfaces/org.freedesktop.UPower.Device.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.UPower.KbdBacklight.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.UPower.xml
%{_datadir}/gir-1.0/UPowerGlib-1.0.gir
%{_includedir}/libupower-glib
%{_pkgconfigdir}/upower-glib.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libupower-glib.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/UPower
%endif
