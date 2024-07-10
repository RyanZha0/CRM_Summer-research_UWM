import pandas as pd
from datetime import datetime

file_path = r'D:\summer research\dataexperiment\data3min.csv'
df = pd.read_csv(file_path)

def convert_timestamp_to_datetime(Timestamp):
    try:
        dt_object = datetime.fromtimestamp(Timestamp)
        return dt_object
    except Exception as e:
        print(f"Error converting {Timestamp} to datetime: {e}")
        return None

df['datetime'] = df['Timestamp'].apply(convert_timestamp_to_datetime)

df = df.drop(['Timestamp', 'Device', 'X', 'Y'], axis=1)

cols = df.columns.tolist()
cols = ['datetime'] + [col for col in cols if col != 'datetime']
df = df[cols]

print(df.head())

output_path = r'D:\summer research\dataexperiment\data3min_daytime1.csv'
df.to_csv(output_path, index=False)
