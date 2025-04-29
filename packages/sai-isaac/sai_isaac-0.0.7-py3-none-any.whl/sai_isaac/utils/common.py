import importlib
from typing import Any, Dict, Union
import inspect
import os
import yaml

import gymnasium as gym
import torch

def load_cfg_from_registry(task_name: str, entry_point_key: str) -> dict | object:
    """Load default configuration given its entry point from the gym registry.

    This function loads the configuration object from the gym registry for the given task name.
    It supports both YAML and Python configuration files.

    It expects the configuration to be registered in the gym registry as:

    .. code-block:: python

        gym.register(
            id="My-Awesome-Task-v0",
            ...
            kwargs={"env_entry_point_cfg": "path.to.config:ConfigClass"},
        )

    The parsed configuration object for above example can be obtained as:

    .. code-block:: python

        from isaaclab_tasks.utils.parse_cfg import load_cfg_from_registry

        cfg = load_cfg_from_registry("My-Awesome-Task-v0", "env_entry_point_cfg")

    Args:
        task_name: The name of the environment.
        entry_point_key: The entry point key to resolve the configuration file.

    Returns:
        The parsed configuration object. If the entry point is a YAML file, it is parsed into a dictionary.
        If the entry point is a Python class, it is instantiated and returned.

    Raises:
        ValueError: If the entry point key is not available in the gym registry for the task.
    """
    # obtain the configuration entry point
    cfg_entry_point = gym.spec(task_name).kwargs.get(entry_point_key)
    # check if entry point exists
    if cfg_entry_point is None:
        raise ValueError(
            f"Could not find configuration for the environment: '{task_name}'."
            f" Please check that the gym registry has the entry point: '{entry_point_key}'."
        )
    # parse the default config file
    if isinstance(cfg_entry_point, str) and cfg_entry_point.endswith(".yaml"):
        if os.path.exists(cfg_entry_point):
            # absolute path for the config file
            config_file = cfg_entry_point
        else:
            # resolve path to the module location
            mod_name, file_name = cfg_entry_point.split(":")
            mod_path = os.path.dirname(importlib.import_module(mod_name).__file__)
            # obtain the configuration file path
            config_file = os.path.join(mod_path, file_name)
        # load the configuration
        print(f"[INFO]: Parsing configuration from: {config_file}")
        with open(config_file, encoding="utf-8") as f:
            cfg = yaml.full_load(f)
    else:
        if callable(cfg_entry_point):
            # resolve path to the module location
            mod_path = inspect.getfile(cfg_entry_point)
            # load the configuration
            cfg_cls = cfg_entry_point()
        elif isinstance(cfg_entry_point, str):
            # resolve path to the module location
            mod_name, attr_name = cfg_entry_point.split(":")
            mod = importlib.import_module(mod_name)
            cfg_cls = getattr(mod, attr_name)
        else:
            cfg_cls = cfg_entry_point
        # load the configuration
        print(f"[INFO]: Parsing configuration from: {cfg_entry_point}")
        if callable(cfg_cls):
            cfg = cfg_cls()
        else:
            cfg = cfg_cls
    return cfg


def create_isaacsim_env(
    env_entry_point: Union[str, Any],
    env_cfg_entry_point: Union[str, Any],
    env_cfg: Union[Dict[str, Any], object, None] = None,
    app_cfg: Union[Dict[str, Any], None] = None,
    render_mode: Union[str, None] = None,
) -> gym.Env:
    """Create an IsaacSim environment with the specified configuration.

    This function creates and initializes an IsaacSim environment using the provided
    entry points for both the environment and its configuration. It handles CUDA availability
    checks and IsaacLab package imports.

    Args:
        env_entry_point: Either a string in the format "module:class" or a class object
            representing the environment to create.
        env_cfg_entry_point: Either a string in the format "module:class" or a class object
            representing the environment configuration.
        env_cfg: A dictionary containing the configuration for the environment.
        app_cfg: A dictionary containing the configuration for the IsaacSim app.
        render_mode: The rendering mode to use for the environment.
    Returns:
        A Gymnasium environment instance.

    Raises:
        ValueError: If the entry points are invalid or not properly formatted.
    """

    # Check if CUDA is available
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is not available on this device")

    # Import IsaacLab packages
    try:
        from isaaclab.app import AppLauncher  # noqa: F401
    except ImportError:
        raise ImportError(
            "Please install the `isaaclab` package to use the IsaacSimGym"
        )
    # Launch Isaac Sim
    if app_cfg is None:
        app_cfg = {}

    # Some environments have custom cameras
    if isinstance(app_cfg, dict):
        app_cfg.update({"enable_cameras": True})

    AppLauncher(app_cfg)

    # Parse and import environment class
    if isinstance(env_entry_point, str):
        try:
            mod_name, cls_name = env_entry_point.rsplit(":", 1)
            mod = importlib.import_module(mod_name)
            entry_cls = getattr(mod, cls_name)
        except (ValueError, ImportError, AttributeError) as e:
            raise ValueError(
                f"Invalid environment entry point '{env_entry_point}': {str(e)}"
            )
    else:
        entry_cls = env_entry_point

    # Parse and import environment configuration
    if isinstance(env_cfg_entry_point, str):
        try:
            mod_name, cls_name = env_cfg_entry_point.rsplit(":", 1)
            mod = importlib.import_module(mod_name)
            env_cfg_cls = getattr(mod, cls_name)()
        except (ValueError, ImportError, AttributeError) as e:
            raise ValueError(
                f"Invalid environment config entry point '{env_cfg_entry_point}': {str(e)}"
            )
    else:
        env_cfg_cls = env_cfg_entry_point

    if env_cfg is not None:
        if isinstance(env_cfg, dict):
            env_cfg_cls.from_dict(env_cfg)
        elif isinstance(env_cfg, type(env_cfg_cls)):
            env_cfg_cls = env_cfg
        else:
            raise ValueError(
                f"Invalid environment config entry point '{env_cfg_entry_point}'"
            )

    return entry_cls(cfg=env_cfg_cls, render_mode=render_mode)
