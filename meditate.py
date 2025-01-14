import streamlit as st
import pandas as pd
import streamlit_antd_components as sac
import random
import numpy as np

@st.cache_data
def read_data():
    df = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vQHSHPGtVPIWeDM4rOd6zoJQS1Dwz9X2B3mqCtdcOQSbbu7u-Qd0riHxSesY5L6N-snBlCl4jvr2o84/pub?gid=1101369220&single=true&output=csv')
    df['duration'] = df['duration'].astype(int)
    return df

selected_media = False
selected_sub_categories = []
df = read_data()

categories = pd.DataFrame(df['category'].unique(),columns=['Category'])
languages =  pd.DataFrame(df['language'].unique(),columns=['language'])
ui_cols = st.columns(2)
with(ui_cols[0]):
    selected_categories = [st.segmented_control("Select Category", categories, selection_mode="single",default=categories.iloc[0])]
with(ui_cols[1]):
    selected_languages = st.segmented_control("Filter Languages", languages, selection_mode="multi",default=languages)
    if 'Any' in selected_languages:
        selected_languages = df['language'].unique().tolist()

max_duration = df['duration'].max()
if selected_categories[0] and len(selected_languages)>0:
    sub_df = df[(df['category'].isin(selected_categories))&
                      ((df['language'].isin(selected_languages)))]
    max_duration = sub_df['duration'].max()

    sub_categories = pd.DataFrame(sub_df['sub_category'].unique(),columns=['SubCategory'])

    if len(sub_categories) > 0:
        selected_sub_categories = st.segmented_control("Select SubCategory", sub_categories, selection_mode="multi",
                                                                            default = sub_categories)
    if not np.isnan(max_duration):
        duration_selection = st.slider("Duration", min_value=0,
                      max_value=max_duration, value=(0,max_duration)),

        df_selected = sub_df[(sub_df['category'].isin(selected_categories))&
                         (sub_df['duration']>=duration_selection[0][0])&
                         (sub_df['duration']<=duration_selection[0][1])&
                         (sub_df['sub_category'].isin(selected_sub_categories))
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

            selected_item = sac.menu(selection_menu)

            item = df_selected[df_selected['title'] == selected_item].iloc[0]
            youtube_url = item['youtube_url']
            st.video(youtube_url)
            st.link_button(f"For more videos by {item['author']}", f"{item['channel']}")
