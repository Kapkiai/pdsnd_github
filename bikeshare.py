import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington)
    
    while True:
        city = input("Enter city.. options: [Chicago, New York City, Washington]\n").upper().strip()
        if city in ['CHICAGO', 'NEW YORK CITY', 'WASHINGTON']:
            break


    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Enter month.. options [All, January, February, March, April, May, June]\n").upper().strip()
        if month in ['ALL', 'JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE']:
            break


    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Enter day of week.. options [All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday]\n").upper().strip()
        if day in ['ALL', 'MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY']:
            break

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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("Most Common Month: ", str(df['month'].mode()[0]))


    # display the most common day of week
    print("Most Common day of week is: ", str(df['day_of_week'].mode()[0]))


    # display the most common start hour
    print("Most common start hour is: ", str(df['Start Time'].dt.hour.mode()[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    
#     print(df.info())

    # display most commonly used start station
    print('Most Commonly Used Start Station')
    print(df['Start Station'].mode()[0])


    # display most commonly used end station
    print('\nMost Commonly Used End Station')
    print(df['End Station'].mode()[0])


    # display most frequent combination of start station and end station trip
    print('\nMost frequent combination of start station and end station trip')
    df1 = '[Start]: ' + df['Start Station'] + ' [Stop]: ' + df['End Station']
    print(df1.mode()[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('\nTotal travel time in days, hours, min and seconds', sep='\n')
    print(pd.to_timedelta(str(df['Trip Duration'].sum()) + 's'))


    # display mean travel time
    print('\nMean travel time in days, hours, min and seconds')
    print(pd.to_timedelta(str(df['Trip Duration'].mean()) + 's'))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("\nCounts of user types")
    print(df.groupby(['User Type']).size().to_string())


    # Display counts of gender
    print("\nCounts of gender")
    if 'Gender' in df.columns:
        print(df.groupby(['Gender']).size().to_string())
        
    else:
        print('Gender stats cannot be calculated because \'Gender\' does not appear in the dataframe')
   


    # Display earliest, most recent, and most common year of birth
    print("\nEarliest, most recent, and most common year of birth")
    
    if 'Birth Year' in df.columns:
        print("Earliest year: ", df["Birth Year"].min(), end="\n\n")

        print("Most recent year: ", df["Birth Year"].max(), end="\n\n")

        print("Common year: ", df["Birth Year"].mode()[0], end="\n\n")
    else:
        print('Birth Year stats cannot be calculated because \'Birth Year\' does not appear in the dataframe')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """
    This function displays the content of the dataframe depending on users choice
    
    Args:
        (dataframe) df - Pandas dataframe containing data 
    Returns:
        null
    """
    view_data = input("Would you like to view rows of individual trip data? Enter yes or no?\n").upper().strip()
    start_loc = 0
    num_rows = 0
    
    while (view_data == "yes"):
        while True:
            rows = input("Enter number of rows you want to view\n").strip()
            
            if rows.isdigit():
                num_rows = int(rows)
                break
                
            else:
                print(num_rows, ": is no valid. Enter valid integer!!", end='\n\n')
                
        stop_loc = start_loc + num_rows
        df_len = len(df)
        
        print("\n","-"*40,"Displaying rows: ", start_loc, " to: ", df_len if stop_loc > len(df) else stop_loc , "-"*40, end='\n\n')
        
        print(df.iloc[start_loc:start_loc + num_rows].to_string())
        
        start_loc += num_rows
        
        view_display = input("\nDo you wish to continue viewing the next set of data?: Enter yes or no \n").lower()
        
        view_data = view_display
        
        if start_loc > df_len and view_data == 'yes':
            print("\nYou have already viewed all data, exiting.....\n")
            break
            

def main():
    while True:
        city, month, day = get_filters()
        print(city, month, day)
        df = load_data(city, month, day)

        time_stats(df)

        station_stats(df)

        trip_duration_stats(df)

        user_stats(df)

        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no., \n')
        
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
