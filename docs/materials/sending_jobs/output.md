---
layout: default
parent: Sending Your First Gaussian Job
grand_parent: Materials
title: Output
nav_order: 6
---

# Diving into the Text Output
{: .fs-9 }

The `.log` file is the text output file that contains all the information about the job you just ran. This file is dense and very hard to read. But knowing where to look can help make sense of what it is.

Let's take a look at the `.log` file for example 2.1.

## Opening the `.log` File in Terminal

To open the `.log` file, we will be using `nano` a terminal-based text editor. 

```bash
nano formaldehyde.log
```

{: .note-title }
> Important!
>
> Make sure you are in the same directory as the `.log` file you want to open. If you are not, you will need to navigate to the correct directory using the `cd` command.

You can navigate through the file using the arrow keys. To exit `nano`, press `Ctrl + X`. You will be prompted to save the changes you made. Press `Y` to save the changes, or `N` to discard them. We don't want to make any changes, so press `N`.

## Normal Termination

At the very end of the `.log` file, you will see the following lines:

```bash
 Job cpu time:       0 days  0 hours  1 minutes 55.6 seconds.
 Elapsed time:       0 days  0 hours  1 minutes 55.9 seconds.
 File lengths (MBytes):  RWF=      6 Int=      0 D2E=      0 Chk=      2 Scr=      1
 Normal termination of Gaussian 16 at Tue Apr  2 20:57:42 2024.
```
`Normal termination` means that the job ran successfully. If you see `Error termination`, that meant something went wrong in the process, often accompanied by error messages.

## SCF Done

Use the search command `crtl + w` or `f6` key to search for `SCF Done`. Here you will find the total energy of the molecule. 

```bash
 SCF Done:  E(RAPFD) =  -114.442264139     A.U. after   10 cycles
            NFock= 10  Conv=0.22D-08     -V/T= 2.0033
```

`a.u` stands for atomic units. It is also called Hartrees.

## Dipole Moment

Use the search command `crtl + w` or `f6` key to search for `Dipole moment`. Here you will find the dipole moment of the molecule.

```bash
 Dipole moment (field-independent basis, Debye):
    X=              2.5367    Y=              0.0000    Z=              0.0000  Tot=              2.5367
```