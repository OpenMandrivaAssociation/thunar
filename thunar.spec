%define oname Thunar
%define iconname thunar.png

%define major 2
%define apiversion 1
%define libname %mklibname %{name} %{apiversion} %{major}
%define develname %mklibname %{name} -d

Summary:	File manager for the Xfce Desktop Environment
Name:		thunar
Version:	0.8.0
Release:	%mkrel 9
License:	GPL
Group:		Graphical desktop/Xfce
URL:		http://thunar.xfce.org
Source0:	%{oname}-%{version}.tar.bz2
Patch0:		%{oname}-0.8.0-zombies.patch
BuildRequires:	libgdk_pixbuf2.0-devel
BuildRequires:	libxml2-devel >= 2.4.0
BuildRequires:	exo-devel
BuildRequires:	gamin-devel
BuildRequires:	hal-devel
BuildRequires:	perl(XML::Parser)
BuildRequires:	desktop-file-utils
BuildRequires:	dbus-glib-devel
BuildRequires:	desktop-file-utils
BuildRequires:	xfce-panel-devel
Requires:	shared-mime-info >= 0.15
Requires(post):	desktop-file-utils >= 0.10
Requires(postun): desktop-file-utils >= 0.10
Requires:	exo
Requires:	thunar-volman
Obsoletes:	xffm
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
Thunar is a file manager for the Xfce Desktop Environment.

%package -n %{libname}
Summary:	Libraries for the thunar filemanager
Group:		Graphical desktop/Xfce

%description -n %{libname}
Libraries for the thunar filemanager.

%package -n %{develname}
Summary:	Development files for the thunar filemanager
Group:		Development/Other
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Obsoletes:	%mklibname %{name} 1 2 -d

%description -n %{develname}
Development files for the thunar filemanager.

%prep
%setup -qn %{oname}-%{version}
%patch0 -p1

%build
%configure2_5x \
    --sysconfdir=%{_sysconfdir}/X11 \
    --with-volume-manager=hal \
    --enable-dbus \
    --enable-gnome-thumbnailers \
    --enable-startup-notification \
    --enable-exif \
    --enable-pcre

%make

%install
rm -rf %{buildroot}
%makeinstall_std

desktop-file-install \
    --remove-category="System" \
    --add-category="FileManager" \
    --add-only-show-in="XFCE" \
    --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

# Remove unneeded files
rm -f %{buildroot}%{_libdir}/thunarx-1/thunar-uca.la
rm -f %{buildroot}%{_datadir}/doc/Thunar/README.thunarrc
rm -f %{buildroot}%{_datadir}/doc/Thunar/README.volumes

%find_lang %{oname}

%clean
rm -rf %{buildroot}

%post
%{update_menus}
%{update_desktop_database}
%{update_mime_database}
%update_icon_cache hicolor

%postun
%{clean_menus}
%{clean_desktop_database}
%{clean_mime_database}
%clean_icon_cache hicolor

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%files -f %{oname}.lang
%defattr(-,root,root)
%doc AUTHORS ChangeLog FAQ HACKING README THANKS TODO
%doc docs/README.*
%dir %{_sysconfdir}/X11/xdg/Thunar
%dir %{_datadir}/Thunar
%exclude %{_sysconfdir}/X11/xdg/Thunar/uca.xml
%{_bindir}/*
%{_datadir}/applications/*
%{_iconsdir}/hicolor/*
%{_datadir}/pixmaps/*
%{_datadir}/dbus-1/services/*
%{_datadir}/doc/Thunar
%{_datadir}/Thunar/sendto/thunar-sendto-email.desktop
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
%{_mandir}/man1/*
%{_datadir}/thumbnailers/thunar-vfs-font-thumbnailer-1.desktop
%{_libdir}/xfce4/panel-plugins/thunar-tpa
%{_datadir}/xfce4/panel-plugins/thunar-tpa.desktop

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*%{apiversion}.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%dir %{_includedir}/thunar-vfs-1
%{_includedir}/thunar-vfs-1/*
%dir %{_includedir}/thunarx-1
%{_includedir}/thunarx-1/*
%{_libdir}/lib*.so
%{_libdir}/lib*.*a
%{_libdir}/pkgconfig/*.pc
