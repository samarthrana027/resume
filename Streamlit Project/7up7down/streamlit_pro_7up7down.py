import random
import streamlit as st
def roll_dice():
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    return dice1, dice2, dice1 + dice2
def play_7_up_7_down():
    st.title("Welcome to 7 Up 7 Down!")
    st.write(""" 
    **Rules:**
    1. Guess whether the sum of two dice will be:
        - 'up' (greater than 7)
        - 'down' (less than 7)
        - 'exact' (exactly 7).
    2. Type your guess and click to roll the dice!
    """)

    
    guess = st.radio("Enter your guess:", ("up", "down", "exact"), key="guess_radio")

    if st.button("Roll Dice"):
        dice1, dice2, total = roll_dice()
        st.write(f"\nThe dice rolls are: {dice1} and {dice2}. Total = {total}.")
        
        if total > 7 and guess == "up":
            st.success("You guessed right! It's 7 Up!")
        elif total < 7 and guess == "down":
            st.success("You guessed right! It's 7 Down!")
        elif total == 7 and guess == "exact":
            st.success("You guessed right! It's exactly 7!")
        else:
            st.error("Oops! Better luck next time!")

if __name__ == "__main__":
    play_7_up_7_down()