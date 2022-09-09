#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	22.08.1
%define		kframever	5.94.0
%define		qtver		5.15.2
%define		kaname		kdenetwork-filesharing
Summary:	KDENetwork file sharing
Name:		ka5-%{kaname}
Version:	22.08.1
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	a553f12ce1fdec3ccf52b7fd1e83bb10
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5Gui-devel >= 5.11.1
BuildRequires:	Qt5Widgets-devel
BuildRequires:	cmake >= 2.8.12
BuildRequires:	gettext-devel
BuildRequires:	kf5-kcoreaddons-devel >= %{kframever}
BuildRequires:	kf5-kdoctools-devel >= %{kframever}
BuildRequires:	kf5-ki18n-devel >= %{kframever}
BuildRequires:	kf5-kio-devel >= %{kframever}
BuildRequires:	kf5-kwidgetsaddons-devel >= %{kframever}
BuildRequires:	ninja
BuildRequires:	qt5-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
kcontrol filesharing config module for SMB.

%description -l pl.UTF-8
Moduł do konfiguracji współdzielenia plików przez SMB.

%prep
%setup -q -n %{kaname}-%{version}

%build
install -d build
cd build
%cmake \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DHTML_INSTALL_DIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	..
%ninja_build

%if %{with tests}
ctest
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{kaname}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_prefix}/libexec/kauth/authhelper
%{_datadir}/dbus-1/system-services/org.kde.filesharing.samba.service
%{_datadir}/dbus-1/system.d/org.kde.filesharing.samba.conf
%{_datadir}/metainfo/org.kde.kdenetwork-filesharing.metainfo.xml
%{_datadir}/polkit-1/actions/org.kde.filesharing.samba.policy
%{_libdir}/qt5/plugins/kf5/propertiesdialog/sambausershareplugin.so
