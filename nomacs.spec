%define		srcdir	ImageLounge
Name:		nomacs
Version:	1.4.0
Release:	6
License:	GPLv3
Group:		Graphics
Summary:	A fast and small image viewer
Source0:	http://sourceforge.net/projects/%{name}/files/%{name}-%{version}/%{name}-%{version}-source.tar.bz2
Url:		http://www.nomacs.org

BuildRequires:	qt4-devel
BuildRequires:	cmake
BuildRequires:	pkgconfig(libraw)
BuildRequires:	pkgconfig(opencv)
BuildRequires:	pkgconfig(exiv2)
BuildRequires:	gomp-devel
BuildRequires:	desktop-file-utils

%description

nomacs is a free image viewer small, fast and able to handle the most
common image formats including RAW images.
Additionally it is possible to synchronize multiple viewers.
A synchronization of viewers running on
the samecomputer or via LAN is possible.
It allows to compare images and spot the differences 
(e.g. schemes of architects to show the progress).

%prep
%setup -q

%build
%cmake_qt4
%make

%install
%makeinstall_std -C build

desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%files
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_mandir}/man1/%{name}.1.*
%{_datadir}/%{name}/translations/%{name}_*.qm
%{_datadir}/pixmaps/%{name}.png
