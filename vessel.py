import simpy
from config import NUM_CONTAINERS, CRANE_LIFT_TIME, TRUCK_CYCLE_TIME

class Vessel:
    def __init__(self, env, id, berth_resource, crane_resource, truck_resource, truck_store):
        self.env = env
        self.id = id
        self.containers = NUM_CONTAINERS
        self.berth_resource = berth_resource
        self.crane_resource = crane_resource
        self.truck_resource = truck_resource
        self.truck_store = truck_store
        

    def berth(self):
        """Simulate vessel berthing"""
        with self.berth_resource.request() as request:
            yield request
            print(f"Time {self.env.now}: Vessel {self.id} starts berthing.")
            yield self.env.process(self.unload())
    
    
    def unload_container(self, container_id):
        """Unload a single container and request a truck"""
        # Ensure the crane is available
        with self.crane_resource.request() as crane_request:
            yield crane_request
            print(f"Time {self.env.now}: Crane starts unloading container {container_id + 1} from vessel {self.id}.")
            yield self.env.timeout(CRANE_LIFT_TIME)  # Crane time to unload one container
            print(f"Time {self.env.now}: Crane finished unloading container {container_id + 1} from vessel {self.id}.")

           
                # Request a truck to transport the container
            with self.truck_resource.request() as truck_request:
                yield truck_request
                print(f"Time {self.env.now}: Truck assigned to container {container_id + 1} from vessel {self.id}.")
                
                # Get a truck from the store
                truck = yield self.truck_store.get()
                
                # Start the transport process for this container
                self.env.process(self.transport_container(container_id, truck))
            
            # Continue unloading the next container if there are still containers to unload
            if self.containers > 0:
                self.env.process(self.unload_next_container())

    def transport_container(self, container_id, truck):
        """Transport the container using a truck"""
        print(f"Time {self.env.now}: Truck starts transporting container {container_id + 1} from vessel {self.id}.")
        yield self.env.timeout(TRUCK_CYCLE_TIME)  # Truck time to transport the container
        print(f"Time {self.env.now}: Truck finished transporting container {container_id + 1} from vessel {self.id}.")

        

        # Return the truck to the truck store after transport is complete
        yield self.truck_store.put(truck)
      

    def unload_next_container(self):
        """Unload the next container if there are still containers left"""
        if self.containers > 0:
            container_id = NUM_CONTAINERS - self.containers
            self.containers -= 1
            yield self.env.process(self.unload_container(container_id))

    def unload(self):
        """Unload all containers from the vessel"""
        if self.containers > 0:
            yield self.env.process(self.unload_next_container())

        

    def process(self):
        """Process the entire sequence of arrival, berthing, and unloading"""
        yield self.env.process(self.berth())



