%define capsname Thunar
%define iconname thunar.png

%define version     0.8.0
%define release     2
%define __libtoolize    /bin/true

%define lib_major   1
%define lib_minor   2
%define lib_name    %mklibname thunar %{lib_major}_%{lib_minor}


Summary:    File manager for the Xfce Desktop Environment
Name:       thunar
Version:    %{version}
Release:    %mkrel %{release}
License:    GPL
URL:        http://thunar.xfce.org/
Source0:    %{capsname}-%{version}.tar.bz2
Group:      Graphical desktop/Xfce
BuildRoot:  %{_tmppath}/%{name}-root
#BuildRequires: xfce-mcs-manager-devel >= %{version}
BuildRequires:  libgdk_pixbuf2.0-devel
BuildRequires:  libxml2-devel >= 2.4.0
BuildRequires:  exo-devel
BuildRequires:  ImageMagick
BuildRequires:  gamin-devel
BuildRequires:  hal-devel
BuildRequires:  perl-XML-Parser
BuildRequires:  desktop-file-utils
BuildRequires:  dbus-glib-devel
BuildRequires: desktop-file-utils
Requires:   shared-mime-info >= 0.15
Requires(post):   desktop-file-utils >= 0.10
Requires(postun):   desktop-file-utils >= 0.10
Requires:   exo
Requires:   thunar-volman
Obsoletes: xffm

%description
Thunar is a file manager for the Xfce Desktop Environment.

%package -n %{lib_name}
Summary:        Libraries for the thunar filemanager
Group:          Graphical desktop/Xfce

%description -n %{lib_name}
Libraries for the thunar filemanager.

%package -n %{lib_name}-devel
Summary:        Development files for the thunar filemanager
Group:          Development/Other
Provides:   thunar-devel
Requires:   %{lib_name} = %{version}

%description -n %{lib_name}-devel
Development files for the thunar filemanager.

%prep
%setup -q -n %{capsname}-%{version}


%build
%configure2_5x --sysconfdir=%_sysconfdir/X11
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

mkdir -p %{buildroot}{%{_miconsdir},%{_iconsdir},%{_liconsdir},%{_menudir}}
convert icons/48x48/Thunar.png -geometry 48x48 %{buildroot}%{_liconsdir}/%{iconname}
convert icons/48x48/Thunar.png -geometry 32x32 %{buildroot}%{_iconsdir}/%{iconname}
convert icons/48x48/Thunar.png -geometry 16x16 %{buildroot}%{_miconsdir}/%{iconname}

# Menu
(cd $RPM_BUILD_ROOT
cat > .%{_menudir}/%name <<EOF
?package(%name):\
command="%{_bindir}/%{name}"\
icon="%{iconname}"\
title="Thunar"\
longtitle="Thunar is a filemanager for Xfce."\
needs="x11"\
section="System/File Tools" \
xdg="true"
EOF
)

desktop-file-install --vendor="" \
--remove-category="Application" \
--add-category="X-MandrivaLinux-System-FileTools" \
--add-category="FileManager" \
--add-only-show-in="XFCE" \
--dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*

# Remove unneeded files
rm -f $RPM_BUILD_ROOT%{_libdir}/thunarx-1/thunar-uca.la
rm -f $RPM_BUILD_ROOT%{_datadir}/doc/Thunar/README.thunarrc
rm -f $RPM_BUILD_ROOT%{_datadir}/doc/Thunar/README.volumes

%find_lang %{capsname}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_menus
%update_icon_cache hicolor

%postun
%clean_menus
%clean_icon_cache hicolor

%post -n %{lib_name} -p /sbin/ldconfig

%postun -n %{lib_name} -p /sbin/ldconfig


%files -f %{capsname}.lang
%defattr(-,root,root)
%doc AUTHORS ChangeLog FAQ HACKING README THANKS TODO
%doc docs/README.*
%config(noreplace) %{_sysconfdir}/X11/xdg/Thunar/uca.xml
%{_bindir}/*
%{_datadir}/applications/*
%{_datadir}/icons/*
%{_datadir}/pixmaps/*
%{_datadir}/dbus-1/services/*
%{_datadir}/doc/Thunar
%{_datadir}//Thunar/sendto/thunar-sendto-email.desktop
%{_libdir}/thunarx-1/thunar-uca.so
%{_libdir}/ThunarHelp
%{_libdir}/thunar-vfs-mime-cleaner-1
%{_libdir}/ThunarBulkRename
%{_libdir}/thunarx-1/thunar-apr.*
%{_libdir}/thunarx-1/thunar-sbr.*
%{_libdir}/thunar-sendto-email
%{_libdir}/thunar-vfs-font-thumbnailer-1
%{_libdir}/thunar-vfs-pixbuf-thumbnailer-1
%{_libdir}/thunar-vfs-update-thumbnailers-cache-1
%{_mandir}/man1/Thunar.1.bz2
%{_menudir}/%{name}
%{_miconsdir}/%{iconname}
%{_iconsdir}/%{iconname}
%{_liconsdir}/%{iconname}
%{_datadir}/thumbnailers/thunar-vfs-font-thumbnailer-1.desktop


%files -n %{lib_name}
%defattr(-,root,root)
%{_libdir}/lib*.so.*


%files -n %{lib_name}-devel
%defattr(-,root,root)
%dir %{_includedir}/thunar-vfs-1
%{_includedir}/thunar-vfs-1/*
%dir %{_includedir}/thunarx-1
%{_includedir}/thunarx-1/*
%{_libdir}/lib*.so
%{_libdir}/lib*.*a
%{_libdir}/pkgconfig/*.pc




