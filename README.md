# Fault-tolerant-demo-IBM5Q

This is the code for a small experiement to be conducted on the IBM 5Q chip of the [IBM Quantum Experience](https://quantumexperience.ng.bluemix.net), whose access to is needed in order to run the experiment. It also uses the [Python SDK](https://github.com/IBM/qiskit-sdk-py) developed especially by IBM for this. Some installation is needed, see below or follow the previous links.

The experiment consist in testing a small quantum error detecting code, and comparing its performance on several circuits to the unencoded versions of them.

For more information you can read :
[Gottesman2016](https://arxiv.org/abs/1610.03507)
[Vuillot2017 ... soon]


## Organisation

The Jupyter notebook Demonstration_Fault_Tolerance.ipynb contains the experiment.
The folder tools/ contains tool functions for the experiement in the file Experiment_tools.py.
The folder data/ contains text files for storing the ids of all previous experiments.


### Install Dependencies

> pip install -r requires.txt

