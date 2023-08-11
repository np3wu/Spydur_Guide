---
layout: default
parent: Getting Started
title: Accessing the Cluster
---

# Accessing the Spydur Cluster
{: .fs-9 }

## Using Terminal

#### Mac/Linux

Your terminal is already set up to access the cluster. Simply type the following command into your terminal:

```bash
ssh URID@spydur
```

You will see some text printed out that says something like:

```bash
This is a University of Richmond (UofR) computer system.

All data contained within UofR computer systems is owned by
the University of Richmond, and may be monitored, intercepted,
recorded, read, copied, or captured in any manner and
disclosed in any manner, by authorized personnel.

THERE IS NO RIGHT OF PRIVACY IN THIS SYSTEM.

System personnel may disclose any potential evidence of crime found on
UofR computer systems for any reason.

USE OF THIS SYSTEM BY ANY USER, AUTHORIZED OR UNAUTHORIZED,
CONSTITUTES CONSENT TO THIS MONITORING, INTERCEPTION,
RECORDING, READING, COPYING, or CAPTURING and DISCLOSURE.
```

And a prompt to enter your password. Enter your password (it will not show up as you type) and press enter. You should now be logged into the cluster! 

#### Windows

If you are using Windows, you will need something like [Putty] to access the cluster via the command line.

```bash
ssh URID@spydur
```

Same exact instructions as above.

## Using WinSCP

WinSCP is a SFTP client for Windows with a Graphical User Interface. It is a great tool for transferring files between your computer and the cluster.

Simply open WinSCP and enter the following information in the appropriate fields:

- Host name: spydur.richmond.edu
- User name: URID
- Password: Your password (Optional)

![winscp_startup_window](./images/program/winscp/winscp_startup_window.PNG)


Additionally, you can also save a workspace by clicking the "Save" button in the bottom left corner. This will allow you to quickly access the cluster in the future.

---
[Putty]: https://www.putty.org/