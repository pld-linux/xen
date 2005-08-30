# TODO:
# - pldized init scripts
# - script for rc-boot
Summary:	Xen - a virtual machine monitor
Summary(pl):	Xen - monitor maszyny wirtualnej
Name:		xen
Version:	2.0.7
Release:	0.1
Epoch:		0
Group:		Applications/System
License:	GPL
Source0:	http://www.cl.cam.ac.uk/Research/SRG/netos/xen/downloads/%{name}-%{version}-src.tgz
# Source0-md5:	ce09744be2b34ad6ffd8eb15dae2eb1f
Source1:	%{name}-xend.init
Source2:	%{name}-xendomains.init
Patch0:		%{name}-twisted.patch
Patch1:		%{name}-scripts.patch
URL:		http://www.cl.cam.ac.uk/Research/SRG/netos/xen/index.html
BuildRequires:	XFree86-devel
BuildRequires:	curl-devel
BuildRequires:	libidn-devel
BuildRequires:	ncurses-devel
BuildRequires:	python-Twisted
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	tetex-dvips
BuildRequires:	tetex-format-latex
BuildRequires:	tetex-latex-psnfss
BuildRequires:	transfig
BuildRequires:	which
BuildRequires:	zlib-devel
Requires:	ZopeInterface
Requires:	bridge-utils
Requires:	losetup
Requires:	python-TwistedWeb
ExclusiveArch:	%{ix86}
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

%package doc
Summary:	Xen documentation
Summary(pl):	Dokumentacja xena
Group:		Applications/System
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description doc
Xen documentation.

%description doc -l pl
Dokumentacja xena.

%prep
%setup -q -n %{name}-2.0
%patch0 -p1
%patch1 -p1
chmod -R u+w .
#echo 'CXXFLAGS+=-I/usr/include/ncurses' >> tools/ioemu/gui/Makefile

%build
CFLAGS="%{rpmcflags}" \
CXXFLAGS="%{rpmcflags}" \
%{__make} xen tools docs \
	CC="%{__cc}" \
	CXX="%{__cxx}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install-xen install-tools install-docs \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/xend
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/xendomains

install -d $RPM_BUILD_ROOT%{_localstatedir}/lib/%{name}/xend-db/{domain,vnet}

#install -d $RPM_BUILD_ROOT%{_mandir}
#cp -a $RPM_BUILD_ROOT%{_prefix}/man/* $RPM_BUILD_ROOT%{_mandir}

#install -d doc-html-install/{interface,user}
#cp -a docs/html/interface/*.{png,html,css} doc-html-install/interface
#cp -a docs/html/user/*.{png,html,css} doc-html-install/user

rm -f $RPM_BUILD_ROOT%{_includedir}/%{name}/COPYING

%{py_comp} $RPM_BUILD_ROOT%{_libdir}/python
%{py_ocomp} $RPM_BUILD_ROOT%{_libdir}/python
find $RPM_BUILD_ROOT%{_libdir}/python -name '*.py' -exec rm "{}" ";"

install -d $RPM_BUILD_ROOT%{_datadir}/xen/
cp -f $RPM_BUILD_ROOT%{_datadir}/doc/xen/pdf/*.pdf $RPM_BUILD_ROOT%{_datadir}/xen/

install -d $RPM_BUILD_ROOT%{_sharedstatedir}/xen
install -d $RPM_BUILD_ROOT%{_sharedstatedir}/xen/{sv,xend-db}
install -d $RPM_BUILD_ROOT%{_sharedstatedir}/xen/xend-db/{domain,vnet,migrate}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
/sbin/chkconfig --add xend
/sbin/chkconfig --add xendomains

%postun -p /sbin/ldconfig

%preun
if [ "$1" = "0" ]; then
#	if [ -f /var/lock/subsys/xend ]; then
#		/etc/rc.d/init.d/xend stop 1>&2
#	fi
	/sbin/chkconfig --del xend
#	if [ -f /var/lock/subsys/xendomains ]; then
#		/etc/rc.d/init.d/xendomains stop 1>&2
#	fi
	/sbin/chkconfig --del xendomains
fi

%files
%defattr(644,root,root,755)
#%doc COPYING ChangeLog README docs/misc/* doc-html-install/*
%doc COPYING ChangeLog README docs/misc/*
/boot/%{name}-syms-%{version}
/boot/%{name}-%{version}.gz
/boot/%{name}.gz
%attr(754,root,root) /etc/rc.d/init.d/*
%dir %{_sysconfdir}/xen
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/xen/*.*
#%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/xen/b*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/xen/xmexample[12]
%dir %{_sysconfdir}/xen/auto
%dir %{_sysconfdir}/xen/scripts
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/xen/scripts/*
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*
%{_libdir}/python/%{name}
%attr(755,root,root) %{_libdir}/python/%{name}/lowlevel/*.so
%{_mandir}/man?/*
%dir %{_sharedstatedir}/xen
%dir %{_sharedstatedir}/xen/sv
%dir %{_sharedstatedir}/xen/xend-db
%dir %{_sharedstatedir}/xen/xend-db/domain
%dir %{_sharedstatedir}/xen/xend-db/vnet
%dir %{_sharedstatedir}/xen/xend-db/migrate

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%files doc
%defattr(644,root,root,755)
%dir %{_datadir}/xen
%{_datadir}/xen/*.pdf
