%define ft1 freetype-pre1.4

Summary: A free and portable TrueType font rendering engine.
Name: freetype
Version: 2.0.3
Release: 6
License: GPL
Group: System Environment/Libraries
URL: http://freetype.sourceforge.net
Source: freetype-%{version}.tar.bz2
Source1: ftdocs-2.0.3.tar.bz2
Source3: %{ft1}.tar.bz2
Source4: ttmkfdir2.tar.bz2
Patch0: ttmkfdir-libtool.patch
Patch1: ttmkfdir-foundrynames.patch
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
%setup -q -b 1 -a 3 -a 4
%patch0 -p1 -b .libtool
%patch1 -p1 -b .foundrynames

%build
export CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS"
make setup CFG="--prefix=/usr"
make
cd %{ft1}
%configure --disable-debug \
           --enable-static --enable-shared \
           --with-locale-dir=%{_datadir}/locale
make
cd ..
make -C ttmkfdir2 clean
make -C ttmkfdir2 #DEBUG="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
cd %{ft1}
%makeinstall gnulocaledir=$RPM_BUILD_ROOT/%{_datadir}/locale
cd ..
%makeinstall gnulocaledir=$RPM_BUILD_ROOT/%{_datadir}/locale
install -m 755 ttmkfdir2/.libs/ttmkfdir $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT/%{_prefix}/include/freetype1
mv $RPM_BUILD_ROOT/%{_prefix}/include/freetype $RPM_BUILD_ROOT/%{_prefix}/include/freetype1

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/ttmkfdir
%{_libdir}/libttf.so.*
%{_libdir}/libfreetype.so.*
%lang(de) %{_datadir}/locale/de/*
%lang(fr) %{_datadir}/locale/fr/*
%lang(cs) %{_datadir}/locale/cs/*
%lang(nl) %{_datadir}/locale/nl/*
%lang(es) %{_datadir}/locale/es/*
%doc %{ft1}/README %{ft1}/announce docs

%files utils
%defattr(-,root,root)
%{_bindir}/ftdump
%{_bindir}/fterror
%{_bindir}/ftlint
%{_bindir}/ftmetric
%{_bindir}/ftsbit
%{_bindir}/ftstrpnm

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
