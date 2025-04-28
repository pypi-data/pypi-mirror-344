import os
import streamlit.components.v1 as components

_RELEASE = True

if not _RELEASE:
    _component_func = components.declare_component(
        "mas_cookie_manager",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "build")
    _component_func = components.declare_component(
        "mas_cookie_manager", path=build_dir
    )

def cookie_manager(action: str, name: str, value: str = "", days: int = 1):
    return _component_func(action=action, name=name, value=value, days=days, default=None)
