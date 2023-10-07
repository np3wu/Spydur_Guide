---
layout: default
title: nbo_extractor
parent: Scripts
nav_order: 5
---

# nbo_extractor
{: .fs-9 }

This script is used to extract the NBO analysis from a Gaussian 16 output file. The output of this script is a EXcel file that contains 

## Overview
{: .fs-6 .fw-300 }

The nbo_extractor script is made to collect NBO data from your NBO calculation and organize them neatly into a csv file.  The script will collect the following data from your NBO calculation:

- <NATURAL BOND ORBITAL ANALYSIS> section.

- <Natural Bond Orbitals (Summary)> section.

You can check out these sections in any NBO calculations you have made by opening the *output*.log file and searching for the above sections.

## How to use nbo_extractor
{: .fs-6 .fw-300 }

If you have already downloaded the script, you can simply copy the script file into a folder containing your NBO calculations. 


Open a terminal and navigate to the folder containing the script.  Then run the following command:

```bash
python nbo_extractor.py
```

It will ask you what the ending of your NBO output file is.  For example, if your NBO output file is named "output.log", you would enter ".log" when prompted.  If your NBO output file is named "output.out", you would enter ".out" when prompted.

```bash
My NBO output files ends in: .log
```

You will be prompted to choose one of the section of the NBO output to collect:

```bash
Choose a function group to use:
1. Extract Bonding NBOs
2. Extract Summary NBO Section
Enter your choice (1-2):
```

If you choose option 1, the script will collect the <NATURAL BOND ORBITAL ANALYSIS> section.  If you choose option 2, the script will collect the <Natural Bond Orbitals (Summary)> section.  The script will then create a csv file containing the data from the section you chose.

You can choose to name the excel file yourself or keep empty, the default name will be "nbo_data.xlsx"
**Note: If you choose to name the excel file yourself, you do not need to include the .xlsx extension.**