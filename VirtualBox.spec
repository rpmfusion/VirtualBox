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
#global prerel RC4
%global prereltag %{?prerel:_%(awk 'BEGIN {print toupper("%{prerel}")}')}

#if 0%{?fedora} < 20
%global enable_webservice 1
#else
#global enable_webservice 0
#endif

#if 0%{?fedora} < 18
%global enable_docs 1
#else
#global enable_docs 0
#endif

Name:       VirtualBox
Version:    4.2.6
Release:    3%{?prerel:.%{prerel}}%{?dist}
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
%ifarch x86_64
Patch10:     VirtualBox-4.2.0-32bit.patch
%endif
Patch15:    VirtualBox-OSE-4.0.0-makeself.patch
Patch17:    VirtualBox-OSE-4.0.0-beramono.patch
Patch18:    VirtualBox-OSE-4.0.2-aiobug.patch
Patch22:    VirtualBox-OSE-4.1.12-gsoap.patch
Patch23:    VirtualBox-4.2.0-mesa.patch
Patch24:    VirtualBox-4.2.0-VBoxGuestLib.patch
Patch25:    VirtualBox-4.2.0-xorg111.patch
Patch26:    VirtualBox-4.2.4-no-bundles.patch

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
%if 0%{?fedora} >= 18
BuildRequires:  doxygen-latex
BuildRequires:  texlive-collection-fontsrecommended
BuildRequires:  texlive-ec
BuildRequires:  texlive-ucs
BuildRequires:  texlive-tabulary
BuildRequires:  texlive-fancybox
%endif
BuildRequires:  boost-devel
#BuildRequires:  liblzf-devel
BuildRequires:  libxml2-devel
BuildRequires:  libpng-devel
BuildRequires:  zlib-devel
BuildRequires:  device-mapper-devel
#BuildRequires:  glibc(x86-32) glibc-devel(x86-32) libstdc++(x86-32)
#BuildRequires:  glibc.i686 glibc-devel.i686 libstdc++.i686
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

# Remove prebuilt binary tools 
%if 0%{?fedora} < 16
rm -rf kBuild
%endif
rm -rf tools
# Remove bundle X11 sources and some lib sources, before patching.
rm -rf src/VBox/Additions/x11/x11include
rm -rf src/VBox/Additions/x11/x11stubs
rm -rf src/libs/boost-1.37.0/   
#rm -rf src/libs/liblzf-3.4/     
rm -rf src/libs/libxml2-2.6.31/ 
rm -rf src/libs/libpng-1.2.8/   
rm -rf src/libs/zlib-1.2.6/ 

%patch1 -p1 -b .noupdates
%patch2 -p1 -b .strings
%patch3 -p1 -b .libcxx
%patch15 -p1 -b .makeself
%ifarch x86_64
%patch10 -p1 -b .32bit
%endif
%patch17 -p1 -b .beramono
%patch18 -p1 -b .aiobug
%if 0%{?fedora} < 16
%patch22 -p1 -b .gsoap
%endif
%patch23 -p1 -b .mesa
%patch24 -p1 -b .guestlib
%if 0%{?fedora} < 17
%patch25 -p1 -b .xorg111
%endif
%patch26 -p1 -b .nobundles

# CRLF->LF
sed -i 's/\r//' COPYING

# Testings 
#for S in doc/manual/fr_FR/*xml
#do
#    sed -i 's/[&][a-zA-Z0-9]\{2,5\}[;]/ /g' $S
#done

%build
./configure --disable-kmods \
%if %{enable_webservice}
  --enable-webservice \
%endif
%if %{enable_docs}
%else
  --disable-docs \
%endif

#--disable-java
#--disable-xpcom
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
    VBOX_USE_SYSTEM_XORG_HEADERS=1 \
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
%if %{enable_webservice}
ln -s VBox $RPM_BUILD_ROOT%{_bindir}/vboxwebsrv
%endif
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
    obj/bin/VBoxBalloonCtrl \
%if %{enable_webservice}
    obj/bin/vboxwebsrv  \
    obj/bin/webtest     \
%endif
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
# Michael Thayer from Oracle wrote: I have applied the patch [1] I posted so that you 
# can build with VBOX_USE_SYSTEM_XORG_HEADERS=1 set in future to only 
# build the X.Org drivers against the installed system headers.
# also wrote:
# As vboxmouse_drv is not needed at all for X.Org Server 1.7 and later do not
# build it in this case.
# and
# Build using local X.Org headers.  We assume X.Org Server 1.7 or later.
# 
# [1] https://www.virtualbox.org/changeset/43588/vbox

install -m 0755 -D obj/bin/additions/vboxvideo_drv_system.so \
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

# Assign USB devices
# reference for non-systemd OS
#if /sbin/udevadm control --reload-rules >/dev/null 2>&1
#then
#   /sbin/udevadm trigger --subsystem-match=usb >/dev/null 2>&1 || :
#   /sbin/udevadm settle >/dev/null 2>&1 || :
#fi
%if 0%{?fedora} < 18
    systemctl restart udev.service
    systemctl restart udev-trigger.service
    systemctl restart udev-settle.service
%else
    systemctl restart systemd-udevd.service
    systemctl restart systemd-udev-trigger.service
    systemctl restart systemd-udev-settle.service
%endif

# should be in kmod package, not here
/bin/systemctl try-restart fedora-loadmodules.service >/dev/null 2>&1 || :

%preun
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable vboxweb.service > /dev/null 2>&1 || :
    /bin/systemctl stop vboxweb.service > /dev/null 2>&1 || :
fi

%postun
if [ $1 -eq 0 ] ; then
    # Package upgrade, not uninstall
    # Web service
    # Run these because the SysV package being removed won't do them
    /sbin/chkconfig --del vboxweb-service >/dev/null 2>&1 || :
fi

/bin/systemctl daemon-reload >/dev/null 2>&1 || :

/usr/bin/update-desktop-database &>/dev/null || :
/usr/bin/update-mime-database %{_datadir}/mime &>/dev/null || :

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

# Guest additions install
%post guest 
/sbin/ldconfig
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
# should be in kmod package, not here
/bin/systemctl try-restart fedora-loadmodules.service >/dev/null 2>&1 || :
/bin/systemctl enable vboxservice.service >/dev/null 2>&1 || :
/bin/systemctl restart vboxservice.service >/dev/null 2>&1 || :

%preun guest
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable vboxservice.service > /dev/null 2>&1 || :
    /bin/systemctl stop vboxservice.service > /dev/null 2>&1 || :
fi

%postun guest
/sbin/ldconfig
/bin/systemctl daemon-reload >/dev/null 2>&1 || :

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
%if %{enable_webservice}
%{_bindir}/vboxwebsrv
%endif
%{_bindir}/VBoxVRDP
%dir %{_libdir}/virtualbox
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
%if %{enable_webservice}
%{_libdir}/virtualbox/vboxwebsrv
%{_libdir}/virtualbox/webtest
%endif
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
%doc COPYING*
%doc doc/*.*
%if %{enable_docs}
%doc obj/bin/UserManual*.pdf
%endif
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
* Sat Jan 26 2013 Sérgio Basto <sergio@serjux.com> - 4.2.6-3
- fix for rfbz #2662, systemd of F18 changed names of udev services.

* Tue Jan 15 2013 Sérgio Basto <sergio@serjux.com> - 4.2.6-2
- Re enable_docs after add some BuildRequires of new texlive.
- VBoxGuestLib is not need for new X11-xorg, so no compile instead patch source to
  build with system sources.
- Delete source bundles before patching sources and adjustments on the corresponding patches.
- VirtualBox-4.2.0-libcxx.patch minor imporvements.

* Mon Dec 24 2012 Sérgio Basto <sergio@serjux.com> - 4.2.6-1
- New upstream release.
- Fix some changelog dates.

* Sun Dec 02 2012 Sérgio Basto <sergio@serjux.com> - 4.2.4-3
- Use global variables enable_webservice and enable_docs to deal better with enable and disable that.
- Include fr UserManual.pdf and put this docs in /usr/share/docs (the right place) .
- Unbundle sources that aren't used.

* Mon Oct 29 2012 Sérgio Basto <sergio@serjux.com> - 4.2.4-2
- Try load new vbox modules right after install or upgrade.
- Try better reload of vboxservice.service when as guest system.
- Minor improves on systemd upgrade.

* Sat Oct 27 2012 Sérgio Basto <sergio@serjux.com> - 4.2.4-1
- New upstream release.
- Drop patch VirtualBox-4.2.0-xorg17.patch and add VBOX_USE_SYSTEM_XORG_HEADERS=1. Changeset r43588, 
https://www.virtualbox.org/changeset/43588/vbox , allow compile vboxvideo with system headers, and
"As vboxmouse_drv is not needed at all for X.Org Server 1.7 and later do not build it".
- enable-webservice on F17 and lower (stables) and disable-docs on F18 and rawhide, can't buid it
 on F18 and rawhide, new libxslt and new pdflatex problems.

* Sun Sep 30 2012 Sérgio Basto <sergio@serjux.com> - 4.2.0-4
- On F16, need add one xorg header for xorg-x11-server 1.11.x

* Sun Sep 23 2012 Sérgio Basto <sergio@serjux.com> - 4.2.0-3
- Another clean X11 bundle sources (src/VBox/Additions/x11/x11stubs), minor improve on 
VirtualBox-4.2.0-xorg17.patch and split VBoxGuestLib part into VirtualBox-4.2.0-VBoxGuestLib.patch 

* Sat Sep 15 2012 Sérgio Basto <sergio@serjux.com> - 4.2.0-2
- Disable websrv because fails to build on rawhide, temporarily I hope.

* Thu Sep 13 2012 Sérgio Basto <sergio@serjux.com> - 4.2.0-1
- 4.2.0 released
- Rebase and rework VirtualBox-4.2.0-xorg17.patch, add 2 new Definitions: XSERVER_LIBPCIACCESS XORG_VERSION_CURRENT=101300000
- Rename and rework VirtualBox-OSE-4.1.10-mesa.patch 
- Reorganize last 2 patches.
- Revert attempt to remove 32-bits patch.

* Thu Sep 13 2012 Sérgio Basto <sergio@serjux.com> - 4.2.0-0.7.RC4 
- Another try to compile with 32-bits suport on x86_64.

* Sun Sep 09 2012 Sérgio Basto <sergio@serjux.com> - 4.2.0-0.6.RC4
- Update to RC4. 
- Rename 32-bits patch to VirtualBox-4.2.0-32bit.patch
- Drop patch23 to fix ABI/API breakages in X11 1.13, appears fixed in RC4 !
- Compile VBoxGuestLib with X11 sources from system and fix VBoxGuestR3LibRuntimeXF86.cpp. 
- Removes X11 includes from sources (src/VBox/Additions/x11/x11include).

* Fri Sep 07 2012 Sérgio Basto <sergio@serjux.com> - 4.2.0-0.5.RC3
- not drop 32-bit patch, on x86_64 as quick resolution of not have glic-devel.i686 on x86_64.

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

* Sun Jan 15 2012 Sérgio Basto <sergio@serjux.com> - 4.1.8-4
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

* Sat Aug 08 2009 Lubomir Rintel <lkundrak@v3.sk> - 3.0.4-3
- Include VBoxRandR
- Add dri module to guest
- Resize attempts in GDM make SELinux unhappy
- Fix HAL policy file location

* Sat Aug 08 2009 Lubomir Rintel <lkundrak@v3.sk> - 3.0.4-2
- Don't quote INSTALL_DIR in vbox.cfg so that we don't confuse vboxgtk
- Add python- subpackage
- Correct permissions on SDK directories (#754)

* Sat Aug 08 2009 Lubomir Rintel <lkundrak@v3.sk> - 3.0.4-1
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

* Sat Apr 21 2007 Till Maas <opensource till name> - 1.3.8-2
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
