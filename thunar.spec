%define oname Thunar
%define iconname thunar.png
%define url_ver %(echo %{version} | cut -c 1-3)

%define major 0
%define apiversion 2
%define libname %mklibname %{name} %{apiversion} %{major}
%define develname %mklibname %{name} -d

Summary:	New modern file manager for the Xfce Desktop Environment
Name:		thunar
Version:	1.3.1
Release:	1
License:	GPLv2+
Group:		Graphical desktop/Xfce
URL:		http://thunar.xfce.org
Source0:	http://archive.xfce.org/src/xfce/%{name}/%{url_ver}/%{oname}-%{version}.tar.bz2
Patch12:	Thunar-1.3.1-add-gmodule-link.patch
BuildRequires:	gtk-doc
BuildRequires:	libgdk_pixbuf2.0-devel
BuildRequires:	exo-devel >= 0.7.2
BuildRequires:	gamin-devel
BuildRequires:	perl(XML::Parser)
BuildRequires:	dbus-glib-devel
BuildRequires:	desktop-file-utils
BuildRequires:	xfce4-panel-devel >= 4.9.1
BuildRequires:	libxfce4util-devel >= 4.9.0
BuildRequires:	libxfce4ui-devel >= 4.9.1
BuildRequires:	libpng-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpcre-devel
BuildRequires:	libexif-devel
BuildRequires:	libGConf2-devel
BuildRequires:	libusb-devel
BuildRequires:	xfconf-devel >= 4.9.0
BuildRequires:	pkgconfig(gudev-1.0)
BuildRequires:	libnotify-devel
BuildRequires:	intltool
BuildRequires:	desktop-file-utils
Requires:	shared-mime-info >= 0.15
Requires:	exo
Requires:	thunar-volman
Requires:	%{libname} = %{version}-%{release}
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
%patch12 -p1

%build
# (tpg) needed for patch 12
xdt-autogen

# re-generate it
pushd thunar
exo-csource --name=thunar_window_ui thunar-window-ui.xml > thunar-window-ui.h
popd

%configure2_5x \
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
%{_datadir}/xfce4/panel-plugins/thunar-tpa.desktop
%{_datadir}/gtk-doc/html/thunarx/*

%files -n %{libname}
%{_libdir}/*%{apiversion}.so.%{major}*

%files -n %{develname}
%dir %{_includedir}/thunarx-%{apiversion}
%{_includedir}/thunarx-%{apiversion}/*
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
