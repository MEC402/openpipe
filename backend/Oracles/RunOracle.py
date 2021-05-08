from backend.Oracles.CityOracle import CityOracle
from backend.Oracles.CountryOracle import CountryOracle
from backend.Oracles.CultureOracle import CultureOracle
from backend.Oracles.Formatter import Formatter

co=CountryOracle()
co.runOracle()
print("=================================================================================================")
cci=CityOracle()
cci.runOracle()

# cu=CultureOracle()
# cu.runOracle()


