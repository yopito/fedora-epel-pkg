Name:		burp
Summary:	A network-based backup and restore program
Version:	1.4.40
Release:	4%{?dist}
Group:		Backup Server
License:	AGPLv3 and BSD and GPLv2+ and LGPLv2+
URL:		http://burp.grke.org/
Source0:	https://github.com/grke/burp/archive/%{version}.tar.gz
Source1:	burp.init
Source2:	burp.service
# Workaround to RHBZ#1307363
# Caused by narrowing props on arm and i386
# Approach adopted from src/conffile.c in burb-2.0.32
Patch0:		burp-1.4.40-narrowing.patch
Patch1:		burp-1.4.40_burp_ca-lock.patch
%if 0%{?rhel} < 7
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
%endif
BuildRequires:	librsync-devel
BuildRequires:	zlib-devel
BuildRequires:	openssl-devel
BuildRequires:	ncurses-devel
BuildRequires:	libacl-devel
# burp 1.x provides its own uthash
#BuildRequires:	uthash-devel
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
Provides:	burp-client = %{version}-%{release}

%description client
Burp is a network backup and restore program, using client and server.
It uses librsync in order to save network traffic and to save on the 
amount of space that is used by each backup. 
It also uses VSS (Volume Shadow Copy Service) to make snapshots when 
backing up Windows computers.

%package server
Summary:	burp backup server
Group:		Backup Server
Requires:	burp-client%{?_isa} = %{version}-%{release}
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
%setup -q -n %{name}-%{version}
%patch0 -p1

%build
%configure --sysconfdir=%{_sysconfdir}/%{name}
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
%if 0%{?fedora} >= 19 || 0%{?rhel} >= 7
mkdir -p %{buildroot}%{_unitdir}
install -p -m 0644 %{SOURCE2} %{buildroot}%{_unitdir}/
%else
mkdir -p %{buildroot}%{_initrddir}
install -p -m 0755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}
%endif

# a copy is present in doc stuff
rm -f %{buildroot}%{_sysconfdir}/burp/clientconfdir/testclient
rm -f %{buildroot}%{_sysconfdir}/burp/clientconfdir/incexc/example

%files client
%defattr(-,root,root,-)
%doc README CHANGELOG DONATIONS TODO CONTRIBUTORS UPGRADING
%doc configs/client
%if 0%{?rhel} <= 6
	%doc LICENSE
%else
	%license LICENSE
%endif
%config(noreplace) %{_sysconfdir}/burp/burp.conf
%dir %{_sysconfdir}/burp/CA-client
%dir %{_sysconfdir}/burp
%{_sbindir}/burp
%{_sbindir}/burp_ca
%{_mandir}/man8/burp.8*

%files server
%doc docs/*
%doc configs/server
%config(noreplace) %{_sysconfdir}/burp/CA.cnf
%config(noreplace) %{_sysconfdir}/burp/burp-server.conf
%config(noreplace) %{_sysconfdir}/burp/timer_script
%config(noreplace) %{_sysconfdir}/burp/summary_script
%config(noreplace) %{_sysconfdir}/burp/notify_script
%config(noreplace) %{_sysconfdir}/burp/ssl_extra_checks_script
%config(noreplace) %{_sysconfdir}/burp/autoupgrade/server/win32/script
%config(noreplace) %{_sysconfdir}/burp/autoupgrade/server/win64/script
%dir %{_sysconfdir}/burp/autoupgrade/server/win32
%dir %{_sysconfdir}/burp/autoupgrade/server/win64
%dir %{_sysconfdir}/burp/autoupgrade/server
%dir %{_sysconfdir}/burp/autoupgrade
%dir %{_sysconfdir}/burp/clientconfdir/incexc
%dir %{_sysconfdir}/burp/clientconfdir
%dir %{_localstatedir}/spool/burp %attr(750 root root)
%{_sbindir}/vss_strip
%{_sbindir}/bedup
%{_mandir}/man8/vss_strip.8*
%{_mandir}/man8/bedup.8*
%{_mandir}/man8/burp_ca.8*
%if 0%{?fedora} >= 19 || 0%{?rhel} >= 7
%{_unitdir}/burp.service
%else
%{_initrddir}/%{name}
%endif

%post server
%if 0%{?fedora} >= 19 || 0%{?rhel} >= 7
%systemd_post burp.service
%else
/sbin/chkconfig --add %{name}
%endif

%preun server
%if 0%{?fedora} >= 19 || 0%{?rhel} >= 7
%systemd_preun burp.service
%else
if [ $1 = 0 ]; then
  /sbin/service %{name} stop > /dev/null 2>&1
  /sbin/chkconfig --del %{name}
fi
%endif

%if 0%{?fedora} >= 19 || 0%{?rhel} >= 7
%postun server
%systemd_postun_with_restart burp.service
%endif


%changelog
* Sun Mar 13 2016 Pierre Bourgin <pierre.bourgin@free.fr> - 1.4.40-4
- client: fix race condition in burp_ca
- server: use glob for docs/* files.
- copy <source>/configs/<subpkg>/ into their documentation (including crontab samples)
- fix for rhel5 building.

* Fri Feb 19 2016 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.4.40-3
- Add burp-1.4.40-narrowing.patch (F24FTBFS, RHBZ#1307363).

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
