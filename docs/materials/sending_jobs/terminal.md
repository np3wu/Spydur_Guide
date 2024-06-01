---
layout: default
parent: Sending Your First Gaussian Job
grand_parent: Materials
title: Using Terminal
nav_order: 2
---

# Using Terminal to Send Jobs
{: .fs-9 }

In this section, we will be using the terminal to send jobs to Gaussian through the SPYDUR cluster. 

{: .note-title }
> Important Note
>
> Again example 2.1 shows you how to send jobs using the Gaussview interface, but we do not have the entire Gaussian suite of programs installed on your personal computer. We will be interacting with a **remote machine** which has Gaussian installed. Your personal computer (the client) will be sending jobs to the remote machine (the server) to run the calculations.

## Logging into the SPYDUR Cluster

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

And a prompt to enter your password. Enter your password and press enter. You should now be logged into the cluster!

{: .important }
>The first time you log in it will ask to save the fingerprint of the server. Type `yes` and press enter.
>
> Your password will not show up as you type it in. This is a security feature to prevent people from seeing your password!

## Navigating The Terminal

Unlike folders on your computer, the terminal does not have the convienience of a graphical user interface. Instead, you will have to use commands to navigate through the terminal. Here are some basic commands to get you started:

```bash
ls
```

This command lists all the files and folders in your current directory.

```bash
mkdir work
```

This command creates a new directory named `work`.

```bash
cd work
```

This command changes your current directory to the `work` directory.

```bash
cd ..
```

This command changes your current directory to the parent directory.

```bash
rm -r work
```

This command removes the `work` directory and all its contents.

A list of more commands can be found [here](https://www.codecademy.com/articles/command-line-commands).

## Making a Gaussian Input File

Now that you are logged into the cluster, you can start making your Gaussian input file. 

Let's start by making a new directory to store all the files as you are working through the examples in the book. 

```bash
mkdir gaussian_tutorial
cd gaussian_tutorial
```
To create a Gaussian input file, you can use the `nano` command to create a new file. Our gaussian input file will be named `e2_1_formaldehyde.com`. The extension is very important! Do not forget `.com`

```bash
nano e2_1_formaldehyde.com
```
{: .note-title }
> Naming Convention
>
> Names should all be lowercase and without any spaces or special characters, including dots and commas. If you need to separate the words, use an underscore `_` instead. 

Using the nano editor, you can now type in the following input file:

```
%mem=2GB
%nprocshared=12
%chk=e2_1_formaldehyde.chk
# APFD/6-311+G(2d,p)

0 1
paste the coordinates here


 

```

{: .note-title }
> Important Note
>
> The Detailed Description of the file can be found on page 44-45 of the book "Exploring Chemistry with Electronic Structure Methods" by James B. Foresman and Æleen Frisch.

Now hit `Ctrl + X` to exit the nano editor. It will ask you if you want to save the changes. Type `Y` and press enter. Then, hit any key to escape the editor.

## Submitting the Job

Now that you have created the input file, you can submit the job to the cluster. We are using the `qg16` command to submit the job. 

```bash
qg16 e2_1_formaldehyde.com
```

To monitor the job, you can use the `squeue` command. This allows you to monitor the job as it is running.

```bash
squeue -u URID
```

{: .note-title }
> Important Note
>
> If you don't see your job in the queue, it may have died prematurely! use the `ls` command to see if the output file was created. If it was, you can use the `cat` command to see the output file.

## Conclusion

Congratulations on your first job submission! You can now go to the next section to learn how to visualize the output file using Chemcraft.