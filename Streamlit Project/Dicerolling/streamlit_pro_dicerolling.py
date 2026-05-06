import random
import streamlit as st

def roll_dice():
    # Generate a random number between 1 and 6
    no = random.randint(1, 6)
    
    dice_faces = {
        1: "[-------]\n[       ]\n[   o   ]\n[       ]\n[-------]",
        2: "[-------]\n[o      ]\n[       ]\n[      o]\n[-------]",
        3: "[-------]\n[o      ]\n[   o   ]\n[      o]\n[-------]",
        4: "[-------]\n[o     o]\n[       ]\n[o     o]\n[-------]",
        5: "[-------]\n[o     o]\n[   o   ]\n[o     o]\n[-------]",
        6: "[-------]\n[o     o]\n[o     o]\n[o     o]\n[-------]"
    }
    
    return dice_faces[no]

# Streamlit UI
st.title("Dice Roller")
st.write("Click the button below to roll the dice.")

# Button to roll the dice
if st.button("Roll Dice"):
    dice_result = roll_dice()
    st.text(dice_result)