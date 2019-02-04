#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 27 21:16:20 2018

Working Directory:
/Users/pongtit/Documents/Hult/DD Mod A/Class Python/Team Project Python

@author: pongtit
Purpose:
    Working on Final Report Python
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

########################################################################
###### Load dataset from excel to python ##############################

file = 'world_data_hult_regions_mai.xlsx'

world_bank = pd.read_excel(file)

##############################

world_bank['Hult_Team_Regions'] = world_bank['Hult_Team_Regions'].map(
        {'Middle East & North Africa': 'ME & NAf',
         'Central Africa 2': 'CAf2',
         'Central Aftica 1':'CAf1',
         'Central Asia and some Europe': 'CAs & EU',
         'Europe': 'EU',
         'Greater Mediteranian Region': 'Med',
         'Northern Europe and Northern Americas': 'NEU & NAm',
         'Northern Latin America / Caribbean': 'NLAm & Car',
         'Nothern Asia and Northern Pacific': 'NAs & NP',
         'Southern Africa': 'SAf',
         'Southern Asia and Southern Pacific': 'SAs & SP',
         'Southern Latin America / Caribbean': 'SLAm & Car',
         'World': 'World'
               })

########################################################################
###### Create sub dataset to compare each regions of the world #########
########################################################################
    

middle_east = world_bank[world_bank['Hult_Team_Regions'] == 'ME & NAf']

central_africa2 = world_bank[world_bank['Hult_Team_Regions'] == 'CAf2']

central_africa1 = world_bank[world_bank['Hult_Team_Regions'] == 'CAf1']

central_asia_europe = world_bank[world_bank['Hult_Team_Regions'] == 'CAs & EU']

europe = world_bank[world_bank['Hult_Team_Regions'] == 'EU']

mediteranian = world_bank[world_bank['Hult_Team_Regions'] == 'Med']

europe_na = world_bank[world_bank['Hult_Team_Regions'] == 'NEU & NAm']

north_latin_carib = world_bank[world_bank['Hult_Team_Regions'] == 'NLAm & Car']

north_asia_pacific = world_bank[world_bank['Hult_Team_Regions'] == 'NAs & NP']

south_africa = world_bank[world_bank['Hult_Team_Regions'] == 'SAf']

south_asia_pacific = world_bank[world_bank['Hult_Team_Regions'] == 'SAs & SP']

south_latin_carib = world_bank[world_bank['Hult_Team_Regions'] == 'SLAm & Car']

world = world_bank[world_bank['Hult_Team_Regions'] == 'World']

### Find percentage of missing value of each region to the world

print(central_africa1.isnull().sum().sum()/(central_africa1.isnull().sum().sum()+central_africa1.count().sum()))

print(central_africa2.isnull().sum().sum()/(central_africa2.isnull().sum().sum()+central_africa2.count().sum()))

print(central_asia_europe.isnull().sum().sum()/(central_asia_europe.isnull().sum().sum()+central_asia_europe.count().sum()))

print(middle_east.isnull().sum().sum()/(middle_east.isnull().sum().sum()+middle_east.count().sum()))

print(europe.isnull().sum().sum()/(europe.isnull().sum().sum()+europe.count().sum()))

print(mediteranian.isnull().sum().sum()/(mediteranian.isnull().sum().sum()+mediteranian.count().sum()))

print(europe_na.isnull().sum().sum()/(europe_na.isnull().sum().sum()+europe_na.count().sum()))

print(north_latin_carib.isnull().sum().sum()/(north_latin_carib.isnull().sum().sum()+north_latin_carib.count().sum()))

print(north_asia_pacific.isnull().sum().sum()/(north_asia_pacific.isnull().sum().sum()+north_asia_pacific.count().sum()))

print(south_africa.isnull().sum().sum()/(south_africa.isnull().sum().sum()+south_africa.count().sum()))

print(south_asia_pacific.isnull().sum().sum()/(south_asia_pacific.isnull().sum().sum()+south_asia_pacific.count().sum()))

print(south_latin_carib.isnull().sum().sum()/(south_latin_carib.isnull().sum().sum()+south_latin_carib.count().sum()))

print(world.isnull().sum().sum()/(world.isnull().sum().sum()+world.count().sum()))

# Compare average in every region and middle east to see what is interesting

print(middle_east.mean())
print(central_africa2.mean())
print(central_africa1.mean())
print(central_asia_europe.mean())
print(europe.mean())
print(mediteranian.mean())
print(europe_na.mean())
print(north_latin_carib.mean())
print(north_asia_pacific.mean())
print(south_africa.mean())
print(south_asia_pacific.mean())
print(south_latin_carib.mean())
print(middle_east.count())

####### Create boxplot to see difference in our dataset 

####### Create dictionaries for y lable and title

mydict = {'access_to_electricity_pop': 'Access to electricity population',
          'access_to_electricity_rural': 'Access to electricity rural',
          'access_to_electricity_urban': 'Access to eletricity urban',
          'CO2_emissions_per_capita)': 'CO2_emissions_per_capita',
          'compulsory_edu_yrs': 'Compulsory Education',
          'pct_female_employment': 'Female Employment',
          'pct_male_employment': 'Male Employment',
          'pct_agriculture_employment': 'Argriculture Employment',
          'pct_industry_employment': 'Industry Employment',
          'pct_services_employment': 'Services Employment',
          'exports_pct_gdp': 'Export to GDP',
          'fdi_pct_gdp': 'FDI to GDP',
          'gdp_usd': 'GDP',
          'gdp_growth_pct': 'GDP Growth',
          'incidence_hiv': 'HIV incidence',
          'internet_usage_pct': 'Internet usage',
          'homicides_per_100k': 'Homicides',
          'adult_literacy_pct': 'Adult literacy',
          'child_mortality_per_1k': 'Children mortality',
          'avg_air_pollution': 'Average air pollution',
          'women_in_parliament': 'Women in parliament',
          'tax_revenue_pct_gdp': 'Tax revenue to GDP',
          'unemployment_pct': 'Unemployment Rate',
          'urban_population_pct': 'Urban population',
          'urban_population_growth_pct': 'Urban population Growth rate'
          }

ylabeldict = {'access_to_electricity_pop': '% of population',
              'access_to_electricity_rural': '% of population',
              'access_to_electricity_urban': '% of population',
              'CO2_emissions_per_capita)': 'metric ton per capita',
              'compulsory_edu_yrs': 'years',
              'pct_female_employment': '% of female employment',
              'pct_male_employment': '% of male employment',
              'pct_agriculture_employment': '% of total employment',
              'pct_industry_employment': '% of total employment',
              'pct_services_employment': '% of total employment',
              'exports_pct_gdp': '% of GDP',
              'fdi_pct_gdp': '% of GDP',
              'gdp_usd': 'ten trillion USD',
              'gdp_growth_pct': 'annual %',
              'incidence_hiv': '% population ages 15-49',
              'internet_usage_pct': '% of population',
              'homicides_per_100k': 'per 100k',
              'adult_literacy_pct': '% of people ages 15 and above',
              'child_mortality_per_1k': 'per 1k live births',
              'avg_air_pollution': 'micro gram per cubic meter',
              'women_in_parliament': '% of parliamentary seats',
              'tax_revenue_pct_gdp': '% of GDP',
              'unemployment_pct': '% of total labor force',
              'urban_population_pct': '% of total',
              'urban_population_growth_pct': 'annual %'
              }    

#######
    
palet = {"CAf2": "b",
          "CAf1": "b",
          "CAs & EU":"b",
          "EU":"b",
          "Med":"b",
          "ME & NAf":"r",
          "NEU & NAm":"b",
          "NLAm & Car":"b",
          "NAs & NP":"b",
          "SAf":"b",
          "SAs & SP":"b",
          "SLAm & Car":"b",
          "World":"y"
          }
    
    
slice = world_bank.iloc[:,5:]
    
column_number = 25

while column_number > 1: 
    
    for column in slice:
        plt.subplots(figsize = (10,10))
        sns.boxplot(x = world_bank['Hult_Team_Regions'],
                    y = world_bank[column],
                    palette = palet,
                    boxprops = dict(alpha = 0.3),
                    showmeans = True,
                    meanline = True
                    )
        plt.xticks(rotation=90)
        plt.axhline(y=middle_east[column].mean(),
                    linestyle = '--')
        plt.xlabel('')
        plt.rc('xtick', labelsize = 12)
        plt.rc('ytick', labelsize = 12)
        plt.rc('axes', titlesize = 14)
        plt.rc('figure', titlesize = 25)
        plt.title(mydict[column])
        plt.ylabel(ylabeldict[column])
        plt.tight_layout()
        plt.savefig(mydict[column])
        plt.show()
    
        column_number = column_number - 1
        
    else:
        break


##############################################################################
####### See outliers of our data set ########################################

middle_east.describe()

column_number = 25

while column_number > 1: 

    for cname in slice:
    
        middle_east.boxplot(column = [cname])
        plt.title(mydict[cname])
        plt.savefig(mydict[cname])
        plt.show()
        
    else:
        break
    

##############################################################################
######## Impute our missing data ############################################

print(middle_east.isnull().any())

print(middle_east.isnull().sum())

middle_east['CO2_emissions_per_capita)'].isnull().astype(int).sort_values()
    
for element in middle_east:
    
    print(element)
    
    if middle_east[element].isnull().any():
        middle_east['m_'+element] = middle_east[element].isnull().astype(int)


CO_2 = middle_east['CO2_emissions_per_capita)']
print(CO_2.skew())
CO_2 = CO_2.dropna()
sns.distplot(CO_2,
             bins = 'fd',
             color = 'blue')

CO_2_limit = 45

plt.xlabel('CO2 per Capita')
plt.title('Carbon Dioxide per Capita')

plt.axvline(x = CO_2_limit,
            linestyle = '--',
            color = 'r'
            )
plt.show

# Skewed so we use median

compul = middle_east['compulsory_edu_yrs']
print(compul.skew())
compul = compul.dropna()
sns.distplot(compul,
             bins = 'fd',
             color = 'blue')

compul_limit_hi = 13
compul_limit_low = 6

plt.xlabel('Compulsory education (Year)')
plt.title('Compulsory education years')

plt.axvline(x = compul_limit_hi,
            linestyle = '--',
            color = 'red'
            )
plt.axvline(x = compul_limit_low,
            linestyle = '--',
            color = 'red'
            )
plt.savefig('Compulsory education years.png', dpi = 500)
plt.show

# Normal distribution so we used mean

export = middle_east['exports_pct_gdp']
print(export.skew())
export = export.dropna()
sns.distplot(export,
             bins = 'fd',
             color = 'blue')

exp_limit = 100

plt.xlabel('Export to GDP (%)')
plt.title('Percentage of export to GDP')

plt.axvline(x = exp_limit,
            linestyle = '--',
            color = 'red'
            )

plt.show

# Skewed so we use median

fdi = middle_east['fdi_pct_gdp']
print(fdi.skew())
fdi = fdi.dropna()
sns.distplot(fdi,
             bins = 'fd',
             color = 'blue')

fdi_limit = 6

plt.xlabel('FDI to GDP (%)')
plt.title('Percentage of Foreign Direct Investment to GDP')

plt.axvline(x = fdi_limit,
            linestyle = '--',
            color = 'red'
            )

plt.show

# skewed so we use median

gdp = middle_east['gdp_usd']
print(gdp.skew())
gdp = gdp.dropna()
sns.distplot(gdp,
             bins = 'fd',
             color = 'b')

plt.show

# Skewed so we use median

growth = middle_east['gdp_growth_pct']
print(growth.skew())
growth = growth.dropna()
sns.distplot(growth,
             bins = 'fd',
             color = 'b')

gdp_growth_limit_hi = 5
gdp_growth_limit_low = -1

plt.xlabel('GDP Growth (%)')
plt.title('Percentage of GDP Growth')

plt.axvline(x = gdp_growth_limit_hi,
            linestyle = '--',
            color = 'red'
            )

plt.axvline(x = gdp_growth_limit_low,
            linestyle = '--',
            color = 'red'
            )

plt.savefig('Percentage of GDP Growth.png', dpi = 500)

plt.show

# Skewed so we use median

hiv = middle_east['incidence_hiv']
print(hiv.skew())
hiv = hiv.dropna()
sns.distplot(hiv,
             bins = 'fd',
             color = 'b')

plt.show

# Skewed so we use median

parlia = middle_east['women_in_parliament']
print(parlia.skew())
parlia = parlia.dropna()
sns.distplot(parlia,
             bins = 'fd',
             color = 'b')
plt.xlabel('Women in parliament')
plt.title('Women in parliament')

plt.savefig('Women in parliament.png.', dpi = 500)

plt.show

# Normal so we use mean

################## Graph for presentation ###########################

plt.subplot(2,2,1)
compul = middle_east['compulsory_edu_yrs']
print(compul.skew())
compul = compul.dropna()
sns.distplot(compul,
             bins = 'fd',
             color = 'lightblue')

compul_limit_hi = 13
compul_limit_low = 6

plt.xlabel('Compulsory education (Year)')
plt.title('Compulsory education years')

plt.axvline(x = compul_limit_hi,
            linestyle = '--',
            color = 'red'
            )
plt.axvline(x = compul_limit_low,
            linestyle = '--',
            color = 'red'
            )

plt.subplot(2,2,2)

parlia = middle_east['women_in_parliament']
print(parlia.skew())
parlia = parlia.dropna()
sns.distplot(parlia,
             bins = 'fd',
             color = 'lightgreen')
plt.xlabel('Women in parliament')
plt.title('Women in parliament')

plt.subplot(2,2,3)

growth = middle_east['gdp_growth_pct']
print(growth.skew())
growth = growth.dropna()
sns.distplot(growth,
             bins = 'fd',
             color = 'b')

gdp_growth_limit_hi = 5
gdp_growth_limit_low = -1

plt.xlabel('GDP Growth (%)')
plt.title('Percentage of GDP Growth')

plt.axvline(x = gdp_growth_limit_hi,
            linestyle = '--',
            color = 'red'
            )

plt.axvline(x = gdp_growth_limit_low,
            linestyle = '--',
            color = 'red'
            )

plt.subplot(2,2,4)

CO_2 = middle_east['CO2_emissions_per_capita)']
print(CO_2.skew())
CO_2 = CO_2.dropna()
sns.distplot(CO_2,
             bins = 'fd',
             color = 'grey')

CO_2_limit = 45

plt.xlabel('CO2 per Capita')
plt.title('Carbon Dioxide per Capita')

plt.axvline(x = CO_2_limit,
            linestyle = '--',
            color = 'r'
            )
plt.show


plt.tight_layout()
plt.savefig('presentation.png', dpi=500)
plt.show()

##############################################################################
###### Impute Data with our assumption above #################################

##### Impute compulsory with mean first

ME_fix = pd.DataFrame.copy(middle_east)

compul_mean = ME_fix['compulsory_edu_yrs'].mean()

ME_fix['compulsory_edu_yrs'] = (ME_fix['compulsory_edu_yrs'].fillna(compul_mean)
                                .round(0))

women_mean = ME_fix['women_in_parliament'].mean()

ME_fix['women_in_parliament'] = (ME_fix['women_in_parliament'].fillna(women_mean)
                                .round(0))

##### Impute the rest of data with median

for col in ME_fix:
    if ME_fix[col].isnull().any():
        col_median = ME_fix[col].median()
        ME_fix[col] = (ME_fix[col].fillna(col_median))
        
ME_fix = ME_fix.iloc[:,1:30]

ME_fix = ME_fix.drop('homicides_per_100k', axis = 1)
ME_fix = ME_fix.drop('adult_literacy_pct', axis = 1)
ME_fix = ME_fix.drop('tax_revenue_pct_gdp', axis = 1)

##############################################################################
##### Remove data which has NA more than our acceptable number ##############

# We decided to drop column which has missing values more than 60% of total 
# data since it is not make sense to use mean or median to fix it.
# Note that each country has difference characteristic.
# We combined low income and lower middle income together because in our
# dataset we have only 2 countries in low income and it could not make correlation
# In additional, it is not making senses if we cut our 2 data row out        

ME_high = ME_fix[ME_fix.income_group == 'High income']
ME_upper_middle = ME_fix[ME_fix.income_group == 'Upper middle income']
ME_low = ME_fix[ME_fix.income_group == 'Low income'] & ME_fix[ME_fix.income_group == 'Lower middle income']

High_cor = ME_high.corr().round(2)
High_cor.to_excel('High_cor.xlsx', index=True)

Upper_cor = ME_upper_middle.corr().round(2)
Upper_cor.to_excel('Upper_cor.xlsx', index=True)

Low_cor = ME_low.corr().round(2)
Low_cor.to_excel('low_cor.xlsx', index=True)

# Find mean in each region

sns.heatmap(High_cor, 
            cmap ='Blues',
            square = True,
            annot = False,
            linecolor = 'black',
            linewidths = 0.5)

plt.show()

#### Create pie chart

labels = 'Industry', 'Services', 'Agricultural'
sizes = [middle_east['pct_industry_employment'].mean(),
         middle_east['pct_services_employment'].mean(),
         middle_east['pct_agriculture_employment'].mean()]
colors = ['black', 'red', 'green']
explode = (0.1,0,0)

plt.pie(sizes, explode = explode, labels = labels, colors = colors,
        shadow = True, startangle = 140)

plt.axis('equal')
plt.savefig('piechart.png')
plt.show()

# Find correlation for high income group

high_inc = High_cor.iloc[[3],3:]
high = high_inc.sort_values(by = 'CO2_emissions_per_capita)', axis = 1)
myheat = high.iloc[:,:18]
myheat.columns = ['Service employment',
                  'Women in parliament',
                  'Compulsory education',
                  'Unemployment rate',
                  'GDP growth',
                  'FDI/GDP',
                  'Female employment',
                  'Export/GDP',
                  'Male employment',
                  'Agricultural employment',
                  'GDP',
                  'Child mortality',
                  'Urban population',
                  'Urban population growth',
                  'Internet usage',
                  'Air pollution',
                  'Industry employment',
                  'CO2 emissions',
                  ]

sns.heatmap(myheat, 
            cmap ='Blues',
            square = True,
            annot = False,
            linecolor = 'black',
            linewidths = 0.5)
plt.savefig('heatmap.png', dpi = 500)
plt.show()

#### Correlation for presentation

present_corr = pd.DataFrame.copy(ME_high)

present_corr = present_corr[present_corr.country_name != 'Bahrain']
present_corr = present_corr[present_corr.country_name != 'Isarael']
present_corr = present_corr[present_corr.country_name != 'Malta']
present_corr = present_corr[present_corr.country_name != 'Oman']

present_corr = present_corr.loc[:,['CO2_emissions_per_capita)','avg_air_pollution']]

mycor = present_corr.corr().round(2)
mycor.rename(columns = {'CO2_emissions_per_capita)':'CO2','avg_air_pollution':'Avg. air pollution'},
             index={'CO2_emissions_per_capita)':'CO2','avg_air_pollution':'Avg. air pollution'},
             inplace = True)
sns.heatmap(mycor, cmap = 'Oranges', annot = True)
