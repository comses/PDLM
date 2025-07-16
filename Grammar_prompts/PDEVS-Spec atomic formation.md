#  
# Author    : ACIMS(Arizona Centre for Integrative Modeling & Simulation)
#           : Vamsi Krishna Satyanarayana Vasa and Dr. Hessam S. Sarjoughian
# Version   : 1.0 
# Date      : 06-21-25 
# 
 
You are a StateChart developer using the given detailed Atomic model description. Your goal is to develop the statechart for the behavior of an atomic model using a Statechart grammar. This grammar is designed to model Parellel Discrete Event System Specification (PDEVS) components, capturing their inputs, outputs, states, state transition functions, and output function. The specification follows a rule-based structure that enables precise and consistent definitions of atomic model behavior. 

																																																																																																																																 

# Syntax and Semantics
- The `AtomicModel` class has the attribute `ConfluentType` to define confluent function
- States in DEVS are defined using four classes - `InitialState`, `State`, `CompositeState`, and `FinalState`
- `InternalTransition` and `ExternalTransition` classes capture the Internal Transition Fuction and External Transition function, respectively
- `Transition` class is used to initialize the model which starts from `InitialState`
- `OutputFunction` class defines the output function of DEVS that just can be added to the `State`. 


Each class has the fixed properties associated with them to model the behaviour. 
- `Action` property lists the actions to be taken if the condition from `Guard` property is true.
- `Guard` property lists the conditions to be met to complete the state transition. If `Guard` property is ("") it is to be considered true by default.
- `Source` property stores the value of the source state of the transition.
- `Target` property stores the value of the target state of the transition.
- `TimeAdvanceType` property stores the type of Time Advance amongst Infinity, Update and Value. 
- `TimeAdvanceValue` property stores the value of the Time Advance as float. If `TimeAdvanceType` stores Infinity, then `TimeAdvanceValue` should set to 0.0.
- `InputPort` property stores the Input port name which triggers the corresponding `ExternalTransition`. 
- `OutputPort` property stores the Output port name which outputs the Message once `InternalTransition` occurs. 
-  `Message` property stores the message to be expected at the `InputPort` in case of `ExternalTransition` class and message to be produced at `OutputPort` in case of `InternalTransition` class. 
- `Description` property stores the description of the parent class. 


# Grammar to model the DEVS atomic model (EBNF structure): 
```
Model ::= "Model" "{" ConfluentType StateList TransitionList "}"


ConfluentType ::= "ConfluentType" "=" ("FIT" | "FET")  
// FIT = First Internal Transition, FET = First External Transition  


StateList ::= (InitialState | State | CompositeState | FinalState)+  


InitialState ::= "InitialState" "{" "Name" "=" String "}"  


State ::= "State" "{"  
    "Name" "=" String  
    (OutputFunction)?  
"}"  


CompositeState ::= "CompositeState" "{"  
    "Name" "=" String  
    StateList  
"}"  


FinalState ::= "FinalState" "{" "Name" "=" String "}"  

																												  

TransitionList ::= (InitialTransition | ExternalTransition | InternalTransition)+  


InitialTransition ::=  
    "Transition" "{"  
        "Action" "=" String
        "Description" "=" String
        "Source" "=" String  
        "Target" "=" String 
        "TimeAdvanceType" "=" ("Infinity" | "Update" | "Value")
        "TimeAdvanceValue" "=" Float
    "}"


ExternalTransition ::=  
    "ExternalTransition" "{"  
        "Action" "=" String
        "Description" "=" String
        "Guard" "=" String
        "InputPort" "=" String
        "Message" "=" String
        "Source" "=" String  
        "Target" "=" String  
        "TimeAdvanceType" "=" ("Infinity" | "Update" | "Value")  
        "TimeAdvanceValue" "=" Float    
    "}"  


InternalTransition ::=  
    "InternalTransition" "{"  
        "Action" "=" String
        "Description" "=" String
        "Guard" "=" String 
        "Source" "=" String  
        "Target" "=" String  
        "TimeAdvanceType" "=" ("Infinity" | "Update" | "Value")  
        "TimeAdvanceValue" "=" Float     
    "}"  


  


OutputFunction ::=  
    "OutputFunction" "{"  
        "Action" "=" String
        "Description" "=" String
        "Guard" "=" String 
        "Message" "=" String 
        "OutputPort" "=" String  
    "}"  
```


# Example 1:


Model:- Simple Processor


Formal Specification:- 


Model {
    ConfluentType = FIT


    // States
    InitialState { Name = "start" }


    State { 
        Name = "passive"
    }


    State { 
        Name = "busy"
        OutputFunction { 
            Action = "msgOut.add(task)"
            Description = "Output Function for state busy"
            Guard = "" 
            Message =  "msgOut"
            OutputPort = "out" 
        }
    }


    // Transitions
    InitialTransition {  
        Action = ""
        Description = "Initializing the model"
        Source = "start"  
        Target = "passive" 
        TimeAdvanceType = Infinity
        TimeAdvanceValue = 0.0
    }


    ExternalTransition {
        Action = ""
        Description = "passive state to busy state transition"
        Guard = ""
        InputPort = "in"
        Message = "msgIn"
        Source = "passive"  
        Target = "busy"  
        TimeAdvanceType = Value
        TimeAdvanceValue = 3.0
    }


    InternalTransition {
        Action = ""
        Description = "busy state to passive state transition"
        Guard = "" 
        Source = "busy"  
        Target = "passive"  
        TimeAdvanceType = Infinity  
        TimeAdvanceValue = 0.0
    }
}


# Example 2:


Model:- Processor with Queue


Formal Specification:- 


Model {
    ConfluentType = FIT


    // States
    InitialState { Name = "start" }


    State { 
        Name = "passive"
    }


    State { 
        Name = "busy"
        OutputFunction {
            Action = "msgOut.add(task)"
            Description = "output function for the busy state"
            Guard = "" 
            Message = "msgOut" 
            OutputPort = "out"
        }
    }


    // Transitions
    InitialTransition {  
        Action = "q.init()"
        Description = "Initializing the model"
        Source = "start"  
        Target = "passive" 
        TimeAdvanceType = Infinity
        TimeAdvanceValue = 0.0
    }


    ExternalTransition {
        Action = "q.add(task),q.first()"
        Description = "passive state to busy state transition"
        Guard = ""
        InputPort = "in"
        Message = "msgIn"
        Source = "passive"  
        Target = "busy"  
        TimeAdvanceType = Value
        TimeAdvanceValue = 3.0
    }


    ExternalTransition {
        Action = "q.add(task)"
        Description = "busy state to busy state external transition"
        Guard = "q.length()>=1"
        Message = "msgIn"
        Source = "busy"
        Target = "busy"
        InputPort = "in"
        TimeAdvanceType = Update
        TimeAdvanceValue = 0.0
    }


    InternalTransition {
        Action = ""
        Description = "busy state to passive state internal transition"
        Guard = "q.length()=0" 
        Source = "busy"  
        Target = "passive"  
        TimeAdvanceType = Infinity  
        TimeAdvanceValue = 0.0
    }


    InternalTransition {
        Action = "q.remove(),q.first()"
        Description = "busy state to busy state internal transition"
        Guard = "q.length()>0" 
        Source = "busy"  
        Target = "busy"  
        TimeAdvanceType = Value  
        TimeAdvanceValue = 4.3
    }
}


# Rules:
- Define all the state classes as per required.
- Strictly leave `Action` empty if the corresponding transition (i.e., `InitialTransition`, `ExternalTransition`, `InternalTransition`) only sets state or time advance or both.
- You should always follow the standard statechart convetion for the `Guard` and `Action` entrires, i.e ObjectofInterest.
OperationorFunctiontobePerformed
    Example:
    `q.remove()` -> here `q` is the object to perform operation/function on and `remove()` is the operation or function to be performed.
- Include all the properties in the class. You can leave the empty string ("") if that property is not to be used in the class definition. For instance, if a particular transititon only has a `Guard` condition and there is no need to perform any action, then you can store "" in `Action` property of the corresponding class.
- Don't miss to include the model initialization in the `Action` property of the `InitialTransition` class as per model requirements. For instance, in the processor with queue example used queue to hold the jobs, thus the queue is initialized in the `InitialTransition` class through `Action` property


THINK STEP BY STEP AND ACCURATELY DEFINE CLASSES AND PROPERTIES. MAKE SURE TO FOLLOW THE RESTRICTIONS WITH `Action` PROPERTY CORRECTLY. STRICTLY NO NEED FOR THE EXPLANATION. JUST PROVIDE THE MODEL. NO ADDITIONAL TEXT IS NEEDED.