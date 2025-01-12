import streamlit as st
import pandas as pd
import streamlit_antd_components as sac
import random

@st.cache_data
def read_data():
    df = pd.read_csv('resources.csv')
    df['duration'] = df['duration'].astype(int)
    return df

selected_media = False
selected_sub_categories = []
df = read_data()

categories = pd.DataFrame(df['category'].unique(),columns=['Category'])

selected_categories = [st.segmented_control("Select Category", categories, selection_mode="single",default=categories.iloc[0])]

min_duration = df['duration'].min()
max_duration = df['duration'].max()
if selected_categories[0]:
    min_duration = df[df['category'].isin(selected_categories)]['duration'].min()
    max_duration = df[df['category'].isin(selected_categories)]['duration'].max()

sub_categories = pd.DataFrame(df[df['category'].isin(selected_categories)]['sub_category'].unique(),columns=['SubCategory'])

if len(sub_categories) > 0:
    selected_sub_categories = st.segmented_control("Select SubCategory", sub_categories, selection_mode="multi",
                                                                        default = sub_categories)

duration_selection = st.slider("Duration", min_value=min_duration,
              max_value=max_duration, value=(min_duration,max_duration)),

df_selected = df[(df['category'].isin(selected_categories))&
                 (df['duration']>=duration_selection[0][0])&
                 (df['duration']<=duration_selection[0][1])&
                 (df['sub_category'].isin(selected_sub_categories))
                ]

selection_menu = []

if df_selected.shape[0]>0:
    for i, item in df_selected.iterrows():
        minutes_text = "דקות" if item['language'] == "Hebrew" else "minutes"
        selection_menu.append(
            sac.MenuItem( item['title'],
                          icon='play-btn-fill',
                          description = f"{item['author']} - {item['duration']} {minutes_text}",
            ))

    selected_item = sac.menu(selection_menu, size='sm', index=random.randint(0, len(selection_menu) - 1))

    item = df_selected[df_selected['title'] == selected_item].iloc[0]
    youtube_url = item['youtube_url']
    st.video(youtube_url)
    st.link_button(f"For more videos by {item['author']}", f"{item['channel']}")
