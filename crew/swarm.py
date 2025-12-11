# crew/swarm.py
from simulator.microgrid import households
from agents.agent import Agent
import random

agents = [Agent(h) for h in households]
trades = []
total_kwh = 0.0
total_usd = 0.0

def run_hour(hour: int):
    global total_kwh, total_usd
    for h in households:
        h.update(hour % 24)

    for _ in range(12):
        seller, buyer = random.sample(agents, 2)
        if seller.household.surplus > 0.8 and buyer.household.deficit > 0.8:
            offer = seller.speak(f"Selling to {buyer.household.persona}")
            reply = buyer.speak(offer)
            if any(w in reply.lower() for w in ["yes","deal","buy","lfg","sold","take"]):
                kwh = round(min(seller.household.surplus, buyer.household.deficit, 4), 2)
                price = round(random.uniform(0.07, 0.11), 3)
                total_kwh += kwh
                total_usd += kwh * price
                trades.append(f"{seller.household.persona} → {buyer.household.persona}: {kwh} kWh @ ${price}")