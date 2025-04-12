import streamlit as st
import pandas as pd

### magic commands...
st.title("DATAFRAME")
st.write("Meu dataframe do coracao.")
st.write(pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
}))