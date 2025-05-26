import os
import re
import subprocess
from flask import Flask, request, render_template, render_template_string
import html 

app = Flask(__name__)
app.secret_key = os.urandom(32)

def flexible_command_executor(command_parts):
    if not isinstance(command_parts, list) or len(command_parts) == 0:
        return "Error: Command must be a list of arguments."

    executable = command_parts[0].lower()
    
    allowed_executables = ["cat", "ls", "echo", "uname", "id", "pwd", "find", "grep"]
    if executable not in allowed_executables:
        return f"Error: Executable '{executable}' is not on the allowed list for this interface."

    dangerous_strings_in_args = ["&", ";", "|", "`", "$(", ")", "&&", "||", ">", "<", "$(("] 
    for part in command_parts:
        for dangerous in dangerous_strings_in_args:
            if dangerous in str(part): 
                return f"Error: Command part '{part}' contains a highly restricted character/pattern: '{dangerous}'."

    try:
        result = subprocess.run(command_parts, capture_output=True, text=True, timeout=5, check=False)
        
        output = ""
        if result.stdout:
            output += f"[OUTPUT]:\n{result.stdout}\n"
        if result.stderr:
            output += f"[OUTPUT]:\n{result.stderr}\n" 
        
        if not output:
            output = "[Command executed, no output produced or an issue occurred]"
            
        output += f"\n[Exit Code: {result.returncode}]"
        return output

    except subprocess.TimeoutExpired:
        return "Error: Command timed out."
    except FileNotFoundError: 
        return f"Error: Executable '{command_parts[0]}' not found."
    except Exception as e:
        return f"Error during command execution: {str(e)}"

app.config['GENERAL_COMMAND_INTERFACE'] = flexible_command_executor
app.config['APP_VERSION'] = "2.0.0-RCE_Edition" 
app.config['WELCOME_MESSAGE'] = "flagflag."

SENSITIVE_KEYWORDS = [
    "__class__", "__mro__", "__base__", "__subclasses__", "__globals__", 
    "__builtins__", "__import__", "__init__", "__dict__",
    "eval", "exec", "open", "read", "write", "system", "popen", "subprocess",
    "os", "environ", "sys", "platform", "getattr", "setattr", "delattr",
    "lipsum", "cycler", "joiner", "namespace", "config.update", "config.from_",
    "application.config", "current_app.config", "url_for", "get_flashed_messages",
    "request.args", "request.form", "request.cookies", "request.headers",
    "|join", "|attr", "|map", "|sum", "|sort", "|reverse",
    "{{_", "{%_",
    "self", "handler", "app."
]

DANGEROUS_PATTERNS = re.compile(
    r"(\.__[a-zA-Z_0-9]*__)|"
    r"(\{\{[^\{]*?(?:"
        r"\._|\.append\b|\.pop\b|\.insert\b|\.update\b|"
        r"\[\s*(?P<q_inner>'|\")_(.*?)(?P=q_inner)\s*\]|"
        r"eval\b|exec\b|compile\b|open\b|read\b|write\b|system\b|popen\b|subprocess\b|"
        r"os\b|sys\b|platform\b|getattr\b|setattr\b|delattr\b|import\b|builtins\b|globals\b|locals\b"
    r").*?\}\})|"
    r"(\._[a-zA-Z_0-9]*)|" 
    r"(\[\s*(?P<q_outer>'|\")_(.*?)(?P=q_outer)\s*\])|"
    r"(\{\%)|(\{\#)"
)

TARGET_PAYLOAD_REGEX = re.compile(r"\{\{\s*config\s*\[\s*('|\")GENERAL_COMMAND_INTERFACE\1\s*\]\s*\((.*?)\)\s*\}\}", re.IGNORECASE | re.DOTALL)
SIMPLE_CONFIG_REGEX = re.compile(r"\{\{\s*config\s*\}\}", re.IGNORECASE)


def sanitize_and_filter(user_input_str):
    if not isinstance(user_input_str, str):
        return "[Invalid Input Type]"
    sanitized_input = user_input_str
    is_target_payload = bool(TARGET_PAYLOAD_REGEX.fullmatch(sanitized_input))
    is_simple_config_display = bool(SIMPLE_CONFIG_REGEX.fullmatch(sanitized_input))

    if is_target_payload or is_simple_config_display:
        return sanitized_input 
    sanitized_input = re.sub(r"(\{\%)|(\{\#)", "[CTRL_CMNT_FILT]", sanitized_input)
    try:
        sanitized_input = DANGEROUS_PATTERNS.sub("[PATT_FILT]", sanitized_input)
    except TimeoutError: 
        return "[FILTER_TIMEOUT]"
    for keyword in SENSITIVE_KEYWORDS:
        sanitized_input = re.sub(r'(?i)' + re.escape(keyword), f"[KW_FILT:{keyword[:5]}]", sanitized_input)
    return sanitized_input

@app.route('/', methods=['GET', 'POST'])
def home():
    output = None
    error = None
    last_input_val = ""

    if request.method == 'POST':
        user_input = request.form.get('user_input', '')
        last_input_val = user_input
        sanitized_input = sanitize_and_filter(user_input)

        if not sanitized_input.strip():
            if user_input.strip():
                 error = "Input was fully sanitized or became empty."
            else:
                 error = "Input was empty. Please provide a probe."
        elif ("[PATT_FILT]" in sanitized_input or \
              "[KW_FILT" in sanitized_input or \
              "[CTRL_CMNT_FILT]" in sanitized_input) and \
             not (TARGET_PAYLOAD_REGEX.fullmatch(sanitized_input) or SIMPLE_CONFIG_REGEX.fullmatch(sanitized_input)):
            error = f"Input contains disallowed patterns/keywords or was altered. Processed: {html.escape(sanitized_input)}"
        else:
            is_target_payload_structure = bool(TARGET_PAYLOAD_REGEX.fullmatch(sanitized_input))
            is_simple_config_display = bool(SIMPLE_CONFIG_REGEX.fullmatch(sanitized_input))
            is_likely_simple_text = not any(c in sanitized_input for c in "{{}}") and not (is_target_payload_structure or is_simple_config_display)

            if is_target_payload_structure or is_simple_config_display or is_likely_simple_text:
                try:
                    rendered_output = render_template_string(sanitized_input)
                    if is_simple_config_display:
                        output = f"<pre>{html.escape(rendered_output)}</pre>"
                    elif is_target_payload_structure:
                        output = f"<pre>{html.escape(rendered_output)}</pre>"
                    else: 
                        output = html.escape(rendered_output)
                except Exception as e:
                    print(f"Render_template_string error for input '{sanitized_input}': {e}", flush=True)
                    error = "Template rendering error. Invalid syntax or restricted operation within the template engine."
            else:
                 error = f"Processed input '{html.escape(sanitized_input)}' has an invalid structure for direct rendering."

    return render_template('index.html', 
                           output_message=output, 
                           error_message=error, 
                           last_input=last_input_val)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)