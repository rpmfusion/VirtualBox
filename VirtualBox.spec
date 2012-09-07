%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

# Standard compiler flags, without:
# -Wall        -- VirtualBox takes care of reasonable warnings very well
# -m32, -m64   -- 32bit code is built besides 64bit on x86_64
# -fexceptions -- R0 code doesn't link against C++ library, no __gxx_personality_v0
%global optflags %(rpm --eval %%optflags |sed 's/-Wall//;s/-m[0-9][0-9]//;s/-fexceptions//')

# In prerelease builds (such as betas), this package has the same
# major version number, while the kernel module abi is not guarranteed
# to be stable. This is so that we force the module update in sync with
# userspace.
%global prerel RC3
%global prereltag %{?prerel:_%(awk 'BEGIN {print toupper("%{prerel}")}')}

Name:       VirtualBox
Version:    4.2.0
Release:    0.4%{?prerel:.%{prerel}}%{?dist}
Summary:    A general-purpose full virtualizer for PC hardware

Group:      Development/Tools
License:    GPLv2 or (GPLv2 and CDDL)
URL:        http://www.virtualbox.org/wiki/VirtualBox
Source0:    http://dlc.sun.com.edgesuite.net/virtualbox/%{version}%{?prereltag}/VirtualBox-%{version}%{?prereltag}.tar.bz2
Source3:    VirtualBox-90-vboxdrv.rules
Source5:    VirtualBox-60-vboxguest.rules
Source6:    VirtualBox.modules
Source7:    VirtualBox-guest.modules
Source8:    VirtualBox-vboxresize.desktop
Source9:    VirtualBox-00-vboxvideo.conf
Source10:   vboxweb.service
Source11:   vboxservice.service
Patch1:     VirtualBox-OSE-4.1.4-noupdate.patch
Patch2:     VirtualBox-4.1.18-strings.patch
Patch3:     VirtualBox-4.2.0-libcxx.patch
Patch5:     VirtualBox-4.2.0-xorg17.patch
Patch15:    VirtualBox-OSE-4.0.0-makeself.patch
Patch17:    VirtualBox-OSE-4.0.0-beramono.patch
Patch18:    VirtualBox-OSE-4.0.2-aiobug.patch
Patch22:    VirtualBox-OSE-4.1.12-gsoap.patch
Patch23:    VirtualBox-OSE-4.1.10-mesa.patch
Patch24:    VirtualBox-4.1.20-x113.patch

%if 0%{?fedora} < 16
BuildRequires:  kBuild >= 0.1.98
%endif
BuildRequires:  SDL-devel xalan-c-devel
BuildRequires:  openssl-devel
BuildRequires:  libcurl-devel
BuildRequires:  dev86 iasl libxslt-devel xerces-c-devel libIDL-devel
BuildRequires:  yasm
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  python-devel
BuildRequires:  desktop-file-utils
BuildRequires:  libcap-devel
BuildRequires:  qt4-devel
BuildRequires:  gsoap-devel
BuildRequires:  xz
BuildRequires:  pam-devel
BuildRequires:  mkisofs
BuildRequires:  java-devel >= 1.6
BuildRequires:  /usr/bin/pdflatex
BuildRequires:  libpng-devel
BuildRequires:  glibc.i686 glibc-devel.i686 libstdc++.i686
#BuildRequires:  /usr/lib/libc.so
#BuildRequires:  /usr/lib/libstdc++.so.6 /lib/libc.so.6 

# For the X11 module
BuildRequires:  libdrm-devel
BuildRequires:  libpciaccess-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libOSMesa-devel
BuildRequires:  pixman-devel
BuildRequires:  xorg-x11-proto-devel
BuildRequires:  xorg-x11-server-source
BuildRequires:  xorg-x11-server-devel
BuildRequires:  libXcursor-devel
BuildRequires:  libXcomposite-devel
BuildRequires:  libXmu-devel

BuildRequires: systemd-units
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

# Plague-specific weirdness
%if 0%{?fedora} > 11 || 0%{?rhel} > 5
ExclusiveArch:  i686 x86_64
%else %if 0%{?fedora} > 10
ExclusiveArch:  i586 x86_64
%else
ExclusiveArch:  i386 x86_64
%endif

Provides:   %{name}-OSE = %{version}-%{release}
Obsoletes:  %{name}-OSE < %{version}-%{release}
Requires:   %{name}-kmod = %{version}
Provides:   %{name}-kmod-common = %{version}-%{release}
Provides:   %{name}-OSE-kmod-common = %{version}-%{release}
Obsoletes:  %{name}-OSE-kmod-common < %{version}-%{release}
Conflicts:  %{name}-guest <= %{version}-%{release}

%description
A general-purpose full virtualizer and emulator for 32-bit and
64-bit x86 based PC-compatible machines.


%package devel
Summary:    %{name} SDK
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
Requires:   python-%{name} = %{version}-%{release}
Provides:   %{name}-OSE-devel = %{version}-%{release}
Obsoletes:  %{name}-OSE-devel < %{version}-%{release}

%description devel
%{name} Software Development Kit.


%package -n python-%{name}
Summary:    Python bindings for %{name}
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
Provides:   python-%{name}-OSE = %{version}-%{release}
Obsoletes:  python-%{name}-OSE < %{version}-%{release}

%description -n python-%{name}
Python XPCOM bindings to %{name}.


%package guest
Summary:    %{name} Guest Additions
Group:      System Environment/Base
Provides:   %{name}-OSE-guest = %{version}-%{release}
Obsoletes:  %{name}-OSE-guest < %{version}-%{release}
Requires:   %{name}-kmod = %{version}
Provides:   %{name}-kmod-common = %{version}-%{release}
Provides:   %{name}-OSE-kmod-common = %{version}-%{release}
Obsoletes:  %{name}-OSE-kmod-common < %{version}-%{release}
Requires:   xorg-x11-server-Xorg
Requires:   xorg-x11-xinit
Provides:   xorg-x11-drv-VirtualBox = %{version}-%{release}
Obsoletes:  xorg-x11-drv-VirtualBox < %{version}-%{release}
Provides:   xorg-x11-drv-VirtualBox-OSE = %{version}-%{release}
Obsoletes:  xorg-x11-drv-VirtualBox-OSE < %{version}-%{release}
%if "%(xserver-sdk-abi-requires 2>/dev/null)"
Requires:   %(xserver-sdk-abi-requires ansic)
Requires:   %(xserver-sdk-abi-requires videodrv)
Requires:   %(xserver-sdk-abi-requires xinput)
%endif
Conflicts:  %{name} <= %{version}-%{release}


%description guest
This is the same that Guest Additions, therefore should only be installed on a guest system.
Tools that utilize kernel modules for supporting integration
with the Host, including file sharing and tracking of mouse pointer
movement and X.org X11 video and mouse driver.


%package kmodsrc
Summary:    %{name} kernel module source code
Group:      System Environment/Kernel
Provides:   %{name}-OSE-kmodsrc = %{version}-%{release}
Obsoletes:  %{name}-OSE-kmodsrc < %{version}-%{release}

%description kmodsrc
Source tree used for building kernel module packages (%{name}-kmod)
which is generated during the build of main package.


%prep
%setup -qn %{name}-%{version}%{prereltag}
find -name '*.py[co]' -delete

%patch1 -p1 -b .noupdates
%patch2 -p1 -b .strings
%patch3 -p1 -b .libcxx
%patch5 -p1 -b .xorg17
%patch15 -p1 -b .makeself
%patch17 -p1 -b .beramono
%patch18 -p1 -b .aiobug
%if 0%{?fedora} < 16
%patch22 -p1 -b .gsoap
%endif
%if 0%{?fedora} > 16
%patch23 -p1 -b .mesa
%endif
%if 0%{?fedora} > 17
%patch24 -p1 -b .x113
%endif

# Remove prebuilt binary tools
%if 0%{?fedora} < 16
rm -rf kBuild
%endif
rm -rf tools
#rm -rf src/VBox/Additions/x11/x11include

# CRLF->LF
sed -i 's/\r//' COPYING


%build
./configure --disable-kmods --enable-webservice
#--disable-java
. ./env.sh

# VirtualBox build system installs and builds in the same step,
# not allways looking for the installed files to places they have
# really been installed to. Therefore we do not override any of
# the installation paths, but install the tree with the default
# layout under 'obj' and shuffle files around in %%install.
kmk %{_smp_mflags} \
    KBUILD_VERBOSE=2 TOOL_YASM_AS=yasm PATH_OUT="$PWD/obj"      \
    VBOX_PATH_APP_PRIVATE=%{_libdir}/virtualbox         \
    VBOX_WITH_REGISTRATION_REQUEST= VBOX_WITH_UPDATE_REQUEST=   \
    VBOX_GCC_OPT="%{optflags}" VBOX_GCC_GC_OPT="%{optflags}"    \
    VBOX_GCC_R0_OPT="%{optflags}" VBOX_GCC_WERR=""          \
    VBOX_XCURSOR_LIBS="Xcursor Xext X11 GL"             \
    VBOX_JAVA_HOME=%{_prefix}/lib/jvm/java \
    VBOX_BUILD_PUBLISHER=_%{?vendor:%(echo %{vendor} \
    | sed -e 's/ //g' | cut -c 1-9)}%{?!vendor:custom}


%install
# The directory layout created below attempts to mimic the one of
# the commercially supported version to minimize confusion

# Directory structure
install -d $RPM_BUILD_ROOT/%{_lib}/security
install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{_sbindir}
install -d $RPM_BUILD_ROOT%{_libdir}
install -d $RPM_BUILD_ROOT%{_libdir}/virtualbox
install -d $RPM_BUILD_ROOT%{_libdir}/virtualbox/components
install -d $RPM_BUILD_ROOT%{_libdir}/virtualbox/nls
install -d $RPM_BUILD_ROOT%{_libdir}/virtualbox/ExtensionPacks
install -d $RPM_BUILD_ROOT%{_libdir}/dri
install -d $RPM_BUILD_ROOT%{_libdir}/virtualbox/sdk
install -d $RPM_BUILD_ROOT%{_datadir}/pixmaps
install -d $RPM_BUILD_ROOT%{_datadir}/mime/packages
install -d $RPM_BUILD_ROOT%{_datadir}/icons
install -d $RPM_BUILD_ROOT%{_prefix}/src/%{name}-kmod-%{version}
install -d $RPM_BUILD_ROOT%{python_sitelib}/virtualbox

# Binaries and Wrapper with Launchers
install -p -m 0755 obj/bin/VBox.sh $RPM_BUILD_ROOT%{_bindir}/VBox
ln -s VBox $RPM_BUILD_ROOT%{_bindir}/VirtualBox
ln -s VBox $RPM_BUILD_ROOT%{_bindir}/virtualbox
ln -s VBox $RPM_BUILD_ROOT%{_bindir}/VBoxManage
ln -s VBox $RPM_BUILD_ROOT%{_bindir}/vboxmanage
ln -s VBox $RPM_BUILD_ROOT%{_bindir}/VBoxSDL
ln -s VBox $RPM_BUILD_ROOT%{_bindir}/vboxsdl
ln -s VBox $RPM_BUILD_ROOT%{_bindir}/VBoxVRDP
ln -s VBox $RPM_BUILD_ROOT%{_bindir}/VBoxHeadless
ln -s VBox $RPM_BUILD_ROOT%{_bindir}/vboxheadless
ln -s VBox $RPM_BUILD_ROOT%{_bindir}/VBoxBalloonCtrl
ln -s VBox $RPM_BUILD_ROOT%{_bindir}/vboxballoonctrl
ln -s VBox $RPM_BUILD_ROOT%{_bindir}/vboxwebsrv
ln -s VBox $RPM_BUILD_ROOT%{_bindir}/VBoxBFE
ln -s VBox $RPM_BUILD_ROOT%{_bindir}/vboxbfe

install -p -m 0755 -t $RPM_BUILD_ROOT%{_bindir} \
    obj/bin/VBoxTunctl  \

# Components
install -p -m 0755 -t $RPM_BUILD_ROOT%{_libdir}/virtualbox/components \
    obj/bin/components/*

# Lib
install -p -m 0755 -t $RPM_BUILD_ROOT%{_libdir}/virtualbox \
    obj/bin/*.so

install -p -m 0644 -t $RPM_BUILD_ROOT%{_libdir}/virtualbox \
    obj/bin/V*.gc       \
    obj/bin/V*.r0       \
    obj/bin/VBoxEFI*.fd

# Documentation
install -p -m 0644 -t $RPM_BUILD_ROOT%{_libdir}/virtualbox \
    obj/bin/UserManual.pdf

# Executables
install -p -m 0755 -t $RPM_BUILD_ROOT%{_libdir}/virtualbox \
    obj/bin/VBoxHeadless    \
    obj/bin/VBoxSDL     \
    obj/bin/VBoxNetDHCP \
    obj/bin/VBoxNetAdpCtl   \
    obj/bin/VirtualBox  \
    obj/bin/VBoxManage  \
    obj/bin/VBoxSVC     \
    obj/bin/VBoxXPCOMIPCD   \
    obj/bin/VBoxSysInfo.sh  \
    obj/bin/vboxshell.py    \
    obj/bin/VBoxTestOGL \
    obj/bin/VBoxExtPackHelperApp \
    obj/bin/vboxwebsrv  \
    obj/bin/VBoxBalloonCtrl \
    obj/bin/webtest     \
    obj/bin/VBoxBFE

# Language files
install -p -m 0755 -t $RPM_BUILD_ROOT%{_libdir}/virtualbox/nls \
    obj/bin/nls/*

# SDK
pushd obj/bin/sdk/installer
VBOX_INSTALL_PATH=%{_libdir}/virtualbox \
    python vboxapisetup.py install --prefix %{_prefix} --root $RPM_BUILD_ROOT
popd
cp -rp obj/bin/sdk/. $RPM_BUILD_ROOT%{_libdir}/virtualbox/sdk
rm -rf $RPM_BUILD_ROOT%{_libdir}/virtualbox/sdk/installer

# Icons
install -p -m 0644 -t $RPM_BUILD_ROOT%{_datadir}/pixmaps \
    obj/bin/VBox.png
#ln -f $RPM_BUILD_ROOT%{_datadir}/pixmaps/{VBox,virtualbox}.png
for S in obj/bin/icons/*
do
    SIZE=$(basename $S)
    install -d $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/$SIZE/{mimetypes,apps}
    install -p -m 0644 $S/* $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/$SIZE/mimetypes
    [ -f $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/$SIZE/mimetypes/virtualbox.png ] && mv \
        $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/$SIZE/mimetypes/virtualbox.png \
        $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/$SIZE/apps/virtualbox.png
done
install -p -m 0644 obj/bin/virtualbox.xml $RPM_BUILD_ROOT%{_datadir}/mime/packages

# Guest X.Org drivers
# With the xorg17 patch, the _17 driver builds against what's
# actually available for the system, so would probably be a 1.6
# driver when compiled on Fedora 10, despite its name
%global x11_api 17

install -m 0755 -D obj/bin/additions/vboxmouse_drv_%{x11_api}.so \
    $RPM_BUILD_ROOT%{_libdir}/xorg/modules/drivers/vboxmouse_drv.so
install -m 0755 -D obj/bin/additions/vboxvideo_drv_%{x11_api}.so \
    $RPM_BUILD_ROOT%{_libdir}/xorg/modules/drivers/vboxvideo_drv.so

# Guest tools
install -m 0755 -t $RPM_BUILD_ROOT%{_sbindir}   \
    obj/bin/additions/mount.vboxsf

install -m 0755 -t $RPM_BUILD_ROOT%{_bindir}    \
    obj/bin/additions/VBoxService       \
    obj/bin/additions/VBoxClient        \
    obj/bin/additions/VBoxControl

# Ideally, Xorg should autodetect this, but for some reason it no longer does
install -m 0644 -D %{SOURCE9} \
    $RPM_BUILD_ROOT%{_sysconfdir}/X11/xorg.conf.d/00-vboxvideo.conf

install -m 0644 -D %{SOURCE10} \
    $RPM_BUILD_ROOT%{_unitdir}/vboxweb.service

install -m 0644 -D %{SOURCE11} \
    $RPM_BUILD_ROOT%{_unitdir}/vboxservice.service

install -m 0755 -D src/VBox/Installer/linux/VBoxCreateUSBNode.sh \
    $RPM_BUILD_ROOT/lib/udev/VBoxCreateUSBNode.sh

install -m 0755 -D src/VBox/Additions/x11/Installer/98vboxadd-xclient \
    $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/xinitrc.d/98vboxadd-xclient.sh

install -m 0644 -D src/VBox/Additions/x11/Installer/vboxclient.desktop \
    $RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart/vboxclient.desktop

install -m 0644 -D %{SOURCE8} \
    $RPM_BUILD_ROOT%{_datadir}/gdm/autostart/LoginWindow/vbox-autoresize.desktop

desktop-file-validate $RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart/vboxclient.desktop
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/gdm/autostart/LoginWindow/vbox-autoresize.desktop

# Guest libraries
install -m 0755 -t $RPM_BUILD_ROOT%{_libdir}    \
    obj/bin/additions/VBoxOGL*.so
ln -sf ../VBoxOGL.so $RPM_BUILD_ROOT%{_libdir}/dri/vboxvideo_dri.so

install -m 0755 -t $RPM_BUILD_ROOT/%{_lib}/security \
    obj/bin/additions/pam_vbox.so

# Installation root configuration
install -d $RPM_BUILD_ROOT/%{_sysconfdir}/vbox
echo 'INSTALL_DIR=%{_libdir}/virtualbox' > $RPM_BUILD_ROOT/%{_sysconfdir}/vbox/vbox.cfg

# Install udev rules
install -p -m 0644 -D %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/90-vboxdrv.rules
install -p -m 0644 -D %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/60-vboxguest.rules

# Install modules load script
install -p -m 0755 -D %{SOURCE6} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/modules/%{name}.modules
install -p -m 0755 -D %{SOURCE7} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/modules/%{name}-guest.modules

# Module Source Code
mkdir -p %{name}-kmod-%{version}
cp -al obj/bin/src/vbox* obj/bin/additions/src/vbox* %{name}-kmod-%{version}
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}-kmod-%{version}
tar --use-compress-program xz -cf $RPM_BUILD_ROOT%{_datadir}/%{name}-kmod-%{version}/%{name}-kmod-%{version}.tar.xz \
    %{name}-kmod-%{version}

# Menu entry
desktop-file-install --dir=$RPM_BUILD_ROOT%{_datadir}/applications \
    --remove-key=DocPath --remove-category=X-MandrivaLinux-System \
    --vendor='' obj/bin/virtualbox.desktop

%post
# Group for USB devices
getent group vboxusers >/dev/null || groupadd -r vboxusers

# Desktop databases
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
/usr/bin/update-desktop-database &>/dev/null || :
/usr/bin/update-mime-database %{_datadir}/mime &>/dev/null || :

# Web service
# Run these because the SysV package being removed won't do them
/sbin/chkconfig --del vboxweb-service >/dev/null 2>&1 || :
/bin/systemctl daemon-reload >/dev/null 2>&1 || :

# Assign USB devices
if /sbin/udevadm control --reload-rules >/dev/null 2>&1
then
#   /sbin/udevadm trigger --subsystem-match=usb >/dev/null 2>&1 || :
#   /sbin/udevadm settle >/dev/null 2>&1 || :
    systemctl restart udev-trigger.service
    systemctl restart udev-settle.service
fi


%preun
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable vboxweb.service > /dev/null 2>&1 || :
    /bin/systemctl stop vboxweb.service > /dev/null 2>&1 || :
fi


%postun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :

/usr/bin/update-desktop-database &>/dev/null || :
/usr/bin/update-mime-database %{_datadir}/mime &>/dev/null || :

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


# Guest additions install the OGL libraries
%post guest 
/sbin/ldconfig
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
/bin/systemctl enable vboxservice.service >/dev/null 2>&1 || :

%preun guest
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable vboxservice.service > /dev/null 2>&1 || :
    /bin/systemctl stop vboxservice.service > /dev/null 2>&1 || :
fi

%postun guest
/sbin/ldconfig
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart vboxservice.service >/dev/null 2>&1 || :
fi


%files
%{_bindir}/VBox
%{_bindir}/vboxballoonctrl
%{_bindir}/VBoxBalloonCtrl
%{_bindir}/vboxbfe
%{_bindir}/VBoxBFE
%{_bindir}/vboxheadless
%{_bindir}/VBoxHeadless
%{_bindir}/vboxmanage
%{_bindir}/VBoxManage
%{_bindir}/vboxsdl
%{_bindir}/VBoxSDL
%{_bindir}/VBoxTunctl
%{_bindir}/virtualbox
%{_bindir}/VirtualBox
%{_bindir}/vboxwebsrv
%{_bindir}/VBoxVRDP
%dir %{_libdir}/virtualbox
%doc %{_libdir}/virtualbox/*.pdf
%{_libdir}/virtualbox/*.[^p]*
%{_libdir}/virtualbox/*.py*
%{_libdir}/virtualbox/components
%{_libdir}/virtualbox/nls
%{_libdir}/virtualbox/VBoxExtPackHelperApp
%{_libdir}/virtualbox/VBoxManage
%{_libdir}/virtualbox/VBoxSVC
%{_libdir}/virtualbox/VBoxTestOGL
%{_libdir}/virtualbox/VBoxXPCOMIPCD
%{_libdir}/virtualbox/VBoxBalloonCtrl
%{_libdir}/virtualbox/vboxwebsrv
%{_libdir}/virtualbox/webtest
%attr(4755,root,root) %{_libdir}/virtualbox/VBoxHeadless
%attr(4755,root,root) %{_libdir}/virtualbox/VBoxSDL
%attr(4755,root,root) %{_libdir}/virtualbox/VBoxBFE
%attr(4755,root,root) %{_libdir}/virtualbox/VBoxNetDHCP
%attr(4755,root,root) %{_libdir}/virtualbox/VBoxNetAdpCtl
%attr(4755,root,root) %{_libdir}/virtualbox/VirtualBox
%{_datadir}/pixmaps/*
%{_datadir}/icons/*
%{_datadir}/mime/*
%{_datadir}/applications/*.desktop
%dir %{_sysconfdir}/vbox
%config %{_sysconfdir}/vbox/vbox.cfg
%config %{_sysconfdir}/udev/rules.d/90-vboxdrv.rules
%config %{_sysconfdir}/sysconfig/modules/%{name}.modules
%doc COPYING
%{_unitdir}/vboxweb.service
/lib/udev/VBoxCreateUSBNode.sh


%files devel
%{_libdir}/virtualbox/sdk


%files -n python-%{name}
%{python_sitelib}/virtualbox
%{python_sitelib}/vboxapi*


%files guest
/%{_lib}/security/pam_vbox.so
%{_sbindir}/mount.vboxsf
%{_bindir}/VBoxClient
%{_bindir}/VBoxControl
%{_bindir}/VBoxService
%{_libdir}/xorg/modules/drivers/*
%{_libdir}/dri/*
%{_libdir}/VBoxOGL*.so
%{_sysconfdir}/X11/xorg.conf.d/00-vboxvideo.conf
%{_sysconfdir}/X11/xinit/xinitrc.d/98vboxadd-xclient.sh
%{_sysconfdir}/xdg/autostart/vboxclient.desktop
%exclude %{_datadir}/gdm
%config %{_sysconfdir}/udev/rules.d/60-vboxguest.rules
%config %{_sysconfdir}/sysconfig/modules/%{name}-guest.modules
%doc COPYING
%{_unitdir}/vboxservice.service


%files kmodsrc
%{_datadir}/%{name}-kmod-%{version}


%changelog
* Fri Sep 07 2012 Sérgio Basto <sergio@serjux.com> - 4.2.0-0.4.RC3
- Also Compile guest drives vboxvideo_drv and vboxmouse_drv with X11 sources from system.
- Fix ABI/API breakages in X11 1.13.

* Mon Sep 03 2012 Sérgio Basto <sergio@serjux.com> - 4.2.0-0.3.RC3
- fix requires kmod, with version with prerealeses.

* Mon Sep 03 2012 Sérgio Basto <sergio@serjux.com> - 4.2.0-0.2.RC3
- vim :retab, reformat all tabs.
- add BR # libstdc++.i686 and libc-devel.i686 for 32-bits
BuildRequires:  /usr/lib/libc.so
BuildRequires:  /usr/lib/libstdc++.so.6 /lib/libc.so.6
- drop 32-bit patch and testmangle patch, no fails. 
- rename and remove some patches
cvs diff: VirtualBox-4.1.20-libcxx.patch was removed, no comparison available
cvs diff: VirtualBox-4.1.20-x113.patch is a new entry, no comparison available
cvs diff: VirtualBox-4.2.0-libcxx.patch is a new entry, no comparison available
cvs diff: VirtualBox-4.2.0-xorg17.patch is a new entry, no comparison available
cvs diff: VirtualBox-OSE-3.2.0-visibility.patch was removed, no comparison available
cvs diff: VirtualBox-OSE-4.0.0-32bit.patch was removed, no comparison available
cvs diff: VirtualBox-OSE-4.1.2-testmangle.patch was removed, no comparison available
cvs diff: VirtualBox-OSE-4.1.2-usblib.patch was removed, no comparison available
cvs diff: VirtualBox-OSE-4.1.4-xorg17.patch was removed, no comparison available

* Mon Sep 03 2012 Sérgio Basto <sergio@serjux.com> - 4.2.0-0.1.RC3
- New major release, devel release of rpms  .
- rebase patches VirtualBox-4.1.20-libcxx.patch, VirtualBox-OSE-4.1.4-xorg17.patch
  and VirtualBox-OSE-4.0.0-32bit.patch

* Sat Sep 01 2012 Sérgio Basto <sergio@serjux.com> - 4.1.20-1
- New upstream release.
- Redo VirtualBox-4.1.20-libcxx.patch
- Patch9 (VirtualBox-OSE-3.2.4-optflags.patch) integrated in Patch3 (VirtualBox-4.1.20-libcxx.patch).
- drop Patch12 (VirtualBox-OSE-3.2.10-noansi.patch) no need anymore.
- drop Patch11 (VirtualBox-OSE-3.2.0-visibility.patch) no need anymore.
- fix rfbz #2416 - /bin/mount.vboxsf must be moved to /sbin/mount.vboxsf
- move files VirtualBox-OSE .rules .modules .desktop and .conf to VirtualBox

* Mon Jul 09 2012 Sérgio Basto <sergio@serjux.com> 4.1.18-2
- Improve some strings suggest on rfbz #1826

* Thu Jun 21 2012 Sérgio Basto <sergio@serjux.com> - 4.1.18-1
- New upstream release.

* Sat Jun 16 2012 Sérgio Basto <sergio@serjux.com> - 4.1.16-5
- Kernel patches just for rawhide, so we don't need recompile kmods.
- Update strings.

* Wed Jun 13 2012 Sérgio Basto <sergio@serjux.com> - 4.1.16-4
- Upstreamed patches to fix compiles with 3.5 kernels, kindly alerted by virtualbox team.

* Sat Jun 09 2012 Sérgio Basto <sergio@serjux.com> - 4.1.16-3
- From Packaging Guidelines, https://fedoraproject.org/wiki/Packaging:Systemd, Packages with systemd
  unit files must put them into %{_unitdir}.
- Install VBoxCreateUSBNode.sh in /lib/udev, and udev rules from upstream.

* Wed May 23 2012 Sérgio Basto <sergio@serjux.com> - 4.1.16-2
- Obsolete also VirtualBox-OSE-kmodsrc.

* Tue May 22 2012 Sérgio Basto <sergio@serjux.com> - 4.1.16-1
- New upstream release.

* Mon May 21 2012 Sérgio Basto <sergio@serjux.com> - 4.1.14-7 
- Customize VBOX_VERSION_STRING. 

* Wed May 16 2012 Sérgio Basto <sergio@serjux.com> - 4.1.14-6
- Bump a release, to build a new tag, one more try.

* Wed May 16 2012 Sérgio Basto <sergio@serjux.com> - 4.1.14-5
- Bump a release, to build a new tag.

* Wed May 16 2012 Sérgio Basto <sergio@serjux.com> - 4.1.14-4
- Rename to VirtualBox, rfbz #1826

* Tue May 1 2012 Sérgio Basto <sergio@serjux.com> - 4.1.14-3
- Review spec with fedora-review 
- Remove requirement for hal for F15
- .desktop, .service and xorg.conf.d/vboxvideo.conf are text files, put chmod 644
- don't try start vboxservice.service, because vboxservice.service depends on kmods, maybe start when
  modules are loaded. 

* Sun Apr 29 2012 Sérgio Basto <sergio@serjux.com> - 4.1.14-2
- Migrating vboxweb-service to a systemd unit file from a SysV initscript 
- Add vboxservice.service systemd unit file in guest package, rfbz #2274. 

* Thu Apr 26 2012 Sérgio Basto <sergio@serjux.com> - 4.1.14-1
- new release
- mesa patch only for F17 or higher

* Fri Apr 13 2012 Sérgio Basto <sergio@serjux.com> - 4.1.12-3
- F17 mesa patch, fix compile fakedri and unbundle part of mesa sources, unbunble mesa source must be tested.

* Fri Apr 13 2012 Sérgio Basto <sergio@serjux.com> - 4.1.12-2
- F15 patch gsoap 2.7 which pkg-config gsoapssl++ --libs don't have -lssl -lcrypto
- F17 kBuild workarround, but still not build in F17,
  https://bugs.freedesktop.org/show_bug.cgi?id=47971 .

* Tue Apr 3 2012 Sérgio Basto <sergio@serjux.com> - 4.1.12-1
- New release.
- drop buildroot
- drop the backported patch.

* Fri Mar 23 2012 Sérgio Basto <sergio@serjux.com> - 4.1.10-1
- New release.
- Upsteam says that java stuff is fiexd , https://www.virtualbox.org/ticket/9848#comment:5
- Upsteam says that have compile fixes for kernel 3.3-rc1 (in changelog).
- backport fix for web-service with newer versions of GSOAP, Changeset 40476 and 40477 in vbox, kindly
  fixed from Frank Mehnert "The real fix can be found in r40476 and r40477. You should be able to 
  apply these fixes to VBox 4.1.10 as well." and add -lssl and -lcrypto by my self.
- drop Patch to allow to build with GCC 4.7

* Tue Jan 15 2012 Sérgio Basto <sergio@serjux.com> - 4.1.8-4
- Patch to allow to build with GCC 4.7
- Try fix usb/udev problem on updates without reboot computer.
- Improves on xorg17 patch, which is the xorg on guest part, we try build with our sources!.
  Currently broken on rawhide with xorg-x11-server-1.11.99.901-2.20120103.fc17. As mentioned on
  https://bugs.freedesktop.org/show_bug.cgi?id=43235, it fix on git, so I hope that will be fix on
  next build of xorg-x11-server.

* Sun Jan 01 2012 Nicolas Chauvet <kwizart@gmail.com> - 4.1.8-3
- Fix vboxweb-service installation

* Sat Dec 24 2011 Sérgio Basto <sergio@serjux.com> - 4.1.8-2
- merge spec 4.0.4 from Lubomir Rintel <lkundrak@v3.sk>, which re-add BuildRequires: hal-devel on
  F-15

* Fri Dec 23 2011 Sérgio Basto <sergio@serjux.com> - 4.1.8-1
- New release.
- remove backported patch, compile_fixes, for reference https://www.virtualbox.org/ticket/9743.

* Mon Dec 12 2011 Sérgio Basto <sergio@serjux.com> - 4.1.6-7
- complete list of commands of VBox command line based on
  src/VBox/Installer/linux/rpm/VirtualBox.tmpl.spec, revert some cleanups.
- add source vboxweb-service to package.

* Sun Dec 11 2011 Sérgio Basto <sergio@serjux.com> - 4.1.6-6
- added compile fixes for kernel 3.2, although guest client still not start with X, now I got a
  segfault, but will help who want try guest client with rawhide.

* Mon Dec 5 2011 Sérgio Basto <sergio@serjux.com> - 4.1.6-5
- Now rawhide needs explicit BuildRequires libpng-devel

* Mon Dec 5 2011 Sérgio Basto <sergio@serjux.com> - 4.1.6-4
- revert change for "bug #1468, conflict symbols have been fixed upstream".

* Sat Dec 3 2011 Sérgio Basto <sergio@serjux.com> - 4.1.6-3
- increase one release number to override my external link.

* Sat Dec 3 2011 Sérgio Basto <sergio@serjux.com> - 4.1.6-2
- bug #1468, conflict symbols have been fixed upstream.
- bug #2052, drop requirement of HAL in Fedora >= 16.
- bug #2040, is also fixed (update to 4.1.6).

* Fri Dec 2 2011 Sérgio Basto <sergio@serjux.com> - 4.1.6-1
- New release
- drop up streamed patch VirtualBox-OSE-4.1.2-vboxpci.patch
- fix strings patch
- add VirtualBox-OSE-add-VBoxExtPackHelperApp.patch bz #1656
- redo xorg17 patch (still need some improvements, I will wait for a new change that break the patch)
- redo noupdate patch.
- disable java binding seems non maintained.
- some cleanups.

* Wed Sep 21 2011 Lubomir Rintel <lkundrak@v3.sk> - 4.1.2-1
- New release
- Assign USB devices to vboxusers
- Add a web service
- Install MIME types for disk images

* Sun Apr 03 2011 Lubomir Rintel <lkundrak@v3.sk> - 4.0.4-1
- New release
- Add requires for particular server ABIs

* Tue Feb 08 2011 Lubomir Rintel <lkundrak@v3.sk> - 4.0.2-2
- Fix build with GCC 4.6

* Fri Feb 04 2011 Lubomir Rintel <lkundrak@v3.sk> - 4.0.2-1
- New release

* Thu Feb 03 2011 Lubomir Rintel <lkundrak@v3.sk> - 4.0.0-1
- New release

* Fri Nov 12 2010 Lubomir Rintel <lkundrak@v3.sk> - 3.2.10-1
- New release

* Sun Aug 8 2010 Lubomir Rintel <lkundrak@v3.sk> - 3.2.8-1
- New release

* Tue Jul 13 2010 Lubomir Rintel <lkundrak@v3.sk> - 3.2.6-2
- Ship with Xorg configuration

* Mon Jul 12 2010 Lubomir Rintel <lkundrak@v3.sk> - 3.2.6-1
- New release, fix build
- Fix compile with GCC 4.5
- Fix acpi compilation with newer iasl

* Thu Jun 17 2010 Lubomir Rintel <lkundrak@v3.sk> - 3.2.4-1
- New release
- Do not use /usr/bin/xargs in module script (Piergiorgio Sartor, #1256)
- No longer blacklist KVM (Nicolas Chauvet, #1280)
- Hypervisor conflicts with guest (Henrique Martins, #1239)

* Wed May 19 2010 Lubomir Rintel <lkundrak@v3.sk> - 3.2.0-1
- Release

* Fri May 14 2010 Lubomir Rintel <lkundrak@v3.sk> - 3.2.0-0.2.beta3
- Beta 3
- Add a release status tag into kernel abi dependency

* Mon May 10 2010 Lubomir Rintel <lkundrak@v3.sk> - 3.2.0-0.2.beta2
- 3.2.0 beta2
- Move pdf documentation to libdir, so that UI can find it

* Wed Apr 28 2010 Lubomir Rintel <lkundrak@v3.sk> - 3.2.0-0.1.beta1
- 3.2.0 beta
- Build i686 on el6

* Fri Mar 26 2010 Lubomir Rintel <lkundrak@v3.sk> - 3.1.6-1
- New upstream release
- Workaround trouble linking with new linker
- modprobe configuration files into right directory (LI Rui Bin)
- Own /etc/vbox (LI Rui Bin)
- Use parallel build
- Attempt to address #1083 by insmodding instead of modprobe

* Tue Feb 16 2010 Lubomir Rintel <lkundrak@v3.sk> - 3.1.4-1
- New upstream, new release :)

* Tue Jan 26 2010 Lubomir Rintel <lkundrak@v3.sk> - 3.1.2-1
- New upstream release

* Mon Nov 30 2009 Lubomir Rintel <lkundrak@v3.sk> - 3.1.0-1
- Upstream release (they do that quite often, huh?)

* Sat Nov 21 2009 Lubomir Rintel <lkundrak@v3.sk> - 3.1.0-0.1.beta2
- Another upstream beta

* Thu Nov 12 2009 Lubomir Rintel <lkundrak@v3.sk> - 3.1.0-0.1.beta1
- Upstream beta release

* Sun Nov 01 2009 Lubomir Rintel <lkundrak@v3.sk> - 3.0.10-1
- Update to newer upstream release
- Fix mixed up source files (Tony Nelson, #881)

* Wed Oct 07 2009 Lubomir Rintel <lkundrak@v3.sk> - 3.0.8-1
- Update to newer upstream
- Fixes SunSolve #268188 security issue

* Thu Sep 10 2009 Lubomir Rintel <lkundrak@v3.sk> - 3.0.6-1
- Bring hardening back, stupid Lubomir
- Update to recent upstream release
- Drop upstreamed patches for Fedora 12 Alpha support

* Sat Aug 22 2009 Lubomir Rintel <lkundrak@v3.sk> - 3.0.4-7
- Correct the path in udev rule and adjust for non-hardening
- Fix build with recent x86_64 glibc

* Thu Aug 20 2009 Lubomir Rintel <lkundrak@v3.sk> - 3.0.4-6
- No exceptions in R0 code, should fix unresolved symbol problem

* Sun Aug 16 2009 Lubomir Rintel <lkundrak@v3.sk> - 3.0.4-5
- Enable debuginfo package
- Correctly use compiler flags
- Make it possible to blacklist our modules
- Blacklist KVM

* Sat Aug 15 2009 Lubomir Rintel <lkundrak@v3.sk> - 3.0.4-4
- Exchange hardening for filesystem capabilities
- Enable web services

* Sun Aug 08 2009 Lubomir Rintel <lkundrak@v3.sk> - 3.0.4-3
- Include VBoxRandR
- Add dri module to guest
- Resize attempts in GDM make SELinux unhappy
- Fix HAL policy file location

* Sun Aug 08 2009 Lubomir Rintel <lkundrak@v3.sk> - 3.0.4-2
- Don't quote INSTALL_DIR in vbox.cfg so that we don't confuse vboxgtk
- Add python- subpackage
- Correct permissions on SDK directories (#754)

* Sun Aug 08 2009 Lubomir Rintel <lkundrak@v3.sk> - 3.0.4-1
- Update to later upstream release
- Re-enable DRI again, fix drm_release crash

* Tue Aug 04 2009 Lubomir Rintel <lkundrak@v3.sk> - 3.0.2-4
- Build for i686
- Fix build with newer PulseAudio
- Don't bundle static libc++, fix build with newer one
- Build Xorg 1.7 drivers, and only them
- Adjust Mouse driver for XInput 2
- Temporarily disable DRI

* Tue Aug 04 2009 Lubomir Rintel <lkundrak@v3.sk> - 3.0.2-3
- Add netadp bmodule (Vlastimil Holer, #744)

* Mon Jul 20 2009 Lubomir Rintel <lkundrak@v3.sk> - 3.0.2-2
- Properly replace the xorg driver package

* Sun Jul 12 2009 Lubomir Rintel <lkundrak@v3.sk> - 3.0.2-1
- New upstream release
- Dropping the upstreamed netfreeze patch

* Fri Jul 10 2009 Lubomir Rintel <lkundrak@v3.sk> - 3.0.0-3
- Fix freeze of guests on network load (upstream ticket/4343)

* Wed Jul 08 2009 Lubomir Rintel <lkundrak@v3.sk> - 3.0.0-2
- Tidy up the filelist check
- Libs need to be executable for the dep generator (#698)

* Fri Jul 03 2009 Jonathan Dieter <jdieter@gmail.com> - 3.0.0-1
- New upstream release

* Thu Jul 02 2009 Lubomir Rintel <lkundrak@v3.sk> - 2.2.4-3
- Enable resize for the login window
- Add the guest udev rules
- Actually install documentation

* Mon Jun 29 2009 Lubomir Rintel <lkundrak@v3.sk> - 2.2.4-2
- They left for beer too early, dicks, so we fix up wbox now
- Make guest additions just work
- Merge xorg stuff with rest of guest additions

* Sun May 31 2009 Lubomir Rintel <lkundrak@v3.sk> - 2.2.4-1
- New upstream release

* Sun May 03 2009 Lubomir Rintel <lkundrak@v3.sk> - 2.2.2-1
- Damnit, another new upstream release! :)
- Improved packaging checks
- Upstream fixed libcap detection, drop patch
- Drop gcc44 patch, upstream supports it now

* Sat Apr 25 2009 Lubomir Rintel <lkundrak@v3.sk> - 2.2.0-1
- New upstream release
- Allow for disabling of hardening to allow group-based vboxdrv control
- Disable automatic updates

* Fri Apr 24 2009 Lubomir Rintel <lkundrak@v3.sk> - 2.1.4-4
- Adjust architecture list for plague

* Sun Apr 12 2009 Lubomir Rintel <lkundrak@v3.sk> - 2.1.4-3
- Fix SDK permissions
- Fix SDK requires

* Mon Mar 30 2009 Lubomir Rintel <lkundrak@v3.sk> - 2.1.4-2
- Fix the swab fix so that we don't break pre-2.6.29 build

* Sat Mar 14 2009 Lubomir Rintel <lkundrak@v3.sk> - 2.1.4-1
- Update to 2.1.4
- Pack and compress the module source code
- Drop vendor from desktop entry

* Sat Mar 14 2009 Lubomir Rintel <lkundrak@v3.sk> - 2.1.2-3
- Fix build with GCC 4.4

* Thu Feb 05 2009 Lubomir Rintel <lkundrak@v3.sk> - 2.1.2-2
- Fix Fedora build, don't attempt to use compat gcc

* Sat Jan 24 2009 Lubomir Rintel <lkundrak@v3.sk> - 2.1.2-1
- New upstream release

* Sun Jan 11 2009 Lubomir Rintel <lkundrak@v3.sk> - 2.1.0-2
- Fix EL-5 panic
- Build on x86_64 (w/o 32bit toolchain)

* Mon Dec 29 2008 Lubomir Rintel <lkundrak@v3.sk> - 2.1.0-1
- New upstream release
- Add guest additions subpackage
- Build QT4 frontend in Fedora

* Mon Sep 29 2008 Lubomir Rintel <lkundrak@v3.sk> - 2.0.2-2
- Fix locales path

* Sat Sep 20 2008 Lubomir Rintel <lkundrak@v3.sk> - 2.0.2-1
- Update to 2.0.2
- Fix vditool library path

* Thu Sep 04 2008 Lubomir Rintel <lkundrak@v3.sk> - 1.6.4-3
- Do the previous change correctly
- Replace occurencies of 'vboxdrv setup'

* Wed Sep 03 2008 Lubomir Rintel <lkundrak@v3.sk> - 1.6.4-2
- Move the VboxDD* libs to a less wrong place

* Tue Sep 02 2008 Lubomir Rintel <lkundrak@v3.sk> - 1.6.4-1
- Remove selinux subpackage
- Pack the generated source tree for kernel module
- Split off SDK
- Install to more-or-less FHS compliant tree

* Sat Mar 08 2008 Till Maas <opensource till name> - 1.5.6-5
- update group management to match the current guidelines

* Sat Mar 08 2008 Till Maas <opensource till name> - 1.5.6-4
- remove bogus %%post script for kernel module removing and loading.
  It worked with dkms, but maybe it was bad anyway.

* Sat Mar 08 2008 Till Maas <opensource till name> - 1.5.6-3
- add requires/provides to be used with kmod package

* Sun Feb 24 2008 Lubomir Kundrak <lkundrak@redhat.com> - 1.5.6-2
- SDL-static not needed, as well as the SDL patch
- do not patch configure for kernel sources, use command line switch

* Sun Feb 24 2008 Till Maas <opensource till name> - 1.5.6-1
- update to new version
- add BR: pulseaudio-libs-devel
- remove uneeded recompiler patch
- remove dkms subpackage (it is now a standalone package)

* Sat Feb 16 2008 Lubomir Kundrak <lkundrak@redhat.com> - 1.5.2-3
- Hacks to build with gcc43, on F8

* Tue Oct 30 2007 Till Maas <opensource till name> - 1.5.2-2
- add support for x86_64

* Tue Oct 30 2007 Till Maas <opensource till name> - 1.5.2-1
- Update to new version

* Wed Oct 03 2007 Till Maas <opensource till name> 
- 1.5.2-0.2.20071003svn5134
- update to devel Version

* Wed Sep 19 2007 Till Maas <opensource till name> 
- 1.5.2-0.1.20070919svn4897
- Update to devel Version that may support Fedora as Guest again
- Make /dev/vboxdrv owned by root instead of vboxusers, because only 
  the group is needed

* Mon Sep 03 2007 Till Maas <opensource till name> - 1.5.0-1
- update to new version
- update License Tag

* Wed Jun 27 2007 Till Maas <opensource till name> - 1.4.0-1
- Update to new version
- Adapt to new kBuild version, which seems to be needed

* Wed Apr 21 2007 Till Maas <opensource till name> - 1.3.8-2
- minor bugfixes in the wrapper script
- rename to VirtualBox-OSE

* Wed Apr 11 2007 Till Maas <opensource till name> - 1.3.8-1
- version bump
- add mkdir $RPM_BUILD_ROOT to %%install to prevent racing condition
- start VBoxSVC with --daemonize
- change source directory in %%prep
- add vditool to wrapper script
- fix path: s/sysconf/sysconfig/ for .modules file
- send rmmod output to /dev/null
- add selinux support
- do not unload the kernel module in preun

* Sun Mar 11 2007 Till Maas <opensource till name> - 1.3.6-3
- new wrapper script, include VBoxSDL
- Use vbox.cfg
- load module in dkms package automatically with sysconfig/modules/virtualbox.modules
- move udev rule to -dkms package
- remove vboxdrv module when deinstalling -dkms package
- add LocalConfig.kmk to make it honour at least some rpm optflags

* Sat Mar 10 2007 Till Maas <opensource till name> - 1.3.6-2
- add COPYING.LIB
- CRLF to LF in COPYING
- add xorg-x11-drv-virtualbox package

* Fri Mar 09 2007 Till Maas <opensource till name> - 1.3.6-1
- Initial release for Fedora, inspired by OpenSuSE spec
