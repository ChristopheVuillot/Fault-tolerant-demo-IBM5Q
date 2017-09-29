###########################################################################################
#            Tools for demonstrating fault-tolerance on the IBM 5Q chip
#
#   contributor : Christophe Vuillot
#   affiliations : - JARA Institute for Quantum Information, RWTH Aachen university
#                  - QuTech, TU Delft
#
###########################################################################################

import random
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import t, norm

# Functions that create all the circuits inside a given QuantumProgram module
#############################################################################

# Misc aux circuits
###################
def swap_circuit(pair,qp, qri=0, cri=0):
    qrs = [qp.get_quantum_register(qrn) for qrn in qp.get_quantum_register_names()]
    crs = [qp.get_classical_register(crn) for crn in qp.get_classical_register_names()]
    qcircuitswap = qp.create_circuit("SWAP"+str(pair),qrs,crs)
    qcircuitswap.cx(qrs[qri][pair[0]],qrs[qri][pair[1]])
    qcircuitswap.h(qrs[qri][pair[0]])
    qcircuitswap.h(qrs[qri][pair[1]])
    qcircuitswap.cx(qrs[qri][pair[0]],qrs[qri][pair[1]])
    qcircuitswap.h(qrs[qri][pair[0]])
    qcircuitswap.h(qrs[qri][pair[1]])
    qcircuitswap.cx(qrs[qri][pair[0]],qrs[qri][pair[1]])
    return qcircuitswap

def measure_all(qp, qri=0, cri=0):
    qrs = [qp.get_quantum_register(qrn) for qrn in qp.get_quantum_register_names()]
    crs = [qp.get_classical_register(crn) for crn in qp.get_classical_register_names()]
    qcircuitmeasure = qp.create_circuit("Measure all",qrs,crs)
    qcircuitmeasure.measure(qrs[qri][0],crs[cri][0])
    qcircuitmeasure.measure(qrs[qri][1],crs[cri][1])
    qcircuitmeasure.measure(qrs[qri][2],crs[cri][2])
    qcircuitmeasure.measure(qrs[qri][3],crs[cri][3])
    qcircuitmeasure.measure(qrs[qri][4],crs[cri][4])
    return qcircuitmeasure

# The encoded preparations
##########################
def encoded_00_prep_FTv1(qp, qri=0, cri=0):
    qrs = [qp.get_quantum_register(qrn) for qrn in qp.get_quantum_register_names()]
    crs = [qp.get_classical_register(crn) for crn in qp.get_classical_register_names()]
    qc_FTv1 = qp.create_circuit("e|00>FTv1",qrs,crs)
    qc_FTv1.h(qrs[qri][2])
    qc_FTv1.cx(qrs[qri][2],qrs[qri][0])
    qc_FTv1.cx(qrs[qri][2],qrs[qri][1])
    qc_FTv1.h(qrs[qri][2])
    qc_FTv1.h(qrs[qri][3])
    qc_FTv1.cx(qrs[qri][3],qrs[qri][2])
    qc_FTv1.h(qrs[qri][2])
    qc_FTv1.h(qrs[qri][3])
    qc_FTv1.cx(qrs[qri][2],qrs[qri][4])
    qc_FTv1.cx(qrs[qri][2],qrs[qri][0])
    #qc_FTv1.measure(qrs[qri][0],crs[cri][0])
    return qc_FTv1

def encoded_00_prep_NFTv1(qp, qri=0, cri=0):
    qrs = [qp.get_quantum_register(qrn) for qrn in qp.get_quantum_register_names()]
    crs = [qp.get_classical_register(crn) for crn in qp.get_classical_register_names()]
    qc_NFTv1 = qp.create_circuit("e|00>NFTv1",qrs,crs)
    qc_NFTv1.h(qrs[qri][3])
    qc_NFTv1.cx(qrs[qri][3],qrs[qri][4])
    qc_NFTv1.cx(qrs[qri][3],qrs[qri][2])
    qc_NFTv1.cx(qrs[qri][2],qrs[qri][1])
    return qc_NFTv1

def encoded_00_prep_FTv2(qp, qri=0, cri=0):
    qrs = [qp.get_quantum_register(qrn) for qrn in qp.get_quantum_register_names()]
    crs = [qp.get_classical_register(crn) for crn in qp.get_classical_register_names()]
    qc_FTv2 = qp.create_circuit("e|00>FTv2",qrs,crs)
    qc_FTv2.h(qrs[qri][3])
    qc_FTv2.cx(qrs[qri][3],qrs[qri][2])
    qc_FTv2.h(qrs[qri][2])
    qc_FTv2.h(qrs[qri][3])
    qc_FTv2.cx(qrs[qri][2],qrs[qri][1])
    qc_FTv2.cx(qrs[qri][3],qrs[qri][4])
    qc_FTv2.h(qrs[qri][4])
    qc_FTv2.extend(swap_circuit([2,4],qp))
    qc_FTv2.cx(qrs[qri][2],qrs[qri][0])
    qc_FTv2.cx(qrs[qri][1],qrs[qri][0])
    qc_FTv2.h(qrs[qri][4])
    #qc_FTv2.measure(qrs[qri][0],crs[cri][0])
    return qc_FTv2
    
def encoded_00_prep_NFTv2(qp, qri=0, cri=0):
    qrs = [qp.get_quantum_register(qrn) for qrn in qp.get_quantum_register_names()]
    crs = [qp.get_classical_register(crn) for crn in qp.get_classical_register_names()]
    qc_NFTv2 = qp.create_circuit("e|00>NFTv2",qrs,crs)
    qc_NFTv2.h(qrs[qri][2])
    qc_NFTv2.h(qrs[qri][3])
    qc_NFTv2.cx(qrs[qri][3],qrs[qri][4])
    qc_NFTv2.h(qrs[qri][4])
    qc_NFTv2.cx(qrs[qri][2],qrs[qri][4])
    qc_NFTv2.h(qrs[qri][4])
    qc_NFTv2.extend(swap_circuit([2,1],qp))
    qc_NFTv2.cx(qrs[qri][3],qrs[qri][2])
    qc_NFTv2.cx(qrs[qri][2],qrs[qri][0])
    qc_NFTv2.h(qrs[qri][0])
    qc_NFTv2.cx(qrs[qri][1],qrs[qri][0])
    qc_NFTv2.h(qrs[qri][0])
    qc_NFTv2.h(qrs[qri][1])
    #qc_NFTv2.measure(qrs[qri][0],crs[cri][0])
    return qc_NFTv2

def encoded_0p_prep(qp, qri=0, cri=0):
    qrs = [qp.get_quantum_register(qrn) for qrn in qp.get_quantum_register_names()]
    crs = [qp.get_classical_register(crn) for crn in qp.get_classical_register_names()]
    qc_0p = qp.create_circuit("e|0+>",qrs,crs)
    qc_0p.h(qrs[qri][1])
    qc_0p.h(qrs[qri][3])
    qc_0p.cx(qrs[qri][3],qrs[qri][2])
    qc_0p.extend(swap_circuit([2,1],qp))
    qc_0p.cx(qrs[qri][2],qrs[qri][4])
    return qc_0p
    
def encoded_2cat_prep(qp, qri=0, cri=0):
    qrs = [qp.get_quantum_register(qrn) for qrn in qp.get_quantum_register_names()]
    crs = [qp.get_classical_register(crn) for crn in qp.get_classical_register_names()]
    qc_2cat = qp.create_circuit("e|00>+|11>",qrs,crs)
    qc_2cat.h(qrs[qri][2])
    qc_2cat.h(qrs[qri][3])
    qc_2cat.cx(qrs[qri][2],qrs[qri][1])
    qc_2cat.cx(qrs[qri][3],qrs[qri][4])
    return qc_2cat
    
    
# The bare preparations
#######################
def bare_00_prep(pair, qp, qri=0, cri=0):
    qrs = [qp.get_quantum_register(qrn) for qrn in qp.get_quantum_register_names()]
    crs = [qp.get_classical_register(crn) for crn in qp.get_classical_register_names()]
    qcircuit_bare_00 = qp.create_circuit("b|00>"+str(pair),qrs,crs)
    return qcircuit_bare_00

def bare_0p_prep(pair, qp, qri=0, cri=0):
    qrs = [qp.get_quantum_register(qrn) for qrn in qp.get_quantum_register_names()]
    crs = [qp.get_classical_register(crn) for crn in qp.get_classical_register_names()]
    qcircuit_bare_0p = qp.create_circuit("b|0+>"+str(pair),qrs,crs)
    qcircuit_bare_0p.h(qrs[qri][pair[1]])
    return qcircuit_bare_0p

def bare_2cat_prep(pair, qp, qri=0, cri=0):
    qrs = [qp.get_quantum_register(qrn) for qrn in qp.get_quantum_register_names()]
    crs = [qp.get_classical_register(crn) for crn in qp.get_classical_register_names()]
    qcircuit_bare_2cat = qp.create_circuit("b|00>+|11>"+str(pair),qrs,crs)
    qcircuit_bare_2cat.h(qrs[qri][pair[0]])
    qcircuit_bare_2cat.cx(qrs[qri][pair[0]],qrs[qri][pair[1]])
    return qcircuit_bare_2cat

# The encoded gates
###################
def encoded_X1_circuit(mapping, qp, qri=0, cri=0):
    qrs = [qp.get_quantum_register(qrn) for qrn in qp.get_quantum_register_names()]
    crs = [qp.get_classical_register(crn) for crn in qp.get_classical_register_names()]
    qcircuit_encoded_X1 = qp.create_circuit("eX1",qrs,crs)
    qcircuit_encoded_X1.x(qrs[qri][mapping[0]])
    qcircuit_encoded_X1.x(qrs[qri][mapping[1]])
    return qcircuit_encoded_X1

def encoded_X2_circuit(mapping, qp, qri=0, cri=0):
    qrs = [qp.get_quantum_register(qrn) for qrn in qp.get_quantum_register_names()]
    crs = [qp.get_classical_register(crn) for crn in qp.get_classical_register_names()]
    qcircuit_encoded_X2 = qp.create_circuit("eX2",qrs,crs)
    qcircuit_encoded_X2.x(qrs[qri][mapping[0]])
    qcircuit_encoded_X2.x(qrs[qri][mapping[2]])
    return qcircuit_encoded_X2

def encoded_Z1_circuit(mapping, qp, qri=0, cri=0):
    qrs = [qp.get_quantum_register(qrn) for qrn in qp.get_quantum_register_names()]
    crs = [qp.get_classical_register(crn) for crn in qp.get_classical_register_names()]
    qcircuit_encoded_Z1 = qp.create_circuit("eZ1",qrs,crs)
    qcircuit_encoded_Z1.z(qrs[qri][mapping[1]])
    qcircuit_encoded_Z1.z(qrs[qri][mapping[3]])
    return qcircuit_encoded_Z1

def encoded_Z2_circuit(mapping, qp, qri=0, cri=0):
    qrs = [qp.get_quantum_register(qrn) for qrn in qp.get_quantum_register_names()]
    crs = [qp.get_classical_register(crn) for crn in qp.get_classical_register_names()]
    qcircuit_encoded_Z2 = qp.create_circuit("eZ2",qrs,crs)
    qcircuit_encoded_Z2.z(qrs[qri][mapping[2]])
    qcircuit_encoded_Z2.z(qrs[qri][mapping[3]])
    return qcircuit_encoded_Z2

def encoded_CZ_circuit(mapping, qp, qri=0, cri=0):
    qrs = [qp.get_quantum_register(qrn) for qrn in qp.get_quantum_register_names()]
    crs = [qp.get_classical_register(crn) for crn in qp.get_classical_register_names()]
    qcircuit_encoded_CZ = qp.create_circuit("eCZ",qrs,crs)
    qcircuit_encoded_CZ.s(qrs[qri][mapping[0]])
    qcircuit_encoded_CZ.s(qrs[qri][mapping[1]])
    qcircuit_encoded_CZ.s(qrs[qri][mapping[2]])
    qcircuit_encoded_CZ.s(qrs[qri][mapping[3]])
    return qcircuit_encoded_CZ

def encoded_HHS_circuit(mapping, qp, qri=0, cri=0):
    qrs = [qp.get_quantum_register(qrn) for qrn in qp.get_quantum_register_names()]
    crs = [qp.get_classical_register(crn) for crn in qp.get_classical_register_names()]
    qcircuit_encoded_HHS = qp.create_circuit("eHHS",qrs,crs)
    qcircuit_encoded_HHS.h(qrs[qri][mapping[0]])
    qcircuit_encoded_HHS.h(qrs[qri][mapping[1]])
    qcircuit_encoded_HHS.h(qrs[qri][mapping[2]])
    qcircuit_encoded_HHS.h(qrs[qri][mapping[3]])
    return qcircuit_encoded_HHS

# The bare gates
################
def bare_X1_circuit(pair, qp, qri=0, cri=0):
    qrs = [qp.get_quantum_register(qrn) for qrn in qp.get_quantum_register_names()]
    crs = [qp.get_classical_register(crn) for crn in qp.get_classical_register_names()]
    qcircuit_bare_X1 = qp.create_circuit("bX1"+str(pair),qrs,crs)
    qcircuit_bare_X1.x(qrs[qri][pair[0]])
    return qcircuit_bare_X1

def bare_X2_circuit(pair, qp, qri=0, cri=0):
    qrs = [qp.get_quantum_register(qrn) for qrn in qp.get_quantum_register_names()]
    crs = [qp.get_classical_register(crn) for crn in qp.get_classical_register_names()]
    qcircuit_bare_X2 = qp.create_circuit("bX2"+str(pair),qrs,crs)
    qcircuit_bare_X2.x(qrs[qri][pair[1]])
    return qcircuit_bare_X2

def bare_Z1_circuit(pair, qp, qri=0, cri=0):
    qrs = [qp.get_quantum_register(qrn) for qrn in qp.get_quantum_register_names()]
    crs = [qp.get_classical_register(crn) for crn in qp.get_classical_register_names()]
    qcircuit_bare_Z1 = qp.create_circuit("bZ1"+str(pair),qrs,crs)
    qcircuit_bare_Z1.z(qrs[qri][pair[1]])
    return qcircuit_bare_Z1

def bare_Z2_circuit(pair, qp, qri=0, cri=0):
    qrs = [qp.get_quantum_register(qrn) for qrn in qp.get_quantum_register_names()]
    crs = [qp.get_classical_register(crn) for crn in qp.get_classical_register_names()]
    qcircuit_bare_Z2 = qp.create_circuit("bZ2"+str(pair),qrs,crs)
    qcircuit_bare_Z2.z(qrs[qri][pair[1]])
    return qcircuit_bare_Z2

def bare_CZ_circuit(pair, qp, qri=0, cri=0):
    qrs = [qp.get_quantum_register(qrn) for qrn in qp.get_quantum_register_names()]
    crs = [qp.get_classical_register(crn) for crn in qp.get_classical_register_names()]
    qcircuit_bare_CZ = qp.create_circuit("bCZ"+str(pair),qrs,crs)
    qcircuit_bare_CZ.h(qrs[qri][pair[1]])
    qcircuit_bare_CZ.cx(qrs[qri][pair[0]],qrs[0][pair[1]])
    qcircuit_bare_CZ.h(qrs[qri][pair[1]])
    return qcircuit_bare_CZ

def bare_HHS_circuit(pair, qp, qri=0, cri=0):
    qrs = [qp.get_quantum_register(qrn) for qrn in qp.get_quantum_register_names()]
    crs = [qp.get_classical_register(crn) for crn in qp.get_classical_register_names()]
    qcircuit_bare_HHS = qp.create_circuit("bHHS"+str(pair),qrs,crs)
    qcircuit_bare_HHS.h(qrs[qri][pair[0]])
    qcircuit_bare_HHS.h(qrs[qri][pair[1]])
    return qcircuit_bare_HHS

# The dictionaries for all circuits
###################################

DICT_ENCODED = dict(zip(
                        ['eX1','eX2','eZ1','eZ2','eHHS','eCZ','e|00>FTv1','e|00>FTv2','e|00>NFTv1','e|00>NFTv2','e|0+>','e|00>+|11>'],
                                 [encoded_X1_circuit,
                                  encoded_X2_circuit,
                                  encoded_Z1_circuit,
                                  encoded_Z2_circuit,
                                  encoded_HHS_circuit,
                                  encoded_CZ_circuit,
                                  encoded_00_prep_FTv1,
                                  encoded_00_prep_FTv2,
                                  encoded_00_prep_NFTv1,
                                  encoded_00_prep_NFTv2,
                                  encoded_0p_prep,
                                  encoded_2cat_prep]))

DICT_BARE = dict(zip(['bX1','bX2','bZ1','bZ2','bHHS','bCZ','b|00>','b|0+>','b|00>+|11>'],
                              [bare_X1_circuit,
                               bare_X2_circuit,
                               bare_Z1_circuit,
                               bare_Z2_circuit,
                               bare_HHS_circuit,
                               bare_CZ_circuit,
                               bare_00_prep,
                               bare_0p_prep,
                               bare_2cat_prep]))


# The circuits for the experiment with input state and output distribution
##########################################################################
CIRCUITS = [[['X1', 'HHS', 'CZ', 'X2'], '|00>', [0.25, 0.25, 0.25, 0.25]],
            [['HHS', 'Z1', 'CZ'], '|00>', [0.25, 0.25, 0.25, 0.25]],
            [['HHS', 'Z1', 'Z2'], '|00>', [0.25, 0.25, 0.25, 0.25]],
            [['HHS', 'Z2', 'CZ'], '|00>', [0.25, 0.25, 0.25, 0.25]],
            [['Z2', 'X2'], '|00>+|11>', [0, .5, .5, 0]],
            [['X1', 'Z2'], '|0+>', [0, 0, .5, .5]],
            [['HHS', 'Z1'], '|00>', [0.25, 0.25, 0.25, 0.25]],
            [['HHS', 'CZ'], '|00>', [0.25, 0.25, 0.25, 0.25]],
            [['X1', 'X2'], '|00>', [0, 0, 0, 1]],
            [['HHS', 'Z2'], '|00>', [0.25, 0.25, 0.25, 0.25]],
            [['X1'], '|00>+|11>', [0, .5, .5, 0]],
            [['X1'], '|0+>', [0, 0, .5, .5]],
            [['HHS'], '|00>', [0.25, 0.25, 0.25, 0.25]],
            [['Z2'], '|00>+|11>', [.5, 0, 0, .5]],
            [['Z2'], '|0+>', [.5, .5, 0, 0]],
            [['X1'], '|00>', [0, 0, 1, 0]],
            [['X2'], '|00>', [0, 1, 0, 0]],
            [[], '|00>+|11>', [.5, 0, 0, .5]],
            [[], '|0+>', [.5, .5, 0, 0]],
            [[], '|00>', [1, 0, 0, 0]]]

# The names of the different versions for encoding |00> and the chosen mapping
##############################################################################
ENCODED_VERSION_LIST = ['FTv1', 'FTv2', 'NFTv1', 'NFTv2']
MAPPING = [3,2,1,4]

# Function that assembles all circuits within a given QuantumProgram module
###########################################################################

def all_circuits(qp, possible_pairs, mapping=MAPPING, circuits=CIRCUITS, dict_bare=DICT_BARE, dict_encoded=DICT_ENCODED, encoded_version_list=ENCODED_VERSION_LIST):
    qrs = [qp.get_quantum_register(qrn) for qrn in qp.get_quantum_register_names()]
    crs = [qp.get_classical_register(crn) for crn in qp.get_classical_register_names()]
    circuit_names = []
    for lc in circuits:
        for pair in possible_pairs:
            qcirc = qp.create_circuit('b'+'-'.join(reversed(lc[0]))+lc[1]+str(pair),qrs,crs)
            circuit_names.append('b'+'-'.join(reversed(lc[0]))+lc[1]+str(pair))
            qcirc.extend(dict_bare['b'+lc[1]](pair,qp))
            for g in lc[0]:
                qcirc.extend(dict_bare['b'+g](pair,qp))
            qcirc.extend(measure_all(qp))
        if lc[1]=='|00>':
            for v in encoded_version_list:
                qcirc = qp.create_circuit('e'+'-'.join(reversed(lc[0]))+lc[1]+v,qrs,crs)
                circuit_names.append('e'+'-'.join(reversed(lc[0]))+lc[1]+v)
                qcirc.extend(dict_encoded['e'+lc[1]+v](qp))
                for g in lc[0]:
                    qcirc.extend(dict_encoded['e'+g](mapping,qp))
                qcirc.extend(measure_all(qp))
        else:
            qcirc = qp.create_circuit('e'+'-'.join(reversed(lc[0]))+lc[1],qrs,crs)
            circuit_names.append('e'+'-'.join(reversed(lc[0]))+lc[1])
            qcirc.extend(dict_encoded['e'+lc[1]](qp))
            for g in lc[0]:
                qcirc.extend(dict_encoded['e'+g](mapping,qp))
            qcirc.extend(measure_all(qp))
    return circuit_names
            


# Function that creates all the qasm codes and misc information about the circuits to be run
def create_all_circuits(cp):
    
    # The circuits for the experiment with input state and output distribution
    circuits = [[['X1', 'HHS', 'CZ', 'X2'], '|00>', [0.25, 0.25, 0.25, 0.25]],
                [['HHS', 'Z1', 'CZ'], '|00>', [0.25, 0.25, 0.25, 0.25]],
                [['HHS', 'Z1', 'Z2'], '|00>', [0.25, 0.25, 0.25, 0.25]],
                [['HHS', 'Z2', 'CZ'], '|00>', [0.25, 0.25, 0.25, 0.25]],
                [['Z2', 'X2'], '|00>+|11>', [0, .5, .5, 0]],
                [['X1', 'Z2'], '|0+>', [0, 0, .5, .5]],
                [['HHS', 'Z1'], '|00>', [0.25, 0.25, 0.25, 0.25]],
                [['HHS', 'CZ'], '|00>', [0.25, 0.25, 0.25, 0.25]],
                [['X1', 'X2'], '|00>', [0, 0, 0, 1]],
                [['HHS', 'Z2'], '|00>', [0.25, 0.25, 0.25, 0.25]],
                [['X1'], '|00>+|11>', [0, .5, .5, 0]],
                [['X1'], '|0+>', [0, 0, .5, .5]],
                [['HHS'], '|00>', [0.25, 0.25, 0.25, 0.25]],
                [['Z2'], '|00>+|11>', [.5, 0, 0, .5]],
                [['Z2'], '|0+>', [.5, .5, 0, 0]],
                [['X1'], '|00>', [0, 0, 1, 0]],
                [['X2'], '|00>', [0, 1, 0, 0]],
                [[], '|00>+|11>', [.5, 0, 0, .5]],
                [[], '|0+>', [.5, .5, 0, 0]],
                [[], '|00>', [1, 0, 0, 0]]]

    # Definition of the possible gates to perform and their possible qasm implementations
    gates = ['X1','X2','Z1','Z2','HHS','CZ']

    # Count of 1- and 2-qubit physical gates
    gate_count_bare_1q = [1,1,1,1,2,2]
    gate_count_bare_2q = [0,0,0,0,0,1]

    gate_count_encoded_1q = [2,2,2,2,4,4]
    gate_count_encoded_2q = [0,0,0,0,0,0]

    # Doing the SWAP in software require swapping X1<->X2 and Z1<->Z2 depending on how many SWAPs have been done before
    indices = [[0,1,2,3,4,5],[1,0,3,2,4,5]];

    # QASM code for the gates in their bare version
    gates_qasm = [['x q['+str(cp[0])+'];\n'],
                  ['x q['+str(cp[1])+'];\n'],
                  ['z q['+str(cp[0])+'];\n'],
                  ['z q['+str(cp[1])+'];\n'],
                  ['h q['+str(cp[0])+'];\nh q['+str(cp[1])+'];\n'],
                  ['h q['+str(cp[1])+'];\ncx q['+str(cp[0])+'], q['+str(cp[1])+'];\nh q['+str(cp[1])+'];\n']]

    # QASM code for the gates in their encoded version
    gates_qasm_encoded = [['x q[1];\nx q[4];\n','x q[2];\nx q[3];\n'],
                          ['x q[1];\nx q[3];\n','x q[2];\nx q[4];\n'],
                          ['z q[1];\nz q[3];\n','z q[2];\nz q[4];\n'],
                          ['z q[1];\nz q[4];\n','z q[2];\nz q[3];\n'],
                          ['h q[1];\nh q[2];\nh q[3];\nh q[4];\n'],
                          ['s q[1];\ns q[2];\ns q[3];\ns q[4];\n']]

    #names of input states
    state_names = ['|00>','|0+>','|00>+|11>']

    # Definition of the pre- and post- circuits
    code_heading = """
OPENQASM 2.0;
include "qelib1.inc";
qreg q[5];
creg c[5];
"""

    bare_pre_circuit = ["","",""]
    bare_pre_circuit_count_1q = [0,1,1]
    bare_pre_circuit_count_2q = [0,0,1]
    
    bare_pre_circuit[1] = """
h q["""+str(cp[1])+"""];
barrier q["""+str(cp[0])+"""],q["""+str(cp[1])+"""];
"""
    
    bare_pre_circuit[2] = """
h q["""+str(cp[0])+"""];
cx q["""+str(cp[0])+"""], q["""+str(cp[1])+"""];
barrier q["""+str(cp[0])+"""],q["""+str(cp[1])+"""];
"""
    
    bare_post_circuit = """
measure q["""+str(cp[0])+"""] -> c["""+str(cp[0])+"""];
measure q["""+str(cp[1])+"""] -> c["""+str(cp[1])+"""];
"""
    
    encoded_pre_circuit = ["","",""]
    encoded_pre_circuit_count_1q = [11,6,2]
    encoded_pre_circuit_count_2q = [8,5,2]
    
    encoded_pre_circuit[0] = """
h q[3];
cx q[3],q[4];
cx q[4],q[2];
cx q[1],q[2];
h q[1];
h q[2];
cx q[1],q[2];
h q[1];
h q[2];
cx q[1],q[2];
cx q[3],q[2];
h q[0];
h q[1];
h q[2];
cx q[0],q[1];
cx q[0],q[2];
h q[0];
h q[1];
h q[2];
barrier q[0],q[1],q[2],q[3],q[4];
"""
    
    encoded_pre_circuit[1] = """
h q[3];
cx q[3],q[2];
cx q[1],q[2];
h q[1];
h q[2];
cx q[1],q[2];
h q[1];
h q[2];
cx q[1],q[2];
h q[4];
cx q[4],q[2];
barrier q[0],q[1],q[2],q[3],q[4];
"""
    
    encoded_pre_circuit[2] = """
h q[3];
cx q[3],q[4];
h q[1];
cx q[1],q[2];
barrier q[0],q[1],q[2],q[3],q[4];
"""
   
    encoded_post_circuit = """
measure q[0] -> c[0];
measure q[1] -> c[1];
measure q[2] -> c[2];
measure q[3] -> c[3];
measure q[4] -> c[4];
"""
    
    #For each circuit, concatenating the state preparation code, the circuit code and the measurment code
    #Adding some misc information about the circuits on the way.
    circuit_list = []
    
    for c in circuits:
        idx = 0
        qasm_bare = code_heading + bare_pre_circuit[state_names.index(c[1])]
        qasm_encoded = code_heading + encoded_pre_circuit[state_names.index(c[1])]
        circuit_gate_count_bare_1q = bare_pre_circuit_count_1q[state_names.index(c[1])]
        circuit_gate_count_bare_2q = bare_pre_circuit_count_2q[state_names.index(c[1])]
        circuit_gate_count_encoded_1q = encoded_pre_circuit_count_1q[state_names.index(c[1])]
        circuit_gate_count_encoded_2q = encoded_pre_circuit_count_2q[state_names.index(c[1])]
        for g in c[0]:
            k = gates.index(g)
            if g=='HHS':
                idx = (idx + 1) % 2
            l = len(gates_qasm[k])
            qasm_bare += gates_qasm[indices[idx][k]][random.randrange(0,l)]
            l = len(gates_qasm_encoded[k])
            qasm_encoded += gates_qasm_encoded[k][random.randrange(0,l)]
            circuit_gate_count_bare_1q += gate_count_bare_1q[k]
            circuit_gate_count_bare_2q += gate_count_bare_2q[k]
            circuit_gate_count_encoded_1q += gate_count_encoded_1q[k]
            circuit_gate_count_encoded_2q += gate_count_encoded_2q[k]
        
        circuit_list.append({'circuit_desc':" ".join(c[0]),
                             'qasm_bare':qasm_bare + bare_post_circuit,
                             'qasm_encoded':qasm_encoded + encoded_post_circuit,
                             'nH':idx,
                             'gate_count_bare':(circuit_gate_count_bare_1q,circuit_gate_count_bare_2q),
                             'gate_count_encoded':(circuit_gate_count_encoded_1q,circuit_gate_count_encoded_2q),
                             'input_state':c[1],
                             'output_distribution':c[2]})
    return circuit_list

# Function that analyse one run (8192 shots) of one circuit in its bare version
def analysis_one_bare_expe(expe_bare, circuit, cpp):
    
    raw_labels_list = [['0','0','0','0','0'],['0','0','0','0','0'],['0','0','0','0','0'],['0','0','0','0','0']];
    raw_labels_list[1][4-cpp[1]] = '1';
    raw_labels_list[2][4-cpp[0]] = '1';
    raw_labels_list[3][4-cpp[1]] = '1';
    raw_labels_list[3][4-cpp[0]] = '1';
    
    raw_labels = [''.join(rll) for rll in raw_labels_list];
    
    data_bare = expe_bare['result']['data']['counts']
    
    labels = ['00','01','10','11']
    labels_bare = sorted(data_bare)
    
    values_bare = np.array([0,0,0,0],dtype=float)
    total_valid_bare = 0
    total_err_bare = 0
    
    for label in labels_bare:
        if label==raw_labels[0]:
            values_bare[0] += data_bare[label]
            total_valid_bare += data_bare[label]
        elif label==raw_labels[1]:
            if circuit['nH']==0:
                values_bare[1] += data_bare[label]
            else:
                values_bare[2] += data_bare[label]
            total_valid_bare += data_bare[label]
        elif label==raw_labels[2]:
            if circuit['nH']==0:
                values_bare[2] += data_bare[label]
            else:
                values_bare[1] += data_bare[label]
            total_valid_bare += data_bare[label]
        elif label==raw_labels[3]:
            values_bare[3] += data_bare[label]
            total_valid_bare += data_bare[label]
        else:
            total_err_bare += data_bare[label]
        
    values_expectation = np.array(circuit['output_distribution'])
    
    stand_dev = np.sqrt(values_bare/total_valid_bare*(1-values_bare/total_valid_bare)/total_valid_bare)
    
    post_selected_ratio_bare = total_valid_bare/(total_valid_bare+total_err_bare)
    
    stat_dist_bare = .5*sum(np.abs(values_bare/total_valid_bare-values_expectation))
    
    stat_dist_stand_dev = 0
    for j in range(0,4):
        stat_dist_stand_dev += values_bare[j]/total_valid_bare*(1-values_bare[j]/total_valid_bare)/(4*total_valid_bare)
    for i in range(0,4):
        for j in range(0,4):
            if i!=j:
                stat_dist_stand_dev += values_bare[i]/total_valid_bare*values_bare[j]/total_valid_bare/(4*total_valid_bare)

    stat_dist_stand_dev = np.sqrt(stat_dist_stand_dev)
    
    return {'circuit_desc':circuit['circuit_desc'],
            'version':'bare',
            'gate_count':sum(circuit['gate_count_bare']),
            'input_state':circuit['input_state'],
            'labels':labels,
            'values':values_bare,
            'total_valid':total_valid_bare,
            'total_err':total_err_bare,
            'output_distribution':values_expectation,
            'stand_dev':stand_dev,
            'post_selected_ratio':post_selected_ratio_bare,
            'stat_dist':stat_dist_bare,
            'stat_dist_stand_dev':stat_dist_stand_dev}  

# Function that analyse one run (8192 shots) of one circuit in its encoded version
def analysis_one_encoded_expe(expe_encoded, circuit):

    data_encoded = expe_encoded['result']['data']['counts']
    
    labels = ['00','01','10','11']
    labels_encoded = sorted(data_encoded)
    
    values_encoded = np.array([0,0,0,0],dtype=float)
    total_valid_encoded = 0
    total_err_encoded = 0
    
    for label in labels_encoded:
        if label=='00000' or label=='11110':
            values_encoded[0] += data_encoded[label]
            total_valid_encoded += data_encoded[label]
        elif label=='01010' or label=='10100':
            values_encoded[1] += data_encoded[label]
            total_valid_encoded += data_encoded[label]
        elif label=='10010' or label=='01100':
            values_encoded[2] += data_encoded[label]
            total_valid_encoded += data_encoded[label]
        elif label=='11000' or label=='00110':
            values_encoded[3] += data_encoded[label]
            total_valid_encoded += data_encoded[label]
        else:
            total_err_encoded += data_encoded[label]

    values_expectation = np.array(circuit['output_distribution'])
    
    stand_dev = np.sqrt(values_encoded/total_valid_encoded*(1-values_encoded/total_valid_encoded)/total_valid_encoded)
    
    post_selected_ratio_encoded = total_valid_encoded/(total_valid_encoded+total_err_encoded)

    stat_dist_encoded = .5*sum(np.abs(values_encoded/total_valid_encoded-values_expectation))

    stat_dist_stand_dev = 0
    for j in range(0,4):
        stat_dist_stand_dev += values_encoded[j]/total_valid_encoded*(1-values_encoded[j]/total_valid_encoded)/(4*total_valid_encoded)
    for i in range(0,4):
        for j in range(0,4):
            if i!=j:
                stat_dist_stand_dev += values_encoded[i]/total_valid_encoded*values_encoded[j]/total_valid_encoded/(4*total_valid_encoded)

    stat_dist_stand_dev = np.sqrt(stat_dist_stand_dev)
    
    return {'circuit_desc':circuit['circuit_desc'],
            'version':'encoded',
            'gate_count':sum(circuit['gate_count_encoded']), 
            'input_state':circuit['input_state'],
            'labels':labels,
            'values':values_encoded,
            'total_valid':total_valid_encoded,
            'total_err':total_err_encoded,
            'output_distribution':values_expectation,
            'stand_dev':stand_dev,
            'post_selected_ratio':post_selected_ratio_encoded,
            'stat_dist':stat_dist_encoded,
            'stat_dist_stand_dev':stat_dist_stand_dev}

# Plotting one bare run next to one encoded run with the expected output distribution
def plot_one_expe(analysed_data1,analysed_data2,confidence):
    N = 4;
    ind = np.arange(N)
    
    width = 0.25
    
    fig, ax = plt.subplots()
    hist1 = ax.bar(ind, analysed_data1['values']/analysed_data1['total_valid'], width, color='r', yerr=analysed_data1['stand_dev']*norm.ppf(1/2+confidence/2),label=analysed_data1['version']+' (stat dist : '+str(analysed_data1['stat_dist'])+')')
    hist2 = ax.bar(ind+width, analysed_data2['values']/analysed_data2['total_valid'], width, color='b', yerr=analysed_data2['stand_dev']*norm.ppf(1/2+confidence/2),label=analysed_data2['version']+' (stat dist : '+str(analysed_data2['stat_dist'])+')')
    hist3 = ax.bar(ind+2*width, analysed_data1['output_distribution'], width, color='g',label='Expectation')
    
    ax.set_ylabel('Frequencies')
    ax.set_title('Performance on the circuit : '+analysed_data1['circuit_desc']
                 +' (ratio of post-selection : '+str(analysed_data2['post_selected_ratio'])+')')
    ax.set_xticks(ind + width)
    ax.set_xticklabels(analysed_data1['labels'])
    
    ax.legend(loc='lower left', bbox_to_anchor=(1, 0))
    
    plt.show();

    
# Function that analyse all the runs per circuit
def analyse_all_expe(listlist_bare, listlist_encoded, confidence):
    
    all_expe = []
    
    for expe in range(0,20):
        bare_runs = [e[expe] for e in listlist_bare]
        encoded_runs = [e[expe] for e in listlist_encoded]
        
        bare_mean_stat_dist = 0
        encoded_mean_stat_dist = 0
        
        bare_std_dev = 0
        encoded_std_dev = 0
        
        for r in bare_runs:
            bare_mean_stat_dist += r['stat_dist']/len(bare_runs)
            
        for r in encoded_runs:
            encoded_mean_stat_dist += r['stat_dist']/len(encoded_runs)
            
        for r in bare_runs:
            bare_std_dev += (r['stat_dist']-bare_mean_stat_dist)**2/(len(bare_runs)-1)
        bare_std_dev = np.sqrt(bare_std_dev)
        ct = t.interval(confidence, len(bare_runs)-1, loc=0, scale=1)[1]
        bare_confi = ct*bare_std_dev/np.sqrt(len(bare_runs))
            
        for r in encoded_runs:
            encoded_std_dev += (r['stat_dist']-encoded_mean_stat_dist)**2/(len(encoded_runs)-1)
        encoded_std_dev = np.sqrt(encoded_std_dev)    
        ct = t.interval(confidence, len(encoded_runs)-1, loc=0, scale=1)[1]
        encoded_confi = ct*encoded_std_dev/np.sqrt(len(encoded_runs))
            
        all_expe.append({'circuit_desc':bare_runs[0]['circuit_desc'],
                         'gate_count_bare':bare_runs[0]['gate_count'],
                         'gate_count_encoded':encoded_runs[0]['gate_count'],
                         'input_state':bare_runs[0]['input_state'],
                         'output_distribution':bare_runs[0]['output_distribution'],
                         'bare_mean_stat_dist':bare_mean_stat_dist,
                         'encoded_mean_stat_dist':encoded_mean_stat_dist,
                         'bare_std_dev':bare_std_dev,
                         'encoded_std_dev':encoded_std_dev,
                         'bare_conf_int':bare_confi,
                         'encoded_conf_int':encoded_confi,
                         'confidence':confidence})
    return all_expe

# Plotting the difference in statistical distance between encoded and bare version for all circuits
def plot_stat_dist(all_expe):
    
    ng = np.array([e['gate_count_bare'] for e in all_expe])
    sdb = np.array([e['bare_mean_stat_dist'] for e in all_expe])
    sde = np.array([e['encoded_mean_stat_dist'] for e in all_expe])
    cib = np.array([e['bare_conf_int'] for e in all_expe])
    cie = np.array([e['encoded_conf_int'] for e in all_expe])
    
    fig, ax = plt.subplots();
    
    ax.errorbar(ng, sde-sdb, yerr=cib+cie, fmt='rx', label='Difference')
    
    ax.set_ylabel('Difference')
    ax.set_xlabel('Number of gates in the bare circuit')
    ax.set_title('Statistical distances from the ideal distribution\ndepending on the number of gates in the bare circuit\nConfidence interval at '+str(all_expe[0]['confidence']*100)+'%')
    
    ax.legend(loc='lower left', bbox_to_anchor=(1, 0))
    plt.grid()
    plt.show()
