import dash_bootstrap_components as dbc
from dash import dcc


def input_group(label, component_id, value, input_type='text', placeholder=None, **kwargs):
    match input_type:
        case 'text':
            return dbc.InputGroup(
                [dbc.InputGroupText(label), dbc.Input(placeholder=placeholder, id=component_id, value=value)],
                className="mb-3",
            ),
        case 'number':
            return dbc.InputGroup(
                [dbc.InputGroupText(label),
                 dbc.Input(placeholder=placeholder, id=component_id, value=value, type='number')],
                className="mb-3",
            ),
        case 'date':
            return dbc.InputGroup(
                [dbc.InputGroupText(label), dcc.DatePickerSingle(id=component_id, date=value)],
                className="mb-3",
            )
        case 'dropdown':
            return dbc.InputGroup(
                [dbc.InputGroupText(label),
                 dbc.Select(id=component_id, value=value, options=kwargs.get('options', []))],
                className="mb-3",
            )
