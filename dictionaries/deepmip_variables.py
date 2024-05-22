#################################################################################
# DeepMIP output variables following the CMIP6 data request
#################################################################################

#### Atmosphere variables

variable_dict = dict()

variable_dict["tas"] = {
    "longname": "Near-surface air temperature",
    "label": "temperature",
    "unit": "K",
    "dimensions": 3,
    "realm": "atmos",
}

variable_dict["pr"] = {
    "longname": "Precipitation",
    "label": "precipitation",
    "unit": "kgm^{-2}s^{-1}",
    "dimensions": 3,
    "realm": "atmos",
}

variable_dict["ts"] = {
    "longname": "Surface skin temperature",
    "unit": "K",
    "dimensions": 3,
    "realm": "atmos",
}

variable_dict["evspsbl"] = {
    "longname": "Total evaporation",
    "unit": "kgm^{-2}s^{-1}",
    "dimensions": 3,
    "realm": "atmos",
}

variable_dict["clt"] = {
    "longname": "Total cloud cover fraction",
    "unit": "[0,1]",
    "dimensions": 3,
    "realm": "atmos",
}

variable_dict["rlds"] = {
    "longname": "Surface downwelling longwave radiation",
    "unit": "Wm^{-2}",
    "dimensions": 3,
    "realm": "atmos",
}

variable_dict["rlus"] = {
    "longname": "Surface upwelling longwave radiation",
    "unit": "Wm^{-2}",
    "dimensions": 3,
    "realm": "atmos",
}

variable_dict["rsds"] = {
    "longname": "Surface downwelling shortwave radiation",
    "unit": "Wm^{-2}",
    "dimensions": 3,
    "realm": "atmos",
}

variable_dict["rsus"] = {
    "longname": "Surface upwelling shortwave radiation",
    "unit": "Wm^{-2}",
    "dimensions": 3,
    "realm": "atmos",
}

variable_dict["rsdt"] = {
    "longname": "TOA incident shortwave radiation",
    "unit": "Wm^{-2}",
    "dimensions": 3,
    "realm": "atmos",
}

variable_dict["rsut"] = {
    "longname": "TOA outgoing shortwave radiation",
    "unit": "Wm^{-2}",
    "dimensions": 3,
    "realm": "atmos",
}

variable_dict["rlut"] = {
    "longname": "TOA outgoing longwave radiation",
    "unit": "Wm^{-2}",
    "dimensions": 3,
    "realm": "atmos",
}

variable_dict["rldscs"] = {
    "longname": "Surface downwelling longwave radiation (clear sky)",
    "unit": "Wm^{-2}",
    "dimensions": 3,
    "realm": "atmos",
}

variable_dict["rsdscs"] = {
    "longname": "Surface downwelling shortwave radiation (clear sky)",
    "unit": "Wm^{-2}",
    "dimensions": 3,
    "realm": "atmos",
}

variable_dict["rsuscs"] = {
    "longname": "Surface upwelling shortwave radiation (clear sky)",
    "unit": "Wm^{-2}",
    "dimensions": 3,
    "realm": "atmos",
}

variable_dict["rsutcs"] = {
    "longname": "TOA outgoing shortwave radiation (clear sky)",
    "unit": "Wm^{-2}",
    "dimensions": 3,
    "realm": "atmos",
}

variable_dict["rlutcs"] = {
    "longname": "TOA outgoing longwave radiation (clear sky)",
    "unit": "Wm^{-2}",
    "dimensions": 3,
    "realm": "atmos",
}

variable_dict["hfss"] = {
    "longname": "Sensible heat flux (upward)",
    "unit": "Wm^{-2}",
    "dimensions": 3,
    "realm": "atmos",
}

variable_dict["hfls"] = {
    "longname": "Latent heat flux (upward)",
    "unit": "Wm^{-2}",
    "dimensions": 3,
    "realm": "atmos",
}

variable_dict["uas"] = {
    "longname": "Near-surface eastward wind",
    "unit": "ms^{-1}",
    "dimensions": 3,
    "realm": "atmos",
}

variable_dict["vas"] = {
    "longname": "Near-surface northward wind",
    "unit": "ms^{-1}",
    "dimensions": 3,
    "realm": "atmos",
}

variable_dict["uas"] = {
    "longname": "Near-surface eastward wind",
    "unit": "ms^{-1}",
    "dimensions": 3,
    "realm": "atmos",
}

variable_dict["tauu"] = {
    "longname": "Surface eastward wind stress",
    "unit": "Nm^{-2}",
    "dimensions": 3,
    "realm": "atmos",
}

variable_dict["tauv"] = {
    "longname": "Surface northward wind stress",
    "unit": "Nm^{-2}",
    "dimensions": 3,
    "realm": "atmos",
}

variable_dict["psl"] = {
    "longname": "Mean sea level pressure",
    "unit": "Pa",
    "dimensions": 3,
    "realm": "atmos",
}

variable_dict["ps"] = {
    "longname": "Surface pressure",
    "unit": "Pa",
    "dimensions": 3,
    "realm": "atmos",
}

variable_dict["ua"] = {
    "longname": "Eastward wind on model levels",
    "unit": "ms^{-1}",
    "dimensions": 4,
    "realm": "atmos",
}

variable_dict["va"] = {
    "longname": "Northward wind on model levels",
    "unit": "ms^{-1}",
    "dimensions": 4,
    "realm": "atmos",
}

variable_dict["wa"] = {
    "longname": "Vertical wind on model levels",
    "unit": "ms^{-1}",
    "dimensions": 4,
    "realm": "atmos",
}

variable_dict["uap"] = {
    "longname": "Eastward wind on pressure levels",
    "unit": "ms^{-1}",
    "dimensions": 4,
    "realm": "atmos",
}

variable_dict["vap"] = {
    "longname": "Northward wind on pressure levels",
    "unit": "ms^{-1}",
    "dimensions": 4,
    "realm": "atmos",
}

variable_dict["wap"] = {
    "longname": "Vertical wind on pressure levels",
    "unit": "Pas^{-1}",
    "dimensions": 4,
    "realm": "atmos",
}

variable_dict["zg"] = {
    "longname": "Geopotential height on pressure levels",
    "unit": "m",
    "dimensions": 4,
    "realm": "atmos",
}

variable_dict["ta"] = {
    "longname": "Temperature on pressure levels",
    "unit": "K",
    "dimensions": 4,
    "realm": "atmos",
}

variable_dict["hus"] = {
    "longname": "Specific humidity on pressure levels",
    "unit": "kgkg^{-1}",
    "dimensions": 4,
    "realm": "atmos",
}

variable_dict["cl"] = {
    "longname": "Cloud fraction on pressure levels",
    "unit": "[0,1]",
    "dimensions": 4,
    "realm": "atmos",
}

variable_dict["cll"] = {
    "longname": "Low-level cloud fraction",
    "unit": "[0,1]",
    "dimensions": 3,
    "realm": "atmos",
}

variable_dict["clm"] = {
    "longname": "Medium-level cloud fraction",
    "unit": "[0,1]",
    "dimensions": 3,
    "realm": "atmos",
}

variable_dict["clh"] = {
    "longname": "High-level cloud fraction",
    "unit": "[0,1]",
    "dimensions": 3,
    "realm": "atmos",
}

#### Ocean variables

variable_dict["tos"] = {
    "longname": "Sea surface temperature",
    "label": "temperature",
    "unit": "°C",
    "dimensions": 3,
    "realm": "ocean",
}

variable_dict["siconc"] = {
    "longname": "Sea-ice fraction",
    "unit": "[0,1]",
    "dimensions": 3,
    "realm": "ocean",
}

variable_dict["uo"] = {
    "longname": "Eastward velocity on model levels",
    "unit": "cms^{-1}",
    "dimensions": 4,
    "realm": "ocean",
}

variable_dict["vo"] = {
    "longname": "Northward velocity on model levels",
    "unit": "cms^{-1}",
    "dimensions": 4,
    "realm": "ocean",
}

variable_dict["wo"] = {
    "longname": "Vertical velocity on model levels",
    "unit": "cms^{-1}",
    "dimensions": 4,
    "realm": "ocean",
}

variable_dict["thetao"] = {
    "longname": "Potential temperature on model levels",
    "unit": "°C",
    "dimensions": 4,
    "realm": "ocean",
}

variable_dict["so"] = {
    "longname": "Salinity on model levels",
    "unit": "psu",
    "dimensions": 4,
    "realm": "ocean",
}

variable_dict["mlotst"] = {
    "longname": "Mixed-layer depth",
    "unit": "m",
    "dimensions": 3,
    "realm": "ocean",
}

variable_dict["zos"] = {
    "longname": "Sea surface height",
    "unit": "m",
    "dimensions": 3,
    "realm": "ocean",
}

variable_dict["tauuo"] = {
    "longname": "Surface eastward wind stress (on ocean grid)",
    "unit": "Nm^{-2}",
    "dimensions": 3,
    "realm": "ocean",
}

variable_dict["tauvo"] = {
    "longname": "Surface northward wind stress (on ocean grid)",
    "unit": "Nm^{-2}",
    "dimensions": 3,
    "realm": "ocean",
}

variable_dict["hfno"] = {
    "longname": "Net surface heat flux (on ocean grid)",
    "unit": "Wm^{-2}",
    "dimensions": 3,
    "realm": "ocean",
}

variable_dict["wfno"] = {
    "longname": "Net surface freshwater flux (on ocean grid)",
    "unit": "kgm^{-2}s^{-1}",
    "dimensions": 3,
    "realm": "ocean",
}

variable_dict["difvto"] = {
    "longname": "Vertical ocean tracer diffusivity",
    "unit": "m^{-2}s^{-1}",
    "dimensions": 4,
    "realm": "ocean",
}

variable_dict["difvmo"] = {
    "longname": "Vertical ocean momentum diffusivity",
    "unit": "m^{-2}s^{-1}",
    "dimensions": 4,
    "realm": "ocean",
}

variable_dict["sftbarot"] = {
    "longname": "Barotropic streamfunction",
    "unit": "Sv",
    "dimensions": 3,
    "realm": "ocean",
}

variable_dict["sftmyz"] = {
    "longname": "Global overturning streamfunction",
    "unit": "Sv",
    "dimensions": 3,
    "realm": "ocean",
}

#### Boundary conditions

variable_dict["sftlf"] = {
    "longname": "Land-sea mask (on atmospheric grid)",
    "unit": "[0,1]",
    "dimensions": 2,
    "realm": "atmos",
}

variable_dict["orog"] = {
    "longname": "Topography (on atmospheric grid)",
    "unit": "[0,1]",
    "dimensions": 2,
    "realm": "atmos",
}

variable_dict["deptho"] = {
    "longname": "Bathymetry (on ocean grid)",
    "unit": "[0,1]",
    "dimensions": 2,
    "realm": "ocean",
}