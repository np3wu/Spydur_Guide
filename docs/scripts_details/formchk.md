---
layout: default
title: formchk
parent: Scripts
nav_order: 2
---

# formchk
{: .fs-9 }

While not a complicated script, it is still useful to understand what it does. This script is used to convert the output of a Gaussian 16 job to a format that can be read by other programs. For example, if you want to visualize the output of a Gaussian 16 job using [GaussView](https://gaussian.com/gaussview6/), you will need to convert the output `.chk` file to a `.fchk` file short for formated checkpoint.

The difference between this script and Gaussian's built in script is that this script will go over the entire folder **indiscriminately**. Meaning that **any** `.chk` file will be converted to a `.fchk` file. This is useful if you have multiple jobs in a folder and you want to convert all of them to `.fchk` files.

## Usage

No need to edit anything in this script. Just run it in the folder that contains the `.chk` files you want to convert.