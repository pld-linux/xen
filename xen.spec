Summary:	Xen - a virtual machine monitor
Summary(pl):	Xen - monitor maszyny wirtualnej
Name:		xen
Version:	2
Release:	20041205
Group:		Development/Libraries
License:	GPL
Source0:	http://www.cl.cam.ac.uk/Research/SRG/netos/xen/downloads/%{name}-unstable-src.tgz
URL:		http://sourceforge.net/projects/xen/
BuildRequires:	curl-devel
BuildRequires:	python-devel
BuildRequires:	python-Twisted
BuildRequires:	bridge-utils
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_localstatedir	/var/lib

%description
This package contains the Xen hypervisor and Xen tools, needed to run
virtual machines on x86 systems, together with the kernel-xen*
packages. Information on how to use Xen can be found at the Xen
project pages.

Virtualisation can be used to run multiple versions or multiple Linux
distributions on one system, or to test untrusted applications in a
sandboxed environment. Note that the Xen technology is still in
development, and this RPM has received extremely little testing. Don't
be surprised if this RPM eats your data, drinks your coffee or makes
fun of you in front of your friends.

%description -l pl
Ten pakiet zawiera nadzorcê oraz narzêdzia Xen, potrzebne do
uruchamiania wirtualnych maszyn w systemach x86, wraz z pakietami
kernel-xen*. Informacje jak u¿ywaæ Xena mo¿na znale¼æ na stronach
projektu.

Wirtualizacja mo¿e byæ u¿ywana do uruchamiania wielu wersji lub wielu
dystrybucji Linuksa na jednym systemie lub do testowaania nie
zaufanych aplikacji w odizolowanym ¶rodowisku. Nale¿y zauwa¿yæ, ¿e
technologia Xen jest ci±gle rozwijana, a ten RPM by³ s³abo testowany.
Nie nale¿y byæ zdziwionym, je¶li ten pakiet zje dane, wypije ca³±
kawê czy bêdzie siê wy¶miewa³ w obecno¶ci przyjació³.

%prep
%setup -q -n xen-unstable

%build
CFLAGS="%{rpmcflags}" \
%{__make} xen tools docs

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install-xen install-tools install-docs \
	prefix=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_mandir}
mv -f $RPM_BUILD_ROOT%{_prefix}/man/* $RPM_BUILD_ROOT%{_mandir}

rm -f $RPM_BUILD_ROOT%{_includedir}/%{name}/COPYING

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING ChangeLog README docs
/boot/%{name}-syms
/boot/%{name}.gz
%attr(755,root,root) %{_sbindir}/netfix
%attr(755,root,root) %{_sbindir}/xend
%attr(755,root,root) %{_sbindir}/xensv
%attr(755,root,root) %{_sbindir}/xfrd
%attr(755,root,root) %{_sbindir}/xm
%attr(755,root,root) %{_sbindir}/xenperf
%attr(755,root,root) %{_bindir}/xenperf
%attr(755,root,root) %{_bindir}/miniterm
%attr(755,root,root) %{_bindir}/xencons
%attr(755,root,root) %{_bindir}/xentrace
%attr(755,root,root) %{_bindir}/xentrace_format
%attr(755,root,root) %{_libdir}/libxc.so.*
%attr(755,root,root) %{_libdir}/libxutil.so.*

# -devel ?
%attr(755,root,root) %{_libdir}/libxc.so
%attr(755,root,root) %{_libdir}/libxutil.so
%{_libdir}/libxutil.a
%{_includedir}/*.h
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h
# XXX: missing dir(s)!
%{_includedir}/%{name}/*/*.h

%dir %{py_sitedir}/%{name}
%{py_sitedir}/%{name}/*.pyc
%{py_sitedir}/%{name}/*.py
# XXX: missing dir(s)!
%{py_sitedir}/%{name}/*/*.pyc
%{py_sitedir}/%{name}/*/*.py
# XXX: missing dir(s)!
%{py_sitedir}/%{name}/*/*/*.pyc
%{py_sitedir}/%{name}/*/*/*.py
%dir %{py_sitedir}/%{name}/lowlevel
%{py_sitedir}/%{name}/lowlevel/*.so
%{_mandir}/man?/*.?*
%dir %{_localstatedir}/%{name}
%dir %{_localstatedir}/%{name}/sv
%dir %{_localstatedir}/%{name}/sv/inc
%{_localstatedir}/%{name}/sv/inc/*.css
%{_localstatedir}/%{name}/sv/inc/*.js
%dir %{_localstatedir}/%{name}/sv/images
%{_localstatedir}/%{name}/sv/images/*.png
%{_localstatedir}/%{name}/sv/images/*.jpg
%{_localstatedir}/%{name}/sv/*.rpy
%attr(754,root,root) /etc/rc.d/init.d/xend
%attr(754,root,root) /etc/rc.d/init.d/xendomains
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/scripts
%{_sysconfdir}/%{name}/scripts/block-enbd
%{_sysconfdir}/%{name}/scripts/block-file
%{_sysconfdir}/%{name}/scripts/network
%{_sysconfdir}/%{name}/scripts/vif-bridge
%{_sysconfdir}/%{name}/xend-config.sxp
%{_sysconfdir}/%{name}/xmexample1
%{_sysconfdir}/%{name}/xmexample2
