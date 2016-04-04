
# packaging notes:
#
# XXX Group "Backup Server" is unknown (f22+)
# XXX use a dedicated user for burp ?
# XXX SElinux stuff ?
# XXX remove packaging notes.

Name:		burp2
Summary:	A Network-based backup and restore program
Version:	2.0.36
Release:	1%{?dist}
Group:		Backup Server
License:	AGPLv3 and BSD and GPLv2+ and LGPLv2+
URL:		http://burp.grke.org/
Source0:	https://github.com/grke/burp/archive/%{version}.tar.gz#/burp-%{version}.tar.gz
Source1:	burp.init
Source2:	burp.service
BuildRequires:	autoconf
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
BuildArch:	noarch

%description doc
Burp is a network backup and restore program, using client and server.
It uses librsync in order to save network traffic and to save on the 
amount of space that is used by each backup. 
It also uses VSS (Volume Shadow Copy Service) to make snapshots when 
backing up Windows computers.


%package server
Summary:	burp backup server
Requires:	burp2-client%{?_isa} = %{version}-%{release}
Requires:	openssl-perl
Provides:	burp-server = %{version}-%{release}
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
autoreconf -vif
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
mkdir -p %{buildroot}%{_initddir}
install -p -m 0755 %{SOURCE1} %{buildroot}%{_initddir}/burp
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
%config(noreplace) %{_sysconfdir}/burp/clientconfdir/testclient
%dir %{_sysconfdir}/burp/clientconfdir/incexc
%dir %{_sysconfdir}/burp/clientconfdir
%dir %{_localstatedir}/spool/burp %attr(750 root root)
%{_bindir}/vss_strip
%{_sbindir}/bsigs
%{_sbindir}/bedup
%{_mandir}/man8/vss_strip.8*
%{_mandir}/man8/bedup.8*
%{_mandir}/man8/bsigs.8*
%if 0%{?fedora} >= 19 || 0%{?rhel} >= 7
%{_unitdir}/burp.service
%else
%{_initddir}/burp
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
