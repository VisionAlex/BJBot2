import json

def get_strategy():
    with open('strategy/strategy.json', newline='') as file:
       strategy = json.loads(file.read())
       return strategy


