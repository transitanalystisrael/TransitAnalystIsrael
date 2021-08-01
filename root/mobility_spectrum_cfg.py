#sel_muni_name = "Giv'atayim"
sel_muni_name = "Rishon LeZiyyon" # RLZ

analysis_locs = [
    {'name': 'RLZ_center_HertzelxRothchild', 'loc': ['31.963961', '34.803033'] },
    {'name': 'RLZ_Azrieli_Rishonim', 'loc': ['31.949232', '34.803299'] },
    {'name': 'RLZ_Canyon_Hazahav', 'loc': ['31.990121', '34.774849'] },
    {'name': 'Moshe_Dayan_Train_Station', 'loc': ['31.987453', '34.757259'] }, 
    {'name': 'ramathahayal', 'loc': ['32.10959', '34.83878'] }, 
    {'name': 'Tel_Aviv_City_Hall', 'loc': ['32.081656', '34.781205'] }, 
    {'name': 'hashalom_Azrieli_Tel_Aviv', 'loc': ['32.073600', '34.790000'] }
]
'''
    {'name': 'RLZ_center_HertzelxRothchild', 'loc': ['31.963961', '34.803033'] },
    {'name': 'RLZ_Azrieli_Rishonim', 'loc': ['31.949232', '34.803299'] }
    {'name': 'RLZ_Canyon_Hazahav', 'loc': ['31.990121', '34.774849'] },
    {'name': 'RLZ_Ikea', 'loc': ['31.951411', '34.771101'] }, 
    {'name': 'Moshe_Dayan_Train_Station', 'loc': ['31.987453', '34.757259'] }, 
    {'name': 'Tel_Aviv_City_Hall', 'loc': ['32.081656', '34.781205'] }, 
    {'name': 'hashalom_Azrieli_Tel_Aviv', 'loc': ['32.073600', '34.790000'] }, 
    {'name': 'TAU', 'loc': ['32.11249', '34.80559'] }, 
    {'name': 'ramathahayal', 'loc': ['32.10959', '34.83878'] }, 
'''
gtfsdate1 = '20190526'
servicedate1 = '20190526'
gtfsdate2 = '20210425'
servicedate2 = '20210425'

analysis_time = '080000'

percentofarealist = ['25','50','75']

local_url = "http://localhost:9191/v1/coverage/"
munifilein = 'built_area_in_muni2017simplifyed50.geojson'

#On demand date on local pc
get_service_date = 'on_demand'

processedpath = 'processed'
mobilitypath = 'mobility'

# transit_time_map config
default_coverage_name = 'default'
secondary_custom_coverage_name = 'secondary-cov'
on_demand_coverage_prefix = 'ondemand-'

time_map_server_local_url = "http://localhost:9191/v1/coverage/"


