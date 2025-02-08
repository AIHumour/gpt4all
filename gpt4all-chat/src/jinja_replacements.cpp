// The map in this file is automatically generated by Jared. Do not hand-edit it.

#include "jinja_replacements.h"

// This is a list of prompt templates known to GPT4All and their associated replacements which are automatically used
// instead when loading the chat template from GGUF. These exist for two primary reasons:
// - HuggingFace model authors make ugly chat templates because they do not expect the end user to see them;
// - and chat templates occasionally use features we do not support. This is less true now that we use minja.

// The substitution list.

const std::unordered_map<std::string_view, std::string_view> CHAT_TEMPLATE_SUBSTITUTIONS {
    // calme-2.1-phi3.5-4b.Q6_K.gguf (reported by ThilotE on Discord), Phi-3.5-mini-instruct-Q4_0.gguf (nomic-ai/gpt4all#3345)
    {
        // original
        R"TEMPLATE({% for message in messages %}{% if message['role'] == 'system' and message['content'] %}{{'<|system|>
' + message['content'] + '<|end|>
'}}{% elif message['role'] == 'user' %}{{'<|user|>
' + message['content'] + '<|end|>
'}}{% elif message['role'] == 'assistant' %}{{'<|assistant|>
' + message['content'] + '<|end|>
'}}{% endif %}{% endfor %}{% if add_generation_prompt %}{{ '<|assistant|>
' }}{% else %}{{ eos_token }}{% endif %})TEMPLATE",
        // replacement
        R"TEMPLATE({%- for message in messages %}
    {%- if message['role'] == 'system' and message['content'] %}
        {{- '<|system|>\n' + message['content'] + '<|end|>\n' }}
    {%- elif message['role'] == 'user' %}
        {{- '<|user|>\n' + message['content'] + '<|end|>\n' }}
    {%- elif message['role'] == 'assistant' %}
        {{- '<|assistant|>\n' + message['content'] + '<|end|>\n' }}
    {%- endif %}
{%- endfor %}
{%- if add_generation_prompt %}
    {{- '<|assistant|>\n' }}
{%- else %}
    {{- eos_token }}
{%- endif %})TEMPLATE",
    },
    // DeepSeek-R1-Distill-Qwen-7B-Q4_0.gguf
    {
        // original
        R"TEMPLATE({% if not add_generation_prompt is defined %}{% set add_generation_prompt = false %}{% endif %}{% set ns = namespace(is_first=false, is_tool=false, is_output_first=true, system_prompt='') %}{%- for message in messages %}{%- if message['role'] == 'system' %}{% set ns.system_prompt = message['content'] %}{%- endif %}{%- endfor %}{{bos_token}}{{ns.system_prompt}}{%- for message in messages %}{%- if message['role'] == 'user' %}{%- set ns.is_tool = false -%}{{'<｜User｜>' + message['content']}}{%- endif %}{%- if message['role'] == 'assistant' and message['content'] is none %}{%- set ns.is_tool = false -%}{%- for tool in message['tool_calls']%}{%- if not ns.is_first %}{{'<｜Assistant｜><｜tool▁calls▁begin｜><｜tool▁call▁begin｜>' + tool['type'] + '<｜tool▁sep｜>' + tool['function']['name'] + '\n' + '```json' + '\n' + tool['function']['arguments'] + '\n' + '```' + '<｜tool▁call▁end｜>'}}{%- set ns.is_first = true -%}{%- else %}{{'\n' + '<｜tool▁call▁begin｜>' + tool['type'] + '<｜tool▁sep｜>' + tool['function']['name'] + '\n' + '```json' + '\n' + tool['function']['arguments'] + '\n' + '```' + '<｜tool▁call▁end｜>'}}{{'<｜tool▁calls▁end｜><｜end▁of▁sentence｜>'}}{%- endif %}{%- endfor %}{%- endif %}{%- if message['role'] == 'assistant' and message['content'] is not none %}{%- if ns.is_tool %}{{'<｜tool▁outputs▁end｜>' + message['content'] + '<｜end▁of▁sentence｜>'}}{%- set ns.is_tool = false -%}{%- else %}{% set content = message['content'] %}{% if '</think>' in content %}{% set content = content.split('</think>')[-1] %}{% endif %}{{'<｜Assistant｜>' + content + '<｜end▁of▁sentence｜>'}}{%- endif %}{%- endif %}{%- if message['role'] == 'tool' %}{%- set ns.is_tool = true -%}{%- if ns.is_output_first %}{{'<｜tool▁outputs▁begin｜><｜tool▁output▁begin｜>' + message['content'] + '<｜tool▁output▁end｜>'}}{%- set ns.is_output_first = false %}{%- else %}{{'\n<｜tool▁output▁begin｜>' + message['content'] + '<｜tool▁output▁end｜>'}}{%- endif %}{%- endif %}{%- endfor -%}{% if ns.is_tool %}{{'<｜tool▁outputs▁end｜>'}}{% endif %}{% if add_generation_prompt and not ns.is_tool %}{{'<｜Assistant｜>'}}{% endif %})TEMPLATE",
        // replacement
        R"TEMPLATE({%- if not add_generation_prompt is defined %}
    {%- set add_generation_prompt = false %}
{%- endif %}
{%- if messages[0]['role'] == 'system' %}
    {{- messages[0]['content'] }}
{%- endif %}
{%- for message in messages %}
    {%- if message['role'] == 'user' %}
        {{- '<｜User｜>' + message['content'] }}
    {%- endif %}
    {%- if message['role'] == 'assistant' %}
        {%- set content = message['content'] | regex_replace('^[\\s\\S]*</think>', '') %}
        {{- '<｜Assistant｜>' + content + '<｜end▁of▁sentence｜>' }}
    {%- endif %}
{%- endfor -%}
{%- if add_generation_prompt %}
    {{- '<｜Assistant｜>' }}
{%- endif %})TEMPLATE",
    },
    // gemma-2-9b-it-Q4_0.gguf (nomic-ai/gpt4all#3282)
    {
        // original
        R"TEMPLATE({{ bos_token }}{% if messages[0]['role'] == 'system' %}{{ raise_exception('System role not supported') }}{% endif %}{% for message in messages %}{% if (message['role'] == 'user') != (loop.index0 % 2 == 0) %}{{ raise_exception('Conversation roles must alternate user/assistant/user/assistant/...') }}{% endif %}{% if (message['role'] == 'assistant') %}{% set role = 'model' %}{% else %}{% set role = message['role'] %}{% endif %}{{ '<start_of_turn>' + role + '
' + message['content'] | trim + '<end_of_turn>
' }}{% endfor %}{% if add_generation_prompt %}{{'<start_of_turn>model
'}}{% endif %})TEMPLATE",
        // replacement
        R"TEMPLATE({{- bos_token }}
{%- if messages[0]['role'] == 'system' %}
    {{- raise_exception('System role not supported') }}
{%- endif %}
{%- for message in messages %}
    {%- if (message['role'] == 'user') != (loop.index0 % 2 == 0) %}
        {{- raise_exception('Conversation roles must alternate user/assistant/user/assistant/...') }}
    {%- endif %}
    {%- if message['role'] == 'assistant' %}
        {%- set role = 'model' %}
    {%- else %}
        {%- set role = message['role'] %}
    {%- endif %}
    {{- '<start_of_turn>' + role + '\n' + message['content'] | trim + '<end_of_turn>\n' }}
{%- endfor %}
{%- if add_generation_prompt %}
    {{- '<start_of_turn>model\n' }}
{%- endif %})TEMPLATE",
    },
    // ghost-7b-v0.9.1-Q4_0.gguf
    {
        // original
        R"TEMPLATE({% for message in messages %}
{% if message['role'] == 'user' %}
{{ '<|user|>
' + message['content'] + eos_token }}
{% elif message['role'] == 'system' %}
{{ '<|system|>
' + message['content'] + eos_token }}
{% elif message['role'] == 'assistant' %}
{{ '<|assistant|>
'  + message['content'] + eos_token }}
{% endif %}
{% if loop.last and add_generation_prompt %}
{{ '<|assistant|>' }}
{% endif %}
{% endfor %})TEMPLATE",
        // replacement
        R"TEMPLATE({%- for message in messages %}
    {%- if message['role'] == 'user' %}
        {{- '<|user|>\n' + message['content'] + eos_token }}
    {%- elif message['role'] == 'system' %}
        {{- '<|system|>\n' + message['content'] + eos_token }}
    {%- elif message['role'] == 'assistant' %}
        {{- '<|assistant|>\n'  + message['content'] + eos_token }}
    {%- endif %}
    {%- if loop.last and add_generation_prompt %}
        {{- '<|assistant|>' }}
    {%- endif %}
{%- endfor %})TEMPLATE",
    },
    // Hermes-3-Llama-3.2-3B.Q4_0.gguf, mistral-7b-openorca.gguf2.Q4_0.gguf
    {
        // original
        R"TEMPLATE({% if not add_generation_prompt is defined %}{% set add_generation_prompt = false %}{% endif %}{% for message in messages %}{{'<|im_start|>' + message['role'] + '
' + message['content'] + '<|im_end|>' + '
'}}{% endfor %}{% if add_generation_prompt %}{{ '<|im_start|>assistant
' }}{% endif %})TEMPLATE",
        // replacement
        R"TEMPLATE({%- for message in messages %}
    {{- '<|im_start|>' + message['role'] + '\n' + message['content'] + '<|im_end|>\n' }}
{%- endfor %}
{%- if add_generation_prompt %}
    {{- '<|im_start|>assistant\n' }}
{%- endif %})TEMPLATE",
    },
    // ibm-granite/granite-3.1-3b-a800m-instruct.gguf, ibm-granite/granite-3.1-8b-instruct.gguf (nomic-ai/gpt4all#3159)
    {
        // original
        R"TEMPLATE({%- if messages[0]['role'] == 'system' %}{%- set system_message = messages[0]['content'] %}{%- set loop_messages = messages[1:] %}{%- else %}{%- set system_message = "Knowledge Cutoff Date: April 2024. You are Granite, developed by IBM." %}{%- if tools and documents %}{%- set system_message = system_message + " You are a helpful AI assistant with access to the following tools. When a tool is required to answer the user's query, respond with <|tool_call|> followed by a JSON list of tools used. If a tool does not exist in the provided list of tools, notify the user that you do not have the ability to fulfill the request. Write the response to the user's input by strictly aligning with the facts in the provided documents. If the information needed to answer the question is not available in the documents, inform the user that the question cannot be answered based on the available data." %}{%- elif tools %}{%- set system_message = system_message + " You are a helpful AI assistant with access to the following tools. When a tool is required to answer the user's query, respond with <|tool_call|> followed by a JSON list of tools used. If a tool does not exist in the provided list of tools, notify the user that you do not have the ability to fulfill the request." %}{%- elif documents %}{%- set system_message = system_message + " Write the response to the user's input by strictly aligning with the facts in the provided documents. If the information needed to answer the question is not available in the documents, inform the user that the question cannot be answered based on the available data." %}{%- else %}{%- set system_message = system_message + " You are a helpful AI assistant." %}{%- endif %}{%- if controls and 'citations' in controls and documents %}{%- set system_message = system_message + ' In your response, use the symbols <co> and </co> to indicate when a fact comes from a document in the search result, e.g <co>0</co> for a fact from document 0. Afterwards, list all the citations with their corresponding documents in an ordered list.' %}{%- endif %}{%- if controls and 'hallucinations' in controls and documents %}{%- set system_message = system_message + ' Finally, after the response is written, include a numbered list of sentences from the response that are potentially hallucinated and not based in the documents.' %}{%- endif %}{%- set loop_messages = messages %}{%- endif %}{{- '<|start_of_role|>system<|end_of_role|>' + system_message + '<|end_of_text|> ' }}{%- if tools %}{{- '<|start_of_role|>tools<|end_of_role|>' }}{{- tools | tojson(indent=4) }}{{- '<|end_of_text|> ' }}{%- endif %}{%- if documents %}{{- '<|start_of_role|>documents<|end_of_role|>' }}{%- for document in documents %}{{- 'Document ' + loop.index0 | string + ' ' }}{{- document['text'] }}{%- if not loop.last %}{{- ' '}}{%- endif%}{%- endfor %}{{- '<|end_of_text|> ' }}{%- endif %}{%- for message in loop_messages %}{{- '<|start_of_role|>' + message['role'] + '<|end_of_role|>' + message['content'] + '<|end_of_text|> ' }}{%- if loop.last and add_generation_prompt %}{{- '<|start_of_role|>assistant' }}{%- if controls %}{{- ' ' + controls | tojson()}}{%- endif %}{{- '<|end_of_role|>' }}{%- endif %}{%- endfor %})TEMPLATE",
        // replacement
        R"TEMPLATE({%- if messages[0]['role'] == 'system' %}
   {%- set system_message = messages[0]['content'] %}
   {%- set loop_messages = messages[1:] %}
{%- else %}
   {%- set system_message = "Knowledge Cutoff Date: April 2024.\nYou are Granite, developed by IBM." %}
{%- if tools and documents %}
   {%- set system_message = system_message + " You are a helpful AI assistant with access to the following tools. When a tool is required to answer the user's query, respond with <|tool_call|> followed by a JSON list of tools used. If a tool does not exist in the provided list of tools, notify the user that you do not have the ability to fulfill the request.\n\nWrite the response to the user's input by strictly aligning with the facts in the provided documents. If the information needed to answer the question is not available in the documents, inform the user that the question cannot be answered based on the available data." %}
{%- elif tools %}
   {%- set system_message = system_message + " You are a helpful AI assistant with access to the following tools. When a tool is required to answer the user's query, respond with <|tool_call|> followed by a JSON list of tools used. If a tool does not exist in the provided list of tools, notify the user that you do not have the ability to fulfill the request." %}
{%- elif documents %}
   {%- set system_message = system_message + " Write the response to the user's input by strictly aligning with the facts in the provided documents. If the information needed to answer the question is not available in the documents, inform the user that the question cannot be answered based on the available data." %}
{%- else %}
   {%- set system_message = system_message + " You are a helpful AI assistant." %}
{%- endif %}
{%- if controls and 'citations' in controls and documents %}
   {%- set system_message = system_message + '\n\nIn your response, use the symbols <co> and </co> to indicate when a fact comes from a document in the search result, e.g <co>0</co> for a fact from document 0. Afterwards, list all the citations with their corresponding documents in an ordered list.' %}
{%- endif %}
{%- if controls and 'hallucinations' in controls and documents %}
   {%- set system_message = system_message + '\n\nFinally, after the response is written, include a numbered list of sentences from the response that are potentially hallucinated and not based in the documents.' %}
{%- endif %}
   {%- set loop_messages = messages %}
{%- endif %}
{{- '<|start_of_role|>system<|end_of_role|>' + system_message + '<|end_of_text|>\n' }}
{%- if tools %}
{{- '<|start_of_role|>tools<|end_of_role|>' }}
{{- tools | tojson(indent=4) }}
{{- '<|end_of_text|>\n' }}
{%- endif %}
{%- if documents %}
   {{- '<|start_of_role|>documents<|end_of_role|>' }}
{%- for document in documents %}
   {{- 'Document ' + loop.index0 | string + '\n' }}
   {{- document['text'] }}
   {%- if not loop.last %}
   {{- '\n\n'}}
{%- endif%}
{%- endfor %}
{{- '<|end_of_text|>\n' }}
{%- endif %}
{%- for message in loop_messages %}
   {{- '<|start_of_role|>' + message['role'] + '<|end_of_role|>' + message['content'] + '<|end_of_text|>\n' }}
{%- if loop.last and add_generation_prompt %}
   {{- '<|start_of_role|>assistant' }}
{%- if controls %}
   {{- ' ' + controls | tojson()}}
{%- endif %}
   {{- '<|end_of_role|>' }}
{%- endif %}
{%- endfor %})TEMPLATE",
    },
    // Llama-3.2-1B-Instruct-Q4_0.gguf, Llama-3.2-3B-Instruct-Q4_0.gguf, SummLlama3.2-3B-Q4_0.gguf (nomic-ai/gpt4all#3309)
    {
        // original
        R"TEMPLATE({{- bos_token }}
{%- if custom_tools is defined %}
    {%- set tools = custom_tools %}
{%- endif %}
{%- if not tools_in_user_message is defined %}
    {%- set tools_in_user_message = true %}
{%- endif %}
{%- if not date_string is defined %}
    {%- if strftime_now is defined %}
        {%- set date_string = strftime_now("%d %b %Y") %}
    {%- else %}
        {%- set date_string = "26 Jul 2024" %}
    {%- endif %}
{%- endif %}
{%- if not tools is defined %}
    {%- set tools = none %}
{%- endif %}

{#- This block extracts the system message, so we can slot it into the right place. #}
{%- if messages[0]['role'] == 'system' %}
    {%- set system_message = messages[0]['content']|trim %}
    {%- set messages = messages[1:] %}
{%- else %}
    {%- set system_message = "" %}
{%- endif %}

{#- System message #}
{{- "<|start_header_id|>system<|end_header_id|>\n\n" }}
{%- if tools is not none %}
    {{- "Environment: ipython\n" }}
{%- endif %}
{{- "Cutting Knowledge Date: December 2023\n" }}
{{- "Today Date: " + date_string + "\n\n" }}
{%- if tools is not none and not tools_in_user_message %}
    {{- "You have access to the following functions. To call a function, please respond with JSON for a function call." }}
    {{- 'Respond in the format {"name": function name, "parameters": dictionary of argument name and its value}.' }}
    {{- "Do not use variables.\n\n" }}
    {%- for t in tools %}
        {{- t | tojson(indent=4) }}
        {{- "\n\n" }}
    {%- endfor %}
{%- endif %}
{{- system_message }}
{{- "<|eot_id|>" }}

{#- Custom tools are passed in a user message with some extra guidance #}
{%- if tools_in_user_message and not tools is none %}
    {#- Extract the first user message so we can plug it in here #}
    {%- if messages | length != 0 %}
        {%- set first_user_message = messages[0]['content']|trim %}
        {%- set messages = messages[1:] %}
    {%- else %}
        {{- raise_exception("Cannot put tools in the first user message when there's no first user message!") }}
{%- endif %}
    {{- '<|start_header_id|>user<|end_header_id|>\n\n' -}}
    {{- "Given the following functions, please respond with a JSON for a function call " }}
    {{- "with its proper arguments that best answers the given prompt.\n\n" }}
    {{- 'Respond in the format {"name": function name, "parameters": dictionary of argument name and its value}.' }}
    {{- "Do not use variables.\n\n" }}
    {%- for t in tools %}
        {{- t | tojson(indent=4) }}
        {{- "\n\n" }}
    {%- endfor %}
    {{- first_user_message + "<|eot_id|>"}}
{%- endif %}

{%- for message in messages %}
    {%- if not (message.role == 'ipython' or message.role == 'tool' or 'tool_calls' in message) %}
        {{- '<|start_header_id|>' + message['role'] + '<|end_header_id|>\n\n'+ message['content'] | trim + '<|eot_id|>' }}
    {%- elif 'tool_calls' in message %}
        {%- if not message.tool_calls|length == 1 %}
            {{- raise_exception("This model only supports single tool-calls at once!") }}
        {%- endif %}
        {%- set tool_call = message.tool_calls[0].function %}
        {{- '<|start_header_id|>assistant<|end_header_id|>\n\n' -}}
        {{- '{"name": "' + tool_call.name + '", ' }}
        {{- '"parameters": ' }}
        {{- tool_call.arguments | tojson }}
        {{- "}" }}
        {{- "<|eot_id|>" }}
    {%- elif message.role == "tool" or message.role == "ipython" %}
        {{- "<|start_header_id|>ipython<|end_header_id|>\n\n" }}
        {%- if message.content is mapping or message.content is iterable %}
            {{- message.content | tojson }}
        {%- else %}
            {{- message.content }}
        {%- endif %}
        {{- "<|eot_id|>" }}
    {%- endif %}
{%- endfor %}
{%- if add_generation_prompt %}
    {{- '<|start_header_id|>assistant<|end_header_id|>\n\n' }}
{%- endif %})TEMPLATE",
        // replacement
        R"TEMPLATE({{- bos_token }}
{%- set date_string = strftime_now('%d %b %Y') %}

{#- This block extracts the system message, so we can slot it into the right place. #}
{%- if messages[0]['role'] == 'system' %}
    {%- set system_message = messages[0]['content'] | trim %}
    {%- set loop_start = 1 %}
{%- else %}
    {%- set system_message = '' %}
    {%- set loop_start = 0 %}
{%- endif %}

{#- System message #}
{{- '<|start_header_id|>system<|end_header_id|>\n\n' }}
{{- 'Cutting Knowledge Date: December 2023\n' }}
{{- 'Today Date: ' + date_string + '\n\n' }}
{{- system_message }}
{{- '<|eot_id|>' }}

{%- for message in messages %}
    {%- if loop.index0 >= loop_start %}
        {{- '<|start_header_id|>' + message['role'] + '<|end_header_id|>\n\n' + message['content'] | trim + '<|eot_id|>' }}
    {%- endif %}
{%- endfor %}
{%- if add_generation_prompt %}
    {{- '<|start_header_id|>assistant<|end_header_id|>\n\n' }}
{%- endif %})TEMPLATE",
    },
    // Llama-3.3-70B-Instruct-Q4_0.gguf (nomic-ai/gpt4all#3305)
    {
        // original
        R"TEMPLATE({{- bos_token }}
{%- if custom_tools is defined %}
    {%- set tools = custom_tools %}
{%- endif %}
{%- if not tools_in_user_message is defined %}
    {%- set tools_in_user_message = true %}
{%- endif %}
{%- if not date_string is defined %}
    {%- set date_string = "26 Jul 2024" %}
{%- endif %}
{%- if not tools is defined %}
    {%- set tools = none %}
{%- endif %}

{#- This block extracts the system message, so we can slot it into the right place. #}
{%- if messages[0]['role'] == 'system' %}
    {%- set system_message = messages[0]['content']|trim %}
    {%- set messages = messages[1:] %}
{%- else %}
    {%- set system_message = "" %}
{%- endif %}

{#- System message + builtin tools #}
{{- "<|start_header_id|>system<|end_header_id|>\n\n" }}
{%- if builtin_tools is defined or tools is not none %}
    {{- "Environment: ipython\n" }}
{%- endif %}
{%- if builtin_tools is defined %}
    {{- "Tools: " + builtin_tools | reject('equalto', 'code_interpreter') | join(", ") + "\n\n"}}
{%- endif %}
{{- "Cutting Knowledge Date: December 2023\n" }}
{{- "Today Date: " + date_string + "\n\n" }}
{%- if tools is not none and not tools_in_user_message %}
    {{- "You have access to the following functions. To call a function, please respond with JSON for a function call." }}
    {{- 'Respond in the format {"name": function name, "parameters": dictionary of argument name and its value}.' }}
    {{- "Do not use variables.\n\n" }}
    {%- for t in tools %}
        {{- t | tojson(indent=4) }}
        {{- "\n\n" }}
    {%- endfor %}
{%- endif %}
{{- system_message }}
{{- "<|eot_id|>" }}

{#- Custom tools are passed in a user message with some extra guidance #}
{%- if tools_in_user_message and not tools is none %}
    {#- Extract the first user message so we can plug it in here #}
    {%- if messages | length != 0 %}
        {%- set first_user_message = messages[0]['content']|trim %}
        {%- set messages = messages[1:] %}
    {%- else %}
        {{- raise_exception("Cannot put tools in the first user message when there's no first user message!") }}
{%- endif %}
    {{- '<|start_header_id|>user<|end_header_id|>\n\n' -}}
    {{- "Given the following functions, please respond with a JSON for a function call " }}
    {{- "with its proper arguments that best answers the given prompt.\n\n" }}
    {{- 'Respond in the format {"name": function name, "parameters": dictionary of argument name and its value}.' }}
    {{- "Do not use variables.\n\n" }}
    {%- for t in tools %}
        {{- t | tojson(indent=4) }}
        {{- "\n\n" }}
    {%- endfor %}
    {{- first_user_message + "<|eot_id|>"}}
{%- endif %}

{%- for message in messages %}
    {%- if not (message.role == 'ipython' or message.role == 'tool' or 'tool_calls' in message) %}
        {{- '<|start_header_id|>' + message['role'] + '<|end_header_id|>\n\n'+ message['content'] | trim + '<|eot_id|>' }}
    {%- elif 'tool_calls' in message %}
        {%- if not message.tool_calls|length == 1 %}
            {{- raise_exception("This model only supports single tool-calls at once!") }}
        {%- endif %}
        {%- set tool_call = message.tool_calls[0].function %}
        {%- if builtin_tools is defined and tool_call.name in builtin_tools %}
            {{- '<|start_header_id|>assistant<|end_header_id|>\n\n' -}}
            {{- "<|python_tag|>" + tool_call.name + ".call(" }}
            {%- for arg_name, arg_val in tool_call.arguments | items %}
                {{- arg_name + '="' + arg_val + '"' }}
                {%- if not loop.last %}
                    {{- ", " }}
                {%- endif %}
                {%- endfor %}
            {{- ")" }}
        {%- else  %}
            {{- '<|start_header_id|>assistant<|end_header_id|>\n\n' -}}
            {{- '{"name": "' + tool_call.name + '", ' }}
            {{- '"parameters": ' }}
            {{- tool_call.arguments | tojson }}
            {{- "}" }}
        {%- endif %}
        {%- if builtin_tools is defined %}
            {#- This means we're in ipython mode #}
            {{- "<|eom_id|>" }}
        {%- else %}
            {{- "<|eot_id|>" }}
        {%- endif %}
    {%- elif message.role == "tool" or message.role == "ipython" %}
        {{- "<|start_header_id|>ipython<|end_header_id|>\n\n" }}
        {%- if message.content is mapping or message.content is iterable %}
            {{- message.content | tojson }}
        {%- else %}
            {{- message.content }}
        {%- endif %}
        {{- "<|eot_id|>" }}
    {%- endif %}
{%- endfor %}
{%- if add_generation_prompt %}
    {{- '<|start_header_id|>assistant<|end_header_id|>\n\n' }}
{%- endif %})TEMPLATE",
        // replacement
        R"TEMPLATE({{- bos_token }}
{%- set date_string = strftime_now('%d %b %Y') %}

{#- This block extracts the system message, so we can slot it into the right place. #}
{%- if messages[0]['role'] == 'system' %}
    {%- set system_message = messages[0]['content'] | trim %}
    {%- set loop_start = 1 %}
{%- else %}
    {%- set system_message = '' %}
    {%- set loop_start = 0 %}
{%- endif %}

{#- System message #}
{{- '<|start_header_id|>system<|end_header_id|>\n\n' }}
{{- 'Cutting Knowledge Date: December 2023\n' }}
{{- 'Today Date: ' + date_string + '\n\n' }}
{{- system_message }}
{{- '<|eot_id|>' }}

{%- for message in messages %}
    {%- if loop.index0 >= loop_start %}
        {{- '<|start_header_id|>' + message['role'] + '<|end_header_id|>\n\n' + message['content'] | trim + '<|eot_id|>' }}
    {%- endif %}
{%- endfor %}
{%- if add_generation_prompt %}
    {{- '<|start_header_id|>assistant<|end_header_id|>\n\n' }}
{%- endif %})TEMPLATE",
    },
    // Llama3-DiscoLeo-Instruct-8B-32k-v0.1-Q4_0.gguf (nomic-ai/gpt4all#3347)
    {
        // original
        R"TEMPLATE({% set loop_messages = messages %}{% for message in loop_messages %}{% set content = '<|start_header_id|>' + message['role'] + '<|end_header_id|>

'+ message['content'] | trim + '<|eot_id|>' %}{% if loop.index0 == 0 %}{% set content = bos_token + content %}{% endif %}{{ content }}{% endfor %}{% if add_generation_prompt %}{{ '<|start_header_id|>assistant<|end_header_id|>

' }}{% endif %})TEMPLATE",
        // replacement
        R"TEMPLATE({%- for message in messages %}
    {%- set content = '<|start_header_id|>' + message['role'] + '<|end_header_id|>\n\n' + message['content'] | trim + '<|eot_id|>' %}
    {%- if loop.index0 == 0 %}
        {%- set content = bos_token + content %}
    {%- endif %}
    {{- content }}
{%- endfor %}
{%- if add_generation_prompt %}
    {{- '<|start_header_id|>assistant<|end_header_id|>\n\n' }}
{%- endif %})TEMPLATE",
    },
    // Meta-Llama-3.1-8B-Instruct-128k-Q4_0.gguf
    {
        // original
        R"TEMPLATE({% set loop_messages = messages %}{% for message in loop_messages %}{% set content = '<|start_header_id|>' + message['role'] + '<|end_header_id|>

'+ message['content'] | trim + '<|eot_id|>' %}{% if loop.index0 == 0 %}{% set content = bos_token + content %}{% endif %}{{ content }}{% endfor %}{{ '<|start_header_id|>assistant<|end_header_id|>

' }})TEMPLATE",
        // replacement
        R"TEMPLATE({%- set loop_messages = messages %}
{%- for message in loop_messages %}
    {%- set content = '<|start_header_id|>' + message['role'] + '<|end_header_id|>\n\n'+ message['content'] | trim + '<|eot_id|>' %}
    {%- if loop.index0 == 0 %}
        {%- set content = bos_token + content %}
    {%- endif %}
    {{- content }}
{%- endfor %}
{{- '<|start_header_id|>assistant<|end_header_id|>\n\n' }})TEMPLATE",
    },
    // Meta-Llama-3-8B-Instruct.Q4_0.gguf
    {
        // original
        R"TEMPLATE({% set loop_messages = messages %}{% for message in loop_messages %}{% set content = '<|start_header_id|>' + message['role'] + '<|end_header_id|>

'+ message['content'] | trim + '<|eot_id|>' %}{{ content }}{% endfor %}{% if add_generation_prompt %}{{ '<|start_header_id|>assistant<|end_header_id|>

' }}{% endif %})TEMPLATE",
        // replacement
        R"TEMPLATE({%- set loop_messages = messages %}
{%- for message in loop_messages %}
    {%- set content = '<|start_header_id|>' + message['role'] + '<|end_header_id|>\n\n'+ message['content'] | trim + '<|eot_id|>' %}
    {{- content }}
{%- endfor %}
{%- if add_generation_prompt %}
    {{- '<|start_header_id|>assistant<|end_header_id|>\n\n' }}
{%- endif %})TEMPLATE",
    },
    // Mistral-Nemo-Instruct-2407-Q4_0.gguf (nomic-ai/gpt4all#3284)
    {
        // original
        R"TEMPLATE({%- if messages[0]["role"] == "system" %}
    {%- set system_message = messages[0]["content"] %}
    {%- set loop_messages = messages[1:] %}
{%- else %}
    {%- set loop_messages = messages %}
{%- endif %}
{%- if not tools is defined %}
    {%- set tools = none %}
{%- endif %}
{%- set user_messages = loop_messages | selectattr("role", "equalto", "user") | list %}

{#- This block checks for alternating user/assistant messages, skipping tool calling messages #}
{%- set ns = namespace() %}
{%- set ns.index = 0 %}
{%- for message in loop_messages %}
    {%- if not (message.role == "tool" or message.role == "tool_results" or (message.tool_calls is defined and message.tool_calls is not none)) %}
        {%- if (message["role"] == "user") != (ns.index % 2 == 0) %}
            {{- raise_exception("After the optional system message, conversation roles must alternate user/assistant/user/assistant/...") }}
        {%- endif %}
        {%- set ns.index = ns.index + 1 %}
    {%- endif %}
{%- endfor %}

{{- bos_token }}
{%- for message in loop_messages %}
    {%- if message["role"] == "user" %}
        {%- if tools is not none and (message == user_messages[-1]) %}
            {{- "[AVAILABLE_TOOLS][" }}
            {%- for tool in tools %}
                {%- set tool = tool.function %}
                {{- '{"type": "function", "function": {' }}
                {%- for key, val in tool.items() if key != "return" %}
                    {%- if val is string %}
                        {{- '"' + key + '": "' + val + '"' }}
                    {%- else %}
                        {{- '"' + key + '": ' + val|tojson }}
                    {%- endif %}
                    {%- if not loop.last %}
                        {{- ", " }}
                    {%- endif %}
                {%- endfor %}
                {{- "}}" }}
                {%- if not loop.last %}
                    {{- ", " }}
                {%- else %}
                    {{- "]" }}
                {%- endif %}
            {%- endfor %}
            {{- "[/AVAILABLE_TOOLS]" }}
            {%- endif %}
        {%- if loop.last and system_message is defined %}
            {{- "[INST]" + system_message + "\n\n" + message["content"] + "[/INST]" }}
        {%- else %}
            {{- "[INST]" + message["content"] + "[/INST]" }}
        {%- endif %}
    {%- elif (message.tool_calls is defined and message.tool_calls is not none) %}
        {{- "[TOOL_CALLS][" }}
        {%- for tool_call in message.tool_calls %}
            {%- set out = tool_call.function|tojson %}
            {{- out[:-1] }}
            {%- if not tool_call.id is defined or tool_call.id|length != 9 %}
                {{- raise_exception("Tool call IDs should be alphanumeric strings with length 9!") }}
            {%- endif %}
            {{- ', "id": "' + tool_call.id + '"}' }}
            {%- if not loop.last %}
                {{- ", " }}
            {%- else %}
                {{- "]" + eos_token }}
            {%- endif %}
        {%- endfor %}
    {%- elif message["role"] == "assistant" %}
        {{- message["content"] + eos_token}}
    {%- elif message["role"] == "tool_results" or message["role"] == "tool" %}
        {%- if message.content is defined and message.content.content is defined %}
            {%- set content = message.content.content %}
        {%- else %}
            {%- set content = message.content %}
        {%- endif %}
        {{- '[TOOL_RESULTS]{"content": ' + content|string + ", " }}
        {%- if not message.tool_call_id is defined or message.tool_call_id|length != 9 %}
            {{- raise_exception("Tool call IDs should be alphanumeric strings with length 9!") }}
        {%- endif %}
        {{- '"call_id": "' + message.tool_call_id + '"}[/TOOL_RESULTS]' }}
    {%- else %}
        {{- raise_exception("Only user and assistant roles are supported, with the exception of an initial optional system message!") }}
    {%- endif %}
{%- endfor %})TEMPLATE",
        // replacement
        R"TEMPLATE({%- if messages[0]['role'] == 'system' %}
    {%- set system_message = messages[0]['content'] %}
    {%- set loop_start = 1 %}
{%- else %}
    {%- set loop_start = 0 %}
{%- endif %}

{{- bos_token }}
{%- for message in messages %}
    {#- This block checks for alternating user/assistant messages, skipping tool calling messages #}
    {%- if (message['role'] == 'user') != (loop.index0 % 2 == 0) %}
        {{- raise_exception('After the optional system message, conversation roles must alternate user/assistant/user/assistant/...') }}
    {%- endif %}

    {%- if message['role'] == 'user' %}
        {%- if loop.last and loop_start == 1 %}
            {{- '[INST]' + system_message + '\n\n' + message['content'] + '[/INST]' }}
        {%- else %}
            {{- '[INST]' + message['content'] + '[/INST]' }}
        {%- endif %}
    {%- elif message['role'] == 'assistant' %}
        {{- message['content'] + eos_token }}
    {%- else %}
        {{- raise_exception('Only user and assistant roles are supported, with the exception of an initial optional system message!') }}
    {%- endif %}
{%- endfor %})TEMPLATE",
    },
    // Nous-Hermes-2-Mistral-7B-DPO.Q4_0.gguf
    {
        // original
        R"TEMPLATE({% for message in messages %}{{'<|im_start|>' + message['role'] + '
' + message['content'] + '<|im_end|>' + '
'}}{% endfor %}{% if add_generation_prompt %}{{ '<|im_start|>assistant
' }}{% endif %})TEMPLATE",
        // replacement
        R"TEMPLATE({%- for message in messages %}
    {{- '<|im_start|>' + message['role'] + '\n' + message['content'] + '<|im_end|>\n' }}
{%- endfor %}
{%- if add_generation_prompt %}
    {{- '<|im_start|>assistant\n' }}
{%- endif %})TEMPLATE",
    },
    // occiglot-7b-de-en-instruct.Q4_0.gguf (nomic-ai/gpt4all#3283)
    {
        // original
        R"TEMPLATE({{'<s>'}}{% if messages[0]['role'] == 'system' %}{% set loop_messages = messages[1:] %}{% set system_message = messages[0]['content'] %}{% else %}{% set loop_messages = messages %}{% set system_message = 'You are a helpful assistant. Please give a long and detailed answer.' %}{% endif %}{% if not add_generation_prompt is defined %}{% set add_generation_prompt = false %}{% endif %}{% for message in loop_messages %}{% if loop.index0 == 0 %}{{'<|im_start|>system
' + system_message + '<|im_end|>
'}}{% endif %}{{'<|im_start|>' + message['role'] + '
' + message['content'] + '<|im_end|>' + '
'}}{% endfor %}{% if add_generation_prompt %}{{ '<|im_start|>assistant
' }}{% endif %})TEMPLATE",
        // replacement
        R"TEMPLATE({{- bos_token }}
{%- if messages[0]['role'] == 'system' %}
    {%- set loop_start = 1 %}
    {%- set system_message = messages[0]['content'] %}
{%- else %}
    {%- set loop_start = 0 %}
    {%- set system_message = 'You are a helpful assistant. Please give a long and detailed answer.' %}
{%- endif %}
{{- '<|im_start|>system\n' + system_message + '<|im_end|>\n' }}
{%- for message in messages %}
    {%- if loop.index0 >= loop_start %}
        {{- '<|im_start|>' + message['role'] + '\n' + message['content'] + '<|im_end|>\n' }}
    {%- endif %}
{%- endfor %}
{%- if add_generation_prompt %}
    {{- '<|im_start|>assistant\n' }}
{%- endif %})TEMPLATE",
    },
    // allenai/OLMoE-1B-7B-0924-Instruct-GGUF (nomic-ai/gpt4all#3053)
    {
        // original
        R"TEMPLATE({{ bos_token }}{% for message in messages %}
{% if message['role'] == 'system' %}
{{ '<|system|>
' + message['content'] }}
{% elif message['role'] == 'user' %}
{{ '<|user|>
' + message['content'] }}
{% elif message['role'] == 'assistant' %}
{{ '<|assistant|>
'  + message['content'] + eos_token }}
{% endif %}
{% if loop.last and add_generation_prompt %}
{{ '<|assistant|>' }}
{% endif %}
{% endfor %})TEMPLATE",
        // replacement
        R"TEMPLATE({{ bos_token }}
{% for message in messages %}
{% if message['role'] == 'system' %}
   {{ '<|system|>\n' + message['content'] }}
{% elif message['role'] == 'user' %}
   {{ '<|user|>\n' + message['content'] }}
{% elif message['role'] == 'assistant' %}
   {{ '<|assistant|>\n'  + message['content'] + eos_token }}
{% endif %}
{% if loop.last and add_generation_prompt %}
   {{ '<|assistant|>' }}
{% endif %}
{% endfor %})TEMPLATE",
    },
    // Phi-3.1-mini-128k-instruct-Q4_0.gguf (nomic-ai/gpt4all#3346)
    {
        // original
        R"TEMPLATE({% for message in messages %}{% if message['role'] == 'system' %}{{'<|system|>
' + message['content'] + '<|end|>
'}}{% elif message['role'] == 'user' %}{{'<|user|>
' + message['content'] + '<|end|>
'}}{% elif message['role'] == 'assistant' %}{{'<|assistant|>
' + message['content'] + '<|end|>
'}}{% endif %}{% endfor %}{% if add_generation_prompt %}{{ '<|assistant|>
' }}{% else %}{{ eos_token }}{% endif %})TEMPLATE",
        // replacement
        R"TEMPLATE({%- for message in messages %}
    {%- if message['role'] == 'system' %}
        {{- '<|system|>\n' + message['content'] + '<|end|>\n' }}
    {%- elif message['role'] == 'user' %}
        {{- '<|user|>\n' + message['content'] + '<|end|>\n' }}
    {%- elif message['role'] == 'assistant' %}
        {{- '<|assistant|>\n' + message['content'] + '<|end|>\n' }}
    {%- endif %}
{%- endfor %}
{%- if add_generation_prompt %}
    {{- '<|assistant|>\n' }}
{%- else %}
    {{- eos_token }}
{%- endif %})TEMPLATE",
    },
    // Phi-3-mini-4k-instruct.Q4_0.gguf
    {
        // original
        R"TEMPLATE({{ bos_token }}{% for message in messages %}{{'<|' + message['role'] + '|>' + '
' + message['content'] + '<|end|>
' }}{% endfor %}{% if add_generation_prompt %}{{ '<|assistant|>
' }}{% else %}{{ eos_token }}{% endif %})TEMPLATE",
        // replacement
        R"TEMPLATE({{- bos_token }}
{%- for message in messages %}
    {{- '<|' + message['role'] + '|>\n' + message['content'] + '<|end|>\n' }}
{%- endfor %}
{%- if add_generation_prompt %}
    {{- '<|assistant|>\n' }}
{%- else %}
    {{- eos_token }}
{%- endif %})TEMPLATE",
    },
    // qwen2-1_5b-instruct-q4_0.gguf (nomic-ai/gpt4all#3263), qwen2-72b-instruct-q4_0.gguf
    {
        // original
        R"TEMPLATE({% for message in messages %}{% if loop.first and messages[0]['role'] != 'system' %}{{ '<|im_start|>system
You are a helpful assistant.<|im_end|>
' }}{% endif %}{{'<|im_start|>' + message['role'] + '
' + message['content'] + '<|im_end|>' + '
'}}{% endfor %}{% if add_generation_prompt %}{{ '<|im_start|>assistant
' }}{% endif %})TEMPLATE",
        // replacement
        R"TEMPLATE({%- for message in messages %}
    {%- if loop.first and messages[0]['role'] != 'system' %}
        {{- '<|im_start|>system\nYou are a helpful assistant.<|im_end|>\n' }}
    {%- endif %}
    {{- '<|im_start|>' + message['role'] + '\n' + message['content'] + '<|im_end|>\n' }}
{%- endfor %}
{%- if add_generation_prompt %}
    {{- '<|im_start|>assistant\n' }}
{%- endif %})TEMPLATE",
    },
};
