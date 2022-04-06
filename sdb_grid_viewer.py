import dash
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.express as px
from dash import dcc, html, Input, Output, State
from sqlalchemy import create_engine

# -----------------------------------------------------------------------------
# Custom styles

# the style arguments for the sidebar.
SIDEBAR_STYLE = {
    # 'position': 'fixed',
    # 'top': 0,
    # 'left': 0,
    # 'bottom': 0,
    # 'width': '20%',
    # 'padding': '20px 10px',
    'overflow': 'scroll'
}

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}])

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

controls = dbc.Container(
    [
        dbc.Card([
            dbc.Label('Select color:'),
            dbc.Select(
                id='dropdown_colors',
                options=[
                    {'label': 'z_i', 'value': 'z_i'},
                    {'label': 'm_i', 'value': 'm_i'},
                    {'label': 'm_env', 'value': 'm_env'},
                    {'label': 'center_he4', 'value': 'y_c'},
                ],
                value='m_i',
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
                value='z_i',
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
    dcc.Markdown('''
        _sdB Grid Viever_ is the tool to quickly inspect the grid of evolutionary
        models of sdB stars calculated for
        the [ARDASTELLA](https://ardastella.up.krakow.pl/) research group.
        
        ## Overview of the grid
        
        ***
        The models were calculated using the set-up described
        by [Ostrowski et al. (2021)](https://ui.adsabs.harvard.edu/abs/2021MNRAS.503.4646O/abstract)
        , utilizing the computational resources provided
        by [Wrocław Centre for Networking and Supercomputing](https://www.wcss.pl/en/).
        Evolutionary models were calculated using the
        [MESA](https://github.com/MESAHub/mesa) code
        ([Paxton et al. 2011](https://ui.adsabs.harvard.edu/abs/2011ApJS..192....3P/abstract)
        ,
        [2013](https://ui.adsabs.harvard.edu/abs/2013ApJS..208....4P/abstract),
        [2015](https://ui.adsabs.harvard.edu/abs/2015ApJS..220...15P/abstract),
        [2018](https://ui.adsabs.harvard.edu/abs/2018ApJS..234...34P/abstract),
        [2019](https://ui.adsabs.harvard.edu/abs/2019ApJS..243...10P/abstract)),
        version 11701, and supplemented by adiabatic non-radial pulsational models
        calculated using the [GYRE](https://github.com/rhdtownsend/gyre) code
        ([Townsend & Teitler 2013](https://ui.adsabs.harvard.edu/abs/2013MNRAS.435.3406T/abstract)
        ,
        [Townsend et al. 2018](https://ui.adsabs.harvard.edu/abs/2018MNRAS.475..879T/abstract)
        ,
        [Goldstein & Townsend 2020](https://ui.adsabs.harvard.edu/abs/2020ApJ...899..116G/abstract))
        , version 5.2.
        
        The models were calculated for progenitors with initial masses, Mi, in the
        range of 1.0 − 1.8 Ms, with a step of 0.005 Ms, and metallicities, Z, in the
        range of 0.005 − 0.035, with a step of 0.005. The considered envelope masses,
        Menv, are in the range of 0.0001 − 0.0030 Ms, with a step of 0.0001 Ms, and
        0.003 − 0.010 Ms, with a step of 0.001 Ms. Central helium abundance, Yc, is in
        the range of 0.9 − 0.1, with a step of 0.05.
        
        The full grid is not publicly available at the moment.
        
        ## Available data
        
        ***
        The selection of columns available in _sdB Grid Viewer_:
        
        * **id** - id of a model
        * **m_i** - initial mass of a progenitor (solar units)
        * **m_env** - envelope mass of an sdb model (solar units)
        * **z_i** - initial metallicity of a progenitor
        * **y_i** - initial helium abundance of a progenitor
        * **m_he_core** - mass of a helium core of progenitor before removal of the
          envelope
        * **log_g** - logarithm of surface gravity of a model (cgs)
        * **radius** - radius of a model (solar units)
        * **age** - total age of a model calculated from the beginning of the PMS
          evolution (years)
        * **z_surf** - surface metallicity of a model
        * **y_surf** - surface helium abundance of a model
        * **center_he4** - exact central helium abundance of a model
        * **y_c** - central helium abundance of a model rounded to two decimal points
        * **Teff** - effective temperature of a model
        * **L** - luminosity of a model (solar units)
        
        ## Usage
        
        ***
        
        ### Settings
        
        Options in the menu:
        
        * **Select color** - select a parameter shown by color. Options: z_i, m_i,
          m_env, center_he4.
        * **Select symbols** - select a parameter shown by symbols. Options: z_i, m_i,
          m_env, center_he4.
        * **Z_i** - initial metallicity of progenitors
        * **M_i** - initial mass of progenitors in solar units
        * **M_env** - envelope mass of sdB models in solar units
        * **Y_c** - central helium abundance of sdB models
        * **Hover data** - select parameters shown for data points in the hover menu
        
        ### Available plots
        
        There are three predefined plots available: **logg vs. Teff**, **L vs. Teff**,
        and **R vs. Teff**, and also a **custom plot** that can be customized to show
        any grid columns accessible by _sdB Grid Viever_. The custom plot also allows
        user to reverse axes and apply to them the base-10 logarithmic or exponential
        function.
    ''')
])

tabs = dbc.Tabs(
    [
        dbc.Tab(tab_logg_teff, label='logg vs. Teff'),
        dbc.Tab(tab_lum_teff, label='L vs. Teff'),
        dbc.Tab(tab_rad_teff, label='R vs. Teff'),
        dbc.Tab(tab_custom_plot, label='Custom plot'),
        dbc.Tab(tab_about, label='About'),
    ]
)

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
    State('dropdown_hover_data', 'value'),
)
def update_lum_teff(n_clicks,
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
    State('dropdown_hover_data', 'value'),
)
def update_radius_teff(n_clicks,
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
