import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import glob
import os
import sqlite3
import seaborn as sns
import numpy.polynomial.polynomial as poly

import streamlit as st
#streamlit page config:
st.set_page_config(page_icon=':bar_chart', page_title='DEMO STREAMLIT MAP', layout='wide')

numbers = [5, 8]

selected_number = st.selectbox('Select a number:', numbers)
st.write(f'Selected number: {selected_number}')

number = st.number_input("Enter a number", min_value=10, max_value=50, value=20, step=1)

# Display the entered number
st.write("You entered:", number)