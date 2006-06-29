# TODO:
# - pldized init scripts
# - script for rc-boot
#
# Conditional build:
%bcond_without	pae		# build without PAE (HIGHMEM64G) support (PLD Xen* kernels require PAE)
#
Summary:	Xen - a virtual machine monitor
Summary(pl):	Xen - monitor maszyny wirtualnej
Name:		xen
Version:	3.0.2
Release:	0.2
Epoch:		0
License:	GPL
Group:		Applications/System
Source0:	http://www.cl.cam.ac.uk/Research/SRG/netos/xen/downloads/%{name}-%{version}-src.tgz
# Source0-md5:	544eab940a0734a55459d648e5c3b224
Source1:	%{name}-xend.init
Source2:	%{name}-xendomains.init
Patch0:		%{name}-python_scripts.patch
Patch1:		%{name}-bash_scripts.patch
Patch2:		%{name}-bridge_setup.patch
URL:		http://www.cl.cam.ac.uk/Research/SRG/netos/xen/index.html
BuildRequires:	XFree86-devel
BuildRequires:	curl-devel
BuildRequires:	latex2html
BuildRequires:	libidn-devel
BuildRequires:	ncurses-devel
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
Requires:	ZopeInterface
Requires:	bridge-utils
Requires:	losetup
Requires:	python-TwistedWeb
Requires:	rc-scripts
Requires:	kernel(xen) = %{version}
Obsoletes:	xen-doc
ExclusiveArch:	%{ix86}
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

%description -l pl
Ten pakiet zawiera nadzorcê oraz narzêdzia Xen, potrzebne do
uruchamiania wirtualnych maszyn w systemach x86, wraz z pakietami
kernel-xen*. Informacje jak u¿ywaæ Xena mo¿na znale¼æ na stronach
projektu.

Wirtualizacja mo¿e byæ u¿ywana do uruchamiania wielu wersji lub wielu
dystrybucji Linuksa na jednym systemie lub do testowania nie zaufanych
aplikacji w odizolowanym ¶rodowisku. Nale¿y zauwa¿yæ, ¿e technologia
Xen jest ci±gle rozwijana, a ten RPM by³ s³abo testowany. Nie nale¿y
byæ zdziwionym, je¶li ten pakiet zje dane, wypije ca³± kawê czy bêdzie
siê wy¶miewa³ w obecno¶ci przyjació³.

%package devel
Summary:	Header files for xen
Summary(pl):	Pliki nag³ówkowe xena
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description devel
Header files for xen.

%description devel -l pl
Pliki nag³ówkowe xena.

%package static
Summary:	Static xen libraries
Summary(pl):	Statyczne biblioteki xena
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Static xen libraries.

%description static -l pl
Statyczne biblioteki xena.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

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

rm -f $RPM_BUILD_ROOT%{_includedir}/%{name}/COPYING

%{py_comp} $RPM_BUILD_ROOT%{py_sitedir}
%{py_ocomp} $RPM_BUILD_ROOT%{py_sitedir}
%{py_comp} $RPM_BUILD_ROOT%{py_sitescriptdir}
%{py_ocomp} $RPM_BUILD_ROOT%{py_sitescriptdir}


find $RPM_BUILD_ROOT%{py_sitedir} -name '*.py' -exec rm "{}" ";"
find $RPM_BUILD_ROOT%{py_sitescriptdir} -name '*.py' -exec rm "{}" ";"
rm -rf $RPM_BUILD_ROOT/usr/share/doc/xen
rm -rf $RPM_BUILD_ROOT/etc/init.d

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
/sbin/chkconfig --add xend
/sbin/chkconfig --add xendomains

%postun -p /sbin/ldconfig

%preun
if [ "$1" = "0" ]; then
	%service xend stop
	/sbin/chkconfig --del xend

	%service xendomains stop
	/sbin/chkconfig --del xendomains
fi

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
%attr(755,root,root) %{_libdir}/lib*.so.*
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/bin
%attr(744,root,root) %{_libdir}/%{name}/bin/*
%{_datadir}/xen
%dir %{py_sitedir}/%{name}
%dir %{py_sitedir}/%{name}/lowlevel
%{py_sitedir}/%{name}/lowlevel/*.py*
%attr(755,root,root) %{py_sitedir}/%{name}/lowlevel/*.so
%{py_sitedir}/%{name}/sv
%{py_sitedir}/%{name}/util
%{py_sitedir}/%{name}/web
%{py_sitedir}/%{name}/xend
%{py_sitedir}/%{name}/xm
%{py_sitedir}/%{name}/*.py*
%{py_sitescriptdir}/*
%{_mandir}/man?/*
%{_sharedstatedir}/xen
%{_sharedstatedir}/xenstored
%dir /var/run/xen-hotplug
%dir %attr(700,root,root) /var/run/xend
%dir /var/run/xenstored

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
