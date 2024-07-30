# Container Terminal Simulation

This project simulates the operations of a port terminal using SimPy, focusing on the unloading process of containers from vessels using cranes and trucks. The simulation models the arrival of vessels, the berthing process, the unloading of containers using cranes, and the transportation of containers by trucks.

## Table of Contents

- [Introduction](#Introduction)
- [Project Structure](#Project-Structure)
- [Installation](#Installation)
- [Configuration](#Configuration) 
- [Usage](#Usage)
- [Simulation Details](#Simulation-Details) 
- [License](#License)

## Introduction

This project is designed to provide a detailed simulation of port terminal operations, including vessel berthing, crane unloading, and truck transportation. 

## Project Structure
The project consists of the following main components:

- `main.py`: The entry point of the simulation. It handles user inputs and initiates the simulation.
- `config.py`: Contains configurable parameters for the simulation.
- `vessel.py`: Defines the Vessel class, which simulates the berthing and unloading process of a vessel.
- `simulation.py`: Defines the Simulation class, which sets up the environment and runs the simulation.

## Installation
To run this project, ensure you have Python installed. Follow these steps to set up the environment:

1. Clone the repository
```
git clone https://github.com/patelsoumyaranjan04/Container_Terminal_Simulation.git
cd Container_Terminal_Simulation
```
2. Create a virtual environment (optional but recommended):
```
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

```
3. Install the required packages:
```
pip install -r requirements.txt

```

## Configuration
The simulation parameters can be adjusted in the `config.py` file. 

Here are the default settings:


```
# Configurable parameters

# Vessel parameters
AVERAGE_INTERARRIVAL_TIME = 5  # Average interarrival time in hours
NUM_CONTAINERS = 150 # Number of containers per vessel

# Terminal resources
NUM_BERTHS = 2  # Number of berth slots
NUM_CRANES = 2  # Number of quay cranes
CRANES_PER_BERTH=1 #Number of cranes per berth
CRANE_LIFT_TIME = 3  # Time to lift one container in minutes

# Truck parameters
NUM_TRUCKS = 3  # Number of trucks
TRUCK_CYCLE_TIME = 6  # Time for truck to drop off container and return in minutes


```

## Usage
Run the simulation using the main.py script. You will be prompted to enter the number of hours to run the simulation:

```
python main.py

```
Example Input

```
Enter the number of hours to run the simulation: 24

```
## Simulation Details
### Vessel Class (`vessel.py`)

- **berth:** Simulates the vessel berthing process, manages the allocation of cranes, and waits for all cranes to complete the unloading process.
- **transport_container:** Manages the transportation of a container by a truck from the vessel to the storage yard.
- **unload:** Manages the unloading of all containers from the vessel using cranes, and requests trucks for transporting the containers. It ensures cranes operate efficiently without waiting for truck availability.
- **process:** Coordinates the entire sequence of arrival, berthing, and unloading of the vessel.

### Simulation Class (`simulation.py`)

- **init:** Sets up the simulation environment and resources.
- **generate_vessels:** Generates vessels arriving at the port based on the average interarrival time.
- **run:** Runs the simulation for the specified duration.

### Example Output
The simulation will produce output similar to the following, detailing the progress of vessel berthing, container unloading, and transportation:

```
Enter the number of hours to run the simulation: 5
Time 277.60: Vessel 1 has arrived at port.
Time 277.60: Vessel 1 starts berthing.
Time 277.60: Vessel 1 has acquired a crane
Time 277.60: Crane starts unloading  Container 1 from Vessel 1
Time 280.60: Crane finished unloading  Container 1 from Vessel 1
Time 280.60: Container 1 from Vessel 1 is waiting for a truck
Time 280.60: Container 1 from Vessel 1 has acquired a truck
Time 280.60: Crane starts unloading  Container 2 from Vessel 1
Time 280.60: Truck starts transporting container 1 from vessel 1.
Time 283.60: Crane finished unloading  Container 2 from Vessel 1
Time 283.60: Container 2 from Vessel 1 is waiting for a truck
Time 283.60: Container 2 from Vessel 1 has acquired a truck
Time 283.60: Crane starts unloading  Container 3 from Vessel 1
Time 283.60: Truck starts transporting container 2 from vessel 1.
```

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

