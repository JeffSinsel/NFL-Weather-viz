import re
import pandas as pd

unclean = pd.read_csv('unclean.csv')

#removing data without scores
unclean = unclean.rename(columns = {'Unnamed: 0' : 'week', '0': 'data' })

#cleaning data before seperation
unclean['data'] = unclean['data'].str.replace('\n','',regex=False) 
unclean['data'] = unclean['data'].str.replace('\t','',regex=False)
unclean['data'] = unclean['data'].str.replace('Final|:',' Final:',regex=False)
unclean['data'] = unclean['data'].str.replace(' +',' ',regex=True)
unclean['data'] = unclean['data'].str.replace('|Details|','',regex=False)
unclean['data'] = unclean['data'].str.replace('||','',regex=False) 
unclean['data'] = unclean['data'].str.replace('\w+\|','',regex=True)
unclean['data'] = unclean['data'].astype(str)

#seperating the games
unclean['data'] = unclean['data'].str[2:]
unclean['data'] = unclean['data'].str.split('|')
for i in range(16):
    unclean['game'+str(i+1)] = unclean['data'].str[i]

#reorganized games back into induvidual rows
unclean.drop('data',axis=1,inplace=True)
unclean = pd.melt(unclean, id_vars='week', var_name='game', value_name='game_data')
unclean = unclean[unclean['game_data'].notna()].reset_index()
unclean.drop('index',axis=1,inplace=True)
unclean.drop('game',axis=1,inplace=True)

#seperate week and year
unclean['week'] = unclean['week'].str.split('|')
unclean['year'] = unclean.week.str[0]
unclean['week'] = unclean.week.str[1]

#seperate away team
unclean['game_data'] = unclean['game_data'].str.split('@')
unclean['away_team'] = unclean['game_data'].str[0]
unclean['game_data'] = unclean['game_data'].str[1]

#seperate home team and scores
unclean['game_data'] = unclean['game_data'].str.split('  ')
unclean['home_and_score'] = unclean['game_data'].str[0]
unclean['game_data'] = unclean['game_data'].str[1]
unclean['home_and_score'] = unclean['home_and_score'].str.split('-')
unclean['home_score'] = unclean['home_and_score'].str[-1]
unclean['home_and_score'] = unclean['home_and_score'].str[0]
unclean['home_and_score'] = unclean['home_and_score'].str.split('Final:')
unclean['home_team'] = unclean['home_and_score'].str[0]
unclean['away_score'] = unclean['home_and_score'].str[-1]
unclean.drop('home_and_score',axis=1,inplace=True)

#seperate weather
unclean['game_data'] = unclean['game_data'].str.split('.')
unclean['wind'] = unclean['game_data'].str[-1]
unclean['wind'] = unclean['wind'].str.split(' ')
unclean['wind_dir'] = unclean['wind'].str[-1]
unclean['wind'] = unclean['wind'].str[0]
unclean['temperature'] = unclean['game_data'].str[0]
unclean['game_data'] = unclean['game_data'].str[0:2]
unclean['temperature'] = unclean['temperature'].str.split(' ')
unclean['temperature'] = unclean['temperature'].str[0]
unclean['game_data'] = unclean['game_data'].str[0] + unclean['game_data'].str[1]

#special cases
unclean['home_team'][2771] = 'Steelers'
unclean['away_score'][2771] = '17'
unclean['temperature'][2532] = '51' #had two tempuratues listed 
unclean['temperature'][1216] = '53'

#remove incomplete data
unclean = unclean[unclean['temperature'].notna()].reset_index()
unclean.drop('index',axis=1,inplace=True)

# clean up the columns, add total score, and add dtypes
unclean['away_score'] = unclean['away_score'].str.replace(' +','',regex=True)
unclean = unclean[unclean['away_score'] != ''].reset_index()
unclean.drop('index',axis=1,inplace=True)
unclean['away_score'] = unclean['away_score'].astype(int)

unclean['home_score'] = unclean['home_score'].str.replace('NFL','') 
unclean['home_score'] = unclean['home_score'].str.replace(' +','',regex=True)
unclean = unclean[unclean['home_score'].notna()].reset_index()
unclean.drop('index',axis=1,inplace=True)

unclean['home_score'] = unclean['home_score'].astype(int)
unclean['total_score'] = unclean['home_score'] + unclean['away_score']

unclean = unclean[unclean['total_score'].notna()].reset_index()
unclean.drop('index',axis=1,inplace=True)

unclean['temperature'] = unclean['temperature'].str.replace('f','')
unclean['temperature'] = unclean['temperature'].str.replace('DOME','70') #domes are assumed to be 70 degrees
unclean['temperature'] = unclean['temperature'].astype(int)

unclean['wind'] = unclean['wind'].str.replace('(DOME)|0|m','',regex=True)
unclean['wind'] = unclean['wind'].str.replace('\d+f','',regex=True)
unclean['wind'][739] = ''
unclean['wind'] = unclean['wind'].mask(unclean['wind']=='')

unclean['wind_dir'] = unclean['wind_dir'].str.replace('\W','',regex=True)

unclean['week'] = unclean['week'].str.replace('Week ','',regex=False)

unclean['home_team'] = unclean['home_team'].str.replace(' ','',regex=True)

unclean['year'] = unclean['year'].astype("Int64")
unclean['week'] = unclean['week'].astype("Int64")
unclean['wind'] = unclean['wind'].astype("Int64")

#rename/order columns
cols=['year','week','total_score','temperature','home_team','home_score','away_team','away_score','wind','wind_dir']
unclean=unclean[cols]
print(unclean.head())
#creates csv from clean data
unclean.to_csv('clean.csv')