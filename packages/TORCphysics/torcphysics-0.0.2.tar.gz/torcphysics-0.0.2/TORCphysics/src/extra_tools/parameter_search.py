import numpy as np
import multiprocessing
import multiprocessing.pool
from TORCphysics import parallelization_tools as pt
from scipy.stats import ks_2samp

# The porpuse of this script is to help run calibration processes where we want to find optimum parametrizations
# that reproduce certain behaviours.

# Calibrate according rates given a reference system
def calibrate_w_rate(info_list, target_dict, n_simulations, additional_results=False):

    # Prepare variables
    objective=0.0
    n_systems = len(info_list)
    output_list = []  # Let's return it as a list as well

    # Create a multiprocessing pool
    pool = multiprocessing.Pool()

    # Run simulations
    # --------------------------------------------------------------
    # Go through each system, run simulations in parallel, collect outputs, repeat
    for i in range(n_systems):

        # This contains all the info we need to run the simulation and apply variations
        system = info_list[i]
        additional_dict = {}

        # Sort the processing info
        # --------------------------------------------------
        # Overall
        my_circuit = pt.load_circuit(system['global_conditions'])
        total_time = my_circuit.dt * my_circuit.frames
        # dt = my_circuit.dt
        # frames = my_circuit.frames

        # Sites - get sites that are not bare DNA or EXT
        target_sites = [site.name for site in my_circuit.site_list if 'DNA' not in site.site_type and 'EXT' not in site.site_type]
        # target_genes = [site.name for site in my_circuit.site_list if site.site_type == 'gene' ]
        target_genes = [site.name for site in my_circuit.site_list if 'gene' in site.site_type ]

        # Define x-axes
        # x_system = tct.get_interpolated_x(1, my_circuit.size, x_spacing=20)

        # We need a list of items, so the pool can pass each item to the function
        Items = []
        for simulation_number in range(n_simulations):
            g_dict = dict(system['global_conditions'])
            g_dict['n_simulations'] = simulation_number
            Item = {'global_conditions': g_dict, 'variations': system['variations']}
            Items.append(Item)

        # Run in parallel
        # ----------------------------
        # Run simulations in parallel within this subset
        pool_results = pool.map(pt.single_simulation_w_variations_return_dfs, Items)

        # TODO: We still need to calculate cross_correlations  and  KDEs?
        # Process transcripts - Serial
        # ----------------------------
        # Collect results (is it better to do it in serial or parallel? What causes more overhead?)
        transcript_list = []
        for result in pool_results:
            environmental_df = result['environmental_df']
            mask = environmental_df['name'] == target_dict['reporter']

            if len(environmental_df[mask]['concentration']) == 0:
                transcript = 0
            else:
                transcript = environmental_df[mask]['concentration'].iloc[-1]
            transcript_list.append(transcript)

            # sites_df = result['sites_df']
            # mask = sites_df['name'] == target_dict['reporter']
            # unbinding_event = sites_df[mask]['unbinding'].to_numpy()

            # Calculate number of transcripts produced by the reporter  (no need to do the rate as the time will be canceled out)
            # transcripts += np.sum(unbinding_event[:])

        # Convert to a NumPy arraypool_results
        transcripts_array = np.array(transcript_list)

        # Calculate mean and standard deviation
        mean_transcripts = np.mean(transcripts_array)
        std_transcripts = np.std(transcripts_array)

        transcripts = np.array([mean_transcripts, std_transcripts])

        system['transcripts'] = transcripts

        # --------------------------------------------------------------------
        # Here process additional stuff
        # --------------------------------------------------------------------
        if additional_results:   # Note I add it here to start giving shape to the code, in case in the future
                                 # I want to add the KDEs or the processing bit, so it can

            # Total transcripts
            additional_dict['transcripts'] = transcripts
            output_list.append(additional_dict)

            # System info
            output_list[i]['name'] = system['name']
            output_list[i]['despcription'] = system['description']
            output_list[i]['bacterium'] = system['bacterium']
            output_list[i]['promoter'] = system['promoter']
            output_list[i]['strain'] = system['strain']

            output_list[i]['reference'] = np.array([system['reference'], system['reference_std']])

            # Global sigma
            # --------------------------------------------------------------------
            global_superhelical = []
            for result in pool_results:
                 sites_df = result['sites_df']
                 mask_circuit = sites_df['type'] == 'circuit'
                 # Collect measurements
                 global_superhelical.append(sites_df[mask_circuit]['superhelical'].to_numpy())
            output_list[i]['global_superhelical'] = np.array(global_superhelical)

            # Get site related measurements: local supercoiling, correlations & positions
            # --------------------------------------------------------------------
            local_superhelical = {}
            for site_name in target_sites:
                local_superhelical[site_name] = []
                for result in pool_results:
                    sites_df = result['sites_df']
                    site_mask = sites_df['name'] == site_name

                    # Collect measurements
                    local_superhelical[site_name].append(sites_df[site_mask]['superhelical'].to_numpy())
                local_superhelical[site_name] = np.array(local_superhelical[site_name])
            output_list[i]['local_superhelical'] = local_superhelical

            # Get transcripts
            # --------------------------------------------------------------------
            # Collect results (is it better to do it in serial or parallel? What causes more overhead?)
            production_Rate = {}
            for gene_name in target_genes:
                production_Rate[gene_name] = []
                transcript_list = []
                for result in pool_results:
                    environmental_df = result['environmental_df']
                    mask = environmental_df['name'] == gene_name

                    if len(environmental_df[mask]['concentration']) == 0:
                        transcript = 0
                    else:
                        transcript = environmental_df[mask]['concentration'].iloc[-1]
                    transcript_list.append(transcript)
                expression_array = np.array(transcript_list)/total_time
                mean_expression = np.mean(expression_array)
                std_expression = np.std(expression_array)

                production_Rate[gene_name] = np.array([mean_expression, std_expression])
            output_list[i]['production_rate'] = production_Rate

    # Objective function part
    # --------------------------------------------------------------
    # We need to calculate the relative rate and add to the objective function
    ref_transcript = [d for d in info_list if d['name'] == target_dict['reference_system']][0]['transcripts'][0]

    if ref_transcript <= 0:
        objective += 100  #Something big because it'll give inf or NaN
        if additional_results:
            for i in range(n_systems):
                output_list[i]['objective'] = 0
                output_list[i]['relative_rate'] = 0
    else:
        for i in range(n_systems):
            system = info_list[i]
            relative_rate = system['transcripts']/ref_transcript
            system['relative_rate'] = relative_rate
            system_objective = (system['reference']-relative_rate[0])**2
            objective+= system_objective

            # Add values to additional outputs
            if additional_results:
                output_list[i]['objective'] = system_objective
                output_list[i]['relative_rate'] = relative_rate

    return objective, output_list

# Optimize given an empirical (experimental) distribution of relative rates according the Kolmogorov-Smirnov test
# Uses the scipy.stats ks_2samp function
def KS_calibrate_w_rate(info_list, target_dict, n_simulations, metric='pvalue', additional_results=False):

    # Prepare variables
    objective=0.0
    n_systems = len(info_list)
    output_list = []  # Let's return it as a list as well

    # Create a multiprocessing pool
    pool = multiprocessing.Pool()

    # Run simulations
    # --------------------------------------------------------------
    # Go through each system, run simulations in parallel, collect outputs, repeat
    for i in range(n_systems):

        # This contains all the info we need to run the simulation and apply variations
        system = info_list[i]
        additional_dict = {}

        # Sort the processing info
        # --------------------------------------------------
        # Overall
        my_circuit = pt.load_circuit(system['global_conditions'])
        total_time = my_circuit.dt * my_circuit.frames
        dt = my_circuit.dt
        frames = my_circuit.frames

        # Sites - get sites that are not bare DNA or EXT
        target_sites = [site.name for site in my_circuit.site_list if 'DNA' not in site.site_type and 'EXT' not in site.site_type]
        target_genes = [site.name for site in my_circuit.site_list if site.site_type == 'gene' ]

        # Define x-axes
        # x_system = tct.get_interpolated_x(1, my_circuit.size, x_spacing=20)

        # We need a list of items, so the pool can pass each item to the function
        Items = []
        for simulation_number in range(n_simulations):
            g_dict = dict(system['global_conditions'])
            g_dict['n_simulations'] = simulation_number
            Item = {'global_conditions': g_dict, 'variations': system['variations']}
            Items.append(Item)

        # Run in parallel
        # ----------------------------
        # Run simulations in parallel within this subset
        pool_results = pool.map(pt.single_simulation_w_variations_return_dfs, Items)

        # TODO: We still need to calculate cross_correlations  and  KDEs?
        # Process transcripts - Serial
        # ----------------------------
        # Collect results (is it better to do it in serial or parallel? What causes more overhead?)
        transcript_list = []
        for result in pool_results:
            environmental_df = result['environmental_df']
            mask = environmental_df['name'] == target_dict['reporter']

            if len(environmental_df[mask]['concentration']) == 0:
                transcript = 0
            else:
                transcript = environmental_df[mask]['concentration'].iloc[-1]
            transcript_list.append(transcript)

            # sites_df = result['sites_df']
            # mask = sites_df['name'] == target_dict['reporter']
            # unbinding_event = sites_df[mask]['unbinding'].to_numpy()

            # Calculate number of transcripts produced by the reporter  (no need to do the rate as the time will be canceled out)
            # transcripts += np.sum(unbinding_event[:])

        # Convert to a NumPy arraypool_results
        transcripts_array = np.array(transcript_list)

        system['transcripts'] = transcripts_array

        # --------------------------------------------------------------------
        # Here process additional stuff
        # --------------------------------------------------------------------
        if additional_results:   # Note I add it here to start giving shape to the code, in case in the future
                                 # I want to add the KDEs or the processing bit, so it can

            # Total transcripts
            additional_dict['transcripts'] = transcripts_array
            output_list.append(additional_dict)

            # System info
            output_list[i]['name'] = system['name']
            output_list[i]['despcription'] = system['description']
            output_list[i]['bacterium'] = system['bacterium']
            output_list[i]['promoter'] = system['promoter']
            output_list[i]['strain'] = system['strain']

            # This time is just the reference (it is a list of measurements rathre than a mean and std)
            output_list[i]['reference'] = system['reference'] #np.array([system['reference'], system['reference_std']])

            # Global sigma
            # --------------------------------------------------------------------
            global_superhelical = []
            for result in pool_results:
                 sites_df = result['sites_df']
                 mask_circuit = sites_df['type'] == 'circuit'
                 # Collect measurements
                 global_superhelical.append(sites_df[mask_circuit]['superhelical'].to_numpy())
            output_list[i]['global_superhelical'] = np.array(global_superhelical)

            # Get site related measurements: local supercoiling, correlations & positions
            # --------------------------------------------------------------------
            local_superhelical = {}
            for site_name in target_sites:
                local_superhelical[site_name] = []
                for result in pool_results:
                    sites_df = result['sites_df']
                    site_mask = sites_df['name'] == site_name

                    # Collect measurements
                    local_superhelical[site_name].append(sites_df[site_mask]['superhelical'].to_numpy())
                local_superhelical[site_name] = np.array(local_superhelical[site_name])
            output_list[i]['local_superhelical'] = local_superhelical

            # Get transcripts
            # --------------------------------------------------------------------
            # Collect results (is it better to do it in serial or parallel? What causes more overhead?)
            production_Rate = {}
            for gene_name in target_genes:
                production_Rate[gene_name] = []
                transcript_list = []
                for result in pool_results:
                    environmental_df = result['environmental_df']
                    mask = environmental_df['name'] == gene_name

                    if len(environmental_df[mask]['concentration']) == 0:
                        transcript = 0
                    else:
                        transcript = environmental_df[mask]['concentration'].iloc[-1]
                    transcript_list.append(transcript)
                expression_array = np.array(transcript_list)/total_time
                mean_expression = np.mean(expression_array)
                std_expression = np.std(expression_array)

                production_Rate[gene_name] = np.array([mean_expression, std_expression])
            output_list[i]['production_rate'] = production_Rate

    # Objective function part
    # --------------------------------------------------------------
    # We need to calculate the relative rate and add to the objective function
    ref_transcript = np.mean([d for d in info_list if d['name'] == target_dict['reference_system']][0]['transcripts'])

    if ref_transcript <= 0:
        objective += 100  #Something big because it'll give inf or NaN
        if additional_results:
            for i in range(n_systems):
                output_list[i]['objective'] = 0
                output_list[i]['relative_rate'] = 0
    else:
        for i in range(n_systems):
            system = info_list[i]
            relative_rate = system['transcripts']/ref_transcript
            system['relative_rate'] = relative_rate

            # Perform statistical test: Kolmogorov-Smirnov test to compare distributions
            KS_test = ks_2samp(system['relative_rate'], system['reference'])
            statistic = KS_test.statistic
            pvalue = KS_test.pvalue
            if metric == 'pvalue':
                if pvalue > 1e-10:
                    system_objective =  -np.log(pvalue)
                else:
                    system_objective = 100
            elif metric == 'statistic':
                system_objective = statistic
            else:
                print('Error, metric not recognised!')
                system_objective = 100
            objective+= system_objective

            # Add values to additional outputs
            if additional_results:
                output_list[i]['objective'] = system_objective
                output_list[i]['relative_rate'] = relative_rate
                output_list[i]['KS_test'] = KS_test

    return objective, output_list

# Optimize given an empirical (experimental) distribution of relative rates according the Kolmogorov-Smirnov test
# Uses the scipy.stats ks_2samp function
def KS_calibrate_w_rate_batches(info_list, target_dict, n_simulations, n_batches, metric='pvalue', additional_results=False):

    # Prepare variables
    objective=0.0
    n_systems = len(info_list)
    output_list = []  # Let's return it as a list as well

    # Create a multiprocessing pool
    pool = multiprocessing.Pool()

    # Run simulations
    # --------------------------------------------------------------
    # Go through each system, run simulations in parallel, collect outputs, repeat
    for i in range(n_systems):

        # This contains all the info we need to run the simulation and apply variations
        system = info_list[i]
        additional_dict = {}

        # Sort the processing info
        # --------------------------------------------------
        # Overall
        my_circuit = pt.load_circuit(system['global_conditions'])
        total_time = my_circuit.dt * my_circuit.frames
        dt = my_circuit.dt
        frames = my_circuit.frames

        # Sites - get sites that are not bare DNA or EXT
        target_sites = [site.name for site in my_circuit.site_list if 'DNA' not in site.site_type and 'EXT' not in site.site_type]
        target_genes = [site.name for site in my_circuit.site_list if site.site_type == 'gene' ]

        # Define x-axes
        # x_system = tct.get_interpolated_x(1, my_circuit.size, x_spacing=20)

        # We need a list of items, so the pool can pass each item to the function
        Items = []
        for simulation_number in range(n_simulations):
            g_dict = dict(system['global_conditions'])
            g_dict['n_simulations'] = simulation_number
            Item = {'global_conditions': g_dict, 'variations': system['variations']}
            Items.append(Item)

        # Run in parallel
        # ----------------------------
        # Run simulations in parallel within this subset
        pool_results = pool.map(pt.single_simulation_w_variations_return_dfs, Items)

        # Organise data into batches
        batches = distribute_into_batches(pool_results, n_batches)

        # Process transcripts - Serial
        # ----------------------------
        # Collect results (is it better to do it in serial or parallel? What causes more overhead?)
        transcript_list = []
        for batch in batches:
            transcript_batch = []
            for result in batch:
                environmental_df = result['environmental_df']
                mask = environmental_df['name'] == target_dict['reporter']

                if len(environmental_df[mask]['concentration']) == 0:
                    transcript = 0
                else:
                    transcript = environmental_df[mask]['concentration'].iloc[-1]
                transcript_batch.append(transcript)

            transcript_list.append( np.mean(transcript_batch) )

        # Convert to a NumPy arraypool_results
        transcripts_b_array = np.array(transcript_list)

        system['batch_transcripts'] = transcripts_b_array

        # --------------------------------------------------------------------
        # Here process additional stuff
        # --------------------------------------------------------------------
        if additional_results:   # Note I add it here to start giving shape to the code, in case in the future
                                 # I want to add the KDEs or the processing bit, so it can

            additional_dict['batch_transcripts'] = transcripts_b_array
            output_list.append(additional_dict)

                                 # Total transcripts
            transcript_list = []
            for result in pool_results:
                environmental_df = result['environmental_df']
                mask = environmental_df['name'] == target_dict['reporter']

                if len(environmental_df[mask]['concentration']) == 0:
                    transcript = 0
                else:
                    transcript = environmental_df[mask]['concentration'].iloc[-1]
                    transcript_list.append(transcript)

            # Convert to a NumPy arraypool_results
            transcripts_array = np.array(transcript_list)

            system['transcripts'] = transcripts_array

            output_list[i]['transcripts'] = transcripts_array

            # System info
            output_list[i]['name'] = system['name']
            output_list[i]['despcription'] = system['description']
            output_list[i]['bacterium'] = system['bacterium']
            output_list[i]['promoter'] = system['promoter']
            output_list[i]['strain'] = system['strain']

            # This time is just the reference (it is a list of measurements rathre than a mean and std)
            output_list[i]['reference'] = system['reference'] #np.array([system['reference'], system['reference_std']])

            # Global sigma
            # --------------------------------------------------------------------
            global_superhelical = []
            for result in pool_results:
                 sites_df = result['sites_df']
                 mask_circuit = sites_df['type'] == 'circuit'
                 # Collect measurements
                 global_superhelical.append(sites_df[mask_circuit]['superhelical'].to_numpy())
            output_list[i]['global_superhelical'] = np.array(global_superhelical)

            # Get site related measurements: local supercoiling, correlations & positions
            # --------------------------------------------------------------------
            local_superhelical = {}
            for site_name in target_sites:
                local_superhelical[site_name] = []
                for result in pool_results:
                    sites_df = result['sites_df']
                    site_mask = sites_df['name'] == site_name

                    # Collect measurements
                    local_superhelical[site_name].append(sites_df[site_mask]['superhelical'].to_numpy())
                local_superhelical[site_name] = np.array(local_superhelical[site_name])
            output_list[i]['local_superhelical'] = local_superhelical

            # Get transcripts
            # --------------------------------------------------------------------
            # Collect results (is it better to do it in serial or parallel? What causes more overhead?)
            production_Rate = {}
            for gene_name in target_genes:
                production_Rate[gene_name] = []
                transcript_list = []
                for result in pool_results:
                    environmental_df = result['environmental_df']
                    mask = environmental_df['name'] == gene_name

                    if len(environmental_df[mask]['concentration']) == 0:
                        transcript = 0
                    else:
                        transcript = environmental_df[mask]['concentration'].iloc[-1]
                    transcript_list.append(transcript)
                expression_array = np.array(transcript_list)/total_time
                mean_expression = np.mean(expression_array)
                std_expression = np.std(expression_array)

                production_Rate[gene_name] = np.array([mean_expression, std_expression])
            output_list[i]['production_rate'] = production_Rate

    # Objective function part
    # --------------------------------------------------------------
    # We need to calculate the relative rate and add to the objective function
    ref_transcript = np.mean([d for d in info_list if d['name'] == target_dict['reference_system']][0]['batch_transcripts'])

    if ref_transcript <= 0:
        objective += 100  #Something big because it'll give inf or NaN
        if additional_results:
            for i in range(n_systems):
                output_list[i]['objective'] = 0
                output_list[i]['relative_rate'] = 0
    else:
        for i in range(n_systems):
            system = info_list[i]
            relative_rate = system['batch_transcripts']/ref_transcript
            system['relative_rate'] = relative_rate

            # Perform statistical test: Kolmogorov-Smirnov test to compare distributions
            KS_test = ks_2samp(system['relative_rate'], system['reference'])
            statistic = KS_test.statistic
            pvalue = KS_test.pvalue
            if metric == 'pvalue':
                if pvalue > 1e-10:
                    system_objective =  -np.log(pvalue)
                else:
                    system_objective = 100
            elif metric == 'statistic':
                system_objective = statistic
            else:
                print('Error, metric not recognised!')
                system_objective = 100
            objective+= system_objective

            # Add values to additional outputs
            if additional_results:
                output_list[i]['objective'] = system_objective
                output_list[i]['relative_rate'] = relative_rate
                output_list[i]['KS_test'] = KS_test

    return objective, output_list

# Similar to KS_calibrate_w_rate_batches, but here we aim to relax a bit the memory bottleneck, and it returns an
# objective dictionary.
# This function optimizes the system given an empirical (experimental) distribution of relative rates according the Kolmogorov-Smirnov test
# Uses the scipy.stats ks_2samp function for the statistical test
# It returns the objective_dict which is a dictionary that contains the test loss, the loss of each system, and additionally, 
# very minimalistic unprocessed information to analyse performance of random search, like average transcripts and their std's.
# and an output_list if additional_results=True, which contains output information for analysis of a selected parameter set (usually the best).
def KS_calibrate_dist_batches_lossdict(info_list, target_dict, n_simulations, n_batches, metric='pvalue', additional_results=False):

    # Prepare variables
    objective=0.0
    n_systems = len(info_list)
    output_list = []  # Let's return it as a list as well
    objective_dict = {'loss': 1000, 'status':'fail', 'system_loss': {}, 'batch_transcripts': {}, 'relative_rate': {}}

    # Create a multiprocessing pool
    pool = multiprocessing.Pool()

    # Run simulations
    # --------------------------------------------------------------
    # Go through each system, run simulations in parallel, collect outputs, repeat
    for i in range(n_systems):

        # This contains all the info we need to run the simulation and apply variations
        system = info_list[i]
        additional_dict = {}

        # Let's initially the objective list
        # objective_dict['system_loss'][system['name']] = 1000
        # objective_dict = {'loss': 1000, 'system_loss': {}, 'batch_transcripts': {}}


        # Sort the processing info
        # --------------------------------------------------
        # Overall
        my_circuit = pt.load_circuit(system['global_conditions'])
        total_time = my_circuit.dt * my_circuit.frames
        # dt = my_circuit.dt
        # frames = my_circuit.frames

        # Sites - get sites that are not bare DNA or EXT
        target_sites = [site.name for site in my_circuit.site_list if 'DNA' not in site.site_type and 'EXT' not in site.site_type]
        # target_genes = [site.name for site in my_circuit.site_list if site.site_type == 'gene' ]
        target_genes = [site.name for site in my_circuit.site_list if 'gene' in site.site_type ]

        # Define x-axes
        # x_system = tct.get_interpolated_x(1, my_circuit.size, x_spacing=20)

        # We need a list of items, so the pool can pass each item to the function
        Items = []
        for simulation_number in range(n_simulations):
            g_dict = dict(system['global_conditions'])
            g_dict['n_simulations'] = simulation_number
            Item = {'global_conditions': g_dict, 'variations': system['variations']}
            Items.append(Item)

        # Run in parallel
        # ----------------------------
        # Run simulations in parallel within this subset
        pool_results = pool.map(pt.single_simulation_w_variations_return_dfs, Items)

        # Organise data into batches
        batches = distribute_into_batches(pool_results, n_batches)

        # Process transcripts - Serial
        # ----------------------------
        # Collect results (is it better to do it in serial or parallel? What causes more overhead?)
        transcript_list = []
        for batch in batches:
            transcript_batch = []
            for result in batch:
                environmental_df = result['environmental_df']
                mask = environmental_df['name'] == target_dict['reporter']

                if len(environmental_df[mask]['concentration']) == 0:
                    transcript = 0
                else:
                    transcript = environmental_df[mask]['concentration'].iloc[-1]
                transcript_batch.append(transcript)

            transcript_list.append( np.mean(transcript_batch) )

        # Convert to a NumPy arraypool_results
        transcripts_b_array = np.array(transcript_list)

        system['batch_transcripts'] = transcripts_b_array

        # --------------------------------------------------------------------
        # Here process additional stuff
        # --------------------------------------------------------------------
        if additional_results:   # Note I add it here to start giving shape to the code, in case in the future
                                 # I want to add the KDEs or the processing bit, so it can

            additional_dict['batch_transcripts'] = transcripts_b_array
            output_list.append(additional_dict)

                                 # Total transcripts
            transcript_list = []
            for result in pool_results:
                environmental_df = result['environmental_df']
                mask = environmental_df['name'] == target_dict['reporter']

                if len(environmental_df[mask]['concentration']) == 0:
                    transcript = 0
                else:
                    transcript = environmental_df[mask]['concentration'].iloc[-1]
                    transcript_list.append(transcript)

            # Convert to a NumPy arraypool_results
            transcripts_array = np.array(transcript_list)

            system['transcripts'] = transcripts_array

            output_list[i]['transcripts'] = transcripts_array

            # System info
            output_list[i]['name'] = system['name']
            output_list[i]['despcription'] = system['description']
            output_list[i]['bacterium'] = system['bacterium']
            output_list[i]['promoter'] = system['promoter']
            output_list[i]['strain'] = system['strain']

            # This time is just the reference (it is a list of measurements rathre than a mean and std)
            output_list[i]['reference'] = system['reference'] #np.array([system['reference'], system['reference_std']])

            # Global sigma
            # --------------------------------------------------------------------
            global_superhelical = []
            for result in pool_results:
                 sites_df = result['sites_df']
                 mask_circuit = sites_df['type'] == 'circuit'
                 # Collect measurements
                 global_superhelical.append(sites_df[mask_circuit]['superhelical'].to_numpy())
            output_list[i]['global_superhelical'] = np.array(global_superhelical)

            # Get site related measurements: local supercoiling, correlations & positions
            # --------------------------------------------------------------------
            local_superhelical = {}
            for site_name in target_sites:
                local_superhelical[site_name] = []
                for result in pool_results:
                    sites_df = result['sites_df']
                    site_mask = sites_df['name'] == site_name

                    # Collect measurements
                    local_superhelical[site_name].append(sites_df[site_mask]['superhelical'].to_numpy())
                local_superhelical[site_name] = np.array(local_superhelical[site_name])
            output_list[i]['local_superhelical'] = local_superhelical

            # Get transcripts
            # --------------------------------------------------------------------
            # Collect results (is it better to do it in serial or parallel? What causes more overhead?)
            production_Rate = {}
            for gene_name in target_genes:
                production_Rate[gene_name] = []
                transcript_list = []
                for result in pool_results:
                    environmental_df = result['environmental_df']
                    mask = environmental_df['name'] == gene_name

                    if len(environmental_df[mask]['concentration']) == 0:
                        transcript = 0
                    else:
                        transcript = environmental_df[mask]['concentration'].iloc[-1]
                    transcript_list.append(transcript)
                expression_array = np.array(transcript_list)/total_time
                mean_expression = np.mean(expression_array)
                std_expression = np.std(expression_array)

                production_Rate[gene_name] = np.array([mean_expression, std_expression])
            output_list[i]['production_rate'] = production_Rate

    # Objective function part
    # --------------------------------------------------------------
    # We need to calculate the relative rate and add to the objective function
    ref_transcript = np.mean([d for d in info_list if d['name'] == target_dict['reference_system']][0]['batch_transcripts'])

    if ref_transcript <= 0:
        objective += 100  #Something big because it'll give inf or NaN
        if additional_results:
            for i in range(n_systems):
                output_list[i]['objective'] = 0
                output_list[i]['relative_rate'] = 0
    else:
        objective_dict['status'] = 'ok'  # Everything OK!

        for i in range(n_systems):
            system = info_list[i]
            relative_rate = system['batch_transcripts']/ref_transcript
            system['relative_rate'] = relative_rate

            # Perform statistical test: Kolmogorov-Smirnov test to compare distributions
            KS_test = ks_2samp(system['relative_rate'], system['reference'])
            statistic = KS_test.statistic
            pvalue = KS_test.pvalue
            if metric == 'pvalue':
                if pvalue > 1e-10:
                    system_objective =  -np.log(pvalue)
                else:
                    system_objective = 100
            elif metric == 'statistic':
                system_objective = statistic
            else:
                print('Error, metric not recognised!')
                system_objective = 100

            objective+= system_objective

            # Add objectives components to objective_dict
            # --------------------------------------------------------------------
            objective_dict['system_loss'][system['name']] = system_objective
            objective_dict['batch_transcripts'][system['name']] = system['batch_transcripts']
            objective_dict['relative_rate'][system['name']] = relative_rate #np.mean(relative_rate)

            # Add values to additional outputs
            if additional_results:
                output_list[i]['objective'] = system_objective
                output_list[i]['relative_rate'] = relative_rate
                output_list[i]['KS_test'] = KS_test
                
    objective_dict['loss'] = objective

    return objective_dict, output_list

def distribute_into_batches(elements, M):
    """
    Distribute a list of elements into M batches as evenly as possible.

    Parameters:
    - elements: List of N elements to distribute.
    - M: Number of batches.

    Returns:
    - List of M sublists (batches).
    """
    if M <= 0:
        raise ValueError("Number of batches (M) must be greater than 0.")
    if M > len(elements):
        raise ValueError("M cannot be greater than the number of elements.")

    # Compute the size of each batch
    batch_size = len(elements) // M
    remainder = len(elements) % M

    # Distribute elements into batches
    batches = []
    index = 0
    for i in range(M):
        extra = 1 if i < remainder else 0  # Distribute remainder to first few batches
        batches.append(elements[index:index + batch_size + extra])
        index += batch_size + extra

    return batches

