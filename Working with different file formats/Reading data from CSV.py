import piplite
await piplite.install(['seaborn', 'lxml', 'openpyxl'])
import pandas as pd

from pyodide.http import pyfetch

filename = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0101EN-SkillsNetwork/labs/Module%205/data/addresses.csv"

async def download(url, filename):
    response = await pyfetch(url)
    if response.status == 200:
        with open(filename, "wb") as f:
            f.write(await response.bytes())

await download(filename, "addresses.csv")

df = pd.read_csv("addresses.csv", header=None)

#Adding column name to the DataFrame
df.columns =['First Name', 'Last Name', 'Location ', 'City','State','Area Code']
df

#Selecting a single column
df["First Name"]

#Selecting multiple columns
df = df[['First Name', 'Last Name', 'Location ', 'City','State','Area Code']]
df

#Selecting rows using .iloc and .loc
# To select the first row
df.loc[0]

# To select the 0th,1st and 2nd row of "First Name" column only
df.loc[[0,1,2], "First Name" ]

# To select the 0th,1st and 2nd row of "First Name" column only
df.iloc[[0,1,2], 0]

#Transform Function in Pandas
#import library
import pandas as pd
import numpy as np

#creating a dataframe
df=pd.DataFrame(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]), columns=['a', 'b', 'c'])
df

#applying the transform function
df = df.transform(func = lambda x : x + 10)
df

result = df.transform(func = ['sqrt'])
result



