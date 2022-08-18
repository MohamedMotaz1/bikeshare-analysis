from calendar import day_name, month
import os
from statistics import mean
import sys
import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
city_names = ('chicago', 'new york city', 'washington')
months_names = ('january', 'february', 'march',
                'april', 'may', 'june', 'july', 'all')
day_name = ('saturday', 'sunday', 'monday', 'tuesday',
            'wednesday', 'thursday', 'friday', 'all')


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
    while True:
        city = input('please inter the city name:').lower()
        if city not in city_names:
            print('please enter a valid name.')
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input(
            'please input a full month name from january to june or all for all months:').lower()
        if month not in months_names:
            print('please input a valid month name.')
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('please input the name of the day "all" for all days:').lower()
        if day not in day_name:
            print('please input a valid day name.')
        else:
            break
    print('you choosed {} for city \n {} for month \n {} for day'.format(
        city, month, day))
    print('-'*40)
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

    df = pd.read_csv(os.path.join(sys.path[0] ,CITY_DATA[city]))
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()
    if month != 'all':
        df = df[df['month'] == month.title()]
    else:
        pass
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    else:
        pass
    return df


def time_stats(df,month,day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month == 'all' :
        print('The most common month for trips: {}.'.format(df['month'].mode()[0]))
    

    # display the most common day of week
    if day == 'all' and month == 'all' :
        print('The most common day for trips: {}.'.format(df['day_of_week'].mode()[0]))
    if day != 'all'and month != 'all':
        print('The most common day for trips: {}.'.format(df['day_of_week'][df['month']==month.title()].mode()[0]))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    if day == 'all' and month == 'all':
        print('The most common start hour: {}.'.format(df['hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most common start station is {}. '.format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print('The most common end station is: {}.'.format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    df['most_frequent_combination'] = df['Start Station'] + df['End Station']
    print('The most frequent combination of start and end stations is: {}.'.format(df['most_frequent_combination'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    # Start Time is converted into datetime earlier now it's time to convert End Time
    df['End Time'] = pd.to_datetime(df['End Time'])
    print('Total travel time: {}'.format((df['End Time'] - df['Start Time']).sum()))

    # display mean travel time
    mean_travel_time = (df['End Time'] - df['Start Time']).mean()
    # show mean travel time in seconds
    print('The mean travel time is: {}'.format(mean_travel_time.total_seconds()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, City):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    subscriber_count = user_types[0]
    customer_count = user_types[1]

    print("There are {} subscribers.\n and {} customers.".format(
        subscriber_count, customer_count))
    # Display counts of gender
    if City in ('chicago', 'new york city'):
        gender_count = df['Gender'].value_counts()

        print('There are {} male and {} female users in {}.'.format(
            gender_count[0], gender_count[1], City))

    # Display earliest, most recent, and most common year of birth
    if City in ('chicago', 'new york city'):
        earliest_birth = df['Birth Year'].min()
        most_recent_birth = df['Birth Year'].max()
        most_comon_birth = df['Birth Year'].mode()[0]

        print('The earliest year is {}.'.format(earliest_birth))
        print('The most recent year of birth is {}.'.format(most_recent_birth))
        print('The most common year of birth is {}.'.format(most_comon_birth))

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

def raw_data_input(df, start_loc = 0):
    while True:
        raw_data_question = input('would you like to view 5 rows of data? Enter yes or no: ').lower()
        if raw_data_question not in ('yes','no'):
            print('please input a valid answer')
        else:
            break
    while raw_data_question == 'yes' :
        stop_loc = start_loc + 5
        print(df.iloc[start_loc:stop_loc])
        stop_loc += 5
        raw_data_continue = input('would you like to see more rows? yes or no.').lower()
        if raw_data_continue == 'yes':
            start_loc += 5
            print(df.iloc[start_loc:stop_loc])
        else:
            break
        



    


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df,month,day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data_input(df)
        

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
