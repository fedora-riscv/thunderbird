# Option: Freetype Patch (FC3+)
%define freetype_fc3 1

%define desktop_file_utils_version 0.3

ExclusiveArch: i386 x86_64 ia64 ppc

Summary:	Mozilla Thunderbird mail/newsgroup client
Name:		thunderbird
Version:	0.8.0
Release:	7
Epoch:		0
URL:		http://www.mozilla.org/projects/thunderbird/
License:	MPL
Group:		Applications/Internet
Source0:	http://ftp.mozilla.org/pub/mozilla.org/thunderbird/releases/0.8/thunderbird-source-0.8.tar.bz2
Source1:	thunderbird.desktop
# This icon is used with the permission of mozilla.org.
Source2:	thunderbird-icon.png
Source3:	thunderbird.sh.in
Source4:	thunderbird-mozconfig
Source5:	release-notes.html
Source6:	thunderbird-open-browser.sh
Source7:	thunderbird-prefs
Source100:	find-external-requires
Patch1:		thunderbird-0.7.3-em-register.patch
Patch2:		thunderbird-0.7.3-em-fileuri.patch
Patch3:		thunderbird-0.7.3-enigmail-debian.patch
Patch4:         thunderbird-0.7.3-freetype-compile.patch
Patch5:         thunderbird-0.7.3-psfonts.patch
Patch6:         thunderbird-0.7.3-gnome-uriloader.patch


# Backported patches, intended for upstream
Patch90:        thunderbird-0.8.0-gtk-file-chooser-trunk.patch
Patch91:        thunderbird-0.8.0-gtk-file-chooser-updates.patch

# Already upstreamed
Patch100:       thunderbird-0.8.0-js-64bit-math.patch
Patch101:       thunderbird-0.8.0-pkgconfig.patch
Patch102:       thunderbird-0.8.0-button-focus.patch
Patch103:       thunderbird-0.8.0-imap-race.patch
Patch104:       thunderbird-0.8.0-xremote-program-name.patch
Patch105:       thunderbird-0.8.0-xremote-crash.patch
Patch106:       thunderbird-0.8.0-access-64bit-crash.patch
Patch107:       mozilla-1.7.3-pango-render.patch




BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	libpng-devel, libjpeg-devel, gtk2-devel
BuildRequires:	zlib-devel, gzip, zip, unzip
BuildRequires:	XFree86-devel
BuildRequires:	libIDL-devel
BuildRequires:	tcsh
BuildRequires:	freetype-devel
BuildRequires:  autoconf213
Prereq:		desktop-file-utils >= %{desktop_file_utils_version}
Obsoletes:	MozillaThunderbird
Provides:	MozillaThunderbird = %{epoch}:%{version}

%define tbdir %{_libdir}/thunderbird-%{version}

AutoProv: 0
%define _use_internal_dependency_generator 0
%define __find_requires %{SOURCE100}

%description
Mozilla Thunderbird is a standalone mail and newsgroup client.

#===============================================================================

%prep
%setup -q -n mozilla
cp -f %{SOURCE4} .mozconfig
echo "ac_add_options --libdir=%{_libdir}" >> .mozconfig
echo "ac_add_options --with-default-mozilla-five-home=%{tbdir}" >> .mozconfig
echo "mk_add_options MOZ_MAKE_FLAGS='%{?_smp_mflags}'" >> .mozconfig
cp -f %{SOURCE5} .
%if %{freetype_fc3}
%patch4 -p0 -b .freetype
%endif
%patch5 -p1 -b .psfonts
%patch6 -p1 -b .gnome-uriloader
%patch90 -p0 -b .gtk-file-chooser-trunk
%patch91 -p1 -b .gtk-file-chooser-updates
%patch100 -p0 -b .js-64bit-math
%patch101 -p0 -b .pkgconfig
%patch102 -p0 -b .button-focus
%patch103 -p0 -b .imap-race
%patch104 -p0 -b .xremote-programname
%patch105 -p0 -b .xremote-crash
%patch106 -p0 -b .access-64bit-crash
%patch107 -p1 -b .pango

#===============================================================================

%build
autoconf-2.13

export RPM_OPT_FLAGS=$(echo $RPM_OPT_FLAGS | sed 's/-O2/-Os/')
export CFLAGS="$RPM_OPT_FLAGS"
export CXXFLAGS="$CFLAGS"
export BUILD_OFFICIAL=1
export MOZILLA_OFFICIAL=1
time make -f client.mk build_all

#===============================================================================

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}{%{tbdir},%{_bindir}}

cd dist/bin
tar ch ./ | ( cd %{buildroot}%{tbdir} ; tar xf - )
cd -

# menu entry
install -p -D %{SOURCE2} %{buildroot}%{_datadir}/pixmaps/thunderbird-icon.png
desktop-file-install --vendor mozilla			\
	--dir %{buildroot}%{_datadir}/applications  	\
	--add-category X-Red-Hat			\
	--add-category Application			\
	--add-category Network				\
	%{SOURCE1}

install -m755 %{SOURCE3} %{buildroot}%{_bindir}/mozilla-thunderbird
perl -pi -e 's|TBDIR|%{tbdir}|g' %{buildroot}%{_bindir}/mozilla-thunderbird
( cd %{buildroot}%{_bindir} ; ln -s mozilla-thunderbird thunderbird )

install -m755 %{SOURCE6} %{buildroot}%{tbdir}/open-browser.sh
perl -pi -e 's|LIBDIR|%{_libdir}|g' %{buildroot}%{tbdir}/open-browser.sh

install -m644 %{SOURCE7} %{buildroot}%{tbdir}/defaults/pref/all.js
perl -pi -e 's|COMMAND|%{tbdir}/open-browser.sh|g' \
  %{buildroot}%{tbdir}/defaults/pref/all.js

cd %{buildroot}%{tbdir}
export MOZ_DISABLE_GNOME=1
./thunderbird -register

rm -rf %{buildroot}/%{tbdir}/chrome/{classic,comm,embed-sample,en-{mac,win},help,messenger}
# ...

#===============================================================================

%clean
#rm -rf %{buildroot}

#===============================================================================

%files
%defattr(-,root,root,-)
%attr(755,root,root) %{_bindir}/mozilla-thunderbird
%attr(755,root,root) %{_bindir}/thunderbird
%attr(644,root,root) %{_datadir}/applications/mozilla-thunderbird.desktop
%attr(644,root,root) %{_datadir}/pixmaps/thunderbird-icon.png
%{tbdir}
%doc release-notes.html

#===============================================================================

%changelog
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
- delete %{_libdir}/thunderbird in %%pre

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

* Sun Apr 04 2004 David Hill <djh[at]ii.net>	0:0.5-0.fdr.8
- minor improvements to open-browser.sh and startup script
- update to latest version of Blizzard's x-remote patch

* Thu Mar 25 2004 David Hill <djh[at]ii.net>	0:0.5-0.fdr.7
- update open-browser.sh, startup script, and BuildRequires

* Sun Mar 14 2004 David Hill <djh[at]ii.net>	0:0.5-0.fdr.6
- update open-browser script, modify BuildRequires (Warren)
- add Blizzard's x-remote patch
- initial attempt at x-remote-enabled startup script

* Sun Mar 07 2004 David Hill <djh[at]ii.net>	0:0.5-0.fdr.5
- refuse to run with excessive privileges

* Fri Feb 27 2004 David Hill <djh[at]ii.net>	0:0.5-0.fdr.4
- add Mozilla x86_64 patch (Oliver Sontag)
- Enigmail source filenames now include the version
- modify BuildRoot

* Thu Feb 26 2004 David Hill <djh[at]ii.net>	0:0.5-0.fdr.3
- use the updated official tarball

* Wed Feb 18 2004 David Hill <djh[at]ii.net>	0:0.5-0.fdr.2
- fix %%prep script

* Mon Feb 16 2004 David Hill <djh[at]ii.net>	0:0.5-0.fdr.1
- update Enigmail to 0.83.3
- use official source tarball (after removing the CRLFs)
- package renamed to thunderbird

* Mon Feb 09 2004 David Hill <djh[at]ii.net>	0:0.5-0.fdr.0
- update to 0.5
- check for lockfile before launching

* Fri Feb 06 2004 David Hill <djh[at]ii.net>
- update to latest cvs
- update to Enigmail 0.83.2

* Thu Jan 29 2004 David Hill <djh[at]ii.net>	0:0.4-0.fdr.5
- update to Enigmail 0.83.1
- removed Mozilla/Firebird script patching

* Sat Jan 03 2004 David Hill <djh[at]ii.net>	0:0.4-0.fdr.4
- add startup notification to .desktop file

* Thu Dec 25 2003 Warren Togami <warren@togami.com> 0:0.4-0.fdr.3
- open-browser.sh release 3
- patch broken /usr/bin/mozilla script during install
- dir ownership
- XXX: Source fails build on x86_64... fix later

* Tue Dec 23 2003 David Hill <djh[at]ii.net>	0:0.4-0.fdr.2
- update to Enigmail 0.82.5
- add Warren's open-browser.sh (#1113)

* Tue Dec 09 2003 David Hill <djh[at]ii.net>	0:0.4-0.fdr.1
- use Thunderbird's mozilla-xremote-client to launch browser

* Sun Dec 07 2003 David Hill <djh[at]ii.net>	0:0.4-0.fdr.0
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

* Thu Oct 16 2003 David Hill <djh[at]ii.net>	0:0.3-0.fdr.0
- update to 0.3

* Sun Oct 12 2003 David Hill <djh[at]ii.net>	0:0.3rc3-0.fdr.0
- update to 0.3rc3
- update Enigmail to 0.81.7

* Thu Oct 02 2003 David Hill <djh[at]ii.net>	0:0.3rc2-0.fdr.0
- update to 0.3rc2

* Wed Sep 17 2003 David Hill <djh[at]ii.net>	0:0.2-0.fdr.2
- simplify startup script

* Wed Sep 10 2003 David Hill <djh[at]ii.net>	0:0.2-0.fdr.1
- add GPG support (Enigmail 0.81.6)
- specfile fixes (#679)

* Thu Sep 04 2003 David Hill <djh[at]ii.net>	0:0.2-0.fdr.0
- update to 0.2

* Mon Sep 01 2003 David Hill <djh[at]ii.net>
- initial RPM
  (based on the fedora MozillaFirebird-0.6.1 specfile)

