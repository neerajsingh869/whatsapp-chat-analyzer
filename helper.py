from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji


# Function to extract common stats
def fetch_stats(selected_user, df):
    # filtering the dataframe with respect to selected_user
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    # fetching number of messages
    num_messages = df.shape[0]
    # fetching number of total words
    words = []
    for message in df['message']:
        words.extend(message.split())
    num_words = len(words)
    # fetching the number of media files shared
    num_media = df[df['message'] == '<Media omitted>\n'].shape[0]
    # fetching the number of links shared
    extractor = URLExtract()
    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))
    num_links = len(links)
    return num_messages, num_words, num_media, num_links


# Function to extract most busy users in a group (MeaningFul only for Overall Analysis)
def fetch_top_users(df):
    # removing group notification messages
    df = df[df['user'] != 'group_notification']
    top_users = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return top_users, df.head()


# Function to fetch the monthly timeline of Users from the data
def fetch_monthly_timeline(selected_user, df):
    # filtering the dataframe with respect to selected_user
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    # Building new dataframe using df to fetch monthly timeline data
    monthly_timeline_df = df.groupby(['year', 'month', 'month_num']).count()['message'].reset_index()
    time = []
    for i in range(monthly_timeline_df.shape[0]):
        print(str(monthly_timeline_df['year'][i]) + "-" + monthly_timeline_df['month'][i])
        time.append(str(monthly_timeline_df['year'][i]) + "-" + monthly_timeline_df['month'][i])
    monthly_timeline_df['time'] = time
    return monthly_timeline_df


# Function to fetch the daily timeline of Users from the data
def fetch_daily_timeline(selected_user, df):
    # filtering the dataframe with respect to selected_user
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    daily_timeline_df = df.groupby(['only_date']).count()['message'].reset_index()
    return daily_timeline_df


# Function to get weekly activity map
def weekly_activity_map(selected_user, df):
    # filtering the dataframe with respect to selected_user
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    return df['day_name'].value_counts()


# Function to get monthly activity map
def monthly_activity_map(selected_user, df):
    # filtering the dataframe with respect to selected_user
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    return df['month'].value_counts()


# Function to get activity heatmap
def activity_heatmap(selected_user, df):
    # filtering the dataframe with respect to selected_user
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    # Building pivot table
    activity_pivot_table = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return activity_pivot_table

# # Function to get yearly activity map
# def yearly_activity_map(selected_user, df):
#     # filtering the dataframe with respect to selected_user
#     if selected_user != "Overall":
#         df = df[df['user'] == selected_user]
#     return df['month'].value_counts()


# Function to create the Word Cloud
def create_wordcloud(selected_user, df):
    handle = open('stop_hinglish.txt', 'r')
    stop_words = handle.read()
    # filtering the dataframe with respect to selected_user
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    # removing group notification messages
    temp = df[df['user'] != 'group_notification']
    # removing media omitted messages
    temp = temp[temp['message'] != '<Media omitted>\n']
    # removing messages which comes when a message is deleted
    temp = temp[temp['message'] != 'This message was deleted\n']
    # removing stop words in hinglish language
    total_imp_words = ''
    for message in temp['message']:
        new_words_in_message = []
        for word in message.lower().split():
            if word not in stop_words:
                new_words_in_message.append(word)
        total_imp_words += " ".join(new_words_in_message) + " "
    wc = WordCloud(height=1000, width=1600, min_font_size=10,
                   margin=0, colormap='Set2', collocations=False)
    # Generating wordcloud image by first converting the message
    # column data into a string
    wc_df = wc.generate(total_imp_words)
    return wc_df


# Function for finding most common words
def most_common_words(selected_user, df):
    handle = open('stop_hinglish.txt', 'r')
    stop_words = handle.read()
    # filtering the dataframe with respect to selected_user
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    # removing group notification messages
    temp = df[df['user'] != 'group_notification']
    # removing media omitted messages
    temp = temp[temp['message'] != '<Media omitted>\n']
    # removing messages which comes when a message is deleted
    temp = temp[temp['message'] != 'This message was deleted\n']
    # removing stopwords in hinglish language
    word_list = []
    for message in temp['message']:
        message = message.lower()
        message_split = message.split()
        for word in message_split:
            if word not in stop_words:
                word_list.append(word)
    # Storing 15 most common words in the dataframe
    most_common_words_df = pd.DataFrame(Counter(word_list).most_common(15),
                                        columns=['word', 'count'])
    return most_common_words_df


def emoji_data(selected_user, df):
    # filtering the dataframe with respect to selected_user
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])
    emoji_df = pd.DataFrame(Counter(emojis).most_common(10), columns=['Emoji', 'Count'])
    emoji_df['emoji_name'] = emoji_df['Emoji'].apply(lambda x: emoji.UNICODE_EMOJI['en'][x])
    emoji_df['emoji_name'] = emoji_df['emoji_name'].str.replace(':', '')
    emoji_df['emoji_name'] = emoji_df['emoji_name'].str.replace('_', ' ')
    return emoji_df
