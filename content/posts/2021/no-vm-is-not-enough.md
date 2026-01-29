---
date: 2021-09-20T10:00:00+05:30
draft: false
title: "No, A Virtual Machine Is Not Enough: Why Developers Need Native Linux"
description:
  "An exploration of why corporate Windows/Mac development environments with VM
  workarounds fail to provide the productivity and experience that native Linux
  offers to power users."
tags:
  - "productivity"
  - "linux"
  - "corporate"
  - "development-tools"
  - "rant"
---

I use a MacBook Pro 2018 for work. I work in a company which, like many
corporates, uses JAMF to manage their Macs. The developer experience is, I have
no other words for it, abysmal.

The alternative for Macs at my workplace is Windows, and that's a whole other
bag of nope. Corporate Windows machines at my previous companies have had
extreme rules placed on the workstations. They give you Dell Latitude or XPS
machines - they're good machines otherwise - but they pile on the bloatware, and
more importantly, they don't let you run anything.

I'm not talking about running Wireshark by the way. Of course, if I run that on
a workstation, I've been told that my manager will get a very salacious email.

You cannot run anything on these laptops.

I'm going to break this down into 2 sections: Windows and Macs.

## Disclaimer

I am not disparaging anyone who is satisfied using a Windows or a Mac machine
for development. If you're satisfied with the experience, and it works for you,
that is very good. However, I've heard far too many tell me that since it works
for many developers, it should suffice for everyone; or that enterprises cannot
afford to maintain Linux builds of their tools.

That's my beef with the problem. A Windows or a Mac is not enough for _my_
purposes. I am a power user, who has been burnt by "accepted, enterprise
solutions" way too many times, and I do not find them acceptable.

## Windows Experience

### Custom Tooling and Package Management

Enterprise Windows installations controlled by the IT team usually tell you that
you should not, and _cannot_ run software you download from the internet on the
laptop. The entire experience is geared towards Managers and people who either
use MS Excel or MS PowerPoint. I have spent my fair share of time on those tools
and I would sacrifice them in a heartbeat to have my development tools work as
they should.

In some companies, IT tries to be cool and says you _can_ run foreign
executables, as long as you run them from a specific folder. I've seen this
applied to either `C:\TOOLS` (heh) or `C:\Software`. This is theoretically a
good idea. But now I'd like you to think back to the days when you used Windows
and remember how you install _most_ of your applications.

They don't go there. _Sure_, you _can_ install applications wherever you want,
but the defaults are _defaults_ for a very strong reason. Not all applications
allow this sort of portability in Windows. You _have_ places like
[portableapps](https://portableapps.com) which give you portable packages of
most common tools, but if you read between the lines, you'll realize that this
portability is _inapplicable_ to a lot of libraries.

The thing with using Windows is that sometimes, your tools depend on system
executables, and, _surprise, surprise_, you can't execute other executables
which are installed elsewhere through forks of the process you're executing from
your special, IT-specified folder, since they _will not run_. This becomes a
problem for the following reasons:

**Python**: You cannot make meaningful virtual environments anymore. You _have_
to make _všesé_ your `venv` folders in a central location, or fall back to using
`conda`, which is yet another problem, since `conda` stores all environments in
one central location.

The same problem exists with `nodejs` and `golang`. _Hell_, this problem is also
persistent with `rust`!

The widely accepted way of letting your devs run arbitrary tools on Windows is
dangerously flawed. If I were to get into that scenario (again), I would spend
more hours pulling my hair out rather than write code.

{{< warning title="Software Installation Reality" >}} Most software isn't
conducive to installations running willy-nilly on a Windows machine, especially
when IT restrictions are in play. {{< /warning >}}

Note that while I _am_ aware of `chocolatey`, I have not been able to use it
since enterprise machines also have the problem of needing to configure a proxy.
These proxies don't give themselves freely to downloading from public
registries, such as those used by `chocolatey`.

### Environment Variables

To add to this problem is Windows' _sweet, sweet Environment Variable_ problem.
To add environment variables to Windows, you _need_ to use the GUI and set them
there. The dialog not only has a cap of 256 characters (unless you choose to
daisy chain them with `%VAR%`), it also has a huge problem with usability. Not
to mention, IT blocks the setting of environment variables most of the time. If
they don't do it right now, they _will_, sometime.

Why is this a problem? Can't I use a `bat` file with a bunch of `SET VAR=10`
lines?

_Sure_. I _can_ do that. But it's not straightforward to `Import-Module` on
starting a PowerShell instance, for example. Besides, there's another problem.

### PowerShell vs. The World

Your servers are running Linux. You're already dealing with `bash` foo. Do you
want to keep up to date on `PowerShell`?

Seriously. I, as do many other developers who care about their custom configs,
store my `dotfiles` in GitHub. The first thing I do when I get a new laptop is
run a few `ansible` scripts, and configure my machine to work the way I want. I
need my terminal to run flawlessly, with the fonts I prefer, and with the
predefined configurations for everything from `neovim` to `pgcli` to `VS Code`.

And why is this important?

It is _crippling_ to use a machine which feels foreign to you. You neither have
the energy to recustomize a machine, nor the facility to do so on a platform
like Windows.

### Services and Background Processes

I have several scripts I run as a service on my personal laptop. One of them is
a Discord bot, another is an ngrok tunnel, and there are a few others that I
run. On my work laptop, I currently don't run any scripts. I _do_ have a few
private CLIs that I use for things like toggling my proxies and changing the
WiFi, but beyond that, I haven't written anything.

At a place where that's possible, I'd love to be able to write tools that make
my life easier. I could update and create Jira tickets easily, and autogenerate
my `TODO` file based on them every week.

I _could_ do these things, but with Windows, adding a new service, even if it is
at the _user_ level, is an atrocious process.

### Process Control

At this point, I'm just listing the differences between Windows and Linux. I
cannot stress how important this is to me. In Linux, the shell process is a
_first class citizen_. It isn't a hacked-together afterthought like PowerShell
or the command prompt. This gives me extended super-powers. I can kill a
process, figure out which are the forks and how much RAM each is using. I can
use `lsof` to list processes using a file, and I can also use a true terminal
emulator.

## MacBook Pro Experience

### Gatekeeper: No Apple, That's a Tool I Need

macOS has this wonderful feature called Gatekeeper that prevents you from
running "unverified" applications. While this is great for security, it becomes
a nightmare when you need to run development tools that haven't gone through
Apple's notarization process.

Want to use that new Rust CLI tool you compiled? Sorry, Apple doesn't trust it.
Downloaded a beta version of a development tool? Nope. The workarounds exist,
but they're cumbersome and break the flow of development.

### Docker on Mac: A Study in Frustration

Docker on Mac is... special. It runs in a VM (because macOS doesn't have native
container support), which means:

- Performance is significantly worse than native Linux
- File system mounting is slow and problematic
- Memory and CPU usage is higher
- Network behavior is different from production Linux environments

When your entire development workflow depends on containers, this becomes a
daily source of frustration.

### USB-C: The Dongle Life

Let's talk about hardware for a moment. USB-C is great in theory, but when you
need to connect:

- External monitors
- Your custom mechanical keyboard
- A mouse
- An external SSD
- A debugger or development board

You're suddenly living in dongle hell. And guess what? Corporate IT doesn't
always provide the dongles you need, and good luck getting approval to buy the
specific ones that work well.

### Bash Version Archaeological Dig

```bash
$ bash --version
GNU bash, version 3.2.57(1)-release (x86_64-apple-darwin19)
```

macOS ships with Bash 3.2 from 2007. Bash 4.0 was released in 2009. We're
missing over a decade of improvements because of licensing issues. Sure, you can
install a newer version via Homebrew, but then you have to update all your
scripts to use the non-default shell path.

### Services and System Restrictions

macOS has gotten increasingly locked down over the years:

- **Minikube issues**: Local Kubernetes development becomes problematic when you
  can't override localhost firewall rules
- **System integrity**: Can't modify system files even with sudo
- **Keychain complexity**: Certificate and credential management is opaque
- **Service management**: launchd is powerful but complex compared to systemd

## The Common "Solutions" and Why They Don't Work

### "Why Not Use Cygwin or MinGW?"

Ah yes. The time-tested solution(s).

No. Both Cygwin and MinGW will try to get executables and store them in a _faux_
HOME folder. This will _not_ work, because IT specifies that only one specific
folder will work.

Atop of this, not everything that I use will work on both those platforms. At
times, I compile tools that I've found, either written in Golang or in Rust, and
these won't have Windows support sometimes. If you ask me to abandon those
tools, all I have to say is that I am yet to find alternatives for such tools on
Windows.

And more importantly, _why should I?_ I use them all the time on a Linux
machine. Why should I be denied them here?

### "Why Not Use a Virtual Machine?"

I love this reply. I get it _all_ the time. Even from friends who are good
coders.

The problems with VMs are numerous:

#### Performance Overhead

- VMs consume significant RAM and CPU
- I/O performance is degraded
- GPU acceleration is limited or unavailable
- Battery life suffers on laptops

#### Networking Complexity

- VPN conflicts with VM networking
- Port forwarding becomes complex
- Corporate network access may be restricted from VMs
- SSH keys and certificates need to be managed separately

#### Multi-Monitor Hell

- VM display scaling issues
- Window management becomes cumbersome
- Clipboard sharing is unreliable
- Full-screen applications don't work well across monitors

#### File System Integration

- Shared folders are slow
- File permissions get mangled
- No native file indexing/search
- Backup solutions don't work properly

### "Use Docker and Run Multiple Containers"

That is a good answer. In fact, this would work, _if_ the executables _and_ the
firewall weren't blocking everything in red tape from here to Timbuktu.

I'm serious. Docker will not work because of several reasons:

- You won't have a properly configured hypervisor on your machine, because IT
  will say "Why do you need a VM?"
- Or you will not get it working because of how convoluted your administrator
  access protocols are
- Corporate proxies interfere with image pulling
- Security scanning tools flag container usage

### "Use WSL and the Windows Terminal"

WSL is Microsoft's best attempt at solving this problem, but it still falls
short:

- **WSL 1**: Not a real Linux kernel, lots of compatibility issues
- **WSL 2**: Runs in a VM (back to VM problems)
- **File system performance**: Cross-boundary file access is slow
- **Network limitations**: Port binding and networking can be problematic
- **GPU access**: Limited or non-existent
- **System service integration**: systemd support is recent and limited

The Windows Terminal is indeed nice, but the terminal is just the interface -
the underlying system limitations remain.

### "Use a Cloud Development Environment"

Cloud-based development environments are becoming popular, but they have their
own issues:

#### Network Dependency

- VPN instability ruins the experience
- Latency affects productivity
- Offline work becomes impossible
- Video calls + remote development = bandwidth competition

#### Limited Hardware Access

- Can't debug hardware devices
- USB device access is impossible
- Custom input devices don't work
- Specialized development boards are inaccessible

#### File Access Limitations

- Can't easily search/access local files
- Collaboration with local tools is difficult
- Version control integration is complex
- Backup and sync become complicated

## What I Actually Want

When I interview, one of my primary questions, beyond the nature of work and my
teammates, is the laptop I will be given to work on, the OS that I will be
using, and the level of permissions I will have on this machine.

I do not compromise on this. Give me a machine running Linux, preferably Ubuntu,
Debian, or Fedora. Bonus points if I can bring my own device, and use my own
choice of distro. I will be impressed if you have your own distro that you
locally maintain, with software registries and all.

### My Ideal Setup

- **Native Linux**: Ubuntu 22.04 LTS or Fedora latest
- **Hardware**: High-performance laptop with good Linux driver support
- **Permissions**: Sudo access for development needs
- **Network**: Reasonable proxy configuration that doesn't break package
  managers
- **Security**: Sensible security policies that don't interfere with development

### Why This Matters

1. **Tool Ecosystem**: The best development tools are built for Linux first
2. **Performance**: Native performance without virtualization overhead
3. **Consistency**: Development environment matches production environment
4. **Customization**: Full control over the development environment
5. **Hardware Access**: Direct access to hardware for debugging and development

## "We're a Corporate, We Cannot Give You a Linux Machine"

This is the response I often get, and it's simply not true:

### Enterprise Linux Solutions Exist

- **Red Hat Enterprise Linux**: Full corporate support and compliance
- **SUSE Linux Enterprise**: Another enterprise-grade option
- **Ubuntu Pro**: Canonical's enterprise offering
- **CentOS Stream**: Community enterprise Linux (though being phased out)

### Security and Management

- **LDAP Integration**: Enterprise authentication works fine on Linux
- **VPN Clients**: All major VPN solutions have Linux clients
- **Monitoring**: Corporate monitoring tools exist for Linux
- **Compliance**: Linux can meet the same compliance requirements

### The Real Solution

Give developers what they need to be productive. The cost of developer
productivity loss far exceeds the cost of supporting an additional platform.
Happy, productive developers write better code, solve problems faster, and stick
around longer.

## Conclusion

The fundamental issue isn't that Windows or macOS are bad operating systems -
they're not. The issue is that for power users who need deep system integration,
fine-grained control, and a development environment that matches production,
these platforms with their corporate restrictions create more friction than
productivity.

Virtual machines, containers, and remote development environments are band-aids
on a deeper problem. They add complexity, reduce performance, and create
additional failure points in the development workflow.

{{< quote title="Developer Experience Matters" >}} The tools we use shape the
work we create. When we're fighting our development environment, we're not
building great software. {{< /quote >}}

Companies that recognize this and provide Linux workstations to developers who
request them see benefits in:

- Higher developer satisfaction
- Increased productivity
- Better retention rates
- More innovative solutions

It's not about being elitist or demanding. It's about recognizing that different
developers have different needs, and one size does not fit all. A productive
developer on their preferred platform will always outperform a frustrated
developer on a restricted one.

The question isn't whether your company _can_ provide Linux workstations - it's
whether they want to prioritize developer productivity over administrative
convenience.
