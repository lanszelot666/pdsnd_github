import time
import pandas as pd
import numpy as np
import calendar
from pyfiglet import Figlet


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# MONTH_DATA_DICT = dict((v,k) for k,v in enumerate(calendar.month_name))
MONTH_DATA_DICT = {'January' : 1, 'February' : 2, 'March' : 3, 'April' : 4, 'May' : 5, 'June' : 6}
MONTH_NAMES_LIST = list(MONTH_DATA_DICT.keys())

DAY_DATA_DICT = dict((v,k) for k,v in enumerate(calendar.day_name))
DAY_NAMES_LIST = list(DAY_DATA_DICT.keys())

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    f=Figlet(font='slant')
    print(f.renderText('US BIKESHARE\n-----------'))

    city, month, day = '', '', ''
    # Get user input for city (chicago, new york city, washington)
    while True:
        city = str(input('Please define the city, you would like to analyze: ')).lower()
        if city in CITY_DATA.keys():
            break
        else:
            print('\nInvalid city as input! \nPlease choose from: \"Chicago\", \"Washington\" or \"New York City\"!\n')

    # Get user input for month (all, january, february, ... , june)
    while True:
        month = str(input('Please define the month: ')).title()
        if month in MONTH_DATA_DICT or month == 'All':
            break
        else:
            print('\nInvalid month as input! \nPlease choose from the first 6 months, or type \'All\' to analyze the whole period!\n')

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = str(input('Please define the day:   ')).title()
        if day in DAY_DATA_DICT or day == 'All':
            break
        else:
            print('\nInvalid day as input! \nPlease type any valid day name in english, or type \"All\" for proper analyzation!\n')

    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['weekday_name'] = df['Start Time'].dt.weekday_name
    df['start_hour'] = df['Start Time'].dt.hour
    df['end_hour'] = df['End Time'].dt.hour

    # filter by month if applicable
    if month != 'All':
        # filter by month to create the new dataframe
        df = df[df['month'] == MONTH_DATA_DICT[month]]

    # filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df[df['weekday_name'] == day]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    print('The most common month was:             {}'.format(MONTH_NAMES_LIST[df['month'].mode()[0] - 1]))

    # Display the most common day of week
    print('The most common day of the week was:   {}'.format(df['weekday_name'].mode()[0]))

    # Display the most common start hour
    print('The most common start hour was:        {}'.format(df['start_hour'].mode()[0]))

    # Display the most common end hour
    print('The most common end hour was:          {}'.format(df['end_hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    print('The most commonly used start station: {}'.format(df['Start Station'].mode()[0]))

    # Display most commonly used end station
    print('The most commonly used end station:   {}'.format(df['End Station'].mode()[0]))

    # Display most frequent combination of start station and end station trip
    print('The most frequent combination of start and end station: {}'.format((df['Start Station'] + ' and ' + df['End Station']).mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_travel_time_sec = int(df['Trip Duration'].sum())
    total_travel_time = pd.to_timedelta(total_travel_time_sec, unit = 's')
    print('Total travel time in seconds: {:>10} , which equals to {:>18}'.format(str(total_travel_time_sec), str(total_travel_time)))

    # Display mean travel time
    mean_travel_time_sec = int(df['Trip Duration'].mean())
    mean_travel_time = pd.to_timedelta(mean_travel_time_sec, unit = 's')
    print('Mean travel time in seconds:  {:>10} , which equals to {:>18}'.format(str(mean_travel_time_sec), str(mean_travel_time)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('\nThe number of each user type: \n\n{}\n'.format(user_types.to_frame()))

    # Display counts of gender
    try:
        gender_types = df['Gender'].value_counts()
        print('\nThe number of each gender: \n\n{}\n'.format(gender_types.to_frame()))
    except KeyError:
        print('\nFor this table, there is no gender data provided!')

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_birth = int(df['Birth Year'].min())
        most_recent_birth = int(df['Birth Year'].max())
        most_common_birth = int(df['Birth Year'].mode()[0])
        print('Earliest birth year:    {:d}'.format(earliest_birth))
        print('Most recent birth year: {:d}'.format(most_recent_birth))
        print('Most common birth year: {:d}'.format(most_common_birth))
    except KeyError:
        print('\nFor this table, there is no gender date provided!')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data_display(df):
    row_counter = 5;
    if str(input('Would You like to see the raw data? Type \'yes\' if so: ')).lower() == 'yes':
        print('\n',df.iloc[0:row_counter,:],'\n')
        while True:
            if str(input('Would You like to see 5 more rows of the raw data? Type \'yes\' if so: ')).lower() == 'yes':
                print('\n',df.iloc[row_counter:row_counter+5,:],'\n')
                row_counter += 5
            else:
                break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        raw_data_display(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data_display(df)

        restart = input('\nWould you like to restart? Enter yes or no: ')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
