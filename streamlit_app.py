import streamlit

streamlit.title('My Moms New Healthy Diner')

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Outmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
#choose the Fruit Name Column as the Index
my_fruit_list = my_fruit_list.set_index('Fruit')

#create picklist to select fruits to include
streamlit.multiselect("pick some fruits:", list(my_fruit_list.index))

#display list on the streamlit page
streamlit.dataframe(my_fruit_list)
