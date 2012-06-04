#
# TODO:
#  - most of the qemu config options aren't detected (curses, NPTL, vde, fdt)
#
#
# Conditional build:
%bcond_without	ocaml		# build Ocaml libraries for Xen tools
#
%define	xen_extfiles_url	http://xenbits.xensource.com/xen-extfiles
Summary:	Xen - a virtual machine monitor
Summary(pl.UTF-8):	Xen - monitor maszyny wirtualnej
Name:		xen
Version:	4.1.2
Release:	4
License:	GPL v2, interface parts on BSD-like
Group:		Applications/System
Source0:	http://bits.xensource.com/oss-xen/release/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	73561faf3c1b5e36ec5c089b5db848ad
# used by stubdoms
Source10:	%{xen_extfiles_url}/lwip-1.3.0.tar.gz
# Source10-md5:	36cc57650cffda9a0269493be2a169bb
Source11:	%{xen_extfiles_url}/newlib-1.16.0.tar.gz
# Source11-md5:	bf8f1f9e3ca83d732c00a79a6ef29bc4
Source12:	%{xen_extfiles_url}/zlib-1.2.3.tar.gz
# Source12-md5:	debc62758716a169df9f62e6ab2bc634
Source13:	%{xen_extfiles_url}/pciutils-2.2.9.tar.bz2
# Source13-md5:	cec05e7785497c5e19da2f114b934ffd
Source14:	%{xen_extfiles_url}/grub-0.97.tar.gz
# Source14-md5:	cd3f3eb54446be6003156158d51f4884
Source15:	%{xen_extfiles_url}/ipxe-git-v1.0.0.tar.gz
# Source15-md5:	fb7df96781d337899066d82059346885
Source30:	proc-xen.mount
Source31:	var-lib-xenstored.mount
Source32:	blktapctrl.service
Source33:	blktapctrl.sysconfig
Source34:	xenconsoled.service
Source35:	xenconsoled.sysconfig
Source36:	xenstored.service
Source37:	xenstored.sysconfig
Source38:	xenstored.tmpfiles
Source39:	xend.service
Source40:	xend.tmpfiles
Source41:	xen-watchdog.service
Source42:	xen-dom0-modules-load.conf
# sysvinit scripts
Source50:	xend.init
Source51:	xenconsoled.init
Source52:	xenstored.init
Source53:	xen-watchdog.init
Source54:	xendomains.init
Source55:	xen.logrotate
Patch0:		%{name}-python_scripts.patch
Patch1:		%{name}-symbols.patch
Patch2:		%{name}-curses.patch
Patch3:		%{name}-xz.patch
Patch4:		pygrubfix.patch
Patch5:		pygrubfix2.patch
Patch6:		qemu-xen-4.1-testing.git-3cf61880403b4e484539596a95937cc066243388.patch
Patch7:		xen-4.1-testing.23190.patch
Patch8:		xend.catchbt.patch
Patch9:		xend.empty.xml.patch
Patch10:	xend-pci-loop.patch
Patch11:	xen-dumpdir.patch
Patch12:	xen-net-disable-iptables-on-bridge.patch
Patch13:	xen-configure-xend.patch
Patch14:	xen-initscript.patch
# stubdom patch
Patch100:	grub-ext4-support.patch
URL:		http://www.cl.cam.ac.uk/Research/SRG/netos/xen/index.html
BuildRequires:	OpenGL-devel
BuildRequires:	SDL-devel
BuildRequires:	acpica
BuildRequires:	bcc
BuildRequires:	bluez-libs-devel
BuildRequires:	brlapi-devel
BuildRequires:	curl-devel
BuildRequires:	e2fsprogs-devel
BuildRequires:	gcc >= 5:3.4
BuildRequires:	gettext-devel
BuildRequires:	gnutls-devel
BuildRequires:	latex2html
BuildRequires:	libidn-devel
BuildRequires:	ncurses-devel
%if %{with ocaml}
BuildRequires:	ocaml >= 3.04-7
BuildRequires:	ocaml-findlib
%endif
BuildRequires:	pciutils-devel
BuildRequires:	pkgconfig
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.647
#BuildRequires:	texlive-dvips
#BuildRequires:	texlive-latex-data
BuildRequires:	texlive-latex-psnfss
BuildRequires:	transfig
BuildRequires:	which
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	zlib-devel
Requires(post,preun):	/sbin/chkconfig
Requires(post,preun,postun):	systemd-units >= 38
Requires:	%{name}-libs = %{version}-%{release}
Requires:	ZopeInterface
Requires:	bridge-utils
Requires:	coreutils
Requires:	diffutils
Requires:	gawk
Requires:	iptables
Requires:	losetup
Requires:	net-tools
Requires:	python-%{name} = %{version}-%{release}
Requires:	rc-scripts
Requires:	sed
Requires:	systemd-units >= 38
Requires:	util-linux
Requires:	which
Obsoletes:	xen-doc
Obsoletes:	xen-udev
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
Summary:	Xen libraries
Summary(pl.UTF-8):	Biblioteki Xena
Group:		Libraries

%description libs
Xen libraries.

%description libs -l pl.UTF-8
Biblioteki Xena.

%package devel
Summary:	Header files for Xen
Summary(pl.UTF-8):	Pliki nagłówkowe Xena
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for Xen.

%description devel -l pl.UTF-8
Pliki nagłówkowe Xena.

%package static
Summary:	Static Xen libraries
Summary(pl.UTF-8):	Statyczne biblioteki Xena
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Xen libraries.

%description static -l pl.UTF-8
Statyczne biblioteki Xena.

%package xend
Summary:	xend daemon
Summary(pl.UTF-8):	Demon xend
Group:		Daemons
Requires(post,preun,postun):	systemd-units >= 38
Requires:	systemd-units >= 38

%description xend
xend daemon.

%description xend -l pl.UTF-8
Demon xend.

%package -n ocaml-xen
Summary:	OCaml bindings for Xen
Summary(pl.UTF-8):	Wiązania OCamla dla Xena
License:	LGPL v2.1 with linking exception
Group:		Libraries
Requires:	%{name}-libs = %{version}-%{release}
%requires_eq	ocaml-runtime

%description -n ocaml-xen
OCaml bindings for Xen.

%description -n ocaml-xen -l pl.UTF-8
Wiązania OCamla dla Xena.

%package -n ocaml-xen-devel
Summary:	OCaml bindings for Xen - development files
Summary(pl.UTF-8):	Wiązania OCamla dla Xena - pliki programistyczne
License:	LGPL v2.1 with linking exception
Group:		Development/Libraries
Requires:	ocaml-xen = %{version}-%{release}
%requires_eq	ocaml

%description -n ocaml-xen-devel
OCaml bindings for Xen - development files.

%description -n ocaml-xen-devel -l pl.UTF-8
Wiązania OCamla dla Xena - pliki programistyczne.

%package -n python-xen
Summary:	Xen Python modules
Summary(pl.UTF-8):	Moduły Pythona dla Xena
Group:		Libraries
Requires:	%{name}-libs = %{version}-%{release}
Conflicts:	xen < 3.2.1-0.3

%description -n python-xen
Xen Python modules.

%description -n python-xen -l pl.UTF-8
Moduły Pythona dla Xena.

%package -n bash-completion-%{name}
Summary:    bash-completion for Xen (xl)
Summary(pl.UTF-8):	Bashowe dopełnianie poleceń dla Xena (xl)
Group:      Applications/Shells
Requires:   %{name} = %{version}-%{release}
Requires:   bash-completion

%description -n bash-completion-%{name}
This package provides bash-completion for Xen (xl).

%description -n bash-completion-%{name} -l pl.UTF-8
Ten pakiet zapewnia bashowe dopełnianie poleceń dla Xena (xl).

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1

%{__rm} -v tools/check/*.orig

# stubdom sources
ln -s %{SOURCE10} %{SOURCE11} %{SOURCE12} %{SOURCE13} %{SOURCE14} stubdom
ln -s %{PATCH100} stubdom/grub.patches/99grub-ext4-support.patch
ln -s %{SOURCE15} tools/firmware/etherboot/ipxe.tar.gz

%build
export CFLAGS="%{rpmcflags} -I/usr/include/ncurses"
export CXXFLAGS="%{rpmcflags} -I/usr/include/ncurses"

%{__make} dist-xen dist-tools dist-docs \
	%{!?with_ocaml:OCAML_TOOLS=n} \
	prefix=%{_prefix} \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	V=1

unset CFLAGS
unset CXXFLAGS
%{__make} -j1 dist-stubdom \
	%{!?with_ocaml:OCAML_TOOLS=n} \
	CC="%{__cc}" \
	CXX="%{__cxx}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{xen/examples,modules-load.d,logrotate.d} \
	$RPM_BUILD_ROOT{/usr/lib/tmpfiles.d,%{systemdunitdir},/var/log/xen/console}

%{__make} -j1 install-xen install-tools install-stubdom install-docs \
	%{!?with_ocaml:OCAML_TOOLS=n} \
	prefix=%{_prefix} \
	DESTDIR=$RPM_BUILD_ROOT \
	HOTPLUGS=install-udev

%if "%{_lib}" == "lib64"
ln -s %{_prefix}/lib/%{name}/bin/qemu-dm $RPM_BUILD_ROOT%{_libdir}/%{name}/bin/qemu-dm
%endif

install %{SOURCE30} $RPM_BUILD_ROOT%{systemdunitdir}/proc-xen.mount
install %{SOURCE31} $RPM_BUILD_ROOT%{systemdunitdir}/var-lib-xenstored.mount
install %{SOURCE32} $RPM_BUILD_ROOT%{systemdunitdir}/blktapctrl.service
install %{SOURCE33} $RPM_BUILD_ROOT/etc/sysconfig/blktapctrl
install %{SOURCE34} $RPM_BUILD_ROOT%{systemdunitdir}/xenconsoled.service
install %{SOURCE35} $RPM_BUILD_ROOT/etc/sysconfig/xenconsoled
install %{SOURCE36} $RPM_BUILD_ROOT%{systemdunitdir}/xenstored.service
install %{SOURCE37} $RPM_BUILD_ROOT/etc/sysconfig/xenstored
install %{SOURCE38} $RPM_BUILD_ROOT/usr/lib/tmpfiles.d/xenstored.conf
install %{SOURCE39} $RPM_BUILD_ROOT%{systemdunitdir}/xend.service
install %{SOURCE40} $RPM_BUILD_ROOT/usr/lib/tmpfiles.d/xend.conf
install %{SOURCE41} $RPM_BUILD_ROOT%{systemdunitdir}/xen-watchdog.service
install %{SOURCE42} $RPM_BUILD_ROOT/etc/modules-load.d/xen-dom0.conf
# sysvinit scripts
%{__rm} $RPM_BUILD_ROOT/etc/rc.d/init.d/*
install %{SOURCE50} $RPM_BUILD_ROOT/etc/rc.d/init.d/xend
install %{SOURCE51} $RPM_BUILD_ROOT/etc/rc.d/init.d/xenconsoled
install %{SOURCE52} $RPM_BUILD_ROOT/etc/rc.d/init.d/xenstored
install %{SOURCE53} $RPM_BUILD_ROOT/etc/rc.d/init.d/xen-watchdog
install %{SOURCE54} $RPM_BUILD_ROOT/etc/rc.d/init.d/xendomains
install %{SOURCE55} $RPM_BUILD_ROOT/etc/logrotate.d/xen

mv $RPM_BUILD_ROOT/etc/xen/{xmexample*,examples}

cp -p tools/blktap/README{,.blktap}
cp -p tools/xenmon/README{,.xenmon}

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
/sbin/chkconfig --add xen-watchdog
/sbin/chkconfig --add xenconsoled
/sbin/chkconfig --add xenstored
/sbin/chkconfig --add xendomains
%systemd_post xen-watchdog.service xenconsoled.service xenstored.service

%preun
if [ "$1" = "0" ]; then
	%service xendomains stop
	/sbin/chkconfig --del xendomains

	%service xenconsoled stop
	/sbin/chkconfig --del xenconsoled

	%service xenstored stop
	/sbin/chkconfig --del xenstored

	%service xen-watchdog stop
	/sbin/chkconfig --del xen-watchdog
fi
%systemd_preun xen-watchdog.service xenconsoled.service xenstored.service

%postun
%systemd_reload

%post xend
/sbin/chkconfig --add xend
%systemd_post xend.service

%preun xend
if [ "$1" = "0" ]; then
	%service xend stop
	/sbin/chkconfig --del xend
fi
%systemd_preun xend.service

%postun xend
%systemd_reload

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
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/xenconsoled
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/xenstored
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/xendomains
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/xen
%attr(754,root,root) /etc/rc.d/init.d/xen-watchdog
%attr(754,root,root) /etc/rc.d/init.d/xenconsoled
%attr(754,root,root) /etc/rc.d/init.d/xenstored
%attr(754,root,root) /etc/rc.d/init.d/xendomains
%config(noreplace) %verify(not md5 mtime size) /etc/modules-load.d/xen-dom0.conf
%{systemdunitdir}/proc-xen.mount
%{systemdunitdir}/var-lib-xenstored.mount
%{systemdunitdir}/xen-watchdog.service
%{systemdunitdir}/xenconsoled.service
%{systemdunitdir}/xenstored.service
%dir %{_sysconfdir}/xen
%dir %{_sysconfdir}/xen/auto
%dir %{_sysconfdir}/xen/examples
%dir %{_sysconfdir}/xen/scripts
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/xen/scripts/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/xen/examples/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/xen/README*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/xen/cpupool
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/xen/xl.conf
%config(noreplace) %verify(not md5 mtime size) /etc/udev/rules.d/xen-backend.rules
%attr(755,root,root) %{_bindir}/pygrub
%attr(755,root,root) %{_bindir}/qemu-img-xen
%attr(755,root,root) %{_bindir}/qemu-nbd-xen
%attr(755,root,root) %{_bindir}/remus
%attr(755,root,root) %{_bindir}/xen-detect
%attr(755,root,root) %{_bindir}/xencons
%attr(755,root,root) %{_bindir}/xenstore*
%attr(755,root,root) %{_bindir}/xentrace*
%attr(755,root,root) %{_sbindir}/blktapctrl
%attr(755,root,root) %{_sbindir}/flask-*
%attr(755,root,root) %{_sbindir}/gdbsx
%attr(755,root,root) %{_sbindir}/gtrace*
%attr(755,root,root) %{_sbindir}/img2qcow
%attr(755,root,root) %{_sbindir}/kdd
%attr(755,root,root) %{_sbindir}/lock-util
%attr(755,root,root) %{_sbindir}/qcow-create
%attr(755,root,root) %{_sbindir}/qcow2raw
%attr(755,root,root) %{_sbindir}/tap-ctl
%attr(755,root,root) %{_sbindir}/tapdisk*
%attr(755,root,root) %{_sbindir}/td-util
%attr(755,root,root) %{_sbindir}/vhd-*
%attr(755,root,root) %{_sbindir}/xen-*
%attr(755,root,root) %{_sbindir}/xenbaked
%attr(755,root,root) %{_sbindir}/xenconsoled
%attr(755,root,root) %{_sbindir}/xenlockprof
%attr(755,root,root) %{_sbindir}/xenmon.py
%attr(755,root,root) %{_sbindir}/xenpaging
%attr(755,root,root) %{_sbindir}/xenperf
%attr(755,root,root) %{_sbindir}/xenpm
%attr(755,root,root) %{_sbindir}/xenpmd
%attr(755,root,root) %{_sbindir}/xenstored
%attr(755,root,root) %{_sbindir}/xentop
%attr(755,root,root) %{_sbindir}/xentrace_setmask
%attr(755,root,root) %{_sbindir}/xenwatchdogd
%attr(755,root,root) %{_sbindir}/xl
%attr(755,root,root) %{_sbindir}/xsview
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/bin
%attr(744,root,root) %{_libdir}/%{name}/bin/*
%if "%{_lib}" != "lib"
%dir %{_prefix}/lib/%{name}
%dir %{_prefix}/lib/%{name}/bin
%attr(755,root,root) %{_prefix}/lib/%{name}/bin/qemu-dm
%attr(755,root,root) %{_prefix}/lib/%{name}/bin/stubdom-dm
%attr(755,root,root) %{_prefix}/lib/%{name}/bin/stubdompath.sh
%endif
%dir %{_prefix}/lib/%{name}/boot
%{_prefix}/lib/%{name}/boot/ioemu-stubdom.gz
%{_prefix}/lib/%{name}/boot/pv-grub-x86_32.gz
%ifarch %{x8664}
%{_prefix}/lib/%{name}/boot/pv-grub-x86_64.gz
%endif
%attr(744,root,root) %{_prefix}/lib/%{name}/boot/hvmloader
%{_datadir}/xen
%{_mandir}/man1/xentop.1*
%{_mandir}/man1/xentrace_format.1*
%{_mandir}/man1/xm.1*
%{_mandir}/man5/xend-config.sxp.5*
%{_mandir}/man5/xmdomain.cfg.5*
%{_mandir}/man8/xentrace.8*
%{_sharedstatedir}/xen
%{_sharedstatedir}/xenstored
%dir /var/run/xenstored
%{systemdtmpfilesdir}/xenstored.conf
%dir %attr(0700,root,root) /var/log/xen
%dir %attr(0700,root,root) /var/log/xen/console

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libblktap.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libblktap.so.3.0
%attr(755,root,root) %{_libdir}/libblktapctl.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libblktapctl.so.1.0
%attr(755,root,root) %{_libdir}/libflask.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libflask.so.1.0
%attr(755,root,root) %{_libdir}/libfsimage.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfsimage.so.1.0
%attr(755,root,root) %{_libdir}/libvhd.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libvhd.so.1.0
%attr(755,root,root) %{_libdir}/libxenctrl.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libxenctrl.so.4.0
%attr(755,root,root) %{_libdir}/libxenguest.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libxenguest.so.4.0
%attr(755,root,root) %{_libdir}/libxenlight.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libxenlight.so.1.0
%attr(755,root,root) %{_libdir}/libxenstore.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libxenstore.so.3.0
%attr(755,root,root) %{_libdir}/libxlutil.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libxlutil.so.1.0
%dir %{_libdir}/fs
%dir %{_libdir}/fs/ext2fs-lib
%dir %{_libdir}/fs/fat
%dir %{_libdir}/fs/iso9660
%dir %{_libdir}/fs/reiserfs
%dir %{_libdir}/fs/ufs
%dir %{_libdir}/fs/zfs
%attr(755,root,root) %{_libdir}/fs/*/fsimage.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libblktap.so
%attr(755,root,root) %{_libdir}/libblktapctl.so
%attr(755,root,root) %{_libdir}/libflask.so
%attr(755,root,root) %{_libdir}/libfsimage.so
%attr(755,root,root) %{_libdir}/libvhd.so
%attr(755,root,root) %{_libdir}/libxenctrl.so
%attr(755,root,root) %{_libdir}/libxenguest.so
%attr(755,root,root) %{_libdir}/libxenlight.so
%attr(755,root,root) %{_libdir}/libxenstore.so
%attr(755,root,root) %{_libdir}/libxlutil.so
%{_includedir}/_libxl_types.h
%{_includedir}/blktaplib.h
%{_includedir}/fsimage*.h
%{_includedir}/libxl*.h
%{_includedir}/xen*.h
%{_includedir}/xs*.h
%{_includedir}/xen

%files static
%defattr(644,root,root,755)
%{_libdir}/libblktap.a
%{_libdir}/libblktapctl.a
%{_libdir}/libflask.a
%{_libdir}/libvhd.a
%{_libdir}/libxenctrl.a
%{_libdir}/libxenguest.a
%{_libdir}/libxenlight.a
%{_libdir}/libxenstore.a
%{_libdir}/libxlutil.a

%files xend
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/blktapctrl
%{systemdunitdir}/blktapctrl.service
%{systemdunitdir}/xend.service
%attr(754,root,root) %{_sysconfdir}/rc.d/init.d/xend
%config(noreplace) %verify(not md5 mtime size) /etc/udev/rules.d/xend.rules
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/xen/xm*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/xen/xend*
%attr(755,root,root) %{_sbindir}/xend
%attr(755,root,root) %{_sbindir}/xm
%dir %attr(700,root,root) /var/run/xend
%{systemdtmpfilesdir}/xend.conf

%if %{with ocaml}
%files -n ocaml-xen
%defattr(644,root,root,755)
%doc tools/ocaml/LICENSE
%attr(755,root,root) %{_sbindir}/oxenstored
%dir %{_libdir}/ocaml/site-lib/eventchn
%attr(755,root,root) %{_libdir}/ocaml/site-lib/eventchn/dlleventchn_stubs.so
%dir %{_libdir}/ocaml/site-lib/log
%attr(755,root,root) %{_libdir}/ocaml/site-lib/log/dllsyslog_stubs.so
%dir %{_libdir}/ocaml/site-lib/mmap
%attr(755,root,root) %{_libdir}/ocaml/site-lib/mmap/dllmmap_stubs.so
%dir %{_libdir}/ocaml/site-lib/xb
%attr(755,root,root) %{_libdir}/ocaml/site-lib/xb/dllxb_stubs.so
%dir %{_libdir}/ocaml/site-lib/xc
%attr(755,root,root) %{_libdir}/ocaml/site-lib/xc/dllxc_stubs.so
%dir %{_libdir}/ocaml/site-lib/xl
%attr(755,root,root) %{_libdir}/ocaml/site-lib/xl/dllxl_stubs.so

%files -n ocaml-xen-devel
%defattr(644,root,root,755)
%{_libdir}/ocaml/site-lib/eventchn/META
%{_libdir}/ocaml/site-lib/eventchn/libeventchn_stubs.a
%{_libdir}/ocaml/site-lib/eventchn/eventchn.a
%{_libdir}/ocaml/site-lib/eventchn/eventchn.cm[aix]*
%{_libdir}/ocaml/site-lib/log/META
%{_libdir}/ocaml/site-lib/log/libsyslog_stubs.a
%{_libdir}/ocaml/site-lib/log/log.a
%{_libdir}/ocaml/site-lib/log/*.cm[aix]*
%{_libdir}/ocaml/site-lib/mmap/META
%{_libdir}/ocaml/site-lib/mmap/libmmap_stubs.a
%{_libdir}/ocaml/site-lib/mmap/mmap.a
%{_libdir}/ocaml/site-lib/mmap/mmap.cm[aix]*
%dir %{_libdir}/ocaml/site-lib/uuid
%{_libdir}/ocaml/site-lib/uuid/META
%{_libdir}/ocaml/site-lib/uuid/uuid.a
%{_libdir}/ocaml/site-lib/uuid/uuid.cm[aix]*
%{_libdir}/ocaml/site-lib/xb/META
%{_libdir}/ocaml/site-lib/xb/libxb_stubs.a
%{_libdir}/ocaml/site-lib/xb/xb.a
%{_libdir}/ocaml/site-lib/xb/*.cm[aix]*
%{_libdir}/ocaml/site-lib/xc/META
%{_libdir}/ocaml/site-lib/xc/libxc_stubs.a
%{_libdir}/ocaml/site-lib/xc/xc.a
%{_libdir}/ocaml/site-lib/xc/xc.cm[aix]*
%{_libdir}/ocaml/site-lib/xl/META
%{_libdir}/ocaml/site-lib/xl/libxl_stubs.a
%{_libdir}/ocaml/site-lib/xl/xl.a
%{_libdir}/ocaml/site-lib/xl/xl.cm[aix]*
%dir %{_libdir}/ocaml/site-lib/xs
%{_libdir}/ocaml/site-lib/xs/META
%{_libdir}/ocaml/site-lib/xs/xs.a
%{_libdir}/ocaml/site-lib/xs/*.cm[aix]*
%{_libdir}/ocaml/site-lib/xs/xs*.mli
%endif

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
%{py_sitedir}/pygrub-0.3-py*.egg-info
%{py_sitedir}/xen-3.0-py*.egg-info
%endif

%files -n bash-completion-%{name}
%defattr(644,root,root,755)
/etc/bash_completion.d/xl.sh
