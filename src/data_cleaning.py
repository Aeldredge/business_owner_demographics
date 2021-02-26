import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

data07 = pd.read_csv('~/Documents/dsi/capstone/capstone1/data/2007/2007_slim_data.csv')
data12 = pd.read_csv('~/Documents/dsi/capstone/capstone1/data/2012/2012_data.csv')
data17 = pd.read_csv('~/Documents/dsi/capstone/capstone1/data/2017/2017_data.csv')

def clean(data, year):
    if year == 2007:
        data07 = data
        data07['year'] = 2007
        data07['year'] = pd.to_numeric(data07['year'])
        data07['race1'] = data07['race'].str.slice(stop=1)
        data07['race2'] = data07['race'].str.slice(start=1).str.strip()
        pst_data07 = data07[data07['sector'] == 54]
        pst_df07 = pst_data07.groupby(['race1', 'race2','ethnicity','sex']).agg({'sector':'count'})
        percent07 = pst_df07.groupby(level=0).apply(lambda x: 100 * x / float(sum(pst_df07['sector'])))
        percent07.rename(columns={'sector':'percent'},inplace=True)
        out = percent07
    elif year == 2012:
        df12 = data.groupby(['RACE_GROUP_TTL', 'ETH_GROUP_TTL','SEX_TTL']).agg({'FIRMALL':'sum'})
        df12.rename(columns={'FIRMALL':'count'},inplace=True)
        df12.drop(index='Meaning of Race code',inplace=True)
        df12['count'] = pd.to_numeric(df12['count'])
        df12['percent'] = 100 * (df12['count'] / df12.iloc[0,0])
        percent12 = df12.sort_values('percent',ascending=False)
        out = percent12
    elif year == 2017:
        data17 = data[1:]
        data17['OWNPDEMP'].replace({'D':'1'}, inplace=True)
        data17['OWNPDEMP'] = pd.to_numeric(data17['OWNPDEMP'])
        data17 = data17[data17['OWNCHAR_LABEL'] == 'Total reporting']
        data17 = data17[data17['OWNER_RACE_LABEL'] != 'Minority']
        data17 = data17[data17['OWNER_RACE_LABEL'] != 'Nonminority']
        data17 = data17[data17['OWNER_VET_LABEL'] == 'All owners of respondent firms']
        df17 = data17.groupby(['OWNER_RACE_LABEL', 'OWNER_ETH_LABEL','OWNER_SEX_LABEL']).agg({'OWNPDEMP':'sum'})
        df17.rename(columns={'OWNPDEMP':'count'},inplace=True)
        df17['percent'] = 100 * (df17['count'] / df17.iloc[0,0])
        percent17 = df17.sort_values('percent',ascending=False)
        out = percent17
    return out

 
def demographic(demo, year):
    if year == 2007:
        data = data07
        if demo == 'race':
            race07 = clean(data, year).groupby(level=0).agg({'percent':'sum'})
            race07.sort_values('percent',ascending=False,inplace=True)
            race07.reset_index(inplace=True)
            race07.rename(columns={'race1':'race'},inplace=True)
            race07['race'] = np.array(['White','Asian','Black or African American','American Indian and Alaska Native', 'Some other race', 'Native Hawaiian and Other Pacific Islander'])
            out = race07
        elif demo == 'ethnicity':
            eth07 = clean(data, year).groupby(level=2).agg({'percent':'sum'})
            eth07.sort_values('percent',ascending=False,inplace=True)
            eth07.reset_index(inplace=True)
            eth07['ethnicity'] = np.array(['Non-Hispanic','Hispanic'])
            out = eth07
        elif demo == 'sex':
            sex07 = clean(data, year).groupby(level=3).agg({'percent':'sum'})
            sex07.sort_values('percent',ascending=False,inplace=True)
            sex07.reset_index(inplace=True)
            sex07['sex'] = np.array(['Male','Female'])
            out = sex07
        else:
            out = 'Invalid demographic input.  Valid inputs: \'race\', \'ethnicity\', or \'sex\''
        return out
    elif year == 2012:
        data = data12
        if demo == 'race':
            consolidate12 = clean(data, year)[1:].drop(index='All firms',level=0)
            consolidate12 = consolidate12[1:].drop(index='All firms',level=1)
            race12 = consolidate12.groupby(level=0).agg({'percent':'sum'})
            race12.sort_values('percent',ascending=False,inplace=True)
            race12.reset_index(inplace=True)
            race12.rename(columns={'RACE_GROUP_TTL':'race'},inplace=True)
            out = race12
        elif demo == 'ethnicity':
            eth12 = clean(data, year)[1:].drop(index='All firms',level=1)
            eth12.reset_index(inplace=True)
            eth12 = eth12[eth12['RACE_GROUP_TTL'] == 'All firms']
            eth12 = eth12[eth12['SEX_TTL'] == 'All firms']
            eth12 = eth12[eth12['ETH_GROUP_TTL'].isin(['Non-Hispanic', 'Hispanic'])]
            eth12 = eth12.drop(columns=['RACE_GROUP_TTL','SEX_TTL','count']).rename(columns={'ETH_GROUP_TTL':'ethnicity'})
            out = eth12
        elif demo == 'sex':
            sex12 = clean(data, year)[1:].drop(index='All firms',level=2)
            sex12 = sex12.loc[('All firms','All firms')]
            sex12 = sex12[1:].drop(columns='count')
            sex12.reset_index(inplace=True)
            sex12.rename(columns={'SEX_TTL':'sex'},inplace=True)
            sex12 = sex12[:2]
            sex12['sex'] = np.array(['Male','Female'])
            out = sex12
        else:
            out = 'Invalid demographic input.  Valid inputs: \'race\', \'ethnicity\', or \'sex\''
        return out
    elif year == 2017:
        data = data17
        if demo == 'race':
            consolidate17 = clean(data, year)[1:].drop(index='All owners of respondent firms',level=0)
            race17 = consolidate17.drop(index='Male',level=2)
            race17 = race17.drop(index='Female',level=2)
            race17 = race17.reset_index()
            race17 = race17.drop(columns=['OWNER_ETH_LABEL','OWNER_SEX_LABEL', 'count']).rename(columns={'OWNER_RACE_LABEL':'race'})
            out = race17
        elif demo == 'ethnicity':
            eth17 = clean(data, year)[1:].drop(index='All owners of respondent firms',level=1)
            eth17.reset_index(inplace=True)
            eth17 = eth17.drop(columns=['count','OWNER_RACE_LABEL']).rename(columns={'OWNER_ETH_LABEL':'ethnicity'})
            eth17 = eth17[eth17['OWNER_SEX_LABEL'] == 'All owners of respondent firms']
            eth17 = eth17.drop(columns='OWNER_SEX_LABEL')
            out = eth17
        elif demo == 'sex':
            sex17 = clean(data, year)[1:].drop(index='All owners of respondent firms',level=2)
            sex17 = sex17.loc[('All owners of respondent firms','All owners of respondent firms')]
            sex17.reset_index(inplace=True)
            sex17 = sex17.drop(columns='count').rename(columns={'OWNER_SEX_LABEL':'sex'})
            out = sex17
        else:
            out = 'Invalid demographic input.  Valid inputs: \'race\', \'ethnicity\', or \'sex\''
        return out
    else:
        out = 'Invalid year input.  Valid inputs: 2007, 2012, or 2017'
    return out


if __name__ == '__main__':

    # print(demographic('demo', year))
    print(demographic('sex', 2012))