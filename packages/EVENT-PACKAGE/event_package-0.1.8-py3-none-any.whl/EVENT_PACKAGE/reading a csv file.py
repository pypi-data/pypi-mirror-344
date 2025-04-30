import pandas as pd

df = pd.read_csv('testing data.csv')

# See the first 5 rows
print(df.head(51))
print('\n')

# print(type(df))


columns_list = df.columns.tolist()
print(columns_list)

data1 = df[columns_list[1]].tolist()
print(data1)

for elements in data1:
    if str(elements) == 'nan':
        print('not a number')