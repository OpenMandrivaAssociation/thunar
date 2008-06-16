%define oname Thunar
%define iconname thunar.png

%define major 2
%define apiversion 1
%define libname %mklibname %{name} %{apiversion} %{major}
%define develname %mklibname %{name} -d

Summary:	New modern file manager for the Xfce Desktop Environment
Name:		thunar
Version:	0.9.0
Release:	%mkrel 10
License:	GPLv2+
Group:		Graphical desktop/Xfce
URL:		http://thunar.xfce.org
Source0:	%{oname}-%{version}.tar.bz2
Patch0:		%{oname}-0.9.0-zombies.patch
Patch1:         %{oname}-0.9.0-missing-audio-cds-for-volman.patch
Patch2:         %{oname}-0.9.0-use-eject-where-necessary.patch
#(tpg) http://bugzilla.xfce.org/show_bug.cgi?id=3614
# (tpg) here's the never, and probably better version of the patch https://qa.mandriva.com/show_bug.cgi?id=40230
Patch3:		%{oname}-0.9.0-icons-extension-strip2.patch
Patch4:		%{oname}-0.9.0-dont-die-on-dbus-disconnect.patch
BuildRequires:	libgdk_pixbuf2.0-devel
BuildRequires:	exo-devel
BuildRequires:	gamin-devel
BuildRequires:	hal-devel
BuildRequires:	perl(XML::Parser)
BuildRequires:	dbus-glib-devel
BuildRequires:	desktop-file-utils
BuildRequires:	xfce4-panel-devel
BuildRequires:	libpng-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpcre-devel
BuildRequires:	libexif-devel
BuildRequires:	libGConf2-devel
BuildRequires:	libusb-devel
Requires:	shared-mime-info >= 0.15
Requires:	exo
Requires:	thunar-volman
Requires(post):	desktop-file-utils >= 0.10
Requires(postun): desktop-file-utils >= 0.10
Obsoletes:	xffm
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
Thunar has been designed from the ground up to be fast and easy-to-use.
Its user interface is clean and intuitive, and does not include any confusing
or useless options. Thunar is fast and responsive with a good start up time
and directory load time. Thunar is accessible using Assistive Technologies and
is fully standards  compliant.

Beside the basic file management features, Thunar includes additional features
that set it ahead of other file managers available for the Unix/Linux desktop
today. For example, Thunar includes a so called Bulk Renamer that allows users
to easily rename multiple files at once using criterions that can be specified
using the available renamer plugins. Probably the most interesting renamer here
is the Audio Tags renamer, which generates new file names based on the tags
present in audio files.

Using the Thunar Extensions Framework it is easy to extend the basic
functionality provided by Thunar to integrate even complex tasks into the file
manager, although the extension framework is still very limited in the 1.0
series, and the 2.0 series will include a way more powerful plugin interface
that allows to adjust virtually every aspect of the file manager. But since
writing extensions for the file manager is still a difficult and time consuming
job, the User Customizable Actions plugin provides users with an easy way to
extend the file and folder context menus with their own custom actions.

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
%patch1 -p0
%patch2 -p1 -b .eject
%patch3 -p1 -b .icon
%patch4 -p1 -b .dbus

%build
%configure2_5x \
%if %mdkversion < 200900
    --sysconfdir=%{_sysconfdir}/X11 \
%endif
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

%if %mdkversion < 200900
%post
%{update_menus}
%{update_desktop_database}
%{update_mime_database}
%update_icon_cache hicolor
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%{clean_desktop_database}
%{clean_mime_database}
%clean_icon_cache hicolor
%endif

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files -f %{oname}.lang
%defattr(-,root,root)
%doc AUTHORS FAQ HACKING README THANKS TODO
%doc docs/README.*
%if %mdkversion < 200900
%dir %{_sysconfdir}/X11/xdg/Thunar
%exclude %{_sysconfdir}/X11/xdg/Thunar/uca.xml
%else
%dir %{_sysconfdir}/xdg/Thunar
%exclude %{_sysconfdir}/xdg/Thunar/uca.xml
%endif
%dir %{_datadir}/Thunar
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
%{_libdir}/thunarx-1
%{_libdir}/thunar-sendto-email
%{_libdir}/thunar-vfs-font-thumbnailer-1
%{_libdir}/thunar-vfs-pixbuf-thumbnailer-1
%{_libdir}/thunar-vfs-update-thumbnailers-cache-1
%{_mandir}/man1/*
%{_datadir}/thumbnailers/thunar-vfs-font-thumbnailer-1.desktop
%{_libdir}/xfce4/panel-plugins/thunar-tpa
%{_datadir}/xfce4/panel-plugins/thunar-tpa.desktop
%{_datadir}/gtk-doc/html/thunar-vfs/*
%{_datadir}/gtk-doc/html/thunarx/*

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
