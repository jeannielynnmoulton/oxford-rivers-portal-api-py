{
 "cells": [
  {
   "metadata": {},
   "cell_type": "raw",
   "source": [
    "from src.oxrivers_api.client import OxfordRiversClient\n",
    "from src.oxrivers_api.determinands_discovery import DeterminandsDiscovery\n",
    "from src.oxrivers_api.loader import Loader\n",
    "from src.oxrivers_api.sites_discovery import SitesDiscovery\n",
    "\n",
    "# choose where to store json\n",
    "data_dir: str = \"../data\"\n",
    "\n",
    "# set up Oxford Rivers Client and Pandas loader\n",
    "client = OxfordRiversClient(data_dir)\n",
    "loader = Loader(client)\n",
    "\n",
    "# see what determinands there are\n",
    "determinands_discovery = DeterminandsDiscovery.get_determinands_info()"
   ],
   "id": "21db000cb68ffbf7"
  }
 ],
 "metadata": {},
 "nbformat": 4,
 "nbformat_minor": 5
}
