# Use system nspr/nss?

%define system_nss        1

# Build as a debug package?
%define debug_build       0

%if 0%{?fedora} < 20
%define system_sqlite 0
%define system_ffi    0
%else
%define system_sqlite 1
%define system_ffi    1
%endif

%define build_langpacks 1

%if %{?system_nss}
%global nspr_version 4.10.6
%global nspr_build_version %(pkg-config --silence-errors --modversion nspr 2>/dev/null || echo 65536)
%global nss_version 3.16.2.3
%global nss_build_version %(pkg-config --silence-errors --modversion nss 2>/dev/null || echo 65536)
%endif

%define cairo_version 1.8.8
%define freetype_version 2.1.9

%if %{?system_sqlite}
%define sqlite_version 3.8.4.2
# The actual sqlite version (see #480989):
%global sqlite_build_version %(pkg-config --silence-errors --modversion sqlite3 2>/dev/null || echo 65536)
%endif

%define libnotify_version 0.4
%global libvpx_version 1.3.0
%define _default_patch_fuzz 2

%define thunderbird_app_id \{3550f703-e582-4d05-9a08-453d09bdfdc6\} 
# Bump one with each minor lightning release
%define gdata_version 1.9
%define gdata_version_internal 0.2
%global gdata_extname %{_libdir}/mozilla/extensions/{3550f703-e582-4d05-9a08-453d09bdfdc6}/{a62ef8ec-5fdc-40c2-873c-223b8a6925cc}

# The tarball is pretty inconsistent with directory structure.
# Sometimes there is a top level directory.  That goes here.
#
# IMPORTANT: If there is no top level directory, this should be 
# set to the cwd, ie: '.'
%define tarballdir   comm-esr38
%define objdir       objdir
%define mozappdir    %{_libdir}/%{name}

%define official_branding 1
# enable crash reporter only for iX86
%ifarch %{ix86} x86_64
%define enable_mozilla_crashreporter 1
%else
%define enable_mozilla_crashreporter 0
%endif


Summary:        Mozilla Thunderbird mail/newsgroup client
Name:           thunderbird
Version:        38.2.0
Release:        2%{?dist}
URL:            http://www.mozilla.org/projects/thunderbird/
License:        MPLv1.1 or GPLv2+ or LGPLv2+
Group:          Applications/Internet
Source0:        ftp://ftp.mozilla.org/pub/thunderbird/releases/%{version}%{?pre_version}/source/thunderbird-%{version}%{?pre_version}.source.tar.bz2
%if %{build_langpacks}
Source1:        thunderbird-langpacks-%{version}-20150819.tar.xz
%endif
# Locales for lightning
Source2:        l10n-lightning-%{version}.tar.xz
Source3:        mklangsource.sh

Source10:       thunderbird-mozconfig
Source11:       thunderbird-mozconfig-branded
Source12:       thunderbird-redhat-default-prefs.js
Source20:       thunderbird.desktop
Source21:       thunderbird.sh.in

# Mozilla (XULRunner) patches
Patch0:         thunderbird-install-dir.patch
Patch9:         mozilla-build-arm.patch

# Build patches
Patch100:       thunderbird-objdir.patch
Patch101:        build-nspr-prbool.patch
Patch102:        build-werror.patch
Patch103:       rhbz-1219542-s390-build.patch

# Linux specific
Patch200:       thunderbird-enable-addons.patch

# PPC fixes
Patch300:       xulrunner-24.0-jemalloc-ppc.patch

# Fedora specific patches
Patch400:       rhbz-966424.patch
Patch402:       rhbz-1014858.patch
# libvpx no longer has compat defines, use the current ones

%if %{official_branding}
# Required by Mozilla Corporation

%else
# Not yet approved by Mozillla Corporation

%endif

%if %{?system_nss}
BuildRequires:  nss-static >= %{nss_version}
BuildRequires:  nspr-devel >= %{nspr_version}
BuildRequires:  nss-devel >= %{nss_version}
Requires:       nspr >= %{nspr_build_version}
Requires:       nss >= %{nss_build_version}
%endif
BuildRequires:  cairo-devel >= %{cairo_version}
BuildRequires:  libnotify-devel >= %{libnotify_version}
BuildRequires:  libpng-devel
BuildRequires:  libjpeg-devel
BuildRequires:  zip
BuildRequires:  bzip2-devel
BuildRequires:  zlib-devel
BuildRequires:  libIDL-devel
BuildRequires:  gtk2-devel
BuildRequires:  krb5-devel
BuildRequires:  pango-devel
BuildRequires:  freetype-devel >= %{freetype_version}
BuildRequires:  libXt-devel
BuildRequires:  libXrender-devel
BuildRequires:  hunspell-devel
%if %{?system_sqlite}
BuildRequires:  sqlite-devel >= %{sqlite_version}
Requires:       sqlite >= %{sqlite_build_version}
%endif
%if %{?system_ffi}
BuildRequires:  libffi-devel
%endif
BuildRequires:  startup-notification-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  autoconf213
BuildRequires:  desktop-file-utils
BuildRequires:  libcurl-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  libvpx-devel >= %{libvpx_version}
Requires:       libvpx >= %{libvpx_version}
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  libicu-devel
Requires:       mozilla-filesystem
Obsoletes:      thunderbird-lightning
Provides:       thunderbird-lightning


%description
Mozilla Thunderbird is a standalone mail and newsgroup client.

%if %{enable_mozilla_crashreporter}
%global moz_debug_prefix %{_prefix}/lib/debug
%global moz_debug_dir %{moz_debug_prefix}%{mozappdir}
%global uname_m %(uname -m)
%global symbols_file_name %{name}-%{version}.en-US.%{_os}-%{uname_m}.crashreporter-symbols.zip
%global symbols_file_path %{moz_debug_dir}/%{symbols_file_name}
%global _find_debuginfo_opts -p %{symbols_file_path} -o debugcrashreporter.list
%global crashreporter_pkg_name mozilla-crashreporter-%{name}-debuginfo
%package -n %{crashreporter_pkg_name}
Summary: Debugging symbols used by Mozilla's crash reporter servers
Group: Development/Debug
%description -n %{crashreporter_pkg_name}
This package provides debug information for XULRunner, for use by
Mozilla's crash reporter servers.  If you are trying to locally
debug %{name}, you want to install %{name}-debuginfo instead.
%files -n %{crashreporter_pkg_name} -f debugcrashreporter.list
%defattr(-,root,root)
%endif

%global tb_version %{version}

%package lightning-gdata
Summary:        Lightning data provider for Google Calendar
Version:        %{gdata_version}.%{gdata_version_internal}
Requires:       %{name}%{?_isa} = %{tb_version}-%{release}

%description lightning-gdata
This extension allows Lightning to read and write events to a Google Calendar.

Please read http://wiki.mozilla.org/Calendar:GDATA_Provider for more details
and before filing a bug. Also, be sure to visit the dicussion forums, maybe
your bug already has a solution!


%prep
%setup -q -c
cd %{tarballdir}

%patch0   -p1 -b .dir
%patch100 -p2 -b .objdir

# Mozilla (XULRunner) patches
cd mozilla
%patch9   -p2 -b .arm
%patch300 -p2 -b .852698
%patch102 -p2 -b .build-werror
%patch101 -p1 -b .nspr-prbool
%ifarch s390
%patch103 -p1 -b .rhbz-1219542-s390-build
%endif
%patch400 -p1 -b .966424
%patch402 -p1 -b .rhbz-1014858

cd ..
%patch200 -p1 -b .addons

%if %{official_branding}
# Required by Mozilla Corporation

%else
# Not yet approved by Mozilla Corporation

%endif

%{__rm} -f .mozconfig
%{__cp} %{SOURCE10} .mozconfig
%if %{official_branding}
%{__cat} %{SOURCE11} >> .mozconfig
%endif

%if %{?system_nss}
echo "ac_add_options --with-system-nspr" >> .mozconfig
echo "ac_add_options --with-system-nss" >> .mozconfig
%else
echo "ac_add_options --without-system-nspr" >> .mozconfig
echo "ac_add_options --without-system-nss" >> .mozconfig
%endif

# s390(x) fails to start with jemalloc enabled
%ifarch s390 s390x
echo "ac_add_options --disable-jemalloc" >> .mozconfig
%endif

%if %{?system_sqlite}
echo "ac_add_options --enable-system-sqlite"  >> .mozconfig
%else
echo "ac_add_options --disable-system-sqlite" >> .mozconfig
%endif

%if %{?system_ffi}
echo "ac_add_options --enable-system-ffi" >> .mozconfig
%endif

%if %{?debug_build}
echo "ac_add_options --enable-debug" >> .mozconfig
echo "ac_add_options --disable-optimize" >> .mozconfig
%else
echo "ac_add_options --disable-debug" >> .mozconfig
echo "ac_add_options --enable-optimize" >> .mozconfig
%endif

%ifarch %{arm}
echo "ac_add_options --disable-elf-hack" >> .mozconfig
%endif

%ifnarch %{ix86} x86_64
echo "ac_add_options --disable-webrtc" >> .mozconfig
%endif

%ifarch armv7hl
echo "ac_add_options --with-arch=armv7-a" >> .mozconfig
echo "ac_add_options --with-float-abi=hard" >> .mozconfig
echo "ac_add_options --with-fpu=vfpv3-d16" >> .mozconfig
echo "ac_add_options --disable-elf-hack" >> .mozconfig
%endif
%ifarch armv7hnl
echo "ac_add_options --with-arch=armv7-a" >> .mozconfig
echo "ac_add_options --with-float-abi=hard" >> .mozconfig
echo "ac_add_options --with-fpu=neon" >> .mozconfig
echo "ac_add_options --disable-elf-hack" >> .mozconfig
echo "ac_add_options --disable-ion" >> .mozconfig
echo "ac_add_options --disable-yarr-jit" >> .mozconfig
%endif
%ifarch armv5tel
echo "ac_add_options --with-arch=armv5te" >> .mozconfig
echo "ac_add_options --with-float-abi=soft" >> .mozconfig
echo "ac_add_options --disable-elf-hack" >> .mozconfig
echo "ac_add_options --disable-ion" >> .mozconfig
echo "ac_add_options --disable-yarr-jit" >> .mozconfig
%endif

# install lightning langpacks
cd ..
%{__tar} xf %{SOURCE2}
cd -
#===============================================================================

%build
%if %{?system_sqlite}
# Do not proceed with build if the sqlite require would be broken:
# make sure the minimum requirement is non-empty, ...
sqlite_version=$(expr "%{sqlite_version}" : '\([0-9]*\.\)[0-9]*\.') || exit 1
# ... and that major number of the computed build-time version matches:
case "%{sqlite_build_version}" in
  "$sqlite_version"*) ;;
  *) exit 1 ;;
esac
%endif

cd %{tarballdir}

# Update the various config.guess to upstream release for aarch64 support
find ./ -name config.guess -exec cp /usr/lib/rpm/config.guess {} ';'

# -fpermissive is needed to build with gcc 4.6+ which has become stricter
#
# Mozilla builds with -Wall with exception of a few warnings which show up
# everywhere in the code; so, don't override that.
#
# Disable C++ exceptions since Mozilla code is not exception-safe
# 
MOZ_OPT_FLAGS=$(echo "$RPM_OPT_FLAGS -fpermissive" | \
                      %{__sed} -e 's/-Wall//')
#rhbz#1037353
MOZ_OPT_FLAGS="$MOZ_OPT_FLAGS -Wformat-security -Wformat -Werror=format-security"
%if %{?debug_build}
MOZ_OPT_FLAGS=$(echo "$MOZ_OPT_FLAGS" | %{__sed} -e 's/-O2//')
%endif
%ifarch s390
MOZ_OPT_FLAGS=$(echo "$MOZ_OPT_FLAGS" | %{__sed} -e 's/-g/-g1/')
# If MOZ_DEBUG_FLAGS is empty, firefox's build will default it to "-g" which
# overrides the -g1 from line above and breaks building on s390
# (OOM when linking, rhbz#1238225)
export MOZ_DEBUG_FLAGS=" "
%endif
%ifarch s390 %{arm} ppc aarch64 i686
MOZ_LINK_FLAGS="-Wl,--no-keep-memory -Wl,--reduce-memory-overheads"
%endif

export CFLAGS=`echo $MOZ_OPT_FLAGS |sed -e 's/-fpermissive//g'`
export CXXFLAGS=$MOZ_OPT_FLAGS
export LDFLAGS=$MOZ_LINK_FLAGS

export PREFIX='%{_prefix}'
export LIBDIR='%{_libdir}'

MOZ_SMP_FLAGS=-j1
# On x86 architectures, Mozilla can build up to 4 jobs at once in parallel,
# however builds tend to fail on other arches when building in parallel.
%ifarch %{ix86} x86_64 ppc %{power64} aarch64
[ -z "$RPM_BUILD_NCPUS" ] && \
     RPM_BUILD_NCPUS="`/usr/bin/getconf _NPROCESSORS_ONLN`"
[ "$RPM_BUILD_NCPUS" -ge 2 ] && MOZ_SMP_FLAGS=-j2
[ "$RPM_BUILD_NCPUS" -ge 4 ] && MOZ_SMP_FLAGS=-j4
[ "$RPM_BUILD_NCPUS" -ge 8 ] && MOZ_SMP_FLAGS=-j8
%endif

make -f client.mk build STRIP="/bin/true" MOZ_MAKE_FLAGS="$MOZ_SMP_FLAGS"

# Package l10n files
cd %{objdir}/calendar/lightning
grep -v 'osx' ../../../calendar/locales/shipped-locales | while read lang x
do
   make AB_CD=en-US L10N_XPI_NAME=lightning libs-$lang
done
# install l10n files
make tools
cd -

# create debuginfo for crash-stats.mozilla.com
%if %{enable_mozilla_crashreporter}
make -C %{objdir} buildsymbols
%endif

#===============================================================================

%install
cd %{tarballdir}/%{objdir}

DESTDIR=$RPM_BUILD_ROOT make install

cd ..

# install icons
for s in 16 22 24 32 48 256; do
    %{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${s}x${s}/apps
    %{__cp} -p other-licenses/branding/%{name}/mailicon${s}.png \
               $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${s}x${s}/apps/thunderbird.png
done


desktop-file-install --vendor mozilla \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  %{SOURCE20}


# set up the thunderbird start script
rm -f $RPM_BUILD_ROOT/%{_bindir}/thunderbird
%{__cat} %{SOURCE21}  > $RPM_BUILD_ROOT%{_bindir}/thunderbird
%{__chmod} 755 $RPM_BUILD_ROOT/%{_bindir}/thunderbird

# set up our default preferences
%{__cat} %{SOURCE12} | %{__sed} -e 's,THUNDERBIRD_RPM_VR,%{tb_version}-%{release},g' > \
        $RPM_BUILD_ROOT/rh-default-prefs
%{__install} -D $RPM_BUILD_ROOT/rh-default-prefs $RPM_BUILD_ROOT/%{mozappdir}/greprefs/all-redhat.js
%{__install} -D $RPM_BUILD_ROOT/rh-default-prefs $RPM_BUILD_ROOT/%{mozappdir}/defaults/pref/all-redhat.js
%{__rm} $RPM_BUILD_ROOT/rh-default-prefs

%{__rm} -f $RPM_BUILD_ROOT%{_bindir}/thunderbird-config

# own mozilla plugin dir (#135050)
%{__mkdir_p} $RPM_BUILD_ROOT%{_libdir}/mozilla/plugins

# own extension directories
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/mozilla/extensions/%{thunderbird_app_id}
%{__mkdir_p} $RPM_BUILD_ROOT%{_libdir}/mozilla/extensions/%{thunderbird_app_id}

# Install langpacks
%{__rm} -f %{name}.lang # Delete for --short-circuit option
touch %{name}.lang
%if %{build_langpacks}
%{__mkdir_p} $RPM_BUILD_ROOT%{mozappdir}/langpacks
%{__tar} xf %{SOURCE1}
for langpack in `ls thunderbird-langpacks/*.xpi`; do
  language=`basename $langpack .xpi`
  extensionID=langpack-$language@thunderbird.mozilla.org

  language=`echo $language | sed -e 's/-/_/g'`
  %{__install} -m 644 ${langpack} $RPM_BUILD_ROOT%{mozappdir}/langpacks/${extensionID}.xpi
  echo "%%lang($language) %{mozappdir}/langpacks/${extensionID}.xpi" >> %{name}.lang
done
%{__rm} -rf thunderbird-langpacks
%endif # build_langpacks

# Get rid of devel package and its debugsymbols
%{__rm} -rf $RPM_BUILD_ROOT%{_libdir}/%{name}-devel-%{tb_version}

# Copy over the LICENSE
cd mozilla
install -c -m 644 LICENSE $RPM_BUILD_ROOT%{mozappdir}
cd -

# Use the system hunspell dictionaries
%{__rm} -rf $RPM_BUILD_ROOT/%{mozappdir}/dictionaries
ln -s %{_datadir}/myspell $RPM_BUILD_ROOT%{mozappdir}/dictionaries

# ghost files
%{__mkdir_p} $RPM_BUILD_ROOT%{mozappdir}/components
touch $RPM_BUILD_ROOT%{mozappdir}/components/compreg.dat
touch $RPM_BUILD_ROOT%{mozappdir}/components/xpti.dat

# Add debuginfo for crash-stats.mozilla.com 
%if %{enable_mozilla_crashreporter}
%{__mkdir_p} $RPM_BUILD_ROOT/%{moz_debug_dir}
%{__cp} %{objdir}/dist/%{symbols_file_name} $RPM_BUILD_ROOT/%{moz_debug_dir}
%endif

# Register as an application to be visible in the software center
#
# NOTE: It would be *awesome* if this file was maintained by the upstream
# project, translated and installed into the right place during `make install`.
#
# See http://www.freedesktop.org/software/appstream/docs/ for more details.
#
mkdir -p $RPM_BUILD_ROOT%{_datadir}/appdata
cat > $RPM_BUILD_ROOT%{_datadir}/appdata/mozilla-thunderbird.appdata.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!-- Copyright 2014 Richard Hughes <richard@hughsie.com> -->
<!--
BugReportURL: https://bugzilla.mozilla.org/show_bug.cgi?id=1071065
SentUpstream: 2014-09-22
-->
<application>
  <id type="desktop">mozilla-thunderbird.desktop</id>
  <metadata_license>CC0-1.0</metadata_license>
  <description>
    <p>
      Thunderbird is an email client that allows you to read, write and organise all
      of your email messages. It is compatible with most email accounts, including the
      most popular webmail services.
    </p>
    <p>
      Thunderbird is designed by Mozilla, a global community working together to make
      the Internet better. Mozilla believe that the Internet should be open, public,
      and accessible to everyone without any restrictions.
    </p>
    <ul>
      <li>Easier than ever to set up a new e-mail account</li>
      <li>Awesome search allows you to find your messages fast</li>
      <li>Thousands of add-ons give you the freedom to make Thunderbird your own</li>
    </ul>
  </description>
  <url type="homepage">http://www.mozilla.org/thunderbird/</url>
  <!--
  <screenshots>
    <screenshot type="default">https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/mozilla-thunderbird/a.png</screenshot>
  </screenshots>
  -->
  <!-- FIXME: change this to an upstream email address for spec updates
  <updatecontact>someone_who_cares@upstream_project.org</updatecontact>
   -->
</application>
EOF

# lightning-gdata
mkdir -p $RPM_BUILD_ROOT%{gdata_extname}
touch $RPM_BUILD_ROOT%{gdata_extname}/chrome.manifest

unzip -qod $RPM_BUILD_ROOT%{gdata_extname} %{objdir}/dist/xpi-stage/gdata-provider-%{gdata_version}.en-US.linux-*.xpi

#===============================================================================

%post
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

# lightning-gdata files=========================================================
%files lightning-gdata
%doc %{tarballdir}/mozilla/LEGAL %{tarballdir}/mozilla/LICENSE %{tarballdir}/mozilla/README.txt
%{gdata_extname}
#===============================================================================
%files -f %{tarballdir}/%{name}.lang
%defattr(-,root,root,-)
%attr(755,root,root) %{_bindir}/thunderbird
%{_datadir}/appdata/*.appdata.xml
%attr(644,root,root) %{_datadir}/applications/mozilla-thunderbird.desktop
%dir %{_datadir}/mozilla/extensions/%{thunderbird_app_id}
%dir %{_libdir}/mozilla/extensions/%{thunderbird_app_id}
%dir %{mozappdir}
%doc %{mozappdir}/LICENSE
%{mozappdir}/chrome
%dir %{mozappdir}/components
%ghost %{mozappdir}/components/compreg.dat
%ghost %{mozappdir}/components/xpti.dat
%{mozappdir}/components/components.manifest
%{mozappdir}/components/libdbusservice.so
%{mozappdir}/components/libmozgnome.so
%{mozappdir}/omni.ja
%{mozappdir}/plugin-container
%{mozappdir}/defaults
%{mozappdir}/dictionaries
%dir %{mozappdir}/extensions
%{mozappdir}/extensions/{972ce4c6-7e08-4474-a285-3208198ce6fd}
%dir %{mozappdir}/langpacks
%{mozappdir}/greprefs
%{mozappdir}/isp
%{mozappdir}/run-mozilla.sh
%{mozappdir}/thunderbird-bin
%{mozappdir}/thunderbird
%{mozappdir}/*.so
%{mozappdir}/platform.ini
%{mozappdir}/application.ini
%{mozappdir}/blocklist.xml
%exclude %{mozappdir}/removed-files
%{_datadir}/icons/hicolor/16x16/apps/thunderbird.png
%{_datadir}/icons/hicolor/22x22/apps/thunderbird.png
%{_datadir}/icons/hicolor/24x24/apps/thunderbird.png
%{_datadir}/icons/hicolor/256x256/apps/thunderbird.png
%{_datadir}/icons/hicolor/32x32/apps/thunderbird.png
%{_datadir}/icons/hicolor/48x48/apps/thunderbird.png
%if %{enable_mozilla_crashreporter}
%{mozappdir}/crashreporter
%{mozappdir}/crashreporter.ini
%{mozappdir}/Throbber-small.gif
%endif
%if !%{?system_nss}
%{mozappdir}/*.chk
%endif
%exclude %{_datadir}/idl/%{name}-%{tb_version}
%exclude %{_includedir}/%{name}-%{tb_version}
%{mozappdir}/chrome.manifest
%{mozappdir}/searchplugins
%{mozappdir}/dependentlibs.list
%{mozappdir}/distribution

#===============================================================================

%changelog
* Thu Aug 20 2015 Jan Horak <jhorak@redhat.com> - 38.2.0-2
- Thunderbird provides thunderbird-lightning now

* Wed Aug 19 2015 Jan Horak <jhorak@redhat.com> - 38.2.0-1
- Update to 38.2.0

* Thu Jul  9 2015 Jan Horak <jhorak@redhat.com> - 38.1.0-1
- Update to 38.1.0

* Thu Jun 18 2015 Jan Horak <jhorak@redhat.com> - 38.0.1-3
- Bundling calendar extension

* Tue Jun  9 2015 Jan Horak <jhorak@redhat.com> - 38.0.1-1
- Update to 38.0.1

* Tue May 12 2015 Martin Stransky <stransky@redhat.com> - 31.7.0-1
- Update to 31.7.0

* Mon Apr  6 2015 Tom Callaway <spot@fedoraproject.org> - 31.6.0-2
- rebuild for libvpx 1.4.0
- stop using compat defines, they went away in libvpx 1.4.0

* Tue Mar 31 2015 Jan Horak <jhorak@redhat.com> - 31.6.0-1
- Update to 31.6.0

* Thu Mar 26 2015 Richard Hughes <rhughes@redhat.com> - 31.5.0-3
- Add an AppData file for the software center

* Thu Mar 19 2015 Jan Horak <jhorak@redhat.com> - 31.5.0-2
- Fixed build flags for s390(x)

* Tue Feb 24 2015 Jan Horak <jhorak@redhat.com> - 31.5.0-1
- Update to 31.5.0

* Fri Feb 20 2015 Martin Stransky <stransky@redhat.com> - 31.4.0-2
- Fixed rhbz#1187746 - GLib allocation error
  when starting thunderbird

* Wed Jan 14 2015 Jan Horak <jhorak@redhat.com> - 31.4.0-1
- Update to 31.4.0

* Mon Jan  5 2015 Jan Horak <jhorak@redhat.com> - 31.3.0-2
- Exclude ppc64 arch for epel7

* Mon Dec  1 2014 Jan Horak <jhorak@redhat.com> - 31.3.0-1
- Update to 31.3.0

* Tue Oct 14 2014 Jan Horak <jhorak@redhat.com> - 31.2.0-1
- Update to 31.2.0

* Wed Oct 1 2014 Martin Stransky <stransky@redhat.com> - 31.1.1-2
- Sync prefs with Firefox

* Thu Sep 11 2014 Jan Horak <jhorak@redhat.com> - 31.1.1-1
- Update to 31.1.1

* Mon Sep  1 2014 Jan Horak <jhorak@redhat.com> - 31.1.0-1
- Update to 31.1.0

* Tue Aug 26 2014 Karsten Hopp <karsten@redhat.com> 31.0-5
- ppc64 patch 304 got removed and isn't required anymore (mozbz#973977)

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 31.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Aug  4 2014 Peter Robinson <pbrobinson@fedoraproject.org> 31.0-3
- Build with system FFI as per firefox/xulrunner (fixes aarch64)

* Wed Jul 30 2014 Martin Stransky <stransky@redhat.com> - 31.0-2
- Added patch for mozbz#858919

* Tue Jul 29 2014 Martin Stransky <stransky@redhat.com> - 31.0-1
- Update to 31.0

* Tue Jul 22 2014 Jan Horak <jhorak@redhat.com> - 24.7.0-1
- Update to 24.7.0

* Mon Jun  9 2014 Jan Horak <jhorak@redhat.com> - 24.6.0-1
- Update to 24.6.0

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 24.5.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 Brent Baude <baude@us.ibm.com> - 24.5.0-5
- Moving the ppc64 conditional up before the cd so it will
- apply cleanly

* Fri May 23 2014 Martin Stransky <stransky@redhat.com> - 24.5.0-4
- Added a build fix for ppc64 - rhbz#1100495

* Mon May  5 2014 Jan Horak <jhorak@redhat.com> - 24.5.0-3
- Fixed find requires

* Mon Apr 28 2014 Jan Horak <jhorak@redhat.com> - 24.5.0-1
- Update to 24.5.0

* Tue Apr 22 2014 Jan Horak <jhorak@redhat.com> - 24.4.0-2
- Added support for ppc64le

* Tue Mar 18 2014 Jan Horak <jhorak@redhat.com> - 24.4.0-1
- Update to 24.4.0

* Mon Feb  3 2014 Jan Horak <jhorak@redhat.com> - 24.3.0-1
- Update to 24.3.0

* Mon Dec 16 2013 Martin Stransky <stransky@redhat.com> - 24.2.0-4
- Fixed rhbz#1024232 - thunderbird: squiggly lines used 
  for spelling correction disappear randomly

* Fri Dec 13 2013 Martin Stransky <stransky@redhat.com> - 24.2.0-3
- Build with -Werror=format-security (rhbz#1037353)

* Wed Dec 11 2013 Martin Stransky <stransky@redhat.com> - 24.2.0-2
- rhbz#1001998 - added a workaround for system notifications

* Mon Dec  9 2013 Jan Horak <jhorak@redhat.com> - 24.2.0-1
- Update to 24.2.0

* Sat Nov 02 2013 Dennis Gilmore <dennis@ausil.us> - 24.1.0-2
- remove ExcludeArch: armv7hl

* Wed Oct 30 2013 Jan Horak <jhorak@redhat.com> - 24.1.0-1
- Update to 24.1.0

* Thu Oct 17 2013 Martin Stransky <stransky@redhat.com> - 24.0-4
- Fixed rhbz#1005611 - BEAST workaround not enabled in Firefox

* Wed Sep 25 2013 Jan Horak <jhorak@redhat.com> - 24.0-3
- Update to 24.0

* Mon Sep 23 2013 Jan Horak <jhorak@redhat.com> - 17.0.9-1
- Update to 17.0.9 ESR

* Mon Aug  5 2013 Jan Horak <jhorak@redhat.com> - 17.0.8-1
- Update to 17.0.8

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 17.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun 25 2013 Jan Horak <jhorak@redhat.com> - 17.0.7-1
- Update to 17.0.7

* Wed Jun 12 2013 Jan Horak <jhorak@redhat.com> - 17.0.6-2
- Fixed rhbz#973371 - unable to install addons

* Tue May 14 2013 Jan Horak <jhorak@redhat.com> - 17.0.6-1
- Update to 17.0.6

* Tue Apr  2 2013 Jan Horak <jhorak@redhat.com> - 17.0.5-1
- Update to 17.0.5

* Mon Mar 11 2013 Jan Horak <jhorak@redhat.com> - 17.0.4-1
- Update to 17.0.4

* Tue Feb 19 2013 Jan Horak <jhorak@redhat.com> - 17.0.3-1
- Update to 17.0.3

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 17.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 15 2013 Martin Stransky <stransky@redhat.com> - 17.0.2-3
- Added fix for NM regression (mozbz#791626)

* Tue Jan 15 2013 Jan Horak <jhorak@redhat.com> - 17.0.2-2
- Added mozilla-746112 patch to fix crash on ppc(64)

* Thu Jan 10 2013 Jan Horak <jhorak@redhat.com> - 17.0.2-1
- Update to 17.0.2

* Mon Nov 19 2012 Jan Horak <jhorak@redhat.com> - 17.0-1
- Update to 17.0

* Mon Oct 29 2012 Jan Horak <jhorak@redhat.com> - 16.0.2-1
- Update to 16.0.2

* Tue Oct 16 2012 Jan Horak <jhorak@redhat.com> - 16.0.1-2
- Fixed nss and nspr versions

* Thu Oct 11 2012 Jan Horak <jhorak@redhat.com> - 16.0.1-1
- Update to 16.0.1

* Tue Oct  9 2012 Jan Horak <jhorak@redhat.com> - 16.0-1
- Update to 16.0

* Tue Sep 18 2012 Dan Horák <dan[at]danny.cz> - 15.0.1-3
- Added fix for rhbz#855923 - TB freezes on Fedora 18 for PPC64

* Fri Sep 14 2012 Martin Stransky <stransky@redhat.com> - 15.0.1-2
- Added build flags for second arches

* Tue Sep 11 2012 Jan Horak <jhorak@redhat.com> - 15.0.1-1
- Update to 15.0.1

* Fri Sep  7 2012 Jan Horak <jhorak@redhat.com> - 15.0-2
- Added workaround fix for PPC (rbhz#852698)

* Mon Aug 27 2012 Jan Horak <jhorak@redhat.com> - 15.0-1
- Update to 15.0

* Wed Aug 1 2012 Martin Stransky <stransky@redhat.com> - 14.0-4
- Removed StartupWMClass (rhbz#844863)
- Fixed -g parameter
- Removed thunderbird-devel before packing to avoid debugsymbols duplicities (rhbz#823940)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 17 2012 Jan Horak <jhorak@redhat.com> - 14.0-1
- Update to 14.0

* Fri Jun 15 2012 Jan Horak <jhorak@redhat.com> - 13.0.1-1
- Update to 13.0.1

* Tue Jun  5 2012 Jan Horak <jhorak@redhat.com> - 13.0-1
- Update to 13.0

* Mon May 7 2012 Martin Stransky <stransky@redhat.com> - 12.0.1-2
- Fixed #717245 - adhere Static Library Packaging Guidelines

* Mon Apr 30 2012 Jan Horak <jhorak@redhat.com> - 12.0.1-1
- Update to 12.0.1

* Tue Apr 24 2012 Jan Horak <jhorak@redhat.com> - 12.0-1
- Update to 12.0

* Mon Apr 16 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 11.0.1-2
- Add upstream patch to fix FTBFS on ARM

* Thu Mar 29 2012 Jan Horak <jhorak@redhat.com> - 11.0.1-1
- Update to 11.0.1

* Thu Mar 22 2012 Jan Horak <jhorak@redhat.com> - 11.0-6
- Added translations to thunderbird.desktop file

* Fri Mar 16 2012 Martin Stransky <stransky@redhat.com> - 11.0-5
- gcc 4.7 build fixes

* Wed Mar 14 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 11.0-4
- Add ARM configuration options

* Wed Mar 14 2012 Martin Stransky <stransky@redhat.com> - 11.0-3
- Build with system libvpx

* Tue Mar 13 2012 Martin Stransky <stransky@redhat.com> - 11.0-1
- Update to 11.0

* Thu Feb 23 2012 Jan Horak <jhorak@redhat.com> - 10.0.1-3
- Added fix for proxy settings mozbz#682832

* Thu Feb 16 2012 Martin Stransky <stransky@redhat.com> - 10.0.1-2
- Added fix for mozbz#727401

* Thu Feb  9 2012 Jan Horak <jhorak@redhat.com> - 10.0.1-1
- Update to 10.0.1

* Mon Feb 6 2012 Martin Stransky <stransky@redhat.com> - 10.0-2
- gcc 4.7 build fixes

* Tue Jan 31 2012 Jan Horak <jhorak@redhat.com> - 10.0-1
- Update to 10.0

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jan 05 2012 Dan Horák <dan[at]danny.cz> - 9.0-6
- disable jemalloc on s390(x) (taken from xulrunner)

* Wed Jan 04 2012 Dan Horák <dan[at]danny.cz> - 9.0-5
- fix build on secondary arches (cherry-picked from 13afcd4c097c)

* Thu Dec 22 2011 Jan Horak <jhorak@redhat.com> - 9.0-4
- Update to 9.0

* Fri Dec 9 2011 Martin Stransky <stransky@redhat.com> - 8.0-4
- enabled gio support (#760644)

* Tue Nov 29 2011 Jan Horak <jhorak@redhat.com> - 8.0-3
- Fixed s390x issues

* Thu Nov 10 2011 Jan Horak <jhorak@redhat.com> - 8.0-2
- Enable Mozilla's crash reporter again for all archs
- Temporary workaround for langpacks
- Disabled addon check UI (#753551)

* Tue Nov  8 2011 Jan Horak <jhorak@redhat.com> - 8.0-1
- Update to 8.0

* Tue Oct 18 2011 Martin Stransky <stransky@redhat.com> - 7.0.1-3
- Added NM patches (mozbz#627672, mozbz#639959)

* Wed Oct 12 2011 Dan Horák <dan[at]danny.cz> - 7.0.1-2
- fix build on secondary arches (copied from xulrunner)

* Fri Sep 30 2011 Jan Horak <jhorak@redhat.com> - 7.0.1-1
- Update to 7.0.1

* Tue Sep 27 2011 Jan Horak <jhorak@redhat.com> - 7.0-1
- Update to 7.0

* Tue Sep  6 2011 Jan Horak <jhorak@redhat.com> - 6.0.2-1
- Update to 6.0.2

* Wed Aug 31 2011 Jan Horak <jhorak@redhat.com> - 6.0-3
- Distrust a specific Certificate Authority

* Wed Aug 31 2011 Dan Horák <dan[at]danny.cz> - 6.0-2
- add secondary-ipc patch from xulrunner

* Tue Aug 16 2011 Jan Horak <jhorak@redhat.com> - 6.0-1
- Update to 6.0

* Tue Aug 16 2011 Remi Collet <remi@fedoraproject.org> 5.0-4
- Don't unzip the langpacks

* Mon Aug 15 2011 Jan Horak <jhorak@redhat.com> - 5.0-3
- Rebuild due to rhbz#728707

* Wed Jul 20 2011 Dan Horák <dan[at]danny.cz> - 5.0-2
- add xulrunner patches for secondary arches

* Tue Jun 28 2011 Jan Horak <jhorak@redhat.com> - 5.0-1
- Update to 5.0

* Tue Jun 21 2011 Jan Horak <jhorak@redhat.com> - 3.1.11-1
- Update to 3.1.11

* Wed May 25 2011 Caolán McNamara <caolanm@redhat.com> - 3.1.10-2
- rebuild for new hunspell

* Thu Apr 28 2011 Jan Horak <jhorak@redhat.com> - 3.1.10-1
- Update to 3.1.10

* Thu Apr 21 2011 Christopher Aillon <caillon@redhat.com> - 3.1.9-7
- Make gvfs-open launch a compose window (salimma)
- Spec file cleanups (salimma, caillon)
- Split out mozilla crashreporter symbols to its own debuginfo package (caillon)

* Sat Apr  2 2011 Christopher Aillon <caillon@redhat.com> - 3.1.9-6
- Drop gio support: the code hooks don't exist yet for TB 3.1.x

* Fri Apr  1 2011 Orion Poplawski <orion@cora.nwra.com> - 3.1.9-5
- Enable startup notification

* Sun Mar 20 2011 Dan Horák <dan[at]danny.cz> - 3.1.9-4
- updated the s390 build patch

* Fri Mar 18 2011 Jan Horak <jhorak@redhat.com> - 3.1.9-3
- Removed gnome-vfs2, libgnomeui and libgnome from build requires

* Wed Mar  9 2011 Jan Horak <jhorak@redhat.com> - 3.1.9-2
- Disabled gnomevfs, enabled gio

* Mon Mar  7 2011 Jan Horak <jhorak@redhat.com> - 3.1.9-1
- Update to 3.1.9

* Tue Mar  1 2011 Jan Horak <jhorak@redhat.com> - 3.1.8-3
- Update to 3.1.8

* Wed Feb  9 2011 Christopher Aillon <caillon@redhat.com> - 3.1.7-6
- Drop the -lightning subpackage, it needs to be in its own SRPM

* Mon Feb  7 2011 Christopher Aillon <caillon@redhat.com> - 3.1.7-5
- Bring back the default mailer check but fix up the directory

* Wed Dec 15 2010 Jan Horak <jhorak@redhat.com> - 3.1.7-4
- Mozilla crash reporter enabled

* Thu Dec  9 2010 Jan Horak <jhorak@redhat.com> - 3.1.7-2
- Fixed useragent

* Thu Dec  9 2010 Jan Horak <jhorak@redhat.com> - 3.1.7-1
- Update to 3.1.7

* Sat Nov 27 2010 Remi Collet <fedora@famillecollet.com> - 3.1.6-8
- fix cairo + nspr required version
- lightning: fix thunderbird version required
- lightning: fix release (b3pre)
- lightning: clean install

* Mon Nov 22 2010 Jan Horak <jhorak@redhat.com> - 3.1.6-7
- Added x-scheme-handler/mailto to thunderbird.desktop file

* Mon Nov  8 2010 Jan Horak <jhorak@redhat.com> - 3.1.6-4
- Added libnotify patch
- Removed dependency on static libraries

* Fri Oct 29 2010 Jan Horak <jhorak@redhat.com> - 3.1.6-2
- Move thunderbird-lightning extension from Sunbird package to Thunderbird

* Wed Oct 27 2010 Jan Horak <jhorak@redhat.com> - 3.1.6-1
- Update to 3.1.6

* Tue Oct 19 2010 Jan Horak <jhorak@redhat.com> - 3.1.5-1
- Update to 3.1.5

* Thu Sep 16 2010 Dan Horák <dan[at]danny.cz> - 3.1.3-2
- fix build on s390

* Tue Sep  7 2010 Jan Horak <jhorak@redhat.com> - 3.1.3-1
- Update to 3.1.3

* Fri Aug  6 2010 Jan Horak <jhorak@redhat.com> - 3.1.2-1
- Update to 3.1.2
- Disable updater

* Tue Jul 20 2010 Jan Horak <jhorak@redhat.com> - 3.1.1-1
- Update to 3.1.1

* Thu Jun 24 2010 Jan Horak <jhorak@redhat.com> - 3.1-1
- Thunderbird 3.1

* Fri Jun 11 2010 Jan Horak <jhorak@redhat.com> - 3.1-0.3.rc2
- TryExec added to desktop file

* Wed Jun  9 2010 Christopher Aillon <caillon@redhat.com> 3.1-0.2.rc2
- Thunderbird 3.1 RC2

* Tue May 25 2010 Christopher Aillon <caillon@redhat.com> 3.1-0.1.rc1
- Thunderbird 3.1 RC1

* Fri Apr 30 2010 Jan Horak <jhorak@redhat.com> - 3.0.4-3
- Fix for mozbz#550455

* Tue Apr 13 2010 Martin Stransky <stransky@redhat.com> - 3.0.4-2
- Fixed langpacks (#580444)

* Tue Mar 30 2010 Jan Horak <jhorak@redhat.com> - 3.0.4-1
- Update to 3.0.4

* Sat Mar 06 2010 Kalev Lember <kalev@smartlink.ee> - 3.0.3-2
- Own extension directories (#532132)

* Mon Mar  1 2010 Jan Horak <jhorak@redhat.com> - 3.0.3-1
- Update to 3.0.3

* Thu Feb 25 2010 Jan Horak <jhorak@redhat.com> - 3.0.2-1
- Update to 3.0.2

* Wed Jan 20 2010 Martin Stransky <stransky@redhat.com> - 3.0.1-1
- Update to 3.0.1

* Mon Jan 18 2010 Martin Stransky <stransky@redhat.com> - 3.0-5
- Added fix for #480603 - thunderbird takes 
  unacceptably long time to start

* Wed Dec  9 2009 Jan Horak <jhorak@redhat.com> - 3.0-4
- Update to 3.0

* Thu Dec  3 2009 Jan Horak <jhorak@redhat.com> - 3.0-3.13.rc2
- Update to RC2

* Wed Nov 25 2009 Jan Horak <jhorak@redhat.com> - 3.0-3.12.rc1
- Sync with Mozilla latest RC1 build

* Thu Nov 19 2009 Jan Horak <jhorak@redhat.com> - 3.0-3.11.rc1
- Update to RC1

* Thu Sep 17 2009 Christopher Aillon <caillon@redhat.com> - 3.0-3.9.b4
- Update to 3.0 b4

* Thu Aug  6 2009 Martin Stransky <stransky@redhat.com> - 3.0-3.8.beta3
- Added fix for #437596
- Removed unused patches

* Thu Aug  6 2009 Jan Horak <jhorak@redhat.com> - 3.0-3.7.beta3
- Removed unused build requirements

* Mon Aug  3 2009 Jan Horak <jhorak@redhat.com> - 3.0-3.6.beta3
- Build with system hunspell

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-3.5.b3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 24 2009 Jan Horak <jhorak@redhat.com> - 3.0-2.5.beta3
- Use system hunspell

* Tue Jul 21 2009 Jan Horak <jhorak@redhat.com> - 3.0-2.4.beta3
- Update to 3.0 beta3

* Mon Mar 30 2009 Jan Horak <jhorak@redhat.com> - 3.0-2.2.beta2
- Fixed open-browser.sh to use xdg-open instead of gnome-open

* Mon Mar 23 2009 Christopher Aillon <caillon@redhat.com> - 3.0-2.1.beta2
- Disable the default app nag dialog

* Tue Mar 17 2009 Jan Horak <jhorak@redhat.com> - 3.0-2.beta2
- Fixed clicked link does not open in browser (#489120)
- Fixed missing help in thunderbird (#488885)

* Mon Mar  2 2009 Jan Horak <jhorak@redhat.com> - 3.0-1.beta2
- Update to 3.0 beta2
- Added Patch2 to build correctly when building with --enable-shared option 

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan 07 2009 Christopher Aillon <caillon@redhat.com> - 2.0.0.18-2
- Disable the crash dialog

* Wed Nov 19 2008 Christopher Aillon <caillon@redhat.com> 2.0.0.18-1
- Update to 2.0.0.18

* Thu Oct  9 2008 Christopher Aillon <caillon@redhat.com> 2.0.0.17-1
- Update to 2.0.0.17

* Wed Jul 23 2008 Christopher Aillon <caillon@redhat.com> 2.0.0.16-1
- Update to 2.0.0.16

* Thu May  1 2008 Christopher Aillon <caillon@redhat.com> 2.0.0.14-1
- Update to 2.0.0.14
- Use the system dictionaries

* Fri Apr 18 2008 Christopher Aillon <caillon@redhat.com> 2.0.0.12-6
- Icon belongs in _datadir/pixmaps

* Fri Apr 18 2008 Christopher Aillon <caillon@redhat.com> 2.0.0.12-5
- rebuilt

* Mon Apr  7 2008 Christopher Aillon <caillon@redhat.com> 2.0.0.12-4
- Add %%lang attributes to langpacks

* Sat Mar 15 2008 Christopher Aillon <caillon@redhat.com> 2.0.0.12-3
- Avoid conflict between gecko debuginfos

* Mon Mar 03 2008 Martin Stransky <stransky@redhat.com> 2.0.0.12-2
- Updated starting script (#426331)

* Tue Feb 26 2008 Christopher Aillon <caillon@redhat.com> 2.0.0.12-1
- Update to 2.0.0.12
- Fix up icon location and some scriptlets

* Sun Dec  9 2007 Christopher Aillon <caillon@redhat.com> 2.0.0.9-2
- Fix some rpmlint warnings
- Drop some old patches and obsoletes

* Thu Nov 15 2007 Christopher Aillon <caillon@redhat.com> 2.0.0.9-1
- Update to 2.0.0.9

* Wed Sep 26 2007 Martin Stransky <stransky@redhat.com> 2.0.0.6-6
- Fixed #242657 - firefox -g doesn't work

* Tue Sep 25 2007 Christopher Aillon <caillon@redhat.com> 2.0.0.6-5
- Removed hardcoded MAX_PATH, PATH_MAX and MAXPATHLEN macros

* Tue Sep 11 2007 Christopher Aillon <caillon@redhat.com> 2.0.0.6-4
- Fix crashes when using GTK+ themes containing a gtkrc which specify 
  GtkOptionMenu::indicator_size and GtkOptionMenu::indicator_spacing

* Mon Sep 10 2007 Martin Stransky <stransky@redhat.com> 2.0.0.6-3
- added fix for #246248 - firefox crashes when searching for word "do"

* Mon Aug 13 2007 Christopher Aillon <caillon@redhat.com> 2.0.0.6-2
- Update the license tag

* Wed Aug  8 2007 Christopher Aillon <caillon@redhat.com> 2.0.0.6-1
- Update to 2.0.0.6
- Own the application directory (#244901)

* Tue Jul 31 2007 Martin Stransky <stransky@redhat.com> 2.0.0.0-3
- added pango ligature fix

* Thu Apr 19 2007 Christopher Aillon <caillon@redhat.com> 2.0.0.0-1
- Update to 2.0.0.0 Final

* Fri Apr 13 2007 Christopher Aillon <caillon@redhat.com> 2.0.0.0-0.5.rc1
- Fix the desktop file
- Clean up the files list
- Remove the default client stuff from the pref window

* Thu Apr 12 2007 Christopher Aillon <caillon@redhat.com> 2.0.0.0-0.4.rc1
- Rebuild into Fedora

* Wed Apr 11 2007 Christopher Aillon <caillon@redhat.com> 2.0.0.0-0.3.rc1
- Update langpacks

* Thu Apr  5 2007 Christopher Aillon <caillon@redhat.com> 2.0.0.0-0.2.rc1
- Build option tweaks
- Bring the install section to parity with Firefox's

* Thu Apr  5 2007 Christopher Aillon <caillon@redhat.com> 2.0.0.0-0.1.rc1
- Update to 2.0.0.0 RC1

* Sun Mar 25 2007 Christopher Aillon <caillon@redhat.com> 1.5.0.11-1
- Update to 1.5.0.11

* Fri Mar 2 2007 Martin Stransky <stransky@redhat.com> 1.5.0.10-1
- Update to 1.5.0.10

* Mon Feb 12 2007 Martin Stransky <stransky@redhat.com> 1.5.0.9-8
- added fix for #227406: garbage characters on some websites
  (when pango is disabled)
  
* Tue Jan 30 2007 Christopher Aillon <caillon@redhat.com> 1.5.0.9-7
- Updated cursor position patch from tagoh to fix issue with "jumping"
  cursor when in a textfield with tabs.

* Tue Jan 30 2007 Christopher Aillon <caillon@redhat.com> 1.5.0.9-6
- Fix the DND implementation to not grab, so it works with new GTK+.

* Thu Dec 21 2006 Behdad Esfahbod <besfahbo@redhat.com> 1.5.0.9-5
- Added firefox-1.5-pango-underline.patch

* Wed Dec 20 2006 Behdad Esfahbod <besfahbo@redhat.com> 1.5.0.9-4
- Added firefox-1.5-pango-justified-range.patch

* Tue Dec 19 2006 Behdad Esfahbod <besfahbo@redhat.com> 1.5.0.9-3
- Added firefox-1.5-pango-cursor-position-more.patch

* Tue Dec 19 2006 Matthias Clasen <mclasen@redhat.com> 1.5.0.9-2
- Add a Requires: launchmail  (#219884)

* Tue Dec 19 2006 Christopher Aillon <caillon@redhat.com> 1.5.0.9-1
- Update to 1.5.0.9
- Take firefox's pango fixes
- Don't offer to import...nothing.

* Tue Nov  7 2006 Christopher Aillon <caillon@redhat.com> 1.5.0.8-1
- Update to 1.5.0.8
- Allow choosing of download directory
- Take the user to the correct directory from the Download Manager.
- Patch to add support for printing via pango from Behdad.

* Sun Oct  8 2006 Christopher Aillon <caillon@redhat.com> - 1.5.0.7-4
- Default to use of system colors

* Wed Oct  4 2006 Christopher Aillon <caillon@redhat.com> - 1.5.0.7-3
- Bring the invisible character to parity with GTK+

* Wed Sep 27 2006 Christopher Aillon <caillon@redhat.com> - 1.5.0.7-2
- Fix crash when changing gtk key theme
- Prevent UI freezes while changing GNOME theme
- Remove verbiage about pango; no longer required by upstream.

* Wed Sep 13 2006 Christopher Aillon <caillon@redhat.com> - 1.5.0.7-1
- Update to 1.5.0.7

* Thu Sep  7 2006 Christopher Aillon <caillon@redhat.com> - 1.5.0.5-8
- Shuffle order of the install phase around

* Thu Sep  7 2006 Christopher Aillon <caillon@redhat.com> - 1.5.0.5-7
- Let there be art for Alt+Tab again
- s/tbdir/mozappdir/g

* Wed Sep  6 2006 Christopher Aillon <caillon@redhat.com> - 1.5.0.5-6
- Fix for cursor position in editor widgets by tagoh and behdad (#198759)

* Tue Sep  5 2006 Christopher Aillon <caillon@redhat.com> - 1.5.0.5-5
- Update nopangoxft.patch
- Fix rendering of MathML thanks to Behdad Esfahbod.
- Update start page text to reflect the MathML fixes.
- Enable pango by default on all locales
- Build using -rpath
- Re-enable GCC visibility

* Thu Aug  3 2006 Kai Engert <kengert@redhat.com> - 1.5.0.5-4
- Fix a build failure in mailnews mime code.

* Tue Aug  1 2006 Matthias Clasen <mclasen@redhat.com> - 1.5.0.5-3
- Rebuild

* Thu Jul 27 2006 Christopher Aillon <caillon@redhat.com> - 1.5.0.5-2
- Update to 1.5.0.5

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.5.0.4-2.1
- rebuild

* Mon Jun 12 2006 Kai Engert <kengert@redhat.com> - 1.5.0.4-2
- Update to 1.5.0.4
- Fix desktop-file-utils requires

* Wed Apr 19 2006 Christopher Aillon <caillon@redhat.com> - 1.5.0.2-2
- Update to 1.5.0.2

* Thu Mar 16 2006 Christopher Aillon <caillon@redhat.com> - 1.5-7
- Bring the other arches back

* Mon Mar 13 2006 Christopher Aillon <caillon@redhat.com> - 1.5.6
- Temporarily disable other arches that we don't ship FC5 with, for time

* Mon Mar 13 2006 Christopher Aillon <caillon@redhat.com> - 1.5-5
- Add a notice to the mail start page denoting this is a pango enabled build.

* Fri Feb 10 2006 Christopher Aillon <caillon@redhat.com> - 1.5-3
- Add dumpstack.patch
- Improve the langpack install stuff

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.5-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Jan 27 2006 Christopher Aillon <caillon@redhat.com> - 1.5-2
- Add some langpacks back in
- Stop providing MozillaThunderbird

* Thu Jan 12 2006 Christopher Aillon <caillon@redhat.com> - 1.5-1
- Official 1.5 release is out

* Wed Jan 11 2006 Christopher Aillon <caillon@redhat.com> - 1.5-0.5.6.rc1
- Fix crash when deleting highlighted text while composing mail within
  plaintext editor with spellcheck enabled.

* Tue Jan  3 2006 Christopher Aillon <caillon@redhat.com> - 1.5-0.5.5.rc1
- Looks like we can build on ppc64 again.

* Fri Dec 16 2005 Christopher Aillon <caillon@redhat.com> - 1.5-0.5.4.rc1
- Rebuild

* Fri Dec 16 2005 Christopher Aillon <caillon@redhat.com> - 1.5-0.5.3.rc1
- Once again, disable ppc64 because of a new issue.
  See https://bugzilla.redhat.com/bugzilla/show_bug.cgi?id=175944

- Use the system NSS libraries
- Build on ppc64

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Nov 28 2005 Christopher Aillon <caillon@redhat.com> - 1.5-0.5.1.rc1
- Fix issue with popup dialogs and other actions causing lockups

* Sat Nov  5 2005 Christopher Aillon <caillon@redhat.com> 1.5-0.5.0.rc1
- Update to 1.5 rc1

* Sat Oct  8 2005 Christopher Aillon <caillon@redhat.com> 1.5-0.5.0.beta2
- Update to 1.5 beta2

* Wed Sep 28 2005 Christopher Aillon <caillon@redhat.com> 1.5-0.5.0.beta1
- Update to 1.5 beta1
- Bring the install phase of the spec file up to speed

* Sun Aug 14 2005 Christopher Aillon <caillon@redhat.com> 1.0.6-4
- Rebuild

* Sat Aug  6 2005 Christopher Aillon <caillon@redhat.com> 1.0.6-3
- Add patch to make file chooser dialog modal

* Fri Jul 22 2005 Christopher Aillon <caillon@redhat.com> 1.0.6-2
- Update to 1.0.6

* Mon Jul 18 2005 Christopher Aillon <caillon@redhat.com> 1.0.6-0.1.fc5
- 1.0.6 Release Candidate

* Fri Jul 15 2005 Christopher Aillon <caillon@redhat.com> 1.0.2-8
- Use system NSPR
- Fix crash on 64bit platforms (#160330)

* Thu Jun 23 2005 Kristian Høgsberg <krh@redhat.com>  1.0.2-7
- Add firefox-1.0-pango-cairo.patch to get rid of the last few Xft
  references, fixing the "no fonts" problem.

* Fri May 13 2005 Christopher Aillon <caillon@redhat.com> 1.0.2-6
- Change the Exec line in the desktop file to `thunderbird`

* Fri May 13 2005 Christopher Aillon <caillon@redhat.com> 1.0.2-5
- Update pango patche, MOZ_DISABLE_PANGO now works as advertised.

* Mon May  9 2005 Christopher Aillon <caillon@redhat.com> 1.0.2-4
- Add temporary workaround to not create files in the user's $HOME (#149664)

* Wed May  4 2005 Christopher Aillon <caillon@redhat.com> 1.0.2-3
- Don't have downloads "disappear" when downloading to desktop (#139015)
- Fix for some more cursor issues in textareas (149991, 150002, 152089)
- Add upstream patch to fix bidi justification of pango
- Add patch to fix launching of helper applications
- Add patch to properly link against libgfxshared_s.a
- Fix multilib conflicts

* Wed Apr 27 2005 Warren Togami <wtogami@redhat.com>
- correct confusing PANGO vars in startup script

* Wed Mar 23 2005 Christopher Aillon <caillon@redhat.com> 1.0.2-1
- Thunderbird 1.0.2

* Tue Mar  8 2005 Christopher Aillon <caillon@redhat.com> 1.0-5
- Add patch to compile against new fortified glibc macros

* Sat Mar  5 2005 Christopher Aillon <caillon@redhat.com> 1.0-4
- Rebuild against GCC 4.0
- Add execshield patches
- Minor specfile cleanup

* Mon Dec 20 2004 Christopher Aillon <caillon@redhat.com> 1.0-3
- Rebuild

* Thu Dec 16 2004 Christopher Aillon <caillon@redhat.com> 1.0-2
- Add RPM version to useragent

* Thu Dec 16 2004 Christopher Blizzard <blizzard@redhat.com>
- Port over pango patches from firefox

* Wed Dec  8 2004 Christopher Aillon <caillon@redhat.com> 1.0-1
- Thunderbird 1.0

* Mon Dec  6 2004 Christopher Aillon <caillon@redhat.com> 1.0-0.rc1.1
- Fix advanced prefs

* Fri Dec  3 2004 Christopher Aillon <caillon@redhat.com>
- Make this run on s390(x) now for real

* Wed Dec  1 2004 Christopher Aillon <caillon@redhat.com> 1.0-0.rc1.0
- Update to 1.0 rc1

* Fri Nov 19 2004 Christopher Aillon <caillon@redhat.com>
- Add patches to build and run on s390(x)

* Thu Nov 11 2004 Christopher Aillon <caillon@redhat.com> 0.9.0-2
- Rebuild to fix file chooser

* Fri Nov  5 2004 Christopher Aillon <caillon@redhat.com> 0.9.0-1
- Update to 0.9

* Fri Oct 22 2004 Christopher Aillon <caillon@redhat.com> 0.8.0-10
- Prevent inlining of stack direction detection (#135255)

* Tue Oct 19 2004 Christopher Aillon <caillon@redhat.com> 0.8.0-9
- More file chooser fixes (same as in firefox)
- Fix for upstream 28327.

* Mon Oct 18 2004 Christopher Blizzard <blizzard@redhat.com> 0.8.0-8
- Update the pango patch

* Mon Oct 18 2004 Christopher Blizzard <blizzard@redhat.com> 0.8.0-8
- Pull over patches from firefox build:
  - disable default application dialog
  - don't include software update since it doesn't work
  - make external app support work

* Thu Oct 14 2004 Christopher Blizzard <blizzard@redhat.com> 0.8.0-7
- Use pango for rendering

* Tue Oct 12 2004 Christopher Aillon <caillon@redhat.com> 0.8.0-6
- Fix for 64 bit crash at startup (b.m.o #256603)

* Sat Oct  9 2004 Christopher Aillon <caillon@redhat.com> 0.8.0-5
- Add patches to fix xremote (#135036)

* Fri Oct  8 2004 Christopher Aillon <caillon@redhat.com> 0.8.0-4
- Add patch to fix button focus issues (#133507)
- Add patch for fix IMAP race issues (bmo #246439)

* Fri Oct  1 2004 Bill Nottingham <notting@redhat.com> 0.8.0-3
- filter out library Provides: and internal Requires:

* Tue Sep 28 2004 Christopher Aillon <caillon@redhat.com> 0.8.0-2
- Backport the GTK+ File Chooser.
- Add fix for JS math on x86_64 systems
- Add pkgconfig patch

* Thu Sep 16 2004 Christopher Aillon <caillon@redhat.com> 0.8.0-1
- Update to 0.8.0
- Remove enigmail
- Update BuildRequires
- Remove gcc34 and extension manager patches -- they are upstreamed.
- Fix for gnome-vfs2 error at component registration

* Fri Sep 03 2004 Christopher Aillon <caillon@redhat.com> 0.7.3-5
- Build with --disable-xprint

* Wed Sep 01 2004 David Hill <djh[at]ii.net> 0.7.3-4
- remove all Xvfb-related hacks

* Wed Sep 01 2004 Warren Togami <wtogami@redhat.com> 
- actually apply psfonts
- add mozilla gnome-uriloader patch to prevent build failure

* Tue Aug 31 2004 Warren Togami <wtogami@redhat.com> 0.7.3-3
- rawhide import
- apply NetBSD's freetype 2.1.8 patch
- apply psfonts patch
- remove BR on /usr/bin/ex, breaks beehive

* Tue Aug 31 2004 David Hill <djh[at]ii.net> 0.7.3-0.fdr.2
- oops, fix %%install

* Thu Aug 26 2004 David Hill <djh[at]ii.net> 0.7.3-0.fdr.1
- update to Thunderbird 0.7.3 and Enigmail 0.85.0
- remove XUL.mfasl on startup, add Debian enigmail patches
- add Xvfb hack for -install-global-extension

* Wed Jul 14 2004 David Hill <djh[at]ii.net> 0.7.2-0.fdr.0
- update to 0.7.2, just because it's there
- update gcc-3.4 patch (Kaj Niemi)
- add EM registration patch and remove instdir hack

* Sun Jul 04 2004 David Hill <djh[at]ii.net> 0.7.1-0.fdr.1
- re-add Enigmime 1.0.7, omit Enigmail until the Mozilla EM problems are fixed

* Wed Jun 30 2004 David Hill <djh[at]ii.net> 0.7.1-0.fdr.0
- update to 0.7.1
- remove Enigmail

* Mon Jun 28 2004 David Hill <djh[at]ii.net> 0.7-0.fdr.1
- re-enable Enigmail 0.84.1
- add gcc-3.4 patch (Kaj Niemi)
- use official branding (with permission)

* Fri Jun 18 2004 David Hill <djh[at]ii.net> 0.7-0.fdr.0
- update to 0.7
- temporarily disable Enigmail 0.84.1, make ftp links work (#1634)
- specify libdir, change BR for apt (V. Skyttä, #1617)

* Tue May 18 2004 Warren Togami <wtogami@redhat.com> 0.6-0.fdr.5
- temporary workaround for enigmail skin "modern" bug

* Mon May 10 2004 David Hill <djh[at]ii.net> 0.6-0.fdr.4
- update to Enigmail 0.84.0 
- update launch script

* Mon May 10 2004 David Hill <djh[at]ii.net> 0.6-0.fdr.3
- installation directory now versioned
- allow root to run the program (for installing extensions)
- remove unnecessary %%pre and %%post
- remove separators, update mozconfig and launch script (M. Schwendt, #1460)

* Wed May 05 2004 David Hill <djh[at]ii.net> 0.6-0.fdr.2
- include Enigmail, re-add release notes
- delete %%{_libdir}/thunderbird in %%pre

* Mon May 03 2004 David Hill <djh[at]ii.net> 0.6-0.fdr.1
- update to Thunderbird 0.6

* Fri Apr 30 2004 David Hill <djh[at]ii.net> 0.6-0.fdr.0.rc1
- update to Thunderbird 0.6 RC1
- add new icon, remove release notes

* Thu Apr 15 2004 David Hill <djh[at]ii.net> 0.6-0.fdr.0.20040415
- update to latest CVS, update mozconfig and %%build accordingly
- update to Enigmail 0.83.6
- remove x-remote and x86_64 patches
- build with -Os

* Thu Apr 15 2004 David Hill <djh[at]ii.net> 0.5-0.fdr.12
- update x-remote patch
- more startup script fixes

* Tue Apr 06 2004 David Hill <djh[at]ii.net> 0:0.5-0.fdr.11
- startup script fixes, and a minor cleanup

* Sun Apr 04 2004 Warren Togami <wtogami@redhat.com> 0:0.5-0.fdr.10
- Minor cleanups

* Sun Apr 04 2004 David Hill <djh[at]ii.net> 0:0.5-0.fdr.8
- minor improvements to open-browser.sh and startup script
- update to latest version of Blizzard's x-remote patch

* Thu Mar 25 2004 David Hill <djh[at]ii.net> 0:0.5-0.fdr.7
- update open-browser.sh, startup script, and BuildRequires

* Sun Mar 14 2004 David Hill <djh[at]ii.net> 0:0.5-0.fdr.6
- update open-browser script, modify BuildRequires (Warren)
- add Blizzard's x-remote patch
- initial attempt at x-remote-enabled startup script

* Sun Mar 07 2004 David Hill <djh[at]ii.net> 0:0.5-0.fdr.5
- refuse to run with excessive privileges

* Fri Feb 27 2004 David Hill <djh[at]ii.net> 0:0.5-0.fdr.4
- add Mozilla x86_64 patch (Oliver Sontag)
- Enigmail source filenames now include the version
- modify BuildRoot

* Thu Feb 26 2004 David Hill <djh[at]ii.net> 0:0.5-0.fdr.3
- use the updated official tarball

* Wed Feb 18 2004 David Hill <djh[at]ii.net> 0:0.5-0.fdr.2
- fix %%prep script

* Mon Feb 16 2004 David Hill <djh[at]ii.net> 0:0.5-0.fdr.1
- update Enigmail to 0.83.3
- use official source tarball (after removing the CRLFs)
- package renamed to thunderbird

* Mon Feb 09 2004 David Hill <djh[at]ii.net> 0:0.5-0.fdr.0
- update to 0.5
- check for lockfile before launching

* Fri Feb 06 2004 David Hill <djh[at]ii.net>
- update to latest cvs
- update to Enigmail 0.83.2

* Thu Jan 29 2004 David Hill <djh[at]ii.net> 0:0.4-0.fdr.5
- update to Enigmail 0.83.1
- removed Mozilla/Firebird script patching

* Sat Jan 03 2004 David Hill <djh[at]ii.net> 0:0.4-0.fdr.4
- add startup notification to .desktop file

* Thu Dec 25 2003 Warren Togami <warren@togami.com> 0:0.4-0.fdr.3
- open-browser.sh release 3
- patch broken /usr/bin/mozilla script during install
- dir ownership
- XXX: Source fails build on x86_64... fix later

* Tue Dec 23 2003 David Hill <djh[at]ii.net> 0:0.4-0.fdr.2
- update to Enigmail 0.82.5
- add Warren's open-browser.sh (#1113)

* Tue Dec 09 2003 David Hill <djh[at]ii.net> 0:0.4-0.fdr.1
- use Thunderbird's mozilla-xremote-client to launch browser

* Sun Dec 07 2003 David Hill <djh[at]ii.net> 0:0.4-0.fdr.0
- update to 0.4
- make hyperlinks work (with recent versions of Firebird/Mozilla)

* Thu Dec 04 2003 David Hill <djh[at]ii.net>
- update to 0.4rc2

* Wed Dec 03 2003 David Hill <djh[at]ii.net>
- update to 0.4rc1 and Enigmail 0.82.4

* Thu Nov 27 2003 David Hill <djh[at]ii.net>
- update to latest CVS and Enigmail 0.82.3

* Sun Nov 16 2003 David Hill <djh[at]ii.net>
- update to latest CVS (0.4a)
- update Enigmail to 0.82.2
- alter mozconfig for new build requirements
- add missing BuildReq (#987)

* Thu Oct 16 2003 David Hill <djh[at]ii.net> 0:0.3-0.fdr.0
- update to 0.3

* Sun Oct 12 2003 David Hill <djh[at]ii.net> 0:0.3rc3-0.fdr.0
- update to 0.3rc3
- update Enigmail to 0.81.7

* Thu Oct 02 2003 David Hill <djh[at]ii.net> 0:0.3rc2-0.fdr.0
- update to 0.3rc2

* Wed Sep 17 2003 David Hill <djh[at]ii.net> 0:0.2-0.fdr.2
- simplify startup script

* Wed Sep 10 2003 David Hill <djh[at]ii.net> 0:0.2-0.fdr.1
- add GPG support (Enigmail 0.81.6)
- specfile fixes (#679)

* Thu Sep 04 2003 David Hill <djh[at]ii.net> 0:0.2-0.fdr.0
- update to 0.2

* Mon Sep 01 2003 David Hill <djh[at]ii.net>
- initial RPM
  (based on the fedora MozillaFirebird-0.6.1 specfile)

