import pandas as pd


def get_daily_data():
    daily_url = 'https://www.eia.gov/dnav/ng/hist_xls/RNGWHHDd.xls'
    df = None

    try:
        df = pd.read_excel(daily_url, sheet_name='Data 1', index_col=0, header=2)
    except Exception as ex:
        print('Exception in get_daily_data')
        print(str(ex))
    finally:
        return df


# This is to rename columns and resetting indices for later use
def transform(_df):
    try:
        _df.reset_index(level=0, inplace=True)
        _df.rename(columns={'Date': 'Date', 'Henry Hub Natural Gas Spot Price (Dollars per Million Btu)': 'Price'},
                   inplace=True)
    except Exception as ex:
        print('Exception in transform')
        print(str(ex))
    finally:
        return _df


# Generate monthly data
def generate_monthly_data(_df):
    try:
        _df = df_daily.set_index('Date', inplace=False)
        _df.index = pd.to_datetime(_df.index)

        # To ge the data of first working day of the month. Usually 1st of month but if no data is available then the next available
        # day
        _df = _df.resample('BMS').first()
        _df.reset_index(level=0, inplace=True)
    except Exception as ex:
        print('Exception in generate_monthly_data')
        print(str(ex))
    finally:
        return _df


# Save given dataframe to CSV
def save_csv(_df, file_name='daily.csv'):
    try:
        _df.to_csv(file_name, index=False)
    except Exception as ex:
        print('Exception in saving CSV file.')
        print(str(ex))
    finally:
        return _df


if __name__ == '__main__':
    df_daily = None
    df_monthly = None

    print('1/5: Getting the Daily Henry Hub gas prices data from EIA')

    df_daily = get_daily_data()

    print('2/5: Transforming the data')

    df_daily = transform(df_daily)

    print('3/5: Saving Daily Data into CSV file.')

    save_csv(df_daily)

    print('4/5: Saving Data Data into CSV file.')

    df_monthly = generate_monthly_data(df_daily)

    print('5/5: Saving Monthly Data into CSV file.')
    save_csv(df_monthly, 'monthly.csv')

    print(
        '\n\nThe processes completed. The resultant daily and monthly data can be seen in graphical format in daily.html and monthly.html respectively.\nIn case CSV file name is changed, you must edit the HTML files.')
