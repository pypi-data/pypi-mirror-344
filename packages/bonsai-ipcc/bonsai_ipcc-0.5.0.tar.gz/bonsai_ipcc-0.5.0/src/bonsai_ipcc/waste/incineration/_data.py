from ..._data import Concordance, Dimension, Parameter

dimension = Dimension(
    path_in="data/", atctivitycode="incineration", productcode="waste"
)

parameter = Parameter(["data/waste/incineration/", "data/waste/waste_generation/"])

concordance = Concordance("data/")
