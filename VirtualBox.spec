# Standard compiler flags, without:
# -Wall        -- VirtualBox takes care of reasonable warnings very well
# -m32, -m64   -- 32bit code is built besides 64bit on x86_64
# -fexceptions -- R0 code doesn't link against C++ library, no __gxx_personality_v0
#global optflags %%(rpm --eval %%optflags |sed 's/-Wall//;s/-m[0-9][0-9]//;s/-fexceptions//')
# fix for error: code model kernel does not support PIC mode
#global optflags %%(echo %%{optflags} -fno-pic)
#global optflags %%(echo %%{optflags} | sed 's/-specs=.*cc1 //')

# In prerelease builds (such as betas), this package has the same
# major version number, while the kernel module abi is not guaranteed
# to be stable. This is so that we force the module update in sync with
# userspace.
#global prerel RC1
%global prereltag %{?prerel:_%(awk 'BEGIN {print toupper("%{prerel}")}')}

# Missing build-id in /builddir/build/BUILDROOT/VirtualBox-7.1.6-3.el9.x86_64/usr/lib64/virtualbox/iPxeBaseBin
%undefine _missing_build_ids_terminate_build

#%%if 0%%{?fedora} > 35
    #%%bcond_with webservice
#%%else
%bcond_without webservice
#%%endif
# Now we use upstream pdf
%bcond_with docs
%bcond_without vnc

%if 0%{?rhel} > 9
    %bcond_with 32bits
%else
    %bcond_without 32bits
%endif

%if 0%{?fedora} > 27 || 0%{?rhel} > 8
    %bcond_with guest_additions
%else
    %bcond_without guest_additions
%endif

%if 0%{?fedora}
    %bcond_without system_libtpms
%else
    %bcond_with system_libtpms
%endif

%if 0%{?fedora} || 0%{?rhel} > 8
    %bcond_without dxvk_native
%else
    %bcond_with dxvk_native
%endif

%if 0%{?fedora} > 40
# PyGBase.cpp:225:28: error: ‘PyEval_CallObject’ was not declared in this scope; did you mean ‘PyObject_CallObject’
%bcond_with python3
%else
%bcond_without python3
%endif

Name:       VirtualBox
Version:    7.2.2
Release:    1%{?dist}
Summary:    A general-purpose full virtualizer for PC hardware

License:    GPL-3.0-only AND (GPL-3.0-only OR CDDL-1.0)
URL:        https://www.virtualbox.org/wiki/VirtualBox

ExclusiveArch:  x86_64

Source0:    https://download.virtualbox.org/virtualbox/%{version}%{?prereltag}/VirtualBox-%{version}%{?prereltag}.tar.bz2
Source1:    https://download.virtualbox.org/virtualbox/%{version}%{?prereltag}/UserManual.pdf
Source2:    VirtualBox.appdata.xml
Source3:    VirtualBox-60-vboxdrv.rules
Source4:    vboxdrv.service
Source5:    VirtualBox-60-vboxguest.rules
Source6:    vboxclient.service
Source7:    vboxservice.service
Source8:    96-vboxguest.preset
Source9:    96-vboxhost.preset
Source10:   vboxweb.service
Source20:   os_mageia.png
Source21:   os_mageia_64.png
Source22:   os_mageia_x2.png
Source23:   os_mageia_64_x2.png
Source24:   os_mageia_x3.png
Source25:   os_mageia_64_x3.png
Source26:   os_mageia_x4.png
Source27:   os_mageia_64_x4.png

Patch1:     VirtualBox-7.0.2-noupdate.patch
Patch2:     VirtualBox-6.1.0-strings.patch
Patch3:     VirtualBox-7.1.0-default-to-Fedora.patch
Patch4:     VirtualBox-5.1.0-lib64-VBox.sh.patch
Patch5:     VirtualBox-python3.13.patch

# from Mageia
Patch50:    VirtualBox-7.0.18-update-Mageia-support.patch
# from Fedora
Patch60:    VirtualBox-7.0.2-xclient-cleanups.patch
# from Arch
#Patch70:    009-properly-handle-i3wm.patch
#from Gentoo
Patch80:    029_virtualbox-7.1.4_C23.patch
Patch82:    0001-Print-qt6-version-required.patch

BuildRequires:  gcc-c++
BuildRequires:  kBuild >= 0.1.9998.r3674
BuildRequires:  openssl-devel
BuildRequires:  libcurl-devel
BuildRequires:  iasl
BuildRequires:  libxslt-devel
BuildRequires:  yasm
BuildRequires:  alsa-lib-devel
#BuildRequires:  opus-devel
BuildRequires:  pulseaudio-libs-devel
%if %{with python3}
BuildRequires:  python-rpm-macros
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
%endif
BuildRequires:  desktop-file-utils
BuildRequires:  libcap-devel
BuildRequires:  pkgconfig(Qt6Core)
BuildRequires:  pkgconfig(Qt6Help)
BuildRequires:  pkgconfig(Qt6Scxml)

%if %{with webservice}
BuildRequires:  gsoap-devel
%endif
BuildRequires:  pam-devel
BuildRequires:  genisoimage
#BuildRequires:  java-devel
%if %{with docs}
BuildRequires:  /usr/bin/pdflatex
BuildRequires:  docbook-dtds
BuildRequires:  docbook-style-xsl
BuildRequires:  doxygen-latex
BuildRequires:  texlive-collection-fontsrecommended
BuildRequires:  texlive-ec
BuildRequires:  texlive-ucs
BuildRequires:  texlive-tabulary
BuildRequires:  texlive-fancybox
%endif
BuildRequires:  boost-devel
BuildRequires:  liblzf-devel
BuildRequires:  libxml2-devel
BuildRequires:  libpng-devel
BuildRequires:  xz-devel
BuildRequires:  zlib-devel
BuildRequires:  device-mapper-devel
BuildRequires:  libvpx-devel
BuildRequires:  makeself
#For fixrom.pl
BuildRequires:  perl(FindBin)
BuildRequires:  perl(lib)

# for 32bits on 64
%if %{with 32bits}
%ifarch x86_64
# or BuildRequires: glibc32
BuildRequires:  glibc-devel(x86-32)
BuildRequires:  libgcc(x86-32)
#BuildRequires:  libstdc++-static(x86-32)
%endif
%endif
BuildRequires:  libstdc++-static

# For the X11 module
BuildRequires:  libdrm-devel
BuildRequires:  xorg-x11-proto-devel
BuildRequires:  libXcomposite-devel
BuildRequires:  libXcursor-devel
BuildRequires:  libXdamage-devel
BuildRequires:  libXinerama-devel
BuildRequires:  libXmu-devel
BuildRequires:  libX11-devel
BuildRequires:  libXrandr-devel
BuildRequires:  libXt-devel
BuildRequires:  mesa-libEGL-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libGLU-devel
%if %{with vnc}
BuildRequires:  libvncserver-devel
%endif
%if %{with system_libtpms}
BuildRequires:	pkgconfig(libtpms)
%endif
BuildRequires:	pkgconfig(ogg)
BuildRequires:	pkgconfig(vorbis)
%if %{with dxvk_native}
BuildRequires:	glslang
# build fails with system dxvk_native
#BuildRequires:  dxvk-native-devel
%endif

%{?systemd_requires}
BuildRequires: systemd

Requires:   %{name}-server%{?isa} = %{version}

%description
VirtualBox is a powerful x86 and AMD64/Intel64 virtualization product for
enterprise as well as home use. Not only is VirtualBox an extremely feature
rich, high performance product for enterprise customers, it is also the only
professional solution that is freely available as Open Source Software under
the terms of the GNU General Public License (GPL) version 2.

Presently, VirtualBox runs on Windows, Linux, Macintosh, and Solaris hosts and
supports a large number of guest operating systems including but not limited to
Windows (NT 4.0, 2000, XP, Server 2003, Vista, Windows 7, Windows 8, Windows
10), DOS/Windows 3.x, Linux (2.4, 2.6, 3.x and 4.x), Solaris and OpenSolaris,
OS/2, and OpenBSD.


%package server
Summary:    Core part (host server) for %{name}
Group:      Development/Tools
Requires:   %{name}-kmod = %{version}
Requires:   hicolor-icon-theme
Provides:   %{name}-kmod-common = %{version}-%{release}
%if ! %{with python3}
Obsoletes:   python%{python3_pkgversion}-%{name}%{?isa} < %{version}-%{release}
%endif

%description server
%{name} without Qt GUI part.


%package webservice
Summary:        WebService GUI part for %{name}
Group:          System/Emulators/PC
Requires:       %{name}-server%{?isa} = %{version}

%description webservice
webservice GUI part for %{name}.

%package vnc
Summary:        VNC desktop sharing
Group:          System/Emulators/PC
Requires:       %{name} = %{version}
%description vnc
Virtual Network Computing (VNC) is a graphical desktop sharing system that uses the Remote Frame Buffer
protocol (RFB) to remotely control another computer. When this optional feature is desired, it is installed
as an "extpack" for VirtualBox. The implementation is licensed under GPL.

%package devel
Summary:    %{name} SDK
Group:      Development/Libraries
Requires:   %{name}-server%{?isa} = %{version}-%{release}
%if %{with python3}
Requires:   python%{python3_pkgversion}-%{name}%{?isa} = %{version}-%{release}
%endif

%description devel
%{name} Software Development Kit.


%package -n python%{python3_pkgversion}-%{name}
Summary:    Python3 bindings for %{name}
Group:      Development/Libraries
Requires:   %{name}-server%{?_isa} = %{version}-%{release}
%py_provides python%{python3_pkgversion}-%{name}

%description -n python%{python3_pkgversion}-%{name}
Python3 XPCOM bindings to %{name}.

%package guest-additions
Summary:    %{name} Guest Additions
Group:      System Environment/Base
Requires:   %{name}-kmod = %{version}
Provides:   %{name}-kmod-common = %{version}-%{release}
Requires:   xorg-x11-server-Xorg
Requires:   xorg-x11-xinit
Provides:   %{name}-guest = %{version}-%{release}
Obsoletes:  %{name}-guest < %{version}-%{release}
%if "%(xserver-sdk-abi-requires 2>/dev/null)"
Requires:   %(xserver-sdk-abi-requires ansic)
Requires:   %(xserver-sdk-abi-requires videodrv)
Requires:   %(xserver-sdk-abi-requires xinput)
%endif


%description guest-additions
This package replaces the application of Virtualbox's own methodology to
install Guest Additions (in menu: Devices | Insert Guest Additions CD-image file).
This subpackage provides tools that use kernel modules which support better
integration of VirtualBox guests with the Host, including file sharing, clipboard sharing,
video and mouse driver, USB and webcam proxy and Seamless mode.


%package kmodsrc
Summary:    %{name} kernel module source code
Group:      System Environment/Kernel
BuildArch:  noarch

%description kmodsrc
Source tree used for building kernel module packages (%{name}-kmod)
which is generated during the build of main package.


%prep
%setup -q -n %{name}-%{version}%{?prereltag}
# add Mageia images
cp -a %{SOURCE20} %{SOURCE21} src/VBox/Frontends/VirtualBox/images/
cp -a %{SOURCE22} %{SOURCE23} src/VBox/Frontends/VirtualBox/images/x2/
cp -a %{SOURCE24} %{SOURCE25} src/VBox/Frontends/VirtualBox/images/x3/
cp -a %{SOURCE26} %{SOURCE27} src/VBox/Frontends/VirtualBox/images/x4/

# Remove prebuilt binary tools
find -name '*.py[co]' -delete
rm -r src/VBox/Additions/WINNT
rm -r src/VBox/Additions/os2
rm -r kBuild/
rm -r tools/
# Remove bundle X11 sources and some lib sources, before patching.
rm -r src/VBox/Additions/x11/x11include/
rm -r src/VBox/Additions/3D/mesa/mesa-24.0.2/
# wglext.h has typedefs for Windows-specific extensions
#rm include/VBox/HostServices/wglext.h
# src/VBox/GuestHost/OpenGL/include/GL/glext.h have VBOX definitions
#rm -r src/VBox/GuestHost/OpenGL/include/GL
rm -r src/VBox/Runtime/r3/darwin
rm -r src/VBox/Runtime/r0drv/darwin
rm -r src/VBox/Runtime/darwin

rm -r src/libs/liblzf-3.*/
rm -r src/libs/libpng-1.6.*/
rm -r src/libs/libxml2-2.*/
rm -r src/libs/openssl-3.*/
rm -r src/libs/zlib-1.3.*/
rm -r src/libs/curl-8.*/
rm -r src/libs/libvorbis-1.3.*/
rm -r src/libs/libogg-1.3.*/
rm -r src/libs/liblzma-5.*/
#rm -r src/libs/libslirp-4.*/
%if %{with system_libtpms}
rm -r src/libs/libtpms-0.10.*/
%endif
%if %{with dxvk_native}
#rm -r src/libs/dxvk-2.*/
%endif
#rm -r src/libs/softfloat-3e/

%patch -P 1 -p1 -b .noupdates
%patch -P 2 -p1 -b .strings
%patch -P 3 -p1 -b .default_os_fedora
%patch -P 4 -p1 -b .lib64-VBox.sh
#%%patch -P 5 -p1 -b .py3.13

%patch -P 50 -p1 -b .mageia-support
%patch -P 60 -p1 -b .xclient
#%%patch -P 70 -p1 -b .i3wm
%patch -P 80 -p1 -b .c23
%patch -P 82 -p1 -b qt6_version


%build
./configure --disable-kmods \
%if %{with webservice}
  --enable-webservice \
%endif
%if %{with vnc}
  --enable-vnc \
%endif
%if %{without docs}
  --disable-docs \
%endif
%if %{without python3}
  --disable-python \
%endif
%if %{without 32bits}
  --disable-vmmraw \
%endif
  --disable-java \
  --disable-sdl

%if !%{with docs}
cp %{SOURCE1} UserManual.pdf
%endif

#--enable-libogg --enable-libvorbis
#--enable-vde
#--build-headless --build-libxml2
#--disable-xpcom
. ./env.sh
umask 0022

# The function VBoxExtPackIsValidEditionString only allows uppercase characters (A-Z) in the suffix.
%if "%{vendor}" == "RPM Fusion"
%global publisher _RPMFUSION
%else
%global publisher _%{?vendor:%(echo "%{vendor}" | \
    sed -e 's/[^[:alnum:]]//g; s/FedoraCopruser//' | cut -c -9 | tr '[:lower:]' '[:upper:]')}%{?!vendor:CUSTOM}
%endif

# VirtualBox build system installs and builds in the same step,
# not always looking for the installed files in places they have
# really been installed to. Therefore we do not override any of
# the installation paths
kmk %{_smp_mflags}                                             \
    KBUILD_VERBOSE=2                                           \
    TOOL_YASM_AS=yasm                                          \
    VBOX_PATH_APP_PRIVATE=%{_libdir}/virtualbox \
    VBOX_PATH_APP_PRIVATE_ARCH=%{_libdir}/virtualbox    \
    VBOX_PATH_APP_DOCS=%{_docdir}/VirtualBox    \
    VBOX_WITH_ORIGIN=                                   \
    VBOX_WITH_RUNPATH=%{_libdir}/virtualbox             \
    VBOX_GUI_WITH_SHARED_LIBRARY=1                      \
    VBOX_PATH_SHARED_LIBS=%{_libdir}/virtualbox         \
    VBOX_WITH_VBOX_IMG=1 \
    VBOX_WITH_VBOXIMGMOUNT=1 \
    VBOX_WITH_UNATTENDED=1  \
    VBOX_USE_SYSTEM_XORG_HEADERS=1                             \
    VBOX_USE_SYSTEM_GL_HEADERS=1                               \
    VBOX_NO_LEGACY_XORG_X11=1                                  \
    SDK_VBoxLibPng_INCS=/usr/include/libpng16                 \
    SDK_VBoxLibXml2_INCS=/usr/include/libxml2                 \
    SDK_VBoxLzf_LIBS="lzf"                                    \
    SDK_VBoxLzf_INCS="/usr/include/liblzf"                    \
    SDK_VBoxOpenSslStatic_INCS="/usr/include/openssl"                                   \
    SDK_VBoxOpenSslStatic_LIBS="ssl crypto"                         \
    SDK_VBoxLibLzma_INCS=""                                 \
    SDK_VBoxZlib_INCS=""                                      \
%{?with_system_libtpms:   SDK_VBOX_LIBTPMS_INCS="/usr/include/libtpms"}  \
    SDK_VBoxLibVorbis_INCS="/usr/include/vorbis"                 \
    SDK_VBoxLibOgg_INCS="/usr/include/ogg"                       \
%{!?with_dxvk_native: VBOX_WITH_DXVK= }             \
%{?with_docs:   VBOX_WITH_DOCS=1 }                             \
    VBOX_JAVA_HOME=%{_prefix}/lib/jvm/java  \
    VBOX_WITH_REGISTRATION_REQUEST=         \
    VBOX_WITH_UPDATE_REQUEST=               \
    VBOX_WITH_TESTCASES=                    \
    VBOX_BUILD_PUBLISHER=%{publisher}

%if %{with vnc}
echo "build VNC extension pack"
# tar must use GNU, not POSIX, format here
# sed -i 's/tar /tar --format=gnu /' src/VBox/ExtPacks/VNC/Makefile.kmk
kmk -C src/VBox/ExtPacks/VNC packing KBUILD_VERBOSE=2
%endif

#    VBOX_GCC_WERR= \
#    TOOL_GCC3_CFLAGS="%{optflags}"   \
#    TOOL_GCC3_CXXFLAGS="%{optflags}" \
#    VBOX_GCC_OPT="%{optflags}" \
#    VBOX_WITH_CLOUD_NET:=
#    VBOX_WITH_VBOXSDL=1     \
#    VBoxSDL_INCS += \
#    VBoxSDL_LIBS
#    VBOX_WITH_SYSFS_BY_DEFAULT=1 \
#    VBOX_WITHOUT_PRECOMPILED_HEADERS=1      \
#    VBOX_XCURSOR_LIBS="Xcursor Xext X11 GL"             \
#    VBOX_DOCBOOK_WITH_LATEX    := 1
#    VBOX_WITH_EXTPACK_VBOXDTRACE=           \
#    VBOX_WITH_VBOXBFE :=
#    VBOX_PATH_DOCBOOK_DTD := /usr/share/xml/docbook/schema/dtd/4/


# doc/manual/fr_FR/ missing man_VBoxManage-debugvm.xml and man_VBoxManage-extpack.xml
#    VBOX_WITH_DOCS_TRANSLATIONS=1 \
# we can't build CHM DOCS we need hhc.exe which is not in source and we need
# also install wine:
# wine: cannot find
# '/builddir/build/BUILD/VirtualBox-5.1.6/tools/win.x86/HTML_Help_Workshop/v1.3//hhc.exe'
#    VBOX_WITH_DOCS_CHM=1 \
#    VBOX_WITH_ADDITION_DRIVERS = \
#    VBOX_WITH_INSTALLER = 1 \
#    VBOX_WITH_LINUX_ADDITIONS = 1 \
#    VBOX_WITH_X11_ADDITIONS = 1 \
#VBOX_WITH_LIGHTDM_GREETER=1 \


%install
# The directory layout created below attempts to mimic the one of
# the commercially supported version to minimize confusion

# Directory structure
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_libdir}
install -d %{buildroot}%{_libdir}/virtualbox
install -d %{buildroot}%{_libdir}/virtualbox/components
install -d %{buildroot}%{_libdir}/virtualbox/UnattendedTemplates
install -d %{buildroot}%{_libdir}/virtualbox/nls
install -d %{buildroot}%{_libdir}/virtualbox/ExtensionPacks
install -d %{buildroot}%{_libdir}/virtualbox/sdk
install -d %{buildroot}%{_datadir}/pixmaps
install -d %{buildroot}%{_metainfodir}
install -d %{buildroot}%{_datadir}/mime/packages
install -d %{buildroot}%{_datadir}/icons
install -d %{buildroot}%{_prefix}/src/%{name}-kmod-%{version}

# Libs
install -p -m 0755 -t %{buildroot}%{_libdir}/virtualbox \
    out/linux.*/release/bin/*.so

install -p -m 0644 -t %{buildroot}%{_libdir}/virtualbox \
    out/linux.*/release/bin/VBoxEFI*.fd \
    out/linux.*/release/bin/*.r0

# Binaries
install -p -m 0755 out/linux.*/release/bin/VBox.sh %{buildroot}%{_bindir}/VBox

# Executables
install -p -m 0755 -t %{buildroot}%{_libdir}/virtualbox \
    out/linux.*/release/bin/VirtualBox  \
    out/linux.*/release/bin/VBoxHeadless    \
    out/linux.*/release/bin/VBoxNetDHCP \
    out/linux.*/release/bin/VBoxNetNAT \
    out/linux.*/release/bin/VBoxNetAdpCtl   \
    out/linux.*/release/bin/VBoxVolInfo \
    out/linux.*/release/bin/SUPInstall \
    out/linux.*/release/bin/SUPLoggerCtl \
    out/linux.*/release/bin/SUPUninstall \
    out/linux.*/release/bin/VBoxAutostart \
    out/linux.*/release/bin/VBoxBalloonCtrl \
    out/linux.*/release/bin/VBoxExtPackHelperApp \
    out/linux.*/release/bin/VBoxManage  \
    out/linux.*/release/bin/VBoxSVC     \
    out/linux.*/release/bin/VBoxVMMPreload \
    out/linux.*/release/bin/VBoxSysInfo.sh  \
    out/linux.*/release/bin/vboxweb-service.sh \
%if %{with python3}
    out/linux.*/release/bin/vboxshell.py    \
%endif
    out/linux.*/release/bin/vbox-img    \
    out/linux.*/release/bin/vboximg-mount   \
    out/linux.*/release/bin/VBoxDTrace    \
    out/linux.*/release/bin/VBoxBugReport \
    out/linux.*/release/bin/VirtualBoxVM    \
    out/linux.*/release/bin/bldRTLdrCheckImports  \
    out/linux.*/release/bin/iPxeBaseBin         \
    out/linux.*/release/bin/VBoxCpuReport       \
    out/linux.*/release/bin/VBoxAudioTest       \
%if %{with webservice}
    out/linux.*/release/bin/vboxwebsrv  \
    out/linux.*/release/bin/webtest     \
%endif

#    out/linux.*/release/bin/VBoxSDL   \

# Wrapper with Launchers
ln -s VBox %{buildroot}%{_bindir}/VirtualBox
ln -s VBox %{buildroot}%{_bindir}/virtualbox
ln -s VBox %{buildroot}%{_bindir}/VBoxManage
ln -s VBox %{buildroot}%{_bindir}/vboxmanage
#ln -s VBox %{buildroot}%{_bindir}/VBoxSDL
#ln -s VBox %{buildroot}%{_bindir}/vboxsdl
ln -s VBox %{buildroot}%{_bindir}/VBoxVRDP
ln -s VBox %{buildroot}%{_bindir}/VBoxHeadless
ln -s VBox %{buildroot}%{_bindir}/vboxheadless
ln -s VBox %{buildroot}%{_bindir}/VBoxDTrace
ln -s VBox %{buildroot}%{_bindir}/vboxdtrace
ln -s VBox %{buildroot}%{_bindir}/VBoxBugReport
ln -s VBox %{buildroot}%{_bindir}/vboxbugreport
ln -s VBox %{buildroot}%{_bindir}/VBoxBalloonCtrl
ln -s VBox %{buildroot}%{_bindir}/vboxballoonctrl
ln -s VBox %{buildroot}%{_bindir}/VBoxAutostart
ln -s VBox %{buildroot}%{_bindir}/vboxautostart
ln -s VBox %{buildroot}%{_bindir}/VirtualBoxVM
ln -s VBox %{buildroot}%{_bindir}/virtualboxvm
%if %{with webservice}
ln -s VBox %{buildroot}%{_bindir}/vboxwebsrv
%endif
ln -s ../..%{_libdir}/virtualbox/vbox-img %{buildroot}%{_bindir}
ln -s ../..%{_libdir}/virtualbox/vboximg-mount %{buildroot}%{_bindir}

#ln -s /usr/share/virtualbox/src/vboxhost $RPM_BUILD_ROOT/usr/src/vboxhost-%VER%

# Components, preserve symlinks
cp -a out/linux.*/release/bin/components/* %{buildroot}%{_libdir}/virtualbox/components/
cp out/linux.*/release/bin/UnattendedTemplates/* %{buildroot}%{_libdir}/virtualbox/UnattendedTemplates

# Language files
install -p -m 0755 -t %{buildroot}%{_libdir}/virtualbox/nls \
    out/linux.*/release/bin/nls/*

# Python
%if %{with python3}
pushd out/linux.*/release/bin/sdk/installer/python
export VBOX_INSTALL_PATH=%{_libdir}/virtualbox
%{__python3} vboxapisetup.py install --prefix %{_prefix} --root %{buildroot}
%py3_shebang_fix -pni "%{__python3} %{py3_shbang_opts}" %{buildroot}${VBOX_INSTALL_PATH}/vboxshell.py
popd
%endif

# SDK
cp -rp out/linux.*/release/bin/sdk/. %{buildroot}%{_libdir}/virtualbox/sdk
rm -rf %{buildroot}%{_libdir}/virtualbox/sdk/installer

%if %{with python3}
pushd out/linux.*/release/bin/sdk/installer/python
%py_byte_compile %{__python3} %{buildroot}%{_libdir}/virtualbox/sdk/bindings/xpcom/python
popd
%endif

# Icons
install -p -m 0644 -t %{buildroot}%{_datadir}/pixmaps \
    out/linux.*/release/bin/VBox.png
for S in out/linux.*/release/bin/icons/*
do
    SIZE=$(basename $S)
    install -d %{buildroot}%{_datadir}/icons/hicolor/$SIZE/{mimetypes,apps}
    install -p -m 0644 $S/* %{buildroot}%{_datadir}/icons/hicolor/$SIZE/mimetypes
    [ -f %{buildroot}%{_datadir}/icons/hicolor/$SIZE/mimetypes/virtualbox.png ] && mv \
        %{buildroot}%{_datadir}/icons/hicolor/$SIZE/mimetypes/virtualbox.png \
        %{buildroot}%{_datadir}/icons/hicolor/$SIZE/apps/virtualbox.png
done
install -p -m 0644 out/linux.*/release/bin/virtualbox.xml %{buildroot}%{_datadir}/mime/packages

%if %{with guest_additions}
# Guest X.Org drivers
mkdir -p %{buildroot}%{_libdir}/security

# Guest-additions tools
install -m 0755 -t %{buildroot}%{_sbindir}   \
    out/linux.*/release/bin/additions/VBoxService            \
    out/linux.*/release/bin/additions/mount.vboxsf
install -m 0755 -t %{buildroot}%{_bindir}    \
    out/linux.*/release/bin/additions/VBoxDRMClient          \
    out/linux.*/release/bin/additions/VBoxClient             \
    out/linux.*/release/bin/additions/VBoxControl            \
    out/linux.*/release/bin/additions/vboxwl

# Guest libraries
install -m 0755 -t %{buildroot}%{_libdir}/security \
    out/linux.*/release/bin/additions/pam_vbox.so

install -p -m 0755 -D src/VBox/Additions/x11/Installer/98vboxadd-xclient \
    %{buildroot}%{_sysconfdir}/X11/xinit/xinitrc.d/98vboxadd-xclient.sh
ln -s ../..%{_sysconfdir}/X11/xinit/xinitrc.d/98vboxadd-xclient.sh \
    %{buildroot}%{_bindir}/VBoxClient-all
desktop-file-install --dir=%{buildroot}%{_sysconfdir}/xdg/autostart/ \
    --remove-key=Encoding src/VBox/Additions/x11/Installer/vboxclient.desktop
desktop-file-validate \
    %{buildroot}%{_sysconfdir}/xdg/autostart/vboxclient.desktop

install -p -m 0644 -D %{SOURCE7} %{buildroot}%{_unitdir}/vboxservice.service
install -p -m 0644 -D %{SOURCE8} %{buildroot}%{_presetdir}/96-vboxguest.preset
install -p -m 0644 -D %{SOURCE5} %{buildroot}%{_udevrulesdir}/60-vboxguest.rules
install -p -m 0644 -D %{SOURCE6} %{buildroot}%{_unitdir}/vboxclient.service

# Create a sysusers.d config file
cat >virtualbox-guest-additions.sysusers.conf <<EOF
# Group "vboxsf" for Shared Folders access.
# All users which want to access the auto-mounted Shared Folders
# have to be added to this group.
g vboxsf -
u vboxadd -:1 - /var/run/vboxadd -
EOF
install -m0644 -D virtualbox-guest-additions.sysusers.conf %{buildroot}%{_sysusersdir}/virtualbox-guest-additions.conf

%endif

cat >virtualbox.sysusers.conf << EOF
g vboxusers - - - -
EOF
install -m0644 -D virtualbox.sysusers.conf %{buildroot}%{_sysusersdir}/virtualbox.conf

# Module Source Code
mkdir -p %{name}-kmod-%{version}
cp -al out/linux.*/release/bin/src/vbox* out/linux.*/release/bin/additions/src/vbox* %{name}-kmod-%{version}
install -d %{buildroot}%{_datadir}/%{name}-kmod-%{version}
tar --use-compress-program xz -cf %{buildroot}%{_datadir}/%{name}-kmod-%{version}/%{name}-kmod-%{version}.tar.xz \
    %{name}-kmod-%{version}

%if %{with webservice}
install -m 0644 -D %{SOURCE10} \
    %{buildroot}%{_unitdir}/vboxweb.service
%endif

# Install udev rules
install -p -m 0755 -D out/linux.*/release/bin/VBoxCreateUSBNode.sh %{buildroot}%{_prefix}/lib/udev/VBoxCreateUSBNode.sh
install -p -m 0644 -D %{SOURCE3} %{buildroot}%{_udevrulesdir}/60-vboxdrv.rules

# Install service to load server modules
install -p -m 0644 -D %{SOURCE4} %{buildroot}%{_unitdir}/vboxdrv.service
install -p -m 0644 -D %{SOURCE9} %{buildroot}%{_presetdir}/96-vboxhost.preset

# Menu entry
desktop-file-install --dir=%{buildroot}%{_datadir}/applications \
    out/linux.*/release/bin/virtualbox.desktop
desktop-file-install --dir=%{buildroot}%{_datadir}/applications \
    out/linux.*/release/bin/virtualboxvm.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/virtualbox.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/virtualboxvm.desktop

install -p -m 0644 -D %{SOURCE2} %{buildroot}%{_metainfodir}/%{name}.appdata.xml

# Workaround kvm.ko usurping VMX.
# (Linux kernel commit b4886fab6fb620b96ad7eeefb9801c42dfa91741 is the culprit.
# See also https://lore.kernel.org/kvm/ZwQjUSOle6sWARsr@google.com/T/ )
install -d %{buildroot}%{_modprobedir}
echo options kvm enable_virt_at_load=0 > %{buildroot}%{_modprobedir}/50-virtualbox.conf

%if %{with vnc}
echo "entering VNC extension install section"
pushd out/linux.*/release/packages/
mkdir -p %{buildroot}%{_libdir}/virtualbox/ExtensionPacks/VNC
install -D -m 644 VNC-*.vbox-extpack %{buildroot}%{_libdir}/virtualbox/ExtensionPacks/VNC/VNC-%{version}.vbox-extpack
popd
%endif

# to review:
#set_selinux_permissions /usr/lib/virtualbox /usr/share/virtualbox
# vboxautostart-service

%if %{with vnc}
%post vnc
EXTPACK="%{_libdir}/virtualbox/ExtensionPacks/VNC/VNC-%{version}.vbox-extpack"
ACCEPT="$(tar --to-stdout -xf "${EXTPACK}" ./ExtPack-license.txt | sha256sum | head --bytes=64)"
VBoxManage extpack install --replace "${EXTPACK}" --accept-license="${ACCEPT}" > /dev/null

%files vnc
%license COPYING
%dir %{_libdir}/virtualbox/ExtensionPacks/VNC/
%{_libdir}/virtualbox/ExtensionPacks/VNC/VNC-%{version}.vbox-extpack
%endif

%post server
# Assign USB devices
if /sbin/udevadm control --reload-rules >/dev/null 2>&1
then
   /sbin/udevadm trigger --subsystem-match=usb --action=add >/dev/null 2>&1 || :
   /sbin/udevadm settle >/dev/null 2>&1 || :
fi
%systemd_post vboxdrv.service

%preun server
%systemd_preun vboxdrv.service

%postun server
%systemd_postun vboxdrv.service

%triggerun -- VirtualBox-server < 0:6.1.10-4
/usr/bin/systemctl --no-reload preset vboxdrv.service || :

%post webservice
%systemd_post vboxweb.service

%preun webservice
%systemd_preun vboxweb.service

%postun webservice
%systemd_postun_with_restart vboxweb.service

# Guest additions install
%post guest-additions
%systemd_post vboxclient.service
%systemd_post vboxservice.service

#chcon -u system_u -t mount_exec_t "$lib_path/$PACKAGE/mount.vboxsf" > /dev/null 2>&1
# for i in "$lib_path"/*.so
# do
#     restorecon "$i" >/dev/null
# done
# ;;
#chcon -u system_u -t lib_t "$lib_dir"/*.so

# Our logging code generates some glue code on 32-bit systems.  At least F10
# needs a rule to allow this.  Send all output to /dev/null in case this is
# completely irrelevant on the target system.
#chcon -t unconfined_execmem_exec_t '/usr/bin/VBoxClient' > /dev/null 2>&1
#semanage fcontext -a -t unconfined_execmem_exec_t '/usr/bin/VBoxClient' > /dev/null 2>&1

%preun guest-additions
%systemd_preun vboxclient.service
%systemd_preun vboxservice.service

%postun guest-additions
%systemd_postun_with_restart vboxclient.service
%systemd_postun_with_restart vboxservice.service

%files server
%doc doc/*cpp doc/VMM
%if %{with docs}
%doc out/linux.*/release/bin/UserManual*.pdf
%else
%doc UserManual.pdf
%endif
%license COPYING*
%{_bindir}/VBox
%{_bindir}/VBoxAutostart
%{_bindir}/vboxautostart
%{_bindir}/VBoxBalloonCtrl
%{_bindir}/vboxballoonctrl
%{_bindir}/VBoxBugReport
%{_bindir}/vboxbugreport
%{_bindir}/VBoxDTrace
%{_bindir}/vboxdtrace
%{_bindir}/vboxheadless
%{_bindir}/VBoxHeadless
%{_bindir}/VBoxManage
%{_bindir}/vboxmanage
#{_bindir}/VBoxSDL
#{_bindir}/vboxsdl
%{_bindir}/VBoxVRDP
%{_bindir}/VirtualBoxVM
%{_bindir}/virtualboxvm
%{_bindir}/vbox-img
%{_bindir}/vboximg-mount
%dir %{_libdir}/virtualbox
%{_libdir}/virtualbox/*.[^p]*
%exclude %{_libdir}/virtualbox/VBoxDbg.so
%exclude %{_libdir}/virtualbox/UICommon.so
%exclude %{_libdir}/virtualbox/VirtualBoxVM.so
%{_libdir}/virtualbox/components/
%{_libdir}/virtualbox/VBoxExtPackHelperApp
%{_libdir}/virtualbox/VBoxManage
%{_libdir}/virtualbox/VBoxSVC
%{_libdir}/virtualbox/VBoxBalloonCtrl
%{_libdir}/virtualbox/SUPInstall
%{_libdir}/virtualbox/SUPLoggerCtl
%{_libdir}/virtualbox/SUPUninstall
%{_libdir}/virtualbox/UnattendedTemplates
%{_libdir}/virtualbox/VBoxAutostart
%{_libdir}/virtualbox/VBoxVMMPreload
%{_libdir}/virtualbox/VBoxBugReport
%{_libdir}/virtualbox/VBoxDTrace
%{_libdir}/virtualbox/vbox-img
%{_libdir}/virtualbox/vboximg-mount
%{_libdir}/virtualbox/iPxeBaseBin
%{_libdir}/virtualbox/bldRTLdrCheckImports
%{_libdir}/virtualbox/VBoxCpuReport
%{_libdir}/virtualbox/VBoxAudioTest
# This permissions have to be here, before generator of debuginfo need
# permissions to read this files
%attr(4511,root,root) %{_libdir}/virtualbox/VBoxNetNAT
%attr(4511,root,root) %{_libdir}/virtualbox/VBoxVolInfo
%attr(4511,root,root) %{_libdir}/virtualbox/VBoxHeadless
#%%attr(4511,root,root) %%{_libdir}/virtualbox/VBoxSDL
%attr(4511,root,root) %{_libdir}/virtualbox/VBoxNetDHCP
%attr(4511,root,root) %{_libdir}/virtualbox/VBoxNetAdpCtl
%attr(4511,root,root) %{_libdir}/virtualbox/VirtualBoxVM
%{_udevrulesdir}/60-vboxdrv.rules
%{_unitdir}/vboxdrv.service
%{_modprobedir}/
%{_presetdir}/96-vboxhost.preset
# Group for USB devices
%{_sysusersdir}/virtualbox.conf
%{_prefix}/lib/udev/VBoxCreateUSBNode.sh
%{_datadir}/applications/virtualboxvm.desktop

%files
%{_bindir}/VirtualBox
%{_bindir}/virtualbox
%{_libdir}/virtualbox/VBoxDbg.so
%{_libdir}/virtualbox/UICommon.so
%{_libdir}/virtualbox/VirtualBox
%{_libdir}/virtualbox/VirtualBoxVM.so
%{_libdir}/virtualbox/nls
%{_datadir}/pixmaps/*.png
%{_datadir}/applications/virtualbox.desktop
%{_datadir}/icons/hicolor/*/apps/*.png
%{_datadir}/icons/hicolor/*/mimetypes/*.png
%{_datadir}/icons/hicolor/scalable/mimetypes/virtualbox.svg
%{_datadir}/mime/packages/virtualbox.xml
%{_metainfodir}/%{name}.appdata.xml

%if %{with webservice}
%files webservice
%{_bindir}/vboxwebsrv
%{_unitdir}/vboxweb.service
%{_libdir}/virtualbox/vboxwebsrv
%{_libdir}/virtualbox/webtest
%endif

%files devel
%{_libdir}/virtualbox/sdk

%if %{with python3}
%files -n python%{python3_pkgversion}-%{name}
%{_libdir}/virtualbox/*.py*
%{_libdir}/virtualbox/VBoxPython3*.so
%{python3_sitelib}/vboxapi-1*.egg-info
%{python3_sitelib}/vboxapi
%endif

%if %{with guest_additions}
%files guest-additions
%license COPYING*
%{_bindir}/vboxwl
%{_bindir}/VBoxClient
%{_bindir}/VBoxControl
%{_bindir}/VBoxClient-all
%{_bindir}/VBoxDRMClient
%{_sbindir}/VBoxService
%{_sbindir}/mount.vboxsf
%{_libdir}/security/pam_vbox.so
%{_sysconfdir}/X11/xinit/xinitrc.d/98vboxadd-xclient.sh
%{_sysconfdir}/xdg/autostart/vboxclient.desktop
%{_unitdir}/vboxclient.service
%{_unitdir}/vboxservice.service
%{_presetdir}/96-vboxguest.preset
%{_udevrulesdir}/60-vboxguest.rules
%{_sysusersdir}/virtualbox-guest-additions.conf
%endif

%files kmodsrc
%{_datadir}/%{name}-kmod-%{version}

%changelog
* Thu Sep 11 2025 Sérgio Basto <sergio@serjux.com> - 7.2.2-1
- Update VirtualBox to 7.2.2

* Mon Sep 01 2025 Sérgio Basto <sergio@serjux.com> - 7.2.0-3
- Nat fixes, print qt6 version nedded

* Fri Aug 29 2025 Sérgio Basto <sergio@serjux.com> - 7.2.0-2
- Add patch from Oracle rfbz#7238

* Sun Aug 24 2025 Sérgio Basto <sergio@serjux.com> - 7.2.0-1
- Update VirtualBox to 7.2.0

* Wed Jul 30 2025 Sérgio Basto <sergio@serjux.com> - 7.1.12-1
- Update VirtualBox to 7.1.12

* Sat Jul 26 2025 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 7.1.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jul 12 2025 Sérgio Basto <sergio@serjux.com> - 7.1.10-2
- Disable i686 support on EL, adding --disable-vmmraw on ./configure

* Thu Jun 05 2025 Sérgio Basto <sergio@serjux.com> - 7.1.10-1
- Update VirtualBox to 7.1.10

* Fri May 23 2025 Sérgio Basto <sergio@serjux.com> - 7.1.8-3
- Drop patch 009-properly-handle-i3wm.patch may cause problems

* Fri Apr 18 2025 Sérgio Basto <sergio@serjux.com>
- Sync with Fedora

* Tue Apr 15 2025 Sérgio Basto <sergio@serjux.com> - 7.1.8-1
- Update VirtualBox to 7.1.8

* Sun Mar 30 2025 Sérgio Basto <sergio@serjux.com> - 7.1.6-3
- New support to python
- Disable java because wsimport is not available
- Enable webservice
- Build vnc extension
- Also add sysusers.d config file for vboxusers (server side)
- Add files bldRTLdrCheckImports, iPxeBaseBin, VBoxCpuReport and virtualboxvm.desktop
- Drop BR SDL

* Thu Feb 13 2025 Sérgio Basto <sergio@serjux.com> - 7.1.6-2
- Workaround kvm.ko usurping VMX, copied from OpenSuse
- Add sysusers.d config file to allow rpm to create users/groups automatically

* Wed Feb 12 2025 Sérgio Basto <sergio@serjux.com> - 7.1.6-1
- Update VirtualBox to 7.1.6

* Tue Jan 28 2025 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 7.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Oct 17 2024 Sérgio Basto <sergio@serjux.com> - 7.1.4-1
- Update VirtualBox to 7.1.4

* Fri Oct 04 2024 Sérgio Basto <sergio@serjux.com> - 7.1.2-2
- Not build test cases
- Minor cleanup of scripts for el7

* Fri Sep 27 2024 Sérgio Basto <sergio@serjux.com> - 7.1.2-1
- Update VirtualBox to 7.1.2

* Tue Sep 17 2024 Sérgio Basto <sergio@serjux.com> - 7.1.0-2
- Also drop VirtualBox-python3.12.patch
- Drop support to enable the build of old vboxvideo (guest drive)
  is disabled with VBOX_NO_LEGACY_XORG_X11=1 , no need to patch the code !
  https://www.virtualbox.org/changeset/64270/vbox

* Mon Sep 16 2024 Sérgio Basto <sergio@serjux.com> - 7.1.0-1
- Update VirtualBox to 7.1.0

* Thu Aug 01 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 7.0.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 16 2024 Sérgio Basto <sergio@serjux.com> - 7.0.20-1
- Update VirtualBox to 7.0.20

* Fri May 03 2024 Sérgio Basto <sergio@serjux.com> - 7.0.18-1
- Update VirtualBox to 7.0.18

* Tue Apr 16 2024 Sérgio Basto <sergio@serjux.com> - 7.0.16-1
- Update VirtualBox to 7.0.16

* Sat Feb 03 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 7.0.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 17 2024 Sérgio Basto <sergio@serjux.com> - 7.0.14-1
- Update VirtualBox to 7.0.14

* Tue Oct 17 2023 Sérgio Basto <sergio@serjux.com> - 7.0.12-1
- Update VirtualBox to 7.0.12

* Wed Jul 19 2023 Sérgio Basto <sergio@serjux.com> - 7.0.10-1
- Update VirtualBox to 7.0.10

* Sat Jul 08 2023 Leigh Scott <leigh123linux@gmail.com> - 7.0.8-4
- Rebuilt for Python 3.12

* Sun May 21 2023 Sérgio Basto <sergio@serjux.com> - 7.0.8-3
- (#6660) Fix the documentation, the vboxpci module is not shipped since VirtualBox 6.1.0

* Wed Apr 19 2023 Sérgio Basto <sergio@serjux.com> - 7.0.8-2
- sync with virtualbox-guest-additions.spec
- Replaces with sed -i "s/VBOX_ZLIB_STATIC/VBoxZlibStatic/; s/VBOX_ZLIB-x86/VBoxZlib-x86/; s/VBOX_ZLIB/VBoxZlib/; s/VBOX_LIBXML2/VBoxLibXml2/; s/VBOX_VPX/VBoxLibVpx/;s/VBOX_LZF/VBoxLzf/;s/VBOX_LIBPNG/VBoxLibPng/; s/VBOX_LIBCURL/VBoxLibCurl/;s/VBOX_DXVK/VBoxDxVk/;s/VBOX_OGG/VBoxLibOgg/;s/VBOX_VORBIS/VBoxLibVorbis/; s/VBOX_TPMS/VBoxLibTpms/" VirtualBox.spec

* Tue Apr 18 2023 Sérgio Basto <sergio@serjux.com> - 7.0.8-1
- Update VirtualBox to 7.0.8

* Wed Jan 18 2023 Sérgio Basto <sergio@serjux.com> - 7.0.6-1
- Update VirtualBox to 7.0.6
- Add fix to gcc13

* Wed Dec 14 2022 Sérgio Basto <sergio@serjux.com> - 7.0.4-2
- we should restart vboxdrv just after akmods builds

* Sat Nov 19 2022 Sérgio Basto <sergio@serjux.com> - 7.0.4-1
- Update VirtualBox to 7.0.4
- Drop system-libs.patch and fix-build.patch already upstreamed

* Wed Oct 26 2022 Sérgio Basto <sergio@serjux.com> - 7.0.2-1
- Update to 7.0.2
- Drop python2 support
- Based on Mageia and after on Debian packages
- Drop VirtualBox-6.0.10-convert-map-python3.patch and vb-6.1.16-modal-dialog-parent.patch
- Refresh default-to-Fedora, noupdate.patch, xclient.patch, build-xpcom18a4-with-c++17.patch and python3.11.patch
- Replace fixes_for_Qt5.11to15.patch with remove-duplicated-define.patch, update-Mageia-support.patch and fix-missing-includes-with-qt-5.15.patch
- Add ExtPacks-VBoxDTrace-no-publisher-in-version.patch from Mageia
- Add partial system-libs.patch and fix-build.patch from Debian (libvorbis and libogg system support)
- Add build conditionals for system_libtpms and dxvk-native
- Add VirtualBox-5.1.0-lib64-VBox.sh.patch and finally drop /etc/vbox as upstream did in 5.1.0
- Add BR: nasm (to fix nasm: not found message)

* Wed Oct 12 2022 Sérgio Basto <sergio@serjux.com> - 6.1.40-1
- Update VirtualBox to 6.1.40

* Thu Sep 01 2022 Sérgio Basto <sergio@serjux.com> - 6.1.38-1
- Update VirtualBox to 6.1.38

* Sat Aug 06 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 6.1.36-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Mon Jul 25 2022 Sérgio Basto <sergio@serjux.com> - 6.1.36-1
- Update VirtualBox to 6.1.36

* Sat Jun 25 2022 Robert-André Mauchin <zebob.m@gmail.com> - 6.1.34-5
- Rebuilt for Python 3.11

* Sat Jun 04 2022 Sérgio Basto <sergio@serjux.com> - 6.1.34-4
- use opensuse patch for kernel 5.18

* Tue May 31 2022 Sérgio Basto <sergio@serjux.com> - 6.1.34-3
- Initial fix Windows 10 VM crashes with Linux 5.18 kernel

* Mon Apr 25 2022 Sérgio Basto <sergio@serjux.com> - 6.1.34-2
- Fix for rfbz #6287 (won't launch any VM)

* Tue Apr 19 2022 Sérgio Basto <sergio@serjux.com> - 6.1.34-1
- Update VirtualBox to 6.1.34
- Fix rfbz #6254
- Don't build virtualbox-guest-additions on EL-9 because is already provided by
  kmod SIG

* Mon Feb 21 2022 Sérgio Basto <sergio@serjux.com> - 6.1.32-5
- Re-enable webservice

* Thu Feb 17 2022 Sérgio Basto <sergio@serjux.com> - 6.1.32-4
- Re-enable python on Fedora > 34

* Tue Feb 08 2022 Leigh Scott <leigh123linux@gmail.com> - 6.1.32-3
- Rebuild for libvpx

* Fri Jan 21 2022 Sérgio Basto <sergio@serjux.com> - 6.1.32-2
- Add BR pulseaudio-libs-devel which add pulse audio support
- Move /usr/lib64/virtualbox/VirtualBox to VirtualBox (Qt) package which make
  VirtualBox-server not depend on Qt5

* Tue Jan 18 2022 Sérgio Basto <sergio@serjux.com> - 6.1.32-1
- Update VirtualBox to 6.1.32

* Mon Nov 22 2021 Sérgio Basto <sergio@serjux.com> - 6.1.30-1
- Update VirtualBox to 6.1.30

* Wed Oct 20 2021 Sérgio Basto <sergio@serjux.com> - 6.1.28-1
- Update VirtualBox to 6.1.28 with inspirations in the Mageia and Debian packages

* Mon Aug 09 2021 Sérgio Basto <sergio@serjux.com> - 6.1.26-3
- Fix build on rawhide (disabling python) and BR alsa-lib-devel

* Mon Aug 02 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 6.1.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Aug 02 2021 Sérgio Basto <sergio@serjux.com> - 6.1.26-1
- Update VirtualBox to 6.1.26
- Patch 61 was included upstream

* Tue Jun 15 2021 Leigh Scott <leigh123linux@gmail.com> - 6.1.22-3
- Rebuild for python-3.10

* Mon May 03 2021 Sérgio Basto <sergio@serjux.com> - 6.1.22-2
- Fix picker dialog with patch from OpenSuse (rfbz #5929)

* Thu Apr 29 2021 Sérgio Basto <sergio@serjux.com> - 6.1.22-1
- Update VirtualBox to 6.1.22
- wsimport is not loading on Fedora rawhide so we can't build webservice until have a fix

* Fri Apr 23 2021 Sérgio Basto <sergio@serjux.com> - 6.1.20-3
- We can build webservice with JDK 1.8 as workaround
- Enable system lzf with patch that make it work

* Thu Apr 22 2021 Sérgio Basto <sergio@serjux.com> - 6.1.20-2
- Add back Mageia support and default Linux OS as Fedora
- From Mageia add VirtualBox-6.0.10-convert-map-python3.patch
- Add a couple of patches of openSuse for qt and virtualbox-snpritnf-buffer-overflow.patch
- Drop patch of aiobug is for EL6 only

* Wed Apr 21 2021 Sérgio Basto <sergio@serjux.com> - 6.1.20-1
- Update VirtualBox to 6.1.20

* Tue Feb 02 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 6.1.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan 21 2021 Sérgio Basto <sergio@serjux.com> - 6.1.18-1
- Update VirtualBox to 6.1.18

* Mon Oct 26 2020 Sérgio Basto <sergio@serjux.com> - 6.1.16-2
- Enable webservice (#5809)
- wsimport was removed from Java 11, so we can't build webservice in F33+ until
  Fedora have the package jaxws .

* Wed Oct 21 2020 Sérgio Basto <sergio@serjux.com> - 6.1.16-1
- Update VirtualBox to 6.1.16

* Fri Sep 11 2020 Sérgio Basto <sergio@serjux.com> - 6.1.14-4
- Use upstreamd patch to build webservice on F33+ and more synchronizations
  with the debian package.

* Thu Sep 10 2020 Sérgio Basto <sergio@serjux.com> - 6.1.14-3
- Fixes for kernel 4.9

* Tue Sep 08 2020 Sérgio Basto <sergio@serjux.com> - 6.1.14-2
- Update to VirtualBox-6.1.14a rfbz (#5747)

* Sat Sep 05 2020 Sérgio Basto <sergio@serjux.com> - 6.1.14-1
- Update VBox to 6.1.14

* Mon Aug 17 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 6.1.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Aug 07 2020 Sérgio Basto <sergio@serjux.com> - 6.1.12-3
- Some fixes

* Wed Aug 05 2020 Sérgio Basto <sergio@serjux.com> - 6.1.12-2
- Updates for kernel-5.8

* Thu Jul 16 2020 Sérgio Basto <sergio@serjux.com> - 6.1.12-1
- Update VBox to 6.1.12
- From Debian disable cloud_net "Fix build failure due to missing upstream file"

* Sun Jun 21 2020 Sérgio Basto <sergio@serjux.com> - 6.1.10-5
- The VirtualBox 6.1 changelog says that it supports vboximg-mount on Linux
  hosts

* Wed Jun 17 2020 Sérgio Basto <sergio@serjux.com> - 6.1.10-4
- Fix (#5677)
  https://docs.pagure.org/packaging-guidelines/Packaging%3AScriptlets.html (On
  upgrade, the scripts are run in the following order)

* Sat Jun 13 2020 Sérgio Basto <sergio@serjux.com> - 6.1.10-3
- Syncronize with virtualbox-guest-additions from Fedora
- Add a vboxclient.service which runs VBoxClient --vwsvga when using the
  VMSVGA virtual GPU, this fixes resizing in wayland sessions (rhbz 1789545)
- Drop VBoxClient --vwsvga-x11 from VBoxClient-all, it is not necessary
  now that we run VBoxClient --vwsvga as service and it was breaking resize
  support with the VBoxSVGA virtual GPU (rhbz 1789545)
- Drop ExecStartPre modprove vboxvideo vboxsf from vboxservice.service,
  this is not necessary, they will be loaded automatically


* Mon Jun 08 2020 Sérgio Basto <sergio@serjux.com> - 6.1.10-2
- Install the new VBoxDRMClient binary for guest-additions
- Drop wayland-crash patch and fix wrong path to modprobe
- Rfbz #3966, not using anymore systemd-modules-load.service
  Instead we use one systemd service (vboxdrv.service) to load the server modules.
- Only in epel7 run the scriptlets of Icon Cache, mimeinfo and Desktop databases
- Move icons files from server sub-package to main (Qt/Desktop) sub-package
- Also scriptlets of usb moved to server sub-package
- Minor fixes
  Rename patch VirtualBox-6.1.4-hacks to VirtualBox-6.1.4-gcc10
  Syncronize vboxservice.service with virtualbox-guest-additions from Fedora
  Remove bundled src/libs/openssl

* Sat Jun 06 2020 Sérgio Basto <sergio@serjux.com> - 6.1.10-1
- Update VBox to 6.1.10

* Tue Jun 02 2020 Sérgio Basto <sergio@serjux.com> - 6.1.8-5
- Fix build on EL8

* Sun May 31 2020 Sérgio Basto <sergio@serjux.com> - 6.1.8-4
- Add python-3.9 support
- Fix some conditionals of python especially for el8

* Sat May 30 2020 Leigh Scott <leigh123linux@gmail.com>
- Rebuild for python-3.9

* Tue May 26 2020 Sérgio Basto <sergio@serjux.com> - 6.1.8-3
- Add VirtualBox-6.1.0-VBoxRem.patch rfbz #5652
- Remove pre-compiled headers
- xalan-c-devel and xerces-c-devel are not needed anymore

* Wed May 20 2020 Sérgio Basto <sergio@serjux.com> - 6.1.8-2
- Fix for guest additions on EL7, now we use vboxservice.service to load modules.
  Partial fix for rfbz #3966

* Fri May 15 2020 Sérgio Basto <sergio@serjux.com> - 6.1.8-1
- Update VBox to 6.1.8

* Tue Apr 14 2020 Sérgio Basto <sergio@serjux.com> - 6.1.6-1
- Update VBox to 6.1.6

* Sat Apr 04 2020 Sérgio Basto <sergio@serjux.com> - 6.1.4-4
- Fix rfbz#5581 USB devices are not available
- VirtualBox-6.1.4-VBoxClient-vmsvga-x11-crash.patch, just for epel7
  guest-additions.
- rfbz #5589 2 patches: Fix VBox crash when started under Wayland, Fix
  keyboard-grab under Wayland

* Thu Mar 19 2020 Sérgio Basto <sergio@serjux.com> - 6.1.4-3
- Fixes for kernel 5.6 from
  https://build.opensuse.org/package/show/Virtualization/virtualbox
  but just applied on Fedora, because breaks the build on EPEL 7
- Temporary hack to try to fix upgrade path.
- Fix build on rawhide, perl related.

* Fri Feb 21 2020 Sérgio Basto <sergio@serjux.com> - 6.1.4-2
- Add a hack to fix builds on Rawhide/F32

* Thu Feb 20 2020 Sérgio Basto <sergio@serjux.com> - 6.1.4-1
- Update VBox to 6.1.4

* Tue Feb 04 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 6.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jan 18 2020 Sérgio Basto <sergio@serjux.com> - 6.1.2-1
- Update VBox to 6.1.2

* Wed Dec 18 2019 Sérgio Monteiro Basto <sergio@serjux.com> - 6.1.0-1
- Update VBox to 6.1.0

* Tue Oct 29 2019 Sérgio Basto <sergio@serjux.com> - 6.0.14-2
- Add appstream file (copied from openSUSE)

* Thu Oct 17 2019 Sérgio Basto <sergio@serjux.com> - 6.0.14-1
- Update VBox to 6.0.14

* Sun Oct 06 2019 Sérgio Basto <sergio@serjux.com> - 6.0.12-2
- Disable python bindings on rawhide until we figure out what happened with
  Python 3.8

* Thu Sep 05 2019 Sérgio Basto <sergio@serjux.com> - 6.0.12-1
- Update VBox to 6.0.12

* Sat Aug 24 2019 Leigh Scott <leigh123linux@gmail.com> - 6.0.10-3
- Rebuild for python-3.8

* Fri Aug 09 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 6.0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild
- Fixes warning with: "It's not recommended to have unversioned Obsoletes: Obsoletes:  VirtualBox-qt"

* Tue Jul 16 2019 Sérgio Basto <sergio@serjux.com> - 6.0.10-1
- Update VBox to 6.0.10

* Wed May 15 2019 Sérgio Basto <sergio@serjux.com> - 6.0.8-1
- Update VBox to 6.0.8

* Mon Apr 29 2019 Sérgio Basto <sergio@serjux.com> - 6.0.6-3
- Sync patch 0001-VBoxServiceAutoMount-Change-Linux-mount-code-to-use- with
  Fedora

* Wed Apr 17 2019 Sérgio Basto <sergio@serjux.com> - 6.0.6-2
- Rebase 0001-VBoxServiceAutoMount-Change-Linux-mount-code-to-use-.patch

* Wed Apr 17 2019 Vasiliy N. Glazov <vascom2@gmail.com> - 6.0.6-1
- Update to 6.0.6

* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 6.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 28 2019 Sérgio Basto <sergio@serjux.com> - 6.0.4-1
- Update VBox to 6.0.4

* Wed Jan 23 2019 Sérgio Basto <sergio@serjux.com> - 6.0.2-3
- python3 on epel7
- Fix build of webservice

* Sat Jan 19 2019 Sérgio Basto <sergio@serjux.com> - 6.0.2-2
- Patch 61 might be useful on el7

* Thu Jan 17 2019 Vasiliy N. Glazov <vascom2@gmail.com> - 6.0.2-1
- Update to 6.0.2

* Mon Jan 07 2019 Sérgio Basto <sergio@serjux.com> - 6.0.0-2
- Enable Python3 support, move all SDK python files to devel sub-package, they
  may be used by python2 and python 3.
- Add patch VBoxVNC.fix.patch from Debian
- Issue with EXTPACK_VBOXDTRACE was fix some time ago.

* Sun Dec 30 2018 Sérgio Basto <sergio@serjux.com> - 6.0.0-1
- VirtualBox 6.0
- Patch23 was applied upstream.

* Fri Nov 09 2018 Sérgio Basto <sergio@serjux.com> - 5.2.22-1
- Update VBox to 5.2.22
- Reenable noupdate.patch
- Rebase patches
- Add patch for API changes in kernel 4.20 from Larry Finger (OpenSuse)

* Thu Oct 18 2018 Sérgio Basto <sergio@serjux.com> - 5.2.20-1
- Update VBox to 5.2.20

* Fri Aug 24 2018 Sérgio Basto <sergio@serjux.com> - 5.2.18-1
- Update VBox to 5.2.18

* Thu Jul 26 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 5.2.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jul 26 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 5.2.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jul 21 2018 Sérgio Basto <sergio@serjux.com> - 5.2.16-1
- Update VBox to 5.2.16

* Mon Jul 02 2018 Sérgio Basto <sergio@serjux.com> - 5.2.14-1
- Update VBox to 5.2.14

* Thu May 10 2018 Sérgio Basto <sergio@serjux.com> - 5.2.12-1
- Update VBox to 5.2.12
- Previous bug shows that we don't need VBOX_PATH_DOCBOOK anymore.

* Thu Apr 26 2018 Sérgio Basto <sergio@serjux.com> - 5.2.10-2
- Don't build guest-additions for F28+ (now it is available on Fedora proper)

* Thu Apr 19 2018 Sérgio Basto <sergio@serjux.com> - 5.2.10-1
- Update VBox to 5.2.10

* Sat Mar 17 2018 Sérgio Basto <sergio@serjux.com> - 5.2.8-3
- Add patches from virtualbox-guest-additions of Fedora proper
- python-VirtualBox renamed to python2-VirtualBox
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3
- Enable vnc

* Wed Mar 07 2018 Sérgio Basto <sergio@serjux.com> - 5.2.8-2
- Fix minor spelling mistakes
- Remove Conflicts between subpackages server and guest-additions

* Thu Mar 01 2018 Sérgio Basto <sergio@serjux.com> - 5.2.8-1
- Update VBox to 5.2.8
- Review the new kmk configurations, drop some patches and sent
  VirtualBox-5.0.18-xserver_guest.patch to upstream
- Update the required version of kbuild

* Wed Feb 28 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 5.2.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Feb 28 2018 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 5.2.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Sérgio Basto <sergio@serjux.com> - 5.2.6-3
- Enable GCC 8 support

* Fri Feb 02 2018 Leigh Scott <leigh123linux@googlemail.com>
- Rebuild for boost-1.66

* Fri Jan 19 2018 Sérgio Basto <sergio@serjux.com> - 5.2.6-2
- Make sub-package VirtualBox-kmodsrc noarch

* Wed Jan 17 2018 Sérgio Basto <sergio@serjux.com> - 5.2.6-1
- Update VBox to 5.2.6

* Mon Jan 15 2018 Sérgio Basto <sergio@serjux.com> - 5.2.4-1
- Update VBox to 5.2.4

* Wed Nov 08 2017 Sérgio Basto <sergio@serjux.com> - 5.1.30-2
- Restore kmk configurations VBOX_PATH_APP_PRIVATE and VBOX_PATH_APP_DOCS
  rfbz(#4701)

* Fri Oct 27 2017 Sérgio Basto <sergio@serjux.com> - 5.1.30-1
- Update VBox to 5.1.30
- Some updates on VirtualBox-guest-addition based on VirtualBox-guest-addition.spec in review rhbz #1481630, with
  proper fix for VirtualBox-5.0.22-guest_soname.patch
- TODO check python3 and clean obsoleted scriptlets

* Sat Sep 16 2017 Sérgio Basto <sergio@serjux.com> - 5.1.28-2
- Epel 7 with X 1.19 don't need vboxvideo_drv
  https://forums.virtualbox.org/viewtopic.php?f=15&t=84201

* Thu Sep 14 2017 Sérgio Basto <sergio@serjux.com> - 5.1.28-1
- Update VBox to 5.1.28

* Sun Aug 06 2017 Sérgio Basto <sergio@serjux.com> - 5.1.26-2
- Some improvements based on new virtualbox-guest-additions for Fedora
  rhbz #1481630 and rfbz #4617
- Drop VirtualBox-4.3.0-no-bundles.patch, set make variables instead
- Remove VMSVGA3D from Config.kmk is windows only
- VBOX_WITH_EXTPACK_VBOXDTRACE fails to build with glibc >= 2.26-2.fc27

* Thu Jul 27 2017 Sérgio Basto <sergio@serjux.com> - 5.1.26-1
- Update VBox to 5.1.26

* Tue Jul 18 2017 Sérgio Basto <sergio@serjux.com> - 5.1.24-1
- Update VBox to 5.1.24

* Wed Jun 14 2017 Sérgio Basto <sergio@serjux.com> - 5.1.22-1
- Update VBox to 5.1.22

* Sun Apr 23 2017 Sérgio Basto <sergio@serjux.com> - 5.1.20-3
- Build pdf doc on f26+

* Sat Apr 22 2017 Sérgio Basto <sergio@serjux.com> - 5.1.20-2
- Fix owning /usr/share/icons (rfbz#4509), thanks to Vasiliy N. Glazov

* Wed Apr 19 2017 Sérgio Basto <sergio@serjux.com> - 5.1.20-1
- Update VBox to 5.1.20, security fixes

* Sat Mar 18 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 5.1.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Mar 16 2017 Sérgio Basto <sergio@serjux.com> - 5.1.18-1
- Update VirtualBox to 5.1.18

* Wed Mar 08 2017 Sérgio Basto <sergio@serjux.com> - 5.1.16-1
- Update VBox to 5.1.16

* Mon Jan 23 2017 Sérgio Basto <sergio@serjux.com> - 5.1.14-2
- Drop VirtualBox-OSE-4.1.12-gsoap.patch, was for Fedora 15

* Tue Jan 17 2017 Sérgio Basto <sergio@serjux.com> - 5.1.14-1
- Update VBox to 5.1.14

* Tue Nov 22 2016 Sérgio Basto <sergio@serjux.com> - 5.1.10-1
- New upstream release, 5.1.10

* Wed Oct 19 2016 Sérgio Basto <sergio@serjux.com> - 5.1.8-2
- Fixes for EL7 and X.org-1.19

* Tue Oct 18 2016 Sérgio Basto <sergio@serjux.com> - 5.1.8-1
- Update VBox to 5.1.8

* Sat Oct 15 2016 Sérgio Basto <sergio@serjux.com> - 5.1.6-6
- Minor issues

* Thu Oct 13 2016 Sérgio Basto <sergio@serjux.com> - 5.1.6-5
- Add more one ifdef in VirtualBox-5.0.18-xserver_guest.patch

* Wed Oct 12 2016 Sérgio Basto <sergio@serjux.com> - 5.1.6-4
- Some fixes:
  Add full description on %{name} package.
  Fix requires on sub-packages to %{name}-server.
  Add %{?_isa}.
  Do not provide %{name}-gui, we don't use it and it is ambiguous.
- Refactor the patch VirtualBox-5.0.18-xserver_guest.patch
  using VBOX_USE_SYSTEM_XORG_HEADERS instead drop and replace code, for
  include upstream, also add MIT License.

* Sat Oct 08 2016 Sérgio Basto <sergio@serjux.com> - 5.1.6-3
- rfbz#1169 v2, use another sub-package schema.
  Core sub-package now is called server and main package is Qt part (as end user
  expect). Also is more simple deal with dependencies.
- Add vboxpci to rmmod instructions.
- Remove one line that belongs to akmods process.
- Just building kernel driver for X.Org Server fix building with X.Org Server
  1.19 (guest-additions).

* Thu Sep 15 2016 Sérgio Basto <sergio@serjux.com> - 5.1.6-2
- Packaging:Scriptlets review Systemd, Icon Cache, mimeinfo and desktop-database
- Add back RPMFusion strings to VBox.sh it is used on /usr/bin/VBox
- Create VirtualBox-qt sub-package rfbz#1169
- Create VirtualBox-webservice in a sub-package
- Add python things to python sub-package
- Upstream rules:
    60-vboxguest.rules change user to vboxadd security reasons
    Add a group "vboxsf" for Shared Folders access
- Add Mageia fix revert-VBox.sh.patch
- Add Mageia support
- Update descriptions
- Review Scriptlets for starting vboxservice.service in guest-additions
  https://fedoraproject.org/wiki/Starting_services_by_default
- Adjust vboxdrv.rules and move to 60-vboxdrv.rules as has upstream.
- Remove Encoding key on .desktop files, Encoding key is deprecated.
- Add a new launcher, VBoxBugReport and reorder launchers as upstream spec
- Move more files to sub-packages.

* Tue Sep 13 2016 Sérgio Basto <sergio@serjux.com> - 5.1.6-1
- Update VBox to 5.1.6

* Sat Sep 10 2016 Sérgio Basto <sergio@serjux.com> - 5.1.4-4
- Fix for kernel 4.8.0-rc5

* Wed Sep 07 2016 Sérgio Basto <sergio@serjux.com> - 5.1.4-3
- Fixes for linux kernel-4.8-rc4, fixes from openSUSE
  https://build.opensuse.org/package/show/Virtualization/virtualbox

* Tue Sep 06 2016 Sérgio Basto <sergio@serjux.com> - 5.1.4-2
- Enable webservice with fix of patch 02-gsoap-build-fix, add patch to allow
  gcc-6.2 and add patch 29-fix-ftbfs-as-needed from Debian

* Sun Sep 04 2016 Sérgio Basto <sergio@serjux.com> - 5.1.4-1
- Update VBox to 5.1.4
- Sat Jul 16 2016 Rok Mandeljc <rok.mandeljc@gmail.com>
  - Fixed the 64-bit lib suffix in /usr/bin/VirtualBox so that it finds the
      VirtualBox installation instead of ending up in infinite call loop
  - Update VirtualBox to 5.1.0
  - Drop upstream patches, rebase the rest
  - Add Qt5 dependencies

* Sun Sep 04 2016 Leigh Scott <leigh123linux@googlemail.com> - 5.0.26-2
- Rebuild for new libvpx version

* Mon Jul 18 2016 Sérgio Basto <sergio@serjux.com> - 5.0.26-1
- Update to 5.0.26

* Tue Jun 28 2016 Sérgio Basto <sergio@serjux.com> - 5.0.24-1
- Update VirtualBox to 5.0.24

* Fri Jun 24 2016 Sérgio Basto <sergio@serjux.com> - 5.0.22-2
- Add VirtualBox-5.0.22-guest_soname.patch, do not hack SONAME for
  VBoxOGL and VBoxEGL in guest-additions.

* Fri Jun 24 2016 Sérgio Basto <sergio@serjux.com> - 5.0.22-1
- Update VirtualBox to 5.0.22

* Thu Apr 28 2016 Sérgio Basto <sergio@serjux.com> - 5.0.20-1
- Update VirtualBox to 5.0.20

* Sun Apr 24 2016 Sérgio Basto <sergio@serjux.com> - 5.0.18-3
- Fix Documentation

* Sat Apr 23 2016 Sérgio Basto <sergio@serjux.com> - 5.0.18-2
- Fixed VirtualBox-kmod.spec.tmpl
- And rename package guest to guest-additions as Mageia distro is a better,
  name, imo.

* Tue Apr 19 2016 Sérgio Basto <sergio@serjux.com> - 5.0.18-1
- Update to 5.0.18
- Update python packaging.

* Mon Apr 04 2016 Sérgio Basto <sergio@serjux.com> - 5.0.17-6.106108
- More guest improvements and fixes

* Fri Apr 01 2016 Sérgio Basto <sergio@serjux.com> - 5.0.17-5.106108
- Do not install vboxvideo_drv.so, instead vboxvideo.ko.

* Wed Mar 30 2016 Sérgio Basto <sergio@serjux.com> - 5.0.17-4.106108
- Remove vboxvideo.ko for VirtualBox-guest r106140

* Thu Mar 24 2016 Sérgio Basto <sergio@serjux.com> - 5.0.17-3.106108
- Use upstream patch VirtualBox-5.0.17-r106108-r106140.patch

* Mon Mar 21 2016 Sérgio Basto <sergio@serjux.com> - 5.0.17-2.106108
- Add one upstream patch VirtualBox-5.0.17-r106108-r106114.patch

* Sat Mar 19 2016 Sérgio Basto <sergio@serjux.com> - 5.0.17-1.106108
- Building new Guest Additions for Linux guests.

* Sat Mar 12 2016 Sérgio Basto <sergio@serjux.com> - 5.0.16-3
- Package review with upstream RPM, better organization.
- Delete source8 not in use since 2009.
- Fix some errors: VBoxNetNAT permissions, preserve components symlinks
- vnc don't have snippet to install, disable it (to fix later).
- Add notes to add service vboxautostart and to install rdesktop-vrdp.

* Fri Mar 11 2016 Sérgio Basto <sergio@serjux.com>- 5.0.16-2
- Add GCC6 fixes to compile on F24, still doesn't build on rawhide because glibc
https://www.virtualbox.org/ticket/15205#comment:8
- Use bcond_with and bcond_without macros (see details and how it works on
  /lib/rpm/macros)
- Update help strings to use dnf and akmods.

* Fri Mar 04 2016 Sérgio Basto <sergio@serjux.com> - 5.0.16-1
- Update VirtualBox to 5.0.16

* Wed Jan 20 2016 Sérgio Basto <sergio@serjux.com> - 5.0.14-1
- Update VirtualBox to 5.0.14

* Mon Dec 21 2015 Sérgio Basto <sergio@serjux.com> - 5.0.12-1
- Update VirtualBox to 5.0.12
- Silent warning: Macro expanded in comment.
- Fix VirtualBox-4.3.0-no-bundles.patch and VirtualBox-5.0.12-strings.patch

* Thu Nov 12 2015 Sérgio Basto <sergio@serjux.com> - 5.0.10-1
- Update VirtualBox to 5.0.10

* Thu Oct 22 2015 Sérgio Basto <sergio@serjux.com> - 5.0.8-1
- Update to 5.0.8
- Refactor no-bundles.patch and strings.patch

* Mon Oct 05 2015 Sérgio Basto <sergio@serjux.com> - 5.0.6-1
- Update to VirtualBox-5.0.6, without strings patch (need be rebased)

* Wed Sep 30 2015 Sérgio Basto <sergio@serjux.com> - 5.0.4-2.4
- enabled doc, vnc, and webservices
- Drop beramono patch

* Tue Sep 29 2015 Sérgio Basto <sergio@serjux.com> - 5.0.4-2
- Drop 32bits patch

* Wed Jul 15 2015 Sérgio Basto <sergio@serjux.com> - 4.3.30-1
- Update to 4.3.30

* Wed May 13 2015 Sérgio Basto <sergio@serjux.com> - 4.3.28-1
- Update to 4.3.28 .
- Drop diff_smap_4.patch .

* Mon May 04 2015 Sérgio Basto <sergio@serjux.com> - 4.3.26-3
- Added diff_smap_4.patch from https://www.virtualbox.org/ticket/13961 ,
  may fix problems for kernel >= 3.19, I still need to disable 3D to run plasma 5
  ( https://forums.virtualbox.org/viewtopic.php?f=6&t=64452&start=15#p320557 )

* Mon May 04 2015 Sérgio Basto <sergio@serjux.com> - 4.3.26-2
- Rebuilt for F22 new xorg ABI
- Allow build with gcc 5.1

* Tue Mar 24 2015 Leigh Scott <leigh123linux@googlemail.com> - 4.3.26-1
- New upstream release .

* Fri Dec 26 2014 Sérgio Basto <sergio@serjux.com> - 4.3.20-3
- Improved strings.patch asking to install kmods VirtualBox and also instructions for devel versions.
- Improved description of VirtualBox-guest, alerting to not install on Host, one conclusion on rfbz #3425 .

* Sun Dec 21 2014 Sérgio Basto <sergio@serjux.com> - 4.3.20-2
- Moved files from /etc/modules-load.d/ to /usr/lib/modules-load.d/, fix rfbz #3469 .
- Also moved files from /etc/udev/rules.d/ to /usr/lib/udev/rules.d/ and removed %config directive .
- s/$RPM_BUILD_ROOT/%{buildroot}/g
- Added %{_prefix} to /lib/udev/ .
- Moved pam_vbox.so from %{_lib}/security/ to %{_libdir}/security/ .

* Sun Nov 23 2014 Sérgio Basto <sergio@serjux.com> - 4.3.20-1
- New upstream release .

* Sat Oct 11 2014 Sérgio Basto <sergio@serjux.com> - 4.3.18-1
- New upstream release .
- Removed trailing whitespaces .
- Refactor VirtualBox-4.3.0-VBoxGuestLib.patch to try upstreaming .

* Wed Sep 10 2014 Sérgio Basto <sergio@serjux.com> - 4.3.16-1
- New upstream release .
- Fixed VirtualBox-4.3.0-VBoxGuestLib.patch .

* Sat Aug 23 2014 Sérgio Basto <sergio@serjux.com> - 4.3.14-2
- Rebuild for new gcc https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 15 2014 Sérgio Basto <sergio@serjux.com> - 4.3.14-1
- New upstream release .
- Unbundle kBuild, since KBuild from fedora is working again.

* Fri May 16 2014 Sérgio Basto <sergio@serjux.com> - 4.3.12-1
- New upstream release .
- Rename and split X11 and mesa (for guest) patches .

* Fri May 02 2014 Sérgio Basto <sergio@serjux.com> - 4.3.10-2
- Rebuild for new x11-xorg-server

* Mon Mar 31 2014 Sérgio Basto <sergio@serjux.com> - 4.3.10-1
- In vboxvideo guest drive, don't patch the source code of Mesa part that use glapi and use bundled
  x11include/mesa-7.2 headers of Mesa, which btw rawhide doesn't have it, F20 have glapi in xorg-x11-server-source, but by what
  I saw, seems is not correct use it.
- New upstream release
- Drop upstream patch "39-fix-wrong-vboxvideo_drv-source.patch"

* Sun Mar 16 2014 Sérgio Basto <sergio@serjux.com> - 4.3.8-2
- some cleanups and improvements.

* Thu Mar 13 2014 Sérgio Basto <sergio@serjux.com> - 4.3.8-1
- Update to 4.3.8, need an upstream patch
  39-fix-wrong-vboxvideo_drv-source.patch
- No need patch Config.kmk in VirtualBox-4.3.6-mesa.patch
- small adjustments in others patches.

* Wed Dec 25 2013 Sérgio Basto <sergio@serjux.com> - 4.3.6-4
- Update VirtualBox-4.3-mesa.patch, for guest drives and for Xorg-x11-server-1.14.99 in rawhide, glx internals "fixes" completely removed, eliminating BuildRequires of xorg-x11-server-source.
  Also add to VBoxOGL_LIBS libXcomposite, libXdamage etc of the system.
- Disable webservice for rawhide, problems reported upstream with new gsoap version.

* Sat Dec 21 2013 Nicolas Chauvet <kwizart@gmail.com> - 4.3.6-3
- Rebuilt after branching

* Sat Dec 21 2013 Nicolas Chauvet <kwizart@gmail.com> - 4.3.6-2
- Rebuilt after branching

* Wed Dec 18 2013 Sérgio Basto <sergio@serjux.com> - 4.3.6-1
- New upstream release, a maintenance release of
VirtualBox 4.3 which improves stability and fixes regressions.

* Sat Nov 30 2013 Sérgio Basto <sergio@serjux.com> - 4.3.4-1
- New upstream release, a maintenance release of
VirtualBox 4.3 which improves stability and fixes regressions.

* Sat Nov 02 2013 Sérgio Basto <sergio@serjux.com> - 4.3.2-1
- New upstream release, bugfix release.

* Mon Oct 28 2013 Sérgio Basto <sergio@serjux.com> - 4.3.0-1
- New upstream release.
- Refactor patches VirtualBox-4.3.0-32bit.patch, VirtualBox-4.3.0-libcxx.patch, VirtualBox-4.3.0-mesa.patch,
VirtualBox-4.3.0-no-bundles.patch, VirtualBox-4.3.0-testmangle.patch and VirtualBox-4.3.0-VBoxGuestLib.patch
- Took the opportunity to do a review: add some new binaries, need to review it again .

* Sun Sep 29 2013 Sérgio Basto <sergio@serjux.com> - 4.2.18-2
- Additions/linux: fix shared folders for Linux 3.11

* Fri Sep 20 2013 Sérgio Basto <sergio@serjux.com> - 4.2.18-1
- New upstream release.

* Sun Sep 01 2013 Sérgio Basto <sergio@serjux.com> - 4.2.16-2
- fixes for Kernel 3.11:
    https://www.virtualbox.org/changeset/47484/vbox/trunk
    and
    https://www.virtualbox.org/changeset/47588/vbox/trunk

* Fri Jul 05 2013 Sérgio Basto <sergio@serjux.com> - 4.2.16-1
- New upstream release.

* Sun Jun 30 2013 Sérgio Basto <sergio@serjux.com> - 4.2.14-2
- Bugfix, forgot rename *.modules to *.conf, as defined in modules-load.d(5) .

* Sat Jun 29 2013 Sérgio Basto <sergio@serjux.com> - 4.2.14-1
- Change strings instructions to load modules.
- New upstream release.
- Drop gcc-4.8 patch.

* Sun May 12 2013 Sérgio Basto <sergio@serjux.com> - 4.2.12-2
- drop some Buildrequires as documented in https://www.virtualbox.org/wiki/Linux%20build%20instructions
- Use systemd-modules-load.service instead fedora-loadmodules.service ( Load legacy module
  configuration ).

* Mon Apr 15 2013 Sérgio Basto <sergio@serjux.com> - 4.2.12-1
- New upstream release.

* Sat Mar 16 2013 Sérgio Basto <sergio@serjux.com> - 4.2.10-1
- New upstream release.
- Drop 00-vboxvideo.conf on guest X configuration, because this is fixed a long time ago, but we keep commented just in case.
- Drop upstreamed patch VirtualBox-4.2.8-Linux_3.9.0_rc0_compile_fix.patch .
- Modified noupdate.patch as reflection on bug rfbz #2722, to check updates one time a week and ask for updates of extensions pack and VBoxGuestAdditions. We should also review strings for better dialogs.

* Thu Mar 07 2013 Sérgio Basto <sergio@serjux.com> - 4.2.8-2
- Added upstreamed patch for kernels 3.9, "That fix will be part of the next maintenance
  release".

* Sat Mar 02 2013 Sérgio Basto <sergio@serjux.com> - 4.2.8-1
- New upstream release.
- Small fix on VirtualBox-4.2.0-mesa.patch .

* Sat Feb 23 2013 Sérgio Basto <sergio@serjux.com> - 4.2.6-6
- Enable build with gcc 4.8 .

* Mon Feb 11 2013 Sérgio Basto <sergio@serjux.com> - 4.2.6-5
- Remove if clause in Patch10, may make different src.rpms, my fault, rfbz #2679 .

* Sat Feb 02 2013 Sérgio Basto <sergio@serjux.com> - 4.2.6-4
- Back to old udev commands, systemctl just does the same devadm commands but doesn't help much.
- and add --action=add to udevadm trigger --subsystem-match=usb .
- vboxweb.service fixes.

* Sat Jan 26 2013 Sérgio Basto <sergio@serjux.com> - 4.2.6-3
- fix for rfbz #2662, systemd of F18 changed names of udev services.

* Tue Jan 15 2013 Sérgio Basto <sergio@serjux.com> - 4.2.6-2
- Re enable_docs after add some BuildRequires of new texlive.
- VBoxGuestLib is not need for new X11-xorg, so no compile instead patch source to
  build with system sources.
- Delete source bundles before patching sources and adjustments on the corresponding patches.
- VirtualBox-4.2.0-libcxx.patch minor improvements.

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
https://www.virtualbox.org/changeset/43588/vbox, allow compile vboxvideo with system headers, and
"As vboxmouse_drv is not needed at all for X.Org Server 1.7 and later do not build it".
- enable-webservice on F17 and lower (stables) and disable-docs on F18 and rawhide, can't build it
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
- Another try to compile with 32-bits support on x86_64.

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
- fix requires kmod, with version with prereleases.

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
- F17 mesa patch, fix compile fakedri and unbundle part of mesa sources, unbundle mesa source must be tested.

* Fri Apr 13 2012 Sérgio Basto <sergio@serjux.com> - 4.1.12-2
- F15 patch gsoap 2.7 which pkg-config gsoapssl++ --libs don't have -lssl -lcrypto
- F17 kBuild workaround, but still not build in F17,
  https://bugs.freedesktop.org/show_bug.cgi?id=47971 .

* Tue Apr 3 2012 Sérgio Basto <sergio@serjux.com> - 4.1.12-1
- New release.
- drop buildroot
- drop the backported patch.

* Fri Mar 23 2012 Sérgio Basto <sergio@serjux.com> - 4.1.10-1
- New release.
- Upstream says that java stuff is fixed, https://www.virtualbox.org/ticket/9848#comment:5
- Upstream says that have compile fixes for kernel 3.3-rc1 (in changelog).
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
- Replace occurrences of 'vboxdrv setup'

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
- remove unneeded recompiler patch
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
