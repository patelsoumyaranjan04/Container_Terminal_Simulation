

import simpy
from vessel import Vessel
from config import *
import random

class Simulation:
    def __init__(self, simulation_time):
        self.env = simpy.Environment()
        self.simulation_time = simulation_time
        self.berth_resource = simpy.Resource(self.env, capacity=NUM_BERTHS)
        self.crane_resource = simpy.Resource(self.env, capacity=NUM_CRANES)
        self.truck_resource = simpy.Resource(self.env, capacity=NUM_TRUCKS)
        
    def generate_vessels(self):
        vessel_id = 1
        while True:
            yield self.env.timeout(random.expovariate(1 / (AVERAGE_INTERARRIVAL_TIME * 60)))  # Time between arrivals of vessels
            vessel = Vessel(self.env, vessel_id, self.berth_resource, self.crane_resource, self.truck_resource)
           
            self.env.process(vessel.process())
            vessel_id += 1
           
            
    def run(self):
        """
        Run the simulation
        """
        self.env.process(self.generate_vessels())
        self.env.run(until=self.simulation_time)