#
# TODO:
#  - system ovmf, ipxe? (like system seabios)
#  - check if other tools/libs are not usable in domU, move them to -guest
#    packages if so
#  - pass bconds to qemu configure script (tricky, as the script is called from
#    Xen Makefiles)
#  - fix %doc - some files are installed in docdir both by make install and %d,
#    other are installed once
#  - mini-os objects are relinked on install (because of .PHONY rules used to make them)
#
# Conditional build:
%bcond_without	qemu_traditional	# without qemu-xen-traditional
%bcond_without	opengl			# OpenGL support in Xen qemu
%bcond_without	sdl			# SDL support in Xen qemu
%bcond_without	bluetooth		# bluetooth support in Xen qemu
%bcond_without	brlapi			# brlapi support in Xen qemu
%bcond_with	golang			# Go library
%bcond_without	ocaml			# Ocaml libraries for Xen tools
%bcond_without	pv_grub			# pv-grub (deprecated)
%bcond_with	python2			# CPython 2.x module instead of 3.x
%bcond_without	efi			# EFI hypervisor
%bcond_without	hypervisor		# Xen hypervisor build
%bcond_without	stubdom			# stubdom build
%bcond_without	xsm			# XSM security module (by default, Flask)
%bcond_without	systemd			# systemd

%ifnarch %{x8664} %{arm}
%undefine	with_hypervisor
%endif
%ifnarch %{x8664}
%undefine	with_efi
%endif
%ifnarch %{ix86} %{x8664}
%undefine	with_stubdom
%endif

# from ./stubdom/configure.ac
%define	polarssl_version	1.1.4
%define tpm_emulator_version	0.7.4
%define gmp_version		4.3.2

%define	xen_extfiles_url	https://xenbits.xensource.com/xen-extfiles
Summary:	Xen - a virtual machine monitor
Summary(pl.UTF-8):	Xen - monitor maszyny wirtualnej
Name:		xen
Version:	4.19.2
Release:	1
License:	GPL v2, interface parts on BSD-like
Group:		Applications/System
# for available versions see https://xenproject.org/xen-project-archives/
Source0:	https://downloads.xenproject.org/release/xen/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	e009b933a7ff72ade1ce77afd1a776e4
# used by stubdoms; Source10-19 versions set in stubdom/configure.ac
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
Source17:	%{xen_extfiles_url}/polarssl-%{polarssl_version}-gpl.tgz
# Source17-md5:	7b72caf22b01464ee7d6165f2fd85f44
Source18:	%{xen_extfiles_url}/tpm_emulator-%{tpm_emulator_version}.tar.gz
# Source18-md5:	e26becb8a6a2b6695f6b3e8097593db8
Source19:	https://ftp.gnu.org/gnu/gmp/gmp-%{gmp_version}.tar.bz2
# Source19-md5:	dd60683d7057917e34630b4a787932e8
# ipxe tag set in tools/firmware/etherboot/Makefile
Source20:	%{xen_extfiles_url}/ipxe-git-1d1cf74a5e58811822bee4b3da3cff7282fcdfca.tar.gz
# Source20-md5:	0d0dc7451b47f2c7a2992bbec20bf4d0
Source35:	xenconsoled.sysconfig
Source37:	xenstored.sysconfig
Source38:	xenstored.tmpfiles
# sysvinit scripts
Source46:	xen-qemu-dom0-disk-backend.init
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
# shebang patch for python2-only scripts
Patch0:		%{name}-python_scripts.patch
Patch1:		%{name}-symbols.patch
Patch2:		%{name}-link.patch
Patch3:		pygrubfix.patch
# Warning: this disables ingress filtering implemented in xen scripts!
Patch4:		%{name}-net-disable-iptables-on-bridge.patch
Patch5:		%{name}-qemu.patch
Patch6:		%{name}-doc.patch
Patch7:		%{name}-paths.patch
Patch8:		%{name}-no_fetcher.patch
Patch9:		%{name}-no_Werror.patch
Patch10:	%{name}-stubdom-build.patch
Patch12:	%{name}-systemd.patch
Patch14:	gcc9.patch
Patch15:	gcc10.patch
Patch17:	%{name}-golang-32bit.patch
Patch18:	%{name}-gcc12.patch
URL:		http://www.xen.org/products/xenhyp.html
BuildRequires:	autoconf >= 2.67
%ifarch %{ix86} %{x8664}
BuildRequires:	acpica
BuildRequires:	bcc
BuildRequires:	bin86
%endif
%{?with_efi:BuildRequires:	binutils >= 3:2.23.51.0.3-2}
BuildRequires:	bzip2-devel
%if %{with xsm}
BuildRequires:	checkpolicy
%endif
# tpm_emulator uses cmake
BuildRequires:	cmake >= 2.4
BuildRequires:	e2fsprogs-devel
BuildRequires:	fig2dev
BuildRequires:	gcc >= 6:4.8
%ifarch %{x8664}
BuildRequires:	gcc-multilib-32 >= 6:4.1
%endif
BuildRequires:	gettext-tools
%{?with_golang:BuildRequires:	golang >= 1.11.1}
BuildRequires:	libaio-devel
%ifarch %{arm} aarch64
BuildRequires:	libfdt-devel >= 1.4.0
%endif
BuildRequires:	libnl-devel >= 3.2.8
BuildRequires:	libuuid-devel
BuildRequires:	lzo-devel >= 2
BuildRequires:	ncurses-devel
%if %{with ocaml}
BuildRequires:	ocaml >= 1:4.02.0
BuildRequires:	ocaml-findlib
%endif
BuildRequires:	pandoc
BuildRequires:	perl-base
BuildRequires:	perl-tools-pod
BuildRequires:	pkgconfig
%if %{with python2}
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-markdown
%else
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	python3-markdown
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.647
BuildRequires:	seabios
%{?with_systemd:BuildRequires:	systemd-devel >= 1:209}
BuildRequires:	texlive-dvips
BuildRequires:	texlive-latex-psnfss
BuildRequires:	texlive-xetex
BuildRequires:	which
BuildRequires:	xz-devel
BuildRequires:	yajl-devel
BuildRequires:	zlib-devel
BuildRequires:	zstd-devel
%if %{with qemu_traditional}
%{?with_opengl:BuildRequires:	OpenGL-devel}
%{?with_sdl:BuildRequires:	SDL-devel >= 1.2.1}
%{?with_bluetooth:BuildRequires:	bluez-libs-devel}
%{?with_brlapi:BuildRequires:	brlapi-devel}
BuildRequires:	gnutls-devel
BuildRequires:	pciutils-devel
BuildRequires:	vde2-devel
# for xfsctl (<xfs/xfs.h>)
BuildRequires:	xfsprogs-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel
%endif
%if %{with qemu_traditional}
# FIXME: see qemu configure comments on top of spec
%{!?with_opengl:BuildConflicts:	OpenGL-devel}
%{!?with_sdl:BuildConflicts:	SDL-devel}
%{!?with_sdl:BuildConflicts:	SDL-devel}
%{!?with_bluetooth:BuildConflicts:	bluez-libs-devel}
%{!?with_brlapi:BuildConflicts:	brlapi-devel}
%endif
Requires(post,preun):	/sbin/chkconfig
Requires(post,preun,postun):	systemd-units >= 38
Requires:	%{name}-libs = %{version}-%{release}
Requires:	bridge-utils
Requires:	coreutils
Requires:	diffutils
Requires:	gawk
Requires:	iptables
Requires:	losetup
Requires:	net-tools
%if %{with python2}
Requires:	python-%{name} = %{version}-%{release}
%else
Requires:	python3-%{name} = %{version}-%{release}
%endif
Requires:	rc-scripts
Requires:	sed
Requires:	systemd-units >= 38
Requires:	util-linux
Requires:	which
Requires:	%{name}-guest = %{version}-%{release}
%ifarch %{ix86} %{x8664}
# for HVM
Suggests:	qemu-system-x86
%endif
Obsoletes:	xen-doc < 3
Obsoletes:	xen-udev < 4.1.2-2
Obsoletes:	xen-xend < 4.5
ExclusiveArch:	%{ix86} %{x8664} %{arm} aarch64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# some PPC/SPARC boot images in ELF format
%define		_noautostrip	.*%{_datadir}/\\(xen\\|qemu-xen\\)/qemu/\\(openbios-.*\\|palcode-clipper\\|s390-ccw.img\\)

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
Requires:	libnl >= 3.2.8

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

%package -n python3-xen
Summary:	Xen Python 3 modules
Summary(pl.UTF-8):	Moduły Pythona 3 dla Xena
Group:		Libraries
Requires:	%{name}-libs = %{version}-%{release}
Obsoletes:	python-xen < %{version}-%{release}

%description -n python3-xen
Xen Python 3 modules.

%description -n python3-xen -l pl.UTF-8
Moduły Pythona 3 dla Xena.

%package -n python3-xen-guest
Summary:	Xen Python 3 modules for virtual machines
Summary(pl.UTF-8):	Moduły Pythona 3 dla maszyn wirtualnych Xena
Group:		Libraries
Requires:	%{name}-libs-guest = %{version}-%{release}
Obsoletes:	python-xen-guest < %{version}-%{release}

%description -n python3-xen-guest
Xen Python 3 modules for both dom0 and domU virtual machines.

%description -n python3-xen-guest -l pl.UTF-8
Moduły Pythona 3 dla maszyn wirtualnych dom0 i domU.

%package -n bash-completion-%{name}
Summary:	bash-completion for Xen (xl)
Summary(pl.UTF-8):	Bashowe dopełnianie poleceń dla Xena (xl)
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion

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
%setup -q
%patch -P 0 -p1
%patch -P 1 -p1
%patch -P 2 -p1
%patch -P 3 -p1
%patch -P 4 -p1
%patch -P 5 -p1
%patch -P 6 -p1
%patch -P 7 -p1
%patch -P 8 -p1
%patch -P 9 -p1
%patch -P 10 -p1
%patch -P 12 -p1
%patch -P 14 -p1
%if %(echo %{cc_version} | cut -d. -f1) >= 10
# -Wno-error=enum-conversion requires gcc 10
%patch -P 15 -p1
%if %(echo %{cc_version} | cut -d. -f1) < 12
# -Wno-error=dangling-pointer requires gcc 12
%{__sed} -i -e 's/ -Wno-error=dangling-pointer//' tools/firmware/etherboot/Config
%endif
%endif
%ifarch %{ix86} %{arm}
%patch -P 17 -p1
%endif
%patch -P 18 -p1

# stubdom sources
ln -s %{SOURCE10} %{SOURCE11} %{SOURCE12} %{SOURCE13} %{SOURCE14} stubdom
ln -s %{SOURCE17} %{SOURCE18} %{SOURCE19} stubdom
ln -s %{SOURCE20} tools/firmware/etherboot/ipxe.tar.gz

%if %{with python2}
%{__sed} -i -e '1s,/usr/bin/env python$,%{__python},' \
%else
%{__sed} -i -e '1s,/usr/bin/env python$,%{__python3},; 1s,/usr/bin/python2$,%{__python3},' \
%endif
	tools/misc/xencov_split \
	tools/pygrub/src/pygrub \
	tools/python/scripts/{convert-legacy-stream,verify-stream-v2} \
	tools/xenmon/xenmon.py

# do not allow fetching anything via git
echo GIT=/bin/false >> Config.mk

%build
# based on the 'autoconf.sh' from the sources
%{__autoconf}
cd tools
%{__autoconf}
%{__autoheader}
cd ../stubdom
%{__autoconf}
cd ../docs
%{__autoconf}
cd ..

# if gold is used then bioses and grub don't build
install -d our-ld
ln -f -s /usr/bin/ld.bfd our-ld/ld
export PATH=$(pwd)/our-ld:$PATH

# NOTE on ac_cv_*:
# - use openssl (libcrypto) instead of libgcrypt as openssl is obligatory anyway
# - prevent libiconv from being detected (not needed with glibc)

%configure \
	CPPFLAGS="%{rpmcppflags} -I/usr/include/ncurses" \
	%{?with_python2:PYTHON=%{__python}} \
	ac_cv_lib_gcrypt_gcry_md_hash_buffer=no \
	ac_cv_lib_iconv_libiconv_open=no \
	--disable-debug \
	%{!?with_golang:--disable-golang} \
	%{?with_pv_grub:--enable-pv-grub} \
	%{__enable_disable qemu_traditional qemu-traditional} \
	--enable-systemd%{!?with_systemd:=no} \
	--with-system-seabios=/usr/share/seabios/bios.bin \
%ifarch %{x8664}
	--with-system-qemu=/usr/bin/qemu-system-x86_64 \
%else
	--with-system-qemu=/usr/bin/qemu-system-i386 \
%endif
%if %{with systemd}
	--with-systemd=%{systemdunitdir}
%endif

export EXTRA_CFLAGS_XEN_TOOLS="%{rpmcflags} -I/usr/include/ncurses"
export EXTRA_CFLAGS_QEMU_TRADITIONAL="%{rpmcflags} -I/usr/include/ncurses"
export EXTRA_CFLAGS_QEMU_XEN="%{rpmcflags} -I/usr/include/ncurses"

# exporting these by configure macro break things later
# e.g. -Wl,-as-needed in LDFLAGS causes linking to fail
unset CC
unset CPP
unset CXX
unset CFLAGS
unset CPPFLAGS
unset CXXFLAGS
unset LDFLAGS

# -Werror=implicit-function-declaration breaks host compiler check in gmp, then
# build fails on cross compiling for host generator tools
export HOST_CC="%{__cc} -Wno-error=implicit-function-declaration"

%{__make} dist-xen dist-tools dist-docs \
%ifarch %{ix86}
	XEN_COMPILE_ARCH=x86_32 \
%endif
%ifarch %{x8664}
	XEN_COMPILE_ARCH=x86_64 \
%endif
	%{!?with_ocaml:OCAML_TOOLS=n} \
	XSM_ENABLE=%{?with_xsm:y}%{!?with_xsm:n} \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	V=1

%if %{with stubdom}
%{__make} dist-stubdom \
%ifarch %{ix86}
	XEN_COMPILE_ARCH=x86_32 \
%endif
%ifarch %{x8664}
	XEN_COMPILE_ARCH=x86_64 \
%endif
	%{!?with_ocaml:OCAML_TOOLS=n} \
	XSM_ENABLE=%{?with_xsm:y}%{!?with_xsm:n} \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	V=1
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{xen/examples,modules-load.d,logrotate.d} \
	$RPM_BUILD_ROOT{%{systemdtmpfilesdir},%{systemdunitdir},/var/log/xen/console}

%if %{with efi}
install -d $RPM_BUILD_ROOT/etc/efi-boot/update.d
%endif

%{__make} install-xen install-tools %{?with_stubdom:install-stubdom} install-docs \
%ifarch %{ix86}
	XEN_COMPILE_ARCH=x86_32 \
%endif
%ifarch %{x8664}
	XEN_COMPILE_ARCH=x86_64 \
%endif
	%{!?with_ocaml:OCAML_TOOLS=n} \
	XSM_ENABLE=%{?with_xsm:y}%{!?with_xsm:n} \
	DESTDIR=$RPM_BUILD_ROOT \
	HOTPLUGS=install-udev

install %{SOURCE35} $RPM_BUILD_ROOT/etc/sysconfig/xenconsoled
install %{SOURCE37} $RPM_BUILD_ROOT/etc/sysconfig/xenstored

# sysvinit scripts
%{__rm} $RPM_BUILD_ROOT/etc/rc.d/init.d/*
%{__rm} $RPM_BUILD_ROOT/etc/sysconfig/xencommons
install %{SOURCE51} $RPM_BUILD_ROOT/etc/rc.d/init.d/xenconsoled
install %{SOURCE52} $RPM_BUILD_ROOT/etc/rc.d/init.d/xenstored
install %{SOURCE53} $RPM_BUILD_ROOT/etc/rc.d/init.d/xen-watchdog
install %{SOURCE54} $RPM_BUILD_ROOT/etc/rc.d/init.d/xendomains
install %{SOURCE46} $RPM_BUILD_ROOT/etc/rc.d/init.d/xen-qemu-dom0-disk-backend
install %{SOURCE55} $RPM_BUILD_ROOT/etc/logrotate.d/xen
install %{SOURCE56} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/xen.conf
install -d $RPM_BUILD_ROOT/var/run/xenstored
install %{SOURCE38} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/xenstored.conf

install %{SOURCE60} $RPM_BUILD_ROOT%{_libexecdir}/%{name}/bin/xen-init-list
install %{SOURCE61} $RPM_BUILD_ROOT%{_libexecdir}/%{name}/bin/xen-toolstack

%{__sed} -E -i -e '1s,#!\s*/usr/bin/python(\s|$),#!%{__python}\1,' \
	$RPM_BUILD_ROOT%{_libexecdir}/%{name}/bin/pygrub

%if %{with efi}
install %{SOURCE57} $RPM_BUILD_ROOT/etc/efi-boot/xen.cfg
sed -e's;@libdir@;%{_libdir};g' -e's;@target_cpu@;%{_target_cpu};g' \
			%{SOURCE58} > $RPM_BUILD_ROOT/etc/efi-boot/update.d/xen.conf
%endif

%{__mv} $RPM_BUILD_ROOT/etc/xen/{xlexample*,examples}

install %{SOURCE59} $RPM_BUILD_ROOT%{_sysconfdir}/xen/scripts/vif-openvswitch

# for %%doc
install -d _doc
cp -p tools/pygrub/README _doc/README.pygrub

%if %{with python2}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}

%py_postclean
%else
%py3_comp $RPM_BUILD_ROOT%{py3_sitedir}
%py3_ocomp $RPM_BUILD_ROOT%{py3_sitedir}
%endif

# remove unneeded files
%if %{with hypervisor}
%{__mv} xen/xen-syms $RPM_BUILD_ROOT/boot/%{name}-syms-%{version}
%{__rm} $RPM_BUILD_ROOT/boot/xen-4.19.gz
%{__rm} $RPM_BUILD_ROOT/boot/xen-4.gz
%endif
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/xen
%{__rm} $RPM_BUILD_ROOT%{_includedir}/%{name}/COPYING

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add xen-watchdog
/sbin/chkconfig --add xenconsoled
/sbin/chkconfig --add xenstored
/sbin/chkconfig --add xendomains
/sbin/chkconfig --add xen-qemu-dom0-disk-backend
NORESTART=1
%systemd_post xen-watchdog.service xenconsoled.service xenstored.service xendomains.service xen-qemu-dom0-disk-backend.service

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

	%service xen-qemu-dom0-disk-backend stop
	/sbin/chkconfig --del xen-qemu-dom0-disk-backend
fi
%systemd_preun xen-watchdog.service xenconsoled.service xenstored.service xendomains.service xen-qemu-dom0-disk-backend.service

%postun
%systemd_reload

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%post	libs-guest -p /sbin/ldconfig
%postun	libs-guest -p /sbin/ldconfig

%post efi
[ -x /sbin/efi-boot-update ] && /sbin/efi-boot-update --auto || :

%files
%defattr(644,root,root,755)
%doc COPYING README* docs/misc/* docs/html/* _doc/*
%if %{with hypervisor}
/boot/%{name}-syms-%{version}
/boot/%{name}-%{version}.config
/boot/%{name}-%{version}.gz
/boot/%{name}.gz
%endif
%if %{with xsm}
/boot/xenpolicy-%{version}
%endif
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/xenconsoled
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/xenstored
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/xendomains
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/xen
%attr(754,root,root) /etc/rc.d/init.d/xen-watchdog
%attr(754,root,root) /etc/rc.d/init.d/xenconsoled
%attr(754,root,root) /etc/rc.d/init.d/xenstored
%attr(754,root,root) /etc/rc.d/init.d/xendomains
%attr(754,root,root) /etc/rc.d/init.d/xen-qemu-dom0-disk-backend
%if %{with systemd}
%{_prefix}/lib/modules-load.d/xen.conf
%{systemdunitdir}/proc-xen.mount
%{systemdunitdir}/xen-init-dom0.service
%{systemdunitdir}/xen-watchdog.service
%{systemdunitdir}/xenconsoled.service
%{systemdunitdir}/xenstored.service
%{systemdunitdir}/xendriverdomain.service
%{systemdunitdir}/xendomains.service
%{systemdunitdir}/xen-qemu-dom0-disk-backend.service
%endif
%dir %{_sysconfdir}/xen
%dir %{_sysconfdir}/xen/auto
%dir %{_sysconfdir}/xen/examples
%dir %{_sysconfdir}/xen/scripts
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/xen/scripts/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/xen/examples/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/xen/README*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/xen/cpupool
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/xen/xl.conf
%if %{with qemu_traditional}
%attr(755,root,root) %{_bindir}/qemu-img-xen
%attr(755,root,root) %{_bindir}/qemu-nbd-xen
%endif
%attr(755,root,root) %{_bindir}/vchan-socket-proxy
%attr(755,root,root) %{_bindir}/xen-cpuid
%attr(755,root,root) %{_bindir}/xenalyze
%attr(755,root,root) %{_bindir}/xencov_split
%if %{with xsm}
%attr(755,root,root) %{_sbindir}/flask-*
%endif
%attr(755,root,root) %{_sbindir}/gdbsx
%attr(755,root,root) %{_sbindir}/xen-*
%attr(755,root,root) %{_sbindir}/xenbaked
%attr(755,root,root) %{_sbindir}/xenconsoled
%attr(755,root,root) %{_sbindir}/xencov
%attr(755,root,root) %{_sbindir}/xenhypfs
%attr(755,root,root) %{_sbindir}/xenlockprof
%attr(755,root,root) %{_sbindir}/xenmon
%attr(755,root,root) %{_sbindir}/xenperf
%attr(755,root,root) %{_sbindir}/xenpm
%attr(755,root,root) %{_sbindir}/xenpmd
%attr(755,root,root) %{_sbindir}/xenstored
%attr(755,root,root) %{_sbindir}/xentop
%attr(755,root,root) %{_sbindir}/xentrace
%attr(755,root,root) %{_sbindir}/xentrace_setmask
%attr(755,root,root) %{_sbindir}/xentrace_setsize
%attr(755,root,root) %{_sbindir}/xenwatchdogd
%attr(755,root,root) %{_sbindir}/xl
%dir %{_libexecdir}/%{name}
%dir %{_libexecdir}/%{name}/bin
%attr(744,root,root) %{_libexecdir}/%{name}/bin/*
%dir %{_libexecdir}/%{name}/boot
%if %{with stubdom}
%if %{with qemu_traditional}
%{_libexecdir}/%{name}/boot/ioemu-stubdom.gz
%endif
%if %{with pv_grub}
%ifarch %{ix86} %{x8664}
%{_libexecdir}/%{name}/boot/pv-grub-x86_32.gz
%endif
%ifarch %{x8664}
%{_libexecdir}/%{name}/boot/pv-grub-x86_64.gz
%endif
%endif
%{_libexecdir}/%{name}/boot/vtpm-stubdom.gz
%{_libexecdir}/%{name}/boot/vtpmmgr-stubdom.gz
%{_libexecdir}/%{name}/boot/xenstore-stubdom.gz
%{_libexecdir}/%{name}/boot/xenstorepvh-stubdom.gz
%endif
%{_libexecdir}/%{name}/boot/ipxe.bin
%ifarch %{x8664}
%{_libexecdir}/%{name}/boot/xen-shim
%endif
%attr(744,root,root) %{_libexecdir}/%{name}/boot/hvmloader
%{_mandir}/man1/xenhypfs.1*
%{_mandir}/man1/xentop.1*
%{_mandir}/man1/xl.1*
%{_mandir}/man5/xl.cfg.5*
%{_mandir}/man5/xl.conf.5*
%{_mandir}/man5/xl-disk-configuration.5*
%{_mandir}/man5/xl-network-configuration.5*
%{_mandir}/man5/xl-pci-configuration.5*
%{_mandir}/man5/xlcpupool.cfg.5*
%{_mandir}/man7/xen-pci-device-reservations.7*
%{_mandir}/man7/xen-pv-channel.7*
%{_mandir}/man7/xen-tscmode.7*
%{_mandir}/man7/xen-vbd-interface.7*
%{_mandir}/man7/xen-vtpm.7*
%{_mandir}/man7/xen-vtpmmgr.7*
%{_mandir}/man7/xl-numa-placement.7*
%{_mandir}/man8/xentrace.8*
%{_mandir}/man8/xenwatchdogd.8*
%{_sharedstatedir}/xen
%dir /var/run/xenstored
%{systemdtmpfilesdir}/xen.conf
%{systemdtmpfilesdir}/xenstored.conf
%dir %attr(0700,root,root) /var/log/xen
%dir %attr(0700,root,root) /var/log/xen/console
%if %{with qemu_traditional}
%{_datadir}/xen
%endif

%files guest
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/xen-detect
%attr(755,root,root) %{_bindir}/xenstore
%attr(755,root,root) %{_bindir}/xenstore-chmod
%attr(755,root,root) %{_bindir}/xenstore-control
%attr(755,root,root) %{_bindir}/xenstore-exists
%attr(755,root,root) %{_bindir}/xenstore-list
%attr(755,root,root) %{_bindir}/xenstore-ls
%attr(755,root,root) %{_bindir}/xenstore-read
%attr(755,root,root) %{_bindir}/xenstore-rm
%attr(755,root,root) %{_bindir}/xenstore-watch
%attr(755,root,root) %{_bindir}/xenstore-write
%{_mandir}/man1/xenstore.1*
%{_mandir}/man1/xenstore-chmod.1*
%{_mandir}/man1/xenstore-ls.1*
%{_mandir}/man1/xenstore-read.1*
%{_mandir}/man1/xenstore-write.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libxenfsimage.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libxenfsimage.so.4.19
%attr(755,root,root) %{_libdir}/libxencall.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libxencall.so.1
%attr(755,root,root) %{_libdir}/libxenctrl.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libxenctrl.so.4.19
%attr(755,root,root) %{_libdir}/libxendevicemodel.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libxendevicemodel.so.1
%attr(755,root,root) %{_libdir}/libxenevtchn.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libxenevtchn.so.1
%attr(755,root,root) %{_libdir}/libxenforeignmemory.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libxenforeignmemory.so.1
%attr(755,root,root) %{_libdir}/libxengnttab.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libxengnttab.so.1
%attr(755,root,root) %{_libdir}/libxenguest.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libxenguest.so.4.19
%attr(755,root,root) %{_libdir}/libxenhypfs.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libxenhypfs.so.1
%attr(755,root,root) %{_libdir}/libxenlight.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libxenlight.so.4.19
%attr(755,root,root) %{_libdir}/libxenstat.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libxenstat.so.4.19
%attr(755,root,root) %{_libdir}/libxentoolcore.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libxentoolcore.so.1
%attr(755,root,root) %{_libdir}/libxentoollog.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libxentoollog.so.1
%attr(755,root,root) %{_libdir}/libxenvchan.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libxenvchan.so.4.19
%attr(755,root,root) %{_libdir}/libxlutil.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libxlutil.so.4.19
%dir %{_libdir}/xenfsimage
%dir %{_libdir}/xenfsimage/ext2fs-lib
%dir %{_libdir}/xenfsimage/fat
%dir %{_libdir}/xenfsimage/iso9660
%dir %{_libdir}/xenfsimage/reiserfs
%dir %{_libdir}/xenfsimage/ufs
%dir %{_libdir}/xenfsimage/xfs
%dir %{_libdir}/xenfsimage/zfs
%attr(755,root,root) %{_libdir}/xenfsimage/*/fsimage.so

%files libs-guest
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libxenstore.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libxenstore.so.4

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libxenfsimage.so
%attr(755,root,root) %{_libdir}/libxencall.so
%attr(755,root,root) %{_libdir}/libxenctrl.so
%attr(755,root,root) %{_libdir}/libxendevicemodel.so
%attr(755,root,root) %{_libdir}/libxenevtchn.so
%attr(755,root,root) %{_libdir}/libxenforeignmemory.so
%attr(755,root,root) %{_libdir}/libxengnttab.so
%attr(755,root,root) %{_libdir}/libxenguest.so
%attr(755,root,root) %{_libdir}/libxenhypfs.so
%attr(755,root,root) %{_libdir}/libxenlight.so
%attr(755,root,root) %{_libdir}/libxenstat.so
%attr(755,root,root) %{_libdir}/libxenstore.so
%attr(755,root,root) %{_libdir}/libxentoolcore.so
%attr(755,root,root) %{_libdir}/libxentoollog.so
%attr(755,root,root) %{_libdir}/libxenvchan.so
%attr(755,root,root) %{_libdir}/libxlutil.so
%{_includedir}/_libxl_types.h
%{_includedir}/_libxl_types_json.h
%{_includedir}/libxenvchan.h
%{_includedir}/libxl*.h
%{_includedir}/xen*.h
%{_includedir}/xs*.h
%{_includedir}/xen
%{_includedir}/xenstore-compat
%{_pkgconfigdir}/xencall.pc
%{_pkgconfigdir}/xencontrol.pc
%{_pkgconfigdir}/xendevicemodel.pc
%{_pkgconfigdir}/xenevtchn.pc
%{_pkgconfigdir}/xenforeignmemory.pc
%{_pkgconfigdir}/xengnttab.pc
%{_pkgconfigdir}/xenguest.pc
%{_pkgconfigdir}/xenhypfs.pc
%{_pkgconfigdir}/xenlight.pc
%{_pkgconfigdir}/xenstat.pc
%{_pkgconfigdir}/xenstore.pc
%{_pkgconfigdir}/xentoolcore.pc
%{_pkgconfigdir}/xentoollog.pc
%{_pkgconfigdir}/xenvchan.pc
%{_pkgconfigdir}/xlutil.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libxencall.a
%{_libdir}/libxenctrl.a
%{_libdir}/libxendevicemodel.a
%{_libdir}/libxenevtchn.a
%{_libdir}/libxenforeignmemory.a
%{_libdir}/libxengnttab.a
%{_libdir}/libxenguest.a
%{_libdir}/libxenhypfs.a
%{_libdir}/libxenlight.a
%{_libdir}/libxenvchan.a
%{_libdir}/libxenstat.a
%{_libdir}/libxenstore.a
%{_libdir}/libxentoolcore.a
%{_libdir}/libxentoollog.a
%{_libdir}/libxlutil.a

# -n golang-xen
# XXX: location?
#%{_datadir}/gocode/src/golang.xenproject.org/xenlight

%if %{with ocaml}
%files -n ocaml-xen
%defattr(644,root,root,755)
%doc tools/ocaml/LICENSE
%attr(755,root,root) %{_sbindir}/oxenstored
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/xen/oxenstored.conf
%dir %{_libdir}/ocaml/xenbus
%attr(755,root,root) %{_libdir}/ocaml/xenbus/dllxenbus_stubs.so
%dir %{_libdir}/ocaml/xenctrl
%attr(755,root,root) %{_libdir}/ocaml/xenctrl/dllxenctrl_stubs.so
%dir %{_libdir}/ocaml/xeneventchn
%attr(755,root,root) %{_libdir}/ocaml/xeneventchn/dllxeneventchn_stubs.so
%dir %{_libdir}/ocaml/xenmmap
%attr(755,root,root) %{_libdir}/ocaml/xenmmap/dllxenmmap_stubs.so

%files -n ocaml-xen-devel
%defattr(644,root,root,755)
%{_libdir}/ocaml/xenbus/META
%{_libdir}/ocaml/xenbus/libxenbus_stubs.a
%{_libdir}/ocaml/xenbus/xenbus.a
%{_libdir}/ocaml/xenbus/*.cm[aixo]*
%{_libdir}/ocaml/xenctrl/META
%{_libdir}/ocaml/xenctrl/libxenctrl_stubs.a
%{_libdir}/ocaml/xenctrl/xenctrl.a
%{_libdir}/ocaml/xenctrl/xenctrl.cm[aix]*
%{_libdir}/ocaml/xeneventchn/META
%{_libdir}/ocaml/xeneventchn/libxeneventchn_stubs.a
%{_libdir}/ocaml/xeneventchn/xeneventchn.a
%{_libdir}/ocaml/xeneventchn/xeneventchn.cm[aix]*
%{_libdir}/ocaml/xenmmap/META
%{_libdir}/ocaml/xenmmap/libxenmmap_stubs.a
%{_libdir}/ocaml/xenmmap/xenmmap.a
%{_libdir}/ocaml/xenmmap/xenmmap.cm[aix]*
%dir %{_libdir}/ocaml/xenstore
%{_libdir}/ocaml/xenstore/META
%{_libdir}/ocaml/xenstore/xenstore.a
%{_libdir}/ocaml/xenstore/*.cm[aixo]*
%endif

%if %{with python2}
%files -n python-xen
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/xenfsimage.so
%dir %{py_sitedir}/xen
%{py_sitedir}/xen/util.py[co]
%dir %{py_sitedir}/xen/lowlevel
%attr(755,root,root) %{py_sitedir}/xen/lowlevel/xc.so
%{py_sitedir}/xen/migration
%{py_sitedir}/grub
%{py_sitedir}/pygrub-*-py*.egg-info
%{py_sitedir}/xen-*-py*.egg-info

%files -n python-xen-guest
%defattr(644,root,root,755)
%dir %{py_sitedir}/xen
%{py_sitedir}/xen/__init__.py[co]
%dir %{py_sitedir}/xen/lowlevel
%{py_sitedir}/xen/lowlevel/__init__.py[co]
%attr(755,root,root) %{py_sitedir}/xen/lowlevel/xs.so

%else

%files -n python3-xen
%defattr(644,root,root,755)
%attr(755,root,root) %{py3_sitedir}/xenfsimage.cpython-*.so
%dir %{py3_sitedir}/xen
%dir %{py3_sitedir}/xen/__pycache__
%{py3_sitedir}/xen/util.py
%{py3_sitedir}/xen/__pycache__/util.cpython-*.py[co]
%dir %{py3_sitedir}/xen/lowlevel
%attr(755,root,root) %{py3_sitedir}/xen/lowlevel/xc.cpython-*.so
%{py3_sitedir}/xen/migration
%{py3_sitedir}/grub
%{py3_sitedir}/pygrub-*-py*.egg-info
%{py3_sitedir}/xen-*-py*.egg-info

%files -n python3-xen-guest
%defattr(644,root,root,755)
%dir %{py3_sitedir}/xen
%dir %{py3_sitedir}/xen/__pycache__
%{py3_sitedir}/xen/__init__.py*
%{py3_sitedir}/xen/__pycache__/__init__.cpython-*.py[co]
%dir %{py3_sitedir}/xen/lowlevel
%{py3_sitedir}/xen/lowlevel/__init__.py
%{py3_sitedir}/xen/lowlevel/__pycache__
%attr(755,root,root) %{py3_sitedir}/xen/lowlevel/xs.cpython-*.so
%endif

%files -n bash-completion-%{name}
%defattr(644,root,root,755)
/etc/bash_completion.d/xl

%if %{with efi}
%files efi
%defattr(644,root,root,755)
%dir %{_libdir}/efi
%{_libdir}/efi/*.efi
%attr(644,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/efi-boot/xen.cfg
%attr(644,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/efi-boot/update.d/xen.conf
%endif
