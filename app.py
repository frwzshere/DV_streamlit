import streamlit as st
import altair as alt
import pandas as pd

#####################################
#######   Initial Layout   ##########
#####################################

st.set_page_config(layout="wide")




#####################################
###########   Layout    #############
#####################################

# h1 title
style_h1 = """
<style>
#unveiling-the-evolution-eu-gender-equality-in-10-years {
    text-align: center;
    font-size: 50px; 
    background-color: purple;
    color: white;
}
</style>
"""

# 使用Markdown显示样式化标题
st.markdown(style_h1, unsafe_allow_html=True)
st.markdown("<h1>Unveiling the Evolution : EU Gender Equality in 10 Years</h1>", unsafe_allow_html=True)


# blank
st.write(" ")
st.write(" ")
st.write(" ")
st.write(" ")




#####################################
##########   PART  1    #############
#####################################

# Load Data #
# Gender Equality Index 性别平等指数导入
index_file = pd.ExcelFile('/Users/wangjiuduo/Desktop/DV2/index_file.xlsx')  # Update with the correct file path

# Creating a dictionary to hold dataframes
dfs = {}
for sheet_name in index_file.sheet_names:
    df = pd.read_excel(index_file, sheet_name=sheet_name, usecols=['Index year', 'Gender Equality Index', 'Country'])
    dfs[sheet_name] = df

# Merging dataframes and renaming columns
index_all = pd.concat(dfs.values(), axis=0)
index_all = index_all.rename(columns={'Index year': 'year', 'Gender Equality Index': 'Equality_Index'})
index_all['year'] = index_all['year'].astype(str)

# Ensure unique_years is defined
unique_years = sorted(index_all['year'].unique())

# Filtering EU data
index_eu = index_all[index_all['Country'] == 'EU']

# Assuming the data has been loaded into `index_all` as done previously
# Make sure to filter for EU only data for the line chart
index_eu = index_all[index_all['Country'] == 'EU']

# Find the min and max of the Gender Equality Index to set the y-axis domain for the EU data
min_index = index_eu['Equality_Index'].min()
max_index = index_eu['Equality_Index'].max()

# Create the selection interval for the EU index chart
brush = alt.selection_interval(encodings=['x'], name="brush")

# Create the EU index chart with interval selection and dots
eu_index_chart = alt.Chart(index_eu).mark_line(point=True, color="purple").encode(
    x='year:O',
    y=alt.Y('Equality_Index:Q', scale=alt.Scale(domain=(min_index-2, max_index+2))),
    tooltip=['year', 'Equality_Index']
).properties(
    title='EU Gender Equality Index Over Time',
    width=750,
    height=550
).add_selection(brush)

# Create the ranking chart that will show the average index per country with gradient colors
# The tooltip will display the average index and country
ranking_chart = alt.Chart(index_all).transform_filter(
    brush
).transform_aggregate(
    average_index='mean(Equality_Index)',
    groupby=['Country']
).mark_bar().encode(
    x=alt.X('average_index:Q', title='Average Gender Equality Index'),
    y=alt.Y('Country:N', sort=alt.EncodingSortField(field="average_index", order="descending"), title='Country'),
    color=alt.condition(
        alt.datum.Country == 'EU',  # If the country is EU
        alt.value('red'),  # Use the contrasting color for EU
        alt.Color('average_index:Q', scale=alt.Scale(scheme='purples', domain=[45, 85]))  
    ),
    tooltip=['Country:N', 'average_index:Q']
).properties(
    width=300,
    height=560,
    title='Gender Equality Index Ranking'
)

# Combine the two charts horizontally
part1 = alt.hconcat(eu_index_chart, ranking_chart).resolve_scale(color='independent')


# H2 title
style_h2 = """
<style>
#eu-gender-equality-at-a-glance {
    text-align: center;
    font-size: 35px;
    text-align: left;
    color: purple;
}
</style>
"""
st.markdown(style_h2, unsafe_allow_html=True)
st.markdown("<h2>EU Gender Equality at A Glance</h2>", unsafe_allow_html=True)

# Display the charts using Streamlit
st.altair_chart(part1, use_container_width=True)

st.write(" ")
st.write(" ")
st.write(" ")
st.write(" ")
st.write(" ")


#####################################
##########   PART  2    #############
#####################################

# H2 title
style_h2 = """
<style>
#eu-gender-equality-at-a-glance {
    text-align: center;
    font-size: 35px;
    text-align: left;
    color: purple;
}
</style>
"""
st.markdown(style_h2, unsafe_allow_html=True)
st.markdown("<h2>EU Gender Equality at A Glance</h2>", unsafe_allow_html=True)

countryname_mapping = {
    'BE': 'Belgium',
    'BG': 'Bulgaria',
    'CZ': 'Czech Republic',
    'DK': 'Denmark',
    'DE': 'Germany',
    'EE': 'Estonia',
    'IE': 'Ireland',
    'EL': 'Greece',
    'ES': 'Spain',
    'FR': 'France',
    'HR': 'Croatia',
    'IT': 'Italy',
    'CY': 'Cyprus',
    'LV': 'Latvia',
    'LT': 'Lithuania',
    'LU': 'Luxembourg',
    'HU': 'Hungary',
    'MT': 'Malta',
    'NL': 'Netherlands',
    'AT': 'Austria',
    'PL': 'Poland',
    'PT': 'Portugal',
    'RO': 'Romania',
    'SI': 'Slovenia',
    'SK': 'Slovakia',
    'FI': 'Finland',
    'SE': 'Sweden'
}

# country name dictionary
country_mapping = {
    'BE': 56,
    'BG': 100,
    'CZ': 203,
    'DK': 208,
    'DE': 276,
    'EE': 233,
    'IE': 372,
    'EL': 300,
    'ES': 724,
    'FR': 250,
    'HR': 191,
    'IT': 380,
    'CY': 196,
    'LV': 428,
    'LT': 440,
    'LU': 442,
    'HU': 348,
    #'MT': 'Malta',
    'NL': 528,
    'AT': 40,
    'PL': 616,
    'PT': 620,
    'RO': 642,
    'SI': 705,
    'SK': 703,
    'FI': 246,
    'SE': 752
}

# Creating a dictionary to hold dataframes
dfs = {}
for sheet_name in index_file.sheet_names:
    df = pd.read_excel(index_file, sheet_name=sheet_name, usecols=['Index year', 'WORK', 'Country'])
    dfs[sheet_name] = df

# Merging dataframes and renaming columns
work_all = pd.concat(dfs.values(), axis=0)
work_all = work_all.rename(columns={'Index year': 'year', 'WORK': 'WORK'})
work_all['year'] = work_all['year'].astype(str)

# Ensure unique_years is defined
unique_years_works = sorted(work_all['year'].unique())

# Filtering EU data
work_eu = work_all[work_all['Country'] == 'EU']

work_all['id'] = work_all['Country'].map(country_mapping)
work_all['CountryName'] = work_all['Country'].map(countryname_mapping)
work_all['rank'] = work_all.groupby(['year'])['WORK'].rank(method='min', ascending=False)

work_min = work_all['WORK'].min()
work_max = work_all['WORK'].max()
import pandas as pd
import altair as alt
from vega_datasets import data

# 创建地图
world_map = alt.topo_feature(data.world_110m.url, 'countries')

# 创建地图图表
map_chart_work = alt.Chart(world_map).mark_geoshape(
    stroke='black'
).encode(
    color=alt.Color('WORK:Q', scale=alt.Scale(scheme='purples')),
    tooltip=['Country:N', 'CountryName:N', 'WORK:Q', 'rank:Q']
).transform_lookup(
    lookup='id',
    from_=alt.LookupData(data=work_all, key='id', fields=['Country', 'CountryName', 'WORK', 'rank'])
).project(
    type='mercator',
    clipExtent= [[300, 0], [800, 600]]
).properties(width=600, 
             height=600,
             title='Work Index'
)


# 添加选择交互
select_country = alt.selection_point(fields=['Country'], empty=False, value='EU')
map_chart_work = map_chart_work.add_params(select_country)

# 创建柱状图
bar_chart_work = alt.Chart(work_all).mark_bar(color='lavender').encode(
    x='year:N',
    y=alt.Y('WORK:Q', title='WORK Index', scale=alt.Scale(domain=[work_min-5, work_max+5], clamp=True)),
    #color='year:N',
    tooltip=['Country:N', 'year:N', 'WORK:Q']
).transform_filter(
    select_country
)

# 创建线图
line_chart_work = alt.Chart(work_all).mark_line(point=True, color='purple').encode(
    x='year:N',
    y=alt.Y('rank:Q', axis=alt.Axis(title='Country Rank'), scale=alt.Scale(domain=[30, 0])),
    #color='year:N',
    tooltip=['Country:N', 'year:N', 'rank:Q']
).transform_filter(
    select_country
)

country_chart_work = (bar_chart_work + line_chart_work).resolve_scale(
    y='independent'  
).properties(
    width=400,
    height=300
)

# 组合图表
part2_work = alt.hconcat(map_chart_work, country_chart_work) 

# 在properties()中应用图例的配置
part2_work = part2_work.properties(
    config=alt.Config(legend=alt.LegendConfig(orient='left'))
)


## MONEY


# Creating a dictionary to hold dataframes
dfs = {}
for sheet_name in index_file.sheet_names:
    df = pd.read_excel(index_file, sheet_name=sheet_name, usecols=['Index year', 'MONEY', 'Country'])
    dfs[sheet_name] = df

# Merging dataframes and renaming columns
money_all = pd.concat(dfs.values(), axis=0)
money_all = money_all.rename(columns={'Index year': 'year', 'MONEY': 'MONEY'})
money_all['year'] = money_all['year'].astype(str)

# Ensure unique_years is defined
unique_years_money = sorted(money_all['year'].unique())

# Filtering EU data
money_eu = money_all[money_all['Country'] == 'EU']

money_all['id'] = money_all['Country'].map(country_mapping)
money_all['CountryName'] = money_all['Country'].map(countryname_mapping)
money_all['rank'] = money_all.groupby(['year'])['MONEY'].rank(method='min', ascending=False)

money_min = money_all['MONEY'].min()
money_max = money_all['MONEY'].max()
import pandas as pd
import altair as alt
from vega_datasets import data

# 创建地图
world_map = alt.topo_feature(data.world_110m.url, 'countries')

# 创建地图图表
map_chart_money = alt.Chart(world_map).mark_geoshape(
    stroke='black'
).encode(
    color=alt.Color('MONEY:Q', scale=alt.Scale(scheme='purples')),
    tooltip=['Country:N', 'CountryName:N', 'MONEY:Q', 'rank:Q']
).transform_lookup(
    lookup='id',
    from_=alt.LookupData(data=money_all, key='id', fields=['Country', 'CountryName', 'MONEY', 'rank'])
).project(
    type='mercator',
    clipExtent= [[300, 0], [800, 600]]
).properties(width=600, 
             height=600,
             title='MONEY Index'
)

# 添加选择交互
select_country = alt.selection_point(fields=['Country'], empty=False, value='EU')
map_chart_money = map_chart_money.add_params(select_country)

# 创建柱状图
bar_chart_money = alt.Chart(money_all).mark_bar(color='lavender').encode(
    x='year:N',
    y=alt.Y('MONEY:Q', title='MONEY Index', scale=alt.Scale(domain=[money_min-5, money_max+5], clamp=True)),
    tooltip=['Country:N', 'year:N', 'MONEY:Q']
).transform_filter(
    select_country
)

# 创建线图
line_chart_money = alt.Chart(money_all).mark_line(point=True, color='purple').encode(
    x='year:N',
    y=alt.Y('rank:Q', axis=alt.Axis(title='Country Rank'), scale=alt.Scale(domain=[30, 0])),
    #color='year:N',
    tooltip=['Country:N', 'year:N', 'rank:Q']
).transform_filter(
    select_country
)

country_chart_money = (bar_chart_money + line_chart_money).resolve_scale(
    y='independent'  
).properties(
    width=400,
    height=300
)

# 组合图表
part2_money = alt.hconcat(map_chart_money, country_chart_money).properties(
    config=alt.Config(legend=alt.LegendConfig(orient='left'))
)


## KNOWLEDGE

# Creating a dictionary to hold dataframes
dfs = {}
for sheet_name in index_file.sheet_names:
    df = pd.read_excel(index_file, sheet_name=sheet_name, usecols=['Index year', 'KNOWLEDGE', 'Country'])
    dfs[sheet_name] = df

# Merging dataframes and renaming columns
knowledge_all = pd.concat(dfs.values(), axis=0)
knowledge_all = knowledge_all.rename(columns={'Index year': 'year', 'KNOWLEDGE': 'KNOWLEDGE'})
knowledge_all['year'] = knowledge_all['year'].astype(str)

# Ensure unique_years is defined
unique_years_knowledge = sorted(knowledge_all['year'].unique())

# Filtering EU data
knowledge_eu = knowledge_all[knowledge_all['Country'] == 'EU']

knowledge_all['id'] = knowledge_all['Country'].map(country_mapping)
knowledge_all['CountryName'] = knowledge_all['Country'].map(countryname_mapping)
knowledge_all['rank'] = knowledge_all.groupby(['year'])['KNOWLEDGE'].rank(method='min', ascending=False)

knowledge_min = knowledge_all['KNOWLEDGE'].min()
knowledge_max = knowledge_all['KNOWLEDGE'].max()
import pandas as pd
import altair as alt
from vega_datasets import data

# 创建地图
world_map = alt.topo_feature(data.world_110m.url, 'countries')

# 创建地图图表
map_chart_knowledge = alt.Chart(world_map).mark_geoshape(
    stroke='black'
).encode(
    color=alt.Color('KNOWLEDGE:Q', scale=alt.Scale(scheme='purples')),
    tooltip=['Country:N', 'CountryName:N', 'KNOWLEDGE:Q', 'rank:Q']
).transform_lookup(
    lookup='id',
    from_=alt.LookupData(data=knowledge_all, key='id', fields=['Country', 'CountryName', 'KNOWLEDGE', 'rank'])
).project(
    type='mercator',
    clipExtent= [[300, 0], [800, 600]]
).properties(width=600, 
             height=600,
             title='KNOWLEDGE Index'
)

# 添加选择交互
select_country = alt.selection_point(fields=['Country'], empty=False, value='EU')
map_chart_knowledge = map_chart_knowledge.add_params(select_country)

# 创建柱状图
bar_chart_knowledge = alt.Chart(knowledge_all).mark_bar(color='lavender').encode(
    x='year:N',
    y=alt.Y('KNOWLEDGE:Q', title='KNOWLEDGE Index', scale=alt.Scale(domain=[knowledge_min-5, knowledge_max+5], clamp=True)),
    tooltip=['Country:N', 'year:N', 'KNOWLEDGE:Q']
).transform_filter(
    select_country
)

# 创建线图
line_chart_knowledge = alt.Chart(knowledge_all).mark_line(point=True, color='purple').encode(
    x='year:N',
    y=alt.Y('rank:Q', axis=alt.Axis(title='Country Rank'), scale=alt.Scale(domain=[30, 0])),
    #color='year:N',
    tooltip=['Country:N', 'year:N', 'rank:Q']
).transform_filter(
    select_country
)

country_chart_knowledge = (bar_chart_knowledge + line_chart_knowledge).resolve_scale(
    y='independent'  
).properties(
    width=400,
    height=300
)

# 组合图表
part2_knowledge = alt.hconcat(map_chart_knowledge, country_chart_knowledge).properties(
    config=alt.Config(legend=alt.LegendConfig(orient='left'))
)


## TIME
# Creating a dictionary to hold dataframes
dfs = {}
for sheet_name in index_file.sheet_names:
    df = pd.read_excel(index_file, sheet_name=sheet_name, usecols=['Index year', 'TIME', 'Country'])
    dfs[sheet_name] = df

# Merging dataframes and renaming columns
time_all = pd.concat(dfs.values(), axis=0)
time_all = time_all.rename(columns={'Index year': 'year', 'TIME': 'TIME'})
time_all['year'] = time_all['year'].astype(str)

# Filtering EU data
time_eu = time_all[time_all['Country'] == 'EU']

time_all['id'] = time_all['Country'].map(country_mapping)
time_all['CountryName'] = time_all['Country'].map(countryname_mapping)
time_all['rank'] = time_all.groupby(['year'])['TIME'].rank(method='min', ascending=False)

time_min = time_all['TIME'].min()
time_max = time_all['TIME'].max()
import pandas as pd
import altair as alt
from vega_datasets import data

# 创建地图
world_map = alt.topo_feature(data.world_110m.url, 'countries')

# 创建地图图表
map_chart_time = alt.Chart(world_map).mark_geoshape(
    stroke='black'
).encode(
    color=alt.Color('TIME:Q', scale=alt.Scale(scheme='purples')),
    tooltip=['Country:N', 'CountryName:N', 'TIME:Q', 'rank:Q']
).transform_lookup(
    lookup='id',
    from_=alt.LookupData(data=time_all, key='id', fields=['Country', 'CountryName', 'TIME', 'rank'])
).project(
    type='mercator',
    clipExtent= [[300, 0], [800, 600]]
).properties(width=600, 
             height=600,
             title='TIME Index'
)

# 添加选择交互
select_country = alt.selection_point(fields=['Country'], empty=False, value='EU')
map_chart_time = map_chart_time.add_params(select_country)

# 创建柱状图
bar_chart_time = alt.Chart(time_all).mark_bar(color='lavender').encode(
    x='year:N',
    y=alt.Y('TIME:Q', title='TIME Index', scale=alt.Scale(domain=[time_min-5,time_max+5], clamp=True)),
    tooltip=['Country:N', 'year:N', 'TIME:Q']
).transform_filter(
    select_country
)

# 创建线图
line_chart_time = alt.Chart(time_all).mark_line(point=True, color='purple').encode(
    x='year:N',
    y=alt.Y('rank:Q', axis=alt.Axis(title='Country Rank'), scale=alt.Scale(domain=[30, 0])),
    #color='year:N',
    tooltip=['Country:N', 'year:N', 'rank:Q']
).transform_filter(
    select_country
)

country_chart_time = (bar_chart_time + line_chart_time).resolve_scale(
    y='independent'  
).properties(
    width=400,
    height=300
)

# 组合图表
part2_time = alt.hconcat(map_chart_time, country_chart_time).properties(
    config=alt.Config(legend=alt.LegendConfig(orient='left'))
)

## POWER
# Creating a dictionary to hold dataframes
dfs = {}
for sheet_name in index_file.sheet_names:
    df = pd.read_excel(index_file, sheet_name=sheet_name, usecols=['Index year', 'POWER', 'Country'])
    dfs[sheet_name] = df

# Merging dataframes and renaming columns
power_all = pd.concat(dfs.values(), axis=0)
power_all = power_all.rename(columns={'Index year': 'year', 'POWER': 'POWER'})
power_all['year'] = power_all['year'].astype(str)

# Filtering EU data
power_eu = power_all[power_all['Country'] == 'EU']

power_all['id'] = power_all['Country'].map(country_mapping)
power_all['CountryName'] = power_all['Country'].map(countryname_mapping)
power_all['rank'] = power_all.groupby(['year'])['POWER'].rank(method='min', ascending=False)

power_min = power_all['POWER'].min()
power_max = power_all['POWER'].max()
import pandas as pd
import altair as alt
from vega_datasets import data

# 创建地图
world_map = alt.topo_feature(data.world_110m.url, 'countries')

# 创建地图图表
map_chart_power = alt.Chart(world_map).mark_geoshape(
    stroke='black'
).encode(
    color=alt.Color('POWER:Q', scale=alt.Scale(scheme='purples')),
    tooltip=['Country:N', 'CountryName:N', 'POWER:Q', 'rank:Q']
).transform_lookup(
    lookup='id',
    from_=alt.LookupData(data=power_all, key='id', fields=['Country', 'CountryName', 'POWER', 'rank'])
).project(
    type='mercator',
    clipExtent= [[300, 0], [800, 600]]
).properties(width=600, 
             height=600,
             title='POWER Index'
)

# 添加选择交互
select_country = alt.selection_point(fields=['Country'], empty=False, value='EU')
map_chart_power = map_chart_power.add_params(select_country)

# 创建柱状图
bar_chart_power = alt.Chart(power_all).mark_bar(color='lavender').encode(
    x='year:N',
    y=alt.Y('POWER:Q', title='POWER Index', scale=alt.Scale(domain=[power_min-5,power_max+5], clamp=True)),
    tooltip=['Country:N', 'year:N', 'POWER:Q']
).transform_filter(
    select_country
)

# 创建线图
line_chart_power = alt.Chart(power_all).mark_line(point=True, color='purple').encode(
    x='year:N',
    y=alt.Y('rank:Q', axis=alt.Axis(title='Country Rank'), scale=alt.Scale(domain=[30, 0])),
    #color='year:N',
    tooltip=['Country:N', 'year:N', 'rank:Q']
).transform_filter(
    select_country
)

country_chart_health = (bar_chart_power + line_chart_power).resolve_scale(
    y='independent'  
).properties(
    width=400,
    height=300
)

# 组合图表
part2_power = alt.hconcat(map_chart_power, country_chart_health).properties(
    config=alt.Config(legend=alt.LegendConfig(orient='left'))
)

## HEALTH
# Creating a dictionary to hold dataframes
dfs = {}
for sheet_name in index_file.sheet_names:
    df = pd.read_excel(index_file, sheet_name=sheet_name, usecols=['Index year', 'HEALTH', 'Country'])
    dfs[sheet_name] = df

# Merging dataframes and renaming columns
health_all = pd.concat(dfs.values(), axis=0)
health_all = health_all.rename(columns={'Index year': 'year', 'HEALTH': 'HEALTH'})
health_all['year'] = health_all['year'].astype(str)

# Filtering EU data
health_eu = health_all[health_all['Country'] == 'EU']

health_all['id'] = health_all['Country'].map(country_mapping)
health_all['CountryName'] = health_all['Country'].map(countryname_mapping)
health_all['rank'] = health_all.groupby(['year'])['HEALTH'].rank(method='min', ascending=False)

health_min = health_all['HEALTH'].min()
health_max = health_all['HEALTH'].max()
import pandas as pd
import altair as alt
from vega_datasets import data

# 创建地图
world_map = alt.topo_feature(data.world_110m.url, 'countries')

# 创建地图图表
map_chart_health = alt.Chart(world_map).mark_geoshape(
    stroke='black'
).encode(
    color=alt.Color('HEALTH:Q', scale=alt.Scale(scheme='purples')),
    tooltip=['Country:N', 'CountryName:N', 'HEALTH:Q', 'rank:Q']
).transform_lookup(
    lookup='id',
    from_=alt.LookupData(data=health_all, key='id', fields=['Country', 'CountryName', 'HEALTH', 'rank'])
).project(
    type='mercator',
    clipExtent= [[300, 0], [800, 600]]
).properties(width=600, 
             height=600,
             title='HEALTH Index'
)

# 添加选择交互
select_country = alt.selection_point(fields=['Country'], empty=False, value='EU')
map_chart_health = map_chart_health.add_params(select_country)

# 创建柱状图
bar_chart_health = alt.Chart(health_all).mark_bar(color='lavender').encode(
    x='year:N',
    y=alt.Y('HEALTH:Q', title='HEALTH Index', scale=alt.Scale(domain=[health_min-5,health_max+5], clamp=True)),
    tooltip=['Country:N', 'year:N', 'HEALTH:Q']
).transform_filter(
    select_country
)

# 创建线图
line_chart_health = alt.Chart(health_all).mark_line(point=True, color='purple').encode(
    x='year:N',
    y=alt.Y('rank:Q', axis=alt.Axis(title='Country Rank'), scale=alt.Scale(domain=[30, 0])),
    #color='year:N',
    tooltip=['Country:N', 'year:N', 'rank:Q']
).transform_filter(
    select_country
)

country_chart_health = (bar_chart_health + line_chart_health).resolve_scale(
    y='independent'  
).properties(
    width=400,
    height=300
)

# concat
part2_health = alt.hconcat(map_chart_health, country_chart_health).properties(
    config=alt.Config(legend=alt.LegendConfig(orient='left'))
)


# dropdown
# 设置字体大小为20px
selectbox_style = """
<style>
p {
    font-size: 22px !important;
}
</style>
"""

# 将 CSS 样式应用到页面中
st.markdown(selectbox_style, unsafe_allow_html=True)

# 显示 selectbox
option = st.selectbox(
    'Choose A Dimension to Dive in:',
    ['WORK', 'MONEY', 'KNOWLEDGE', 'TIME', 'POWER', 'HEALTH']
)


# 定义显示图表的函数
def display_chart(dimension):
    if dimension == 'WORK':
        st.altair_chart(part2_work, use_container_width=True)
    elif dimension == 'MONEY':
        st.altair_chart(part2_money, use_container_width=True)
    elif dimension == 'KNOWLEDGE':
        st.altair_chart(part2_knowledge, use_container_width=True)
    elif dimension == 'TIME':
        st.altair_chart(part2_time, use_container_width=True)
    elif dimension == 'POWER':
        st.altair_chart(part2_power, use_container_width=True)
    elif dimension == 'HEALTH':
        st.altair_chart(part2_health, use_container_width=True)

# 显示图表
display_chart(option)


#####################################
##########   PART  3    #############
#####################################

# H2 title
style_h2 = """
<style>
#croatia-you-may-not-know {
    text-align: center;
    font-size: 35px;
    text-align: left;
    color: purple;
}
</style>
"""
st.markdown(style_h2, unsafe_allow_html=True)
st.markdown("<h2>Croatia You May Not Know ...</h2>", unsafe_allow_html=True)




#####################################
###########   Outro    ##############
#####################################

ty_column = st.columns([1])
ty_note = st.columns([1])[0]
ty_note.metric(label="Thank you for making Gender Equality forward", value="", delta="1 more step")



#####################################
###########   Export    #############
#####################################


