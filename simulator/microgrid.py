# simulator/microgrid.py
import numpy as np
import json
from typing import List

with open("agents/personas.json") as f:
    personas = json.load(f)

class Household:
    def __init__(self, id: int, data: dict):
        self.id = id
        self.persona = data["name"]
        self.pv_kw = data["pv_kw"]
        self.battery_kwh = data["battery_kwh"]
        self.soc = np.random.uniform(20, 90)
        self.surplus = 0.0
        self.deficit = 0.0

    def update(self, hour: int):
        solar = max(0, np.sin((hour - 6) * np.pi / 12)) * self.pv_kw * np.random.uniform(0.7, 1.2)
        load = 1.5 + np.random.beta(2, 5) * 3.5 + (3 if 17 <= hour <= 21 else 0)
        net = solar - load
        self.surplus = round(max(0, net), 2)
        self.deficit = round(max(0, -net), 2)

households: List[Household] = [Household(i, personas[i]) for i in range(20)]