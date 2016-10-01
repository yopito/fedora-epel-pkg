
This git repo hosts the source RPM files used to generate binary packages of various softwares:

* burp backup software  
    Related COPR space (hosts binary packages): https://copr.fedorainfracloud.org/coprs/yopito/burp2/

Content:

* [Changelog](#changelog)
* [burp2 packaging status](#burp2-packaging-status)
* [burp 1.x packaging status](#burp-1x-packaging-status)
* [howto use these source packaging](#howto-use-these-source-packaging)


## Changelog

* 2016-10-01 packaged burp 2.0.48 (el5, el6, el7, fedora*)
* 2016-09-06 packaged burp 2.0.46 (el5, el6, el7, fedora*)
* 2016-08-15 fixed burp2-server packaging: remove 'burp-server' property
* 2016-08-04 packaged burp 2.0.44 (el5, el6, el7, fedora*)
* 2016-07-03 packaged burp 2.0.42 (el5, el6, el7, fedora*)
* 2016-06-04 packaged burp 2.0.40 (el5 and others)
* 2016-05-27 package burp 2.0.38 for el5 (RHEL5, CentOS5) platforms
* 2016-05-02 updated to burp 2.0.38
* 2016-05-02 reorganize file structure, added a howto
* 2016-04-04 update to burp 2.0.36
* 2016-03-14 add el5 branch for burp 1.x packaging
* 2016-03-09 add burp2 packaging
* 2016-03-09 add tito stuff inside git repo
* 2016-03-09 initialize git repo

## burp2 packaging status

At this time of writing (2016-05), burp 2.x is not available neither by EPEL yum channel nor Fedora project.  
Here the status of building this software against various distributions:

* el5, el6, el7 : building/packaging is fine
* fedora 22, 23, 24 and fedora-rawhide: building/packaging is fine
* XXX COPR building for arch ARM is unusable, too much wait (2016-02)

NB: elx = RHELx and derivatives  (CentOS x, ScientificLinux x, etc)


## burp 1.x packaging status

version: 1.4.40 (2016-03)

* EPEL channel provides binary package of burp 1.x for el6 and el7, but NOT for el5.
* FedoraProject provides burp 1.x packaging for Fedora 22, Fedora 23, and Fedora-rawhide

* el5 (RHEL5, CentOS 5):
    * not provided by EPEL repository for burp 1.x (as this time of writing)
    * build is fine with the .spec file provided by the 'el5' branch of this repo.
    * need yajl-devel package too, that has to be built to (branch 'el5').
    * does not need uthash package, since uthash provided in burp 1.x source code.
        (that is nice since uthash is not packaged for el5, either in OS, update or EPEL yum channels)


## Howto to build RPMs from this git repo

If you don't want to use the binary packages from the COPR space hosted by Fedora, you can use the packaging provided here.  
Here the instructions to achieve it.

* branch `el5` : source packaging for el5 (RHEL5, CentOS5, etc)
* branch `master` : source packaging for all other platforms than el5

Getting tired of `tito` stuff, I use a more conventional file structure:

```
<pkg>/SPECS/ ......... contains the Specfile of package <pkg>
<pkg>/SOURCES/ ....... contains all needed source files
```

Usage: 

* install and enable use of the EPEL repo

* launch the build of a (binary) package:  
    ```
cd <pkg>
mkdir -p RPMS BUILD SRPMS
rpmbuild --define="_topdir $(pwd)" -bb SPECS/<pkg>.spec
    ```

* build a SRPM source package into `<pkg>/SPRMS/` folder:  
    ```
cd <pkg>
mkdir -p SRPMS
rpmbuild --define="_topdir $(pwd)" -bs SPECS/<pkg>.spec
    ```

To request a build with COPR infrastructure, choose to generate from a SRPM file that you upload. 
