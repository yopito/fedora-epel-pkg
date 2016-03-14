
Packaging for Fedora/EPEL using Fedora COPR building system.

Related COPR space: https://copr.fedorainfracloud.org/coprs/yopito

Changelog: 
* 2016-03-14 add el5 branch for burp 1.x packaging
* 2016-03-09 add burp2 packaging
* 2016-03-09 add tito stuff inside git repo
* 2016-03-09 initialize git repo

## burp2 packaging

version: 2.0.34 (2016-03-09)

At this time of writing, no burp2 packaging is provided by EPEL nor Fedora project.  
Here the status of building this software against various distributions.  

NB: el5 = RHEL5 and derivatives  (CentOS5, ScientificLinux 5, etc)

* XXX Group "Backup Server" is unknown (f22+)
* XXX arm building of COPR are unusable, too much wait (2016-06-10)

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

* XXX fedora 24: build fails, related to f24 itself:  
    ```
Package libssh2-1.7.0-5.fc24.x86_64.rpm is not signed
    ```
    (see https://copr-be.cloud.fedoraproject.org/results/yopito/burp2/fedora-24-x86_64/00166348-burp2/root.log)

* fine for el6, el7, fedora 22, fedora 23 and fedora-rawhide


## burp (1.x) packaging

version: 1.4.40 (2016-03)

* provided by EPEL and FedoraProject for el6, el7, Fedora 22, Fedora 23, and Fedora-rawhide

* el5:
    * not provided by EPEL repository (as this time of writing)
    * build is fine with the .spec file provided by the 'el5' branch of this repo.
    * need yajl-devel package too, that has to be built to (branch 'el5').
    * does not need uthash package, since uthash provided in burp 1.x source code.
        (that is good: uthash is not available as a package for el5, either in os, update or EPEL channels)


