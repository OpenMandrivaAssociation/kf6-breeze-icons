Summary:	Breeze icon theme
Name:		breeze-icons
Version:	5.19.0
Release:	1
License:	GPL
Group:		Graphical desktop/KDE
Url:		http://www.kde.org
Source0:	http://download.kde.org/stable/frameworks/%(echo %{version} |cut -d. -f1-2)/%{name}-%{version}.tar.xz
Patch0:		fix-breeze-dark-inheritance.patch
BuildRequires:	cmake(ECM)
BuildRequires:	pkgconfig(Qt5Test)
BuildArch:	noarch

%description
Breeze icon theme. Compliant with FreeDesktop.org naming schema.

%files
%dir %{_iconsdir}/breeze
%dir %{_iconsdir}/breeze-dark
%{_iconsdir}/breeze*/actions
%{_iconsdir}/breeze*/applets
%{_iconsdir}/breeze*/apps
%{_iconsdir}/breeze*/categories
%{_iconsdir}/breeze*/devices
%{_iconsdir}/breeze*/emblems
%{_iconsdir}/breeze*/emotes
%{_iconsdir}/breeze*/mimetypes
%{_iconsdir}/breeze*/places
%{_iconsdir}/breeze*/status
%{_iconsdir}/breeze*/index.theme
# This is needed as hicolor is the fallback for icons
%{_var}/lib/rpm/filetriggers/gtk-icon-cache-breeze.*
%ghost %{_iconsdir}/breeze/icon-theme.cache
%ghost %{_iconsdir}/breeze-dark/icon-theme.cache

#-----------------------------------------------------------------------------

%prep
%setup -q
%apply_patches
%cmake_kde5

%build
%ninja -C build

%install
%ninja_install -C build

# automatic gtk icon cache update on rpm installs/removals
# (see http://wiki.mandriva.com/en/Rpm_filetriggers)
install -d %{buildroot}%{_var}/lib/rpm/filetriggers
cat > %{buildroot}%{_var}/lib/rpm/filetriggers/gtk-icon-cache-breeze.filter << EOF
^./usr/share/icons/breeze/
^./usr/share/icons/breeze-dark/
EOF
cat > %{buildroot}%{_var}/lib/rpm/filetriggers/gtk-icon-cache-breeze.script << EOF
#!/bin/sh
if [ -x /usr/bin/gtk-update-icon-cache ]; then 
  /usr/bin/gtk-update-icon-cache --force --quiet /usr/share/icons/breeze
  /usr/bin/gtk-update-icon-cache --force --quiet /usr/share/icons/breeze-dark
fi
EOF
chmod 755 %{buildroot}%{_var}/lib/rpm/filetriggers/gtk-icon-cache-breeze.script

touch  %{buildroot}%{_datadir}/icons/{breeze,breeze-dark}/icon-theme.cache
