import ipywidgets as widgets

def get_output_model_id(output_object: widgets.Output):
    if output_object:
        return output_object.outputs[0]["data"]["application/vnd.jupyter.widget-view+json"]["model_id"]
    