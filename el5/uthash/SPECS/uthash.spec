# This package builds a header-only lib, but has some testsuite to check
# the headers' function.  For this reason the main-pkg is build arched and
# produces a noarched subpkg, only.  There is no binary-compiled bits and
# therefore no debuginfo generated.
%global debug_package %{nil}

Name:           uthash
Group:          Development
Version:        1.9.9
Release:        7%{?dist}
Summary:        A hash table for C structures
License:        BSD
URL:            http://troydhanson.github.io/uthash
Source0:        https://github.com/troydhanson/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

%if 0%{?rhel} < 7
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
%endif

%description
Any C structure can be stored in a hash table using uthash. Just add a
UT_hash_handle to the structure and choose one or more fields in your 
structure to act as the key. Then use these macros to store, retrieve or 
delete items from the hash table. 

%package        devel
Group:          Development
Summary:        Development files for %{name}
Provides:       %{name} = %{version}-%{release}
Provides:       %{name}-static = %{version}-%{release}
BuildArch:      noarch

%description    devel
This package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q

%build
# This is a header only package.

%install
install -d %{buildroot}%{_includedir}
install -pm0644 src/*.h %{buildroot}%{_includedir}/

%check
cd tests && make %{?_smp_mflags}

%files devel
%doc LICENSE doc/*.txt
%{_includedir}/ut*.h

%changelog
* Wed May 25 2016 Pierre Bourgin <pierre.bourgin@fre.fr> - 1.9.9-7
- define %%buildroot if <el7 (for el5 support)

* Wed May 28 2014 Björn Esser <bjoern.esser@gmail.com> - 1.9.9-6
- add `%%global debug_package %%{nil}` to avoid empty debuginfo-pkg.

* Thu May 22 2014 Björn Esser <bjoern.esser@gmail.com> - 1.9.9-5
- revert "Root package should be noarch too".
- add provides %%{name} for -devel subpkg.
- add a note about why the mainpkg is arched.

* Wed May 21 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.9.9-4
- Root package should be noarch too

* Wed May 21 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.9.9-3
- Build as noarch

* Sun May 18 2014 Christopher Meng <rpm@cicku.me> - 1.9.9-2
- Move all files to -devel subpkg.

* Sat Mar 29 2014 Christopher Meng <rpm@cicku.me> - 1.9.9-1
- Update to 1.9.9

* Sat Jun 15 2013 Christopher Meng <rpm@cicku.me> - 1.9.8-3
- Add virtual provide.
- Remove 2 wrong tests.

* Fri Jun 14 2013 Christopher Meng <rpm@cicku.me> - 1.9.8-2
- Remove unneeded BR and make files section more clear.

* Sat Jun 01 2013 Christopher Meng <rpm@cicku.me> - 1.9.8-1
- Initial Package.
