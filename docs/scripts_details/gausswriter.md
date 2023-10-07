---
layout: default
title: gausswriter
parent: Scripts
nav_order: 4
---

# gausswriter
{: .fs-9 }

This script is used to write a Gaussian 16 input file, however, limitted to what I have used in my research. 

The purpose of making this is to streamline the process of input file creation by limiting common errors such as typos and missing keywords.

Due to the repetitive nature of the input file. It is prime for automation. Let me show you how this script can help you.

## Usage

The script will ask you a series of questions, much like a wizard, to help you create your input file. 

```bash
python gausswriter.py
```

The first question you will encounter is:

```bash
Do you want to use an existing file in the folder as a template?
This includes the memory, number of processors, and input line.
If yes, include name of file (with extension) as template >>>
```

If you have an existing input file that you want to use as a template! By entering the name of the file (with the extension) the script will then go through the file and extract these information:

- `mem` or Memory
- `nproc` or number of processors
- Input line

and then parse it onto your new file. This will save you time from having to type these information again.

However, if you want to start from scratch, simply press enter and the script will continue.

> One thing to note about the input line is that the pound sign `#` is included in the template for the script. So do not enter the pound sign when prompted for the input line. (an easy fix is to add a check if the pound sign is there or not but I'll leave this here for now)

Let's go over some of the input it requires you to enter:

#### filename

This is the name of your output file. It will be saved as a `.com` file. So if you want to name your input file `input.com`, simply enter `input`.

#### mem

Requires an integer value. This is the amount of memory you want to allocate for your calculation. It is by default in GB. So if you want to allocate 8 GB of memory, simply enter `8`.

#### nproc

Similar to mem, also an integer value. This is the number of processors you want to use for your calculation. If you want to use 4 processors, simply enter `4`.

#### input line

This is the line that you would normally enter in your input file. Not that you do not need the pound sign `#` at the beginning of the line.

Because the pseudopotential is provided by default. You will want to enter `pseudo=read` or `genecp` in this line. An example input line would be:

```bash
HF/pseudo=read opt freq
```

#### Job Title

You can enter anything you want here. This will be the title of your calculation.

#### charge and spin

Both accepts integer values.

#### geom

You can get the geometry by using `Chemcraft` or `Avogadro`. Build your molecule then copy the geometry information into the terminal prompt (right-clicking). Then hit `ctrl`+`d` to end the input.

#### chemical_formula

Finally you will be prompted to enter a chemical formula. This should be simplified as much as possible, containing each element followed by the count. 

For example, if you have 3 carbon, 6 hydrogen, and 1 oxygen, you would enter `C3H6O`. Regardless of if you have a ketone `CH3COCH3` or an alcohol `CH3CH2OH`, or an aldehyde `CH3CH2CHO`. The geometry information you provided above is sufficient for the calculation to distinguish between the different structures.

## Things to consider

You can see that this script is jankey at best. It is not perfect and it is not meant to be. It is a tool that I created to help me with my specific research.

If you find that you want to modify the script to best suit your needs. Feel free to do so. I will provide some details on how this script is built in other sections.