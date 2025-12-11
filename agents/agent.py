# agents/agent.py
from anthropic import Anthropic
from dotenv import load_dotenv
import os
load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

class Agent:
    def __init__(self, household):
        self.household = household

    def speak(self, context=""):
        prompt = f"""You are House {self.household.id}: {self.household.persona}
Battery: {self.household.soc:.0f}% | Next hour: +{self.household.surplus} kWh / {self.household.deficit} kWh deficit
Grid price: $0.134/kWh

{context}

Reply in 1-2 short, in-character sentences."""
        try:
            msg = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=100,
                temperature=0.9,
                messages=[{"role": "user", "content": prompt}]
            )
            return msg.content[0].text.strip()
        except:
            return "brb"