# LTO doesn't work with the mechanism used to turn the icon
# files into object files for the KF6BreezeIcons library
%define _disable_lto 1

%undefine _debugsource_packages
%define major %(echo %{version} |cut -d. -f1-2)
%define stable %([ "$(echo %{version} |cut -d. -f2)" -ge 80 -o "$(echo %{version} |cut -d. -f3)" -ge 80 ] && echo -n un; echo -n stable)
#define git 20240217

Summary:	Breeze icon theme
Name:		kf6-breeze-icons
Version:	6.16.0
Release:	%{?git:0.%{git}.}1
License:	GPL
Group:		Graphical desktop/KDE
Url:		https://www.kde.org
%if 0%{?git:1}
Source0:	https://invent.kde.org/frameworks/breeze-icons/-/archive/master/breeze-icons-master.tar.bz2#/breeze-icons-%{git}.tar.bz2
%else
Source0:	http://download.kde.org/%{stable}/frameworks/%{major}/breeze-icons-%{version}.tar.xz
%endif
#Patch0:		crap.patch
BuildRequires:	cmake(ECM)
BuildRequires:	cmake(KF6Config)
BuildRequires:	cmake(KF6IconThemes)
BuildRequires:	cmake(Qt6)
BuildRequires:	cmake(Qt6Core)
BuildRequires:	cmake(Qt6Test)
BuildRequires:	libxml2-utils
BuildRequires:	python-lxml
BuildRequires:	util-linux-core
# Just to prevent the plasma5 version from being pulled in
BuildRequires:	plasma6-xdg-desktop-portal-kde
Requires:	hicolor-icon-theme
Provides:	breeze-icons = %{EVRD}
BuildSystem:	cmake
BuildOption:	-DBUILD_QCH:BOOL=ON
BuildOption:	-DICONS_LIBRARY:BOOL=ON

%description
Breeze icon theme. Compliant with FreeDesktop.org naming schema.

%files
%dir %{_iconsdir}/breeze
%dir %{_iconsdir}/breeze-dark
%{_iconsdir}/breeze*/actions
%{_iconsdir}/breeze*/animations
%{_iconsdir}/breeze*/applets
%{_iconsdir}/breeze*/apps
%{_iconsdir}/breeze*/categories
%{_iconsdir}/breeze*/devices
%{_iconsdir}/breeze*/emblems
%{_iconsdir}/breeze*/emotes
%{_iconsdir}/breeze*/mimetypes
%{_iconsdir}/breeze*/places
%{_iconsdir}/breeze*/preferences
%{_iconsdir}/breeze*/status
%{_iconsdir}/breeze*/index.theme
%ghost %{_iconsdir}/breeze/icon-theme.cache
%ghost %{_iconsdir}/breeze-dark/icon-theme.cache

#-----------------------------------------------------------------------------
%package devel
Summary:	Development files for Breeze Icons
Group:		Development/KDE and Qt
Requires:	%{name} = %{EVRD}

%description devel
Development files for Breeze Icons

%files devel
%{_libdir}/cmake/KF6BreezeIcons
#-----------------------------------------------------------------------------

%prep
%autosetup -p1 -n breeze-icons-%{?git:master}%{!?git:%{version}}

%install -a
# (crazy) fix calamares not showing right icons here
# reason is we use static names in /home for live user
# that working fine for EN , but now we boot != EN
# and the $HOME/ dirs are translated to whatever language.
# in this case DE is using generic names and pulls $basename.svg
# from theme , which are then the icons from here :)
# We do not needed these , we provide own calamares icon so wipe away.

rm -rf %{buildroot}%{_iconsdir}/breeze/apps/48/calamares.svg
rm -rf %{buildroot}%{_iconsdir}/breeze-dark/apps/48/calamares.svg

# (tpg) try reduce size
hardlink -c -v %{buildroot}%{_iconsdir}

touch  %{buildroot}%{_iconsdir}/{breeze,breeze-dark}/icon-theme.cache

%libpackages
echo '%{_includedir}/KF6/BreezeIcons' >>%{specpartsdir}/%{mklibname -d KF6BreezeIcons}.specpart

# automatic gtk icon cache update on rpm installs/removals
%transfiletriggerin -- %{_iconsdir}/breeze
if [ -x /usr/bin/gtk-update-icon-cache ]; then
    gtk-update-icon-cache --force %{_iconsdir}/breeze &>/dev/null || :
fi

%transfiletriggerin -- %{_iconsdir}/breeze-dark
if [ -x /usr/bin/gtk-update-icon-cache ]; then
    gtk-update-icon-cache --force %{_iconsdir}/breeze-dark &>/dev/null || :
fi

%transfiletriggerpostun -- %{_iconsdir}/breeze
if [ -x /usr/bin/gtk-update-icon-cache ]; then
    gtk-update-icon-cache --force %{_iconsdir}/breeze &>/dev/null || :
fi

%transfiletriggerpostun -- %{_iconsdir}/breeze-dark
if [ -x /usr/bin/gtk-update-icon-cache ]; then
    gtk-update-icon-cache --force %{_iconsdir}/breeze-dark &>/dev/null || :
fi
