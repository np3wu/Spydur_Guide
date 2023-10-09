---
layout: default
parent: Downloading Necessary Scripts
grand_parent: Getting Started
title: Activating the Scripts
nav_order: 2
---

# Activating the Scripts
{: .fs-9 }

## Using the scripts

Now that your have the scripts, you can freely access them using the terminal. Try typing in the terminal (for winscp there is a open session in Putty button on the top bar):

```bash
cd scripts
sg16.py -h
```

the `-h` command is short for help and will show you all the possible commands you can use with the script. And for this you will see the output:

```bash
Current directory:  /home/np3wu
usage: sg16.py [-h] jobname

positional arguments:
  jobname     Name of the job

optional arguments:
  -h, --help  show this help message and exit
```

This means it only takes in 1 arguement `jobname`. The fact that the computer gives you a response means that the script is working.

However, if you try to run the same command outside of the folder:

```bash
cd
python sg16.py -h
```

Nothing happens! This is because the script is not in your path. To do this, you will need to edit your `.bashrc` file. This file is located in your home directory. To edit it, type the following command into your terminal:

```bash
nano ~/.bashrc
```
> NOTE: If you need a refresher on how the `nano` command works checkout this [website](https://linuxize.com/post/how-to-use-nano-text-editor/)

And you will get something that looks like this:

```bash
# .bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
  . /etc/bashrc
  if groups `whoami` | grep -q people; then
      . /usr/local/etc/usersrc/common
  fi
fi

# User specific environment
if ! [[ "$PATH" =~ "$HOME/.local/bin:$HOME/bin:" ]]
then
    PATH="$HOME/.local/bin:$HOME/bin:$PATH"
fi
export PATH

# Uncomment the following line if you don't like systemctl's auto-paging featur$
# export SYSTEMD_PAGER=

# User specific aliases and function:
```

You will need to add the following lines to the bottom of the file:

```bash
# User specific aliases and function:
export PATH="$HOME/scripts:$PATH"
```

and reload your `.bashrc` file with the command

```bash
source ~/.bashrc
```
> NOTE: Everytime you make changes to the `.bashrc ` file, you need to use this line to apply the changes.

Now try the command again, outside of where the script is located. If it works, then you have successfully added the scripts to your path!

> Important Notes:
 The `$HOME` used in the code above is just a shortcut that will work for everyone. If you want to set any other filepath as PATH. You can perform the same operation replacing
```bash
"$HOME/scripts:$PATH"
```
> with any file path that you desire. For example:
```bash
"your/desired/filepath:$PATH"
```

## Setting aliases

You can also set aliases for the scripts. This is useful if you want to shorten the command to run the script. For example, you can set an alias for `sg16.py` to `sg16`. To do this, you will need to edit your `.bashrc` file again. Type the following command into your terminal:

```bash
nano ~/.bashrc
```

and add the following line to the bottom of the file:

```bash
alias sg16="python $HOME/scripts/sg16.py"
```

and then reload your `.bashrc` file with the command

```bash
source ~/.bashrc
```

You can set aliases this way for anyother types of scripts.

There is one more detail I would like you to know and you can check that out in the next page.

[<< Previous](https://np3wu.github.io/Spydur_Guide/docs/gettingstarted/scripts/move_scripts_winscp.html) | [Next >>](https://np3wu.github.io/Spydur_Guide/docs/gettingstarted/scripts/more_scripts.html)