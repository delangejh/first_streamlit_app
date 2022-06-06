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
fruits_selected = streamlit.multiselect("pick some fruits:", list(my_fruit_list.index),['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

#display list on the streamlit page
streamlit.dataframe(fruits_to_show)

#new section to display fruityvice api response
streamlit.header('Fruityvice Fruit Advice!')

import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + "kiwi")
## remove this line from app --streamlit.text(fruityvice_response.json())-- #this just writes data on the screen

#take the json version of the resonse and normalize it
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
#output is on the screen as a table
streamlit.dataframe(fruityvice_normalized)
