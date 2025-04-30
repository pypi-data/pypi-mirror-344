import sys
import pandas as pd
import numpy as np
from TORCphysics import utils, Enzyme, Site, Environment
from unittest import TestCase
from TORCphysics import Circuit
import matplotlib.pyplot as plt

min_circuit_file = '../circuit_min-linear.csv'
complete_circuit_file = '../circuit_complete-linear.csv'
min_sites_file = '../sites_min-linear.csv'
complete_sites_file =  None #'..//sites_complete-linear.csv'
enzymes_filename = None
environment_filename = None #'environment.csv'
output_prefix = 'TORC_plasmid'
series = True
continuation = False

# Arange some needed params
dt = 1.0
final_time = 100 #2000
initial_time = 0
time = np.arange(initial_time, final_time + dt, dt)
frames = len(time)

# Build synthetic cases
# ----------------------------------------------------------------------------------------------------------------------

# Let's creat enzymes that act as boundaries
s0 = Site(site_type='EXT', name='EXT', start=1, end=5000, k_on=0.0)
extra_left = Enzyme(e_type='EXT', name='EXT_L', site=s0,
                    position=1, size=0, effective_size=0,
                    twist=0, superhelical=-0.06)
extra_right = Enzyme(e_type='EXT', name='EXT_R', site=s0,
                     position=5000, size=0, effective_size=0,
                     twist=0, superhelical=-0.06)

# First for the normal cases - (no modifications)
# ----------------------------------------------------------------------------------------------------------------------
# Our sites
min_lac1 = Site(site_type='lacOP', name='min_lac1', start=2057, end=0.0, k_on=0.0)
full_lac1 = Site(site_type='lacOP', name='full_lac1', start=2182, end=0.0, k_on=0.0)

min_PleuWT = Site(site_type='gene', name='min_PleuWT', start=2022, end=1260, k_on=0.0)
full_PleuWT = Site(site_type='gene', name='min_PleuWT', start=2088, end=1260, k_on=0.0)

# Environmentals
min_RNAP= Environment(e_type='RNAP', name='min_RNAP', site_list=[min_PleuWT], concentration=1.0,
                     size=30, effective_size=20, site_type='gene')
full_RNAP= Environment(e_type='RNAP', name='full_RNAP', site_list=[full_PleuWT], concentration=1.0,
                     size=30, effective_size=20, site_type='gene')

# Bound enzymes
bound_min_lac1 = Enzyme(e_type='lac', name='min_lac1', site=min_lac1, position=2057, size=16, effective_size=10,
                 twist=0, superhelical=-0.06)
bound_full_lac1 = Enzyme(e_type='lac', name='full_lac1', site=full_lac1, position=2182, size=16, effective_size=10,
                 twist=0, superhelical=-0.06)

# Build lists
min_enzyme_list = [extra_left, bound_min_lac1, extra_right]
full_enzyme_list = [extra_left, bound_full_lac1, extra_right]

# Let's test for the minimum
available = utils.check_site_availability(site=min_PleuWT, enzyme_list=min_enzyme_list, environmental=min_RNAP)

print('For the standard case - should not block the promoters')

if available:
    print('MinPleuWT available')
else:
    print('MinPleuWT not available')

# Let's test for the full
available = utils.check_site_availability(site=full_PleuWT, enzyme_list=full_enzyme_list, environmental=full_RNAP)

if available:
    print('Full PleuWT available')
else:
    print('Full PleuWT not available')


# For modified cases - we are looking for lacI to block the minimum PleuWT
# ----------------------------------------------------------------------------------------------------------------------
# Our sites - this ones should block the PleuWT for the minimum case
displacement = 16
min_blac1 = Site(site_type='lacOP', name='min_lac1', start=2057-displacement, end=0.0, k_on=0.0)
full_blac1 = Site(site_type='lacOP', name='full_lac1', start=2182-displacement, end=0.0, k_on=0.0)

# Bound lacs for each case
bound_min_blac1 = Enzyme(e_type='lac', name='min_lac1', site=min_lac1, position=2057-displacement, size=16, effective_size=10,
                 twist=0, superhelical=-0.06)
bound_full_blac1 = Enzyme(e_type='lac', name='full_lac1', site=full_lac1, position=2182-displacement, size=16, effective_size=10,
                 twist=0, superhelical=-0.06)

# Build lists
min_enzyme_list = [extra_left, bound_min_blac1, extra_right]
full_enzyme_list = [extra_left, bound_full_blac1, extra_right]

# Let's test for the minimum
available = utils.check_site_availability(site=min_PleuWT, enzyme_list=min_enzyme_list, environmental=min_RNAP)

print('For displacement - should block the Minimal promoter')
if available:
    print('MinPleuWT available')
else:
    print('MinPleuWT not available')

# Let's test for the full
available = utils.check_site_availability(site=full_PleuWT, enzyme_list=full_enzyme_list, environmental=full_RNAP)

if available:
    print('Full PleuWT available')
else:
    print('Full PleuWT not available')


# Now let's test the leaking
# ----------------------------------------------------------------------------------------------------------------------
# Define circuit
my_circuit = Circuit(complete_circuit_file, complete_sites_file, enzymes_filename, environment_filename,
                     output_prefix, frames, series, continuation, dt)
# Define bound lac
bound_lac = Enzyme(e_type='lac', name='full_lac1', site=full_lac1, position=2182-displacement, size=16, effective_size=10,
                 twist=0, superhelical=-0.06, effect_model_name='LacIPoissonBridging',
                   effect_model_oparams={'k_bridge_on': 0.05, 'k_bridge_off': 0.05, 'leakage':.1})

# Let's add the site and the bound lac
my_circuit.site_list.append(full_blac1)
my_circuit.enzyme_list.append(bound_lac)
my_circuit.sort_lists()

# Modify local superhelicity and update
my_circuit.enzyme_list[0].superhelical = -0.25
my_circuit.enzyme_list[1].superhelical = 0.01
my_circuit.update_twist()
my_circuit.update_supercoiling()
my_circuit.update_global_twist()
my_circuit.update_global_superhelical()

enzymes_df, sites_df, environmentals_df = my_circuit.run_return_dfs()

# Let's get global supercoiling
mask_circuit = sites_df['type'] == 'circuit'
global_superhelical = sites_df[mask_circuit]['superhelical'].to_numpy()

# Let's get supercoiling before and after lac
mask_left = enzymes_df['name'] == 'EXT_L'
mask_right = enzymes_df['name'] == bound_lac.name
left_superhelical = enzymes_df[mask_left]['superhelical'].to_numpy()
right_superhelical = enzymes_df[mask_right]['superhelical'].to_numpy()

fig, axs = plt.subplots(1, figsize=(6,3), tight_layout=True)

axs.plot(global_superhelical[1:], lw=3, color='black')
axs.plot(left_superhelical[1:], lw=2, color='blue')
axs.plot(right_superhelical[1:], lw=1,color='red')

axs.grid(True)
axs.set_xlabel('time')
axs.set_ylabel('superhelical')
axs.set_ylim([-.25,.01])
plt.show()

sigma_dif = abs(global_superhelical[1] - global_superhelical[-1])
if sigma_dif < 0.000000001:
    print('Superhelical did not change, so model works as expected')
else:
    print('Superhelical changed, so model is not working')
