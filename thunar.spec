%define oname Thunar
%define iconname thunar.png
%define url_ver %(echo %{version} | cut -d. -f 1,2)
%define _disable_rebuild_configure 1

%define major 0
%define apiversion 3
%define gmajor	3.0
%define libname %mklibname %{name} %{apiversion} %{major}
%define girname %mklibname thunarx-gir %{gmajor}
%define develname %mklibname %{name} -d

Summary:	New modern file manager for the Xfce Desktop Environment
Name:		thunar
Version:	1.8.1
Release:	1
License:	GPLv2+
Group:		Graphical desktop/Xfce
URL:		http://thunar.xfce.org
Source0:	http://archive.xfce.org/src/xfce/%{name}/%{url_ver}/%{oname}-%{version}.tar.bz2
BuildRequires:	gtk-doc
BuildRequires:	pkgconfig(gdk-pixbuf-2.0)
BuildRequires:	pkgconfig(exo-2) >= 0.10.0
BuildRequires:	pkgconfig(gamin)
BuildRequires:	perl(XML::Parser)
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	desktop-file-utils
BuildRequires:	pkgconfig(libxfce4panel-2.0) >= 4.11
BuildRequires:	pkgconfig(libxfce4util-1.0) >= 4.10.1
BuildRequires:	pkgconfig(libxfce4ui-2) >= 4.10.0
BuildRequires:	pkgconfig(libpng)
BuildRequires:	jpeg-devel
BuildRequires:	pkgconfig(libpcre)
BuildRequires:	pkgconfig(libexif)
BuildRequires:	pkgconfig(libusb)
BuildRequires:	pkgconfig(libxfconf-0) >= 4.10.0
BuildRequires:	pkgconfig(gudev-1.0)
BuildRequires:	pkgconfig(libnotify)
BuildRequires:	intltool
BuildRequires:	desktop-file-utils
Requires:	shared-mime-info >= 0.15
Requires:	exo
Requires:	thunar-volman
Requires:	%{libname} = %{version}
Requires(post):	desktop-file-utils >= 0.10
Requires(postun): desktop-file-utils >= 0.10
Obsoletes:	xffm

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

%package -n %{girname}
Summary:	GObject Introspection interface library for Thunarx
Group:		System/Libraries
Requires:	%{libname} = %{version}-%{release}

%description -n %{girname}
GObject Introspection interface library for Thunarx.

%package -n %{develname}
Summary:	Development files for the thunar filemanager
Group:		Development/Other
Provides:	%{name}-devel = %{EVRD}
Requires:	%{libname} = %{version}
Obsoletes:	%mklibname %{name} 1 2 -d
Requires:	%{girname} = %{version}-%{release}

%description -n %{develname}
Development files for the thunar filemanager.

%prep
%setup -qn %{oname}-%{version}

%build
# re-generate it
pushd thunar
exo-csource --name=thunar_window_ui thunar-window-ui.xml > thunar-window-ui.h
popd

%configure \
    --enable-dbus \
    --enable-notifications \
    --enable-exif \
    --enable-pcre \
    --enable-gtk-doc \
    --enable-apr-plugin \
    --enable-tpa-plugin \
    --enable-uca-plugin \
    --enable-wallpaper-plugin \
    --enable-gio-unix \
    --enable-gudev

%make

%install
%makeinstall_std

desktop-file-install \
    --remove-key="Encoding" \
    --add-category="FileManager;FileTools" \
    --remove-category="Application" \
    --add-only-show-in="XFCE" \
    --remove-mime-type="x-directory/normal;x-directory/gnome-default-handler" \
    --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/Thunar*

# Remove unneeded files
rm -f %{buildroot}%{_libdir}/thunarx-1/thunar-uca.la
rm -f %{buildroot}%{_datadir}/doc/Thunar/README.thunarrc
rm -f %{buildroot}%{_datadir}/doc/Thunar/README.volumes

# (tpg) this file is in mandriva-xfce-config package
rm -rf %{buildroot}%{_sysconfdir}/xdg/Thunar/uca.xml

%find_lang %{oname} %{oname}.lang

#gw https://qa.mandriva.com/show_bug.cgi?id=61131
%pre
rm -rf %{_datadir}/doc/Thunar/html/*/images

%files -f %{oname}.lang
%doc AUTHORS FAQ HACKING README THANKS TODO
%doc docs/README.*
%dir %{_sysconfdir}/xdg/Thunar
%dir %{_datadir}/Thunar
%dir %{_datadir}/%{oname}/sendto
%{_bindir}/*
%{_datadir}/applications/*
%{_iconsdir}/hicolor/*
%{_datadir}/pixmaps/*
%{_datadir}/dbus-1/services/*
%{_datadir}/doc/Thunar
%{_datadir}/Thunar/sendto/thunar-sendto-email.desktop
%{_libdir}/%{oname}/ThunarBulkRename
%{_libdir}/thunarx-%{apiversion}
%{_libdir}/%{oname}/thunar-sendto-email
%{_mandir}/man1/*
%{_libdir}/xfce4/panel/plugins/*%{name}-*
%{_datadir}/xfce4/panel/plugins/thunar-tpa.desktop
%{_datadir}/metainfo/org.xfce.thunar.appdata.xml
%{_datadir}/polkit-1/actions/org.xfce.thunar.policy
%{_userunitdir}/thunar.service

%files -n %{libname}
%{_libdir}/*%{apiversion}.so.%{major}*

%files -n %{girname}
%{_libdir}/girepository-1.0/Thunarx-%{gmajor}.typelib

%files -n %{develname}
%doc %{_datadir}/gtk-doc/html/thunarx/
%dir %{_includedir}/thunarx-%{apiversion}
%{_includedir}/thunarx-%{apiversion}/*
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gir-1.0/Thunarx-%{gmajor}.gir
