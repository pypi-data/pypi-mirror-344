import os
import importlib
from .lib.lib import ModuleManager, wrapped_func
from secondbrain import utils


params = utils.params


def _ref_workflows(workflow_id, execution_config=None, workspace_path=None):
    if workspace_path is None:
        workspace_path = params["workspacePath"]
    tool_base_path = os.path.join(workspace_path, "User/Local/Workflow")
    code_folder = os.path.join(tool_base_path, workflow_id)
    code_folder = os.path.normpath(os.path.abspath(code_folder))

    if not os.path.exists(code_folder):
        print(f"Workflow {workflow_id} not found")
        return []

    try:
        with ModuleManager(code_folder) as manager:
            from secondbrain.tool.tool_decorator import all_tools, clear_tools
            clear_tools()
            importlib.import_module("tool")
            export_tools = [tool for tool in all_tools]

    except Exception as e:
        print(f"Error loading workflow {workflow_id}: {e}")
        return []

    ret_export_tools = []
    for tool in export_tools:
        tool = wrapped_func(tool, code_folder)
        if tool.__doc__ is None:
            tool.__doc__ = "This tool is used to " + tool.__name__.replace("_", " ") + "."
        ret_export_tools.append(tool)

    return ret_export_tools


def ref_workflow(workflow_id, workspace_path=None):
    tools = _ref_workflows(workflow_id, workspace_path=workspace_path)
    if len(tools) > 0:
        return tools[0]
    else:
        return None
