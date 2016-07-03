%define major 3
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d
%define		srcdir	ImageLounge
Name:		nomacs
Version:	3.2.0
Release:	1
License:	GPLv3
Group:		Graphics
Summary:	A fast and small image viewer
Source0:	https://github.com/nomacs/nomacs/releases/download/%{version}/%{name}-%{version}-source.tar.bz2
Url:		http://www.nomacs.org


BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5Test)
BuildRequires:	pkgconfig(Qt5Network)
BuildRequires:	pkgconfig(Qt5PrintSupport)
BuildRequires:	pkgconfig(Qt5Concurrent)
BuildRequires:	pkgconfig(Qt5Svg)
BuildRequires:	cmake
BuildRequires:	qmake5
BuildRequires:	qt5-linguist-tools
BuildRequires:	pkgconfig(libraw)
BuildRequires:	pkgconfig(opencv)
BuildRequires:	pkgconfig(exiv2)
BuildRequires:	pkgconfig(libwebp)
BuildRequires:	gomp-devel
BuildRequires:	quazip-devel
BuildRequires:	desktop-file-utils
Requires: %{libname} = %{EVRD}

%description

nomacs is a free image viewer small, fast and able to handle the most
common image formats including RAW images.
Additionally it is possible to synchronize multiple viewers.
A synchronization of viewers running on
the samecomputer or via LAN is possible.
It allows to compare images and spot the differences 
(e.g. schemes of architects to show the progress).

%package -n %{libname}
Summary:	Shared libraries for %{name}
Group:		System/Libraries

%description -n	%{libname}
Shared libraries for %{name}.

%package -n %{develname}
Summary:	Developmentlibraries for %{name}
Group:		Development/Other

%description -n	%{develname}
Development libraries for %{name}.

%prep
%setup -q
%apply_patches

rm -rf 3rdparty/libwebp
rm -rf 3rdparty/quazip*

%build
%cmake	-DUSE_SYSTEM_WEBP=ON \
	-DUSE_SYSTEM_QUAZIP=ON \
	-DENABLE_RAW=1
%make

%install
%makeinstall_std -C build

desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%files
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_mandir}/man1/%{name}.1.*
%{_datadir}/%{name}/translations/%{name}_*.qm
%{_datadir}/pixmaps/%{name}.svg
%{_datadir}/appdata/nomacs.appdata.xml

%files -n %{libname}
%{_libdir}/lib%{name}*.so.3
%{_libdir}/lib%{name}*.so.3.2.0

%files -n %{develname}
%{_libdir}/lib%{name}*.so
