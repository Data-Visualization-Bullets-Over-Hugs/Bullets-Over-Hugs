"""
Thin wrapper so declare_component is called from a real importable module,
not from inside Streamlit's exec() page runner (which has no __module__).
"""
import os
import streamlit.components.v1 as _c

_COMP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "components", "voronoi_treemap")
render = _c.declare_component("voronoi_treemap", path=_COMP_DIR)
