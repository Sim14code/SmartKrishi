# main.py
from advisor.agent import run_advisor

# Example input from farmer
user_input = {
    'land_size': 3,
    'crop': 'Wheat',
    'goal': 90000,
    'language': 'hindi'
}


result = run_advisor(user_input)
print("\nFarming Plan:\n")
print(result)
