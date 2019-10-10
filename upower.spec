Summary:	Power management service
Summary(pl.UTF-8):	Usługa zarządzania energią
Name:		upower
Version:	0.99.11
Release:	1
License:	GPL v2+
Group:		Libraries
# releases <= 0.99.7
# Source0:	https://upower.freedesktop.org/releases/%{name}-%{version}.tar.xz
# since 0.99.8
#Source0Download: https://gitlab.freedesktop.org/upower/upower/tags
Source0:	https://gitlab.freedesktop.org/upower/upower/uploads/93cfe7c8d66ed486001c4f3f55399b7a/%{name}-%{version}.tar.xz
# Source0-md5:	abe6acb617f11f2e8dbd9846fcf86e24
URL:		https://upower.freedesktop.org/
BuildRequires:	autoconf >= 2.65
BuildRequires:	automake >= 1:1.11
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-tools >= 0.19.8
BuildRequires:	glib2-devel >= 1:2.38.0
BuildRequires:	gobject-introspection-devel >= 0.10.0
BuildRequires:	gtk-doc >= 1.11
BuildRequires:	libimobiledevice-devel >= 0.9.7
BuildRequires:	libplist-devel >= 0.12
BuildRequires:	libtool >= 2:2
BuildRequires:	libusb-devel >= 1.0.0
BuildRequires:	pkgconfig
BuildRequires:	systemd-devel
BuildRequires:	tar >= 1:1.22
BuildRequires:	udev-glib-devel >= 1:147
BuildRequires:	xz
Requires(post,preun,postun):	systemd-units >= 38
Requires:	libimobiledevice >= 0.9.7
Requires:	libplist >= 0.12
Requires:	systemd-units >= 38
Requires:	udev-glib >= 1:147
Obsoletes:	DeviceKit-power < 0.15
Obsoletes:	UPower < 0.9.8-2
Obsoletes:	upower-pm-utils
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
Requires:	glib2 >= 1:2.38.0
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
Requires:	glib2-devel >= 1:2.38.0
Obsoletes:	DeviceKit-power-devel
Obsoletes:	UPower-devel
Obsoletes:	upower-pm-utils-devel

%description devel
Header files for UPower library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki UPower.

%package static
Summary:	Static UPower library
Summary(pl.UTF-8):	Statyczna biblioteka UPower
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Obsoletes:	upower-pm-utils-static

%description static
Static UPower library.

%description static -l pl.UTF-8
Statyczna biblioteka UPower.

%package apidocs
Summary:	UPower API documentation
Summary(pl.UTF-8):	Dokumentacja API UPower
Group:		Documentation
Requires:	gtk-doc-common
Obsoletes:	DeviceKit-power-apidocs
Obsoletes:	UPower-apidocs
Obsoletes:	upower-pm-utils-apidocs
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
UPower API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API UPower.

%prep
%setup -q

%build
%{__gtkdocize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	--enable-deprecated \
	--enable-gtk-doc \
	--with-html-dir=%{_gtkdocdir} \
	--with-systemdsystemunitdir=%{systemdunitdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libupower-glib.la

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
%doc AUTHORS HACKING NEWS README
%attr(755,root,root) %{_bindir}/upower
%attr(755,root,root) %{_libexecdir}/upowerd
%dir %{_sysconfdir}/UPower
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/UPower/UPower.conf
%{_datadir}/dbus-1/system-services/org.freedesktop.UPower.service
%{_datadir}/dbus-1/system.d/org.freedesktop.UPower.conf
%{systemdunitdir}/upower.service
/lib/udev/rules.d/95-upower-csr.rules
/lib/udev/rules.d/95-upower-hid.rules
/lib/udev/rules.d/95-upower-hidpp.rules
/lib/udev/rules.d/95-upower-wup.rules
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
%{_datadir}/dbus-1/interfaces/org.freedesktop.UPower.Wakeups.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.UPower.xml
%{_datadir}/gir-1.0/UPowerGlib-1.0.gir
%{_includedir}/libupower-glib
%{_pkgconfigdir}/upower-glib.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libupower-glib.a

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/UPower
