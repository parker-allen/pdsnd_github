import time
import pandas as pd
import numpy as np

def get_filters():
    print('Hello! Let\'s explore some US bikeshare data!')

    # user input for city
    city = input('Which city would you like to analyze? ')
    while city.lower() not in ('chicago', 'new york city', 'washington'):
        city = input('It must be Chicago, New York City, or Washington... ')


    # user input for month of the year
    month = input('Which month would you like to analyze? Type \"all\" for no month filter: ')
    while month.lower() not in ('january', 'february', 'march', 'april', 'may',
                                'june', 'july', 'august', 'september', 'october',
                                'november', 'december'):
        print('It must be a valid month January thru December')
        month = input('Which month would you like to analyze? Type \"all\" for no month filter: ')

    # user input for day of the week
    day = input('Which day of the week would you like to analyze? Type \"all\" for no day filter: ')
    while day.lower() not in ('monday', 'tuesday', 'wednesday', 'thursday',
                                'friday', 'saturday', 'sunday', 'all'):
        day = input('It must be a valid day of the week... ')

    day = day.lower()
    if day != 'all':
        day = day.capitalize()

    print('-'*40)
    return city.lower(), month.lower(), day


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
    df = pd.read_csv(city.replace(' ', '_') + ".csv")
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # creating new columns to make it easier
    df['Month'] = df['Start Time'].dt.month
    df['Day'] = df['Start Time'].dt.day_name()
    df['Start Hour'] = df['Start Time'].dt.hour
    #df['test month'] = df.loc[df['Start Time'].dt.month]

    if month != 'all':
        df = df.loc[df['Start Time'].dt.month == switch_month_num(month)]
        #switches month name to number and cuts panda down to just that month

    if day != 'all':
        df = df.loc[df['Day'] == day.capitalize()]

    return df


def switch_month_num(param):
    """
    :param param: name of month or number associated with month
    :return: name of month or number associated with month, opposite of param
    """
    name = {
        'january': 1,
        'february': 2,
        'march': 3,
        'april': 4,
        'may': 5,
        'june': 6,
        'july': 7,
        'august': 8,
        'september': 9,
        'october': 10,
        'november': 11,
        'december': 12,
        1: 'january',
        2: 'february',
        3: 'march',
        4: 'april',
        5: 'may',
        6: 'june',
        7: 'july',
        8: 'august',
        9: 'september',
        10: 'october',
        11: 'november',
        12: 'december',
    }
    return name.get(param, "non month")


def print_pretty_hour(hour):
    if hour > 12:
        hour = str(hour - 12) + ' PM'
    else:
        hour = str(hour) + ' AM'
    print('The most popular start hour is:', hour)


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['Month'].mode()[0]
    print('The most popular month is:', switch_month_num(popular_month).capitalize())

    # display the most common day of week
    popular_day = df['Day'].mode()[0]
    print('The most popular day of the week is:', popular_day)

    # display the most common start hour
    popular_hour = df['Start Hour'].mode()[0]
    print_pretty_hour(popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('The most popular Start Station is:', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('The most popular End Station is:', popular_end_station, '\n')

    # display most frequent combination of start station and end station trip
    popular_combo = df.groupby(['Start Station', 'End Station']).size()\
                      .to_frame('count').reset_index().sort_values(by='count',
                      ascending=False).iloc[0].head(2)
    print('The most popular station combo is:\n', popular_combo, sep="")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total travel time:')
    tot_travel = float(df['Trip Duration'].sum())
    tot_travel /= 60
    print(round(tot_travel, 2), 'minutes')
    tot_travel /= 60
    print(round(tot_travel, 2), 'hours')
    tot_travel /= 24
    print(round(tot_travel, 2), 'days')

    # display mean travel time
    tot_travel = float(df['Trip Duration'].sum())
    num_trips = len(df.index)
    print('\nMean travel time:')

    print(round(float(tot_travel)/num_trips, 2), 'seconds')
    tot_travel /= 60
    print(round(float(tot_travel)/num_trips, 2), 'minutes')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # Display counts of user types
    if 'User Type' in df:
        print('Number of each type of user:')
        user_types = df['User Type'].value_counts()
        print(user_types, '\n')
    else:
        print('**No data for type of user**')

    # Display counts of gender
    if 'Gender' in df:
        print('Number of each gender:')
        num_each_gender = df['Gender'].value_counts()
        print(num_each_gender, '\n')
    else:
        print('**No data for gender**')

    if 'Birth Year' in df:
        # Display earliest, most recent, and most common year of birth
        earliest_birth = df['Birth Year'].min()
        print('Earliest Birth:', str(int(earliest_birth)))

        most_recent_birth = df['Birth Year'].max()
        print('Most recent birth:', str(int(most_recent_birth)))

        most_common_birth = df['Birth Year'].mode()[0]
        print('Most common birth:', str(int(most_common_birth)))
    else: print('No birth year stats')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    restart = 'yes'
    print('this is it')
    while restart.lower() == 'yes' :
        city, month, day = get_filters()
        df = load_data(city, month, day)
        try:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
        except IndexError:
            print('** ERROR: No data for what you requested **')
        restart = ''
        while restart not in ('yes', 'no'):
            restart = input('\nWould you like to restart? Enter yes or no: ')

if __name__ == "__main__":
	main()
