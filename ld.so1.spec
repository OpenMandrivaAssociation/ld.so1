%define version 1.9.11
%define release  %mkrel 11
%define debrelease 9
%define url ftp://ftp.debian.org/debian/dists/woody/main/source/base
%define fname ld.so

Summary: The Linux dynamic linker, library and utilities
Name: ld.so1
Version: %{version}
Release: %{release}
License: GPL
Group: System/Base
Source: %{url}/%{fname}_%{version}-%{debrelease}.tar.bz2
Patch1: %{fname}-1.9.11-duringinstall.patch.bz2
Patch2: %{fname}-1.9.11.dont-warn-broken-so.patch.bz2
Patch3: %{fname}-1.9.11-cmpwithegcs.patch.bz2
Patch4: %{fname}-1.9.11-norun.patch.bz2
Patch5: %{fname}-1.9.11-zeropreload.patch.bz2
Patch6: %{fname}-1.9.11-ld.patch.bz2
BuildRequires: gcc-cpp
BuildRoot: %{_tmppath}/%{name}-%{version}-root

%description
The dynamic linker provides the user-level support for loading and
linking DLL and ELF shared libraries.  It is required by any program
that uses shared libraries. This package provides the version %{version}
of the loader ld-linux.so.1 for backward compatibility of old libc.5
binary applications.

%prep
%setup -q -n %{fname}-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1 -b .run
%patch5 -p1 -b .preload
%patch6 -p1 -b .ld

%build
make ARCH=%{arch} CC=kgcc
%ifarch %{ix86}
make -C d-link CC=kgcc
%endif
(cd util; make ldd CC=kgcc)
perl -pi -e 's/ldd/ldd-libc5/' man/ldd.1

%install
rm -rf %buildroot
mkdir -p %{buildroot}%_mandir/man1
install -m 644 man/ldd.1 %buildroot%_mandir/man1/ldd-libc5.1

PREFIX=%buildroot sh instldso.sh --force 
#rm -f %buildroot/lib/*libdl*
mv %buildroot%_bindir/ldd %buildroot%_bindir/ldd-libc5

%if %mdkversion < 200900
%post -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README debian/copyright
%_bindir/ldd-libc5
/lib/*
%{_mandir}/*/*

