import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import dcc, html
from dash.dependencies import Input, Output, State
from sqlalchemy import create_engine

MATHJAX_CDN = 'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=TeX-MML-AM_CHTML'

external_scripts = [
    {
        'type': 'text/javascript',
        'id': 'MathJax-script',
        'src': MATHJAX_CDN,
    },
]

# -----------------------------------------------------------------------------
# Helper functions


# -----------------------------------------------------------------------------
# Custom styles

# the style arguments for the sidebar.
SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '20%',
    'padding': '20px 10px',
    'background-color': '#f8f9fa',
    'overflow': 'scroll'
}

# the style arguments for the main content page.
CONTENT_STYLE = {
    'margin-left': '25%',
    'margin-right': '5%',
    'padding': '20px 10p'
}

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                external_scripts=external_scripts,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}])

database = 'data/sdb_grid.db'
engine = create_engine(f'sqlite:///{database}')
df = pd.read_sql('models', engine)
df['Teff'] = 10.0 ** df['log_Teff']
columns = list(df.columns)

hover_data = ['Teff', 'log_g', 'z_i', 'm_i', 'm_env', 'center_he4',
              'log_L', 'radius', 'age']

controls = dbc.Container(
    [
        dbc.Card([
            dbc.Label('Select color:'),
            dcc.Dropdown(
                id='dropdown_colors',
                options=[
                    {'label': 'z_i', 'value': 'z_i'},
                    {'label': 'm_i', 'value': 'm_i'},
                    {'label': 'm_env', 'value': 'm_env'},
                    {'label': 'center_he4', 'value': 'custom_profile'},
                ],
                value='m_i',
                multi=False
            )]),
        dbc.Card([
            dbc.Label('Select symbols:'),
            dcc.Dropdown(
                id='dropdown_symbols',
                options=[
                    {'label': 'z_i', 'value': 'z_i'},
                    {'label': 'm_i', 'value': 'm_i'},
                    {'label': 'm_env', 'value': 'm_env'},
                    {'label': 'center_he4', 'value': 'custom_profile'},
                ],
                value='z_i',
                multi=False
            )]),
        html.Br(),
        dbc.Card([
            dbc.Label('Z_i'),
            dcc.RangeSlider(
                id='z_i_slider',
                min=0.005,
                max=0.035,
                step=0.005,
                marks={0.001 * x: f'{0.001 * x:.3f}' if (x % 10 != 0) else ''
                       for x in range(5, 40, 5)},
                tooltip={'placement': 'bottom', 'always_visible': False},
                value=[0.005, 0.035]
            )]),
        dbc.Card([
            dbc.Label('M_i [M_s]'),
            dcc.RangeSlider(
                id='m_i_slider',
                min=1.0,
                max=1.8,
                step=0.05,
                marks={0.01 * x: f'{0.01 * x:.1f}' if (x % 10 == 0) else ''
                       for x in range(100, 190, 5)},
                tooltip={'placement': 'bottom', 'always_visible': False},
                value=[1.0, 1.5]
            )]),
        dbc.Card([
            dbc.Label('M_env [M_s]'),
            dcc.RangeSlider(
                id='m_env_slider',
                min=0.0,
                max=0.01,
                step=0.001,
                marks={0.001 * x: f'{0.001 * x:.3f}' if (x % 2 == 0) else ''
                       for x in range(0, 11, 1)},
                tooltip={'placement': 'bottom', 'always_visible': False},
                value=[0.0, 0.003]
            )]),
        dbc.Card([
            dbc.Label('Y_c'),
            dcc.RangeSlider(
                id='y_c_slider',
                min=0.1,
                max=0.9,
                step=0.05,
                marks={0.05 * x: f'{0.05 * x:.2f}' if (x % 2 == 0) else ''
                       for x in range(0, 20, 1)},
                tooltip={'placement': 'bottom', 'always_visible': False},
                value=[0.1, 0.9]
            )]),
        html.Br(),
        dbc.Card([
            dbc.Label('Hover data'),
            dcc.Dropdown(
                id='dropdown_hover_data',
                options=[{'label': x, 'value': x} for x in df.columns],
                value=hover_data,
                multi=True
            )]),
        html.Br(),
        html.Div([
            dbc.Button(
                id='submit_button',
                n_clicks=0,
                children='Submit',
                color='primary',
            ),
        ],
            className='d-grid gap-2',
        ),
    ],
    className='text-center'
)

sidebar = html.Div(
    [
        html.H2('Settings', className='text-center'),
        html.Hr(),
        controls
    ],
    style=SIDEBAR_STYLE,
)

content_first_row = dbc.Row(
    [
        dbc.Col(dcc.Graph(id='logg-teff'), md=12)
    ]
)

content = html.Div(
    [
        html.H2(f'sdB Grid Viewer', className='text-center'),
        html.Hr(),
        content_first_row,
    ],
    style=CONTENT_STYLE
)

app.layout = html.Div([sidebar, content])


@app.callback(
    Output('logg-teff', 'figure'),
    Input('submit_button', 'n_clicks'),
    State('dropdown_colors', 'value'),
    State('dropdown_symbols', 'value'),
    State('z_i_slider', 'value'),
    State('m_i_slider', 'value'),
    State('m_env_slider', 'value'),
    State('y_c_slider', 'value'),
    State('dropdown_hover_data', 'value'),
)
def update_logg_teff(n_clicks,
                     colors_value,
                     symbols_value,
                     z_i_slider_value,
                     m_i_slider_value,
                     m_env_slider_value,
                     y_c_slider_value,
                     hover_data_value):
    dff = df[(df['z_i'] >= min(z_i_slider_value))
             & (df['z_i'] <= max(z_i_slider_value))]
    dff = dff[(dff['m_i'] >= min(m_i_slider_value))
              & (dff['m_i'] <= max(m_i_slider_value))]
    dff = dff[(dff['m_env'] >= min(m_env_slider_value))
              & (dff['m_env'] <= max(m_env_slider_value))]
    dff = dff[(dff['custom_profile'] >= min(y_c_slider_value))
              & (dff['custom_profile'] <= max(y_c_slider_value))]

    fig = px.scatter(
        data_frame=dff,
        x='Teff',
        y='log_g',
        color=colors_value,
        # color_continuous_scale='Inferno',
        symbol=symbols_value,
        hover_data=hover_data_value,
        # labels={
        #     'Teff': r'$T_\mathrm{eff}$',
        #     'log_g': r'$\log\,g$'
        # },
    )
    fig.update_layout(legend_orientation='h')
    fig.update_layout(height=800)
    fig.update_xaxes(autorange='reversed')
    fig.update_yaxes(autorange='reversed')

    return fig


if __name__ == '__main__':
    app.run_server(port=8085, debug=True)
