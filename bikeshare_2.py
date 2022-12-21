# this is PFDS project Bikeshare project
import time
import datetime
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']
MONTHS_ = ['All', 'january', 'february', 'march', 'april', 'may', 'june']  # for printing
DAYS_ = ['All (Monday-Sunday)', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


def display_raw_data(df):
    """Displays raw data on user request.
    Args:
        (DataFrame) df - Pandas DataFrame containing city data filtered by month and day
    """
    print(df.head())
    next = 0
    while True:
        view_raw_data = input('\nWould you like to view next five row of raw data? Enter yes or no.\n')
        if view_raw_data.lower() != 'yes':
            return
        next = next + 5
        print(df.iloc[next:next + 5])


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print('*First:\nChoose a CITY:\n1-Chicago\n2-Newyork city\n3-Washington')
    while True:
        choosen_city = int(input('Choose from 1 to 3 and press ENTER: '))
        if choosen_city >= 1 and choosen_city <= 3:
            if choosen_city == 1:
                city = 'chicago'
                print('\n\t **City: Chicago**')
            elif choosen_city == 2:
                city = 'new york city'
                print('\n\t **City: NewYork**')
            elif choosen_city == 3:
                city = 'washington'
                print('\n\t **City: Washington**')
            break
        else:
            print('## invalid input try again ##\n Remember from 0 to 3 only')

    # TO DO: get user input for month (all, january, february, ... , june)
    print('\n**SECOND**:\nChoose a MONTH:')
    for n in range(len(MONTHS_)):
        print('{0}-'.format(n), MONTHS_[n])

    while True:
        choosen_month = int(input('Choose from 0 to 6 and press ENTER : '))
        if choosen_month >= 0 and choosen_month <= 6:
            month = MONTHS[choosen_month - 1].lower()
            print('\n\t **Month:{0}**'.format(month))
            if choosen_month == 0:
                month = 'all'
                print('\n\t **Month: January to June**')
            break
        else:
            print('## invalid input try again ##\n Remember from 0 to 6 only')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    print('\n**THIRD**:\nChoose a DAY:')
    for n in range(len(DAYS_)):
        print('{0}-'.format(n), DAYS_[n])

    while True:
        try:
            day_number = int(input('Choose from 0 to 7 and press ENTER : '))
            if day_number == 0:
                day = 'all'
                break
            elif day_number >= 1 and day_number <= 7:
                day = DAYS[day_number - 1].lower()
                break
        except:
            pass
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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = MONTHS.index(month) + 1

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        # df = [df['day_of_week'] == day.title()]
        df = df.loc[df['day_of_week'] == DAYS.index(day) + 1]
    return df
    no


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]
    print('Most Frequent Month is: {}'.format(MONTHS[popular_month - 1].title()))

    # TO DO: display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most Frequent Day of Week is: {}'.format(DAYS[popular_day].title()))

    # TO DO: display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('Most Frequent Start Hour is: {}:00'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    popular_start_station_num_of_uses = df[df['Start Station'] == popular_start_station].count()[0]
    print("Most popular start station {} was used {} times".format(popular_start_station,
                                                                   popular_start_station_num_of_uses))

    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print("Most popular end station: {} ".format(popular_end_station))

    # TO DO: display most frequent combination of start station and end station trip
    df['Trip'] = 'FROM ' + df['Start Station'] + ' TO ' + df['End Station']
    most_frequent_trip = df['Trip'].mode()[0]
    print("Most popular trip is {}".format(most_frequent_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()  # seconds
    print("Total travel time for all trips is:", total_travel_time)

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("Mean travel time for all trips is:", mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Number of user type:', user_types)

    # TO DO: Display counts of gender
    if 'Gender' in df:
        user_gender = df['Gender'].value_counts()
        print('Number of user gender:', user_gender)

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        year_earliest = df['Birth Year'].min().astype(np.int64)
        year_most_recent = df['Birth Year'].max().astype(np.int64)
        year_most_common = df['Birth Year'].mode()[0].astype(np.int64)
        print("The oldest user was born in {}".format(year_earliest))
        print("The youngest user was born in {}".format(year_most_recent))
        print("The most common birth year of a user is {}".format(year_most_common))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        print(city, month, day)
        print(df.head())
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        while True:
            view_raw_data = input('\nWould you like to view first five row of raw data? Enter yes or no.\n')
            if view_raw_data.lower() != 'yes':
                break
            display_raw_data(df)
            break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
