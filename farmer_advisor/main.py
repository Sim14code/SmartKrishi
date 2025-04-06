# main.py
from advisor.agent import run_advisor

user_input = {
    'land_size': 7,
    'crop': 'Soybean',
    'goal': 40000,
    'language': 'english',
    'city': 'Pune'
}


result = run_advisor(user_input)
print("\nFarming Plan:\n")
print(result)
