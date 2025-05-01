Quick-start
===========

This tutorial shows how to

1. Read a 30-minute *TOA5* file.
2. Compute the energy-balance closure ratio.
3. Flag candidate periods of horizontal / vertical advection.
4. Compute advection fluxes needed to close the balance.

Prerequisites
-------------

.. code-block:: bash

   pip install pandas matplotlib numpy

Step 1 – Load the data
----------------------

.. code-block:: python
    
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd

    df = (
        pd.read_csv("EC_2024.CSV", skiprows=4,  # TOA5 header
                    parse_dates=["TIMESTAMP"], index_col="TIMESTAMP")
        .rename(columns={"Rn": "Rn", "G": "G", "H": "H", "LE": "LE"})
    )

Step 2 – Calculate closure metrics
--------------------------------------

.. code-block:: python

    # Compute energy balance closure ratio
    df["AE"]            = df["Rn"] - df["G"]
    df["Flux_sum"]      = df["H"]  + df["LE"]
    df["closure_ratio"] = df["Flux_sum"] / df["AE"]

Step 3 – Flag advection
---------------------------


.. code-block:: python

    from advection import advect_detect
    flags_h = advect_detect.detect_horizontal_advection(
        main_flux   = df["H"],
        le_main     = df["LE"],
        rn          = df["Rn"],
        g           = df["G"],
    )
    flags_v = advect_detect.detect_vertical_advection(
        main_H = df["H"],
        rn     = df["Rn"],
        g      = df["G"],
    )
    df["adv_h"] = flags_h
    df["adv_v"] = flags_v

Step 4 – Compute & apply flux corrections
-----------------------------------------------

.. code-block:: python
    
    from advection import advection

    out = advection.compute_advection_fluxes(
        main_data = df[["H", "LE", "Rn", "G"]].to_dict("list"),
        detect_horizontal = flags_h,
        detect_vertical   = flags_v,
    )

    corrected = advection.apply_advection_correction(
        main_data = df[["H", "LE", "Rn", "G"]].to_dict("list"),
        H_adv = out["H_adv"], V_adv = out["V_adv"],
    )

---


Energy-balance closure & advection
==================================

Why closure matters
-------------------

Eddy-covariance towers routinely **under-sum the available
energy**—the measured sensible (H) plus latent (LE) heat flux is
typically 10–20 % lower than :math:`R_n - G`.  Recent field campaigns
(BEAREX, EBEX-2000, ADVEX, Wang *et al.* 2024) demonstrate that

* **Horizontal advection** of warm/dry air over irrigated fields can
  enhance ET so that *λE* exceeds the available energy.
* **Vertical advection / storage** during stable nights can transport
  heat downward, driving negative H.

Accurately *flagging* and *quantifying* these terms greatly improves
closure—from ~0.88 to ≥ 0.97 in Wang 2024, for example.

Detection strategy implemented
------------------------------

The :pymod:`advection.advect_detect`
module applies four empirically proven criteria :contentReference[oaicite:0]{index=0}&#8203;:contentReference[oaicite:1]{index=1}:

1. **Up-/down-wind flux divergence** (requires a reference tower).
2. **LE > AE** by >5 %.
3. Daytime negative H.
4. Temperature / humidity gradients.

Vertical advection uses canopy inversions plus mean subsidence tests.

Flux computation
----------------

:pyfunc:`advection.advection.compute_advection_fluxes`
allocates the residual energy to

* *H\_adv* – horizontal component,
* *V\_adv* – vertical component,

by matching wind direction to the relevant upwind tower if supplied :contentReference[oaicite:2]{index=2}&#8203;:contentReference[oaicite:3]{index=3}.

For rigorous background, consult Prueger 2012, Dhungel 2022,
Moderow 2021, and Wang 2024 (see *References* section of the API docs).

advection.advect_detect
==================================

.. automodule:: advection.advect_detect
   :members:
   :undoc-members:
   :show-inheritance:

advection.advection
==============================

.. automodule:: advection.advection
   :members:
   :undoc-members:
   :show-inheritance:
