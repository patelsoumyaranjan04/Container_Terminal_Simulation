import random
import simpy
from config import NUM_CONTAINERS, CRANE_LIFT_TIME, TRUCK_CYCLE_TIME,CRANES_PER_BERTH

class Vessel:
    def __init__(self, env, id, berth_resource, crane_resource, truck_resource):
        
        """
        Initialize a Vessel instance.

        :param env: The simulation environment.
        :param id: The unique ID of the vessel.
        :param berth_resource: The berth resource shared among vessels.
        :param crane_resource: The crane resource shared among vessels.
        :param truck_resource: The truck resource shared among vessels.
        
        """

        self.env = env
        self.id = id
        self.containers = NUM_CONTAINERS
        self.berth_resource = berth_resource
        self.crane_resource = crane_resource
        self.truck_resource = truck_resource
        
        

    def berth(self):
        """
        Simulate vessel berthing and initiate unloading.
        """
        print(f"Time {self.env.now:.2f}: Vessel {self.id} has arrived at port.")
        with self.berth_resource.request() as request: 
            yield request
            print(f"Time {self.env.now:.2f}: Vessel {self.id} starts berthing.")

            # Create an event to signal when unloading is complete
            unload_done_event = self.env.event()

            # Start the unloading process with the available cranes
            cranes= [self.env.process(self.unload(unload_done_event))
                        for _ in range(CRANES_PER_BERTH)
            ]

            # Wait for all the cranes to finish
            yield self.env.all_of(cranes)

            
        print(f"Time {self.env.now:.2f}: Vessel {self.id} finished unloading and leaves the berth.")

    def unload(self, unload_done_event):
        """
        Unload all containers from the vessel using the assigned crane.

        :param unload_done_event: Event to signal unloading completion.
        """        
        
        with self.crane_resource.request() as crane_request:
               
            yield self.env.any_of([crane_request, unload_done_event])

            if( not unload_done_event.triggered):
                # Have a crane, start unloading containers
                print(f'Time {self.env.now:.2f}: Vessel {self.id} has acquired a crane')

                while self.containers > 0 :
                    # get a container
                    self.containers-=1

                    container_id=NUM_CONTAINERS - self.containers

                    print(f'Time {self.env.now:.2f}: Crane starts unloading  Container {container_id} from Vessel {self.id} ')
                    
                    yield self.env.timeout(CRANE_LIFT_TIME)

                    print(f'Time {self.env.now:.2f}: Crane finished unloading  Container {container_id} from Vessel {self.id} ')
                    

                    # Request a truck to transport the container
                    truck_request = self.truck_resource.request()

                    print(f'Time {self.env.now:.2f}: Container {container_id} from Vessel {self.id} is waiting for a truck')
                    
                    yield truck_request
                    
                    print(f'Time {self.env.now:.2f}: Container {container_id} from Vessel {self.id} has acquired a truck')
                    
                    # Start the transport process 
                    self.env.process(self.transport_container(container_id, truck_request))

                # Signal that unloading is complete
                if not unload_done_event.triggered:
                    unload_done_event.succeed()



    def transport_container(self,container_id,truck_request):
        """
        Simulate the transport of a container by a truck.

        :param container_id: The ID of the container being transported.
        :param truck_request: The truck resource request object.
        """
        print(f"Time {self.env.now:.2f}: Truck starts transporting container {container_id} from vessel {self.id}.")
       
        yield self.env.timeout(TRUCK_CYCLE_TIME)  # Truck time to transport the container
        
        print(f"Time {self.env.now:.2f}: Truck finished transporting container {container_id} from vessel {self.id}.")
       
        yield self.truck_resource.release(truck_request)
        
       
        
       

    def process(self):
        """
        Process the entire sequence of arrival, berthing, and unloading.
        """        
        yield self.env.process(self.berth())


