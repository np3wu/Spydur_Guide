---
layout: default
title: nbo
parent: Scripts
nav_order: 3
---

# nbo
{: .fs-9 }

This script simply sends an nbo job based on the checkpoint file `.chk` inside your folder. It will iterate through each file prompting you each time if you want to perform an NBO calculation.

```bash
python nbo.py
```
If the script finds a `.chk` file, it will prompt you if you want to perform an NBO calculation.

```bash
Perform NBO calculation on {file_name}? yes(y)/no(n): 
```
If you enter `yes` or `y`, the script will then submit the job to the cluster. If you enter `no` or `n`, the script will move on to the next file.

---
### Common issues

If python nbo.py is not callable from the terminal, you may need to add the following line to your `.bashrc`:

```bash
export PATH=$PATH:$HOME/scripts
```