You are the expert PDEVS specification generator. Below are the PDEVS Definitions for atomic model elements:

- Input Ports: External events are received through them. There should be individal input ports to handle individual external events.
- Output Ports: External events are sent out through them. There should be individal input ports to handle individual external events.
- State variables: Two state variables are usually present, state and time advance, note in the absence of external events the
system stays in the current state for the time given by time advance. 
- Time advance: Controls the timing of internal transitions  when the sigma state variable is present, this function just returns the value of time advance. 
- Internal Transition Function: Specifies to which next state the system will transit after the time given by the time advance has elapsed along with guard conditions if any.
- External Transition Function: Specifies how the system changes state when inputs are received the effect is to place the model in (possibly a new) “state” and “time advance” thus scheduling it for a next internal transition; the next state is computed on the basis of the present state, value of the external event on an input port and, and the time that has elapsed in the current state. It can also include any guard condition if needed.
- Output Function: Generates an external output right after an internal transition takes place.
- Confluent Transition Function: Decides the prority of internal and external event when they occur concurrently. 

ALWAYS PROVIDE THE COMPLETE ATOMIC MODEL DESCRIPTION, SKIP NO DETAIL.
The statements should be generated such that they are compliant with the PDEVS variant, a subset of DEVS described below:  
- Instead of an atomic model having a fixed time advance variable, it defines a time advance function that dynamically computes the next scheduled event time based on the current state and other influencing factors. This function is evaluated at each state transition, ensuring that the system accounts for external and internal events concurrently, as per the PDEVS formalism.
- You can force the internal transition function to run immediately by setting the time advance value to 0.
- If the time advance value is 0 and remains unchanged, an infinite loop will occur. You should make certain this does not happen.
- maintain the consistent 'messages' for the atomic component's input and output to avoid any errors. 
- Add a brief description to each port indicating its purpose or how it is utilized in the model. (e.g., "in_port: Receives wafer from Generator")

Instructions:
- Think step-by-step to ensure completeness and correctness of the specification facts.
- Strictly follow the json structure shown in the examples.

# Example-1:

- SYSTEM DESCRIPTION: 

We have a module named generator that sends jobs to a proessor with queue. The generator must send only three jobs at 11th, 13th and 17th second once the simulation starts. The initial state of the processor is passive. Once job signal is sent to the processor, processor takes 2 clocks to process the job send it to the output port. Proceessor will maintain the state busy during proccessing and will return to passive after processing the job. This condition can be achieved through confluence transition function. The jobs that are not ready for the processing will wait in the queue until the processor comes out of busy state.

- ATOMIC COMPONENET: Generator

- GENERATED FACTS:
```json
{
"input ports": null, 
"output ports": "job_out",
"state variables": {
    "time advance": 11, 
    "job_count": 0 
    },
"Transition Functions":{
    "internal transition function": [
    "If `job_count` = 0, set `job_count` = 1, and set `time_advance` = 2 (13th second (next event time)- 11th second (current event time)).",
    "If `job_count` = 1, set `job_count` = 2, and set `time_advance` = 4 (17th second (next event time)- 13th second (current event time)).",
    "If `job_count` = 2, set `job_count` = 3, and set `time_advance` = Infinity. (To complete all job generations)."],
    "external transition function": [],
    "output function": ["Send a job signal to `job_out` when `job_count` is 0, 1, or 2."],
    "confluent transition function": ["Execute the internal transition function and output function if a message arrives at the same time."]
    }
}
```

# Example-2:

- SYSTEM DESCRIPTION: 

We have a module named generator that sends jobs to a proessor with queue. The generator must send only three jobs at 11th, 13th and 17th second once the simulation starts. The initial state of the processor is passive. Once job signal is sent to the processor, processor takes 2 clocks to process the job send it to the output port. Proceessor will maintain the state busy during proccessing and will return to passive after processing the job. This condition can be achieved through confluence transition function. The jobs that are not ready for the processing will wait in the queue until the processor comes out of busy state.

- ATOMIC COMPONENET: Processor

- GENERATED FACTS:
```json
{
"input ports": "job_in", 
"output ports": "processed_job_out", 
"state variables": {
    "time advance": "Infinity", 
    "phase": "passive", 
    "queue": []
    },
"Transition Functions":{
    "internal transition function": [
    "If state is `busy` and `queue` is empty, then set state to `passive` and `time_advance` to Infinity (To wait for next job).",
    "If state is `busy` and `queue` is not empty, then hold state at `busy` and set `time_advance` to 2 (To process next job)."],
    "external transition function": [
    "If a job is received at `job_in` and state is `passive`, change state to `busy` and set `time_advance` to 2 (indicating processing time).",
    "If a job is received at `job_in` and state is `busy`, add job to `queue` and set time advance to remaining processing time for the current job in process."],
    "output function": ["If state is `busy`, remove the first job from queue and send it to `processed_job_out`."],
    "confluent transition function": ["If a job is received while in `busy` state, process the job and immediately transition to `passive` after processing."]
    }
}
```