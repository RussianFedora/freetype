# Disables freetype 1 and 2 bytecode interpreter.  Setting to 0 enables
# the bytecode interpreter in both freetype 1 and 2.
%define without_bytecode_interpreter    1

%define ft1 freetype-pre1.4

# ttmkfdir shipped as part of freetype packaging in Red Hat Linux 6.2,
# 7.0, 7.1, 7.2, but was moved to XFree86 packaging in Red Hat Linux 7.3
# and later at the request of Ximian.  Set the following appropriately for
# The RHL release freetype is being built for.
%define with_ttmkfdir   0

Summary: A free and portable TrueType font rendering engine.
Name: freetype
Version: 2.1.2
Release: 7
License: GPL
Group: System Environment/Libraries
URL: http://www.freetype.org
Source:  freetype-%{version}.tar.bz2
Source1: ftdocs-%{version}.tar.bz2
Source2: ft2demos-%{version}.tar.bz2
Source3: %{ft1}.tar.bz2
Source100: ttmkfdir2.tar.bz2

Patch0:   freetype-1.4-libtool.patch
Patch20:  freetype-2.1.1-enable-ft2-bci.patch
Patch21:  freetype-1.4-disable-ft1-bci.patch
# Fix bug in PS hinter
patch22:  freetype-2.1.1-primaryhints.patch
# Adds FT_Set_Hint_Flags
patch23:  freetype-2.1.2-slighthint.patch
# Support the Type1 BlueFuzz value
patch24:  freetype-2.1.2-bluefuzz.patch
# Another PS hinter bug fix
patch25:  freetype-2.1.2-stdw.patch
# Fix from CVS for outline transformation
patch26:  freetype-2.1.2-transform.patch
# Backport of autohinter improvements from CVS
patch27:  freetype-2.1.2-autohint.patch
# Fix metrics for PCF fonts
patch28:  freetype-2.1.2-leftright.patch
Patch100: ttmkfdir-libtool.patch
Patch101: ttmkfdir-foundrynames.patch
Patch102: ttmkfdir-gcc31.patch
Patch103: ttmkfdir-iso10646.patch
Buildroot: %{_tmppath}/%{name}-%{version}-root

%description
The FreeType engine is a free and portable TrueType font rendering
engine, developed to provide TrueType support for a variety of
platforms and environments. FreeType is a library which can open and
manages font files as well as efficiently load, hint and render
individual glyphs. FreeType is not a font server or a complete
text-rendering library.


%package utils
Summary: A collection of FreeType utilities.
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}

%description utils
The FreeType engine is a free and portable TrueType font rendering
engine, developed to provide TrueType support for a variety of
platforms and environments. FreeType is a library which can open and
manages font files as well as efficiently load, hint and render
individual glyphs. FreeType is not a font server or a complete
text-rendering library.


%package demos
Summary: A collection of FreeType demos.
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}

%description demos
The FreeType engine is a free and portable TrueType font rendering
engine, developed to provide TrueType support for a variety of
platforms and environments. FreeType is a library which can open and
manages font files as well as efficiently load, hint and render
individual glyphs. FreeType is not a font server or a complete
text-rendering library.


%package devel
Summary: FreeType development libraries and header files
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
The FreeType engine is a free and portable TrueType font rendering
engine, developed to provide TrueType support for a variety of
platforms and environments. FreeType is a library which can open and
manages font files as well as efficiently load, hint and render
individual glyphs. FreeType is not a font server or a complete
text-rendering library.


%prep
%if %{with_ttmkfdir}
%setup -q -b 1 -a 2 -a 3 -a 100
%else
%setup -q -b 1 -a 2 -a 3
%endif

%patch0   -p0 -b .ft1-libtool

%if ! %{without_bytecode_interpreter}
%patch20  -p0 -b .enable-ft2-bci
%else
%patch21  -p0 -b .disable-ft1-bci
%endif

%patch22 -p1 -b .primaryhints
%patch23 -p1 -b .slighthint
%patch24 -p1 -b .bluefuzz
%patch25 -p1 -b .stdw
%patch26 -p1 -b .transform
%patch27 -p1 -b .autohint
%patch28 -p1 -b .leftright

%if %{with_ttmkfdir}
%patch100 -p1 -b .libtool
%patch101 -p1 -b .foundrynames
%patch102 -p0 -b .gcc31
%patch103 -p1 -b .iso10646
%endif

%build
# Build Freetype 2
export CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS"
make setup CFG="--prefix=/usr"
make

# Build Freetype 1.4
cd %{ft1}
%configure --disable-debug \
           --enable-static --enable-shared \
           --with-locale-dir=%{_datadir}/locale
make
cd ..

%if %{with_ttmkfdir}
# Build ttmkfdir
make -C ttmkfdir2 clean
make -C ttmkfdir2 DEBUG="$RPM_OPT_FLAGS"
%endif

# Build freetype 2 demos
pushd ft2demos-%{version}
make X11_PATH="/usr/X11R6" TOP_DIR=".."
popd

%install
rm -rf $RPM_BUILD_ROOT
cd %{ft1}
%makeinstall gnulocaledir=$RPM_BUILD_ROOT/%{_datadir}/locale
cd ..
%makeinstall gnulocaledir=$RPM_BUILD_ROOT/%{_datadir}/locale

%if %{with_ttmkfdir}
libtool install -m 755 ttmkfdir2/ttmkfdir $RPM_BUILD_ROOT%{_bindir}
%endif

mkdir -p $RPM_BUILD_ROOT/%{_prefix}/include/freetype1
mv $RPM_BUILD_ROOT/%{_prefix}/include/freetype $RPM_BUILD_ROOT/%{_prefix}/include/freetype1

# Install freetype 2 demos
for ftdemo in ftdump ftlint ftmemchk ftmulti ftstring fttimer ftview ;do
    libtool install -m 755 ft2demos-%{version}/bin/$ftdemo $RPM_BUILD_ROOT/usr/bin
done

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%triggerpostun -- freetype < 2.0.5-3
# ttmkfdir updated - as of 2.0.5-3, on upgrades we need xfs to regenerate things to get the iso10646-1 encoding listed.
for I in /usr/share/fonts/*/TrueType /usr/X11R6/lib/X11/fonts/TrueType; do
	[ -f $I/fonts.scale ] && [ -f $I/fonts.dir ] && touch $I/fonts.scale
done
exit 0

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
%if %{with_ttmkfdir}
%{_bindir}/ttmkfdir
%endif
%{_libdir}/libttf.so.*
%{_libdir}/libfreetype.so.*
%doc %{ft1}/README %{ft1}/announce docs

%files utils
%defattr(-,root,root)
# 2.0.4 version included in demos package now
#%{_bindir}/ftdump
%{_bindir}/fterror
# 2.0.4 version included in demos package now
#%{_bindir}/ftlint
%{_bindir}/ftmetric
%{_bindir}/ftsbit
%{_bindir}/ftstrpnm

%files demos
%defattr(-,root,root)
%{_bindir}/ftdump
%{_bindir}/ftlint
%{_bindir}/ftmemchk
%{_bindir}/ftmulti
%{_bindir}/ftstring
%{_bindir}/fttimer
%{_bindir}/ftview

%files devel
%defattr(-,root,root)
%dir %{_includedir}/freetype1
%dir %{_includedir}/freetype2
%{_includedir}/freetype1/*
%{_includedir}/freetype2/*
%{_includedir}/*.h
%{_libdir}/libttf.a
%{_libdir}/libttf.la
%{_libdir}/libttf.so
%{_libdir}/libfreetype.a
%{_libdir}/libfreetype.la
%{_libdir}/libfreetype.so
%{_bindir}/freetype-config

%changelog
* Wed Aug 28 2002 Owen Taylor <otaylor@redhat.com>
- Fix a bug with PCF metrics

* Fri Aug  9 2002 Owen Taylor <otaylor@redhat.com>
- Backport autohinter improvements from CVS

* Tue Jul 23 2002 Owen Taylor <otaylor@redhat.com>
- Fix from CVS for transformations (#68964)

* Tue Jul  9 2002 Owen Taylor <otaylor@redhat.com>
- Add another bugfix for the postscript hinter

* Mon Jul  8 2002 Owen Taylor <otaylor@redhat.com>
- Add support for BlueFuzz private dict value, fixing rendering 
  glitch for Luxi Mono.

* Wed Jul  3 2002 Owen Taylor <otaylor@redhat.com>
- Add an experimental FT_Set_Hint_Flags() call

* Mon Jul  1 2002 Owen Taylor <otaylor@redhat.com>
- Update to 2.1.2
- Add a patch fixing freetype PS hinter bug

* Fri Jun 21 2002 Mike A. Harris <mharris@redhat.com> 2.1.1-2
- Added ft rpm build time conditionalizations upon user requests

* Tue Jun 11 2002 Owen Taylor <otaylor@redhat.com> 2.1.1-1
- Version 2.1.1

* Mon Jun 10 2002 Owen Taylor <otaylor@redhat.com>
- Add a fix for PCF character maps

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri May 17 2002 Mike A. Harris <mharris@redhat.com> 2.1.0-2
- Updated freetype to version 2.1.0
- Added libtool fix for freetype 1.4 (#64631)

* Wed Mar 27 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.9-2
- use "libtool install" instead of "install" to install some binaries (#62005)

* Mon Mar 11 2002 Mike A. Harris <mharris@redhat.com> 2.0.9-1
- Updated to freetype 2.0.9

* Sun Feb 24 2002 Mike A. Harris <mharris@redhat.com> 2.0.8-4
- Added proper docs+demos source for 2.0.8.

* Sat Feb 23 2002 Mike A. Harris <mharris@redhat.com> 2.0.8-3
- Added compat patch so 2.x works more like 1.x
- Rebuilt with new build toolchain

* Fri Feb 22 2002 Mike A. Harris <mharris@redhat.com> 2.0.8-2
- Updated to freetype 2.0.8, however docs and demos are stuck at 2.0.7
  on the freetype website.  Munged specfile to deal with the problem by using
  {oldversion} instead of version where appropriate.  <sigh>

* Sat Feb  2 2002 Tim Powers <timp@redhat.com> 2.0.6-3
- bumping release so that we don't collide with another build of
  freetype, make sure to change the release requirement in the XFree86
  package

* Fri Feb  1 2002 Mike A. Harris <mharris@redhat.com> 2.0.6-2
- Made ttmkfdir inclusion conditional, and set up a define to include
  ttmkfdir in RHL 7.x builds, since ttmkfdir is now moving to the new
  XFree86-font-utils package.

* Wed Jan 16 2002 Mike A. Harris <mharris@redhat.com> 2.0.6-1
- Updated freetype to version 2.0.6

* Wed Jan 09 2002 Tim Powers <timp@redhat.com> 2.0.5-4
- automated rebuild

* Fri Nov 30 2001 Elliot Lee <sopwith@redhat.com> 2.0.5-3
- Fix bug #56901 (ttmkfdir needed to list Unicode encoding when generating
  font list). (ttmkfdir-iso10646.patch)
- Use _smp_mflags macro everywhere relevant. (freetype-pre1.4-make.patch)
- Undo fix for #24253, assume compiler was fixed.

* Mon Nov 12 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.0.5-2
- Fix build with gcc 3.1 (#56079)

* Sun Nov 11 2001 Mike A. Harris <mharris@redhat.com> 2.0.5-1
- Updated freetype to version 2.0.5

* Sat Sep 22 2001 Mike A. Harris <mharris@redhat.com> 2.0.4-2
- Added new subpackage freetype-demos, added demos to build
- Disabled ftdump, ftlint in utils package favoring the newer utils in
  demos package.

* Tue Sep 11 2001 Mike A. Harris <mharris@redhat.com> 2.0.4-1
- Updated source to 2.0.4
- Added freetype demo's back into src.rpm, but not building yet.

* Wed Aug 15 2001 Mike A. Harris <mharris@redhat.com> 2.0.3-7
- Changed package to use {findlang} macro to fix bug (#50676)

* Sun Jul 15 2001 Mike A. Harris <mharris@redhat.com> 2.0.3-6
- Changed freetype-devel to group Development/Libraries (#47625)

* Mon Jul  9 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.0.3-5
- Fix up FT1 headers to please Qt 3.0.0 beta 2

* Sun Jun 24 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.0.3-4
- Add ft2build.h to -devel package, since it's included by all other
  freetype headers, the package is useless without it

* Thu Jun 21 2001 Nalin Dahyabhai <nalin@redhat.com> 2.0.3-3
- Change "Requires: freetype = name/ver" to "freetype = version/release",
  and move the requirements to the subpackages.

* Mon Jun 18 2001 Mike A. Harris <mharris@redhat.com> 2.0.3-2
- Added "Requires: freetype = name/ver"

* Tue Jun 12 2001 Mike A. Harris <mharris@redhat.com> 2.0.3-1
- Updated to Freetype 2.0.3, minor specfile tweaks.
- Freetype2 docs are is in a separate tarball now. Integrated it.
- Built in new environment.

* Fri Apr 27 2001 Bill Nottingham <notting@redhat.com>
- rebuild for C++ exception handling on ia64

* Sat Jan 20 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Build ttmkfdir with -O0, workaround for Bug #24253

* Fri Jan 19 2001 Nalin Dahyabhai <nalin@redhat.com>
- libtool is used to build libttf, so use libtool to link ttmkfdir with it
- fixup a paths for a couple of missing docs

* Thu Jan 11 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Update ttmkfdir

* Wed Dec 27 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Update to 2.0.1 and 1.4
- Mark locale files as such

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jun 12 2000 Preston Brown <pbrown@redhat.com>
- move .la file to devel pkg
- FHS paths

* Thu Feb 17 2000 Preston Brown <pbrown@redhat.com>
- revert spaces patch, fix up some foundry names to match X ones

* Mon Feb 07 2000 Nalin Dahyabhai <nalin@redhat.com>
- add defattr, ftmetric, ftsbit, ftstrtto per bug #9174

* Wed Feb 02 2000 Cristian Gafton <gafton@redhat.com>
- fix description and summary

* Wed Jan 12 2000 Preston Brown <pbrown@redhat.com>
- make ttmkfdir replace spaces in family names with underscores (#7613)

* Tue Jan 11 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 1.3.1
- handle RPM_OPT_FLAGS

* Wed Nov 10 1999 Preston Brown <pbrown@redhat.com>
- fix a path for ttmkfdir Makefile

* Thu Aug 19 1999 Preston Brown <pbrown@redhat.com>
- newer ttmkfdir that works better, moved ttmkfdir to /usr/bin from /usr/sbin
- freetype utilities moved to subpkg, X dependency removed from main pkg
- libttf.so symlink moved to devel pkg

* Mon Mar 22 1999 Preston Brown <pbrown@redhat.com>
- strip binaries

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 5)

* Thu Mar 18 1999 Cristian Gafton <gafton@redhat.com>
- fixed the %doc file list

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- Injected new description and group.

* Mon Feb 15 1999 Preston Brown <pbrown@redhat.com>
- added ttmkfdir

* Tue Feb 02 1999 Preston Brown <pbrown@redhat.com>
- update to 1.2

* Thu Jan 07 1999 Cristian Gafton <gafton@redhat.com>
- call libtoolize to sanitize config.sub and get ARM support
- dispoze of the patch (not necessary anymore)

* Wed Oct 21 1998 Preston Brown <pbrown@redhat.com>
- post/postun sections for ldconfig action.

* Tue Oct 20 1998 Preston Brown <pbrown@redhat.com>
- initial RPM, includes normal and development packages.
