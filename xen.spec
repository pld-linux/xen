#
# TODO:
#  - check if other tools/libs are not usable in domU, move them to -guest
#    packages if so
#  - pass bconds to qemu configure script (tricky, as the script is called from
#    Xen Makefiles)
#  - fix %doc - some files are installed in docdir both by make install and %d,
#    other are installed once
#  - now the build dependencies are insane (because of what qemu can use)
#    we should make them optional or get rid of them all properly
#
#
# Conditional build:
%bcond_without	opengl		# disable OpenGL support in Xen qemu
%bcond_without	sdl		# disable SDL support in Xen qemu
%bcond_without	bluetooth	# disable bluetooth support in Xen qemu
%bcond_without	brlapi		# disable brlapi support in Xen qemu
%bcond_without	ocaml		# build Ocaml libraries for Xen tools
%bcond_without	efi		# build the EFI hypervisor

%ifnarch %{x8664}
%undefine	with_efi
%endif

# from Config.mk:
%define	seabios_version		1.6.3.2

%define	xen_extfiles_url	http://xenbits.xensource.com/xen-extfiles
Summary:	Xen - a virtual machine monitor
Summary(pl.UTF-8):	Xen - monitor maszyny wirtualnej
Name:		xen
Version:	4.2.2
Release:	2
License:	GPL v2, interface parts on BSD-like
Group:		Applications/System
Source0:	http://bits.xensource.com/oss-xen/release/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	f7362b19401a47826f2d8fd603a1782a
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
Source15:	http://xenbits.xen.org/xen-extfiles/ipxe-git-9a93db3f0947484e30e753bbd61a10b17336e20e.tar.gz
# Source15-md5:	7496268cebf47d5c9ccb0696e3b26065
# http://xenbits.xen.org/git-http/seabios.git/
# git archive --prefix=tools/firmware/seabios/ --format=tar rel-%{seabios_version} | xz > seabios-%{seabios_version}.tar.xz
Source16:	seabios-%{seabios_version}.tar.xz
# Source16-md5:	145e07ff5618a3999f94f2e830d06b05
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
Source43:	xendomains.sh
Source44:	xendomains.service
# sysvinit scripts
Source50:	xend.init
Source51:	xenconsoled.init
Source52:	xenstored.init
Source53:	xen-watchdog.init
Source54:	xendomains.init
Source55:	xen.logrotate
Source56:	xen.tmpfiles
Source57:	xen.cfg
Source58:	xen.efi-boot-update
Source59:	vif-openvswitch
Source60:	xen-init-list
Source61:	xen-toolstack
Patch0:		%{name}-python_scripts.patch
Patch1:		%{name}-symbols.patch
Patch2:		%{name}-curses.patch
Patch3:		pygrubfix.patch
Patch4:		xend.catchbt.patch
Patch5:		xend-pci-loop.patch
Patch6:		%{name}-dumpdir.patch
# Warning: this disables ingress filtering implemented in xen scripts!
Patch7:		%{name}-net-disable-iptables-on-bridge.patch
Patch8:		%{name}-configure-xend.patch
Patch9:		%{name}-initscript.patch
Patch10:	%{name}-quemu-softloat-c99.patch
Patch11:	%{name}-qemu.patch
Patch12:	%{name}-scripts-locking.patch
Patch13:	%{name}-close_lockfd_after_lock_attempt.patch
Patch14:	%{name}-librt.patch
Patch15:	%{name}-ulong.patch
Patch16:	%{name}-doc.patch
Patch100:	CVE-2013-1918-1
Patch101:	CVE-2013-1918-2
Patch102:	CVE-2013-1918-3
Patch103:	CVE-2013-1918-4
Patch104:	CVE-2013-1918-5
Patch105:	CVE-2013-1918-6
Patch106:	CVE-2013-1918-7
Patch107:	CVE-2013-1952
Patch108:	CVE-2013-2072
Patch109:	CVE-2013-2076
Patch110:	CVE-2013-2077
Patch111:	CVE-2013-2078
#CVE-2013-2194 XEN XSA-55 integer overflows
#CVE-2013-2195 XEN XSA-55 pointer dereferences
#CVE-2013-2196 XEN XSA-55 other problems
Patch112:	0001-libelf-abolish-libelf-relocate.c.patch
Patch113:	0002-libxc-introduce-xc_dom_seg_to_ptr_pages.patch
Patch114:	0003-libxc-Fix-range-checking-in-xc_dom_pfn_to_ptr-etc.patch
Patch115:	0004-libelf-add-struct-elf_binary-parameter-to-elf_load_i.patch
Patch116:	0005-libelf-abolish-elf_sval-and-elf_access_signed.patch
Patch117:	0006-libelf-move-include-of-asm-guest_access.h-to-top-of-.patch
Patch118:	0007-libelf-xc_dom_load_elf_symtab-Do-not-use-syms-uninit.patch
Patch119:	0008-libelf-introduce-macros-for-memory-access-and-pointe.patch
Patch120:	0009-tools-xcutils-readnotes-adjust-print_l1_mfn_valid_no.patch
Patch121:	0010-libelf-check-nul-terminated-strings-properly.patch
Patch122:	0011-libelf-check-all-pointer-accesses.patch
Patch123:	0012-libelf-Check-pointer-references-in-elf_is_elfbinary.patch
Patch124:	0013-libelf-Make-all-callers-call-elf_check_broken.patch
Patch125:	0014-libelf-use-C99-bool-for-booleans.patch
Patch126:	0015-libelf-use-only-unsigned-integers.patch
Patch127:	0016-libelf-check-loops-for-running-away.patch
Patch128:	0017-libelf-abolish-obsolete-macros.patch
Patch129:	0018-libxc-Add-range-checking-to-xc_dom_binloader.patch
Patch130:	0019-libxc-check-failure-of-xc_dom_-_to_ptr-xc_map_foreig.patch
Patch131:	0020-libxc-check-return-values-from-malloc.patch
Patch132:	0021-libxc-range-checks-in-xc_dom_p2m_host-and-_guest.patch
Patch133:	0022-libxc-check-blob-size-before-proceeding-in-xc_dom_ch.patch
Patch134:	0023-libxc-Better-range-check-in-xc_dom_alloc_segment.patch
Patch135:	CVE-2013-2211
Patch136:	CVE-2013-1432
URL:		http://www.xen.org/products/xenhyp.html
%{?with_opengl:BuildRequires:	OpenGL-devel}
%{?with_sdl:BuildRequires:	SDL-devel >= 1.2.1}
%ifarch %{ix86} %{x8664}
BuildRequires:	acpica
BuildRequires:	bcc
%endif
%{?with_bluetooth:BuildRequires:	bluez-libs-devel}
%{?with_brlapi:BuildRequires:	brlapi-devel}
%{?with_efi:BuildRequires:	binutils >= 3:2.23.51.0.3-2}
BuildRequires:	bzip2-devel
BuildRequires:	ceph-devel
BuildRequires:	curl-devel
BuildRequires:	cyrus-sasl-devel >= 2
BuildRequires:	e2fsprogs-devel
BuildRequires:	gcc >= 5:3.4
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.12
BuildRequires:	gnutls-devel
BuildRequires:	latex2html >= 2008
BuildRequires:	libaio-devel
BuildRequires:	libiscsi-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libuuid-devel
BuildRequires:	lzo-devel >= 2
BuildRequires:	ncurses-devel
%if %{with ocaml}
BuildRequires:	ocaml >= 3.04-7
BuildRequires:	ocaml-findlib
%endif
BuildRequires:	nss-devel >= 3.12.8
BuildRequires:	openssl-devel
BuildRequires:	pciutils-devel
BuildRequires:	perl-base
BuildRequires:	pkgconfig
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.647
BuildRequires:	spice-protocol >= 0.6.0
BuildRequires:	spice-server-devel >= 0.6.0
BuildRequires:	texi2html
BuildRequires:	texlive-dvips
BuildRequires:	texlive-latex-psnfss
BuildRequires:	texlive-xetex
BuildRequires:	usbredir-devel
BuildRequires:	vde2-devel
BuildRequires:	which
# for xfsctl (<xfs/xfs.h>)
BuildRequires:	xfsprogs-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xz-devel
BuildRequires:	yajl-devel
BuildRequires:	zlib-devel
# FIXME: see qemu configure comments on top of spec
%{!?with_opengl:BuildConflicts:	OpenGL-devel}
%{!?with_sdl:BuildConflicts:	SDL-devel}
%{!?with_sdl:BuildConflicts:	SDL-devel}
%{!?with_bluetooth:BuildConflicts:	bluez-libs-devel}
%{!?with_brlapi:BuildConflicts:	brlapi-devel}
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
Requires:	%{name}-guest = %{version}-%{release}
Obsoletes:	xen-doc
Obsoletes:	xen-udev
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# some PPC/SPARC boot images in ELF format
%define         _noautostrip    .*%{_datadir}/\\(xen/qemu\\|qemu-xen\\)/\\(openbios-.*\\|palcode-clipper\\)

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

%package guest
Summary:	Xen tools for virtual machines
Summary(pl.UTF-8):	Narzędzia Xen dla maszyn virtualnych
Group:		Applications/System
Requires:	%{name}-libs-guest = %{version}-%{release}

%description guest
Xen utilities for both dom0 and domU virtual domains.

%description guest -l pl.UTF-8
Narzędzia Xena dla maszyn wirtualnych dom0 i domU.

%package libs
Summary:	Xen libraries
Summary(pl.UTF-8):	Biblioteki Xena
Group:		Libraries
Requires:	%{name}-libs-guest = %{version}-%{release}

%description libs
Xen libraries.

%description libs -l pl.UTF-8
Biblioteki Xena.

%package libs-guest
Summary:	Xen libraries for virtual machines
Summary(pl.UTF-8):	Biblioteki Xena dla maszyn wirtualnych
Group:		Libraries

%description libs-guest
Xen libraries for both dom0 and domU virtual machines.

%description libs-guest -l pl.UTF-8
Biblioteki Xena dla maszyn wirtualnych dom0 i domU.

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
%if %{with ocaml}
%requires_eq	ocaml-runtime
%endif

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
%if %{with ocaml}
%requires_eq	ocaml
%endif

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

%package -n python-xen-guest
Summary:	Xen Python modules for virtual machines
Summary(pl.UTF-8):	Moduły Pythona dla maszyn wirtualnych Xena
Group:		Libraries
Requires:	%{name}-libs-guest = %{version}-%{release}
Conflicts:	xen < 3.2.1-0.3

%description -n python-xen-guest
Xen Python modules for both dom0 and domU virtual machines.

%description -n python-xen-guest -l pl.UTF-8
Moduły Pythona dla maszyn wirtualnych dom0 i domU.

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

%package efi
Summary:	Xen hypervisor binary for EFI
Summary(pl.UTF-8):	Hipernadzorca Xen dla EFI
Group:		Applications/System
Requires:	%{name}-libs-guest = %{version}-%{release}

%description efi
Xen hypervisor EFI binary, which can be booted directly from (U)EFI
firmware without help from any additional bootloader.

%description efi -l pl.UTF-8
Nadzorca Xen w postaci, która może być uruchomiona wprost z firmware
(U)EFI, bez potrzeby oddzielnego bootloadera.

%prep
%setup -q -a 16
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
%patch15 -p1
%patch16 -p1
# CVE
%patch100 -p1
%patch101 -p1
%patch102 -p1
%patch103 -p1
%patch104 -p1
%patch105 -p1
%patch106 -p1
%patch107 -p1
%patch108 -p1
%patch109 -p1
%patch110 -p1
%patch111 -p1
%patch112 -p1
%patch113 -p1
%patch114 -p1
%patch115 -p1
%patch116 -p1
%patch117 -p1
%patch118 -p1
%patch119 -p1
%patch120 -p1
%patch121 -p1
%patch122 -p1
%patch123 -p1
%patch124 -p1
%patch125 -p1
%patch126 -p1
%patch127 -p1
%patch128 -p1
%patch129 -p1
%patch130 -p1
%patch131 -p1
%patch132 -p1
%patch133 -p1
%patch134 -p1
%patch135 -p1
%patch136 -p1

# stubdom sources
ln -s %{SOURCE10} %{SOURCE11} %{SOURCE12} %{SOURCE13} %{SOURCE14} stubdom
ln -s %{SOURCE15} tools/firmware/etherboot/ipxe.tar.gz

# do not allow fetching anything via git
echo GIT=/bin/false >> Config.mk

%build
# if gold is used then bioses and grub doesn't build
install -d our-ld
ln -s /usr/bin/ld.bfd our-ld/ld
export PATH=$(pwd)/our-ld:$PATH

export CFLAGS="%{rpmcflags} -I/usr/include/ncurses"
export CXXFLAGS="%{rpmcflags} -I/usr/include/ncurses"

# NOTE:
# - there is a quoting bug (in tools/driver/Makefile) that causes
#   openssl is used instead of gcrypt; that's OK, openssl is obligatory
#   anyway (see configure), gcrypt is optional
# - prevent libiconv from being detected (not needed with glibc)
cd tools
%configure \
	CPPFLAGS="%{rpmcppflags} -I/usr/include/ncurses" \
	ac_cv_lib_iconv_libiconv_open=no \
	--disable-debug
cd ..

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
	CXX="%{__cxx}" \
	V=1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{xen/examples,modules-load.d,logrotate.d} \
	$RPM_BUILD_ROOT{%{systemdtmpfilesdir},%{systemdunitdir},/var/log/xen/console} \
	$RPM_BUILD_ROOT/etc/efi-boot/update.d

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
install %{SOURCE38} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/xenstored.conf
install %{SOURCE39} $RPM_BUILD_ROOT%{systemdunitdir}/xend.service
install %{SOURCE40} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/xend.conf
install %{SOURCE41} $RPM_BUILD_ROOT%{systemdunitdir}/xen-watchdog.service
install %{SOURCE42} $RPM_BUILD_ROOT/etc/modules-load.d/xen-dom0.conf
install %{SOURCE43} $RPM_BUILD_ROOT%{_prefix}/lib/%{name}/bin/xendomains.sh
install %{SOURCE44} $RPM_BUILD_ROOT%{systemdunitdir}/xendomains.service
# sysvinit scripts
%{__rm} $RPM_BUILD_ROOT/etc/rc.d/init.d/*
install %{SOURCE50} $RPM_BUILD_ROOT/etc/rc.d/init.d/xend
install %{SOURCE51} $RPM_BUILD_ROOT/etc/rc.d/init.d/xenconsoled
install %{SOURCE52} $RPM_BUILD_ROOT/etc/rc.d/init.d/xenstored
install %{SOURCE53} $RPM_BUILD_ROOT/etc/rc.d/init.d/xen-watchdog
install %{SOURCE54} $RPM_BUILD_ROOT/etc/rc.d/init.d/xendomains
install %{SOURCE55} $RPM_BUILD_ROOT/etc/logrotate.d/xen
install %{SOURCE56} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/xen.conf

install %{SOURCE60} $RPM_BUILD_ROOT%{_prefix}/lib/%{name}/bin/xen-init-list
install %{SOURCE61} $RPM_BUILD_ROOT%{_prefix}/lib/%{name}/bin/xen-toolstack

%if %{with efi}
install %{SOURCE57} $RPM_BUILD_ROOT/etc/efi-boot/xen.cfg
sed -e's;@libdir@;%{_libdir};g' -e's;@target_cpu@;%{_target_cpu};g' \
			%{SOURCE58} > $RPM_BUILD_ROOT/etc/efi-boot/update.d/xen.conf
%endif

mv $RPM_BUILD_ROOT/etc/xen/{x{m,l}example*,examples}

install %{SOURCE59} $RPM_BUILD_ROOT%{_sysconfdir}/xen/scripts/vif-openvswitch

# for %%doc
install -d _doc
for tool in blktap blktap2 pygrub xenmon ; do
	cp -p tools/$tool/README _doc/README.$tool
done
cp -al tools/qemu-xen/docs _doc/qemu-xen

%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}

%py_postclean

%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/qemu.1
mv $RPM_BUILD_ROOT%{_mandir}/man1/qemu-img{,-xen}.1
mv $RPM_BUILD_ROOT%{_mandir}/man8/qemu-nbd{,-xen}.8
# seems not needed, the path is wrong anyway
%{__rm} $RPM_BUILD_ROOT%{_prefix}/etc/qemu/target-x86_64.conf

# remove unneeded files
%{__rm} $RPM_BUILD_ROOT/boot/xen-4.2.gz
%{__rm} $RPM_BUILD_ROOT/boot/xen-4.gz
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/xen
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/qemu
%{__rm} $RPM_BUILD_ROOT%{_includedir}/%{name}/COPYING

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add xen-watchdog
/sbin/chkconfig --add xenconsoled
/sbin/chkconfig --add xenstored
/sbin/chkconfig --add xendomains
NORESTART=1
%systemd_post xen-watchdog.service xenconsoled.service xenstored.service xendomains.service

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
%systemd_preun xen-watchdog.service xenconsoled.service xenstored.service xendomains.service

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

%post	libs-guest -p /sbin/ldconfig
%postun	libs-guest -p /sbin/ldconfig

%post efi
[ -x /sbin/efi-boot-update ] && /sbin/efi-boot-update --auto || :

%files
%defattr(644,root,root,755)
%doc COPYING README* docs/misc/*
%doc docs/html/*
%doc tools/qemu-xen-dir/*.html
%doc _doc/*
/boot/%{name}-syms-%{version}
/boot/%{name}-%{version}.gz
/boot/%{name}.gz
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/xenconsoled
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/xenstored
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/xendomains
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/xencommons
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
%{systemdunitdir}/xendomains.service
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
%attr(755,root,root) %{_bindir}/xencons
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
%attr(755,root,root) %{_prefix}/lib/%{name}/bin/*
%endif
%dir %{_prefix}/lib/%{name}/boot
%{_prefix}/lib/%{name}/boot/ioemu-stubdom.gz
%{_prefix}/lib/%{name}/boot/pv-grub-x86_32.gz
%ifarch %{x8664}
%{_prefix}/lib/%{name}/boot/pv-grub-x86_64.gz
%endif
%{_prefix}/lib/%{name}/boot/xenstore-stubdom.gz
%attr(744,root,root) %{_prefix}/lib/%{name}/boot/hvmloader
%{_datadir}/xen
%{_mandir}/man1/qemu-img-xen.1*
%{_mandir}/man1/xentop.1*
%{_mandir}/man1/xentrace_format.1*
%{_mandir}/man1/xl.1*
%{_mandir}/man1/xm.1*
%{_mandir}/man5/xend-config.sxp.5*
%{_mandir}/man5/xl.cfg.5*
%{_mandir}/man5/xl.conf.5*
%{_mandir}/man5/xlcpupool.cfg.5*
%{_mandir}/man5/xmdomain.cfg.5*
%{_mandir}/man8/qemu-nbd-xen.8*
%{_mandir}/man8/xentrace.8*
%{_sharedstatedir}/xen
%{_sharedstatedir}/xenstored
%dir /var/run/xenstored
%{systemdtmpfilesdir}/xenstored.conf
%{systemdtmpfilesdir}/xen.conf
%dir %attr(0700,root,root) /var/log/xen
%dir %attr(0700,root,root) /var/log/xen/console
%{_datadir}/qemu-xen

%files guest
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/xen-detect
%attr(755,root,root) %{_bindir}/xenstore*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libblktap.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libblktap.so.3.0
%attr(755,root,root) %{_libdir}/libblktapctl.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libblktapctl.so.1.0
%attr(755,root,root) %{_libdir}/libfsimage.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfsimage.so.1.0
%attr(755,root,root) %{_libdir}/libvhd.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libvhd.so.1.0
%attr(755,root,root) %{_libdir}/libxenctrl.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libxenctrl.so.4.2
%attr(755,root,root) %{_libdir}/libxenguest.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libxenguest.so.4.2
%attr(755,root,root) %{_libdir}/libxenlight.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libxenlight.so.2.0
%attr(755,root,root) %{_libdir}/libxenstat.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libxenstat.so.0
%attr(755,root,root) %{_libdir}/libxenvchan.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libxenvchan.so.1.0
%attr(755,root,root) %{_libdir}/libxlutil.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libxlutil.so.1.0
%dir %{_libdir}/fs
%dir %{_libdir}/fs/ext2fs-lib
%dir %{_libdir}/fs/fat
%dir %{_libdir}/fs/iso9660
%dir %{_libdir}/fs/reiserfs
%dir %{_libdir}/fs/ufs
%dir %{_libdir}/fs/xfs
%dir %{_libdir}/fs/zfs
%attr(755,root,root) %{_libdir}/fs/*/fsimage.so

%files libs-guest
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libxenstore.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libxenstore.so.3.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libblktap.so
%attr(755,root,root) %{_libdir}/libblktapctl.so
%attr(755,root,root) %{_libdir}/libfsimage.so
%attr(755,root,root) %{_libdir}/libvhd.so
%attr(755,root,root) %{_libdir}/libxenctrl.so
%attr(755,root,root) %{_libdir}/libxenguest.so
%attr(755,root,root) %{_libdir}/libxenlight.so
%attr(755,root,root) %{_libdir}/libxenstat.so
%attr(755,root,root) %{_libdir}/libxenstore.so
%attr(755,root,root) %{_libdir}/libxenvchan.so
%attr(755,root,root) %{_libdir}/libxlutil.so
%{_includedir}/_libxl_list.h
%{_includedir}/_libxl_types.h
%{_includedir}/_libxl_types_json.h
%{_includedir}/blktaplib.h
%{_includedir}/fsimage*.h
%{_includedir}/libxenvchan.h
%{_includedir}/libxl*.h
%{_includedir}/xen*.h
%{_includedir}/xs*.h
%{_includedir}/xen
%{_includedir}/xenstore-compat

%files static
%defattr(644,root,root,755)
%{_libdir}/libblktap.a
%{_libdir}/libblktapctl.a
%{_libdir}/libvhd.a
%{_libdir}/libxenctrl.a
%{_libdir}/libxenguest.a
%{_libdir}/libxenlight.a
%{_libdir}/libxenvchan.a
%{_libdir}/libxenstat.a
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
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/xen/oxenstored.conf
%dir %{_libdir}/ocaml/site-lib/xenbus
%attr(755,root,root) %{_libdir}/ocaml/site-lib/xenbus/dllxenbus_stubs.so
%dir %{_libdir}/ocaml/site-lib/xenctrl
%attr(755,root,root) %{_libdir}/ocaml/site-lib/xenctrl/dllxenctrl_stubs.so
%dir %{_libdir}/ocaml/site-lib/xeneventchn
%attr(755,root,root) %{_libdir}/ocaml/site-lib/xeneventchn/dllxeneventchn_stubs.so
%dir %{_libdir}/ocaml/site-lib/xenlight
%attr(755,root,root) %{_libdir}/ocaml/site-lib/xenlight/dllxenlight_stubs.so
%dir %{_libdir}/ocaml/site-lib/xenmmap
%attr(755,root,root) %{_libdir}/ocaml/site-lib/xenmmap/dllxenmmap_stubs.so

%files -n ocaml-xen-devel
%defattr(644,root,root,755)
%{_libdir}/ocaml/site-lib/xenbus/META
%{_libdir}/ocaml/site-lib/xenbus/libxenbus_stubs.a
%{_libdir}/ocaml/site-lib/xenbus/xenbus.a
%{_libdir}/ocaml/site-lib/xenbus/*.cm[aixo]*
%{_libdir}/ocaml/site-lib/xenctrl/META
%{_libdir}/ocaml/site-lib/xenctrl/libxenctrl_stubs.a
%{_libdir}/ocaml/site-lib/xenctrl/xenctrl.a
%{_libdir}/ocaml/site-lib/xenctrl/xenctrl.cm[aix]*
%{_libdir}/ocaml/site-lib/xeneventchn/META
%{_libdir}/ocaml/site-lib/xeneventchn/libxeneventchn_stubs.a
%{_libdir}/ocaml/site-lib/xeneventchn/xeneventchn.a
%{_libdir}/ocaml/site-lib/xeneventchn/xeneventchn.cm[aix]*
%{_libdir}/ocaml/site-lib/xenmmap/META
%{_libdir}/ocaml/site-lib/xenmmap/libxenmmap_stubs.a
%{_libdir}/ocaml/site-lib/xenmmap/xenmmap.a
%{_libdir}/ocaml/site-lib/xenmmap/xenmmap.cm[aix]*
%{_libdir}/ocaml/site-lib/xenlight/META
%{_libdir}/ocaml/site-lib/xenlight/libxenlight_stubs.a
%{_libdir}/ocaml/site-lib/xenlight/xenlight.a
%{_libdir}/ocaml/site-lib/xenlight/xenlight.cm[aix]*
%dir %{_libdir}/ocaml/site-lib/xenstore
%{_libdir}/ocaml/site-lib/xenstore/META
%{_libdir}/ocaml/site-lib/xenstore/xenstore.a
%{_libdir}/ocaml/site-lib/xenstore/*.cm[aixo]*
%endif

%files -n python-xen
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/fsimage.so
%{py_sitedir}/grub
%attr(755,root,root) %{py_sitedir}/xen/lowlevel/checkpoint.so
%attr(755,root,root) %{py_sitedir}/xen/lowlevel/flask.so
%attr(755,root,root) %{py_sitedir}/xen/lowlevel/netlink.so
%attr(755,root,root) %{py_sitedir}/xen/lowlevel/ptsname.so
%attr(755,root,root) %{py_sitedir}/xen/lowlevel/xc.so
%{py_sitedir}/xen/remus
%{py_sitedir}/xen/sv
%{py_sitedir}/xen/util
%{py_sitedir}/xen/web
%{py_sitedir}/xen/xend
%{py_sitedir}/xen/xm
%{py_sitedir}/xen/xsview
%if "%{py_ver}" > "2.4"
%{py_sitedir}/pygrub-0.3-py*.egg-info
%{py_sitedir}/xen-3.0-py*.egg-info
%endif

%files -n python-xen-guest
%defattr(644,root,root,755)
%dir %{py_sitedir}/xen
%{py_sitedir}/xen/__init__.py*
%dir %{py_sitedir}/xen/lowlevel
%{py_sitedir}/xen/lowlevel/__init__.py*
%attr(755,root,root) %{py_sitedir}/xen/lowlevel/xs.so

%files -n bash-completion-%{name}
%defattr(644,root,root,755)
/etc/bash_completion.d/xl.sh

%if %{with efi}
%files efi
%defattr(644,root,root,755)
%dir %{_libdir}/efi
%{_libdir}/efi/*.efi
%attr(644,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/efi-boot/xen.cfg
%attr(644,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/efi-boot/update.d/xen.conf
%endif
