#  
# Author    : ACIMS(Arizona Centre for Integrative Modeling & Simulation)
#           : Vamsi Krishna Satyanarayana Vasa and Hessam S. Sarjoughian
# Version   : 1.0 
# Date      : 06-21-25 
#

Pretend you are a teacher of a class named "discrete event simulation" giving your students a set of simple facts about a given DEVS modelization. These statements must be a complete and correct list of simple-to-understand facts that describe all the problem restrictions and requirements.  

Including technical information, like which are the DEVS atomic model's ports, internal, external and confluent transition functions, time advance values.

In case of Coupled models, include which are the components to be considered, the DEVS coupled model's ports, internal and external couplings clearly. internal couplings are the connections between the components and external couplings are the connections between the coupled model itself and components. For example, consider a Controller-Light-Sensor system, where Light-Sensor is a coupled model and Controller is connected to this coupled model. Then the internal coupling are the connections between Light and Sensor and External couplings are the connections between Light-Sensor coupled model and Light, and Sensor atomic components.  

AFTER A MODIFICATION IS REQUESTED, SPECIFY ATOMIC MODEL'S STATE VARIABLES, CONNECTIONS, FUNCTIONS, ETC.
THAT IS: ALWAYS PROVIDE THE COMPLETE ATOMIC/COUPLED MODEL DESCRIPTION, SKIP NO DETAIL.
The statements should be generated such that they are compliant with the PDEVS variant, a subset of DEVS described below:
- If you notice a coupled model only give the facts of the atomic components one after the other.
- If you notice a hierarchy of the coupled models give the facts for all the coupled models seperately. Start with the lower hirarchical coupled model and then use this generated coupled model as the atomic model to generate the higher hirarchical coupled models. This is to be followed very importantly.  
- Instead of an atomic model having a fixed time advance variable, it defines a time advance function that dynamically computes the next scheduled event time based on the current state and other influencing factors. This function is evaluated at each state transition, ensuring that the system accounts for external and internal events concurrently, as per the PDEVS formalism.
- Remember that the external transition function is executed when any message from any port is received by the atomic model.
- The output function is executed right after the internal transition function. But not after the external transition function.
- Remember that the confluent transition function is executed when the messages arrive at any input port and any output port at the same time.
- You can force the internal transition function to run immediately by setting the time advance value to 0.
- If the time advance value is 0 and remains unchanged, an infinite loop will occur. You should make certain this does not happen.
- The `lambda` word is reserved in Python and should be changed in specifications to avoid overlapping the keyword.


# Example atomic and coupled model facts

- SYSTEM DESCRIPTION: 

We have a module named generator that sends jobs to a proessor with queue. The generator must send only three jobs at 11th, 13th and 17th second once the simulation starts. The initial state of the processor is passive. Once job signal is sent to the processor, processor takes 2 clocks to process the job send it to the output port. Proceessor will maintain the state busy during proccessing and will return to passive after processing the job. This condition can be achieved through confluence transition function. The jobs that are not ready for the processing will wait in the queue until the processor comes out of busy state.

- GENERATED FACTS:
```
Here is the complete system description for the DEVS modelization of the given problem, following the DEVS specifications:

### Coupled Model: root
- This is the root model that contains instances of the atomic models `Generator` and `Processor`.
- **Ports:**
  - Input Port: None (as this is the overall system and there is no hierarchy above this.)
  - Output Port: None (as this is the overall system and there is no hierarchy above this.)
- **Internal Couplings:**
  - The `Generator` sends job signals to the `Processor`.
  - The `Processor` outputs processed jobs.
- **External Couplings:**
  - None (as this is the overall system and there is no hierarchy above this.)
  
### Atomic Model: Generator
- **Ports:**
  - Output Port: `job_out`
- **State Variables:**
  - `time_advance`: Initially set to 0 (to allow immediate transitions).
  - `job_count`: Initially set to 0 (to count the number of jobs sent).
- **Transition Functions:**
  - **Internal Transition Function (delta_int):**
	- Increment `job_count`.
    - If `job_count` < 3, set `time_advance` to the next scheduled job time (11, 13, or 17 seconds).
    - If `job_count` = 3, set `time_advance` to infinity (to stop sending jobs).
  - **External Transition Function (delta_ext):**
	- Not applicable for this model since it does not receive any messages.  
  - **Output Function (lambda_out):**    
	- Send a job signal to `job_out` when `job_count` is 1, 2, or 3.
  - **Confluent Transition Function (delta_conf):**
    - Execute the internal transition function and output function if a message arrives at the same time.

### Atomic Model: Processor
- **Ports:**
  - Input Port: `job_in`
  - Output Port: `processed_job_out`
- **State Variables:**
  - `time_advance`: Initially set to 2 (the processing time).
  - `state`: Initially set to `passive` (indicating the processor is not busy).
- **Transition Functions:**
  - **Internal Transition Function (delta_int):**
    - Change `state` to `passive`.
    - Set `time_advance` to 2 (to prepare for the next job).
  - **External Transition Function (delta_ext):**
    - If a job is received at `job_in`, change `state` to `busy` and set `time_advance` to 2 (indicating processing time).
  - **Output Function (lambda_out):**
    - Send a processed job signal to `processed_job_out` when transitioning from `busy` to `passive`.
  - **Confluent Transition Function (delta_conf):**
    - If a job is received while in `busy` state, process the job and immediately transition to `passive` after processing.

### Summary of Execution Flow
1. The `Generator` sends a job signal at 11, 13, and 17 seconds.
2. The `Processor` processes the job for 2 seconds, transitioning to `busy` state during processing.
3. Once processing is complete, the `Processor` transitions back to `passive` state and sends the processed job signal.
4. If the `Processor` is busy and a new job arrives, it will wait until the processing is complete.

### Important Notes
- Ensure that the `time_advance` for the `Generator` is properly set to avoid an infinite loop. 
- The `Processor` must not set its `time_advance` to 0 unless it is transitioning to `passive` to avoid infinite loops. 
- The `lambda` keyword has been avoided in the output function naming.
```

# Example coupled model facts for the systems with hierarchy

- SYSTEM DESCRIPTION: 

We have a module named controller that sends on and off signals to a light-sensor system. The controller must send these commands after every second. The initial state of the light is off and the controller will auto-start the cycle 10 seconds after the simulation start. Once started the toggling should never end. The sensor to this setup is added to know if the light is on or off. The light-sensor system will provide the feedback to the controller component.

- GENERATED FACTS:
```
### Coupled Model: Light-Sensor
- This is the coupled model that contains the details about the Light-Sensor system.
- **Ports:**
  - Input Port: in
  - Output Port: out
- **Internal Couplings:**
  - The output port of `Light` component is connected to the input port of Sensor.
- **External Couplings:**
  - The `in` port of the `Light-Sensor` coupled model is connected to the input port of the `Light` component.
  - The output port of the `Sensor` component is connected to the `out` port of the `Light-Sensor` component.

### Coupled Model: Root
- This is the coupled model that contains the details about the overall system.
- **Ports:**
  - Input Port: None (as this is the overall system and there is no hierarchy above this.)
  - Output Port: None (as this is the overall system and there is no hierarchy above this.)
- **Internal Couplings:**
  - The output port of `Generator` component is connected to the input port of `Light-Sensor`.
  - The output port of `Light-Sensor` component is connected to the input port of `Generator`.
- **External Couplings:**
  - None (as there are no Ports for this coupled model).
```

FOR COUPLED MODELS PROVIDE THE FACTS FOR THE LOWER HIERARCHICAL COUPLED MODELS FIRST, THEN GO UP THE HIERARCHY.