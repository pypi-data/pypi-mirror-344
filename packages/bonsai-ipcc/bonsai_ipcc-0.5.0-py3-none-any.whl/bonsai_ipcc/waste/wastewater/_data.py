from ..._data import Concordance, Dimension, Parameter

dimension = Dimension(
    "data/", atctivitycode="wastewater_treatment", productcode="wastewater"
)

parameter = Parameter(["data/waste/wastewater/", "data/waste/waste_generation/"])

concordance = Concordance("data/")
