# dynamicACL
create an acl using a specified list of fqdns

this script requires it run in a vrf with connectivity to the dns server configured on the switch.

## installation
copy to `flash:`

and install into eos:

```
copy flash:dynamicACL.......rpm extension:
extension dynamicACL.....rpm`
copy installed-extensions boot-extensions
```

## configuration
enable the management api

```
management api http-commands
   protocol unix-socket
   no shutdown
   !
   vrf MGMT
      no shutdown
```

for use in a vrf use the following syntax replacing `MGMT` with the desired vrf

`schedule dynamicACL interval 2 timeout 1 max-log-files 0 command bash sudo ip netns exec ns-MGMT /mnt/flash/dynamicACL.py -hosts www.google.com www.novell.com www.arista.com -recordType aaaa`

for use in the default vrf use the following syntax
`schedule dynamicACL interval 2 timeout 1 max-log-files 0 command bash sudo /mnt/flash/dynamicACL.py -hosts www.google.com www.novell.com www.arista.com -recordType aaaa`

