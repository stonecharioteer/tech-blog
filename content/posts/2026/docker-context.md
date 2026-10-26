______________________________________________________________________

date: "2026-10-14T20:53:08+05:30"
draft: true
title: "Using Docker on my Macbook without storing everything on it"
description:
"My M5 Macbook Pro has a 512 GB SSD. I use Docker contexts over Tailscale to
run containers on a used ThinkPad instead."
tags:

- "docker"
- "macbook"
- "homelab"
- "tailscale"

______________________________________________________________________

<!-- Working outline. The opening is draft prose; the section notes are not
finished article text. Confirm the target ThinkPad before publishing. The
active laptop context currently points to a P14s Gen 1, not the P1 Gen 2.
Redact usernames, IP addresses, and actual hostnames in commands and output. -->

I bought an M5 Macbook Pro with a 512 GB SSD. I wanted the 1 TB model, but I
couldn't afford it back then. I've written about
\[why I bought the Macbook\]({{< ref "posts/2026/macbook.md" >}}), and I still
like using it. I just don't want Docker images and build caches taking up the
storage I have.

Around the same time, I was buying used ThinkPads, mostly to set up as GitHub
Actions runners for my own projects. So I already had other machines I could
use. They could run Docker too.

I remembered that the Docker CLI had a way to use a remote host. I couldn't
remember what it was called, but I knew I'd seen it before. A bit of searching
led me to Docker contexts.

That was what I wanted. I could keep typing `docker run` on the Macbook and
have the containers run on one of the ThinkPads. The command runs on my
Macbook, but the Docker engine on the ThinkPad does the work.

I'll start with how that works on a home network. Then I'll add Tailscale,
which lets me use the same setup from a cafe.

## TLDR

- Docker CLI on the Macbook, Docker engine on the ThinkPad.
- A context tells the CLI which Docker engine to use.
- `docker context use laptop` selects it for subsequent commands.
- Images, containers, and volumes live on the ThinkPad. It supplies the CPU
  and RAM too.
- Tailscale makes the ThinkPad reachable when I'm away from home.
- This does not make remote files or ports local. Explain those limits below.

## I already had another machine for this

- Explain why I was buying used ThinkPads for GitHub Actions runners.
- Describe the chosen ThinkPad and its Linux setup after confirming the model.
- Keep the runner setup brief. This post is about using its Docker engine from
  the Macbook, not installing GitHub Actions runners.
- Explain that the Macbook's SSD and RAM do not get larger. The Docker work
  runs elsewhere.

## The Docker command and the Docker engine can be on different machines

- Explain the client/server split before showing configuration.
- Show the path in a small diagram:

```text
Macbook Docker CLI -> SSH over the home network -> ThinkPad Docker engine
```

- Define a context as a named connection configuration for the CLI.
- Explain that contexts can select different local or remote Docker engines.
  SSH is the connection method I use for the remote one.
- No Tailscale needed yet. Both machines are on the home network, and the
  Macbook can already SSH into the ThinkPad.
- Present this as the simplest example, not a claim that I first configured
  my actual setup without Tailscale.

## Setting up the context at home

- Prerequisites: Docker CLI on the Macbook, a running Docker engine and Docker
  CLI on the ThinkPad, and working SSH access over the home network.
- The remote Unix user must have permission to access the Docker socket.
  Mention that Docker access usually gives root-level control of the host.
- Show these commands with a placeholder for the ThinkPad's LAN address or
  a hostname that resolves on the home network:

```bash
docker context create laptop \
  --description "Linux devbox at home" \
  --docker "host=ssh://<remote-user>@<linux-host>"

docker context use laptop
docker context ls
docker info
```

- Explain that `<remote-user>` and `<linux-host>` are placeholders. Keep
  usernames, IP addresses, and actual hostnames out of published output.
- Explain the `*` in `docker context ls` and use `docker info` to confirm the
  server's hostname and operating system.
- Docker sends requests through SSH to the remote Docker socket. There is no
  need to expose the Docker engine on a TCP port.

## I still type `docker run`

```bash
docker run --rm hello-world
docker ps
docker images
```

- Explain where the image downloads and where the container runs.
- Show a one-command override with `docker --context laptop ps`.
- Show how to return to a configured local engine, for example
  `docker context use desktop-linux` for Docker Desktop.
- Note that `DOCKER_HOST`, `DOCKER_CONTEXT`, and command-line options can
  override the saved selection. Check these when a command uses the wrong
  engine.

{{< note title="Does Swarm use contexts underneath?" >}}
No. Docker contexts are client configuration. They tell my Docker CLI which
engine to send requests to. Swarm is part of the Docker engines themselves.
Its managers and workers communicate directly over the network, not through
contexts or the SSH connection from my Macbook.

I don't need to create contexts for machines to join a swarm. I initialize a
manager, then have other engines join using its address and a join token.
Swarm manages membership and schedules service tasks across those machines.

The CLI still selects an engine when I type `docker swarm init`. Without a
custom context or connection override, it normally uses the default context,
which points to a local engine. That is ordinary CLI behaviour, not how Swarm
connects its nodes.

I can separately create a context pointing to a Swarm manager and administer
it remotely. But that is optional. For this setup, I only need to send Docker
commands to another machine. I don't need Swarm for that.

See Docker's [context documentation](https://docs.docker.com/engine/manage-resources/contexts/)
and [Swarm tutorial](https://docs.docker.com/engine/swarm/swarm-tutorial/).
{{< /note >}}

## The parts that are still remote

- Bind mounts refer to the ThinkPad's filesystem. `-v "$PWD:/app"` does not
  upload the Macbook's project directory. Explain the actual file workflow
  once confirmed.
- Published ports belong to the ThinkPad. At home, use its LAN address to
  reach a service, subject to its bind address and firewall. The Macbook's
  `localhost` is still the Macbook.
- The ThinkPad is x86-64; the M5 is ARM64. Explain why the remote engine's
  architecture matters for image selection and builds. Check the selected
  Buildx builder before making claims about where builds run.
- The ThinkPad must be awake and reachable. This is not an offline setup.
- Existing Docker data on the Macbook stays there. Switching contexts does
  not migrate it or reclaim its space.
- If runners share the same engine, mention resource contention and why I
  would not give untrusted workflows access to it.

## But I also want to use this from a cafe

This works while both machines are on my home network. But I bought the
Macbook to take it with me. If I sit down at a cafe, the ThinkPad is still at
home. A Docker context doesn't solve that part. It remembers where to connect;
it doesn't make that address reachable.

This is where I use Tailscale.

- Explain that both machines join my private Tailscale network. The Macbook
  can reach the ThinkPad through that network even when they're on different
  WiFi networks, subject to tailnet policy.
- Confirm SSH access to the ThinkPad's Tailscale address first.
- Update the example context to use that address. This changes the connection
  destination, not where Docker stores data or runs containers.

```bash
# Replace both placeholders with your own values.
ssh <remote-user>@<tailscale-ip>

docker context update laptop \
  --description "Linux devbox over Tailscale" \
  --docker "host=ssh://<remote-user>@<tailscale-ip>"

docker context use laptop
docker info
docker run --rm hello-world
```

```text
Macbook at a cafe -> SSH over Tailscale -> ThinkPad at home -> Docker engine
```

- The `docker run` command is unchanged. The image and container still live
  on the ThinkPad. Cafe WiFi provides the Macbook's internet connection.
- No exit node or router port forwarding is required for this peer connection.
  The ThinkPad must stay awake, online, and accessible under tailnet policy.
- Keep SSH over Tailscale distinct from the Tailscale SSH feature. The
  `ssh://` endpoint alone does not establish which SSH server handles login.
  Link to \[my Tailscale SSH post\]({{< ref "posts/2026/tailscale-ssh.md" >}}).
- For published services, use the ThinkPad's Tailscale address instead of its
  LAN address. Service bindings, the host firewall, and tailnet policy must
  allow the connection. Docker context does not forward application ports.

## What I get out of this

- End with the actual arrangement rather than a general recommendation.
- I keep using the Macbook's terminal. The used ThinkPad stores the Docker
  data and runs the containers.
- The 512 GB SSD is still 512 GB. I just don't need to put this work on it.

## References

- [Docker contexts](https://docs.docker.com/engine/manage-resources/contexts/)
- [Connecting to Docker over SSH](https://docs.docker.com/engine/security/protect-access/)
- [Remote bind-mount limits](https://docs.docker.com/engine/storage/bind-mounts/)
