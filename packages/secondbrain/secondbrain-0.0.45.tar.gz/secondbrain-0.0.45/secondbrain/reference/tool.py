import os
import importlib
from .lib.lib import ModuleManager, wrapped_func
from secondbrain import utils


params = utils.params


def ref_tools(tool_id, execution_config=None, working_directory=None, workspace_path=None):
    execution_path_type = execution_config.get("executionPathType", "codeFolder")
    ui_datas = execution_config.get("uiDatas", {})
    
    if workspace_path is None:
        workspace_path = params["workspacePath"]
    tool_base_path = os.path.join(workspace_path, "User/Local/Tool")
    module_path = os.path.join(tool_base_path, tool_id)
    module_path = os.path.normpath(os.path.abspath(module_path))

    if not os.path.exists(module_path):
        print(f"Tool {tool_id} not found")
        return []

    try:
        with ModuleManager(module_path) as manager:
            from secondbrain.tool.tool_decorator import all_tools, clear_tools
            clear_tools()
            importlib.import_module("tool")
            export_tools = [tool for tool in all_tools]

    except Exception as e:
        print(f"Error loading tool {tool_id}: {e}")
        return []
    
    if execution_path_type == 'codeFolder':
        working_directory = module_path

    ret_export_tools = []
    for tool in export_tools:
        tool = wrapped_func(tool, working_directory, ui_datas)
            
        if tool.__doc__ is None:
            tool.__doc__ = "This tool is used to " + tool.__name__.replace("_", " ") + "."
        ret_export_tools.append(tool)

    return ret_export_tools



