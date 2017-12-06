
# packaging notes:
#
# XXX Group "Backup Server" is unknown (f22+)
# XXX use a dedicated user for burp ?
# XXX link against tcpwrappers ?
# XXX SElinux stuff ?
# XXX remove packaging notes.

Name:		burp2
Summary:	A Network-based backup and restore program
Version:	2.1.24
Release:	1%{?dist}
Group:		Backup Server
License:	AGPLv3 and BSD and GPLv2+ and LGPLv2+
URL:		http://burp.grke.org/
Source0:	http://downloads.sourceforge.net/project/burp/burp-%{version}/burp-%{version}.tar.bz2
Source1:	burp.init
Source2:	burp.service

%if 0%{?rhel} < 7
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
%endif

BuildRequires:	libtool
BuildRequires:	librsync-devel
BuildRequires:	zlib-devel
BuildRequires:	openssl-devel
BuildRequires:	ncurses-devel
BuildRequires:	libacl-devel
BuildRequires:	uthash-devel
BuildRequires:	yajl-devel

%if 0%{?fedora} >= 19 || 0%{?rhel} >= 7
BuildRequires:	systemd-units
%endif


%description
Burp is a network backup and restore program, using client and server.
It uses librsync in order to save network traffic and to save on the 
amount of space that is used by each backup. 
It also uses VSS (Volume Shadow Copy Service) to make snapshots when 
backing up Windows computers.

%package client
Summary:	burp backup client
Group:		Backup Server
Requires:	librsync >= 1.0
Provides:	burp = %{version}-%{release}
Provides:	burp2-client = %{version}-%{release}

# burp 1.x (burp-) and 2.x (burp2-*) are both available. 
# Put conflicts on -client package since -server package relies on it.
Conflicts:	burp-client
# for burp < 1.4.40 (package name changed)
Conflicts:	burp < 2.0


%description client
Burp is a network backup and restore program, using client and server.
It uses librsync in order to save network traffic and to save on the 
amount of space that is used by each backup. 
It also uses VSS (Volume Shadow Copy Service) to make snapshots when 
backing up Windows computers.


%package doc
Summary:	Documentation and samples for Burp backup
Group:		Backup Server
# RHEL 5 does not support noarch subpackages
%if 0%{?fedora} || 0%{?rhel} >= 6
BuildArch:	noarch
%endif

%description doc
Burp is a network backup and restore program, using client and server.
It uses librsync in order to save network traffic and to save on the 
amount of space that is used by each backup. 
It also uses VSS (Volume Shadow Copy Service) to make snapshots when 
backing up Windows computers.


%package server
Summary:	burp backup server
Group:		Backup Server
Requires:	burp2-client%{?_isa} = %{version}-%{release}
Requires:	openssl-perl
Provides:	bedup = %{version}-%{release}
Provides:	vss_strip = %{version}-%{release}


%description server
Burp is a network backup and restore program, using client and server.
It uses librsync in order to save network traffic and to save on the 
amount of space that is used by each backup. 
It also uses VSS (Volume Shadow Copy Service) to make snapshots when 
backing up Windows computers.

%prep
%setup -q -n burp-%{version}

%build
%configure --sysconfdir=%{_sysconfdir}/burp --docdir=%{_defaultdocdir}/%{name}-%{version}
make %{?_smp_mflags}


%install
# "install-all" target: also install config files and scripts
make install-all DESTDIR=%{buildroot}

# service files (server)
%if 0%{?fedora} >= 19 || 0%{?rhel} >= 7
mkdir -p %{buildroot}%{_unitdir}
install -p -m 0644 %{SOURCE2} %{buildroot}%{_unitdir}/
%else
mkdir -p %{buildroot}%{_initrddir}
install -p -m 0755 %{SOURCE1} %{buildroot}%{_initrddir}/burp
%endif

# -doc: add server scripts examples
%global mydocbuild %{buildroot}%{_defaultdocdir}/%{name}-%{version}
mkdir -p %{mydocbuild}/server/scripts
cp -p configs/server/cron.example %{mydocbuild}/server/.
cp -p configs/server/out_of_date_report_script \
      configs/server/offsite-backup \
      %{mydocbuild}/server/scripts/.

# -doc: add server config examples (excluding -client's ones)
mkdir -p %{mydocbuild}/server/config/autoupgrade
cp -p configs/server/autoupgrade/*.script %{mydocbuild}/server/config/autoupgrade/.
cp -pr %{buildroot}%{_sysconfdir}/burp/.  %{mydocbuild}/server/config/.
rmdir %{mydocbuild}/server/config/CA-client
rm %{mydocbuild}/server/config/burp.conf

# -doc: add client scripts and config examples
mkdir -p %{mydocbuild}/client
cp -p configs/client/cron.example \
      configs/client/zfs_script \
      %{buildroot}%{_sysconfdir}/burp/burp.conf \
      %{mydocbuild}/client/.

# -server: do not provide a (test)client
rm %{buildroot}%{_sysconfdir}/burp/clientconfdir/testclient

%files doc
%{_defaultdocdir}/%{name}-%{version}/


%files client
%defattr(-,root,root,-)
%doc README CHANGELOG DONATIONS TODO CONTRIBUTORS UPGRADING
%if 0%{?rhel} <= 6
	%doc LICENSE
%else
	%license LICENSE
%endif
%config(noreplace) %{_sysconfdir}/burp/burp.conf
%dir %{_sysconfdir}/burp/CA-client
%dir %{_sysconfdir}/burp
%{_sbindir}/burp
# yes, burp_ca is needed in client package
%{_sbindir}/burp_ca
%{_mandir}/man8/burp.8*
%{_mandir}/man8/burp_ca.8*


%files server
%{_datadir}/burp
%config(noreplace) %{_sysconfdir}/burp/CA.cnf
%config(noreplace) %{_sysconfdir}/burp/burp-server.conf
%config(noreplace) %{_sysconfdir}/burp/clientconfdir/incexc/example
%dir %{_sysconfdir}/burp/clientconfdir/incexc
%dir %{_sysconfdir}/burp/clientconfdir
%dir %{_localstatedir}/spool/burp %attr(750 root root)
%{_bindir}/vss_strip
%{_sbindir}/bsigs
%{_sbindir}/bedup
%{_sbindir}/bsparse
%{_mandir}/man8/vss_strip.8*
%{_mandir}/man8/bedup.8*
%{_mandir}/man8/bsigs.8*
%{_mandir}/man8/bsparse.8*
%if 0%{?fedora} >= 19 || 0%{?rhel} >= 7
%{_unitdir}/burp.service
%else
%{_initrddir}/burp
%endif

%post server
%if 0%{?fedora} >= 19 || 0%{?rhel} >= 7
%systemd_post burp.service
%else
/sbin/chkconfig --add burp
%endif

%preun server
%if 0%{?fedora} >= 19 || 0%{?rhel} >= 7
%systemd_preun burp.service
%else
if [ $1 = 0 ]; then
  /sbin/service burp stop > /dev/null 2>&1
  /sbin/chkconfig --del burp
fi
%endif

%postun server
%if 0%{?fedora} >= 19 || 0%{?rhel} >= 7
%systemd_postun_with_restart burp.service
%else
if [ $1 -eq 2 ]; then
    /sbin/service burp upgrade || :
fi
%endif


%changelog
* Wed Dec 06 2017 Pierre Bourgin <pierre.bourgin@free.fr> - 2.1.24-1
- Updated to latest version

* Sun Nov 05 2017 Pierre Bourgin <pierre.bourgin@free.fr> - 2.1.22-1
- Updated to latest version

* Sun Oct 01 2017 Pierre Bourgin <pierre.bourgin@free.fr> - 2.1.20-1
- Updated to latest version

* Thu Aug 17 2017 Pierre Bourgin <pierre.bourgin@free.fr> - 2.1.16-1
- Updated to latest version

* Sat Aug 05 2017 Pierre Bourgin <pierre.bourgin@free.fr> - 2.1.14-1
- Updated to latest version

* Wed Jul 05 2017 Pierre Bourgin <pierre.bourgin@free.fr> - 2.1.12-1
- Updated to latest version

* Tue May 02 2017 Pierre Bourgin <pierre.bourgin@free.fr> - 2.1.8-1
- Updated to latest version

* Wed Apr 05 2017 Pierre Bourgin <pierre.bourgin@free.fr> - 2.1.6-1
- Updated to latest version

* Sat Mar 11 2017 Pierre Bourgin <pierre.bourgin@free.fr> - 2.1.4-1
- Updated to latest version
- new bsparse utility: -server package

* Tue Jan 03 2017 Pierre Bourgin <pierre.bourgin@free.fr> - 2.0.54-1
- Updated to latest released version

* Wed Nov 09 2016 Pierre Bourgin <pierre.bourgin@free.fr> - 2.0.52-1
- Updated to latest released version

* Thu Nov 03 2016 Pierre Bourgin <pierre.bourgin@free.fr> - 2.0.50-1
- Updated to latest released version

* Sat Oct 01 2016 Pierre Bourgin <pierre.bourgin@free.fr> - 2.0.48-1
- Updated to latest released version

* Tue Sep 06 2016 Pierre Bourgin <pierre.bourgin@free.fr> - 2.0.46-1
- Updated to latest released version

* Mon Aug 15 2016 Pierre Bourgin <pierre.bourgin@free.fr> - 2.0.44-2
- Removed 'Provides: burp-server' property (fix https://github.com/yopito/fedora-epel-pkg/issues/2)

* Thu Aug 04 2016 Pierre Bourgin <pierre.bourgin@free.fr> - 2.0.44-1
- Updated to latest released version

* Sun Jul 03 2016 Pierre Bourgin <pierre.bourgin@free.fr> - 2.0.42-1
- Updated to latest released version

* Sat Jun 04 2016 Pierre Bourgin <pierre.bourgin@free.fr> - 2.0.40-1
- Updated to latest released version
- merge spec with el5 branch
- do not use autoreconf anymore
- include fix on status monitor
- do not provide a (test)client configuration

* Wed May 04 2016 Pierre Bourgin <pierre.bourgin@free.fr> - 2.0.38-2
- fix ncurses monitoring for a given client ("-C" option)

* Mon May 02 2016 Pierre Bourgin <pierre.bourgin@free.fr> - 2.0.38-1
- Bumped to 2.0.38
- Updated source location to SourceForge

* Mon Apr 04 2016 Pierre Bourgin <pierre.bourgin@free.fr> - 2.0.36-1
- Updated to latest released version

* Wed Mar 02 2016 Pierre Bourgin <pierre.bourgin@free.fr> - 2.0.34-1
- Initial spec file for burp2 package (forked from burp 1.x)
- Mark conflicts with burp* 1.x packages
- Added burp2-doc package: documentation, config samples
- burp2-server: flag 'testclient' as config file

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.40-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jul 08 2015 Pierre Bourgin <pierre.bourgin@free.fr> - 1.4.40-1
- bumped to 1.4.40
- provides burp-{client,server} packages now.
- rewrite to match EPEL SPEC file (http://pkgs.fedoraproject.org/cgit/burp.git/tree/burp.spec)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.36-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri May 15 2015 Andrew Niemantsverdriet <andrewniemants@gmail.com> - 1.4.36.6
- Added two configuration files so they would not be overwritten on update

* Wed May 13 2015 Andrew Niemantsverdriet <andrewniemants@gmail.com> - 1.4.36.5
- Only use license with compatible operating systems
- Fixed typo _initrdir -> _initddir and made sure the file gets the correct name

* Wed May 13 2015 Andrew Niemantsverdriet <andrewniemants@gmail.com> - 1.4.36.4
- Made systemd-units a conditional BuildRequire

* Tue May 12 2015 Andrew Niemantsverdriet <andrewniemants@gmail.com> - 1.4.36-3
- Updated licence field

* Sat May 09 2015 Andrew Niemantsverdriet <andrewniemants@gmail.com> - 1.4.36-2
- Added systemd-units as a build require

* Sat May 09 2015 Andrew Niemantsverdriet <andrewniemants@gmail.com> - 1.4.36-1
- Updated to latest stable version

* Fri May 08 2015 Andrew Niemantsverdriet <andrewniemants@gmail.com> - 1.3.48-6
- Changed the build require from uthash to uthash-devel

* Tue Mar 17 2015 Andrew Niemantsverdriet <andrewniemants@gmail.com> - 1.3.48-5
- Fixed scriptlets to correctly handle systemd

* Tue Feb 17 2015 Andrew Niemantsverdriet <andrewniemants@gmail.com> - 1.3.48-4
- Added scriptlets to handle systemd

* Mon Feb 09 2015 Andrew Niemantsverdriet <andrewniemants@gmail.com> - 1.3.48-3
- Split BuildRequires into one per line
- Moved the LICENSE file to the license macro
- Fixed spacing issue

* Mon Feb 02 2015 Andrew Niemantsverdriet <andrewniemants@gmail.com> - 1.3.48-2
- removed clean section of spec file
- changed install and files to conform to packaging guideline

* Tue Nov 25 2014 Andrew Niemantsverdriet <andrewniemants@gmail.com> - 1.3.48-1
- Initial spec file
