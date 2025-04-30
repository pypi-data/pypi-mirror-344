from unittest import TestCase
from TORCphysics import Circuit, Enzyme
from TORCphysics import effect_model as em
from TORCphysics import binding_model as bm
import pandas as pd

error = 0.00000000001


# TODO: Sort output names of tests
# TODO: Queria ver como puedo definir los bare DNA sites. Pensaba que anadiendo un global en el sites haria las cosas
#  mas faciles, pero aun no se.
class TestCircuit(TestCase):

    # For this test, Circuit should be able to process these non-empty input files (which hopefully are correct).
    # Then, it performs three tests: it counts the number of enzymes, sites and environmentals.
    def test_Circuit_init(self):
        circuit_filename = 'circuit.csv'
        sites_filename = 'sites.csv'
        enzymes_filename = 'enzymes.csv'
        environment_filename = 'environment.csv'
        output_prefix = ''
        frames = 5
        series = True
        continuation = False
        dt = 1
        my_circuit = Circuit(circuit_filename, sites_filename, enzymes_filename, environment_filename,
                             output_prefix, frames, series, continuation, dt)
        self.assertGreater(my_circuit.get_num_enzymes(), 0, "Empty enzyme list")
        self.assertGreater(my_circuit.get_num_sites(), 0, "Empty enzyme list")
        self.assertGreater(my_circuit.get_num_environmentals(), 0, "Empty enzyme list")

        # And test the one with the sequence
        circuit_filename = 'circuit_sequence.csv'
        my_circuit = Circuit(circuit_filename, sites_filename, enzymes_filename, environment_filename,
                             output_prefix, frames, series, continuation, dt)
        self.assertGreater(my_circuit.get_num_enzymes(), 0, "Empty enzyme list")
        self.assertGreater(my_circuit.get_num_sites(), 0, "Empty enzyme list")
        self.assertGreater(my_circuit.get_num_environmentals(), 0, "Empty enzyme list")

    # TODO: Try doing many enzyme types. Topos that bind stochastically, and topos that act continuously on the DNA.
    # TODO:
    #  1.- Let's make the code work with many types of enzymes.
    #  1.1.- Add new bindings - TopoI and Gyrase DONE!
    #  1.2 - Add topoisomerase action - DONE
    #  1.2.1 - Let's make it work for topoI continuum and stochastic, remove the tm and mm parameters, then add both
    #          mechanisms for gyrase - DONE
    #  1.3 - Add Topoisomerases Effects - DONE
    #  2.- Also remove the topo model and mechanistic model and all that DONE!
    #  3.- Then, start documenting and tidying up workflow. We have to do this!
    #  3.1.- Also document and test the new/old functions of:
    #  3.1.1.- Binding - DONE!
    #  3.1.2.- Effect - DONE!
    #  3.1.3.- Unbinding - DONE!
    #  4.- Test models_workflow - Documenting last functions. After documenting, DONEEEE!
    #  4.1.- Try modeling LacI bridging, see if it works! Just for the TORCMeeting. DONE!!!
    #  AQUI ANDO TESTEANDO EL CIRCUITO
    #  5.- Then start tidying and documenting circuit, while doing this, fix the optional inputs, outputs and all that.
    #  5.1.- When you test the circuit, test the individual functions, and make an overall/simple simulation run.
    #  6.- Create a new type of test, where you test systems, and plot the results so you can also use them as examples?
    #    Or better do an example section?
    #  7.-  Also, before continue with the topo calibration, try to simulate the lacI binding and bridging!
    #  8.- Check how effective_size affects everything
    def test_run(self):
        circuit_filename = 'circuit.csv'
        sites_filename = 'sites.csv'
        enzymes_filename = 'enzymes.csv'
        environment_filename = 'environment.csv'
        output_prefix = 'output'
        frames = 500
        series = True
        continuation = False
        dt = 1.0

        my_circuit = Circuit(circuit_filename, sites_filename, enzymes_filename, environment_filename,
                             output_prefix, frames, series, continuation, dt)
        my_circuit.environmental_list[3].unbinding_model.k_off = 0.5
        my_circuit.environmental_list[4].unbinding_model.k_off = 0.5
        # Let's make the rates
        my_circuit.run()

    def test_run2(self):
        circuit_filename = 'circuit.csv'
        sites_filename = 'sites.csv'
        enzymes_filename = 'enzymes.csv'
        environment_filename = 'environment.csv'
        output_prefix = 'output'
        frames = 1500
        series = True
        continuation = False
        dt = 0.5
        tm = 'continuum'
        mm = 'uniform'
        my_circuit = Circuit(circuit_filename, sites_filename, enzymes_filename, environment_filename,
                             output_prefix, frames, series, continuation, dt)
        my_circuit.environmental_list[0].concentration = 0
        my_circuit.environmental_list[1].concentration = 0
        print(my_circuit.environmental_list)
        for site in my_circuit.site_list:  # I'll increase the rates
            # site.k_min = site.k_min * 100
            site.k_min = site.k_on * 0
        print(my_circuit.site_list[2].name)
        my_circuit.site_list[2].k_on = 0.01
        # Let's make the rates
        my_circuit.run()
        print(0)

    # Tests the positions of the fake enzymes
    def test_fake_ends(self):
        # CIRCULAR
        # -----------------------------------------------------------------------------------------
        # Empty case
        circuit_filename = '../test_inputs/test_circuit_circular.csv'
        sites_filename = '../test_inputs/sites_1_gene.csv'
        enzymes_filename = '../test_inputs/empty_enzymes.csv'
        environment_filename = '../test_inputs/RNAP_environment.csv'
        output_prefix = 'output'
        frames = 5
        series = True
        continuation = False
        dt = 1
        my_circuit = Circuit(circuit_filename, sites_filename, enzymes_filename, environment_filename,
                             output_prefix, frames, series, continuation, dt)
        self.assertEqual(my_circuit.enzyme_list[0].position, 0, "Wrong position of left fake enzyme")
        self.assertEqual(my_circuit.enzyme_list[-1].position, my_circuit.size + 1,
                         "Wrong position of right fake enzyme")

        # One Enzyme bound
        enzymes1_filename = '../test_inputs/enzymes_1.csv'
        my_circuit_1 = Circuit(circuit_filename, sites_filename, enzymes1_filename, environment_filename,
                               output_prefix, frames, series, continuation, dt)
        enzyme1 = my_circuit_1.enzyme_list[1]
        #        self.assertEqual(my_circuit_1.enzyme_list[0].position, 1 + enzyme1.position + enzyme1.size - my_circuit_1.size,
        #                         "Wrong position of left fake enzyme")
        self.assertEqual(my_circuit_1.enzyme_list[0].position,
                         enzyme1.position + enzyme1.effective_size - my_circuit_1.size,
                         "Wrong position of left fake enzyme")
        self.assertEqual(my_circuit_1.enzyme_list[-1].position, enzyme1.position + my_circuit_1.size,
                         "Wrong position of right fake enzyme")

        # Two Enzymes bound
        enzymes2_filename = '../test_inputs/enzymes_2.csv'
        my_circuit_2 = Circuit(circuit_filename, sites_filename, enzymes2_filename, environment_filename,
                               output_prefix, frames, series, continuation, dt)
        enzyme1 = my_circuit_2.enzyme_list[1]
        enzyme2 = my_circuit_2.enzyme_list[2]
        #        self.assertEqual(my_circuit_2.enzyme_list[0].position, 1 + enzyme2.position + enzyme2.size - my_circuit_2.size,
        #                         "Wrong position of left fake enzyme")
        self.assertEqual(my_circuit_2.enzyme_list[0].position,
                         enzyme2.position + enzyme2.effective_size - my_circuit_2.size,
                         "Wrong position of left fake enzyme")
        self.assertEqual(my_circuit_2.enzyme_list[-1].position, enzyme1.position + my_circuit_2.size,
                         "Wrong position of right fake enzyme")
        # LINEAR
        # -----------------------------------------------------------------------------------------
        circuit_filename_linear = '../test_inputs/test_circuit_linear.csv'
        # No enzymes
        my_circuit_linear = Circuit(circuit_filename_linear, sites_filename, enzymes_filename, environment_filename,
                                    output_prefix, frames, series, continuation, dt)
        self.assertEqual(my_circuit_linear.enzyme_list[0].position, 0, "Wrong position of left fake enzyme")
        self.assertEqual(my_circuit_linear.enzyme_list[-1].position, my_circuit_linear.size + 1,
                         "Wrong position of right fake enzyme")
        # 1 enzyme
        my_circuit_linear1 = Circuit(circuit_filename_linear, sites_filename, enzymes1_filename, environment_filename,
                                     output_prefix, frames, series, continuation, dt, )
        self.assertEqual(my_circuit_linear1.enzyme_list[0].position, 0, "Wrong position of left fake enzyme")
        self.assertEqual(my_circuit_linear1.enzyme_list[-1].position, my_circuit_linear1.size + 1,
                         "Wrong position of right fake enzyme")
        # 2 enzymes
        my_circuit_linear2 = Circuit(circuit_filename_linear, sites_filename, enzymes2_filename, environment_filename,
                                     output_prefix, frames, series, continuation, dt, )
        self.assertEqual(my_circuit_linear2.enzyme_list[0].position, 0, "Wrong position of left fake enzyme")
        self.assertEqual(my_circuit_linear2.enzyme_list[-1].position, my_circuit_linear2.size + 1,
                         "Wrong position of right fake enzyme")

    def test_add_enzyme(self):

        # Test 1: Linear test with single enzyme.
        # ----------------------------------------------------------------------------
        print("Test 1.0- Linear DNA with new enzyme")

        circuit_filename = 'circuit_linear.csv'
        sites_filename = 'sites.csv'
        enzymes_filename = 'enzymes.csv'
        environment_filename = 'environment_simple.csv'
        output_prefix = ''
        frames = 1000
        series = True
        continuation = False
        dt = 1
        my_circuit = Circuit(circuit_filename, sites_filename, enzymes_filename, environment_filename,
                             output_prefix, frames, series, continuation, dt)
        site = my_circuit.site_list[4]

        n0 = len(my_circuit.enzyme_list) - 2  # Initial number of bound enzymes
        twist0 = my_circuit.twist  # Initial twist
        sigma0 = my_circuit.superhelical  #and supercoiling

        #for enzyme in my_circuit.enzyme_list:
        #    print(enzyme.name, enzyme.twist, enzyme.superhelical)

        # create new enzymes
        enzyme1 = Enzyme(e_type='RNAP', name='test1', site=site, position=4000,
                         size=60, effective_size=30, twist=0.0,
                         superhelical=0.0, effect_model=None,
                         unbinding_model=None)
        new_enzymes = [enzyme1]

        my_circuit.add_new_enzymes(new_enzymes)

        n_enzymes = len(my_circuit.enzyme_list) - 2

        my_circuit.update_global_twist()
        my_circuit.update_global_superhelical()

        dsigma = abs(sigma0 - my_circuit.superhelical)
        dtwist = abs(twist0 - my_circuit.twist)
        self.assertGreater(n_enzymes, n0)  # Check there are more enzymes
        self.assertLessEqual(dsigma, error, "Superhelical changed")
        self.assertLessEqual(dtwist, error, "Twist changed")

        # Test 1.1: Linear test with multiple enzyme.
        # ----------------------------------------------------------------------------
        print("Test 1.1.- Linear DNA with multiple enzymes")

        my_circuit = Circuit(circuit_filename, sites_filename, enzymes_filename, environment_filename,
                             output_prefix, frames, series, continuation, dt)
        site = my_circuit.site_list[4]

        n0 = len(my_circuit.enzyme_list) - 2  # Initial number of bound enzymes
        twist0 = my_circuit.twist  # Initial twist
        sigma0 = my_circuit.superhelical  # and supercoiling

        # create new enzymes
        enzyme1 = Enzyme(e_type='RNAP', name='test1', site=site, position=4000,
                         size=60, effective_size=30, twist=0.0,
                         superhelical=0.0, effect_model=None,
                         unbinding_model=None)
        enzyme2 = Enzyme(e_type='RNAP', name='test2', site=site, position=4300,
                         size=60, effective_size=30, twist=0.0,
                         superhelical=0.0, effect_model=None,
                         unbinding_model=None)
        new_enzymes = [enzyme1, enzyme2]

        my_circuit.add_new_enzymes(new_enzymes)

        n_enzymes = len(my_circuit.enzyme_list) - 2

        my_circuit.update_global_twist()
        my_circuit.update_global_superhelical()

        dsigma = abs(sigma0 - my_circuit.superhelical)
        dtwist = abs(twist0 - my_circuit.twist)
        self.assertGreater(n_enzymes, n0)  # Check there are more enzymes
        self.assertLessEqual(dsigma, error, "Superhelical changed")
        self.assertLessEqual(dtwist, error, "Twist changed")

        # Test 1.2: Linear test with no bound enzymes but multiple enzymes binding.
        # ----------------------------------------------------------------------------
        print("Test 1.2.- Linear DNA with no bound enzymes but multiple binding")
        enzymes_filename = '../test_inputs/empty_enzymes.csv'

        my_circuit = Circuit(circuit_filename, sites_filename, enzymes_filename, environment_filename,
                             output_prefix, frames, series, continuation, dt)
        site = my_circuit.site_list[4]

        n0 = len(my_circuit.enzyme_list) - 2  # Initial number of bound enzymes
        twist0 = my_circuit.twist  # Initial twist
        sigma0 = my_circuit.superhelical  # and supercoiling

        # create new enzymes
        enzyme1 = Enzyme(e_type='RNAP', name='test1', site=site, position=4000,
                         size=60, effective_size=30, twist=0.0,
                         superhelical=0.0, effect_model=None,
                         unbinding_model=None)
        enzyme2 = Enzyme(e_type='RNAP', name='test2', site=site, position=4300,
                         size=60, effective_size=30, twist=0.0,
                         superhelical=0.0, effect_model=None,
                         unbinding_model=None)
        new_enzymes = [enzyme1, enzyme2]

        my_circuit.add_new_enzymes(new_enzymes)

        n_enzymes = len(my_circuit.enzyme_list) - 2

        my_circuit.update_global_twist()
        my_circuit.update_global_superhelical()

        dsigma = abs(sigma0 - my_circuit.superhelical)
        dtwist = abs(twist0 - my_circuit.twist)
        self.assertGreater(n_enzymes, n0)  # Check there are more enzymes
        self.assertLessEqual(dsigma, error, "Superhelical changed")
        self.assertLessEqual(dtwist, error, "Twist changed")

        # Test 2.1: Circular test with single enzyme.
        # ----------------------------------------------------------------------------
        print("Test 2.1.- Circular DNA with new enzyme")

        circuit_filename = 'circuit.csv'
        sites_filename = 'sites.csv'
        enzymes_filename = 'enzymes.csv'
        environment_filename = 'environment_simple.csv'
        output_prefix = ''
        frames = 1000
        series = True
        continuation = False
        dt = 1
        my_circuit = Circuit(circuit_filename, sites_filename, enzymes_filename, environment_filename,
                             output_prefix, frames, series, continuation, dt)
        site = my_circuit.site_list[4]

        n0 = len(my_circuit.enzyme_list) - 2  # Initial number of bound enzymes
        twist0 = my_circuit.twist  # Initial twist
        sigma0 = my_circuit.superhelical  #and supercoiling

        # create new enzymes
        enzyme1 = Enzyme(e_type='RNAP', name='test1', site=site, position=4000,
                         size=60, effective_size=30, twist=0.0,
                         superhelical=0.0, effect_model=None,
                         unbinding_model=None)
        new_enzymes = [enzyme1]

        my_circuit.add_new_enzymes(new_enzymes)

        n_enzymes = len(my_circuit.enzyme_list) - 2

        my_circuit.update_global_twist()
        my_circuit.update_global_superhelical()

        dsigma = abs(sigma0 - my_circuit.superhelical)
        dtwist = abs(twist0 - my_circuit.twist)
        self.assertGreater(n_enzymes, n0)  # Check there are more enzymes
        self.assertLessEqual(dsigma, error, "Superhelical changed")
        self.assertLessEqual(dtwist, error, "Twist changed")

        # Test 2.2: Circular test with multiple enzyme.
        # ----------------------------------------------------------------------------
        print("Test 2.2.- Circular DNA with multiple enzyme")

        circuit_filename = 'circuit.csv'
        sites_filename = 'sites.csv'
        enzymes_filename = 'enzymes.csv'
        environment_filename = 'environment_simple.csv'
        output_prefix = ''
        frames = 1000
        series = True
        continuation = False
        dt = 1
        my_circuit = Circuit(circuit_filename, sites_filename, enzymes_filename, environment_filename,
                             output_prefix, frames, series, continuation, dt)
        site = my_circuit.site_list[4]

        n0 = len(my_circuit.enzyme_list) - 2  # Initial number of bound enzymes
        twist0 = my_circuit.twist  # Initial twist
        sigma0 = my_circuit.superhelical  #and supercoiling

        # create new enzymes
        enzyme1 = Enzyme(e_type='RNAP', name='test1', site=site, position=4000,
                         size=60, effective_size=30, twist=0.0,
                         superhelical=0.0, effect_model=None,
                         unbinding_model=None)
        enzyme2 = Enzyme(e_type='RNAP', name='test2', site=site, position=4300,
                         size=60, effective_size=30, twist=0.0,
                         superhelical=0.0, effect_model=None,
                         unbinding_model=None)
        new_enzymes = [enzyme1, enzyme2]

        my_circuit.add_new_enzymes(new_enzymes)

        n_enzymes = len(my_circuit.enzyme_list) - 2

        my_circuit.update_global_twist()
        my_circuit.update_global_superhelical()

        dsigma = abs(sigma0 - my_circuit.superhelical)
        dtwist = abs(twist0 - my_circuit.twist)
        self.assertGreater(n_enzymes, n0)  # Check there are more enzymes
        self.assertLessEqual(dsigma, error, "Superhelical changed")
        self.assertLessEqual(dtwist, error, "Twist changed")

        # Test 2.3: Circular test with empty enzyme.csv but multiple enzymes binding.
        # ----------------------------------------------------------------------------
        print("Test 2.3.- Circular DNA with no bound enzymes but  multiple trying to bind")

        circuit_filename = 'circuit.csv'
        sites_filename = 'sites.csv'
        enzymes_filename = '../test_inputs/empty_enzymes.csv'
        environment_filename = 'environment_simple.csv'
        output_prefix = ''
        frames = 1000
        series = True
        continuation = False
        dt = 1
        my_circuit = Circuit(circuit_filename, sites_filename, enzymes_filename, environment_filename,
                             output_prefix, frames, series, continuation, dt)
        site = my_circuit.site_list[4]

        n0 = len(my_circuit.enzyme_list) - 2  # Initial number of bound enzymes
        twist0 = my_circuit.twist  # Initial twist
        sigma0 = my_circuit.superhelical  #and supercoiling

        # create new enzymes
        enzyme1 = Enzyme(e_type='RNAP', name='test1', site=site, position=4000,
                         size=60, effective_size=30, twist=0.0,
                         superhelical=0.0, effect_model=None,
                         unbinding_model=None)
        enzyme2 = Enzyme(e_type='RNAP', name='test2', site=site, position=4300,
                         size=60, effective_size=30, twist=0.0,
                         superhelical=0.0, effect_model=None,
                         unbinding_model=None)
        new_enzymes = [enzyme1, enzyme2]

        my_circuit.add_new_enzymes(new_enzymes)

        n_enzymes = len(my_circuit.enzyme_list) - 2

        my_circuit.update_global_twist()
        my_circuit.update_global_superhelical()

        dsigma = abs(sigma0 - my_circuit.superhelical)
        dtwist = abs(twist0 - my_circuit.twist)
        self.assertGreater(n_enzymes, n0)  # Check there are more enzymes
        self.assertLessEqual(dsigma, error, "Superhelical changed")
        self.assertLessEqual(dtwist, error, "Twist changed")

        # Check boundaries
        self.assertEqual(my_circuit.enzyme_list[0].position,
                         enzyme2.position + enzyme2.effective_size - my_circuit.size,
                         "Wrong position of left fake enzyme")
        self.assertEqual(my_circuit.enzyme_list[-1].position, enzyme1.position + my_circuit.size,
                         "Wrong position of right fake enzyme")

        # Test 2.4: Circular test with one bound enzyme and one new one binding on the left edge.
        # ----------------------------------------------------------------------------
        print("Test 2.4.- Circular DNA with no bound enzymes but one binding on the left edge.")

        circuit_filename = 'circuit.csv'
        sites_filename = 'sites.csv'
        enzymes_filename = '1enzyme.csv'
        environment_filename = 'environment_simple.csv'
        output_prefix = ''
        frames = 1000
        series = True
        continuation = False
        dt = 1
        my_circuit = Circuit(circuit_filename, sites_filename, enzymes_filename, environment_filename,
                             output_prefix, frames, series, continuation, dt)
        site = my_circuit.site_list[4]

        n0 = len(my_circuit.enzyme_list) - 2  # Initial number of bound enzymes
        twist0 = my_circuit.twist  # Initial twist
        sigma0 = my_circuit.superhelical  #and supercoiling

        # create new enzymes
        enzyme1 = Enzyme(e_type='RNAP', name='test1', site=site, position=2000,
                         size=60, effective_size=30, twist=0.0,
                         superhelical=0.0, effect_model=None,
                         unbinding_model=None)
        new_enzymes = [enzyme1]

        my_circuit.add_new_enzymes(new_enzymes)

        n_enzymes = len(my_circuit.enzyme_list) - 2

        my_circuit.update_global_twist()
        my_circuit.update_global_superhelical()

        dsigma = abs(sigma0 - my_circuit.superhelical)
        dtwist = abs(twist0 - my_circuit.twist)
        self.assertGreater(n_enzymes, n0)  # Check there are more enzymes
        self.assertLessEqual(dsigma, error, "Superhelical changed")
        self.assertLessEqual(dtwist, error, "Twist changed")

        # Check boundaries
        self.assertEqual(my_circuit.enzyme_list[0].position,
                         my_circuit.enzyme_list[2].position + my_circuit.enzyme_list[
                             2].effective_size - my_circuit.size,
                         "Wrong position of left fake enzyme")
        self.assertEqual(my_circuit.enzyme_list[-1].position, enzyme1.position + my_circuit.size,
                         "Wrong position of right fake enzyme")

        # Test 2.5: Circular test with one bound enzyme and one new one binding on the right edge.
        # ----------------------------------------------------------------------------
        print("Test 2.5.- Circular DNA with no bound enzymes but one binding on the right edge.")

        circuit_filename = 'circuit.csv'
        sites_filename = 'sites.csv'
        enzymes_filename = '1enzyme.csv'
        environment_filename = 'environment_simple.csv'
        output_prefix = ''
        frames = 1000
        series = True
        continuation = False
        dt = 1
        my_circuit = Circuit(circuit_filename, sites_filename, enzymes_filename, environment_filename,
                             output_prefix, frames, series, continuation, dt)
        site = my_circuit.site_list[4]

        n0 = len(my_circuit.enzyme_list) - 2  # Initial number of bound enzymes
        twist0 = my_circuit.twist  # Initial twist
        sigma0 = my_circuit.superhelical  #and supercoiling

        # create new enzymes
        enzyme1 = Enzyme(e_type='RNAP', name='test1', site=site, position=4000,
                         size=60, effective_size=30, twist=0.0,
                         superhelical=0.0, effect_model=None,
                         unbinding_model=None)
        new_enzymes = [enzyme1]

        my_circuit.add_new_enzymes(new_enzymes)

        n_enzymes = len(my_circuit.enzyme_list) - 2

        my_circuit.update_global_twist()
        my_circuit.update_global_superhelical()

        dsigma = abs(sigma0 - my_circuit.superhelical)
        dtwist = abs(twist0 - my_circuit.twist)
        self.assertGreater(n_enzymes, n0)  # Check there are more enzymes
        self.assertLessEqual(dsigma, error, "Superhelical changed")
        self.assertLessEqual(dtwist, error, "Twist changed")

        # Check boundaries
        self.assertEqual(my_circuit.enzyme_list[0].position,
                         my_circuit.enzyme_list[2].position + my_circuit.enzyme_list[
                             2].effective_size - my_circuit.size,
                         "Wrong position of left fake enzyme")
        self.assertEqual(my_circuit.enzyme_list[-1].position, my_circuit.enzyme_list[1].position + my_circuit.size,
                         "Wrong position of right fake enzyme")

    def test_drop_enzyme(self):

        # Test 1.0: Linear test with single enzyme.
        # ----------------------------------------------------------------------------
        print("Test 1.0- Linear DNA dropping one bound enzyme (Simplest case")

        circuit_filename = 'circuit_linear.csv'
        sites_filename = 'sites.csv'
        enzymes_filename = '1enzyme.csv'
        environment_filename = 'environment_simple.csv'
        output_prefix = ''
        frames = 1000
        series = True
        continuation = False
        dt = 1
        my_circuit = Circuit(circuit_filename, sites_filename, enzymes_filename, environment_filename,
                             output_prefix, frames, series, continuation, dt)

        n0 = len(my_circuit.enzyme_list) - 2  # Initial number of bound enzymes
        twist0 = my_circuit.twist  # Initial twist
        sigma0 = my_circuit.superhelical  #and supercoiling
        drop_index = [1]

        my_circuit.drop_enzymes(drop_list=drop_index)

        n_enzymes = len(my_circuit.enzyme_list) - 2

        my_circuit.update_global_twist()
        my_circuit.update_global_superhelical()

        dsigma = abs(sigma0 - my_circuit.superhelical)
        dtwist = abs(twist0 - my_circuit.twist)
        self.assertLess(n_enzymes, n0)  # Check there are more enzymes
        self.assertLessEqual(dsigma, error, "Superhelical changed")
        self.assertLessEqual(dtwist, error, "Twist changed")

        # Test 1.1: Linear test with single enzyme.
        # ----------------------------------------------------------------------------
        print("Test 1.1- Linear DNA dropping two bound enzymes.")

        circuit_filename = 'circuit_linear.csv'
        sites_filename = 'sites.csv'
        enzymes_filename = 'enzymes.csv'
        environment_filename = 'environment_simple.csv'
        output_prefix = ''
        frames = 1000
        series = True
        continuation = False
        dt = 1
        my_circuit = Circuit(circuit_filename, sites_filename, enzymes_filename, environment_filename,
                             output_prefix, frames, series, continuation, dt)

        n0 = len(my_circuit.enzyme_list) - 2  # Initial number of bound enzymes
        twist0 = my_circuit.twist  # Initial twist
        sigma0 = my_circuit.superhelical  #and supercoiling
        drop_index = [1, 2]

        my_circuit.drop_enzymes(drop_list=drop_index)

        n_enzymes = len(my_circuit.enzyme_list) - 2

        my_circuit.update_global_twist()
        my_circuit.update_global_superhelical()

        dsigma = abs(sigma0 - my_circuit.superhelical)
        dtwist = abs(twist0 - my_circuit.twist)
        self.assertLess(n_enzymes, n0)  # Check there are more enzymes
        self.assertLessEqual(dsigma, error, "Superhelical changed")
        self.assertLessEqual(dtwist, error, "Twist changed")

        # Test 2.0: Circular test dropping one enzyme and no one remains.
        # ----------------------------------------------------------------------------
        print("Test 2.0- Circular DNA dropping one bound enzyme and remains empty.")

        circuit_filename = 'circuit.csv'
        sites_filename = 'sites.csv'
        enzymes_filename = '1enzyme.csv'
        environment_filename = 'environment_simple.csv'
        output_prefix = ''
        frames = 1000
        series = True
        continuation = False
        dt = 1
        my_circuit = Circuit(circuit_filename, sites_filename, enzymes_filename, environment_filename,
                             output_prefix, frames, series, continuation, dt)

        n0 = len(my_circuit.enzyme_list) - 2  # Initial number of bound enzymes
        twist0 = my_circuit.twist  # Initial twist
        sigma0 = my_circuit.superhelical  #and supercoiling
        drop_index = [1]

        my_circuit.drop_enzymes(drop_list=drop_index)

        n_enzymes = len(my_circuit.enzyme_list) - 2

        my_circuit.update_global_twist()
        my_circuit.update_global_superhelical()

        dsigma = abs(sigma0 - my_circuit.superhelical)
        dtwist = abs(twist0 - my_circuit.twist)
        self.assertLess(n_enzymes, n0)  # Check there are more enzymes
        self.assertLessEqual(dsigma, error, "Superhelical changed")
        self.assertLessEqual(dtwist, error, "Twist changed")

        # Check EXT
        self.assertEqual(my_circuit.enzyme_list[0].position, 0, "Wrong position of left fake enzyme")
        self.assertEqual(my_circuit.enzyme_list[-1].position, my_circuit.size + 1,
                         "Wrong position of right fake enzyme")


        # Test 2.1
        # ----------------------------------------------------------------------------
        print("Test 2.1- Circular DNA dropping two bound enzyme and remains empty.")

        circuit_filename = 'circuit.csv'
        sites_filename = 'sites.csv'
        enzymes_filename = 'enzymes.csv'
        environment_filename = 'environment_simple.csv'
        output_prefix = ''
        frames = 1000
        series = True
        continuation = False
        dt = 1
        my_circuit = Circuit(circuit_filename, sites_filename, enzymes_filename, environment_filename,
                             output_prefix, frames, series, continuation, dt)

        n0 = len(my_circuit.enzyme_list) - 2  # Initial number of bound enzymes
        twist0 = my_circuit.twist  # Initial twist
        sigma0 = my_circuit.superhelical  #and supercoiling
        drop_index = [1, 2]

        my_circuit.drop_enzymes(drop_list=drop_index)

        n_enzymes = len(my_circuit.enzyme_list) - 2

        my_circuit.update_global_twist()
        my_circuit.update_global_superhelical()

        dsigma = abs(sigma0 - my_circuit.superhelical)
        dtwist = abs(twist0 - my_circuit.twist)
        self.assertLess(n_enzymes, n0)  # Check there are more enzymes
        self.assertLessEqual(dsigma, error, "Superhelical changed")
        self.assertLessEqual(dtwist, error, "Twist changed")

        # Check EXT
        self.assertEqual(my_circuit.enzyme_list[0].position, 0, "Wrong position of left fake enzyme")
        self.assertEqual(my_circuit.enzyme_list[-1].position, my_circuit.size + 1,
                         "Wrong position of right fake enzyme")

        # Test 2.2
        # ----------------------------------------------------------------------------
        print("Test 2.2- Circular DNA dropping one bound enzyme and one ramins.")

        circuit_filename = 'circuit.csv'
        sites_filename = 'sites.csv'
        enzymes_filename = 'enzymes.csv'
        environment_filename = 'environment_simple.csv'
        output_prefix = ''
        frames = 1000
        series = True
        continuation = False
        dt = 1
        my_circuit = Circuit(circuit_filename, sites_filename, enzymes_filename, environment_filename,
                             output_prefix, frames, series, continuation, dt)

        n0 = len(my_circuit.enzyme_list) - 2  # Initial number of bound enzymes
        twist0 = my_circuit.twist  # Initial twist
        sigma0 = my_circuit.superhelical  #and supercoiling
        drop_index = [1]

        my_circuit.drop_enzymes(drop_list=drop_index)

        n_enzymes = len(my_circuit.enzyme_list) - 2

        my_circuit.update_global_twist()
        my_circuit.update_global_superhelical()

        dsigma = abs(sigma0 - my_circuit.superhelical)
        dtwist = abs(twist0 - my_circuit.twist)
        self.assertLess(n_enzymes, n0)  # Check there are more enzymes
        self.assertLessEqual(dsigma, error, "Superhelical changed")
        self.assertLessEqual(dtwist, error, "Twist changed")

        # Check EXT
        self.assertEqual(my_circuit.enzyme_list[0].position,
                         my_circuit.enzyme_list[1].position + my_circuit.enzyme_list[
                             1].effective_size - my_circuit.size,
                         "Wrong position of left fake enzyme")
        self.assertEqual(my_circuit.enzyme_list[-1].position, my_circuit.enzyme_list[1].position + my_circuit.size,
                         "Wrong position of right fake enzyme")


    # TODO: These tests cannot run the current version of the circuit. They need to be updated.
    # TODO: test bind/unbind no topo - one gene, a RNAP binds, then unbinds and twist is conserved. - test with 2 genes
    def test_bind_unbind_1_RNAP_1_gene(self):
        circuit_filename = '../test_inputs/test_circuit_circular.csv'
        sites_filename = '../test_inputs/sites_1_gene.csv'
        enzymes_filename = '../test_inputs/empty_enzymes.csv'
        environment_filename = '../test_inputs/RNAP_environment.csv'
        output_prefix = 'output'
        frames = 500
        series = True
        continuation = False
        tm = 'continuum'
        mm = 'uniform'
        dt = 1
        my_circuit = Circuit(circuit_filename, sites_filename, enzymes_filename, environment_filename,
                             output_prefix, frames, series, continuation, dt, )
        # my_circuit.site_list[2].k_min = 0.0
        s0 = my_circuit.superhelical

        # This is similar to the Run function... but the idea is that we will control the rate
        for frame in range(1, frames + 1):
            my_circuit.frame = frame
            my_circuit.time = frame * dt
            if my_circuit.series:
                my_circuit.append_sites_to_dict_step1()

            # if frame == 100:
            # my_circuit.site_list[2].k_min = .1

            # Apply binding model and get list of new enzymes
            new_enzyme_list = bm.binding_model(my_circuit.enzyme_list, my_circuit.environmental_list, dt,
                                               my_circuit.rng)

            if len(new_enzyme_list) > 0:
                my_circuit.site_list[2].k_min = 0.0
            my_circuit.add_new_enzymes(new_enzyme_list)  # It also calculates fixes the twists and updates supercoiling

            # EFFECT
            # --------------------------------------------------------------
            effects_list = em.effect_model(my_circuit.enzyme_list, my_circuit.environmental_list, dt,
                                           my_circuit.topoisomerase_model, my_circuit.mechanical_model)
            my_circuit.apply_effects(effects_list)

            # UNBINDING
            drop_list_index, drop_list_enzyme = bm.unbinding_model(my_circuit.enzyme_list,
                                                                   my_circuit.dt, my_circuit.rng)
            my_circuit.drop_enzymes(drop_list_index)
            my_circuit.add_to_environment(drop_list_enzyme)

            # UPDATE GLOBALS
            my_circuit.update_global_twist()
            my_circuit.update_global_superhelical()

            # Add to series df if the series option was selected (default=True)
            if series:
                my_circuit.append_enzymes_to_dict()
                my_circuit.append_sites_to_dict_step2(new_enzyme_list, drop_list_enzyme)

        # Output the dataframes: (series)
        if series:
            my_circuit.enzymes_df = pd.DataFrame.from_dict(my_circuit.enzymes_dict_list)
            my_circuit.enzymes_df.to_csv(my_circuit.name + '_enzymes_df.csv', index=False, sep=',')
            my_circuit.sites_df = pd.DataFrame.from_dict(my_circuit.sites_dict_list)
            my_circuit.sites_df.to_csv(my_circuit.name + '_sites_df.csv', index=False, sep=',')

        # Output the log of events
        my_circuit.log.log_out()
        sf = my_circuit.superhelical  # final superhelical
        self.assertEqual(abs(s0 - sf), 0, "Superhelical changed")

    # Bind unbind with 1 NAP on the right
    def test_bind_unbind_1_RNAP_1_gene_1_NAP_right(self):
        circuit_filename = 'test_inputs/test_circuit_circular.csv'
        sites_filename = 'test_inputs/sites_1_gene.csv'
        enzymes_filename = 'test_inputs/enzymes_1.csv'
        environment_filename = 'test_inputs/RNAP_environment.csv'
        output_prefix = 'output'
        frames = 1000
        series = True
        continuation = False
        tm = 'continuum'
        mm = 'uniform'
        dt = 1
        my_circuit = Circuit(circuit_filename, sites_filename, enzymes_filename, environment_filename,
                             output_prefix, frames, series, continuation, dt, )
        # my_circuit.site_list[2].k_min = 0.0
        s0 = my_circuit.superhelical
        t0 = my_circuit.twist
        err = .0000000001

        # This is similar to the Run function... but the idea is that we will control the rate
        for frame in range(1, frames + 1):
            my_circuit.frame = frame
            my_circuit.time = frame * dt
            if my_circuit.series:
                my_circuit.append_sites_to_dict_step1()

            my_circuit.update_global_twist()
            my_circuit.update_global_superhelical()
            if abs(t0 - my_circuit.twist) > err:
                print('error initial, frame', frame)

            # if frame == 10:
            #    my_circuit.site_list[2].k_min = .01

            # if frame == 950:
            #    my_circuit.site_list[2].k_min = .0

            # Apply binding model and get list of new enzymes
            new_enzyme_list = bm.binding_model(my_circuit.enzyme_list, my_circuit.environmental_list, dt,
                                               my_circuit.rng)

            #            if len(new_enzyme_list) > 0:
            #                my_circuit.site_list[2].k_min = 0.0
            my_circuit.add_new_enzymes(new_enzyme_list)  # It also calculates fixes the twists and updates supercoiling

            my_circuit.update_global_twist()
            my_circuit.update_global_superhelical()
            if abs(t0 - my_circuit.twist) > err:
                print('error new_enzymes frame', frame)
            # EFFECT
            # --------------------------------------------------------------
            effects_list = em.effect_model(my_circuit.enzyme_list, my_circuit.environmental_list, dt,
                                           my_circuit.topoisomerase_model, my_circuit.mechanical_model)
            my_circuit.apply_effects(effects_list)

            my_circuit.update_global_twist()
            my_circuit.update_global_superhelical()
            if abs(t0 - my_circuit.twist) > err:
                print('error effects frame', frame)

            # UNBINDING
            drop_list_index, drop_list_enzyme = bm.unbinding_model(my_circuit.enzyme_list,
                                                                   my_circuit.dt, my_circuit.rng)
            my_circuit.drop_enzymes(drop_list_index)
            my_circuit.add_to_environment(drop_list_enzyme)

            # UPDATE GLOBALS
            my_circuit.update_global_twist()
            my_circuit.update_global_superhelical()

            if abs(t0 - my_circuit.twist) > err:
                print('error drop_enzymes, frame', frame)

            # Add to series df if the series option was selected (default=True)
            if series:
                my_circuit.append_enzymes_to_dict()
                my_circuit.append_sites_to_dict_step2(new_enzyme_list, drop_list_enzyme)

        # Output the dataframes: (series)
        if series:
            my_circuit.enzymes_df = pd.DataFrame.from_dict(my_circuit.enzymes_dict_list)
            my_circuit.enzymes_df.to_csv(my_circuit.name + '_enzymes_df.csv', index=False, sep=',')
            my_circuit.sites_df = pd.DataFrame.from_dict(my_circuit.sites_dict_list)
            my_circuit.sites_df.to_csv(my_circuit.name + '_sites_df.csv', index=False, sep=',')

        # Output the log of events
        my_circuit.log.log_out()
        sf = my_circuit.superhelical  # final superhelical
        self.assertLessEqual(abs(s0 - sf), err, "Superhelical changed")

    # Bind unbind with 1 NAP on the left
    def test_bind_unbind_1_RNAP_1_gene_1_NAP_left(self):
        circuit_filename = 'test_inputs/test_circuit_circular.csv'
        sites_filename = 'test_inputs/sites_1_gene_4500.csv'
        enzymes_filename = 'test_inputs/enzymes_1.csv'
        environment_filename = 'test_inputs/RNAP_environment.csv'
        output_prefix = 'output'
        frames = 500
        series = True
        continuation = False
        tm = 'continuum'
        mm = 'uniform'
        dt = 1
        my_circuit = Circuit(circuit_filename, sites_filename, enzymes_filename, environment_filename,
                             output_prefix, frames, series, continuation, dt, )
        # my_circuit.site_list[2].k_min = 0.0
        s0 = my_circuit.superhelical
        t0 = my_circuit.twist
        err = .01

        # This is similar to the Run function... but the idea is that we will control the rate
        for frame in range(1, frames + 1):
            my_circuit.frame = frame
            my_circuit.time = frame * dt
            if my_circuit.series:
                my_circuit.append_sites_to_dict_step1()

            my_circuit.update_global_twist()
            my_circuit.update_global_superhelical()
            if abs(t0 - my_circuit.twist) > err:
                print('error initial, frame', frame)

            # if frame == 100:
            #    my_circuit.site_list[2].k_min = .1

            # Apply binding model and get list of new enzymes
            new_enzyme_list = bm.binding_model(my_circuit.enzyme_list, my_circuit.environmental_list, dt,
                                               my_circuit.rng)

            if len(new_enzyme_list) > 0:
                my_circuit.site_list[2].k_min = 0.0
            my_circuit.add_new_enzymes(new_enzyme_list)  # It also calculates fixes the twists and updates supercoiling

            my_circuit.update_global_twist()
            my_circuit.update_global_superhelical()
            if abs(t0 - my_circuit.twist) > err:
                print('error new_enzymes frame', frame)
            # EFFECT
            # --------------------------------------------------------------
            effects_list = em.effect_model(my_circuit.enzyme_list, my_circuit.environmental_list, dt,
                                           my_circuit.topoisomerase_model, my_circuit.mechanical_model)
            my_circuit.apply_effects(effects_list)

            # UNBINDING
            drop_list_index, drop_list_enzyme = bm.unbinding_model(my_circuit.enzyme_list,
                                                                   my_circuit.dt, my_circuit.rng)
            my_circuit.drop_enzymes(drop_list_index)
            my_circuit.add_to_environment(drop_list_enzyme)

            # UPDATE GLOBALS
            my_circuit.update_global_twist()
            my_circuit.update_global_superhelical()

            if abs(t0 - my_circuit.twist) > err:
                print('error drop_enzymes, frame', frame)

            # Add to series df if the series option was selected (default=True)
            if series:
                my_circuit.append_enzymes_to_dict()
                my_circuit.append_sites_to_dict_step2(new_enzyme_list, drop_list_enzyme)

        # Output the dataframes: (series)
        if series:
            my_circuit.enzymes_df = pd.DataFrame.from_dict(my_circuit.enzymes_dict_list)
            my_circuit.enzymes_df.to_csv(my_circuit.name + '_enzymes_df.csv', index=False, sep=',')
            my_circuit.sites_df = pd.DataFrame.from_dict(my_circuit.sites_dict_list)
            my_circuit.sites_df.to_csv(my_circuit.name + '_sites_df.csv', index=False, sep=',')

        # Output the log of events
        my_circuit.log.log_out()
        sf = my_circuit.superhelical  # final superhelical
        self.assertLessEqual(abs(s0 - sf), err, "Superhelical changed")

    # Bind unbind with 1 NAP on the left and right
    def test_bind_unbind_1_RNAP_1_gene_1_NAP_left_right(self):
        circuit_filename = 'test_inputs/test_circuit_circular.csv'
        sites_filename = 'test_inputs/sites_1_gene_4500.csv'
        enzymes_filename = 'test_inputs/enzymes_2.csv'
        environment_filename = 'test_inputs/RNAP_environment.csv'
        output_prefix = 'output'
        frames = 500
        series = True
        continuation = False
        tm = 'continuum'
        mm = 'uniform'
        dt = 1
        my_circuit = Circuit(circuit_filename, sites_filename, enzymes_filename, environment_filename,
                             output_prefix, frames, series, continuation, dt, )
        # my_circuit.site_list[2].k_min = 0.0
        s0 = my_circuit.superhelical
        t0 = my_circuit.twist
        err = .1

        # This is similar to the Run function... but the idea is that we will control the rate
        for frame in range(1, frames + 1):
            my_circuit.frame = frame
            my_circuit.time = frame * dt
            if my_circuit.series:
                my_circuit.append_sites_to_dict_step1()

            my_circuit.update_global_twist()
            my_circuit.update_global_superhelical()
            if abs(t0 - my_circuit.twist) > err:
                print('error initial, frame', frame)

            # if frame == 100:
            #    my_circuit.site_list[2].k_min = .1

            # if frame == 400:
            #    my_circuit.site_list[2].k_min = 0.0

            # Apply binding model and get list of new enzymes
            new_enzyme_list = bm.binding_model(my_circuit.enzyme_list, my_circuit.environmental_list, dt,
                                               my_circuit.rng)

            # if len(new_enzyme_list) > 0:
            #    my_circuit.site_list[2].k_min = 0.0
            my_circuit.add_new_enzymes(new_enzyme_list)  # It also calculates fixes the twists and updates supercoiling

            my_circuit.update_global_twist()
            my_circuit.update_global_superhelical()
            if abs(t0 - my_circuit.twist) > err:
                print('error new_enzymes frame', frame)
            # EFFECT
            # --------------------------------------------------------------
            effects_list = em.effect_model(my_circuit.enzyme_list, my_circuit.environmental_list, dt,
                                           my_circuit.topoisomerase_model, my_circuit.mechanical_model)
            my_circuit.apply_effects(effects_list)

            # UNBINDING
            drop_list_index, drop_list_enzyme = bm.unbinding_model(my_circuit.enzyme_list,
                                                                   my_circuit.dt, my_circuit.rng)
            my_circuit.drop_enzymes(drop_list_index)
            my_circuit.add_to_environment(drop_list_enzyme)

            # UPDATE GLOBALS
            my_circuit.update_global_twist()
            my_circuit.update_global_superhelical()

            if abs(t0 - my_circuit.twist) > err:
                print('error drop_enzymes, frame', frame)

            # Add to series df if the series option was selected (default=True)
            if series:
                my_circuit.append_enzymes_to_dict()
                my_circuit.append_sites_to_dict_step2(new_enzyme_list, drop_list_enzyme)

        # Output the dataframes: (series)
        if series:
            my_circuit.enzymes_df = pd.DataFrame.from_dict(my_circuit.enzymes_dict_list)
            my_circuit.enzymes_df.to_csv(my_circuit.name + '_enzymes_df.csv', index=False, sep=',')
            my_circuit.sites_df = pd.DataFrame.from_dict(my_circuit.sites_dict_list)
            my_circuit.sites_df.to_csv(my_circuit.name + '_sites_df.csv', index=False, sep=',')

        # Output the log of events
        my_circuit.log.log_out()
        sf = my_circuit.superhelical  # final superhelical
        self.assertLessEqual(abs(s0 - sf), err, "Superhelical changed")

    def test_bind_unbind_many_RNAPs_1_gene(self):
        circuit_filename = 'test_inputs/test_circuit_circular.csv'
        sites_filename = 'test_inputs/sites_1_gene.csv'
        enzymes_filename = 'test_inputs/empty_enzymes.csv'
        environment_filename = 'test_inputs/RNAP_environment.csv'
        output_prefix = 'output'
        frames = 1000
        series = True
        continuation = False
        tm = 'continuum'
        mm = 'uniform'
        dt = 1
        my_circuit = Circuit(circuit_filename, sites_filename, enzymes_filename, environment_filename,
                             output_prefix, frames, series, continuation, dt, )
        # my_circuit.site_list[2].k_min = 0.0
        s0 = my_circuit.superhelical
        t0 = my_circuit.twist
        err = 0.1
        # This is similar to the Run function... but the idea is that we will control the rate
        for frame in range(1, frames + 1):
            # print(frame)
            my_circuit.frame = frame
            my_circuit.time = frame * dt
            if my_circuit.series:
                my_circuit.append_sites_to_dict_step1()

            my_circuit.update_global_twist()
            my_circuit.update_global_superhelical()
            if abs(t0 - my_circuit.twist) > err:
                print('error initial, frame', frame)
            if abs(my_circuit.enzyme_list[0].twist - my_circuit.enzyme_list[-2].twist) > err:
                print('issue initial, frame', frame)

            # if frame == 100:
            #    my_circuit.site_list[2].k_min = .05
            # elif frame == 900:
            #    my_circuit.site_list[2].k_min = 0.0

            # Apply binding model and get list of new enzymes
            new_enzyme_list = bm.binding_model(my_circuit.enzyme_list, my_circuit.environmental_list, dt,
                                               my_circuit.rng)

            my_circuit.add_new_enzymes(new_enzyme_list)  # It also calculates fixes the twists and updates supercoiling

            t2 = my_circuit.twist + 2
            ss = my_circuit.enzyme_list[0].twist
            s1 = sum(enzyme.twist for enzyme in my_circuit.enzyme_list)
            my_circuit.update_global_twist()
            t3 = my_circuit.twist + 3
            my_circuit.update_global_superhelical()
            if abs(t0 - my_circuit.twist) > err:
                print('new enzyme, frame', frame)
            if abs(my_circuit.enzyme_list[0].twist - my_circuit.enzyme_list[-2].twist) > err:
                print('issue new enzyme, frame', frame)

            # EFFECT
            # --------------------------------------------------------------
            effects_list = em.effect_model(my_circuit.enzyme_list, my_circuit.environmental_list, dt,
                                           my_circuit.topoisomerase_model, my_circuit.mechanical_model)
            my_circuit.apply_effects(effects_list)

            my_circuit.update_global_twist()
            my_circuit.update_global_superhelical()
            if abs(t0 - my_circuit.twist) > err:
                print('effects, frame', frame)
            if abs(my_circuit.enzyme_list[0].twist - my_circuit.enzyme_list[-2].twist) > err:
                print('issue effects, frame', frame)

            # UNBINDING
            drop_list_index, drop_list_enzyme = bm.unbinding_model(my_circuit.enzyme_list,
                                                                   my_circuit.dt, my_circuit.rng)
            my_circuit.drop_enzymes(drop_list_index)

            my_circuit.update_global_twist()
            my_circuit.update_global_superhelical()
            if abs(t0 - my_circuit.twist) > err:
                print('error initial, frame', frame)
            if abs(my_circuit.enzyme_list[0].twist - my_circuit.enzyme_list[-2].twist) > err:
                print('issue initial, drop', frame)
            my_circuit.add_to_environment(drop_list_enzyme)

            # UPDATE GLOBALS
            my_circuit.update_global_twist()
            my_circuit.update_global_superhelical()
            if abs(t0 - my_circuit.twist) > err:
                print('Adding to the environment, frame', frame)
            if abs(my_circuit.enzyme_list[0].twist - my_circuit.enzyme_list[-2].twist) > err:
                print('issue environment, frame', frame)

            # Add to series df if the series option was selected (default=True)
            if series:
                my_circuit.append_enzymes_to_dict()
                my_circuit.append_sites_to_dict_step2(new_enzyme_list, drop_list_enzyme)

        # Output the dataframes: (series)
        if series:
            my_circuit.enzymes_df = pd.DataFrame.from_dict(my_circuit.enzymes_dict_list)
            my_circuit.enzymes_df.to_csv(my_circuit.name + '_enzymes_df.csv', index=False, sep=',')
            my_circuit.sites_df = pd.DataFrame.from_dict(my_circuit.sites_dict_list)
            my_circuit.sites_df.to_csv(my_circuit.name + '_sites_df.csv', index=False, sep=',')

        # Output the log of events
        my_circuit.log.log_out()
        sf = my_circuit.superhelical  # final superhelical
        self.assertLessEqual(abs(s0 - sf), err, "Superhelical changed")

    def test_topo_gyra_0_enzymes(self):
        circuit_filename = 'test_inputs/test_circuit_circular.csv'
        sites_filename = 'test_inputs/sites_1_gene.csv'
        enzymes_filename = 'test_inputs/empty_enzymes.csv'
        environment_filename = 'test_inputs/environment.csv'
        output_prefix = 'output'
        frames = 5000
        series = True
        continuation = False
        tm = 'continuum'
        mm = 'uniform'
        dt = 10
        my_circuit = Circuit(circuit_filename, sites_filename, enzymes_filename, environment_filename,
                             output_prefix, frames, series, continuation, dt, )
        # my_circuit.site_list[2].k_min = 0.0
        # This is similar to the Run function... but the idea is that we will control the rate
        for frame in range(1, frames + 1):
            my_circuit.frame = frame
            my_circuit.time = frame * dt
            if my_circuit.series:
                my_circuit.append_sites_to_dict_step1()

            # Apply binding model and get list of new enzymes
            new_enzyme_list = bm.binding_model(my_circuit.enzyme_list, my_circuit.environmental_list, dt,
                                               my_circuit.rng)

            my_circuit.add_new_enzymes(new_enzyme_list)  # It also calculates fixes the twists and updates supercoiling

            # EFFECT
            # --------------------------------------------------------------
            effects_list = em.effect_model(my_circuit.enzyme_list, my_circuit.environmental_list, dt,
                                           my_circuit.topoisomerase_model, my_circuit.mechanical_model)
            my_circuit.apply_effects(effects_list)

            # UNBINDING
            drop_list_index, drop_list_enzyme = bm.unbinding_model(my_circuit.enzyme_list,
                                                                   my_circuit.dt, my_circuit.rng)
            my_circuit.drop_enzymes(drop_list_index)

            # UPDATE GLOBALS
            my_circuit.update_global_twist()
            my_circuit.update_global_superhelical()

            # Add to series df if the series option was selected (default=True)
            if series:
                my_circuit.append_enzymes_to_dict()
                my_circuit.append_sites_to_dict_step2(new_enzyme_list, drop_list_enzyme)

        # Output the dataframes: (series)
        if series:
            my_circuit.enzymes_df = pd.DataFrame.from_dict(my_circuit.enzymes_dict_list)
            my_circuit.enzymes_df.to_csv(my_circuit.name + '_enzymes_df.csv', index=False, sep=',')
            my_circuit.sites_df = pd.DataFrame.from_dict(my_circuit.sites_dict_list)
            my_circuit.sites_df.to_csv(my_circuit.name + '_sites_df.csv', index=False, sep=',')

        # Output the log of events
        my_circuit.log.log_out()
        sf = my_circuit.superhelical  # final superhelical

    #        self.assertLessEqual(abs(s0-sf), err, "Superhelical changed")

    def test_bind_unbind_same_time(self):
        circuit_filename = 'test_inputs/test_circuit_circular.csv'
        sites_filename = 'test_inputs/sites_1_gene.csv'
        enzymes_filename = 'test_inputs/empty_enzymes.csv'
        environment_filename = 'test_inputs/RNAP_environment.csv'
        output_prefix = 'output'
        frames = 100
        series = True
        continuation = False
        tm = 'continuum'
        mm = 'uniform'
        dt = 1
        my_circuit = Circuit(circuit_filename, sites_filename, enzymes_filename, environment_filename,
                             output_prefix, frames, series, continuation, dt, )
        my_circuit.site_list[1].k_min = 0.0
        for site in my_circuit.site_list:  # I'll increase the rates
            site.k_min = site.k_min * 0
        # Let's make the rates
        s0 = my_circuit.superhelical
        t0 = my_circuit.twist
        err = 0.00001
        enzyme1 = Enzyme(e_type=my_circuit.environmental_list[0].enzyme_type,
                         name=my_circuit.environmental_list[0].name, site=my_circuit.site_list[1],
                         position=my_circuit.site_list[1].start,
                         size=my_circuit.environmental_list[0].size, twist=0.0, superhelical=0.0, k_cat=0, k_off=0)

        enzyme2 = Enzyme(e_type=my_circuit.environmental_list[0].enzyme_type,
                         name=my_circuit.environmental_list[0].name, site=my_circuit.site_list[1],
                         position=my_circuit.site_list[1].start + 500,
                         size=my_circuit.environmental_list[0].size, twist=0.0, superhelical=0.0, k_cat=0, k_off=0)

        # This is similar to the Run function... but the idea is that we will control the rate
        for frame in range(1, frames + 1):
            # print(frame)
            my_circuit.frame = frame
            my_circuit.time = frame * dt
            if my_circuit.series:
                my_circuit.append_sites_to_dict_step1()

            my_circuit.update_global_twist()
            my_circuit.update_global_superhelical()
            if abs(t0 - my_circuit.twist) > err:
                print('error initial, frame', frame)
            if abs(my_circuit.enzyme_list[0].twist - my_circuit.enzyme_list[-2].twist) > err:
                print('issue initial, frame', frame)

            if frame == 5:
                new_enzyme_list = [enzyme1, enzyme2]
            else:
                new_enzyme_list = []

            # Apply binding model and get list of new enzymes
            # new_enzyme_list = bm.binding_model(my_circuit.enzyme_list, my_circuit.environmental_list, dt)

            my_circuit.add_new_enzymes(new_enzyme_list)  # It also calculates fixes the twists and updates supercoiling

            t2 = my_circuit.twist + 2
            ss = my_circuit.enzyme_list[0].twist
            s1 = sum(enzyme.twist for enzyme in my_circuit.enzyme_list)
            my_circuit.update_global_twist()
            t3 = my_circuit.twist + 3
            my_circuit.update_global_superhelical()
            if abs(t0 - my_circuit.twist) > err:
                print('new enzyme, frame', frame)
            if abs(my_circuit.enzyme_list[0].twist - my_circuit.enzyme_list[-2].twist) > err:
                print('issue new enzyme, frame', frame)

            # EFFECT
            # --------------------------------------------------------------
            effects_list = em.effect_model(my_circuit.enzyme_list, my_circuit.environmental_list, dt,
                                           my_circuit.topoisomerase_model, my_circuit.mechanical_model)
            my_circuit.apply_effects(effects_list)

            my_circuit.update_global_twist()
            my_circuit.update_global_superhelical()
            if abs(t0 - my_circuit.twist) > err:
                print('effects, frame', frame)
            if abs(my_circuit.enzyme_list[0].twist - my_circuit.enzyme_list[-2].twist) > err:
                print('issue effects, frame', frame)

            # UNBINDING
            drop_list_index, drop_list_enzyme = bm.unbinding_model(my_circuit.enzyme_list,
                                                                   my_circuit.dt, my_circuit.rng)
            my_circuit.drop_enzymes(drop_list_index)

            my_circuit.update_global_twist()
            my_circuit.update_global_superhelical()
            if abs(t0 - my_circuit.twist) > err:
                print('error initial, frame', frame)
            if abs(my_circuit.enzyme_list[0].twist - my_circuit.enzyme_list[-2].twist) > err:
                print('issue initial, drop', frame)
            my_circuit.add_to_environment(drop_list_enzyme)

            # UPDATE GLOBALS
            my_circuit.update_global_twist()
            my_circuit.update_global_superhelical()
            if abs(t0 - my_circuit.twist) > err:
                print('Adding to the environment, frame', frame)
            if abs(my_circuit.enzyme_list[0].twist - my_circuit.enzyme_list[-2].twist) > err:
                print('issue environment, frame', frame)

            # Add to series df if the series option was selected (default=True)
            if series:
                my_circuit.append_enzymes_to_dict()
                my_circuit.append_sites_to_dict_step2(new_enzyme_list, drop_list_enzyme)

        # Output the dataframes: (series)
        if series:
            my_circuit.enzymes_df = pd.DataFrame.from_dict(my_circuit.enzymes_dict_list)
            my_circuit.enzymes_df.to_csv(my_circuit.name + '_enzymes_df.csv', index=False, sep=',')
            my_circuit.sites_df = pd.DataFrame.from_dict(my_circuit.sites_dict_list)
            my_circuit.sites_df.to_csv(my_circuit.name + '_sites_df.csv', index=False, sep=',')

        # Output the log of events
        my_circuit.log.log_out()
        sf = my_circuit.superhelical  # final superhelical
        self.assertLessEqual(abs(s0 - sf), err, "Superhelical changed")
