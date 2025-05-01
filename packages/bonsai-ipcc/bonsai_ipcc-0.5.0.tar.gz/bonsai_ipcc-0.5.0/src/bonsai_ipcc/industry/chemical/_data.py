from ..._data import Concordance, Dimension, Parameter

dimension = Dimension("data/", atctivitycode="petrochem", productcode="refined")

parameter = Parameter(["data/industry/chemical"])

concordance = Concordance("data/")
