%define plugins %{name}-plugins

Name:		nomacs
Version:	3.17.2295
Release:	1
License:	GPLv3
Group:		Graphics
Summary:	A fast and small image viewer
Source0:	https://github.com/nomacs/nomacs/archive/%{version}.tar.gz
Source1:	https://github.com/nomacs/nomacs-plugins/archive/master.tar.gz
Source2:	%{name}.rpmlintrc
Url:		http://www.nomacs.org
Suggests:	%{plugins} >= %{EVRD}
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
BuildRequires:	pkgconfig(opencv4)
BuildRequires:	pkgconfig(exiv2)
BuildRequires:	pkgconfig(libwebp)
BuildRequires:	pkgconfig(libavif)
BuildRequires:	pkgconfig(libjxl)
BuildRequires:	pkgconfig(libtiff-4)
BuildRequires:	desktop-file-utils

%patchlist
nomacs-3.17.2295-plugins-find-qt6.patch
nomacs-qt6.patch

%description
nomacs is a free image viewer small, fast and able to handle the most
common image formats including RAW images.
Additionally it is possible to synchronize multiple viewers.
A synchronization of viewers running on
the samecomputer or via LAN is possible.
It allows to compare images and spot the differences 
(e.g. schemes of architects to show the progress).

%package -n %{plugins}
Summary:	Plugins for %{name}
Group:		System/Libraries
Requires:	%{name} = %{version}

%description -n %{plugins}
Plugins for %{name}.

%prep
# Not using autosetup so we can apply patches after
# the plugins have been moved to the right place
%setup -q -a1
rm -rf 3rdparty/quazip*

rmdir ImageLounge/plugins
mv nomacs-plugins-master ImageLounge/plugins

%autopatch -p1
# Update Qt5 hardcodes
find ImageLounge/plugins -name CMakeLists.txt |xargs sed -i -e 's/Qt5/Qt6/g;s,QT5,QT6,g'

%conf
%cmake \
	-DCMAKE_BUILD_TYPE=Release \
	-DENABLE_RAW=1 \
	-DENABLE_JXL=ON \
	-DENABLE_AVIF=ON \
	-DUSE_SYSTEM_WEBP=ON \
	-DUSE_SYSTEM_QUAZIP=ON \
	-DQT_QMAKE_EXECUTABLE=%{_qtdir}/bin/qmake \
	-DQT_VERSION_MAJOR=6 \
	-G Ninja \
	../ImageLounge

%build
%ninja_build -C build

%install
%ninja_install -C build

desktop-file-validate %{buildroot}%{_datadir}/applications/org.%{name}.ImageLounge.desktop

%files
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
