You are a system designer analyzing a component from a larger system. Your task is to derive atomic, verifiable behavioral conditions for the component under three categories:

- Behavior Types:

1. Internal Behavior:
    Actions or transitions triggered by the component’s own state or internal logic.
    Not caused by external messages.
    E.g., transitioning from busy to idle after finishing a task.

2. External Behavior:
    Actions triggered by receiving an external signal/message/input from another component.
    These occur when the component is in a certain state and responds to the input.
    E.g., transitioning to busy when receiving a job while in idle.

3. Output Behavior:

    Outputs/messages generated because of a state change or a condition.
    Typically sent just before an internal transition occurs.

- Output Requirements:

1. Each condition must be atomic: a minimal, indivisible unit of behavior.
2. Use clear causal phrasing like:
    “If state is X, perform Y”
    “If input Z is received while in state A, transition to B”
    “If state is Y, generate output Z”
3. Format your output strictly as shown below:
        
# Example-1

- SYSTEM DESCRIPTION: 

We have a Module named controller that sends on and off signals to a LigSens module. The controller must send these commands after every second. LigSens has two components: Light, Sensor. The initial state of the lights is off and the controller will auto-start the cycle 10 seconds after simulation starts. Once started the toggling should never end. Light communicates its state with the Sensor. 

- ATOMIC COMPONENET: Controller

- BEHAVIOR CONDITIONS:
```json
{
    "internal behavior": ["start toggling signal after 10 seconds."],
    "external behavior": [],
    "output behavior": ["should send on signal if in on phase", "should send off signal if in off phase"]
}
```

# Example-2

- SYSTEM DESCRIPTION: 

We have a Module named controller that sends on and off signals to a LigSens module. The controller must send these commands after every second. LigSens has two components: Light, Sensor. The initial state of the lights is off and the controller will auto-start the cycle 10 seconds after simulation starts. Once started the toggling should never end. Light communicates its state with the Sensor. 

- ATOMIC COMPONENET: Light

- BEHAVIOR CONDITIONS:
```json
{
    "internal behavior": [],
    "external behavior": ["should turn on when on signal is received.", "should turn off when off signal is received."],
    "output behavior": ["should send on message to Sensor if in on phase.", "should send off message to Sensor if in off phase."]
}
```

# Example-3

- SYSTEM DESCRIPTION:

We have one Generator and one ProcSens component. Generator generates jobs every 5 seconds. ProcSens has two components: Processor, Sensor. The Processor will have a queue which will accomodate the incoming jobs. The processor will take 2 seconds to process a job. It will be initated in idle state and will maintain busy state while processing and will go back to idle if there are no jobs left in the queue. The Sensor will receive the processed jobs from the processor and will keep the count. Once the 5 jobs are processed, it will send stop signal to Generator. 

- ATOMIC COMPONENET: Processor

- BEHAVIOR CONDITIONS:
```json
{
    "internal behavior": ["If job processed and no job in queue should go to idle", "If job processed and job in queue should go to busy"],
    "external behavior": ["Should become busy if idle and job arrives.", "Should add the job to queue if busy and job arrives."],
    "output behavior": ["should send job to Sensor after processing."]
}
```