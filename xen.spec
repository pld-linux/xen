#
# TODO:
#  - most of the qemu config options aren't detected (curses, NPTL, vde, fdt)
#
# Conditional build:
%bcond_without	hvm		# build with hvm (full virtualization) support
#
Summary:	Xen - a virtual machine monitor
Summary(pl.UTF-8):	Xen - monitor maszyny wirtualnej
Name:		xen
Version:	4.1.2
Release:	0.1
License:	GPL
Group:		Applications/System
Source0:	http://bits.xensource.com/oss-xen/release/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	73561faf3c1b5e36ec5c089b5db848ad
Source1:	%{name}-xend.init
Source2:	%{name}-xendomains.init
Patch0:		%{name}-python_scripts.patch
Patch1:		%{name}-symbols.patch
Patch2:		%{name}-curses.patch
Patch3:		%{name}-gcc.patch
URL:		http://www.cl.cam.ac.uk/Research/SRG/netos/xen/index.html
BuildRequires:	SDL-devel
%{?with_hvm:BuildRequires:	bcc}
BuildRequires:	curl-devel
BuildRequires:	e2fsprogs-devel
BuildRequires:	gcc >= 5:3.4
BuildRequires:	gettext-devel
BuildRequires:	latex2html
BuildRequires:	libidn-devel
BuildRequires:	ncurses-devel
BuildRequires:	pciutils-devel
BuildRequires:	pkgconfig
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.268
#BuildRequires:	texlive-dvips
#BuildRequires:	texlive-latex-data
BuildRequires:	texlive-latex-psnfss
BuildRequires:	transfig
BuildRequires:	which
BuildRequires:	zlib-devel
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}-libs = %{version}-%{release}
Requires:	ZopeInterface
Requires:	bridge-utils
Requires:	coreutils
Requires:	diffutils
Requires:	gawk
Requires:	iptables
Requires:	kernel(xen0)
Requires:	losetup
Requires:	net-tools
Requires:	python-%{name} = %{version}-%{release}
Requires:	rc-scripts
Requires:	sed
Requires:	util-linux
Requires:	which
Obsoletes:	xen-doc
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# some PPC/SPARC boot image in ELF format
%define         _noautostrip    .*%{_datadir}/xen/qemu/openbios-.*

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

%description -l pl.UTF-8
Ten pakiet zawiera nadzorcę oraz narzędzia Xen, potrzebne do
uruchamiania wirtualnych maszyn w systemach x86, wraz z pakietami
kernel-xen*. Informacje jak używać Xena można znaleźć na stronach
projektu.

Wirtualizacja może być używana do uruchamiania wielu wersji lub wielu
dystrybucji Linuksa na jednym systemie lub do testowania nie zaufanych
aplikacji w odizolowanym środowisku. Należy zauważyć, że technologia
Xen jest ciągle rozwijana, a ten RPM był słabo testowany. Nie należy
być zdziwionym, jeśli ten pakiet zje dane, wypije całą kawę czy będzie
się wyśmiewał w obecności przyjaciół.

%package libs
Summary:	xen libraries
Summary(pl.UTF-8):	Biblioteki xena
Group:		Libraries

%description libs
xen libraries.

%description libs -l pl.UTF-8
Biblioteki xena.

%package devel
Summary:	Header files for xen
Summary(pl.UTF-8):	Pliki nagłówkowe xena
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for xen.

%description devel -l pl.UTF-8
Pliki nagłówkowe xena.

%package static
Summary:	Static xen libraries
Summary(pl.UTF-8):	Statyczne biblioteki xena
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static xen libraries.

%description static -l pl.UTF-8
Statyczne biblioteki xena.

%package udev
Summary:	xen udev scripts
Summary(pl.UTF-8):	Skrypty udev dla xena
Group:		Applications/System

%description udev
xen udev scripts.

%description udev -l pl.UTF-8
Skrypty udev dla xena.

%package xend
Summary:	xend daemon
Summary(pl.UTF-8):	Demon xend
Group:		Daemons

%description xend
xend daemon.

%description xend -l pl.UTF-8
Demon xend.

%package watchdog
Summary:	watchdog daemon
Summary(pl.UTF-8):	Demon watchdog
Group:		Daemons

%description watchdog
watchdog daemon.

%description watchdog -l pl.UTF-8
Demon watchdog.

%package -n python-xen
Summary:	xen Python modules
Summary(pl.UTF-8):	Moduły Pythona dla xena
Group:		Libraries
Conflicts:	xen < 3.2.1-0.3

%description -n python-xen
xen Python modules.

%description -n python-xen -l pl.UTF-8
Moduły Pythona dla xena.

%package -n bash-completion-%{name}
Summary:    bash-completion for xen
Group:      Applications/Shells
Requires:   %{name} = %{version}-%{release}
Requires:   bash-completion

%description -n bash-completion-%{name}
This package provides bash-completion for xen.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
#%%patch3 -p1

rm -f tools/check/*.orig

%build
CFLAGS="%{rpmcflags} -I/usr/include/ncurses" \
CXXFLAGS="%{rpmcflags} -I/usr/include/ncurses" \
%{__make} -j1 xen tools \
	CC="%{__cc}" \
	CXX="%{__cxx}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/xen/examples

%{__make} install-xen install-tools install-docs \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT/etc/xen/{xmexample*,examples}

cp -a tools/blktap/README{,.blktap}
cp -a tools/xenmon/README{,.xenmon}

%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}

%py_postclean

# remove unneeded files
%{__rm} $RPM_BUILD_ROOT/boot/xen-4.1.gz
%{__rm} $RPM_BUILD_ROOT/boot/xen-4.gz
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/xen
%{__rm} $RPM_BUILD_ROOT%{_includedir}/%{name}/COPYING

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add xencommons
/sbin/chkconfig --add xendomains

%preun
if [ "$1" = "0" ]; then
	%service xendomains stop
	/sbin/chkconfig --del xendomains

	%service xencommons stop
	/sbin/chkconfig --del xencommons
fi

%post  xend
/sbin/chkconfig --add xend

%preun xend
if [ "$1" = "0" ]; then
	%service xend stop
	/sbin/chkconfig --del xend
fi

%post  watchdog
/sbin/chkconfig --add xen-watchdog

%preun watchdog
if [ "$1" = "0" ]; then
	%service xen-watchdog stop
	/sbin/chkconfig --del xen-watchdog
fi

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING README* docs/misc/* 
%doc docs/html/*
%doc tools/blktap/README.blktap tools/xenmon/README.xenmon
%doc tools/ioemu-dir/*.html
/boot/%{name}-syms-%{version}
/boot/%{name}-%{version}.gz
/boot/%{name}.gz
%attr(754,root,root) /etc/rc.d/init.d/xencommons
%attr(754,root,root) /etc/rc.d/init.d/xendomains
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/*
%dir %{_sysconfdir}/xen
%dir %{_sysconfdir}/xen/auto
%dir %{_sysconfdir}/xen/examples
%dir %{_sysconfdir}/xen/scripts
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/xen/scripts/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/xen/examples/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/xen/README*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/xen/cpupool
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/xen/xl.conf
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/[bfgikloqtv]*
%attr(755,root,root) %{_sbindir}/xen??*
%attr(755,root,root) %{_sbindir}/xl
%attr(755,root,root) %{_sbindir}/xsview
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/bin
%attr(744,root,root) %{_libdir}/%{name}/bin/*
%if "%{_lib}" != "lib"
%dir %{_prefix}/lib/%{name}
%endif
%dir %{_prefix}/lib/%{name}/boot
%{?with_hvm:%attr(744,root,root) %{_prefix}/lib/%{name}/boot/hvmloader}
%{_datadir}/xen
%{_mandir}/man?/*
%{_sharedstatedir}/xen
%{_sharedstatedir}/xenstored
%dir /var/run/xenstored

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*
%dir %{_libdir}/fs
%dir %{_libdir}/fs/ext2fs-lib
%dir %{_libdir}/fs/fat
%dir %{_libdir}/fs/iso9660
%dir %{_libdir}/fs/reiserfs
%dir %{_libdir}/fs/ufs
%dir %{_libdir}/fs/zfs
%attr(755,root,root) %{_libdir}/fs/*/*.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%files udev
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) /etc/udev/*

%files xend
%defattr(644,root,root,755)
%attr(754,root,root) %{_sysconfdir}/rc.d/init.d/xend
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/xen/xm*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/xen/xend*
%attr(755,root,root) %{_sbindir}/xend
%attr(755,root,root) %{_sbindir}/xm
%dir %attr(700,root,root) /var/run/xend

%files watchdog
%defattr(644,root,root,755)
%attr(754,root,root) %{_sysconfdir}/rc.d/init.d/xen-watchdog
%attr(755,root,root) %{_sbindir}/xenwatchdogd

%files -n python-xen
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/fsimage.so
%{py_sitedir}/grub
%dir %{py_sitedir}/xen
%dir %{py_sitedir}/xen/lowlevel
%{py_sitedir}/xen/lowlevel/*.py*
%attr(755,root,root) %{py_sitedir}/xen/lowlevel/*.so
%{py_sitedir}/xen/remus
%{py_sitedir}/xen/sv
%{py_sitedir}/xen/util
%{py_sitedir}/xen/web
%{py_sitedir}/xen/xend
%{py_sitedir}/xen/xm
%{py_sitedir}/xen/xsview
%{py_sitedir}/xen/*.py*
%if "%{py_ver}" > "2.4"
%{py_sitedir}/*.egg-info
%endif

%files -n bash-completion-%{name}
%defattr(644,root,root,755)
/etc/bash_completion.d/*
