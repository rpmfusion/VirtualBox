# This is to prevent certain object files from being stripped.
# FIXME: We would not probably get useful information
# without utilizing optflags (see below)
# TODO: Remove executable bit temporarily to prevent stripping
%define debug_package %{nil}

%define groupname vboxusers

Name:           VirtualBox-OSE
Version:        2.1.4
Release:        3%{?dist}
Summary:        A general-purpose full virtualizer for PC hardware

Group:          Development/Tools
License:        GPLv2 or (GPLv2 and CDDL)
URL:            http://www.virtualbox.org/wiki/VirtualBox
Source0:        http://download.virtualbox.org/virtualbox/%{version}/VirtualBox-%{version}-3-OSE.tar.bz2
Source1:        http://download.virtualbox.org/virtualbox/%{version}/UserManual.pdf
Source3:        %{name}.desktop
Source4:        %{name}-90-vboxdrv.rules
Source5:        %{name}.modules
Source6:        %{name}-guest.modules
Patch6:         %{name}-1.6.4-desktop.patch
Patch7:         %{name}-2.0.2-setup.patch
Patch9:         %{name}-2.1.0-icons.patch
Patch10:        %{name}-2.1.0-32bit.patch
Patch11:        %{name}-2.1.2-gcc44.patch
Patch12:        %{name}-2.1.4-swab.patch
Patch13:        %{name}-2.1.4-libcap.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  kBuild >= 0.1.5-1
BuildRequires:  SDL-devel xalan-c-devel hal-devel
BuildRequires:  dev86 iasl libxslt-devel xerces-c-devel libXcursor-devel libIDL-devel
BuildRequires:  yasm
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  libXmu-devel
BuildRequires:  python-devel
BuildRequires:  desktop-file-utils
BuildRequires:  libcap-devel
%if 0%{?fedora} > 6
BuildRequires:  qt4-devel
%else
BuildRequires:  qt-devel < 1:4
%endif

ExclusiveArch:  %{ix86} x86_64
Requires:       %{name}-kmod = %{version}
Provides:       %{name}-kmod-common = %{version}

Requires(pre):  shadow-utils

%description
A general-purpose full virtualizer and emulator for 32-bit and
64-bit x86 based PC-compatible machines.


%package devel
Summary:        %{name} SDK
Group:          Development/Libraries
Requires:       pyxpcom
Requires:       VirtualBox-OSE = %{version}-%{release}

%description devel
%{name} Software Development Kit.


%package guest
Summary:        %{name} Guest Additions
Group:          System Environment/Base
Requires:       %{name}-kmod = %{version}
Provides:       %{name}-kmod-common = %{version}

%description guest
Tools that utilize kernel modules for supporting integration
with the Host, including file sharing and tracking of mouse pointer
movement.


%package kmodsrc
Summary:        %{name} kernel module source code
Group:          System Environment/Kernel
Requires:       xorg-x11-server-Xorg

%description kmodsrc
Source tree used for building kernel module packages (%{name}-kmod)
which is generated during the build of main package.


%package -n xorg-x11-drv-%{name}
Summary:        X.org X11 %{name} video and mouse driver
Group:          User Interface/X Hardware Support
Requires:       xorg-x11-server-Xorg

%description -n xorg-x11-drv-%{name}
X.org X11 %{name} video and mouse driver.


%prep
%setup -q -n VirtualBox-%{version}_OSE
cp %{SOURCE1} . # PDF User Guide

%patch6 -p1 -b .desktop
%patch7 -p1 -b .setup
%patch9 -p1 -b .icons
%patch10 -p1 -b .32bit
%patch11 -p1 -b .gcc44
%patch12 -p1 -b .swab
%patch13 -p1 -b .libcap

# Copy icons forgotten from distribution, see patch9
cp src/VBox/Frontends/VirtualBox4/images/os_*.png src/VBox/Frontends/VirtualBox/images

# Remove prebuilt binary tools
rm -rf kBuild
rm -rf tools

# CRLF->LF
sed -i 's/\r//' COPYING


%build
./configure --disable-kmods \
%if 0%{?fedora} > 6
        --disable-qt3
%else
        --disable-qt4
%endif

. ./env.sh

# VirtualBox build system installs and builds in the same step,
# not allways looking for the installed files to places they have
# really been installed to. Therefore we do not override any of
# the installation paths, but install the tree with the default
# layout under 'obj' and shuffle files around in %%install.

# FIXME: Utilize optflags. This will probably involve patching of makefiles
# Setting VBOX_GCC_OPT to optflags doesn't use the flags for large part of
# the tree, while preventing required symbols to be generated in .r0 files
kmk KBUILD_VERBOSE=2 TOOL_YASM_AS=yasm VBOX_WITH_REGISTRATION_REQUEST= PATH_INS="$PWD/obj"


%install
rm -rf $RPM_BUILD_ROOT

# The directory layout created below attempts to mimic the one of
# the commercially supported version to minimize confusion

# Directory structure
install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{_libdir}
install -d $RPM_BUILD_ROOT%{_libdir}/virtualbox
install -d $RPM_BUILD_ROOT%{_libdir}/virtualbox/components
%if 0%{?fedora} > 6
install -d $RPM_BUILD_ROOT%{_libdir}/virtualbox/nls
%else
install -d $RPM_BUILD_ROOT%{_libdir}/virtualbox/nls3
%endif
install -d $RPM_BUILD_ROOT%{_datadir}/virtualbox/sdk
install -d $RPM_BUILD_ROOT%{_datadir}/pixmaps
install -d $RPM_BUILD_ROOT%{_prefix}/src/%{name}-kmod-%{version}

# Binaries and Wrapper with Launchers
install -p -m 0755 obj/bin/VBox.sh $RPM_BUILD_ROOT%{_bindir}/VBox
ln -sf VBox $RPM_BUILD_ROOT%{_bindir}/VBoxHeadless
ln -sf VBox $RPM_BUILD_ROOT%{_bindir}/VBoxManage
ln -sf VBox $RPM_BUILD_ROOT%{_bindir}/VBoxSDL
ln -sf VBox $RPM_BUILD_ROOT%{_bindir}/VirtualBox
%if 0%{?fedora} <= 6
ln -sf VBox $RPM_BUILD_ROOT%{_bindir}/VirtualBox3
%endif

install -p -m 0755 -t $RPM_BUILD_ROOT%{_bindir} \
        obj/bin/VBoxTunctl      \
        obj/bin/VBoxBFE

# Components
install -p -m 0755 -t $RPM_BUILD_ROOT%{_libdir}/virtualbox/components \
        obj/bin/components/*

# Lib
install -p -m 0644 -t $RPM_BUILD_ROOT%{_libdir}/virtualbox \
        obj/bin/VBoxDD2.so      \
        obj/bin/VBoxDD.so       \
        obj/bin/VBoxDDU.so      \
        obj/bin/VBoxGuestPropSvc.so \
        obj/bin/VBoxHeadless.so \
        obj/bin/VBoxPython.so   \
        obj/bin/VBoxREM.so      \
%ifnarch x86_64
        obj/bin/VBoxREM32.so    \
        obj/bin/VBoxREM64.so    \
%endif
        obj/bin/VBoxRT.so       \
        obj/bin/VBoxSDL.so      \
        obj/bin/VBoxSettings.so \
        obj/bin/VBoxSharedClipboard.so \
        obj/bin/VBoxSharedFolders.so \
        obj/bin/VBoxVMM.so      \
        obj/bin/VBoxXPCOM.so    \
        obj/bin/VBoxBFE.so      \
%if 0%{?fedora} > 6
        obj/bin/VBoxKeyboard.so \
        obj/bin/VirtualBox.so   \
%else
        obj/bin/VBoxKeyboard3.so \
        obj/bin/VirtualBox3.so  \
%endif
        obj/bin/V*.gc           \
        obj/bin/V*.r0

# For some reason this is needed since 2.1.4.
# Upstream binary distribution doesn't do that
pushd $RPM_BUILD_ROOT%{_libdir}/virtualbox/components
ln -sf ../*.so .
popd

# SetUID root binaries
install -p -m 4755 -t $RPM_BUILD_ROOT%{_libdir}/virtualbox \
        obj/bin/VBoxHeadless    \
        obj/bin/VBoxSDL         \
%if 0%{?fedora} > 6
        obj/bin/VirtualBox
%else
        obj/bin/VirtualBox3
%endif

# Other binaries
install -p -m 0755 -t $RPM_BUILD_ROOT%{_libdir}/virtualbox \
        obj/bin/VBoxManage      \
        obj/bin/VBoxSVC         \
        obj/bin/VBoxXPCOMIPCD

# Language files
%if 0%{?fedora} > 6
install -p -m 0755 -t $RPM_BUILD_ROOT%{_libdir}/virtualbox/nls \
        obj/bin/nls/*
%else
install -p -m 0755 -t $RPM_BUILD_ROOT%{_libdir}/virtualbox/nls3 \
        obj/bin/nls3/*
%endif

# SDK
cp -rp obj/bin/sdk/. $RPM_BUILD_ROOT%{_datadir}/virtualbox/sdk

install -p -m 0755 -t $RPM_BUILD_ROOT%{_datadir}/virtualbox \
        obj/bin/VBoxSysInfo.sh

install -p -m 0644 -t $RPM_BUILD_ROOT%{_datadir}/pixmaps \
        obj/bin/VBox.png

# X.Org drivers
install -m 0755 -D obj/bin/additions/vboxmouse_drv_71.so \
        $RPM_BUILD_ROOT%{_libdir}/xorg/modules/drivers/vboxmouse_drv.so
install -m 0755 -D obj/bin/additions/vboxvideo_drv_71.so \
        $RPM_BUILD_ROOT%{_libdir}/xorg/modules/drivers/vboxvideo_drv.so

# Guest Additions
install -p -m 0755 -t $RPM_BUILD_ROOT%{_bindir} \
        obj/bin/additions/mountvboxsf           \
        obj/bin/additions/vboxadd-timesync      \
        obj/bin/additions/VBoxClient            \
        obj/bin/additions/VBoxControl

# Installation root configuration
install -d $RPM_BUILD_ROOT/%{_sysconfdir}/vbox
echo 'INSTALL_DIR="%{_libdir}/virtualbox"' > $RPM_BUILD_ROOT/%{_sysconfdir}/vbox/vbox.cfg

# Install udev rule
install -p -m 0644 -D %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/90-vboxdrv.rules

# Install modules load script
install -p -m 0755 -D %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/modules/%{name}.modules
install -p -m 0755 -D %{SOURCE6} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/modules/%{name}-guest.modules

# Module Source Code
mkdir -p %{name}-kmod-%{version}
cp -al obj/bin/src/vbox* obj/bin/additions/src/vbox* %{name}-kmod-%{version}
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}-kmod-%{version}
tar --use-compress-program lzma -cf $RPM_BUILD_ROOT%{_datadir}/%{name}-kmod-%{version}/%{name}-kmod-%{version}.tar.lzma \
        %{name}-kmod-%{version}

# Menu entry
desktop-file-install --dir=${RPM_BUILD_ROOT}%{_datadir}/applications \
        --vendor='' src/VBox/Installer/linux/VirtualBox.desktop


%clean
rm -rf $RPM_BUILD_ROOT


%pre
getent group %{groupname} >/dev/null || groupadd -r %{groupname}


%files
%defattr(-,root,root,-)
%{_bindir}/VBox
%{_bindir}/VBoxBFE
%{_bindir}/VBoxHeadless
%{_bindir}/VBoxManage
%{_bindir}/VBoxSDL
%{_bindir}/VBoxTunctl
%{_bindir}/VirtualBox
%if 0%{?fedora} <= 6
%{_bindir}/VirtualBox3
%endif
%{_libdir}/virtualbox
%{_datadir}/pixmaps/*
%dir %{_datadir}/virtualbox
%{_datadir}/virtualbox/VBoxSysInfo.sh
%{_datadir}/applications/*.desktop
%config %{_sysconfdir}/vbox/vbox.cfg
%config %{_sysconfdir}/udev/rules.d/90-vboxdrv.rules
%config %{_sysconfdir}/sysconfig/modules/%{name}.modules
%doc COPYING


%files devel
%defattr(0644,root,root,-)
%{_datadir}/virtualbox/sdk
%doc COPYING


%files guest
%defattr(-,root,root,-)
%{_bindir}/mountvboxsf
%{_bindir}/vboxadd-timesync
%{_bindir}/VBoxClient
%{_bindir}/VBoxControl
%config %{_sysconfdir}/sysconfig/modules/%{name}-guest.modules
%doc COPYING


%files kmodsrc
%defattr(-,root,root,-)
%{_datadir}/%{name}-kmod-%{version}


%files -n xorg-x11-drv-%{name}
%defattr(-,root,root,-)
%{_libdir}/xorg/modules/drivers/*


%changelog
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
