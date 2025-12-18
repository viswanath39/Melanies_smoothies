# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruits you want in your smoothie
  """
)

name_on_order = st.text_input("Name of Smoothie:")
st.write("The name on smoothie will be:", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()


my_dataframe = session.table("smoothies.public.fruit_options").select(col('Fruit_name'),col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True)

pd_df = my_dataframe.to_pandas()

ingredients_list = st.multiselect(
    'choose up to 5 ingredients:',my_dataframe,
    max_selections = 5
)

if ingredients_list:

     ingredients_string =''
     for each_fruit in ingredients_list:
          ingredients_string += each_fruit
       
          search_on = pd_df.loc[pd_df['FRUIT_NAME'] == each_fruit,'SEARCH_ON'].iloc[0]
          st.write('The search value for ',each_fruit,' is ',search_on, '.')

          st.subheader(each_fruit + 'Nutrition Information')
          smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_on}")
          sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
         
     st.write(ingredients_string)

     my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+"""')"""
     st.write(my_insert_stmt)
    
    
     time_to_insert = st.button('Submit Order')
    
     if time_to_insert:
         session.sql(my_insert_stmt).collect()
         
         st.success('Your Smoothie is ordered!', icon="✅")



