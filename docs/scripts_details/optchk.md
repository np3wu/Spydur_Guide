---
layout: default
title: optchk
parent: Scripts
nav_order: 6
---

# optchk
{: .fs-9 }

This script is a convient way to determine if your optimization and frequency job yielded a fully optimized structure. 

This script can be used in bash to print out a table summarizing the status of the job from the output file. An additional option can be included to export a `.csv` file of the table.

### Usage

If you have not done so already, please check out the section [Downloading Necessary Scripts] to get the script onto the Cluster.

An example of how to use the script is as follows:

```bash
05:33:52 PM USER@spydur ~/folder1/subfolder1 $ optchk

+--------------------------------------------------+----------------+-------------------------+
| Log File                                         | Is Optimized   | No Negative Frequency   |
+==================================================+================+=========================+
| /home/USER/folder1/subfolder1/co_ii_2_int.log    | True           | False                   |
+--------------------------------------------------+----------------+-------------------------+
| /home/USER/folder1/subfolder1/cr_ii_3_int.log    | False          | False                   |
+--------------------------------------------------+----------------+-------------------------+
| /home/USER/folder1/subfolder1/cu_i_1_int.log     | True           | False                   |
+--------------------------------------------------+----------------+-------------------------+
| /home/USER/folder1/subfolder1/fe_ii_3_int.log    | True           | True                    |
+--------------------------------------------------+----------------+-------------------------+
| /home/USER/folder1/subfolder1/mn_ii_2_int.log    | True           | True                    |
+--------------------------------------------------+----------------+-------------------------+
| /home/USER/folder1/subfolder1/ni_ii_1_int.log    | True           | False                   |
+--------------------------------------------------+----------------+-------------------------+
| /home/USER/folder1/subfolder1/sc_iii_1_int.log   | True           | False                   |
+--------------------------------------------------+----------------+-------------------------+
| /home/USER/folder1/subfolder1/ti_iv_1_th_int.log | False          | False                   |
+--------------------------------------------------+----------------+-------------------------+
| /home/USER/folder1/subfolder1/v_v_1_int.log      | True           | False                   |
+--------------------------------------------------+----------------+-------------------------+
| /home/USER/folder1/subfolder1/zn_ii_1_int.log    | True           | True                    |
+--------------------------------------------------+----------------+-------------------------+
Data will not be exported to CSV.
```

I annonymized the output for privacy. Essentially, the table will help you determine if the optimization and frequency job was successful. The `Is Optimized` column will tell you if an optimized structure was found in the output file. The `No Negative Frequency` column will tell you if the there is any negative frequency in the frequency calculation.

For example, row 1 has True for `Is Optimized` and False for `No Negative Frequency`. This means that the optimization was successful, but the frequency calculation yielded negative frequencies, therefore the optimization did not reach a minima, only a saddle point.

The possible outcomes should be:

| Is Optimized | No Negative Frequency | Looking for | Meaning |
|:------------:|:----------------------:|:-------:| :-------: |
| True         | True                  | A minimum | The structure is a minimum and fully optimized |
| True         | False                 | A minimum | The structure is a saddle point and not fully optimized |
| False        | False                 | A minimum | No Optimized Structure found and potentially no frequency calculation found. Possible error in calculation |

If you would like to know more about the theory behind this, check out Chapter 3 of Exploring Chemistry with Electronic Structure Methods by James B. Foresman and Æleen Frisch.

### Exporting to CSV

If you would like to export the data to a `.csv` file, you can include the `-csv` option:

```bash
05:33:52 PM USER@spydur ~/folder1/subfolder1 $ optchk -csv
```

You will see a file named `optchk.csv` in the directory you ran the command in. The file will contain the same table as the one printed out in the terminal.

[Downloading Necessary Scripts]: https://np3wu.github.io/Spydur_Guide/docs/gettingstarted/scripts/scripts.html