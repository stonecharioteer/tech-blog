# Building an Over-Engineered Download Manager in Rust.

I want to write an over-engineered download manager in Rust, so that I can learn
a lot of Rust features from the ground up.

I want to extend
[`stonecharioteer/download-manager`](https://github.com/stonecharioteer/download-manager)
to _download all the things_. I want it to use every damned concurrency feature
I can find in Rust, and I want it to download HTTP, FTP, P2P and any other types
of download out there.

## Protocols & Sources

- HTTP/HTTPS
- Direct URL downloads
- Redirects (3xx chains)
- HTTP/1.1 vs HTTP/2 vs HTTP/3 (QUIC)
- Range requests (partial content)
- Chunked transfer encoding
- Content-Encoding (gzip, br, etc.)
- Authenticated endpoints (Basic, Bearer, cookies)
- Behind HTTP proxies

## FTP-family

- FTP (active/passive)
- FTPS (explicit/implicit TLS)
- SFTP (over SSH) Web & Remote

## Filesystems

- WebDAV
- SMB / CIFS (network shares)
- NFS mounts treated as remote sources

## Cloud Object Storage

- S3 pre-signed URLs
- S3 API (List/Get/Head)
- GCS / Azure Blob equivalents
- Generic S3-compatible (MinIO, Wasabi)

## P2P / Swarm

- BitTorrent (.torrent files)
- Magnet links
- DHT + trackers (HTTP/UDP)
- uTP / TCP transports
- Private / tracker-only torrents

## Content-addressed / Distributed

- IPFS (ipfs://, ipns://)
- Maybe simple “LAN swarm” protocol of your own

## Streaming-ish

- HLS (m3u8 playlists – sequential TS/fragment downloads)
- MPEG-DASH (MPD manifest)
- Progressive HTTP media (just treat as large files)

## Messaging / Indirect Sources

- Email attachments (IMAP/POP3)
- Slack/Discord/Matrix media URLs (API-based)
- GitHub/GitLab release assets

## Package / Artifact Registries

- HTTP-based package registries (PyPI, npm, crates.io, etc.)
- Container registries (Docker/OCI layers)
- Custom artifact servers (Nexus, Artifactory)

This list is a _LOT_, but doing _all_ this would no doubt help me understand
Rust, no doubt.
