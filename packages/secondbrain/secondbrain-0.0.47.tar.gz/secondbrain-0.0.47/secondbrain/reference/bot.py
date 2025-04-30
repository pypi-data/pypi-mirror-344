import os
from .lib.lib import ModuleManager, wrapped_func
import json
from secondbrain import utils

bot_index = 0

params = utils.params


def ref_bot(bot_id, config=None, workspace_path=None):
    global bot_index
    if workspace_path is None:
        workspace_path = params["workspacePath"]
    tool_base_path = os.path.join(workspace_path, "User/Local/Bot")
    code_folder = os.path.join(tool_base_path, bot_id)
    code_folder = os.path.normpath(os.path.abspath(code_folder))

    if not os.path.exists(code_folder):
        print(f"Bot {bot_id} not found in:" + code_folder)
        return None

    try:
        with ModuleManager(code_folder) as manager:
            info = code_folder + "/info.json"
            with open(info, "r", encoding="utf-8") as f:
                info = json.load(f)
            name = info["name"]
            random_name = "bot_" + str(bot_index)
            bot_index += 1
            function_code = f"""
def {random_name}(command:str) -> str:
    \"\"\"Receives any command string and returns the string result after the AI role ({name} expert) deeply thinks and executes the command.
    The AI role ({name} expert) is skilled at using various tools and provides professional and more accurate results.

    Args:
        command (str): The command string that the AI role ({name} expert) needs to execute.

    Returns:
        str: The result after the AI role ({name} expert) executes the command.
    \"\"\"
    from secondbrain import bot
    from secondbrain import utils
    import tempfile
    import sys

    with tempfile.NamedTemporaryFile(delete=True, mode='w+t') as temp_file:
        sys.stdout = temp_file  # 将输出重定向到临时文件，防止影响AI结果
        result = bot.get_chat_response("botSetting.json", command)
        sys.stdout = sys.__stdout__  # 恢复标准输出
    return result
"""
            exec(function_code)
            tool = eval(random_name)
            tool = wrapped_func(tool, code_folder)

            return tool
    except Exception as e:
        print(f"Error loading bot {bot_id}: {e}")
        return None
