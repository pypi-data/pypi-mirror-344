from jennifer.agent import jennifer_agent
from distutils.version import LooseVersion

__hooking_module__ = 'uvloop'
__minimum_python_version__ = LooseVersion("3.8")
__target_version = None
_original_uvloop_Loop_run_in_executor = None


def get_target_version():
    global __target_version
    return str(__target_version)


def wrap_Loop_run_in_executor(run_in_executor):

    def handler(*args, **kwargs):
        return run_in_executor(*args, **kwargs)

    return handler


def _safe_get(properties, idx, default=None):
    try:
        return properties[idx]
    except IndexError:
        return default


def unhook(uvloop_module):
    pass


def hook(uvloop_module):
    global __target_version
    __target_version = uvloop_module.__version__

    global _original_uvloop_Loop_run_in_executor
    if 'wrap_Loop_run_in_executor.' in str(uvloop_module.Loop.run_in_executor):
        return False

    _original_uvloop_Loop_run_in_executor = uvloop_module.Loop.run_in_executor
    uvloop_module.Loop.run_in_executor = wrap_Loop_run_in_executor(uvloop_module.Loop.run_in_executor)

    return True
