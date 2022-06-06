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
fruit_choise = streamlit.text_input('What fruit do you like info about?', 'Kiwi')
streamlit.write('the user entered', fruit_choise)

import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choise)
## remove this line from app --streamlit.text(fruityvice_response.json())-- #this just writes data on the screen

#take the json version of the resonse and normalize it
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
#output is on the screen as a table
streamlit.dataframe(fruityvice_normalized)


import snowflake.connector

#query account meta data
## my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
## my_cur = my_cnx.cursor()
## my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
## my_data_row = my_cur.fetchone()
## streamlit.text("Hello from Snowflake:")
## streamlit.text(my_data_row)

#query some data
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit_load_list contains:")
streamlit.dataframe(my_data_rows)

#2nd section to add a response
add_my_fruit = streamlit.text_input('What fruit would you like to add?', 'jackfruit')
streamlit.write('Thanks for adding', add_my_fruit)

#this code will not work correctly, just go with it for now
my_cur.execute("insert into fruit_load_list values ('from streamlit')")
