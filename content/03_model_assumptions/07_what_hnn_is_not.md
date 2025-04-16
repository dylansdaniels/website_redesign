<!--
# Title: 3.7 Caveats: What HNN is NOT
# Updated: 2024-01-16
#
# Contributors:
    # Dylan Daniels
-->

# 3.7 Caveats: What HNN is NOT

HNN is **not** a source localization software! Instead, it is a method for *interpreting* the cell and network level generators of a source signal from a localized brain area *after* you have an estimate of the source location, time course, and orientation. There are many excellent source localization software packages for this estimation process. For an example of how to perform source localization using [MNE-Python](https://mne.tools/stable/index.html) followed by cell and circuit level interpretation with HNN, see [our Textbook example here](../08_data_to_simulation/from_meg_to_hnn.html).

Our goal is **not** to promote singular theories on the origin of any particular signal. Instead, we aim to provide a tool based on known biophysics and training resources where researchers can develop testable predictions on the neural origin of their data. The tutorials on use of HNN are based on our prior published studies of ERPs and low-frequency oscillations from the primary somatosensory cortex (see [our Publications page](https://hnn.brown.edu/publications/). We provide data, initial parameter sets, and workflows to teach users how to develop and test hypotheses on the neural origins of these signals, similar to our prior work. Once this workflow is learned, users are able to use HNN to test their own hypotheses.
