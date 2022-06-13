from pathlib import Path

import dash
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.express as px
from dash import dcc, html, Input, Output, State
from sqlalchemy import create_engine

SIDEBAR_STYLE = {
    'overflow': 'scroll'
}

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}])

server = app.server

database = 'data/sdb_grid.db'
engine = create_engine(f'sqlite:///{database}')
df = pd.read_sql('models', engine)
df['Teff'] = 10.0 ** df['log_Teff']
df['L'] = 10.0 ** df['log_L']
cols_to_remove = ['rot_i', 'rot', 'fh', 'fhe', 'fsh', 'mlt', 'sc', 'reimers',
                  'blocker', 'turbulence', 'model_number', 'level',
                  'log_Teff', 'log_L', 'top_dir', 'log_dir']
df = df.drop(columns=cols_to_remove)
df.rename(columns={'custom_profile': 'y_c'}, inplace=True)
columns = list(df.columns)

hover_data = ['Teff', 'log_g', 'z_i', 'm_i', 'm_env', 'y_c',
              'L', 'radius', 'age']

about_file = Path('assets/about.md')
with about_file.open('r') as f:
    about = f.read()

controls = dbc.Container([
    dbc.Card([
        dbc.Label('Select a color:'),
        dbc.Select(
            id='dropdown_colors',
            options=[
                {'label': 'z_i', 'value': 'z_i'},
                {'label': 'm_i', 'value': 'm_i'},
                {'label': 'm_env', 'value': 'm_env'},
                {'label': 'center_he4', 'value': 'y_c'},
            ],
            value='z_i',
            persistence=True
        )]),
    dbc.Card([
        dbc.Label('Select symbols:'),
        dbc.Select(
            id='dropdown_symbols',
            options=[
                {'label': 'z_i', 'value': 'z_i'},
                {'label': 'm_i', 'value': 'm_i'},
                {'label': 'm_env', 'value': 'm_env'},
                {'label': 'center_he4', 'value': 'y_c'},
            ],
            value='m_i',
            persistence=True
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
            value=[0.005, 0.035],
            persistence=True
        )]),
    dbc.Card([
        dbc.Label('M_i [Ms]'),
        dcc.RangeSlider(
            id='m_i_slider',
            min=1.0,
            max=1.8,
            step=0.05,
            marks={0.01 * x: f'{0.01 * x:.1f}' if (x % 10 == 0) else ''
                   for x in range(100, 190, 5)},
            tooltip={'placement': 'bottom', 'always_visible': False},
            value=[1.0, 1.5],
            persistence=True
        )]),
    dbc.Card([
        dbc.Label('M_env [Ms]'),
        dcc.RangeSlider(
            id='m_env_slider',
            min=0.0,
            max=0.01,
            step=0.001,
            marks={0.001 * x: f'{0.001 * x:.3f}' if (x % 2 == 0) else ''
                   for x in range(0, 11, 1)},
            tooltip={'placement': 'bottom', 'always_visible': False},
            value=[0.0, 0.003],
            persistence=True
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
            value=[0.1, 0.9],
            persistence=True
        )]),
    html.Br(),
    dbc.Card([
        dbc.Label('Hover data'),
        dcc.Dropdown(
            id='dropdown_hover_data',
            options=[{'label': x, 'value': x} for x in df.columns],
            value=hover_data,
            multi=True,
            persistence=True
        )]),
    html.Br(),
    dbc.Card([
        dbc.Label('Target (optional)'),
        dbc.Card([
            dbc.InputGroup([
                dbc.InputGroupText('Teff:'),
                dbc.Input(
                    id='target_teff',
                    type='number',
                    value=None,
                    persistence=True
                ),
                dbc.InputGroupText('K'),
            ]),
            dbc.InputGroup([
                dbc.InputGroupText('dTeff:'),
                dbc.Input(
                    id='target_teff_err',
                    type='number',
                    value=None,
                    persistence=True
                ),
                dbc.InputGroupText('K'),
            ]),
        ],
            className='mb-2'),
        dbc.Card([
            dbc.InputGroup([
                dbc.InputGroupText('logg:'),
                dbc.Input(
                    id='target_logg',
                    inputmode='numeric',
                    type='number',
                    value=None,
                    persistence=True
                ),
                dbc.InputGroupText('(cgs)'),
            ]),
            dbc.InputGroup([
                dbc.InputGroupText('dlogg'),
                dbc.Input(
                    id='target_logg_err',
                    inputmode='numeric',
                    type='number',
                    value=None,
                    persistence=True
                ),
                dbc.InputGroupText('(cgs)'),
            ]),
        ],
            className='mb-2'),
        dbc.Card([
            dbc.InputGroup([
                dbc.InputGroupText('L:'),
                dbc.Input(
                    id='target_lum',
                    inputmode='numeric',
                    type='number',
                    value=None,
                    persistence=True
                ),
                dbc.InputGroupText('Ls'),
            ]),
            dbc.InputGroup([
                dbc.InputGroupText('dL'),
                dbc.Input(
                    id='target_lum_err',
                    inputmode='numeric',
                    type='number',
                    value=None,
                    persistence=True
                ),
                dbc.InputGroupText('Ls'),
            ]),
        ],
            className='mb-2'),
        dbc.Card([
            dbc.InputGroup([
                dbc.InputGroupText('R:'),
                dbc.Input(
                    id='target_rad',
                    inputmode='numeric',
                    type='number',
                    value=None,
                    persistence=True
                ),
                dbc.InputGroupText('Rs'),
            ]),
            dbc.InputGroup([
                dbc.InputGroupText('dR'),
                dbc.Input(
                    id='target_rad_err',
                    inputmode='numeric',
                    type='number',
                    value=None,
                    persistence=True
                ),
                dbc.InputGroupText('Rs'),
            ]),
        ],
            className='mb-2'),
        dbc.Card([
            dbc.RadioItems(
                options=[{'label': f'{n} sigma', 'value': n} for n in
                         range(1, 4)],
                value=1,
                id='select_sigma',
                inline=True,
                persistence=True
            ),
            dbc.Row([
                dbc.Col([
                    dbc.Label('Select a color:')
                ]),
                dbc.Col([
                    dbc.Input(
                        type='color',
                        id='colorpicker',
                        value='#000000',
                        style={'width': 100, 'height': 40},
                        persistence=True
                    )
                ])
            ],
                align='center'),
        ])
    ]),
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
    html.Br(),
    html.Br(),
    html.Br(),
],
    className='text-center'
)

sidebar = html.Div([
    html.H2('sdB Grid Viewer', className='text-center'),
    html.Hr(),
    controls
],
    className='bg-light',
    style=SIDEBAR_STYLE,
)

tab_logg_teff = dbc.Row([
    dbc.Col(dcc.Graph(id='logg-teff', mathjax=True), md=12)
])

tab_lum_teff = dbc.Row([
    dbc.Col(dcc.Graph(id='L-teff', mathjax=True), md=12)
])

tab_rad_teff = dbc.Row([
    dbc.Col(dcc.Graph(id='R-teff', mathjax=True), md=12)
])

tab_custom_plot = html.Div([
    dbc.Row([
        dbc.Col(dcc.Graph(id='custom_plot', mathjax=True), md=12)
    ]),
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.Label('X-Axis', className='text-center'),
                dbc.Select(
                    id='x_custom_slider',
                    options=[{'label': label, 'value': label} for label in
                             columns],
                    value='Teff',
                ),
                dbc.Switch(
                    id='x_custom_reverse',
                    label='Reverse x-axis',
                    value=False,
                ),
                dbc.RadioItems(
                    options=[
                        {'label': 'Default', 'value': 1},
                        {'label': 'log10(x)', 'value': 2},
                        {'label': 'exp10(x)', 'value': 3},
                    ],
                    value=1,
                    inline=True,
                    id='x_custom_radio',
                    switch=True,
                ),
            ]),
            md=4
        ),
        dbc.Col(
            dbc.Card([
                dbc.Label('Y-Axis', className='text-center'),
                dbc.Select(
                    id='y_custom_slider',
                    options=[{'label': label, 'value': label} for label in
                             columns],
                    value='log_g',
                ),
                dbc.Switch(
                    id='y_custom_reverse',
                    label='Reverse y-axis',
                    value=False,
                ),
                dbc.RadioItems(
                    options=[
                        {'label': 'Default', 'value': 1},
                        {'label': 'log10(y)', 'value': 2},
                        {'label': 'exp10(y)', 'value': 3},
                    ],
                    value=1,
                    inline=True,
                    id='y_custom_radio',
                    switch=True,
                ),
            ]),
            md=4
        ),
    ],
        justify='center'),
])

tab_about = html.P([
    dcc.Markdown(about, mathjax=True)
])

tabs = dbc.Tabs([
    dbc.Tab(tab_logg_teff, label='logg vs. Teff'),
    dbc.Tab(tab_lum_teff, label='L vs. Teff'),
    dbc.Tab(tab_rad_teff, label='R vs. Teff'),
    dbc.Tab(tab_custom_plot, label='Custom plot'),
    dbc.Tab(tab_about, label='About'),
])

layout = html.Div([
    dbc.Row([
        dbc.Col(sidebar, width=3),
        dbc.Col(tabs, width=True),
    ]),
])

app.layout = layout


@app.callback(
    Output('logg-teff', 'figure'),
    Input('submit_button', 'n_clicks'),
    State('dropdown_colors', 'value'),
    State('dropdown_symbols', 'value'),
    State('z_i_slider', 'value'),
    State('m_i_slider', 'value'),
    State('m_env_slider', 'value'),
    State('y_c_slider', 'value'),
    State('target_teff', 'value'),
    State('target_teff_err', 'value'),
    State('target_logg', 'value'),
    State('target_logg_err', 'value'),
    State('select_sigma', 'value'),
    State('colorpicker', 'value'),
    State('dropdown_hover_data', 'value'),
)
def update_logg_teff(n_clicks,
                     colors_value,
                     symbols_value,
                     z_i_slider_value,
                     m_i_slider_value,
                     m_env_slider_value,
                     y_c_slider_value,
                     target_teff,
                     target_teff_err,
                     target_logg,
                     target_logg_err,
                     sigma_range,
                     box_color,
                     hover_data_value):
    dff = df[(df['z_i'] >= min(z_i_slider_value))
             & (df['z_i'] <= max(z_i_slider_value))]
    dff = dff[(dff['m_i'] >= min(m_i_slider_value))
              & (dff['m_i'] <= max(m_i_slider_value))]
    dff = dff[(dff['m_env'] >= min(m_env_slider_value))
              & (dff['m_env'] <= max(m_env_slider_value))]
    dff = dff[(dff['y_c'] >= min(y_c_slider_value))
              & (dff['y_c'] <= max(y_c_slider_value))]

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

    if target_teff and target_teff_err and target_logg and target_logg_err:
        for sigma in range(1, sigma_range + 1):
            fig.add_shape(type='rect',
                          x0=target_teff - sigma * target_teff_err,
                          y0=target_logg - sigma * target_logg_err,
                          x1=target_teff + sigma * target_teff_err,
                          y1=target_logg + sigma * target_logg_err,
                          line={'color': box_color, 'width': 2})

    return fig


@app.callback(
    Output('L-teff', 'figure'),
    Input('submit_button', 'n_clicks'),
    State('dropdown_colors', 'value'),
    State('dropdown_symbols', 'value'),
    State('z_i_slider', 'value'),
    State('m_i_slider', 'value'),
    State('m_env_slider', 'value'),
    State('y_c_slider', 'value'),
    State('target_teff', 'value'),
    State('target_teff_err', 'value'),
    State('target_lum', 'value'),
    State('target_lum_err', 'value'),
    State('select_sigma', 'value'),
    State('colorpicker', 'value'),
    State('dropdown_hover_data', 'value'),
)
def update_lum_teff(n_clicks,
                    colors_value,
                    symbols_value,
                    z_i_slider_value,
                    m_i_slider_value,
                    m_env_slider_value,
                    y_c_slider_value,
                    target_teff,
                    target_teff_err,
                    target_lum,
                    target_lum_err,
                    sigma_range,
                    box_color,
                    hover_data_value):
    dff = df[(df['z_i'] >= min(z_i_slider_value))
             & (df['z_i'] <= max(z_i_slider_value))]
    dff = dff[(dff['m_i'] >= min(m_i_slider_value))
              & (dff['m_i'] <= max(m_i_slider_value))]
    dff = dff[(dff['m_env'] >= min(m_env_slider_value))
              & (dff['m_env'] <= max(m_env_slider_value))]
    dff = dff[(dff['y_c'] >= min(y_c_slider_value))
              & (dff['y_c'] <= max(y_c_slider_value))]

    fig = px.scatter(
        data_frame=dff,
        x='Teff',
        y='L',
        color=colors_value,
        # color_continuous_scale='Inferno',
        symbol=symbols_value,
        hover_data=hover_data_value,
    )
    fig.update_layout(legend_orientation='h')
    fig.update_layout(height=800)
    fig.update_xaxes(autorange='reversed')

    if target_teff and target_teff_err and target_lum and target_lum_err:
        for sigma in range(1, sigma_range + 1):
            fig.add_shape(type='rect',
                          x0=target_teff - sigma * target_teff_err,
                          y0=target_lum - sigma * target_lum_err,
                          x1=target_teff + sigma * target_teff_err,
                          y1=target_lum + sigma * target_lum_err,
                          line={'color': box_color, 'width': 2})

    return fig


@app.callback(
    Output('R-teff', 'figure'),
    Input('submit_button', 'n_clicks'),
    State('dropdown_colors', 'value'),
    State('dropdown_symbols', 'value'),
    State('z_i_slider', 'value'),
    State('m_i_slider', 'value'),
    State('m_env_slider', 'value'),
    State('y_c_slider', 'value'),
    State('target_teff', 'value'),
    State('target_teff_err', 'value'),
    State('target_rad', 'value'),
    State('target_rad_err', 'value'),
    State('select_sigma', 'value'),
    State('colorpicker', 'value'),
    State('dropdown_hover_data', 'value'),
)
def update_radius_teff(n_clicks,
                       colors_value,
                       symbols_value,
                       z_i_slider_value,
                       m_i_slider_value,
                       m_env_slider_value,
                       y_c_slider_value,
                       target_teff,
                       target_teff_err,
                       target_rad,
                       target_rad_err,
                       sigma_range,
                       box_color,
                       hover_data_value):
    dff = df[(df['z_i'] >= min(z_i_slider_value))
             & (df['z_i'] <= max(z_i_slider_value))]
    dff = dff[(dff['m_i'] >= min(m_i_slider_value))
              & (dff['m_i'] <= max(m_i_slider_value))]
    dff = dff[(dff['m_env'] >= min(m_env_slider_value))
              & (dff['m_env'] <= max(m_env_slider_value))]
    dff = dff[(dff['y_c'] >= min(y_c_slider_value))
              & (dff['y_c'] <= max(y_c_slider_value))]

    fig = px.scatter(
        data_frame=dff,
        x='Teff',
        y='radius',
        color=colors_value,
        # color_continuous_scale='Inferno',
        symbol=symbols_value,
        hover_data=hover_data_value,
    )
    fig.update_layout(legend_orientation='h')
    fig.update_layout(height=800)
    fig.update_xaxes(autorange='reversed')

    if target_teff and target_teff_err and target_rad and target_rad_err:
        for sigma in range(1, sigma_range + 1):
            fig.add_shape(type='rect',
                          x0=target_teff - sigma * target_teff_err,
                          y0=target_rad - sigma * target_rad_err,
                          x1=target_teff + sigma * target_teff_err,
                          y1=target_rad + sigma * target_rad_err,
                          line={'color': box_color, 'width': 2})

    return fig


@app.callback(
    Output('custom_plot', 'figure'),
    Input('submit_button', 'n_clicks'),
    State('dropdown_colors', 'value'),
    State('dropdown_symbols', 'value'),
    State('z_i_slider', 'value'),
    State('m_i_slider', 'value'),
    State('m_env_slider', 'value'),
    State('y_c_slider', 'value'),
    State('dropdown_hover_data', 'value'),
    Input('x_custom_slider', 'value'),
    Input('x_custom_reverse', 'value'),
    Input('x_custom_radio', 'value'),
    Input('y_custom_slider', 'value'),
    Input('y_custom_reverse', 'value'),
    Input('y_custom_radio', 'value'),
)
def update_custom_plot(n_clicks,
                       colors_value,
                       symbols_value,
                       z_i_slider_value,
                       m_i_slider_value,
                       m_env_slider_value,
                       y_c_slider_value,
                       hover_data_value,
                       x_name,
                       x_reverse,
                       x_function,
                       y_name,
                       y_reverse,
                       y_function):
    dff = df[(df['z_i'] >= min(z_i_slider_value))
             & (df['z_i'] <= max(z_i_slider_value))]
    dff = dff[(dff['m_i'] >= min(m_i_slider_value))
              & (dff['m_i'] <= max(m_i_slider_value))]
    dff = dff[(dff['m_env'] >= min(m_env_slider_value))
              & (dff['m_env'] <= max(m_env_slider_value))]
    dff = dff[(dff['y_c'] >= min(y_c_slider_value))
              & (dff['y_c'] <= max(y_c_slider_value))]

    if x_function == 2:
        dff[x_name] = np.log10(dff[x_name])
    elif x_function == 3:
        dff[x_name] = 10.0 ** dff[x_name]

    if y_function == 2:
        dff[y_name] = np.log10(dff[y_name])
    elif y_function == 3:
        dff[y_name] = 10.0 ** dff[y_name]

    fig = px.scatter(
        data_frame=dff,
        x=x_name,
        y=y_name,
        color=colors_value,
        # color_continuous_scale='Inferno',
        symbol=symbols_value,
        hover_data=hover_data_value,
    )
    fig.update_layout(legend_orientation='h')
    fig.update_layout(height=800)
    fig.update_xaxes(
        autorange='reversed' if x_reverse else True)
    fig.update_yaxes(
        autorange='reversed' if y_reverse else True)

    return fig


if __name__ == '__main__':
    app.run_server(port=8085, debug=True)
