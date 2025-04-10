import streamlit as st
import pandas as pd

# Title
st.title("Interconnection Queue Dashboard")

# Example content - Replace with actual data fetching/processing code
st.write("This is where your interconnection queue data will be displayed.")

# Example data to check
data = {'ISO': ['CAISO', 'PJM', 'NYISO'], 'Queue Length': [10, 20, 5]}
df = pd.DataFrame(data)
st.dataframe(df)  # Display the data in a table
