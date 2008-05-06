# TODO:
# - pldized init scripts
# - script for rc-boot
#
# Conditional build:
%bcond_without	pae		# build without PAE (HIGHMEM64G) support (PLD Xen* kernels require PAE)
#
Summary:	Xen - a virtual machine monitor
Summary(pl.UTF-8):	Xen - monitor maszyny wirtualnej
Name:		xen
Version:	3.0.2
Release:	2
License:	GPL
Group:		Applications/System
Source0:	http://www.cl.cam.ac.uk/Research/SRG/netos/xen/downloads/%{name}-%{version}-src.tgz
# Source0-md5:	544eab940a0734a55459d648e5c3b224
Source1:	%{name}-xend.init
Source2:	%{name}-xendomains.init
Patch0:		%{name}-python_scripts.patch
Patch1:		%{name}-bash_scripts.patch
Patch2:		%{name}-bridge_setup.patch
Patch3:		%{name}-xenstore-version.patch
Patch4:		%{name}-reisermodule.patch
Patch5:		%{name}-libvncserver-detect-fix.patch
URL:		http://www.cl.cam.ac.uk/Research/SRG/netos/xen/index.html
BuildRequires:	SDL-devel
BuildRequires:	XFree86-devel
%ifarch %{ix86}
BuildRequires:	bcc
%endif
BuildRequires:	cpp
BuildRequires:	curl-devel
BuildRequires:	e2fsprogs-devel
BuildRequires:	latex2html
BuildRequires:	libidn-devel
BuildRequires:	libvncserver-devel
BuildRequires:	ncurses-devel
BuildRequires:	progsreiserfs-devel
BuildRequires:	python-Twisted
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	tetex-dvips
BuildRequires:	tetex-format-latex
BuildRequires:	tetex-latex-psnfss
BuildRequires:	transfig
BuildRequires:	which
BuildRequires:	zlib-devel
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
Requires:	ZopeInterface
Requires:	bridge-utils
Requires:	kernel(xen0) = %{version}
Requires:	losetup
Requires:	python-TwistedWeb
Requires:	rc-scripts
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
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}

%description devel
Header files for xen.

%description devel -l pl.UTF-8
Pliki nagłówkowe xena.

%package static
Summary:	Static xen libraries
Summary(pl.UTF-8):	Statyczne biblioteki xena
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Static xen libraries.

%description static -l pl.UTF-8
Statyczne biblioteki xena.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

chmod -R u+w .

%build
CFLAGS="%{rpmcflags} -I/usr/include/ncurses" \
CXXFLAGS="%{rpmcflags} -I/usr/include/ncurses" \
%{__make} xen tools docs \
	%{?with_pae:XEN_TARGET_X86_PAE=y} \
	CC="%{__cc}" \
	CXX="%{__cxx}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/var/run/{xen-hotplug,xend,xenstored}

%{__make} install-xen install-tools install-docs \
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
rm -f $RPM_BUILD_ROOT%{_includedir}/%{name}/COPYING
rm -rf $RPM_BUILD_ROOT%{_docdir}/xen
rm -rf $RPM_BUILD_ROOT/etc/init.d
rm -f $RPM_BUILD_ROOT/boot/xen-3.0.gz
rm -f $RPM_BUILD_ROOT/boot/xen-3.gz

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
%doc COPYING ChangeLog README docs/misc/*
%doc docs/html/*
/boot/%{name}-syms-%{version}
/boot/%{name}-%{version}.gz
/boot/%{name}.gz
%attr(754,root,root) /etc/rc.d/init.d/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/*
%config(noreplace) %verify(not md5 mtime size) /etc/udev/*
%attr(755,root,root) /etc/hotplug/*
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
%ifarch %{ix86}
%dir %{_libdir}/%{name}/boot
%attr(744,root,root) %{_libdir}/%{name}/boot/hvmloader
%endif
%{_datadir}/xen
%dir %{py_sitedir}/grub
%{py_sitedir}/grub/*.py[co]
%dir %{py_sitedir}/grub/fsys
%{py_sitedir}/grub/fsys/*.py[co]
%dir %{py_sitedir}/grub/fsys/reiser
%{py_sitedir}/grub/fsys/reiser/*.py[co]
%attr(755,root,root) %{py_sitedir}/grub/fsys/reiser/*.so
%dir %{py_sitedir}/grub/fsys/ext2
%{py_sitedir}/grub/fsys/ext2/*.py[co]
%attr(755,root,root)  %{py_sitedir}/grub/fsys/ext2/*.so
%dir %{py_sitedir}/xen
%dir %{py_sitedir}/xen/lowlevel
%{py_sitedir}/xen/lowlevel/*.py[co]
%attr(755,root,root) %{py_sitedir}/xen/lowlevel/*.so
%{py_sitedir}/xen/sv
%{py_sitedir}/xen/util
%{py_sitedir}/xen/web
%{py_sitedir}/xen/xend
%{py_sitedir}/xen/xm
%{py_sitedir}/xen/*.py[co]
%{_mandir}/man?/*
%{_sharedstatedir}/xen
%{_sharedstatedir}/xenstored
%dir /var/run/xen-hotplug
%dir %attr(700,root,root) /var/run/xend
%dir /var/run/xenstored

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
