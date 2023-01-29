# Open AI
import openai
# openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = "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"

# Logging related
from datetime import datetime
import os
import inspect

# Typing & Formatting
from typing import BinaryIO, TextIO
import re, json, ast

# count tokens
from text_completion_example import count_tokens

# Constants
LOGS_FOLDER = "./logs"
INSTRUCTION_PATHS = {
    "identify_intents": "./instructions/identify_intents.txt",
    "identify_entities": "./instructions/identify_entities.txt",
    "identify_scene": "./instructions/identify_scene.txt",
    "identify_events": "./instructions/identify_events.txt",
    "generate_logics": "./instructions/generate_logics.txt"
}
DATE_TIME_FORMAT = "%Y-%m-%d %H-%M-%S"
LOGS_FILL_WIDTH = 30
LOGS_FILL_CHAR = "-"
def load_instruction_propmt(method_name: str):
    with open(INSTRUCTION_PATHS[method_name], "r", encoding="utf-8") as f:
        return f.read()

def loads_json(json_str: str):
    # Reference: https://bobbyhadz.com/blog/python-jsondecodeerror-expecting-property-name-enclosed-in-double-quotes
    # Reference: https://stackoverflow.com/a/36599122
    # Issue: Trailing Comma or Single Quote

    return ast.literal_eval(json_str)

def compose_request_prompt(query: str, query_info: str="", additional_instructions: str=""):
    # https://stackoverflow.com/questions/5067604/determine-function-name-from-within-that-function-without-using-traceback
    instruction = load_instruction_propmt(inspect.stack()[1][3]) # Use current function name as the input
    user_query = "query_prompt:\n[" + query + "]\n"
    return instruction + additional_instructions + user_query

def identify_intents(query, query_info=""):
    request_prompt = compose_request_prompt(query, query_info)

    current_time_str = datetime.now().strftime(DATE_TIME_FORMAT)
    log_filename = f"[{current_time_str}] IntentIdentification-[{query_info}].txt"
    with open(os.path.join(LOGS_FOLDER, log_filename), "w", encoding="utf-8") as f:
        f.write("Request: Identify Intents\n\n")
        f.write(f"Time: {current_time_str}\n\n")
        f.write(f"Prompt:\n{request_prompt} \n\n")

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=request_prompt,
            temperature=0.3,
            max_tokens=200,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            n=1,
        )

        f.write(f"Response:\n{str(response)}\n")
        text =  response["choices"][0]["text"].replace('\\n', '\n').replace('\\t', '\t')
        return text

def identify_entities(query: str, query_info: str="", file: TextIO=None):
    request_prompt = compose_request_prompt(query, query_info)

    current_time_str = datetime.now().strftime(DATE_TIME_FORMAT)
    log_filename = f"[{current_time_str}] EntityIdentification -[{query_info}].txt"

    logs = "Identify Entities Start".upper().center(LOGS_FILL_WIDTH, LOGS_FILL_CHAR)
    try:
        logs += f"Request: Identify Entities \n\n"
        logs += f"Time: {current_time_str}\n\n"
        logs += f"Request Prompt:\n{request_prompt} \n\n"

        entities = None
        counter = 0

        # In case return None
        while (entities is None and counter < 5):
            counter += 1
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=request_prompt,
                temperature=0.8,
                max_tokens=4097 - count_tokens(request_prompt),
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                n=1,
            )

            logs += f"Response:\n{str(response)} {counter}\n"
            text = response["choices"][0]["text"].replace('\\n', '\n').replace('\\t', '\t')

            regex_pattern = "(.*Entities.*\:[\s]*)({(.|\n)*})"

            try:
                entities = loads_json(re.search(regex_pattern, text).group(2))
            except Exception as e:
                logs += f"Errored: str(e)\n\n"


        logs += f"Extracted Entities in JSON:\n{str(entities)}\n"
        logs += "Identify Entities End".upper().center(LOGS_FILL_WIDTH, LOGS_FILL_CHAR)
        logs += "\n\n"

        entity_names = list(entities.keys())
        return entities, entity_names
    except Exception as e:
        logs += f"Errored: {str(e)}\n\n"
        return None, None
    finally:
        # Logging
        if file:
            file.write(logs)
        else:
            with open(os.path.join(LOGS_FOLDER, log_filename), "w", encoding="utf-8") as f:
                f.write(logs)

def identify_scene(query: str,  entity_names: list, query_info: str="", file: TextIO=None):
    additional_instructions = f"Here is a discovered list of entities: {str(entity_names)}. " \
                              f"However, many entities are not on this list. " \
                              f"Find the root node of the scene from the story in query_prompt. " \
                              f"Add more entities that are described." \
                              f"\n--- Following is the query_prompt ---\n"

    request_prompt = compose_request_prompt(query, additional_instructions=additional_instructions)

    current_time_str = datetime.now().strftime(DATE_TIME_FORMAT)
    log_filename = f"[{current_time_str}] SceneIdentification-[{query_info}].txt"

    logs = "Identify Scene Start".upper().center(LOGS_FILL_WIDTH, LOGS_FILL_CHAR)
    try:
        logs += f"Request: Identify Scene \n\n"
        logs += f"Time: {current_time_str}\n\n"
        logs += f"Request Prompt:\n{request_prompt} \n\n"

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=request_prompt,
            temperature=0.7,
            max_tokens=4097 - count_tokens(request_prompt),
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            n=1,
        )

        logs += f"Response:\n{str(response)}\n"
        text = response["choices"][0]["text"].replace('\\n', '\n').replace('\\t', '\t')
        logs += f"text:\n{str(text)}"

        regex_pattern = "(.*Scene.*\:[\s]*)({(.|\n)*})"
        scene = loads_json(re.search(regex_pattern, text).group(2))

        logs += "Identify Scene End".upper().center(LOGS_FILL_WIDTH, LOGS_FILL_CHAR)
        logs += "\n\n"

        return scene
    except Exception as e:
        logs += f"Errored: {str(e)}\n\n"
        return None
    finally:
        # Logging
        if file:
            file.write(logs)
        else:
            with open(os.path.join(LOGS_FOLDER, log_filename), "w", encoding="utf-8") as f:
                f.write(logs)

def identify_events(query: str,  entity_names: list, query_info: str="", file: TextIO=None):
    additional_instructions = f"Here is a discovered list of entities: {str(entity_names)}. " \
                              f"However, many entities are not on this list. " \
                              f"Find them all and summarize them into a list of events." \
                              f"\n--- Following is the query_prompt ---\n"

    request_prompt = compose_request_prompt(query, additional_instructions=additional_instructions)

    current_time_str = datetime.now().strftime(DATE_TIME_FORMAT)
    log_filename = f"[{current_time_str}] SceneIdentification-[{query_info}].txt"

    logs = "Identify Events Start".upper().center(LOGS_FILL_WIDTH, LOGS_FILL_CHAR)
    try:
        logs += f"Request: Identify Events \n\n"
        logs += f"Time: {current_time_str}\n\n"
        logs += f"Request Prompt:\n{request_prompt} \n\n"

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=request_prompt,
            temperature=0.7,
            max_tokens=4097 - count_tokens(request_prompt),
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            n=1,
        )

        logs += f"Response:\n{str(response)}\n"
        text = response["choices"][0]["text"].replace('\\n', '\n').replace('\\t', '\t')
        logs += f"text:\n{str(text)}"

        regex_pattern = "(.*Events.*\:[\s]*)({(.|\n)*})"
        events = loads_json(re.search(regex_pattern, text).group(2))

        logs += "Identify Events End".upper().center(LOGS_FILL_WIDTH, LOGS_FILL_CHAR)
        logs += "\n\n"

        return events
    except Exception as e:
        logs += f"Errored: {str(e)}\n\n"
        return None
    finally:
        # Logging
        if file:
            file.write(logs)
        else:
            with open(os.path.join(LOGS_FOLDER, log_filename), "w", encoding="utf-8") as f:
                f.write(logs)

def generate_logics(entities: dict, events: dict, query_info: str="", file: TextIO=None):
    # Json dumps for pretty print for nested dict
    # Reference: https://stackoverflow.com/questions/3229419/how-to-pretty-print-nested-dictionaries

    additional_instructions = f"// Known Entities and Behaviors\n" \
                              f"Entities: \n {str(json.dumps(entities))}\n\n" \
                              f"// Events to reconstruct\n" \
                              f"Events: \n {str(json.dumps(events))}\n\n"

    request_prompt = compose_request_prompt(query="// Reconstructed Events\n", additional_instructions=additional_instructions)

    current_time_str = datetime.now().strftime(DATE_TIME_FORMAT)
    log_filename = f"[{current_time_str}] LogicsGeneration-[{query_info}].txt"

    logs = "Generate Logics Start".upper().center(LOGS_FILL_WIDTH, LOGS_FILL_CHAR)
    try:
        logs += f"Request: Generate Logics \n\n"
        logs += f"Time: {current_time_str}\n\n"
        logs += f"Request Prompt:\n{request_prompt} \n\n"

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=request_prompt,
            temperature=0.7,
            max_tokens=4097 - count_tokens(request_prompt),
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            n=1,
        )

        logs += f"Response:\n{str(response)}\n"
        text = response["choices"][0]["text"].replace('\\n', '\n').replace('\\t', '\t')
        logs += f"text:\n{str(text)}"

        generated_logics = text
        logs += "Generate Logics End".upper().center(LOGS_FILL_WIDTH, LOGS_FILL_CHAR)
        logs += "\n\n"

        return generated_logics
    except Exception as e:
        logs += f"Errored: {str(e)}\n\n"
        return None
    finally:
        # Logging
        if file:
            file.write(logs)
        else:
            with open(os.path.join(LOGS_FOLDER, log_filename), "w", encoding="utf-8") as f:
                f.write(logs)


def analyze_story(query: str, query_info: str=""):

    # Setup Logging Doc
    current_time_str = datetime.now().strftime(DATE_TIME_FORMAT)
    log_filename = f"[{current_time_str}] StoryAnalysis -[{query_info}].txt"
    with open(os.path.join(LOGS_FOLDER, log_filename), "w", encoding="utf-8") as f:
        f.write("Request: Analyze Story \n\n")
        f.write(f"Time: {current_time_str}\n\n")
        f.write(f"Original Query:\n{query} \n\n")
        f.write(f"Query Info: {query_info} \n\n")

        # Step 1: generate entities
        entities, entity_names = identify_entities(query, query_info, file=f)
        if entities is None or entity_names is None:
            f.write("Errored when trying to identify entities")
            return None, None, None, None

        # Step 2: analyze the scene with entity_names
        scene = identify_scene(query, entity_names=entity_names, file=f)
        if scene is None:
            f.write("Errored when trying to identify scenes")
            return None, None, None, None

        # Step 3: analyze the events
        events = identify_events(query, entity_names=entity_names, file=f)
        if events is None:
            f.write("Errored when trying to identify entities")
            return None, None, None, None

        # Step 4: generate logics
        logics = generate_logics(entities, events, file=f)
        if logics is None:
            f.write("Errored when trying to generate logics")
            return None, None, None, None

        # Log the results
        f.write(f"\n\n ****** Final Results ****** \n\n")
        f.write(f"Entities: \n{json.dumps(entities)}\n\n")
        f.write(f"Scene: \n{json.dumps(scene)}\n\n")
        f.write(f"Events: \n{json.dumps(events)}\n\n")
        f.write(f"Logics: \n{json.dumps(logics)}\n\n")

        f.write(f"\n\n\n Task End Time: {datetime.now().strftime(DATE_TIME_FORMAT)}")

        return entities, scene, events, logics


def generate_story_full(query: str, query_info: str=""):
    """
    For generating stories to suggest insights
    :param query:
    :param query_info:
    :return:
    """
    pass

def generate_story(query: str, query_info: str=""):
    """
    For generating stories to suggest insights
    :param query:
    :param query_info:
    :return:
    """
    pass

#
# msg_1 = "A yellow corgi under a christmas tree"
# story_path = "./stories/story_2.txt"
# with open(story_path, "r", encoding="utf-8") as f:
#     msg_2 = f.read()
#
# print(analyze_story(msg_2))
