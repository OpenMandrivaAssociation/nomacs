%define plugins %{name}-plugins

Name:		nomacs
Version:	3.22.0
Release:	3
License:	GPLv3
Group:		Graphics
Summary:	A fast and small image viewer
Source0:	https://github.com/nomacs/nomacs/archive/%{version}.tar.gz
Patch0:		nomacs-opencv5.patch
Url:		https://www.nomacs.org

BuildRequires:	cmake(Qt6Core)
BuildRequires:	cmake(Qt6Test)
BuildRequires:	cmake(Qt6Network)
BuildRequires:	cmake(Qt6PrintSupport)
BuildRequires:	cmake(Qt6Concurrent)
BuildRequires:	cmake(Qt6Svg)
BuildRequires:	cmake(Qt6Widgets)
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	qmake-qt6
BuildRequires:	qt6-qttools-linguist-tools
BuildRequires:	pkgconfig(libraw)
BuildRequires:	pkgconfig(opencv5)
BuildRequires:	pkgconfig(exiv2)
BuildRequires:	pkgconfig(libwebp)
BuildRequires:	pkgconfig(libavif)
BuildRequires:	pkgconfig(libjxl)
BuildRequires:	pkgconfig(libtiff-4)
BuildRequires:	desktop-file-utils

Recommends:	qt6-qtimageformats
Recommends:	kf6-kimageformats

Suggests:	%{plugins} >= %{EVRD}
Obsoletes:	%{plugins} < %{version}

%description
nomacs is a free image viewer small, fast and able to handle the most
common image formats including RAW images.
Additionally it is possible to synchronize multiple viewers.
A synchronization of viewers running on
the samecomputer or via LAN is possible.
It allows to compare images and spot the differences 
(e.g. schemes of architects to show the progress).

%package -n %{plugins}
Summary:		Plugins for %{name}
BuildRequires:	cmake(Qt6Core5Compat)
Requires:		%{name} = %{version}

%description -n %{plugins}
Plugins for %{name}.

%prep
%autosetup -p1

# Be sure
rmdir {3rd-party/*,3rd-party}

%conf
%cmake \
	-DCMAKE_BUILD_TYPE=Release \
	-DENABLE_RAW=1 \
	-DENABLE_JXL=ON \
	-DENABLE_AVIF=ON \
	-DUSE_SYSTEM_WEBP=ON \
	-DUSE_SYSTEM_QUAZIP=ON \
	-G Ninja \
	../ImageLounge

%build
%ninja_build -C build

%install
%ninja_install -C build

desktop-file-validate %{buildroot}%{_datadir}/applications/org.%{name}.ImageLounge.desktop

%files
%license ImageLounge/license/*
%doc README.md
%{_bindir}/%{name}
%{_datadir}/applications/org.%{name}.ImageLounge.desktop
%{_mandir}/man1/%{name}.1.*
%{_libdir}/lib*%{name}*.so*
%{_datadir}/icons/hicolor/scalable/apps/org.nomacs.ImageLounge.svg
%{_datadir}/metainfo/org.nomacs.ImageLounge.appdata.xml
%{_datadir}/nomacs

# It will be improved, but nomacs search and find plugins only here
%files -n %{plugins}
%{_libdir}/%{plugins}/lib*Plugin.so*
