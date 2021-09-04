# Loading necessary libraries
import re
import pandas as pd


def preprocess(data):
    pattern = "\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s-\s"

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    # Converting the data into dataframe
    df = pd.DataFrame({'user_message': messages, 'date': dates})
    # converting message_data type
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y, %H:%M - ')

    # separating users from messages
    users = []
    messages = []
    for message in df['user_message']:
        temp = re.split("([\w\W]+?):\s", message)
        # temp[1:] will only exist when there is some user
        if temp[1:]:
            users.append(temp[1])
            messages.append(temp[2])
        else:
            users.append('group_notification')
            messages.append(temp[0])

    # New column for users and messages
    df['user'] = users
    df['message'] = messages
    # dropping the user_message column
    df.drop(columns=['user_message'], inplace=True)

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['month_num'] = df['date'].dt.month
    df['only_date'] = df['date'].dt.date
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    # Adding a period column
    period = []
    for hour in df['hour']:
        if hour == '23':
            period.append(str(hour) + '-' + str('00'))
        elif hour == '0':
            period.append(str('00') + '-' + str(hour + 1))
        else:
            period.append(str(hour) + '-' + str(hour + 1))
    df['period'] = period

    return df
