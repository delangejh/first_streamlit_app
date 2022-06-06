import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Moms New Healthy Diner')

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Outmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
#choose the Fruit Name Column as the Index
my_fruit_list = my_fruit_list.set_index('Fruit')

#create picklist to select fruits to include
fruits_selected = streamlit.multiselect("pick some fruits:", list(my_fruit_list.index),['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

#display list on the streamlit page
streamlit.dataframe(fruits_to_show)

## new section to display fruityvice api response
## streamlit.header('Fruityvice Fruit Advice!')
## fruit_choise = streamlit.text_input('What fruit do you like info about?', 'Kiwi')
## streamlit.write('the user entered', fruit_choise)

##import requests
## fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choise)
## remove this line from app --streamlit.text(fruityvice_response.json())-- #this just writes data on the screen

#take the json version of the resonse and normalize it
## fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
#output is on the screen as a table
## streamlit.dataframe(fruityvice_normalized)

#create the repeatable code block = a function
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return  fruityvice_normalized

#new section to display fruityvice api response
streamlit.header('Fruityvice Fruit Advice!')
try:
    fruit_choice = streamlit.text_input('What fruit do like info about?')
    if not fruit_choice:
        streamlit.error("Please select a fruit to get info.")
    else:
        back_from_function = get_fruityvice_data(fruit_choice)
        streamlit.dataframe(back_from_function)

except URLError as e:
    streamlit.error()

#import snowflake.connector

#query account meta data
## my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
## my_cur = my_cnx.cursor()
## my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
## my_data_row = my_cur.fetchone()
## streamlit.text("Hello from Snowflake:")
## streamlit.text(my_data_row)

#move the Fruit Load List Query and Load into a Button Action
streamlit.header("The fruit load list contains:")
#snowflake related functions
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
         my_cur.execute("select * from fruit_load_list")
         return my_cur.fetchall()
        
#add a button to load the fruit
if streamlit.button('get fruit load list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe(my_data_rows)
   
#2nd section to add a response
#Create a Function and Button to Add the Fruit Name Submissions
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
         my_cur.execute("insert into fruit_load_list values ('from streamlit')")
         return  "Thanks for adding " + new_fruit
    
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a fruit to the list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_my_fruit)
    streamlit.txt(back_from_function)

#streamlit.write('Thanks for adding', add_my_fruit)

#don't run anything past here while we troubleshoot
streamlit.stop()

