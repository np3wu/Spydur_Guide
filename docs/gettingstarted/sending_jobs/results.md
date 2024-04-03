---
layout: default
parent: Sending Your First Gaussian Job
grand_parent: Getting Started
title: Results
nav_order: 4
---

# Checking the Results of Your Job
{: .fs-9 }

Once your job have reached completion, you will be able to see multiple files with the extensions `.log`, `.chk`, and `.fchk`. Try double-clicking on the `.log` file to open it.

Up until now we strayed from the instructions in the example 2.1 due to differences in how we send the job. But now that we have the results, we can use Gaussview (which is installed on your computer) to view the output files.

{: .note-title }
> Notice for Linux users
>
> To open Gaussview on your computer, you will need to use the terminal. You can do this by typing `gv` in the terminal.

## Getting Files from SPYDUR to Your Windows Computer

{: .note-title }
> Important!
>
> This section is for Windows users only!

Now to get those results down to your local machine!

If you are working on a Windows computer, directly transfer the files by highlighting them and dragging them over. I recommend creating a folder in your `Documents` folder to store the work you do on SPYDUR. That way you have backups of your work! Name it something like `SPYDUR_tutorial`. You can even break it down further by creating subfolders for each chapter or section you are working on. Having a system in place will help you stay organized and make it easier to find your work later on.

`Documents` > `SPYDUR_tutorial` > `Chapter_2` > `e2.1`

 Follow the directions on page 46 of the book to open the `.log` file in Gaussview.

## Getting Files from SPYDUR to Your Computer using Terminal

{: .note-title }
> Important!
>
> This section is for Linux users only!

So you're using terminal. Your want to copy the files from SPYDUR to your computer. But there's no option to select and copy! What do you do?

Like everything else in the terminal, there's a command for that. The command you will use is `scp`.

`scp` stands for secure copy. It is a command used to copy files from one computer to another. The syntax for `scp` is as follows:

```bash
scp username@hostname:/path/to/file /path/to/destination
```

Let's break this down a bit more:

>`scp` is the command to copy files.

>`username@hostname:/path/to/file` is the location of the file you want to copy. 
>>- Replace `username` with your username on SPYDUR. i.e. `ur1id`
>>- Replace `hostname` with the hostname of the server you are copying from. i.e. `spydur`
>>- Replace `/path/to/file` with the location of the file you want to copy. i.e. `/home/ur1id/SPYDUR_tutorial/Chapter_2/e2.1/e2.1.log`

{: .note-title }
> Easy way to get the path!
>
> You can get the path by typing `pwd` in the terminal. This will give you the full path of the directory you are currently in. Then just manually add the rest of the path to the file you want to copy.
> Another way is to type `readlink -f filename` and replace `filename` with your desired file.


>`/path/to/destination` is the location where you want to copy the file to. This can be on your local machine or another server.
>>- Navigate through your Linux system with `ls` and `cd` and make a folder with `mkdir`.
>>- A file system such as `Documents` > `SPYDUR_tutorial` > `Chapter_2` > `e2.1` will be `~/Documents/SPYDUR_tutorial/Chapter_2/e2.1`
>>- Type `pwd` in the terminal (a different session that is not connected to SPYDUR) to get the full path of your local machine. 

 Follow the directions on page 46 of the book to open the `.log` file in Gaussview.

