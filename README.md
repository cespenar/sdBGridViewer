# sdB Grid Viewer

_sdB Grid Viever_ is the tool to quickly inspect the grid of evolutionary
models of sdB stars calculated for
the [ARDASTELLA](https://ardastella.up.krakow.pl/) research group.

## Overview of the grid

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
