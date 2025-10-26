You are given the internal/external transitions and output functions from PDEVS specification of particular. Your task is to translate these behaviors into propositional logic using the provided proposition mappings.

- Step-by-step Instructions:
1. Identify cause-effect pairs: For each behavior, find the condition(s) that lead to a state or output change.
2. Map using propositions: Use the proposition mapping to represent each literal condition in propositional form.
3. Translate each behavior into a conditional logic expression using allowed logical operators only.
4. Use parentheses to clearly group expressions.
5. Even if facts contradict, still include them.
6. Follow the exact JSON output format as shown in the example. No extra explanation is allowed.

- Avoid:
1. Any characters other than proposition variables and logical operators.
2. Any numerical values or timing information.
3. Equality symbols (=).

- Logical Operators Allowed:
¬ (negation)
∧ (and/conjunction)
∨ (or/disjunction)
→ (implication/conditional)
() (parentheses for grouping)

# Example-1:
- COMPONENT: Processor

- INTERNAL TRANSITION FUNCTION:
If state is `busy`, set state to `idle` and `time_advance` to Infinity (to wait for the next job).

- EXTERNAL TRANSITION FUNCTION:
If a job is received at `job_in` and state is `idle`, change state to `busy` and set `time_advance` to 2 (indicating processing time).

- OUTPUT FUNCTION:
If state is `busy`, send the processed job signal to `processed_job_out` after processing.

- PROPOSITIONS:
```json
{
"j": "Job signal is received by processor",
"b": "Processor is in busy state",
"i": "Processor is in idle state",
"p": "Job is processed by processor",
"o": "Processed job is sent to output port"
}
```

- PROPOSITIONAL LOGIC:
```json
{
"Logical Expressions": {
  "internal transition function": {
    "1": ["If state is `busy`, set state to `idle` and `time_advance` to Infinity (to wait for the next job).", "(b ∧ p) → (i)"],
    },
  "external transition function": {
    "1": ["If a job is received at `job_in` and state is `idle`, change state to `busy` and set `time_advance` to 2 (indicating processing time).","(j ∧ i) → b"],
    },
  "output function": {
    "1": ["If state is `busy`, send the processed job signal to `processed_job_out` after processing.","(p) → (o)"],
    }
  }
}
```
 