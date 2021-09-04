import streamlit as st
import matplotlib.pyplot as plt
import preprocessor
import helper
import seaborn as sns

st.sidebar.title("WhatsApp Chat Analyzer")

# to upload file
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # Files will be read as byte
    bytes_data = uploaded_file.getvalue()
    # Converting the uploaded data in strings
    data = bytes_data.decode("utf-8")
    # To get the dataframe
    df = preprocessor.preprocess(data)

    # fetch unique user
    user_list = df['user'].unique().tolist()
    # removing group_notification from python list
    user_list.remove("group_notification")
    # sort the list items
    user_list.sort()
    # Add one more item with name Overall for overall analysis
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("Show Analysis with respect to", user_list)

    # Adding a analysis button feature
    if st.sidebar.button("Show Analysis"):
        # Back ground color of all matplotlib plots will be dark
        plt.style.use('dark_background')
        # setting font size to 30
        plt.rcParams.update({'font.size': 14})
        # Selected User Common Stats
        num_messages, num_words, num_media, num_links = helper.fetch_stats(selected_user, df)
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.subheader(num_messages)
        with col2:
            st.header("Total Words")
            st.subheader(num_words)
        with col3:
            st.header("Media files shared")
            st.subheader(num_media)
        with col4:
            st.header("Total Links")
            st.subheader(num_links)

        # Timeline Analysis
        # Daily timeline
        st.title('Daily Timeline')
        daily_timeline_df = helper.fetch_daily_timeline(selected_user, df)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(daily_timeline_df['only_date'], daily_timeline_df['message'], color='#1DA1F2')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Monthly Timeline
        st.title('Monthly Timeline')
        monthly_timeline_df = helper.fetch_monthly_timeline(selected_user, df)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(monthly_timeline_df['time'], monthly_timeline_df['message'], color='#1DA1F2')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Activity maps
        st.title("Activity Maps")
        busy_week = helper.weekly_activity_map(selected_user, df)
        busy_month = helper.monthly_activity_map(selected_user, df)
        col1, col2 = st.columns(2)
        with col1:
            st.header('Weekly Activity Map')
            fig, ax = plt.subplots()
            ax.bar(busy_week.index, busy_week.values, color='#1DA1F2')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.header('Monthly Activity Map')
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='#1DA1F2')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # Showing Activities in Heatmap
        st.title("Activity Heatmap")
        activity_pivot_table = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots(figsize=(12, 7))
        # cmap = sns.dark_palette("#3fdd01", as_cmap=True)
        ax = sns.heatmap(activity_pivot_table)
        ax.set_xlabel("Time Period")
        ax.set_ylabel("")
        plt.yticks(rotation='horizontal')
        st.pyplot(fig)

        # Forming WordCloud
        wc_df = helper.create_wordcloud(selected_user, df)
        st.title("WordCloud")
        fig, ax = plt.subplots(figsize=(20, 10))
        ax.imshow(wc_df, interpolation='bilinear')
        plt.axis('off')
        plt.margins(x=0, y=0)
        st.pyplot(fig)

        # Finding the busiest user in the group (Group Level)
        if selected_user == 'Overall':
            st.title("Most Busy Users")
            top_users, top_users_percent_df = helper.fetch_top_users(df)
            users_names = top_users.index
            users_messages_counts = top_users.values

            col1, col2 = st.columns([41, 50])
            with col1:
                fig, ax = plt.subplots()
                ax.bar(users_names, users_messages_counts, color='#1DA1F2')
                plt.xticks(rotation=30)
                st.pyplot(fig)
            with col2:
                fig, ax = plt.subplots()
                ax.pie(top_users_percent_df['percent'], labels=top_users_percent_df['name'], autopct="%0.2f%%", colors=['#003f5c', '#58508d', '#bc5090', '#ff6361', '#ffa600'], shadow=True, startangle=90)
                ax.axis('equal')
                plt.tight_layout(pad=0)
                st.pyplot(fig)

        # Most common words
        most_common_words_df = helper.most_common_words(selected_user, df)
        st.title("Most Common Words")
        fig, ax = plt.subplots()
        most_common_words_df = most_common_words_df.sort_values(by='count', ascending=True)
        ax.barh(most_common_words_df['word'], most_common_words_df['count'], color='#1DA1F2')
        # ax.bar_label(ax.containers[0])
        st.pyplot(fig)

        # Most common emojis
        st.title("Most Common Emoji")
        top_emoji_df = helper.emoji_data(selected_user, df)
        col1, col2 = st.columns([1, 3])
        with col1:
            st.dataframe(top_emoji_df[['Emoji', 'Count']])
        with col2:
            fig, ax = plt.subplots()
            # Sorting the dataframe in ascending order
            top_emoji_df = top_emoji_df.sort_values(by='Count', ascending=True)
            ax.barh(top_emoji_df['emoji_name'], top_emoji_df['Count'], color='#1DA1F2')
            # To get the count on the bars
            # ax.bar_label(ax.containers[0])
            st.pyplot(fig)