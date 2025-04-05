# main.py
from advisor.agent import run_advisor

user_input = {
    'land_size': 2,
    'crop': 'Wheat',
    'goal': 50000,
    'language': 'english',
    'city': 'Bhopal'
}


result = run_advisor(user_input)
print("\nFarming Plan:\n")
print(result)
