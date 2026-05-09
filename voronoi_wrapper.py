# voronoi_wrapper.py
import os
import streamlit.components.v1 as components

# 1. Get the absolute path to your component folder
_PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
_component_path = os.path.join(_PROJECT_ROOT, "components", "voronoi_treemap")

# 2. Declare the component here at the module level
_voronoi_chart = components.declare_component(
    "voronoi_chart", 
    path=_component_path
)

# 3. Create a clean wrapper function to use in your app
def render_voronoi(chart_data, selected_country, key=None):
    return _voronoi_chart(
        chart_data=chart_data,
        selected_country=selected_country,
        key=key,
        default=selected_country
    )