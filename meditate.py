import streamlit as st
import pandas as pd

@st.cache_data
def read_data():
    df = pd.read_csv('resources.csv')
    df['duration'] = df['duration'].astype(int)
    return df

selected_media = False
df = read_data() 

min_duration = df['duration'].min()
max_duration = df['duration'].max()

categories = pd.DataFrame(df['category'].unique(),columns=['Category'])
category_selection = st.sidebar.dataframe(categories,
                                  on_select='rerun',
                                  hide_index = True,
                                  selection_mode = "multi-row",
                                  )
if len(category_selection.selection['rows']):
    selected_categories = [categories['Category'].iloc[row] for row in category_selection.selection['rows']]
else:
    selected_categories = categories['Category'].values

sub_categories = pd.DataFrame(df[df['category'].isin(selected_categories)]['sub_category'].unique(),columns=['SubCategory'])

subcategory_selection = st.sidebar.dataframe(sub_categories,
                                  on_select='rerun',
                                  hide_index = True,
                                  selection_mode = "multi-row",
                                  )
if len(subcategory_selection.selection['rows']):
    selected_sub_categories = [sub_categories['SubCategory'].iloc[row] for row in subcategory_selection.selection['rows']]
else:
    selected_sub_categories = sub_categories['SubCategory'].values


duration_selection = st.slider("Duration", min_value=min_duration, 
              max_value=max_duration, value=(min_duration,max_duration)),

df_selected = df[(df['category'].isin(selected_categories))&
                 (df['duration']>=duration_selection[0][0])&
                 (df['duration']<=duration_selection[0][1])&
                 (df['sub_category'].isin(selected_sub_categories))
                ]


event = st.dataframe(
    df_selected[['title','author','duration']],
    on_select='rerun',
    selection_mode='single-row',
    use_container_width=True
)

if len(event.selection['rows']):
    youtube_url = df_selected['youtube_url'].iloc[event.selection['rows'][0]]  
    st.video(youtube_url)

