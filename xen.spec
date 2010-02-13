#
# NOTE:
# - this xen-3.3.0 kernel and userspace
#   if you are looking for xen-3.0.2 (kernel.spec:LINUX_2_6_16), checkout
#   this spec from XEN_3_0_2 branch
# - you will also need dom0 enabled kernel
#
# TODO:
# - pldized init scripts
# - script for rc-boot
#
# Conditional build:
%bcond_with	pae		# build with PAE (HIGHMEM64G) support
%bcond_with	hvm		# build with hvm (full virtualization) support
#
%define		major	3.4
%define		minor	2
Summary:	Xen - a virtual machine monitor
Summary(pl.UTF-8):	Xen - monitor maszyny wirtualnej
Name:		xen
Version:	%{major}.%{minor}
Release:	0.1
License:	GPL
Group:		Applications/System
Source0:	http://bits.xensource.com/oss-xen/release/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	f009a7abf51017aeee697c9130b6f8a6
Source1:	%{name}-xend.init
Source2:	%{name}-xendomains.init
Patch0:		%{name}-python_scripts.patch
Patch1:		%{name}-gcc.patch
URL:		http://www.cl.cam.ac.uk/Research/SRG/netos/xen/index.html
%{?with_hvm:BuildRequires:	bcc}
BuildRequires:	curl-devel
BuildRequires:	e2fsprogs-devel
BuildRequires:	gcc >= 5:3.4
BuildRequires:	latex2html
BuildRequires:	libidn-devel
BuildRequires:	ncurses-devel
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	texlive-dvips
BuildRequires:	texlive-latex-data
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
Requires:	kernel(xen0) = %{major}
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

%ifnarch i686 athlon pentium3 pentium4
%undefine	with_pae
%endif

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

%package hotplug
Summary:	xen hotplug scripts
Summary(pl.UTF-8):	Skrypty hotplug dla xena
Group:		Application/System

%description hotplug
xen hotplug scripts.

%description hotplug -l pl.UTF-8
Skrypty hotplug dla xena.

%package udev
Summary:	xen udev scripts
Summary(pl.UTF-8):	Skrypty udev dla xena
Group:		Application/System

%description udev
xen udev scripts.

%description udev -l pl.UTF-8
Skrypty udev dla xena.

%package -n python-xen
Summary:	xen Python modules
Summary(pl.UTF-8):	Moduły Pythona dla xena
Group:		Libraries
Conflicts:	xen < 3.2.1-0.3

%description -n python-xen
xen Python modules.

%description -n python-xen -l pl.UTF-8
Moduły Pythona dla xena.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

find '(' -name '*~' -o -name '*.orig' -o -name '.gitignore' ')' -print0 | xargs -0 -r -l512 rm -fv

%build
CFLAGS="%{rpmcflags} -I/usr/include/ncurses" \
CXXFLAGS="%{rpmcflags} -I/usr/include/ncurses" \
%{__make} -j1 xen tools \
	%{?with_pae:XEN_TARGET_X86_PAE=y} \
	CC="%{__cc}" \
	CXX="%{__cxx}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/var/run/{xen-hotplug,xend,xenstored}

%{__make} install-xen install-tools install-docs \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	%{?with_pae:XEN_TARGET_X86_PAE=y} \
	DESTDIR=$RPM_BUILD_ROOT \
	XEN_PYTHON_NATIVE_INSTALL=1

install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/xend
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/xendomains

install -d $RPM_BUILD_ROOT%{_localstatedir}/lib/%{name}/xend-db/{domain,vnet}
install -d $RPM_BUILD_ROOT%{_sharedstatedir}/xen/save

cp -a dist/install/etc/udev $RPM_BUILD_ROOT%{_sysconfdir}
cp -a dist/install/etc/hotplug $RPM_BUILD_ROOT%{_sysconfdir}

%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}

%py_postclean
# remove unneeded files
rm -f $RPM_BUILD_ROOT%{_includedir}/%{name}/COPYING
rm -rf $RPM_BUILD_ROOT%{_docdir}/xen
rm -rf $RPM_BUILD_ROOT%{_docdir}/qemu/qemu-doc.html
rm -rf $RPM_BUILD_ROOT/''etc/init.d
rm -f $RPM_BUILD_ROOT/boot/xen-3.2.gz
rm -f $RPM_BUILD_ROOT/boot/xen-3.gz
# strip - Unable to recognise the format of the input file 
rm -f $RPM_BUILD_ROOT%{_datadir}/xen/qemu/openbios-sparc32
rm -f $RPM_BUILD_ROOT%{_datadir}/xen/qemu/openbios-sparc64


# conflict with qemu
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/qemu-img.1
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/qemu.1

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add xend
/sbin/chkconfig --add xendomains

%preun
if [ "$1" = "0" ]; then
	%service xend stop
	/sbin/chkconfig --del xend

	%service xendomains stop
	/sbin/chkconfig --del xendomains
fi

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING README docs/misc/*
%doc docs/html/*
/boot/%{name}-syms-%{version}
/boot/%{name}-%{version}.gz
/boot/%{name}.gz
%attr(754,root,root) /etc/rc.d/init.d/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/*
%dir %{_sysconfdir}/xen
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/xen/qemu-ifup
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/xen/*.*
#%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/xen/b*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/xen/xmexample[12]
%dir %{_sysconfdir}/xen/auto
%dir %{_sysconfdir}/xen/scripts
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/xen/scripts/*
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
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
%dir /var/run/xen-hotplug
%dir %attr(700,root,root) /var/run/xend
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
%attr(755,root,root) %{_libdir}/fs/*/*.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%if %{without hvm}
%files hotplug
%defattr(644,root,root,755)
%attr(755,root,root) /etc/hotplug/*
%endif

%files udev
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) /etc/udev/*

%files -n python-xen
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/fsimage.so
%{py_sitedir}/grub
%dir %{py_sitedir}/xen
%dir %{py_sitedir}/xen/lowlevel
%{py_sitedir}/xen/lowlevel/*.py*
%attr(755,root,root) %{py_sitedir}/xen/lowlevel/*.so
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
