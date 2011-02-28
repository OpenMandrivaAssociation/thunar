%define oname Thunar
%define iconname thunar.png
%define url_ver %(echo %{version} | cut -c 1-3)

%define major 0
%define apiversion 2
%define libname %mklibname %{name} %{apiversion} %{major}
%define develname %mklibname %{name} -d

Summary:	New modern file manager for the Xfce Desktop Environment
Name:		thunar
Version:	1.3.0
Release:	%mkrel 2
License:	GPLv2+
Group:		Graphical desktop/Xfce
URL:		http://thunar.xfce.org
Source0:	http://archive.xfce.org/src/xfce/%{name}/%{url_ver}/%{oname}-%{version}.tar.bz2
#(tpg) http://bugzilla.xfce.org/show_bug.cgi?id=3614
# (tpg) here's the never, and probably better version of the patch https://qa.mandriva.com/show_bug.cgi?id=40230
Patch3:		%{oname}-1.0.1-icons-extension-strip.patch
Patch4:		%{oname}-0.9.0-dont-die-on-dbus-disconnect.patch
# (Anssi 06/2008) fix underlinking:
Patch5:		%{oname}-0.9.0-fix-underlinking.patch
# (tpg) prevent crashing of Thunar when you are drag'n'drop some unhandled formats e.g text
Patch6:		Thunar-1.0.1-dont-crash-on-dnd-unhandled-formats.patch
Patch7:		Thunar-1.0.2-icon-naming-spec-compliance.patch
Patch8:		Thunar-1.0.2-window-maximize.patch
Patch9:		Thunar-1.0.2-fix-sidepanel-width.patch
Patch10:	Thunar-1.0.2-update-cursor-on-delete.patch
Patch11:	Thunar-1.0.2-refilter-tree-hidden-dir.patch
BuildRequires:	libgdk_pixbuf2.0-devel
BuildRequires:	exo-devel >= 0.5.4
BuildRequires:	gamin-devel
BuildRequires:	perl(XML::Parser)
BuildRequires:	dbus-glib-devel
BuildRequires:	desktop-file-utils
BuildRequires:	xfce4-panel-devel >= 4.7.0
BuildRequires:	libxfce4util-devel >= 4.7.1
BuildRequires:	libxfce4ui-devel >= 4.7.1
BuildRequires:	libpng-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpcre-devel
BuildRequires:	libexif-devel
BuildRequires:	libGConf2-devel
BuildRequires:	libusb-devel
BuildRequires:	xfconf-devel >= 4.7.1
BuildRequires:	libgudev-devel
BuildRequires:	libnotify-devel
# for patch 5
BuildRequires:	intltool
BuildRequires:	desktop-file-utils
Requires:	shared-mime-info >= 0.15
Requires:	exo
Requires:	thunar-volman
Requires:	%{libname} = %{version}-%{release}
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
#%patch3 -p1 -b .icon
%patch4 -p1 -b .dbus
#%patch5 -p1
#%patch6 -p1
#%patch7 -p1
#%patch8 -p1 fix
#%patch9 -p1 fix
#%patch10 -p1 fix
#%patch11 -p1 fix

%build

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
rm -rf %{buildroot}
%makeinstall_std

desktop-file-install \
    --remove-key="Encoding" \
    --add-category="FileManager;FileTools" \
    --remove-category="Application" \
    --add-only-show-in="XFCE" \
    --remove-mime-type="x-directory/normal;x-directory/gnome-default-handler" \
    --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/Thunar*

desktop-file-install \
    --add-category="FileManager" \
    --add-only-show-in="XFCE" \
    --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/thunar-settings.desktop

# Remove unneeded files
rm -f %{buildroot}%{_libdir}/thunarx-1/thunar-uca.la
rm -f %{buildroot}%{_datadir}/doc/Thunar/README.thunarrc
rm -f %{buildroot}%{_datadir}/doc/Thunar/README.volumes

# (tpg) this file is in mandriva-xfce-config package
rm -rf %{buildroot}%{_sysconfdir}/xdg/Thunar/uca.xml

%find_lang %{oname}

%clean
rm -rf %{buildroot}

#gw https://qa.mandriva.com/show_bug.cgi?id=61131
%pre
rm -rf %_datadir/doc/Thunar/html/*/images

%files -f %{oname}.lang
%defattr(-,root,root)
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
%{_libdir}/%{oname}/ThunarHelp
%{_libdir}/%{oname}/ThunarBulkRename
%{_libdir}/thunarx-%{apiversion}
%{_libdir}/%{oname}/thunar-sendto-email
%{_mandir}/man1/*
%{_libdir}/xfce4/panel/plugins/*%{name}-*
%{_datadir}/xfce4/panel-plugins/thunar-tpa.desktop
%{_datadir}/gtk-doc/html/thunarx/*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*%{apiversion}.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%dir %{_includedir}/thunarx-%{apiversion}
%{_includedir}/thunarx-%{apiversion}/*
%{_libdir}/lib*.so
%{_libdir}/lib*.*a
%{_libdir}/pkgconfig/*.pc
