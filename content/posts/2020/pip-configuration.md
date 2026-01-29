---
date: 2020-02-29T10:00:00+05:30
draft: false
title: Configuring Pip to Work in Enterprise Environments
description:
  How to configure pip for corporate networks with proxy servers and SSL
  certificates. Setting up environment variables and configuration files to work
  around common enterprise networking challenges.
tags:
  - "python"
  - "pip"
  - "enterprise"
  - "configuration"
---

The hardest thing about using package managers within an enterprise is getting
them to download the packages you need on the office network. Oftentimes, you
are hindered by SSL errors, and other times you get bogged by DNS errors.

## Downloading External Packages

Most of us either disable SSL verification at this point or contact IT about
getting trusted certificates. The former is a bad idea. The second option is not
bad, but it does lead down the rabbithole of "why do you need this package?"

Instead, you should know that you can easily set some environment variables to
help with this.

```bash
export HTTP_PROXY=http://<username>:<password>@<proxy.company.com>:<port>
export http_proxy=$HTTP_PROXY
export HTTPS_PROXY=http://<username>:<password>@<proxy.company.com>:<port>
export https_proxy=$HTTP_PROXY
```

This works for most tools. Some tools follow the Windows way, utilizing the
uppercase values, and some use the lowercase. Now that's food for thought. If
you are writing your own tool that works with the internet, make sure to support
_both_ methods. This helps your users' experience greatly.

The above settings should solve your _dns_ issues, but they won't help the SSL
errors. For that, you will need to configure your tools specifically.

For pip, the easiest way is to use the configuration file. Before you do that,
however, ensure you have updated pip to the latest version.

```bash
python3 -m pip install -U pip
```
