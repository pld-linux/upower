Summary:	Power management service
Summary(pl.UTF-8):	Usługa zarządzania energią
Name:		upower
Version:	0.9.13
Release:	1
License:	GPL v2+
Group:		Libraries
Source0:	http://upower.freedesktop.org/releases/%{name}-%{version}.tar.xz
# Source0-md5:	26d2dc53fc632c1f62234cc21715c3e1
URL:		http://upower.freedesktop.org/
BuildRequires:	autoconf >= 2.65
BuildRequires:	automake >= 1:1.11
BuildRequires:	dbus-devel >= 1.0.0
BuildRequires:	dbus-glib-devel >= 0.76
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.22.0
BuildRequires:	gobject-introspection-devel >= 0.10.0
BuildRequires:	gtk-doc >= 1.11
BuildRequires:	intltool >= 0.40.0
BuildRequires:	libimobiledevice-devel >= 0.9.7
BuildRequires:	libtool
BuildRequires:	libusb-devel
BuildRequires:	pkgconfig
BuildRequires:	polkit-devel >= 0.97
BuildRequires:	tar >= 1:1.22
BuildRequires:	udev-glib-devel >= 147
BuildRequires:	xz
Requires:	pm-utils
Requires:	polkit >= 0.97
Obsoletes:	DeviceKit-power < 0.15
Obsoletes:	UPower < 0.9.8-2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
upower provides a daemon, API and command line tools for managing
power devices attached to the system.

%description -l pl.UTF-8
upower dostarcza demona, API i narzędzia linii poleceń do zarządzania
urządzeniami energii dołączonymi do systemu.

%package apidocs
Summary:	UPower API documentation
Summary(pl.UTF-8):	Dokumentacja API UPower
Group:		Documentation
Requires:	gtk-doc-common
Obsoletes:	DeviceKit-power-apidocs
Obsoletes:	UPower-apidocs

%description apidocs
UPower API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API UPower.

%package devel
Summary:	Header files for UPower library
Summary(pl.UTF-8):	Nagłówki biblioteki UPower
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	dbus-devel >= 1.0.0
Requires:	glib2-devel >= 1:2.22.0
Obsoletes:	DeviceKit-power-devel
Obsoletes:	UPower-devel

%description devel
Header files for UPower library.

%description devel -l pl.UTF-8
Nagłówki biblioteki UPower.

%prep
%setup -q

%build
%{__gtkdocize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	--disable-static \
	--enable-gtk-doc \
	--with-html-dir=%{_gtkdocdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang upower

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f upower.lang
%defattr(644,root,root,755)
%doc AUTHORS HACKING NEWS README
%attr(755,root,root) %{_bindir}/upower
%attr(755,root,root) %{_libdir}/upowerd
%attr(755,root,root) %{_libdir}/libupower-glib.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libupower-glib.so.1
%{_libdir}/girepository-1.0/UPowerGlib-1.0.typelib
%config(noreplace) %verify(not md5 mtime size) /etc/dbus-1/system.d/org.freedesktop.UPower.conf
%dir %{_sysconfdir}/UPower
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/UPower/UPower.conf
%{_datadir}/dbus-1/system-services/org.freedesktop.UPower.service
%{_datadir}/polkit-1/actions/org.freedesktop.upower.policy
%{_datadir}/polkit-1/actions/org.freedesktop.upower.qos.policy
/lib/udev/rules.d/95-upower-battery-recall-dell.rules
/lib/udev/rules.d/95-upower-battery-recall-fujitsu.rules
/lib/udev/rules.d/95-upower-battery-recall-gateway.rules
/lib/udev/rules.d/95-upower-battery-recall-ibm.rules
/lib/udev/rules.d/95-upower-battery-recall-lenovo.rules
/lib/udev/rules.d/95-upower-battery-recall-toshiba.rules
/lib/udev/rules.d/95-upower-csr.rules
/lib/udev/rules.d/95-upower-hid.rules
/lib/udev/rules.d/95-upower-wup.rules
%{_mandir}/man1/upower.1*
%{_mandir}/man7/UPower.7*
%{_mandir}/man8/upowerd.8*
%dir /var/lib/upower

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/UPower

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libupower-glib.so
%{_libdir}/libupower-glib.la
%{_datadir}/dbus-1/interfaces/org.freedesktop.UPower.Device.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.UPower.KbdBacklight.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.UPower.QoS.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.UPower.Wakeups.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.UPower.xml
%{_datadir}/gir-1.0/UPowerGlib-1.0.gir
%{_includedir}/libupower-glib
%{_pkgconfigdir}/upower-glib.pc
