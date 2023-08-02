%define stable %([ "$(echo %{version} |cut -d. -f3)" -ge 70 ] && echo -n un; echo -n stable)
%define git 20230802

Summary:	Breeze icon theme
Name:		kf6-breeze-icons
Version:	5.240.0
Release:	%{?git:0.%{git}.}1
License:	GPL
Group:		Graphical desktop/KDE
Url:		http://www.kde.org
%if 0%{?git:1}
Source0:	https://invent.kde.org/frameworks/breeze-icons/-/archive/master/breeze-icons-master.tar.bz2#/breeze-icons-%{git}.tar.bz2
%else
Source0:	http://download.kde.org/%{stable}/frameworks/%(echo %{version} |cut -d. -f1-2)/%{name}-%{version}.tar.xz
%endif
BuildRequires:	cmake(ECM)
BuildRequires:	cmake(KF6Config)
BuildRequires:	cmake(KF6IconThemes)
BuildRequires:	cmake(Qt6)
BuildRequires:	cmake(Qt6Core)
BuildRequires:	cmake(Qt6Test)
BuildRequires:	libxml2-utils
BuildRequires:	python-lxml
BuildRequires:	util-linux-core
# Just to prevent the plasam5 version from being pulled in
BuildRequires:	plasma6-xdg-desktop-portal-kde
BuildArch:	noarch
Requires:	hicolor-icon-theme

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
%cmake \
	-DBUILD_QCH:BOOL=ON \
	-DBUILD_WITH_QT6:BOOL=ON \
	-DKDE_INSTALL_USE_QT_SYS_PATHS:BOOL=ON \
	-G Ninja

%build
%ninja_build -C build

%install
%ninja_install -C build

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
