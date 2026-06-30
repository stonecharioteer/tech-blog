---
date: "2026-06-29T16:42:01+05:30"
draft: false
title: "Why Tailscale SSH Works When OpenSSH Doesn't"
description: "Why Tailscale SSH can log you in when OpenSSH would reject you: tailscaled, ACLs, root privileges, and Unix users."
tags:
  - "tailscale"
  - "ssh"
  - "wireguard"
  - "networking"
  - "homelab"
  - "security"
---

I was setting up a machine recently and noticed something odd.

OpenSSH password authentication was disabled. The user I was logging in as did
not have anything useful in `~/.ssh/authorized_keys`. I do not expose SSH on
this box to the internet either.

Regular SSH should have failed. This still worked:

```bash
tailscale ssh vinay@my-server
```

I got a shell as the local Unix user `vinay`.

That was the bit I wanted to understand. OpenSSH did not accept a password, and
it did not find a public key in `authorized_keys`. In this path, OpenSSH was not
the thing deciding whether I could log in. Tailscale was.

I have been using Tailscale more deliberately lately. I previously wrote about
[setting up a Tailscale exit node][tailscale-exit-node], where the question was
mostly: _how does traffic leave my machine and reach the internet through a home
gateway?_

This post is me working through Tailscale SSH. I started with the assumption
that it was mostly a convenience wrapper around SSH. It is not quite that.

The questions I had were:

- Is this still SSH?
- Is `sshd` involved?
- Where did my SSH keys go?
- What exactly does Tailscale authenticate?
- What does the Tailscale control plane know?
- What can DERP see?
- What role do local Linux users still play?
- What permission does `tailscaled` have that lets it start a shell as that
  Unix user?

## TLDR

Tailscale SSH still gives you an SSH session, but it is not an OpenSSH-server
login. The authentication decision moves from per-host SSH keys to Tailscale
identity and tailnet policy.

The path is:

1. Your devices are already connected through Tailscale's WireGuard mesh.
1. The destination machine has Tailscale SSH enabled with `tailscale up --ssh`.
1. The tailnet policy contains `ssh` rules saying which Tailscale users, groups,
   or tagged devices can log in to which machines as which local Unix users.
1. When you connect to port 22 over the Tailscale address, `tailscaled` handles
   the SSH connection on the tailnet interface.
1. Tailscale checks the source device/user identity against the central policy.
1. If allowed, the privileged `tailscaled` service starts a session as the
   requested local Unix user.

The comparison I keep in my head is:

> OpenSSH usually asks: "Does this client have a key accepted by this host?"
>
> Tailscale SSH asks: "Does this tailnet identity, from this device, have policy
> permission to become this local user on this node?"

The local Unix account still matters. Tailscale does not bypass Linux
permissions. If I log in as `vinay`, I get `vinay`'s files, groups, shell, and
`sudo` rules. Tailscale can create the session because `tailscaled` runs as a
privileged system service on the destination machine.

## Normal SSH first

Before Tailscale enters the picture, this is the usual OpenSSH flow:

{{< diagram type="flow" orientation="horizontal" caption="Classic OpenSSH: the client talks straight to sshd on TCP 22." >}}
[
  {"label": "laptop", "sub": "SSH client", "detail": "Opens a TCP connection to port 22 and speaks the SSH protocol."},
  {"label": "server : sshd", "via": "TCP / 22", "sub": "listens on :22", "detail": "OpenSSH answers, proves its host key, then checks your key or password against authorized_keys / PAM before starting a session."}
]
{{< /diagram >}}

A simplified version of the flow:

1. The client connects to the server on TCP port 22.
1. Client and server negotiate encryption for the SSH transport.
1. The server proves its identity using a host key.
1. The client authenticates as a local username, usually with a private key.
1. `sshd` checks files like `~/.ssh/authorized_keys` for that local user.
1. If accepted, `sshd` creates a login session as that Unix user.

The protocol is not the problem. The annoying part is access distribution:

- every server needs the right public keys;
- removing someone's access means removing keys everywhere;
- host keys need to be trusted or managed;
- if you have many machines, access review becomes annoying.

This is not an argument against OpenSSH. I use it everywhere. The point is that
key distribution and access policy become _your_ distributed system.

OpenSSH certificates solve a related key-distribution problem, but they still
use `sshd` as the login broker. Tailscale SSH moves the authorization decision
into tailnet policy.

## What Tailscale changes

Tailscale already gives every device in your tailnet a cryptographic identity and
a stable private address. My laptop and my server do not need a public inbound
port open to find each other. They can establish a WireGuard-encrypted path using
Tailscale's control plane for coordination, NAT traversal, and policy
information.

Tailscale SSH builds on that. Instead of asking "does this host have this public
key for this local user?", it asks "does this tailnet identity have permission
to become this local user on this host?"

A typical setup has two parts.

On the server:

```bash
tailscale up --ssh
```

In the tailnet policy:

```json
{
  "ssh": [
    {
      "action": "accept",
      "src": ["autogroup:member"],
      "dst": ["tag:server"],
      "users": ["vinay"]
    }
  ]
}
```

Read that as:

> Members of this tailnet may SSH to devices tagged `server`, but only as the
> local Unix user `vinay`.

In practice, I would usually make this stricter: specific users or groups,
specific tags, specific destination machines, and specific local accounts.

## The packet path

When I SSH to a Tailscale machine, the outer network path looks like the normal
Tailscale path.

{{< diagram type="flow" orientation="vertical" caption="The SSH bytes ride inside WireGuard the whole way." >}}
[
  {"label": "laptop", "sub": "SSH client", "detail": "Produces the SSH protocol bytes for the session."},
  {"label": "WireGuard tunnel", "via": "SSH bytes", "sub": "encrypted Tailscale transport", "badges": ["direct UDP", "DERP relay"], "detail": "Tailscale wraps the SSH bytes in WireGuard. It prefers a direct UDP path via NAT traversal, and falls back to a DERP relay only when that fails. DERP forwards ciphertext; it never sees the SSH session."},
  {"label": "server : tailscaled", "via": "encrypted path", "sub": "answers :22 on the tailnet", "detail": "tailscaled receives the connection on the Tailscale interface and terminates the SSH session itself."},
  {"label": "local login session", "via": "authorized", "sub": "shell as the Unix user", "detail": "Once policy allows it, a session starts as the requested local Unix user."}
]
{{< /diagram >}}

The cafe WiFi, airport WiFi, or hotel network sees an encrypted Tailscale flow.
If the connection goes through DERP, the DERP relay forwards encrypted packets;
it does not get to read the SSH session.

There are two layers to keep distinct:

- **Tailscale/WireGuard layer**: gets packets between the two tailnet devices.
- **SSH layer**: creates an interactive shell/session on the destination.

So this is not "SSH without encryption" just because WireGuard already encrypts
traffic. The SSH protocol is still involved. The important difference is the
_authentication and authorization source of truth_.

{{< info title="Control Plane vs Data Plane" >}}
The Tailscale control plane coordinates identity, keys, peer discovery, and
policy. The data plane carries your actual traffic between devices, directly when
possible and through DERP when necessary. Tailscale SSH policy decisions depend
on the control plane, but the shell bytes are carried over the encrypted data
plane.
{{< /info >}}

## Who answers port 22?

This is the part I had wrong at first.

With normal SSH, the process answering port 22 is usually `sshd`. With Tailscale
SSH enabled, `tailscaled` answers SSH connections that arrive over the Tailscale
interface. Same port number, different daemon, different authentication path.

Tailscale SSH does not need the OpenSSH server to accept the login.
`sshd_config`, `authorized_keys`, OpenSSH `AllowUsers`, OpenSSH `DenyUsers`, and
password-login settings are part of the OpenSSH decision path. A Tailscale SSH
connection does not ask `sshd` whether the key is allowed. It asks Tailscale
policy whether this tailnet identity may become the requested local user.

The distinction matters:

{{< diagram type="compare" caption="Same port number, different listener depending on where the connection arrives." >}}
{
  "columns": [
    {"title": "From outside the tailnet", "accent": "red", "steps": [{"label": "TCP / 22"}, {"label": "sshd?", "detail": "Reachable only if your firewall or router forwards the port."}]},
    {"title": "From the tailnet", "accent": "green", "steps": [{"label": "TCP / 22"}, {"label": "tailscaled", "detail": "Answers SSH on the Tailscale interface when Tailscale SSH is enabled."}]}
  ]
}
{{< /diagram >}}

So I can have a machine where OpenSSH is not accepting a user, or regular
key-based SSH is unusable, but Tailscale SSH still works from inside the tailnet.

The destination can be behind NAT, on a home connection, with no port forwarding,
and still be reachable from my laptop.

{{< note title="Same port, different address" >}}
This is the part that finally made the socket model click for me. A port is not
just a number floating around on the machine. A listener is tied to a local
address and a port.

So `100.x.y.z:22` and `192.168.1.50:22` are different sockets. Tailscale SSH can
answer port 22 for connections arriving over the tailnet address while OpenSSH
answers port 22 somewhere else.

<!-- TODO: An interactive diagram would fit here: same host, multiple local addresses, same port number, different listener/process. -->

The same idea is not limited to SSH:

```text
100.x.y.z:80       → internal tailnet dashboard
192.168.1.50:80    → LAN-only service
127.0.0.1:80       → local development server
```

All three are "port 80", but they are not the same endpoint. The address matters
as much as the port.

This also reminded me of how I use Nginx at home, though the mechanism is a bit
different. I run Unbound for DNS and use `.home.arpa` names for homelab services.
Several names can point at the same machine:

```text
service1.home.arpa → 192.168.1.50
service2.home.arpa → 192.168.1.50
```

Both requests arrive at the same machine on port 80. Nginx can still send them
to different upstream services because HTTP carries the requested hostname in the
`Host` header:

```text
GET / HTTP/1.1
Host: service1.home.arpa
```

So the exact comparison is not "different IP, same port" anymore. It is "same
IP, same port, different HTTP host". But it rhymes with the same lesson: port 80
alone does not tell the whole story. The OS first routes traffic to a socket
based on address and port; then a protocol-aware service like Nginx can make a
second decision based on HTTP metadata and reverse proxy internally.

The caveat is `0.0.0.0`. A service bound to `0.0.0.0:80` asks the OS to listen
on all IPv4 interfaces, so it may prevent another process from binding a more
specific address like `192.168.1.50:80`. But the basic shape is still: listeners
are about address plus port, not port alone.
{{< /note >}}

## How can Tailscale become a Unix user?

Tailscale is not mapping my Tailscale account into a Unix user in some global
directory. It is using a privileged local daemon to create a normal local
session.

On Linux, `tailscaled` usually runs as `root` under systemd:

```bash
systemctl status tailscaled
```

It needs elevated privileges for normal Tailscale networking work too: creating
or managing the `tailscale0` interface, installing routes, configuring DNS, and
handling traffic for the tailnet. Tailscale SSH uses that same privileged daemon
as the login broker.

Once the ACL says a login is allowed, `tailscaled` can look up the requested
local user through the operating system's user database: `/etc/passwd`, NSS,
LDAP, or whatever the machine is configured to use.

Conceptually, the privileged process can then do the standard Unix identity
switch:

{{< diagram type="flow" orientation="vertical" caption="The privileged drop-into-a-user dance." >}}
[
  {"label": "lookup local user \"vinay\"", "detail": "Resolve the requested account through /etc/passwd, NSS, LDAP, or whatever the host uses."},
  {"label": "set supplementary groups", "detail": "Initialize vinay's group memberships."},
  {"label": "setgid(primary group)", "detail": "Drop the process group identity."},
  {"label": "setuid(UID)", "detail": "Drop the process user identity; after this the process is no longer root."},
  {"label": "exec shell / session", "detail": "Replace the process image with vinay's shell/session."}
]
{{< /diagram >}}

So if the machine has a user like this:

```text
vinay:x:1000:1000:Vinay:/home/vinay:/bin/bash
```

then the resulting shell is a process with `vinay`'s UID, GID, supplementary
groups, home directory, and shell. The shell is not running as my Tailscale
account. It is not running as some special cloud user. It is running as the local
Unix user `vinay`.

The model I ended up with:

{{< diagram type="flow" orientation="vertical" animate="false" caption="Four responsibilities, four layers." >}}
[
  {"label": "Tailscale identity", "accent": "blue", "sub": "who I am in the tailnet", "detail": "An SSO-backed tailnet user, tied to my devices."},
  {"label": "Tailscale SSH ACL", "accent": "blue", "sub": "which local user I may become", "detail": "Central policy maps identities to destination machines and local accounts."},
  {"label": "tailscaled (root)", "accent": "orange", "sub": "creates the local session", "detail": "The privileged daemon performs the Unix identity switch."},
  {"label": "Linux permissions", "accent": "green", "sub": "what the session can do", "detail": "Groups, sudo rules, and filesystem ACLs are still the OS boundary."}
]
{{< /diagram >}}

There is a real security trade here. Enabling `tailscale up --ssh` is not a
harmless UX toggle. It makes `tailscaled` a login authority for that machine.

That means I trust three things:

1. the `tailscaled` daemon on the destination machine;
1. the tailnet SSH ACLs that decide who can log in;
1. the tailnet admins who can change those ACLs.

The power moved. It moved from per-host OpenSSH config to a privileged local
Tailscale daemon plus centralized tailnet policy. That may be exactly what I
want, but it is not nothing.

## The OpenSSH way to get multiple policies

There is another way to think about this from the OpenSSH side: I could run more
than one `sshd`.

This was a small duh moment for me. I have run multiple instances of services on
a dev box before. Postgres on different ports, for example. But I had never
really thought of SSH that way. I mostly treated `sshd` as "the SSH service on
the machine", singular.

But `sshd` is just a daemon listening on a socket. A server can run multiple
OpenSSH instances as long as they do not bind the same IP/port pair. For
example:

```text
0.0.0.0:22       → normal sshd
100.x.y.z:2222   → tailnet-only sshd with a different config
127.0.0.1:2223   → local/debug sshd
```

Each one can have its own config file:

```bash
/usr/sbin/sshd -f /etc/ssh/sshd_config
/usr/sbin/sshd -f /etc/ssh/sshd_config_tailnet
```

The reason to do this is to keep different SSH policies for different network
paths.

For example, the regular daemon can stay restrictive, while a second OpenSSH
daemon listens only on the Tailscale IP and a non-default port:

```sshconfig
# /etc/ssh/sshd_config_tailnet
Port 2222
ListenAddress 100.x.y.z

PasswordAuthentication no
PermitRootLogin no
AllowUsers deploy
AuthorizedKeysFile .ssh/authorized_keys
```

This is still OpenSSH. The login decision is made by `sshd`, using
`sshd_config`, `authorized_keys`, PAM, and the usual OpenSSH machinery. Tailscale
is only providing the network path.

The comparison looks like this:

```text
Normal OpenSSH:
client → sshd → sshd_config / authorized_keys / PAM → Unix session

Second OpenSSH instance:
client → another sshd → another sshd_config / authorized_keys / PAM → Unix session

Tailscale SSH:
client → tailscaled → Tailscale SSH ACLs → Unix session
```

That distinction matters for automation.

## What happened to `authorized_keys`?

With traditional SSH, access usually lives on the destination host:

```text
/home/vinay/.ssh/authorized_keys
```

With Tailscale SSH, access lives in the tailnet policy:

```json
{
  "ssh": [
    {
      "action": "accept",
      "src": ["vinay@example.com"],
      "dst": ["my-server"],
      "users": ["vinay"]
    }
  ]
}
```

That changes the operational model.

If I want to revoke access, I change policy or remove the device/user from the
tailnet. I don't need to remember every machine that might contain an old public
key.

The practical shift is that SSH authorization becomes centralized and identity
aware.

This explains the case I started with: regular SSH can be disabled for a user
while Tailscale SSH still works.

For example, suppose `vinay` has no public key in
`/home/vinay/.ssh/authorized_keys`, or `sshd_config` contains rules that prevent
`vinay` from logging in through OpenSSH. A normal `ssh vinay@server` path that
lands in `sshd` fails. A Tailscale SSH path can still succeed if the Tailscale
SSH policy says my tailnet identity is allowed to log in as `vinay`.

The two paths are different:

{{< diagram type="compare" caption="Two login paths, two sources of truth." >}}
{
  "columns": [
    {"title": "OpenSSH login decision", "accent": "slate", "steps": [{"label": "client key / password"}, {"label": "sshd"}, {"label": "sshd_config + authorized_keys / PAM", "detail": "The destination host decides using local OpenSSH configuration."}]},
    {"title": "Tailscale SSH login decision", "accent": "blue", "steps": [{"label": "tailnet identity + device"}, {"label": "tailscaled"}, {"label": "tailnet SSH ACLs", "detail": "Tailnet policy decides which identity may become which local user."}]}
  ]
}
{{< /diagram >}}

`authorized_keys` is not the source of truth for Tailscale SSH. The ACL is.

The local user still has to exist on the destination machine. If policy says I
can log in as `vinay`, then `vinay` needs to be a real local account, with a
usable shell, home directory, groups, and permissions. Tailscale can authorize
becoming that user; it does not invent the Unix user or override what that user
can do once the session exists.

Tailscale decides whether I may become `vinay`; Linux decides what `vinay` can do
after that.

## `accept` vs `check`

Tailscale SSH policies can require an additional check before allowing access.
This is useful for sensitive machines or high-privilege accounts.

Conceptually:

```json
{
  "ssh": [
    {
      "action": "check",
      "src": ["autogroup:member"],
      "dst": ["tag:prod"],
      "users": ["root"]
    }
  ]
}
```

`accept` means policy allows the connection.

`check` means policy allows it only after a recent interactive verification. That
might mean reauthenticating through the identity provider before the session is
allowed.

I like this distinction because it separates two questions:

1. _Is this identity allowed in principle?_
1. _Do we want a fresh human confirmation for this sensitive action?_

For a personal homelab, this may feel like overkill. For a production box or a
root login, it is a sane extra guardrail.

## Trust boundaries

The trust question matters more than the syntax: who am I trusting, and for
what?

### The local network

The local network can see that my machine is talking to Tailscale peers or DERP,
and it can see timing and volume. It should not be able to read the session
contents.

### DERP

DERP can relay encrypted packets if a direct connection is not possible. DERP is
in the transport path but not supposed to be in the plaintext path. It forwards
ciphertext.

### Tailscale control plane

The control plane is trusted for identity, coordination, and policy distribution.
It can tell devices who is allowed to talk to whom, distribute network maps, and
enforce the administrative model of the tailnet.

It is not a server sitting in the middle reading my shell session.

### Tailnet admins

Tailnet admins are powerful. They can change ACLs and SSH rules. If an admin can
write policy that grants access to machines, that is a real security boundary.
For a personal tailnet, I am the admin. In a company, this becomes an
organizational trust question.

### The destination machine

Once I log in, the destination machine is the destination machine. Tailscale does
not protect me from a compromised host. If I SSH into a malicious or compromised
box, my terminal session is on that box.

## How I debug the model

These are the commands I use to keep the layers straight.

Check whether the peer is reachable through Tailscale:

```bash
tailscale status
tailscale ping <host>
```

Check the Tailscale IP and MagicDNS name:

```bash
tailscale ip -4
```

Try SSH explicitly:

```bash
tailscale ssh vinay@<host>
# or, depending on setup:
ssh vinay@<host>
```

On the destination, confirm Tailscale SSH is enabled:

```bash
tailscale status
```

And remember the three separate gates:

1. Can the devices reach each other on the tailnet?
1. Does SSH policy allow this source identity to access this destination?
1. Does the requested local Unix user exist and have the expected permissions?

Most of my confusion came from mixing these layers together.

## Ansible, GitHub Actions, and why I still used OpenSSH

Tailscale SSH is pleasant when I am the one typing the command. Deployment
tooling is a different story. A lot of it assumes normal OpenSSH semantics.

Ansible is where I ran into this. Its default shape is:

```text
ansible controller → ssh binary → remote sshd → run Python/modules remotely
```

It knows how to pass SSH arguments, use an inventory hostname, select a private
key, set a port, become another user, copy files, and reuse connections. That
all fits OpenSSH very naturally.

In one deployment, I had trouble making Ansible use Tailscale SSH cleanly from a
GitHub workflow. The target machine was on my tailnet, but the deployment path
was automation, not me typing `tailscale ssh`. I did not want the workflow to
need an exit node just to reach SSH, and I did not want to expose SSH publicly.

The compromise was simple: run OpenSSH on the tailnet, on a different port, and
point the workflow at that.

```text
GitHub workflow runner
  → joins tailnet / can reach tailnet
  → ssh deploy@100.x.y.z -p 2222
  → tailnet-only sshd
  → Ansible runs normally
```

Then the Ansible inventory stays ordinary:

```ini
[servers]
my-server ansible_host=100.x.y.z ansible_port=2222 ansible_user=deploy
```

or in YAML:

```yaml
all:
  hosts:
    my-server:
      ansible_host: 100.x.y.z
      ansible_port: 2222
      ansible_user: deploy
```

This is less elegant than using Tailscale SSH policy everywhere, but it fits the
tooling. Tailscale provides the private network path. OpenSSH provides the
login surface Ansible already understands. Ansible does not need to know anything
special.

The trade-off is that I now have two SSH-like paths to reason about:

- `tailscale ssh vinay@my-server` for human access controlled by Tailscale SSH
  ACLs;
- `ssh -p 2222 deploy@100.x.y.z` for automation controlled by OpenSSH keys and
  the tailnet-only `sshd_config`.

I am fine with that as long as I keep the boundary clear. Tailscale SSH and
OpenSSH-over-Tailscale are not the same thing. One uses `tailscaled` to authorize
and create the login. The other uses `sshd`; Tailscale only supplies the private
route.

## Why this feels nicer than needing an exit node for SSH

The practical benefit for my setup is not "this saves me from public SSH". I do
not expose SSH publicly anyway.

The benefit is that I do not need to route all my traffic through a home exit
node just to administer one machine.

Without Tailscale SSH, one possible remote-admin model is:

```text
laptop → Tailscale exit node / home network path → private server → OpenSSH
```

That works, but it makes SSH access depend on the broader network path being set
up correctly. I need the right routing, possibly LAN access through the exit
node, and then normal SSH authentication on the destination.

With Tailscale SSH, the model is narrower:

```text
laptop → Tailscale mesh → tailscaled on target machine → local Unix session
```

The parts I like are:

- no exit node required just for SSH;
- no router port forwarding;
- no per-host `authorized_keys` drift;
- access is tied to SSO/tailnet identity;
- revocation is centralized;
- policies can be reviewed in one place;
- sensitive logins can require re-checks;
- the network path still benefits from Tailscale's NAT traversal and DERP
  fallback.

For my homelab, that is the win. I can reach the one machine I care about over
the tailnet without turning my whole connection into a full-tunnel VPN through
home.

## The model I am keeping

Tailscale SSH is not "a different terminal" and it is not "SSH replaced by a
VPN".

I now think of it as:

> SSH session semantics, Tailscale network reachability, and centralized
> identity-based authorization.

The SSH server decision moves closer to the tailnet identity layer. The network
path is the same private mesh I already use for other Tailscale services. The
local Unix account remains the final operating-system boundary.

The login answers five separate questions:

{{< diagram type="layers" title="The five questions a login answers" caption="Each question is answered by a different layer." >}}
{
  "layers": [
    {"q": "Who are you?", "a": "Tailscale identity", "accent": "blue", "detail": "Your SSO-backed tailnet user."},
    {"q": "Where are you from?", "a": "Tailscale device identity", "accent": "blue", "detail": "The device you are connecting from."},
    {"q": "May you connect?", "a": "Tailnet SSH policy", "accent": "orange", "detail": "The ACL rules decide accept, check, or deny."},
    {"q": "Who do you become?", "a": "Local Unix username", "accent": "green", "detail": "A real account that must exist on the destination host."},
    {"q": "What can you do?", "a": "Linux permissions", "accent": "green", "detail": "Groups, sudo, and filesystem ACLs."}
  ]
}
{{< /diagram >}}

That decomposition is the main thing I wanted from this post. Once I can name
those layers, Tailscale SSH stops looking like a special exception and starts
looking like a composition of WireGuard, identity, policy, a privileged daemon,
and ordinary Unix users.

## References

- [Tailscale SSH documentation][ts-ssh]
- [Tailscale ACL syntax][ts-acls]
- [Tailscale userspace networking][ts-userspace]
- [How Tailscale works][ts-how]
- [My previous post on Tailscale exit nodes][tailscale-exit-node]

[tailscale-exit-node]: {{< ref "/posts/2026/tailscale-exit-nodes" >}}
[ts-ssh]: https://tailscale.com/kb/1193/tailscale-ssh
[ts-acls]: https://tailscale.com/kb/1018/acls
[ts-userspace]: https://tailscale.com/kb/1112/userspace-networking
[ts-how]: https://tailscale.com/blog/how-tailscale-works

{{< merrilin title="A small plug" >}}
If you liked this post, you might also like [Merrilin](https://merrilin.ai), the
reading app I'm building. It has spoiler-aware AI companions, series-aware
questions, live sync, themes, quote sharing, and e-ink support.

I've written more about it in [the launch post](/posts/2026/merrilin/).
{{< /merrilin >}}
