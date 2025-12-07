import unittest

import pandas as pd

from src.oxrivers_api.client import OxfordRiversClient
from src.oxrivers_api.determinands_discovery import DeterminandsDiscovery
from src.oxrivers_api.loader import Loader

import pandas.testing as pd_testing

class MyTestCase(unittest.TestCase):
    client = OxfordRiversClient("./tests/data")
    loader = Loader(client)
    discovery = DeterminandsDiscovery(loader)

    def test_get_ids(self):
        self.assertEqual(self.discovery.get_ids(), ['Alkalinity to pH 4.5 as CaCO3 (mg/l)', 'Ammonia un-ionised as N (mg/l)', 'Ammonium (mg/L)', 'Ammoniacal Nitrogen as N (mg/l)', 'Blue-Green Algae (RFU)', 'Carbon, Organic, Dissolved as C :- {DOC} (mg/l)', 'Chloride (mg/l)', 'Chlorophyll (µg/L)', 'Conductivity at 25 C (µS/cm)', 'Conductivity (µS/cm)', 'Dissolved organic carbon (mg/l)', 'Escherichia coli (EC)', 'Fluorescent Dissolved Organic Matter (RFU)', 'Intestinal enterococci (IE)', 'Nitrate as N (mg/l)', 'Nitrite as N (mg/l)', 'Nitrogen, Total as N (mg/l)', 'Nitrogen, Total Oxidised as N (mg/l)', 'Orthophosphate, reactive as P (mg/l)', 'Oxygen, Dissolved, % Saturation (%)', 'Oxygen, Dissolved as O2 (mg/l)', 'pH (phunits)', 'Phosphorus, Total as P (mg/l)', 'Secchi Tube: Turbidity (NTU)', 'Silica, reactive as SiO2 (mg/l)', 'Suspended solids (mg/l)', 'Temperature of Water (cel)', 'Water flow', 'Water level'])

    def test_get_columns(self):
        self.assertEqual(self.discovery.get_columns(), ['name', 'description', 'datasets'])

    def test_get_datasets_with_detemrinand(self):
        expected_df = pd.DataFrame(columns=["dataset", "id"])
        expected_df.loc[0] = ["ea_bathing_water", "EC"]
        expected_df.loc[1] = ["wtrt", "EC"]
        pd_testing.assert_frame_equal(self.discovery.get_datasets_with_determinand("Escherichia coli (EC)"), expected_df)

if __name__ == '__main__':
    unittest.main()
