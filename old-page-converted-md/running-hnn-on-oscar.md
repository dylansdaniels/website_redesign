::: {.srj-header .hnn-header .darken-header}
::: {.srj-headertext}
Running HNN on Oscar
:::
:::

\
\
 

::: {.srj .m-width .srj-spacious}
![](https://hnn.brown.edu/wp-content/uploads/2019/06/Gears.png){.srj-small-icon}\

# Setting up an Account with Oscar {#setting-up-an-account-with-oscar .srj-center .hnn-violet}

First, make sure you have an account with Brown\'s computing cluster,
[Oscar](https://docs.ccv.brown.edu/oscar/). If you do not have an
account, you can create
one [here](https://brown.co1.qualtrics.com/jfe/form/SV_0GtBE8kWJpmeG4B) using
your Brown email address and ID number.\
\

::: {.srj .m-width .srj-spacious}
![](https://hnn.brown.edu/wp-content/uploads/2019/06/Gears.png){.srj-small-icon}\

# To Run HNN {#to-run-hnn .srj-center .hnn-violet}

1\. Go
to [Oscar-on-Demand](https://ood.ccv.brown.edu/pun/sys/dashboard).
Choose the Desktop application and launch a new session (pick 6 cores).\
\
2. Once the Desktop is launched, open the Terminal Emulator and enter
the following command. Note that after you have installed and run HNN
for the first time, you no longer need to run this line.\
\
` singularity pull docker://jonescompneurolab/hnn `\
\
3. To open the HNN graphical user interface (GUI), run:\
\
` singularity shell hnn_latest.sif   source /home/hnn_user/hnn_envs  cd /home/hnn_user/hnn_source_code  python3 hnn.py` \
\
4. HNN should open with two windows, and you should be able to click the
\"Run Simulation\" button and see a small dialogue box appear displaying
the time steps of the simulation appear in real-time.  
:::
:::
