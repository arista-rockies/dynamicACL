#!/usr/bin/python3

"""
# Copyright (c) 2025 Arista Networks, Inc.
# Use of this source code is governed by the MIT license
# that can be found in the LICENSE file.
"""

import pyeapi, argparse, uuid
import dns.resolver

parser = argparse.ArgumentParser()
parser.add_argument('-hosts', required=True, nargs='+', help="dns hostnames to resolve.  multiple entries can be specified space separated")
parser.add_argument('-acl', default="DYNAMICACL", help="name of the acl to replace post resolution")
parser.add_argument('-recordType', default="a", help="a or aaaa")
parser.add_argument('-lineFormat', default='permit ip any host {}', help="a python format string to be used for each host line")
parser.add_argument('-preLines', nargs='+', help="any acl lines to include before dns resolves space delimted and wrapped in quotes")
parser.add_argument('-postLines', nargs='+', help="any acl lines to include after dns resolves space delimted and wrapped in quotes")

args = parser.parse_args()

hosts = []
if args.preLines:
    hosts.append("remark preLines")
    hosts.extend(args.preLines)

# do the dns resolve
for host in args.hosts:
    hosts.append(f"remark {host}")

    r = dns.resolver.Resolver(configure=True)
    try:
        answer = r.resolve(host, args.recordType)
    except dns.resolver.NXDOMAIN:
        continue
    except dns.resolver.NoAnswer:
        continue

    for rr in answer:
        hosts.append(args.lineFormat.format(rr))

if args.postLines:
    hosts.append("remark postLines")
    hosts.extend(args.postLines)

if len(hosts):
    # we have hosts now, let's go ahead and rewrite the acl
    family = "ip" if args.recordType == "a" else "ipv6"
    cmds = [
        f"configure session dynamicacl-{str(uuid.uuid4())}",
        f"no {family} access-list {args.acl}",
        f"{family} access-list {args.acl}"
    ]
    cmds.extend(hosts)
    cmds.append("commit")
    client = pyeapi.connect_to('localhost')

    result = client.run_commands(cmds, autoComplete=True, enable=True)
