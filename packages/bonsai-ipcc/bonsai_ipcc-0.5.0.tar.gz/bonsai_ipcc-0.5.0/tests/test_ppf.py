import os
from pathlib import Path

import numpy as np
import pandas as pd

from bonsai_ipcc import PPF

ROOT_PATH = Path(os.path.dirname(__file__)).parent


def test_coke_tier1():
    test = PPF()
    df = pd.DataFrame(
        data={
            "year": [2015, 2015, 2015, 2015, 2015],
            "region": ["PL", "PL", "PL", "PL", "PL"],
            "property": ["def", "min", "max", "abs_min", "abs_max"],
            "value": [10, 8, 12, 0, np.inf],
            "unit": ["t/yr", "t/yr", "t/yr", "t/yr", "t/yr"],
        }
    ).set_index(["year", "region", "property"])

    test.ppf_vol.metal.parameter.coke = df

    df = test.ppf_vol.metal.parameter.product_transf_coeff_coke.copy()
    # Replace 'World' with 'PL' in the 'region' level of the MultiIndex
    df.index = df.index.set_levels(
        df.index.levels[df.index.names.index("region")].map(
            lambda x: "PL" if x == "World" else x
        ),
        level="region",
    )
    test.ppf_vol.metal.parameter.product_transf_coeff_coke = df.copy()

    df = test.ppf_vol.metal.parameter.emission_transf_coeff_coke.copy()
    # Replace 'World' with 'PL' in the 'region' level of the MultiIndex
    df.index = df.index.set_levels(
        df.index.levels[df.index.names.index("region")].map(
            lambda x: "PL" if x == "World" else x
        ),
        level="region",
    )
    test.ppf_vol.metal.parameter.emission_transf_coeff_coke = df.copy()

    s = test.ppf_vol.metal.sequence.coke_tier1(
        year=2015,
        region="PL",
        activity="by-product_recovery",
        uncertainty="monte_carlo",
    )
    dfs = s.to_frames(
        bonsai=True,
        # external_metadata=ppf.ppf._metadata.external_metadata,
        # external_functions=ppf.ppf._metadata.external_functions,
    )
    assert isinstance(dfs["bonsai"]["use"], pd.DataFrame) == True


def test_coke_tier1_sample():
    test = PPF()
    df = pd.DataFrame(
        data={
            "year": [2013],
            "region": ["DE"],
            "property": ["sample"],
            "value": [np.array([10, 8, 12])],
            "unit": ["t/yr"],
        }
    ).set_index(["year", "region", "property"])
    test.ppf_vol.metal.parameter.coke = df

    df = pd.DataFrame(
        data={
            "year": [2013, 2013],
            "region": ["World", "World"],
            "activity": ["by-product_recovery", "no_by-product_recovery"],
            "property": ["sample", "sample"],
            "value": [np.array([0.2, 0.7, 0.5]), np.array([0.8, 0.3, 0.5])],
            "unit": ["t/t", "t/t"],
        }
    ).set_index(["year", "region", "activity", "property"])
    test.ppf_vol.metal.parameter.coke_activity_per_reg = df

    df = pd.DataFrame(
        data={
            "year": [2013, 2013],
            "region": ["DE", "DE"],
            "activity": ["by-product_recovery", "by-product_recovery"],
            "product": ["natural_gas", "electricity"],
            "property": ["sample", "sample"],
            "value": [np.array([0.5, 0.45, 0.55]), np.array([3.5, 3.45, 3.55])],
            "unit": ["GJ/t", "GJ/t"],
        }
    ).set_index(["year", "region", "activity", "product", "property"])
    test.ppf_vol.metal.parameter.energy_use_per_coke = df

    df = pd.DataFrame(
        data={
            "year": [2013, 2013, 2013, 2013],
            "region": ["DE", "DE", "DE", "DE"],
            "activity": [
                "by-product_recovery",
                "no_by-product_recovery",
                "by-product_recovery",
                "no_by-product_recovery",
            ],
            "emission": ["CO2", "CO2", "CH4", "CH4"],
            "property": ["sample", "sample", "sample", "sample"],
            "value": [
                np.array([0.51, 0.48, 0.52]),
                np.array([1.21, 1.48, 1.12]),
                np.array([0.0051, 0.0048, 0.0052]),
                np.array([0.021, 0.048, 0.012]),
            ],
            "unit": ["t/t", "t/t", "t/t", "t/t"],
        }
    ).set_index(["year", "region", "activity", "emission", "property"])
    test.ppf_vol.metal.parameter.emission_per_coke = df

    df = pd.DataFrame(
        data={
            "year": [2013],
            "region": [
                "EUR",
            ],
            "activity": ["by-product_recovery"],
            "property": ["sample"],
            "value": [np.array([1.24, 1.27, 1.23])],
            "unit": ["t/t"],
        }
    ).set_index(["year", "region", "activity", "property"])
    test.ppf_vol.metal.parameter.coal_use_per_coke = df

    df = pd.DataFrame(
        data={
            "year": [2013, 2013],
            "region": ["DE", "DE"],
            "activity": ["by-product_recovery", "no_by-product_recovery"],
            "product": ["coking_coal", "coking_coal"],
            "reference_output": ["cog", "cog"],
            "property": ["sample", "sample"],
            "value": [np.array([0.9, 0.9, 0.9]), np.array([0.0, 0.0, 0.0])],
            "unit": ["t/t", "t/t"],
        }
    ).set_index(
        [
            "year",
            "region",
            "activity",
            "product",
            "reference_output",
            "property",
        ]
    )
    test.ppf_vol.metal.parameter.product_transf_coeff_coke = df

    df = pd.DataFrame(
        data={
            "year": [2013, 2013],
            "region": ["DE", "DE"],
            "activity": ["by-product_recovery", "no_by-product_recovery"],
            "product": ["coking_coal", "coking_coal"],
            "reference_output": ["CO2", "CO2"],
            "property": ["sample", "sample"],
            "value": [np.array([0.1, 0.1, 0.1]), np.array([1.0, 1.0, 1.0])],
            "unit": ["t/t", "t/t"],
        }
    ).set_index(
        [
            "year",
            "region",
            "activity",
            "product",
            "reference_output",
            "property",
        ]
    )
    test.ppf_vol.metal.parameter.emission_transf_coeff_coke = df

    df = pd.DataFrame(
        data={
            "year": [2013, 2013],
            "region": ["DE", "DE"],
            "activity": ["by-product_recovery", "no_by-product_recovery"],
            "product": ["coke_oven_gas", "coke_oven_gas"],
            "property": ["sample", "sample"],
            "value": [np.array([0.0, 0.0, 0.0]), np.array([0.2, 0.3, 0.25])],
            "unit": ["m3/t", "m3/t"],
        }
    ).set_index(["year", "region", "activity", "product", "property"])
    test.ppf_vol.metal.parameter.byproduct_supply_per_coke = df

    df = pd.DataFrame(
        data={
            "year": [2013, 2013],
            "region": ["DE", "DE"],
            "activity": ["by-product_recovery", "by-product_recovery"],
            "product": ["water", "nitrogen"],
            "property": ["sample", "sample"],
            "value": [np.array([0.0, 0.0, 0.0]), np.array([0.2, 0.3, 0.25])],
            "unit": ["m3/t", "m3/t"],
        }
    ).set_index(["year", "region", "activity", "product", "property"])
    test.ppf_vol.metal.parameter.feedstock_use_per_coke = df

    s = test.ppf_vol.metal.sequence.coke_tier1(
        year=2013,
        region="DE",
        activity="by-product_recovery",
        uncertainty="sample",
    )

    dfs = s.to_frames(
        bonsai=True,
        # external_metadata=ppf.ppf._metadata.external_metadata,
        # external_functions=ppf.ppf._metadata.external_functions,
    )
    assert isinstance(dfs["bonsai"]["use"], pd.DataFrame) == True
    assert dfs["bonsai"]["transf_coeff"].empty == False


def test_coke_tier1_sample_samples():
    test = PPF()
    df = pd.DataFrame(
        data={
            "year": [2013],
            "region": ["DE"],
            "property": ["sample"],
            "value": [np.array([10, 8, 12])],
            "unit": ["t/yr"],
        }
    ).set_index(["year", "region", "property"])
    test.ppf_vol.metal.parameter.coke = df

    df = pd.DataFrame(
        data={
            "year": [2013, 2013],
            "region": ["World", "World"],
            "activity": ["by-product_recovery", "no_by-product_recovery"],
            "property": ["sample", "sample"],
            "value": [np.array([0.2, 0.7, 0.5]), np.array([0.8, 0.3, 0.5])],
            "unit": ["t/t", "t/t"],
        }
    ).set_index(["year", "region", "activity", "property"])
    test.ppf_vol.metal.parameter.coke_activity_per_reg = df

    df = pd.DataFrame(
        data={
            "year": [2013, 2013],
            "region": ["DE", "DE"],
            "activity": ["by-product_recovery", "by-product_recovery"],
            "product": ["natural_gas", "electricity"],
            "property": ["sample", "sample"],
            "value": [np.array([0.5, 0.45, 0.55]), np.array([3.5, 3.45, 3.55])],
            "unit": ["GJ/t", "GJ/t"],
        }
    ).set_index(["year", "region", "activity", "product", "property"])
    test.ppf_vol.metal.parameter.energy_use_per_coke = df

    df = pd.DataFrame(
        data={
            "year": [2013, 2013, 2013, 2013],
            "region": ["DE", "DE", "DE", "DE"],
            "activity": [
                "by-product_recovery",
                "no_by-product_recovery",
                "by-product_recovery",
                "no_by-product_recovery",
            ],
            "emission": ["CO2", "CO2", "CH4", "CH4"],
            "property": ["sample", "sample", "sample", "sample"],
            "value": [
                np.array([0.51, 0.48, 0.52]),
                np.array([1.21, 1.48, 1.12]),
                np.array([0.0051, 0.0048, 0.0052]),
                np.array([0.021, 0.048, 0.012]),
            ],
            "unit": ["t/t", "t/t", "t/t", "t/t"],
        }
    ).set_index(["year", "region", "activity", "emission", "property"])
    test.ppf_vol.metal.parameter.emission_per_coke = df

    df = pd.DataFrame(
        data={
            "year": [2013],
            "region": [
                "EUR",
            ],
            "activity": ["by-product_recovery"],
            "property": ["sample"],
            "value": [np.array([1.24, 1.27, 1.23])],
            "unit": ["t/t"],
        }
    ).set_index(["year", "region", "activity", "property"])
    test.ppf_vol.metal.parameter.coal_use_per_coke = df

    df = pd.DataFrame(
        data={
            "year": [2013, 2013],
            "region": ["DE", "DE"],
            "activity": ["by-product_recovery", "no_by-product_recovery"],
            "product": ["coking_coal", "coking_coal"],
            "reference_output": ["cog", "cog"],
            "property": ["sample", "sample"],
            "value": [np.array([0.9, 0.9, 0.9]), np.array([0.0, 0.0, 0.0])],
            "unit": ["t/t", "t/t"],
        }
    ).set_index(
        [
            "year",
            "region",
            "activity",
            "product",
            "reference_output",
            "property",
        ]
    )
    test.ppf_vol.metal.parameter.product_transf_coeff_coke = df

    df = pd.DataFrame(
        data={
            "year": [2013, 2013],
            "region": ["DE", "DE"],
            "activity": ["by-product_recovery", "no_by-product_recovery"],
            "product": ["coking_coal", "coking_coal"],
            "reference_output": ["CO2", "CO2"],
            "property": ["sample", "sample"],
            "value": [np.array([0.1, 0.1, 0.1]), np.array([1.0, 1.0, 1.0])],
            "unit": ["t/t", "t/t"],
        }
    ).set_index(
        [
            "year",
            "region",
            "activity",
            "product",
            "reference_output",
            "property",
        ]
    )
    test.ppf_vol.metal.parameter.emission_transf_coeff_coke = df

    df = pd.DataFrame(
        data={
            "year": [2013, 2013],
            "region": ["DE", "DE"],
            "activity": ["by-product_recovery", "no_by-product_recovery"],
            "product": ["coke_oven_gas", "coke_oven_gas"],
            "property": ["sample", "sample"],
            "value": [np.array([0.0, 0.0, 0.0]), np.array([0.2, 0.3, 0.25])],
            "unit": ["m3/t", "m3/t"],
        }
    ).set_index(["year", "region", "activity", "product", "property"])
    test.ppf_vol.metal.parameter.byproduct_supply_per_coke = df

    df = pd.DataFrame(
        data={
            "year": [2013, 2013],
            "region": ["DE", "DE"],
            "activity": ["by-product_recovery", "by-product_recovery"],
            "product": ["water", "nitrogen"],
            "property": ["sample", "sample"],
            "value": [np.array([0.0, 0.0, 0.0]), np.array([0.2, 0.3, 0.25])],
            "unit": ["m3/t", "m3/t"],
        }
    ).set_index(["year", "region", "activity", "product", "property"])
    test.ppf_vol.metal.parameter.feedstock_use_per_coke = df

    s = test.ppf_vol.metal.sequence.coke_tier1(
        year=2013,
        region="DE",
        activity="by-product_recovery",
        uncertainty="sample",
    )

    dfs = s.to_frames(
        bonsai="samples",
        # external_metadata=ppf.ppf._metadata.external_metadata,
        # external_functions=ppf.ppf._metadata.external_functions,
    )
    assert isinstance(dfs["bonsai"]["use"], pd.DataFrame) == True
    assert dfs["bonsai"]["transf_coeff"].empty == False
