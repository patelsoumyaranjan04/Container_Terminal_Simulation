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
        self.truck_store = simpy.Store(self.env, capacity=3)
     
    
    def generate_vessels(self):
        vessel_id = 1
        while True:
            yield self.env.timeout(random.expovariate(1 / (AVERAGE_INTERARRIVAL_TIME * 60)))  # time between arrivals
            vessel = Vessel(self.env, vessel_id, self.berth_resource, self.crane_resource, self.truck_resource,self.truck_store)
            print(f"Time {self.env.now}: Vessel {vessel_id} arrives.")
            self.env.process(vessel.process())
            
            vessel_id += 1
           
            
    def run(self):
        """Run the simulation"""
        for _ in range(3):  # Initialize with 3 trucks
            self.truck_store.put(f"Truck {_ + 1}")
        self.env.process(self.generate_vessels())
        self.env.run(until=self.simulation_time)

