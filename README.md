
Packaging for Fedora/EPEL using Fedora COPR building system.

Related COPR space: https://copr.fedorainfracloud.org/coprs/yopito/burp2/

Changelog: 

* 2016-05-02 updated to burp 2.0.38
* 2016-05-02 reorganize file structure, added a howto
* 2016-04-04 update to burp 2.0.36
* 2016-03-14 add el5 branch for burp 1.x packaging
* 2016-03-09 add burp2 packaging
* 2016-03-09 add tito stuff inside git repo
* 2016-03-09 initialize git repo

## burp2 packaging status

At this time of writing, burp2 packaging is not provided by EPEL nor Fedora project.  
Here the status of building this software against various distributions.  

NB: el5 = RHEL5 and derivatives  (CentOS5, ScientificLinux 5, etc)

* XXX Group "Backup Server" is unknown (f22+)
* XXX COPR building for arch ARM is unusable, too much wait (2016-02)

* XXX el5: can't build burp2:
    * "Group:" has to be defined in each (sub)package
    * missing some `BuildRequires` packages:  
        https://copr-be.cloud.fedoraproject.org/results/yopito/burp2/epel-5-x86_64/00166348-burp2/mockchain.log.gz
        ```
Error: No Package found for uthash-devel
Error: No Package found for yajl-devel
        ```
    * `autoreconf` needs autoconf 2.61+, el5 has only 2.59.

    Workaround: use burp 1.x from the el5 branch of this repo.

* building/packaging is fine for el6, el7, fedora 22, 23, 24 and fedora-rawhide


## burp (1.x) packaging status

version: 1.4.40 (2016-03)

* EPEL channel provides burp 1.x packaging for el6 and el7, but NOT for el5.
* FedoraProject provides burp 1.x packaging for Fedora 22, Fedora 23, and Fedora-rawhide

* el5 (RHEL5, CentOS 5):
    * not provided by EPEL repository for burp 1.x (as this time of writing)
    * build is fine with the .spec file provided by the 'el5' branch of this repo.
    * need yajl-devel package too, that has to be built to (branch 'el5').
    * does not need uthash package, since uthash provided in burp 1.x source code.
        (that is nice since uthash is not packaged for el5, either in OS, update or EPEL yum channels)


## howto use these source packaging

Getting tired of `tito` stuff, switched back to a more conventional file structure like this: 

```
<pkg>/SPECS/ ......... contains the Specfile of package <pkg>
<pkg>/SOURCES/ ....... contains all needed source files
```

Usage: 

* build a (binary) package:  
    ```
cd <pkg>
mkdir -p RPMS BUILD SRPMS
rpmbuild --define="_topdir $(pwd)" -bb SPECS/<pkg>.spec
    ```

* build a source package into `<pkg>/SPRMS/` folder:  
    ```
cd <pkg>
mkdir -p SRPMS
rpmbuild --define="_topdir $(pwd)" -bs SPECS/<pkg>.spec
    ```

To request a build with COPR infrastructure, choose to generate from a SRPM file that you upload. 
