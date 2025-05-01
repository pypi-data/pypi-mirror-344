from ..._data import Concordance, Dimension, Parameter

dimension = Dimension("data/", atctivitycode="landfill", productcode="waste")

parameter = Parameter(["data/waste/swd/", "data/waste/waste_generation/"])

concordance = Concordance("data/")
