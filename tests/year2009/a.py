"""Tests corresponding to the 2009 QSNMC competition, Challenge A."""

import numpy as np
import sciunit
import sciunit.scores

from ..capabilites import TrainVoltageOnCurrent
from ..comparators import SpikeTrainComparator

####################
# Tests to execute #
####################

# Training data.
current,voltage = load_training_data()  
training = SpikeTrainComparisonTest(observation=voltage,
                                    name="Training Data")

# Test data. Using training data until security is worked out.    
current,voltage = load_training_data() 
test = SpikeTrainComparisonTest(observation=voltage,
                                    name="Test Data")

# Two tests, one indicating agreement with training data, and one indicating
# agreement with test data.  A leaderboard can be constructed from the training 
# data, but the real leaderboard will use the test data.  
tests = [training,test]

###################
# Available Tests #
###################

# Could be moved to neuronunit.tests.  

class SpikeTrainComparisonTest(sciunit.Test):
    """Compares spike trains for concordance of spike times."""

    def __init__(self,
                 observation={'spike_trains':None},
                 name="Spike train comparison test",
                 params={'dt':0.0001, 'T':None, 'method':'Rect'}):
        """
        observation['spike_trains']: a list of spike trains, where each spike 
                                     train is a list of spike times.
        params['dt']: The sampling interval for generating spike count arrays. 
        params['T']: Spike count array will be generated by observed spike 
                     trains from 0 to T seconds.  Defaults to last spike time
                     rounded up to the nearest second.  
        params['method']: 'Rect' or 'Kistler', corresponding to two methods for 
                          computing MDstar.  
        """

        Test.__init__(self,observation,name)
        self.required_capabilities += (ProducesSpikeTrain)

    description = "A test of of the similarity of spike trains."

    score_type = sciunit.scores.PercentScore

    def validate_observation(self, observation):
        try:
            assert type(observation) is dict
            assert type(observation['spike_trains']) is list
            for spike_train in observation['spike_trains']:
                assert type(spike_train) is list
        except AssertionError,e:
            raise sciunit.ObservationError("Observation must be of the form \
                {'spike_trains':[s1a,s1b,...],[s2a,s2b,...]."
        try:
            for spike_train in observation['spike_trains']:
                for spike_time in spike_train:
                    assert type(spike_time) is float
        except:
            raise sciunit.ObservationError("Each observed spike time must be \
                a float."

    def generate_prediction(self, model):
        """Implementation of sciunit.Test.generate_prediction."""
        model.inject_current(self.observation.current) 
        model_spike_trains = model.get_spike_trains()
        prediction = {'spike_trains':model_spike_trains}
        return prediction

    def compute_score(self, observation, prediction):
        """Implementation of sciunit.Test.score_prediction."""
        observed = observation['spike_trains']
        predicted = prediction['spike_trains']
        comparator = SpikeTrainComparator(observed,predicted)
        comparator.compute = getattr(comparator,"computeMD_%s" % method)
        delta = params['delta']
        dt = params['dt']
        MDstar = comparator.compute(delta, dt) 
        score = PercentScore(MDstar / 100.0)
        score.related_data.update(self.params)
        return score

#######################
# Auxiliary Functions #
#######################

def load_testing_data():
    pass # Not implemented until security is worked out.  
