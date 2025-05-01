from ..._data import Concordance, Dimension, Parameter

dimension = Dimension("data/", atctivitycode="metal", productcode="metal_production")

parameter = Parameter(["data/industry/metal", "data/ppf/metal", "data/generic"])

concordance = Concordance("data/")
