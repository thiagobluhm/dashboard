import streamlit as st

container = st.container(border=True)
container.write("dentro do container")
st.write("fora do container")

# Now insert some more in the container
container.write("dentro de novo do container")