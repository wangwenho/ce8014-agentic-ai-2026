from agent import FinancialAgent
from config import get_client

if __name__ == "__main__":
    client = get_client()
    agent = FinancialAgent(client)
    agent.interactive_loop()
