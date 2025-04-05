# advisor/prompt_builder.py

def build_prompt(user_input, analysis):
    return f"""
The farmer has {user_input['land_size']} acres of land and wants to grow {user_input['crop']}. 
They aim to earn ₹{user_input['goal']}.

Based on data:
- Expected Yield: {analysis['expected_yield']:.2f} tons
- Fertilizer Needed: {analysis['fertilizer_needed']:.1f} kg
- Pesticide Needed: {analysis['pesticide_needed']:.1f} kg
- Sustainability Score: {analysis['sustainability']} / 10

Generate a farming plan to help the farmer meet their financial goal.
"""
