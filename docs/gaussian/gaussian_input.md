---
layout: default
parent: Gaussian
title: Sending Gaussian Jobs on Spydur
---

# Sending Gaussian Jobs on Spydur
{: .fs-9 }

### Make Slurm File


First make teh slurm file

```bash
vim namefile.slurm
```

Then copy and paste the following code from [Princeton Research Computing website]. Fill in highlighted portions with your specificities: 


```bash
#!/bin/bash
#SBATCH --job-name= file_name # create a short name for your job

#SBATCH --ntasks=N    # total number of tasks across all nodes
#SBATCH --cpus-per-task=1           # cpu-cores per task
#SBATCH --mem=40G      # total memory per node (4G per cpu-core is default)
#SBATCH --time=01:00:00              # total run time limit (HH:MM:SS)
#SBATCH --mail-type=begin          # send email when job begins
#SBATCH --mail-type=end             # send email when job ends
#SBATCH --mail-user=email address

module purge
module load gaussian/gaussian

cd  /scratch/$USER/test
g16 input.com output.log
```

Then you are ready to run the job!

### Send the Job


```bash
sbatch name.slurm
```

When your job is complete, open WinSCP to see your new .log and .chk files. 


---
[Princeton Research Computing website]: https://researchcomputing.princeton.edu/support/knowledge-base/gaussian
