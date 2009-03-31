Summary:	Power management service
Summary(pl.UTF-8):	Usługa zarządzania energią
Name:		DeviceKit-power
Version:	007
Release:	1
License:	GPL v2+
Group:		Libraries
Source0:	http://hal.freedesktop.org/releases/%{name}-%{version}.tar.gz
# Source0-md5:	4b1159374f36e23fe7d920f934076269
BuildRequires:	DeviceKit-devel >= 003
BuildRequires:	PolicyKit-devel >= 0.8
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake
BuildRequires:	dbus-glib-devel >= 0.76
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.18.0
BuildRequires:	gtk-doc >= 1.3
BuildRequires:	intltool >= 0.40.0
BuildRequires:	libtool
BuildRequires:	libusb-compat-devel
BuildRequires:	pkgconfig
Requires:	DeviceKit >= 003
Requires:	pm-utils
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
DeviceKit-power provides a daemon, API and command line tools for
managing power devices attached to the system.

%description -l pl.UTF-8
DeviceKit-power dostarcza demona, API i narzędzia linii poleceń do
zarządzania urządzeniami energii dołączonymi do systemu.

%package apidocs
Summary:	DeviceKit-power API documentation
Summary(pl.UTF-8):	Dokumentacja API DeviceKit-power
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
DeviceKit-power API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API DeviceKit-power.

%package devel
Summary:	Header files for DeviceKit-power library
Summary(pl.UTF-8):	Nagłówki biblioteki DeviceKit-power
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.12.0

%description devel
Header files for DeviceKit library.

%description devel -l pl.UTF-8
Nagłówki biblioteki DeviceKit-power.

%prep
%setup -q

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-gtk-doc \
	--with-html-dir=%{_gtkdocdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog HACKING NEWS README
%attr(755,root,root) %{_bindir}/devkit-power
%attr(755,root,root) %{_libdir}/devkit-power-daemon
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dbus-1/system.d/org.freedesktop.DeviceKit.Power.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/udev/rules.d/95-devkit-power-csr.rules
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/udev/rules.d/95-devkit-power-hid.rules
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/udev/rules.d/95-devkit-power-wup.rules
%{_datadir}/PolicyKit/policy/org.freedesktop.devicekit.power.policy
%{_datadir}/PolicyKit/policy/org.freedesktop.devicekit.power.qos.policy
%{_datadir}/dbus-1/interfaces/org.freedesktop.DeviceKit.Power.Device.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.DeviceKit.Power.QoS.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.DeviceKit.Power.Wakeups.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.DeviceKit.Power.xml
%{_datadir}/dbus-1/system-services/org.freedesktop.DeviceKit.Power.service
%attr(755,root,root) %{_libdir}/libdevkit-power-gobject.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdevkit-power-gobject.so.1
%{_mandir}/man1/devkit-power.1*
%{_mandir}/man7/DeviceKit-power.7*
%{_mandir}/man8/devkit-power-daemon.8*

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/devkit-power

%files devel
%defattr(644,root,root,755)
%{_includedir}/DeviceKit-power
%attr(755,root,root) %{_libdir}/libdevkit-power-gobject.so
%{_libdir}/libdevkit-power-gobject.la
%{_pkgconfigdir}/devkit-power-gobject.pc
