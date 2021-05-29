"""
 bikeshare_2.py
"""

import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june',
          'july', 'august', 'september', 'october', 'november', 'december']

DAYS_OF_WEEK = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Which city would you like to analyze?\n(Chicago, New York City, Washington): ').lower()
    while city not in CITY_DATA.keys():
        print("\nThat's not a valid city")
        city = input('Which city would you like to analyze?\n(Chicago, New York City, Washington): ').lower()

    # get user input for month (all, january, february, ... , june)
    month = input('Which month would you like to filter by?\n(full month name or "all"): ').lower()
    while month != 'all' and month not in MONTHS:
        print("\nThat's not a valid month")
        month = input('Which month would you like to filter by?\n(full month name or "all"): ').lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Which day would you like to filter by?\n(full day name or "all"): ').lower()
    while day != 'all' and day not in DAYS_OF_WEEK:
        print("\nThat's not a valid day")
        day = input('Which day would you like to filter by?\n(full day name or "all"): ').lower()

    print('-' * 40)

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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday

    if month != 'all':
        df = df[df['month'] == MONTHS.index(month) + 1]

    if day != 'all':
        df = df[df['day_of_week'] == DAYS_OF_WEEK.index(day)]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = MONTHS[df['month'].mode()[0]-1].title()
    print('Most common month is: {}'.format(common_month))

    # display the most common day of week
    common_dow = DAYS_OF_WEEK[df['day_of_week'].mode()[0]].title()
    print('Most common day of week is: {}'.format(common_dow))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print('Most common start hour is: {}'.format(df['hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most common starting station: {}'.format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print('Most common end station: {}'.format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    df['Trip stations'] = df['Start Station'] + ' to ' + df['End Station']
    print('Most common route: {}'.format(df['Trip stations'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total travel time is {} minutes.'.format(df['Trip Duration'].sum()))

    # display mean travel time
    print('The mean trip duration is {} minutes.'.format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("User type counts:")
    for item in user_types.index:
        print('{} : {}'.format(item, user_types[item]))

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print("\nGender counts:")
        for item in gender_counts.index:
            print('{} : {}'.format(item, gender_counts[item]))

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('\nBirth year statistics:')
        print('Earliest birth year: {}'.format(df['Birth Year'].min()))
        print('Most recent birth year: {}'.format(df['Birth Year'].max()))
        print('Most common birth year: {}'.format(df['Birth Year'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        # prompt user for raw data display
        cursor = 0
        view_raw = input('\nWould you like to view the raw data?\n(yes or no): ').lower()
        while view_raw == 'yes':
            print(df[cursor:cursor+5])
            cursor += 5
            view_raw = input('\nWould you like to view more data?\n(yes or no)').lower()

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
