%define		pyver	2.3
Summary:	Xen is a virtual machine monitor
Name:		xen
Version:	2
Release:	20041205
Group:		Development/Libraries
License:	GPL
URL:		http://www.sourceforge.net/projects/xen/
Source0:	http://www.cl.cam.ac.uk/Research/SRG/netos/xen/downloads/%{name}-unstable-src.tgz
BuildRequires:	curl-devel
BuildRequires:	python-devel
BuildRequires:	python-Twisted
BuildRequires:	bridge-utils
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%prep
%setup -q -n xen-unstable

%build
CFLAGS="%{rpmcflags}" %{__make} xen tools docs

%install
rm -rf $RPM_BUILD_ROOT
%{__make} prefix=$RPM_BUILD_ROOT \
	install-xen \
	install-tools \
	install-docs

install -d $RPM_BUILD_ROOT%{_mandir}
mv $RPM_BUILD_ROOT%{_prefix}/man/* $RPM_BUILD_ROOT%{_mandir}

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
%{_includedir}/*.h
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h
%{_includedir}/%{name}/*/*.h
%{_libdir}/libxc.so.*
%{_libdir}/libxutil.so.*
%{_libdir}/libxc.so
%{_libdir}/libxutil.so
%{_libdir}/libxutil.a
%dir %{_libdir}/python%{pyver}/site-packages/%{name}
%{_libdir}/python%{pyver}/site-packages/%{name}/*.pyc
%{_libdir}/python%{pyver}/site-packages/%{name}/*.py
%{_libdir}/python%{pyver}/site-packages/%{name}/*/*.pyc
%{_libdir}/python%{pyver}/site-packages/%{name}/*/*.py
%{_libdir}/python%{pyver}/site-packages/%{name}/*/*/*.pyc
%{_libdir}/python%{pyver}/site-packages/%{name}/*/*/*.py
%{_libdir}/python%{pyver}/site-packages/%{name}/lowlevel/*.so
%{_mandir}/man?/*.?.gz
%dir %{_localstatedir}/%{name}
%{_localstatedir}/%{name}/sv/inc/*.css
%{_localstatedir}/%{name}/sv/inc/*.js
%{_localstatedir}/%{name}/sv/images/*.png
%{_localstatedir}/%{name}/sv/images/*.jpg
%{_localstatedir}/%{name}/sv/*.rpy
%{_sysconfdir}/init.d/xend
%{_sysconfdir}/init.d/xendomains
%dir %{_sysconfdir}/%{name}
%{_sysconfdir}/%{name}/scripts/block-enbd
%{_sysconfdir}/%{name}/scripts/block-file
%{_sysconfdir}/%{name}/scripts/network
%{_sysconfdir}/%{name}/scripts/vif-bridge
%{_sysconfdir}/%{name}/xend-config.sxp
%{_sysconfdir}/%{name}/xmexample1
%{_sysconfdir}/%{name}/xmexample2
