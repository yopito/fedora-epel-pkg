
Packaging for Fedora/EPEL using Fedora COPR building system.

Related COPR space: https://copr.fedorainfracloud.org/coprs/yopito

Changelog: 
* 2016-03-14 add el5 branch for burp 1.x packaging
* 2016-03-09 add burp2 packaging
* 2016-03-09 add tito stuff inside git repo
* 2016-03-09 initialize git repo

## burp2 packaging

version: 2.0.34 (2016-03-09)

* XXX Group "Backup Server" is unknown (f22+)
* XXX arm building of COPR are unusable, too much wait (2016-06-10)

* XXX EPEL-5: does not build:  
    * "Group:" has to be defined in each (sub)package
    * missing some `BuildRequires` packages:  
        https://copr-be.cloud.fedoraproject.org/results/yopito/burp2/epel-5-x86_64/00166348-burp2/mockchain.log.gz
        ```
Error: No Package found for uthash-devel
Error: No Package found for yajl-devel
        ```
    * `autoreconf` needs autoconf 2.61+, el5 has only 2.59.
    workaround: build burp 1.x from the el5 branch of this repo.

* XXX fedora 24: build fails, related to f24 itself:  
    ```
Package libssh2-1.7.0-5.fc24.x86_64.rpm is not signed
    ```
    (see https://copr-be.cloud.fedoraproject.org/results/yopito/burp2/fedora-24-x86_64/00166348-burp2/root.log)

* fine for EPEL6, EPEL7, fedora 22, fedora 23 and fedora-rawhide
