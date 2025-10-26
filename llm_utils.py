import openai
import config
import re
from z3 import *
import json
import time
from groq import Groq

## Fetching OPENAI and GROQ credentials.
openai.api_version = config.OPENAI_API_VERSION
openai.api_type = config.OPENAI_API_TYPE
openai.api_base = config.OPENAI_API_BASE
openai.api_key = config.OPENAI_API_KEY
openrouter_api_key = config.OPENROUTER_API_KEY
groq_api_key = config.GROQ_API_KEY

class LLMAgent:
    def __init__(self, engine, model, system_prompt="You are a helpful AI assistant. Provide clear, concise, and insightful responses."):
        """Initialize the GPT agent with a fixed system prompt and conversation history."""
        self.conversation_history = [{"role": "system", "content": system_prompt}]
        self.engine = engine  # 'openai' or 'groq'
        self.model = model

    # -------------------- internal helpers --------------------
    def _call_model(self):
        if self.engine == 'openai':
            if self.model == 'gpt-3.5-turbo-instruct':
                resp = openai.Completion.create(
                    model="gpt-3.5-turbo-instruct",
                    prompt=self.conversation_history,
                    temperature=0.3,
                )
                return resp["choices"][0]["text"]
            else:
                resp = openai.ChatCompletion.create(
                    model=self.model,
                    messages=self.conversation_history,
                    temperature=0.3,
                )
                return resp["choices"][0]["message"]["content"]

        elif self.engine == 'openrouter':
            openai.api_base = 'https://openrouter.ai/api/v1'
            openai.api_key = openrouter_api_key

            resp = openai.ChatCompletion.create(
                model=self.model,
                messages=self.conversation_history, 
                temperature = 0.3,
                )
            return resp.choices[0].message.content

        elif self.engine == 'groq':
            client = Groq(api_key=groq_api_key)
            resp = client.chat.completions.create(
                model=self.model,
                messages=self.conversation_history,
                temperature=0.3,
                stream=False,
                stop=None,
            )
            return resp.choices[0].message.content

        else:
            raise ValueError(f"Unsupported engine: {self.engine}")

    @staticmethod
    def _strip_code_fences(text: str) -> str:
        t = text.strip()
        if t.startswith("```"):
            # Remove opening/closing fences and optional language tag
            t = re.sub(r"^```[a-zA-Z0-9_-]*\s*", "", t)
            t = re.sub(r"\s*```$", "", t)
        return t.strip()

    @staticmethod
    def _extract_json_candidate(text: str) -> str:
        """
        Try to extract the most likely JSON object/array substring.
        Looks for the first '{' or '[' and the last matching '}' or ']'.
        """
        t = text.strip()
        # Quick path: already looks like pure JSON
        if (t.startswith("{") and t.endswith("}")) or (t.startswith("[") and t.endswith("]")):
            return t

        # Find first JSON opener
        start_brace = t.find("{")
        start_bracket = t.find("[")

        # Select earliest opener
        starts = [x for x in [start_brace, start_bracket] if x != -1]
        if not starts:
            return t  # fallback: return as-is; json.loads will fail and trigger retry
        start = min(starts)

        # Heuristic: prefer matching closer with the same type
        if start == start_brace:
            end = t.rfind("}")
        else:
            end = t.rfind("]")

        if end != -1 and end > start:
            return t[start:end+1]
        return t

    @staticmethod
    def _light_repair(s: str) -> str:
        """
        Minimal, safe-ish repairs:
        - Remove trailing commas before closing } or ]
        - Normalize true/false/null to lowercase (if model used True/False/None)
        - Convert single quotes to double quotes ONLY if it looks like a JSON object with single quotes
        """
        # Remove trailing commas: ",}" -> "}" and ",]" -> "]"
        s = re.sub(r",\s*([}\]])", r"\1", s)

        # Python-ish to JSON
        s = s.replace("None", "null").replace("True", "true").replace("False", "false")

        # If there are no double quotes but there are single quotes around keys/strings, try a cautious replace
        # (Still not perfect for nested quotes, but helps many LLM outputs.)
        if ('"' not in s) and ("'" in s):
            # Replace quotes around keys/strings: 'key': 'value'  ->  "key": "value"
            # This is a heuristic and may fail on complex content with apostrophes inside strings.
            s = re.sub(r"'", '"', s)

        return s

    # -------------------- public API --------------------
    def ask(self, user_input, max_retries=3, backoff_seconds=1.5):
        """
        Send a message to the GPT agent and return parsed JSON.
        Retries:
          1) Ask the model again with a 'return valid JSON' nudge.
          2) Apply light repair heuristics before each parse attempt.
        """
        self.conversation_history.append({"role": "user", "content": user_input})

        last_error = None
        for attempt in range(1, max_retries + 1):
            # Call the model
            assistant_reply = self._call_model()
            # print(assistant_reply)  # debug visibility

            # Clean/Extract
            candidate = self._strip_code_fences(assistant_reply)
            candidate = self._extract_json_candidate(candidate)
            candidate = self._light_repair(candidate)

            # Try parsing
            try:
                result_dict = json.loads(candidate)
                return result_dict
            except json.JSONDecodeError as e:
                last_error = e

                # Prepare a corrective follow-up message for next attempt (except after final)
                if attempt < max_retries:
                    self.conversation_history.append({
                        "role": "user",
                        "content": (
                            "Your previous output was not valid JSON. "
                            "Please respond with ONLY valid JSON, no commentary, "
                            "no code fences, and no trailing commas."
                        )
                    })
                    time.sleep(backoff_seconds)

        # If all attempts failed, raise a clear error with the last parse exception
        raise ValueError(f"Failed to parse LLM output into JSON after {max_retries} attempts. Last error: {last_error}")


class LLMAgent_no_json:
    def __init__(self, engine, model, system_prompt="You are a helpful AI assistant. Provide clear, concise, and insightful responses."):
        """Initialize the GPT agent with a fixed system prompt and conversation history."""
        self.conversation_history = [{"role": "system", "content": system_prompt}]
        self.engine = engine ## options are 'openai' or 'groq'
        self.model = model

    def ask(self, user_input):
        """Send a message to the GPT agent and return the response."""
        self.conversation_history.append({"role": "user", "content": user_input})
        if self.engine == 'openai':
            if self.model == 'gpt-3.5-turbo-instruct':
                response = openai.Completion.create(
                    model="gpt-3.5-turbo-instruct",   # <- Important
                    prompt=self.conversation_history,
                    temperature=0.1,
                )
                assistant_reply = response["choices"][0]["text"]
            else:
                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=self.conversation_history,
                    temperature=0.1,
                )
                assistant_reply = response["choices"][0]["message"]["content"]
        elif self.engine == 'groq':
            client = Groq(api_key = groq_api_key)
            response = client.chat.completions.create(
            model=self.model,
            messages = [self.conversation_history[-1]],
            temperature = 0.1,
            stream=False,
            stop=None,
            )
            assistant_reply = response.choices[0].message.content

        return assistant_reply

def props_extractor(sys_des, engine, model):
    conversion_prompt = open('./Prompts/Proposition extractor_sysdes_CoT.md').read()

    messages = [
        {"role": "system", "content": conversion_prompt},
        {"role": "user", "content": f'- SYSTEM DESCRIPTION:\n\n{sys_des}\n\n- PROPOSITIONS:\n'}
    ]

    if engine == 'openai':
        completion = openai.ChatCompletion.create(
            model=model, messages=messages, temperature=0.3
        )
        PL_statements = completion.choices[0].message["content"]
    elif engine == 'groq':
        client = Groq(api_key = config.GROQ_API_KEY)
        response = client.chat.completions.create(
            model=model, messages = messages, temperature = 0.3, stream=False, stop=None,
        )
        PL_statements = response.choices[0].message.content
    # Remove surrounding triple backticks and optional 'json'
    if PL_statements.strip().startswith("```"):
        PL_statements = PL_statements.strip().strip("`")  # remove backticks
        PL_statements = PL_statements.replace("json", "", 1).strip()  # remove 'json' if present
    # Parse as JSON
    try:
        result_dict = json.loads(PL_statements)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse LLM output into JSON. Error: {e}")
    return result_dict

def PL_conversion_pdevs(pdevs_facts, component, props, engine, model):
    conversion_prompt = open('./Prompts/Proposition extractor_pdevs.md').read()
    messages = [
        {"role": "system", "content": conversion_prompt},
        {"role": "user", "content": f'- COMPONENT: {component}\n\n- INTERNAL TRANSITION FUNCTION:\n{'\n'.join(pdevs_facts['Transition Functions']['internal transition function'])}\n\n- EXTERNAL TRANSITION FUNCTION:\n{'\n'.join(pdevs_facts['Transition Functions']['external transition function'])}\n\n- OUTPUT FUNCTION:\n{'\n'.join(pdevs_facts['Transition Functions']['output function'])}\n\n- PROPOSITIONS:\n{props}\n\n- PROPOSITIONAL LOGIC:\n'}
    ]

    def call_llm():
        print(messages)
        if engine == 'openai':
            completion = openai.ChatCompletion.create(
                model=model, messages=messages, temperature=0.3
            )
            PL_statements = completion.choices[0].message["content"]
        elif engine == 'groq':
            client = Groq(api_key = config.GROQ_API_KEY)
            response = client.chat.completions.create(
                model=model, messages = messages, temperature = 0.3, stream=False, stop=None,
            )
            PL_statements = response.choices[0].message.content
        return PL_statements

    last_error_msg = ""
    for attempt in range(1, 4):
        try:
            if attempt > 1 and last_error_msg:
                messages[1]["content"] = messages[1]["content"] + f"\nEarlier attempt failed due to {last_error_msg}. Avoid the error"
            PL_statements = call_llm()
            # Clean output
            if PL_statements.strip().startswith("```"):
                PL_statements = re.sub(r"^```(json)?", "", PL_statements.strip(), flags=re.IGNORECASE).strip("`").strip()
            # Try parsing
            result_dict = json.loads(PL_statements)
            return result_dict
        except json.JSONDecodeError as e:
            last_error_msg = str(e)
            print(f"[Attempt {attempt}] JSON decoding failed: {e}")
            print("Raw LLM output:\n", PL_statements)
            if attempt < 4:
                time.sleep(2)
                print("Retrying...\n")
            else:
                raise ValueError(f"Failed to parse LLM output into JSON after {4} attempts. Error: {e}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error during LLM call: {e}")
            
    # Remove surrounding triple backticks and optional 'json'
    if PL_statements.strip().startswith("```"):
        PL_statements = PL_statements.strip().strip("`")  # remove backticks
        PL_statements = PL_statements.replace("json", "", 1).strip()  # remove 'json' if present
    # Parse as JSON
    print(PL_statements)
    try:
        result_dict = json.loads(PL_statements)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse LLM output into JSON. Error: {e}")
    return result_dict

def PL_conversion_bc(props, beh_patterns, engine, model):
    conversion_prompt = open('./Prompts/Proposition extractor_bc.md').read()
    messages = [
        {"role": "system", "content": conversion_prompt},
        {"role": "user", "content": f'-Propositions:\n{props}\n\n- BEHAVIOR CONDITIONS:\n{beh_patterns}\n\n- PROPOSITIONAL LOGIC:\n'},
    ]

    def call_llm():
        if engine == 'openai':
            completion = openai.ChatCompletion.create(
                model=model, messages=messages, temperature=0.3
            )
            PL_statements = completion.choices[0].message["content"]
        elif engine == 'groq':
            client = Groq(api_key = config.GROQ_API_KEY)
            response = client.chat.completions.create(
                model=model, messages = messages, temperature = 0.3, stream=False, stop=None,
            )
            PL_statements = response.choices[0].message.content
        return PL_statements
    
    last_error_msg = ""
    for attempt in range(1, 4):
        try:
            if attempt > 1 and last_error_msg:
                messages[1]["content"] = messages[1]["content"] + f"\nEarlier attempt failed due to {last_error_msg}. Avoid the error"
            PL_statements = call_llm()
            # Clean output
            if PL_statements.strip().startswith("```"):
                PL_statements = re.sub(r"^```(json)?", "", PL_statements.strip(), flags=re.IGNORECASE).strip("`").strip()
            # Try parsing
            result_dict = json.loads(PL_statements)
            return result_dict
        except json.JSONDecodeError as e:
            last_error_msg = str(e)
            print(f"[Attempt {attempt}] JSON decoding failed: {e}")
            print("Raw LLM output:\n", PL_statements)
            if attempt < 4:
                time.sleep(2)
                print("Retrying...\n")
            else:
                raise ValueError(f"Failed to parse LLM output into JSON after {4} attempts. Error: {e}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error during LLM call: {e}")
            
    # Remove surrounding triple backticks and optional 'json'
    if PL_statements.strip().startswith("```"):
        PL_statements = PL_statements.strip().strip("`")  # remove backticks
        PL_statements = PL_statements.replace("json", "", 1).strip()  # remove 'json' if present
    # Parse as JSON
    print(PL_statements)
    try:
        result_dict = json.loads(PL_statements)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse LLM output into JSON. Error: {e}")
    return result_dict

def key_conditions_generator(message, component, engine, model):
    beh_cond_prompt = open('./Prompts/behavior_condition_prompt.md').read()

    ## PROMPT FOR BEHAVIOR CONDITIONS
    msg = [
        {"role": "system", "content": beh_cond_prompt},
        {"role": "user", "content": f'- SYSTEM DESCRIPTION:\n\n{message}\n\n- ATOMIC COMPONENET: {component}\n\n- BEHAVIOR CONDITIONS:\n'},
    ]

    if engine == 'openai':
        if 'coupled model' in message.split('\n')[-1].lower():

            completion = openai.ChatCompletion.create(
                model=model, messages=msg, temperature=0.3
            )
            key_conditions = completion.choices[0].message["content"]

        else:

            completion = openai.ChatCompletion.create(
                model=model, messages=msg, temperature=0.3
            )
            key_conditions = completion.choices[0].message["content"]

    elif engine == 'groq':

        client = Groq(api_key = config.GROQ_API_KEY)
        if 'Coupled models to be created:' in msg:

            response = client.chat.completions.create(
            model=model, messages = msg, temperature = 0.3, stream=False, stop=None,
            )
            key_conditions = response.choices[0].message.content

        else:
            response = client.chat.completions.create(
            model=model, messages = msg, temperature = 0.3, stream=False, stop=None,
            )
            key_conditions = response.choices[0].message.content
    
    # Remove surrounding triple backticks and optional 'json'
    if key_conditions.strip().startswith("```"):
        key_conditions = key_conditions.strip().strip("`")  # remove backticks
        key_conditions = key_conditions.replace("json", "", 1).strip()  # remove 'json' if present
    # Parse as JSON
    try:
        result_dict = json.loads(key_conditions)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse LLM output into JSON:\n{code}\nError: {e}")

    return result_dict