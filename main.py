
import simpy
from simulation import Simulation
import config

def main():
    try:
       # Get user input for simulation parameters
        simulation_hours = int(input("Enter the number of hours to run the simulation: "))
   
        simulation_minutes = simulation_hours * 60

        # Validate inputs
        if simulation_minutes <= 0 or config.AVERAGE_INTERARRIVAL_TIME <= 0:
            raise ValueError("Simulation time and interarrival time must be positive values.")

        simulation = Simulation(simulation_minutes)
        simulation.run()
        

    except ValueError as e:
        print(f"Error: {e}")
        raise

if __name__ == "__main__":
    main()
