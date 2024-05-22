#################################################################################
# DeepMIP models participating in the Eocene phase 1 simulations
#################################################################################

model_dict = dict()

model_dict["CESM1.2-CAM5"] = {
    "versn": "v1.0",
    "group": "CESM",
    "abbrv": "CESM",
    "exps": [
        "deepmip-eocene-p1-PI",
        "deepmip-eocene-p1-x1",
        "deepmip-eocene-p1-x3",
        "deepmip-eocene-p1-x6",
        "deepmip-eocene-p1-x9",
    ],
    "gmst": [13.2, 18.4, 25.0, 29.8, 35.5],
    "rotation": "H14",
    "CMIP generation": "CMIP5",
}

model_dict["COSMOS-landveg-r2413"] = {
    "versn": "v1.0",
    "group": "COSMOS",
    "abbrv": "COSMOS",
    "exps": [
        "deepmip-eocene-p1-PI",
        "deepmip-eocene-p1-x1",
        "deepmip-eocene-p1-x3",
        "deepmip-eocene-p1-x4",
    ],
    "gmst": [13.9, 17.0, 25.2, 26.9],
    "rotation": "H14",
    "CMIP generation": "CMIP3",
}

model_dict["GFDL-CM2.1"] = {
    "versn": "v1.0",
    "group": "GFDL",
    "abbrv": "GFDL",
    "exps": [
        "deepmip-eocene-p1-PI",
        "deepmip-eocene-p1-x1",
        "deepmip-eocene-p1-x2",
        "deepmip-eocene-p1-x3",
        "deepmip-eocene-p1-x4",
        "deepmip-eocene-p1-x6",
    ],
    "gmst": [15.6, 19.2, 22.9, 25.4, 27.5, 30.2],
    "rotation": "H14",
    "CMIP generation": "CMIP3",
}

model_dict["HadCM3B-M2.1aN"] = {
    "versn": "v1.0",
    "group": "HadCM3",
    "abbrv": "HadCM3",
    "exps": [
        "deepmip-eocene-p1-PI",
        "deepmip-eocene-p1-x1",
        "deepmip-eocene-p1-x2",
        "deepmip-eocene-p1-x3",
    ],
    "gmst": [13.9, 17.4, 21.2, 25.0],
    "rotation": "H14",
    "CMIP generation": "CMIP3",
}

model_dict["HadCM3BL-M2.1aN"] = {
    "versn": "v1.0",
    "group": "HadCM3",
    "abbrv": "HadCM3L",
    "exps": [
        "deepmip-eocene-p1-PI",
        "deepmip-eocene-p1-x1",
        "deepmip-eocene-p1-x2",
        "deepmip-eocene-p1-x3",
    ],
    "gmst": [13.2, 16.9, 21.1, 26.0],
    "rotation": "H14",
    "CMIP generation": "CMIP3",
}

model_dict["INM-CM4-8"] = {
    "versn": "v1.0",
    "group": "INMCM",
    "abbrv": "INM",
    "exps": ["deepmip-eocene-p1-PI", "deepmip-eocene-p1-x6"],
    "gmst": [13.2, 23.4],
    "rotation": "H14",
    "CMIP generation": "CMIP6",
}

model_dict["IPSLCM5A2"] = {
    "versn": "v1.0",
    "group": "IPSL",
    "abbrv": "IPSL",
    "exps": ["deepmip-eocene-p1-PI", "deepmip-eocene-p1-x1.5", "deepmip-eocene-p1-x3"],
    "gmst": [13.2, 19.4, 25.0],
    "rotation": "H14",
    "CMIP generation": "CMIP5",
}

model_dict["MIROC4m"] = {
    "versn": "v1.0",
    "group": "MIROC",
    "abbrv": "MIROC",
    "exps": [
        "deepmip-eocene-p1-PI",
        "deepmip-eocene-p1-x1",
        "deepmip-eocene-p1-x2",
        "deepmip-eocene-p1-x3",
    ],
    "gmst": [12.9, 16.6, 20.4, 23.5],
    "rotation": "H14",
    "CMIP generation": "CMIP3",
}

model_dict["NorESM1-F"] = {
    "versn": "v1.0",
    "group": "NorESM",
    "abbrv": "NorESM",
    "exps": ["deepmip-eocene-p1-PI", "deepmip-eocene-p1-x2", "deepmip-eocene-p1-x4"],
    "gmst": [14.5, 21.2, 24.1],
    "rotation": "B16",
    "CMIP generation": "CMIP5-6",
}