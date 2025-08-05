%define _rpmfilename %%{NAME}-%%{VERSION}.%%{ARCH}.rpm

Name:           dynamicACL
Version:        1.0.2
Release:        1%{?dist}
Summary:        Dynamic configuration of ACLs based on FQDN
BuildArch:	noarch

License:        GPL
URL:            https://github.com/arista-rockies/dynamicACL
Source0:	https://github.com/arista-rockies/dynamicACL/archive/refs/tags/v%{version}.tar.gz

%description
Script to create a custom acl using FQDN objects. Schedule this command in eos with something like: `schedule tester interval 2 timeout 1 max-log-files 0 command bash sudo ip netns exec ns-MGMT /mnt/flash/dynamicACL.py -hosts www.google.com www.novell.com www.arista.com -recordType aaaa`

%prep
%setup

%install
mkdir -p %{buildroot}/mnt/flash
install -m 755 dynamicACL.py %{buildroot}/mnt/flash/dynamicACL.py

%files
/mnt/flash/dynamicACL.py

%changelog
* Tue Aug 05 2025 Patrick Felt <pfelt@arista.com>
- 
