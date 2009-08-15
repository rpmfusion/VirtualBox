%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

# This is to prevent certain object files from being stripped.
# FIXME: We would not probably get useful information
# without utilizing optflags (see below)
# TODO: Remove executable bit temporarily to prevent stripping
%global debug_package %{nil}

# Lots of useless checks
# This will be enabled by default once RPM is built with caps enabled
%bcond_with hardening

%if %with hardening
%define priv_mode %%attr(4755,root,root)
%else
%define priv_mode %%caps(cap_net_raw+ep)
%endif

Name:           VirtualBox-OSE
Version:        3.0.4
Release:        4%{?dist}
Summary:        A general-purpose full virtualizer for PC hardware

Group:          Development/Tools
License:        GPLv2 or (GPLv2 and CDDL)
URL:            http://www.virtualbox.org/wiki/VirtualBox
Source0:        http://dlc.sun.com/virtualbox/%{version}/VirtualBox-%{version}-OSE.tar.bz2
Source1:        http://download.virtualbox.org/virtualbox/%{version}/UserManual.pdf
Source4:        VirtualBox-OSE-90-vboxdrv.rules
Source5:        VirtualBox-OSE-60-vboxadd.rules
Source6:        VirtualBox-OSE.modules
Source7:        VirtualBox-OSE-guest.modules
Source8:        VirtualBox-OSE-vboxresize.desktop
Patch1:         VirtualBox-OSE-2.2.0-noupdate.patch
Patch2:         VirtualBox-OSE-3.0.0-strings.patch
Patch3:         VirtualBox-OSE-3.0.2-libcxx.patch
Patch4:         VirtualBox-OSE-3.0.4-pulse0916.patch
Patch5:         VirtualBox-OSE-3.0.2-xorg17.patch
Patch6:         VirtualBox-OSE-3.0.2-xinput2.patch
Patch7:         VirtualBox-OSE-3.0.4-videodrv6.patch
Patch8:         VirtualBox-OSE-3.0.4-vblank.patch
Patch10:        VirtualBox-OSE-2.2.0-32bit.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  kBuild >= 0.1.5-1
BuildRequires:  SDL-devel xalan-c-devel
BuildRequires:  hal-devel
BuildRequires:  openssl-devel
BuildRequires:  libcurl-devel
BuildRequires:  dev86 iasl libxslt-devel xerces-c-devel libXcursor-devel libIDL-devel
BuildRequires:  yasm
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  libXmu-devel
BuildRequires:  python-devel
BuildRequires:  desktop-file-utils
BuildRequires:  libcap-devel
BuildRequires:  qt4-devel
BuildRequires:  gsoap-devel

# For the X11 module
BuildRequires:  libdrm-devel
BuildRequires:  libpciaccess-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  pixman-devel
BuildRequires:  xorg-x11-proto-devel
BuildRequires:  xorg-x11-server-source

# Plague-specific weirdness
%if 0%{?fedora} > 11
ExclusiveArch:  i686 x86_64
%else %if 0%{?fedora} > 10
ExclusiveArch:  i586 x86_64
%else
ExclusiveArch:  i386 x86_64
%endif

Requires:       %{name}-kmod = %{version}
Provides:       %{name}-kmod-common = %{version}

%description
A general-purpose full virtualizer and emulator for 32-bit and
64-bit x86 based PC-compatible machines.


%package devel
Summary:        %{name} SDK
Group:          Development/Libraries
Requires:       VirtualBox-OSE = %{version}-%{release}
Requires:       python-VirtualBox-OSE = %{version}-%{release}

%description devel
%{name} Software Development Kit.


%package -n python-%{name}
Summary:        Python bindings for %{name}
Group:          Development/Libraries
Requires:       VirtualBox-OSE = %{version}-%{release}

%description -n python-%{name}
Python XPCOM bindings to %{name}.


%package guest
Summary:        %{name} Guest Additions
Group:          System Environment/Base
Requires:       %{name}-kmod = %{version}
Provides:       %{name}-kmod-common = %{version}
Requires:       hal
Requires:       xorg-x11-server-Xorg
Requires:       xorg-x11-xinit
Provides:       xorg-x11-drv-VirtualBox-OSE = %{version}-%{release}
Obsoletes:      xorg-x11-drv-VirtualBox-OSE < %{version}-%{release}

%description guest
Tools that utilize kernel modules for supporting integration
with the Host, including file sharing and tracking of mouse pointer
movement and X.org X11 video and mouse driver.


%package kmodsrc
Summary:        %{name} kernel module source code
Group:          System Environment/Kernel

%description kmodsrc
Source tree used for building kernel module packages (%{name}-kmod)
which is generated during the build of main package.


%prep
%setup -q -n VirtualBox-%{version}_OSE
cp %{SOURCE1} . # PDF User Guide

%patch1 -p1 -b .noupdates
%patch2 -p1 -b .strings
%patch3 -p1 -b .libcxx
%patch4 -p1 -b .pulse0916
%patch5 -p1 -b .xorg17
%patch6 -p1 -b .xinput2
%patch7 -p1 -b .videodrv6
%patch8 -p1 -b .vblank
%patch10 -p1 -b .32bit

# Remove prebuilt binary tools
rm -rf kBuild
rm -rf tools

# CRLF->LF
sed -i 's/\r//' COPYING


%build
./configure --disable-kmods --enable-webservice \
        %{!?with_hardening:--disable-hardening}

. ./env.sh

# VirtualBox build system installs and builds in the same step,
# not allways looking for the installed files to places they have
# really been installed to. Therefore we do not override any of
# the installation paths, but install the tree with the default
# layout under 'obj' and shuffle files around in %%install.

# FIXME: Utilize optflags. This will probably involve patching of makefiles
# Setting VBOX_GCC_OPT to optflags doesn't use the flags for large part of
# the tree, while preventing required symbols to be generated in .r0 files
kmk KBUILD_VERBOSE=2 TOOL_YASM_AS=yasm VBOX_WITH_REGISTRATION_REQUEST= PATH_INS="$PWD/obj" \
        KMK_REVISION=3000 KBUILD_KMK_REVISION=3000


%install
rm -rf $RPM_BUILD_ROOT

# The directory layout created below attempts to mimic the one of
# the commercially supported version to minimize confusion

# Directory structure
install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{_libdir}
install -d $RPM_BUILD_ROOT%{_libdir}/virtualbox
install -d $RPM_BUILD_ROOT%{_libdir}/virtualbox/components
install -d $RPM_BUILD_ROOT%{_libdir}/virtualbox/nls
install -d $RPM_BUILD_ROOT%{_libdir}/dri
install -d $RPM_BUILD_ROOT%{_datadir}/virtualbox/sdk
install -d $RPM_BUILD_ROOT%{_datadir}/pixmaps
install -d $RPM_BUILD_ROOT%{_prefix}/src/%{name}-kmod-%{version}
install -d $RPM_BUILD_ROOT%{python_sitelib}/virtualbox

# Binaries and Wrapper with Launchers
install -p -m 0755 obj/bin/VBox.sh $RPM_BUILD_ROOT%{_bindir}/VBox
ln -sf VBox $RPM_BUILD_ROOT%{_bindir}/VBoxHeadless
ln -sf VBox $RPM_BUILD_ROOT%{_bindir}/VBoxManage
ln -sf VBox $RPM_BUILD_ROOT%{_bindir}/VBoxSDL
ln -sf VBox $RPM_BUILD_ROOT%{_bindir}/VirtualBox

install -p -m 0755 -t $RPM_BUILD_ROOT%{_bindir} \
        obj/bin/VBoxTunctl      \
        obj/bin/VBoxBFE

# Components
install -p -m 0755 -t $RPM_BUILD_ROOT%{_libdir}/virtualbox/components \
        obj/bin/components/*

# Lib
install -p -m 0755 -t $RPM_BUILD_ROOT%{_libdir}/virtualbox \
        obj/bin/*.so

install -p -m 0644 -t $RPM_BUILD_ROOT%{_libdir}/virtualbox \
        obj/bin/V*.gc           \
        obj/bin/V*.r0

# Executabes
install -p -m 0755 -t $RPM_BUILD_ROOT%{_libdir}/virtualbox \
        obj/bin/VBoxHeadless    \
        obj/bin/VBoxSDL         \
        obj/bin/VBoxNetDHCP     \
        obj/bin/VBoxNetAdpCtl   \
        obj/bin/VirtualBox      \
        obj/bin/VBoxManage      \
        obj/bin/VBoxSVC         \
        obj/bin/VBoxXPCOMIPCD   \
        obj/bin/VBoxSysInfo.sh  \
        obj/bin/vboxshell.py    \
        obj/bin/VBoxTestOGL

# Language files
install -p -m 0755 -t $RPM_BUILD_ROOT%{_libdir}/virtualbox/nls \
        obj/bin/nls/*

# SDK
cp -rp obj/bin/sdk/. $RPM_BUILD_ROOT%{_datadir}/virtualbox/sdk
mv $RPM_BUILD_ROOT%{_datadir}/virtualbox/sdk/bindings/xpcom/python/xpcom \
        $RPM_BUILD_ROOT%{python_sitelib}/virtualbox
ln -sf ../../../../../../..%{python_sitelib}/virtualbox/xpcom \
        $RPM_BUILD_ROOT%{_datadir}/virtualbox/sdk/bindings/xpcom/python/xpcom

# Icon
install -p -m 0644 -t $RPM_BUILD_ROOT%{_datadir}/pixmaps \
        obj/bin/VBox.png

# Guest X.Org drivers
# With the xorg17 patch, the _17 driver builds against what's
# actually available for the system, so would probably be a 1.6
# driver when compiled on Fedora 10, despite its name
%global x11_api 17

install -m 0755 -D obj/bin/additions/vboxmouse_drv_%{x11_api}.so \
        $RPM_BUILD_ROOT%{_libdir}/xorg/modules/drivers/vboxmouse_drv.so
install -m 0755 -D obj/bin/additions/vboxvideo_drv_%{x11_api}.so \
        $RPM_BUILD_ROOT%{_libdir}/xorg/modules/drivers/vboxvideo_drv.so

install -m 0755 -D src/VBox/Additions/linux/installer/90-vboxguest.fdi \
        $RPM_BUILD_ROOT%{_datadir}/hal/fdi/policy/20thirdparty/90-vboxguest.fdi

# Guest tools
install -m 0755 -t $RPM_BUILD_ROOT%{_bindir}    \
        obj/bin/additions/mountvboxsf           \
        obj/bin/additions/VBoxService           \
        obj/bin/additions/VBoxClient            \
        obj/bin/additions/VBoxControl

install -m 0755 src/VBox/Additions/x11/Installer/VBoxRandR.sh \
        $RPM_BUILD_ROOT%{_bindir}/VBoxRandR

install -m 0755 -D src/VBox/Additions/x11/Installer/98vboxadd-xclient \
        $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/xinitrc.d/98vboxadd-xclient.sh

install -m 0755 -D src/VBox/Additions/x11/Installer/vboxclient.desktop \
        $RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart/vboxclient.desktop

install -m 0755 -D %{SOURCE8} \
        $RPM_BUILD_ROOT%{_datadir}/gdm/autostart/LoginWindow/vbox-autoresize.desktop

desktop-file-validate $RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart/vboxclient.desktop
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/gdm/autostart/LoginWindow/vbox-autoresize.desktop

# Guest libraries
install -m 0755 -t $RPM_BUILD_ROOT%{_libdir}    \
        obj/bin/additions/VBoxOGL*.so
ln -sf ../VBoxOGL.so $RPM_BUILD_ROOT%{_libdir}/dri/vboxvideo_dri.so


# Installation root configuration
install -d $RPM_BUILD_ROOT/%{_sysconfdir}/vbox
echo 'INSTALL_DIR=%{_libdir}/virtualbox' > $RPM_BUILD_ROOT/%{_sysconfdir}/vbox/vbox.cfg

# Install udev rules
install -p -m 0644 -D %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/90-vboxdrv.rules
install -p -m 0644 -D %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/60-vboxadd.rules

# Install modules load script
install -p -m 0755 -D %{SOURCE6} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/modules/%{name}.modules
install -p -m 0755 -D %{SOURCE7} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/modules/%{name}-guest.modules

# Module Source Code
mkdir -p %{name}-kmod-%{version}
cp -al obj/bin/src/vbox* obj/bin/additions/src/vbox* %{name}-kmod-%{version}
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}-kmod-%{version}
tar --use-compress-program lzma -cf $RPM_BUILD_ROOT%{_datadir}/%{name}-kmod-%{version}/%{name}-kmod-%{version}.tar.lzma \
        %{name}-kmod-%{version}

# Menu entry
desktop-file-install --dir=$RPM_BUILD_ROOT%{_datadir}/applications \
        --remove-key=DocPath --remove-category=X-MandrivaLinux-System \
        --vendor='' src/VBox/Installer/linux/VirtualBox.desktop


%check
# Dear contributor,
#
# If you forget a file when updating to a later version, it's
# not you fault; as you can see, install section is far from
# ideal. This section is meant to make it easier for you to spot
# files you've forgotten to include. Feel free to blacklist
# uninteresting files here.
#
# Not sure if a file is "uninteresting"? See if closed version
# contains it? No? Remove it. Application doesn't run without
# it? Bring it back.

set +o posix
diff -u <((find obj/bin/additions/* -maxdepth 0 -type f    \
                -not -name 'autorun.sh'                 \
                -not -name '*_drv*'                     \
                -exec basename '{}' \;
        find obj/bin/* -maxdepth 0 -type f              \
                -not -name 'tst*'                       \
                -not -name 'SUP*'                       \
                -not -name 'VBox.sh'                    \
                -not -name 'xpidl'                      \
                -not -name 'vboxkeyboard.tar.gz'        \
                -exec basename '{}' \;) |sort) \
        <(find $RPM_BUILD_ROOT%{_libdir}/virtualbox/*   \
                $RPM_BUILD_ROOT%{_bindir}/*             \
                $RPM_BUILD_ROOT%{_libdir}/*OGL*.so      \
                $RPM_BUILD_ROOT%{_datadir}/{pixmaps,applications}/* \
                -maxdepth 0 -type f                     \
                -not -name '*.py[co]'                   \
                -not -name VBoxRandR                    \
                -not -name VBox -exec basename '{}' \; |sort)
set -o posix


%clean
rm -rf $RPM_BUILD_ROOT


%pre devel
# This changed to a symlink from directory, which would cause
# the new package's CPIO payload to fail to unpack unless removed
PYXP=%{_datadir}/virtualbox/sdk/bindings/xpcom/python/xpcom
[ -d "$PYXP" ] && rm -rf "$PYXP"


# Guest additions install the OGL libraries
%post guest -p /sbin/ldconfig
%postun guest -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%{_bindir}/VBox
%{_bindir}/VBoxBFE
%{_bindir}/VBoxHeadless
%{_bindir}/VBoxManage
%{_bindir}/VBoxSDL
%{_bindir}/VBoxTunctl
%{_bindir}/VirtualBox
%dir %{_libdir}/virtualbox
%{_libdir}/virtualbox/*.*
%{_libdir}/virtualbox/components
%{_libdir}/virtualbox/nls
%{_libdir}/virtualbox/VBoxManage
%{_libdir}/virtualbox/VBoxSVC
%{_libdir}/virtualbox/VBoxTestOGL
%{_libdir}/virtualbox/VBoxXPCOMIPCD
%{priv_mode} %{_libdir}/virtualbox/VBoxHeadless
%{priv_mode} %{_libdir}/virtualbox/VBoxSDL
%{priv_mode} %{_libdir}/virtualbox/VBoxNetDHCP
%{priv_mode} %{_libdir}/virtualbox/VBoxNetAdpCtl
%{priv_mode} %{_libdir}/virtualbox/VirtualBox
%{_datadir}/pixmaps/*
%{_datadir}/applications/*.desktop
%config %{_sysconfdir}/vbox/vbox.cfg
%config %{_sysconfdir}/udev/rules.d/90-vboxdrv.rules
%config %{_sysconfdir}/sysconfig/modules/%{name}.modules
%doc COPYING UserManual.pdf


%files devel
%defattr(0644,root,root,0755)
%{_datadir}/virtualbox


%files -n python-%{name}
%defattr(0644,root,root,0755)
%{python_sitelib}/virtualbox


%files guest
%defattr(-,root,root,-)
%{_bindir}/mountvboxsf
%{_bindir}/VBoxClient
%{_bindir}/VBoxControl
%{_bindir}/VBoxService
%{_bindir}/VBoxRandR
%{_libdir}/xorg/modules/drivers/*
%{_libdir}/dri/*
%{_libdir}/VBoxOGL*.so
%{_sysconfdir}/X11/xinit/xinitrc.d/98vboxadd-xclient.sh
%{_sysconfdir}/xdg/autostart/vboxclient.desktop
# %{_datadir}/gdm/autostart/LoginWindow
%exclude %{_datadir}/gdm
%{_datadir}/hal/fdi/policy/20thirdparty/90-vboxguest.fdi
%config %{_sysconfdir}/udev/rules.d/60-vboxadd.rules
%config %{_sysconfdir}/sysconfig/modules/%{name}-guest.modules
%doc COPYING


%files kmodsrc
%defattr(-,root,root,-)
%{_datadir}/%{name}-kmod-%{version}


%changelog
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
