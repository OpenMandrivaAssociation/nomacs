%define _disable_ld_no_undefined 1
%define _disable_lto 1

%define major 3
%define libname %mklibname %{name} %{major}
%define plugins %{name}-plugins

Name:		nomacs
Version:	3.14.2
Release:	1
License:	GPLv3
Group:		Graphics
Summary:	A fast and small image viewer
Source0:	https://github.com/nomacs/nomacs/archive/%{version}/%{name}-%{version}.tar.gz
Source1:	https://github.com/nomacs/nomacs-plugins/archive/nomacs-plugins-master.zip
Source2:	%{name}.rpmlintrc
Url:		http://www.nomacs.org
Suggests:	%{plugins} >= %{EVRD}
BuildRequires:  cmake(QuaZip5)
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
BuildRequires:  pkgconfig(libtiff-4)
BuildRequires:  pkgconfig(zlib)
BuildRequires:	gomp-devel
BuildRequires:	quazip-devel
BuildRequires:	desktop-file-utils

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

%package -n %{plugins}
Summary:	Plugins for %{name}
Group:		System/Libraries
Requires:	%{name} = %{version}

%description -n %{plugins}
Plugins for %{name}.

%prep
%setup -q

rm -rf 3rdparty/quazip*

cd ..
unzip ../SOURCES/nomacs-plugins-master.zip
mv nomacs-plugins-master %{name}-%{version}/ImageLounge/plugins

%build
export CC=gcc
export CXX=g++
%cmake_qt5 -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_FLAGS_RELEASE:STRING="-O2" -DENABLE_RAW=1 -DUSE_SYSTEM_WEBP=ON -DUSE_SYSTEM_QUAZIP=OFF ../ImageLounge

%make_build

%install
%make_install -C build

desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%files
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_mandir}/man1/%{name}.1.*
%{_datadir}/%{name}/translations/%{name}_*.qm
%{_datadir}/pixmaps/%{name}.svg
%{_datadir}/appdata/nomacs.appdata.xml

%files -n %{libname}
%{_libdir}/lib*%{name}*.so.%{major}*

# It will be improved, but nomacs search and find plugins only here
%files -n %{plugins}
%{_prefix}/lib/%{plugins}/lib*Plugin.so.%{major}*
