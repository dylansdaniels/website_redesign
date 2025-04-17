<!--
# Title: 1.2 Template Model
# Updated: 2024-11-14
#
# Contributors:
    # Dylan Daniels
-->

<!-- compare original: https://hnn.brown.edu/under-the-hood/ -->

# 1.2 Template Model

The following sections contain details on the construction of the cells
and circuits in HNN's canonical **neocortical Template model**
(comprised of a layered cortical column) as well as exogenous driving
inputs. Each section details the parameters that can currently be
adjusted in the HHN-GUI for the user's hypothesis testing needs. If
there are parameters you would like to be able to adjust in the HNN-GUI
but cannot, we encourage you to submit suggestions to our [Github issues
page](https://github.com/jonescompneurolab/hnn/issues).

While the adjustable parameters in the HNN-GUI are necessarily limited,
all parameters and network configurations can be changed based on your
hypothesis testing goals using NEURON-Python code in our documented and
supported [HNN-Core repository
page](https://github.com/jonescompneurolab/hnn-core). Please see
the ["Getting Started"](https://hnn.brown.edu/getting-started/) page
for more details on the functionality of HNN-GUI and HNN-Core, and how
more specialized neocortical Template models can be used and developed.

Our Template model was based on our prior published studies where we developed predictions on the
cell and circuit mechanisms underlying ERPs and low-frequency rhythms and differences across
experimental conditions. These prior studies were motivated by a long history of research, mainly in
animals, investigating the neural mechanisms of ERPs and low-frequency rhythms (ERPs:
[@jones_neural_2007], [@kohl_neural_2022], alpha rhythms: [@jones_quantitative_2009],
[@jones_alpha-frequency_2000], [@pinto_analysis_2003], [@ziegler_transformations_2010],
[@sherman_neural_2016], beta rhythms: [@jones_quantitative_2009], [@pinto_analysis_2003],
[@sherman_neural_2016], gamma rhythms: [@pinto_analysis_2003], [@cardin_driving_2009],
[@carlen_critical_2012], [@vierling-claassen_computational_2010], [@lee_distinguishing_2013]). HNN
allowed us to test if the cell and network elements thought to be the primary generators of these
signals based on animal research (e.g. a sequence of thalamocortical drive to the network) could
produce macro-scale current dipole signals that were in agreement with our recorded data. While the
literature guided us to a starting point that constrained the investigation, the exact parameters to
use to present the data were unknown. By directly comparing the current dipole output of the model
to source localized empirical data, we were able to titrate parameters (both through hand tuning and
algorithmic parameter estimation) to produce a close fit to the source waveform (i.e. small root
mean squared error (RMSE)). Once a close fit to the current dipole waveform was established the
model provided a number of testable predictions on the underlying cell and circuit activity,
i.e. exogenous input timing and strength, cell spiking activity, LFP/CSD, etc. (see
[Publications](https://hnn.brown.edu/publications/)).

The Template model and Tutorials are meant as starting points for how to use HNN to generate testable predictions and **not** to propagate singular theories on signal generation.

#### [3.1 Cortical Column Structure](../03_model_assumptions/cortical_column_structure.html)
#### [3.2 Primary Electrical Currents](../03_model_assumptions/primary_electric_currents.html)
#### [3.3 Neurons: Morphology and Physiology](../03_model_assumptions/neurons_morphology_and_physiology.html)
#### [3.4 Synaptic Connectivity](../03_model_assumptions/synaptic_connectivity.html)
#### [3.5 Evoked and Rhythmic Driving Inputs](../03_model_assumptions/evoked_and_rhythmic_driving_inputs.html)
#### [3.6 Tonic and Noisy Driving Inputs](../03_model_assumptions/tonic_and_noisy_driving_inputs.html)
