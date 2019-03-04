var descEtool1 = '<b>TransitScore Israel</b><br>The relative intensity of the transit service in Israel by location.<br>Scores are normalized to 0-100. Displayed as interactive map.<br>Click on heatmap to get score for location.<br>Useful for comparing transit service level between locations / neighborhoods within a city or town.';

var descEtool2 = '<b>Municipal TransitScore</b><br>The relative average intensity of the transit service in cities and towns in Israel.<br>Scores are normalized to 0-100. Displayed as interactive map.<br>Click on municipality to get score.<br>Useful for comparing transit service level between cities / towns.';

var descEtool3 = '<b>Municipal FairShareScore</b><br>The relative investment in transit service in cities and towns in Israel.<br>Scores are relative to the average national investment per person.<br>E.g. FairShareScore  = 100% investment similar to national average, FairShareScore  = 150% investment 50% higher than national average, FairShareScore  = 70% investment 30% lower than national average.<br>Displayed as interactive map. Click on municipality to get score.<br>Useful for comparing investment in transit service between cities / towns.';

var descEtool4 = '<b>Municipal Transit Ranking</b><br>Municipal ranking by TransitScore, FairShareScore and BuiltDensityScore displayed as charts and lists.<br>Search and sort lists by city / town name or score.<br>Use slider to zoom in on different areas of the chart.<br>Click on name or chart to highlight city / town.<br>Useful for comparing scores between cities / towns.';

var descEtool5 = '<b>Municipal trips per day (tpd) per line</b><br>Display the trips per day (tpd) for each transit line that serves a selected city or town.<br>Displayed as interactive map.<br>Click on municipality to get list of lines and tpd sorted by line frequency.<br>Useful for analyzing in detail the transit service in a city / town and for recommending improvements.';

var descEtool6 = '<b>Frequent Service Lines</b><br>Frequent service lines displayed on an interactive map.<br>Use slider to set level of service to display from 60+ trips per day (tpd) to 240+ tpd.<br>Click on map shows list of frequent lines in the area sorted by frequency.<br>Useful for analyzing what neighborhoods or cities or towns are served by high frequency service and which are not.';

var descEtool7 = '<b>Buses per day on street</b><br>A list of all the lines and their frequency on the street segment selected on a map.<br>The list is sorted by frequency and includes the total number of buses that pass through the selected street segment in a day.<br>Useful to analyze the potential benefit of a dedicated bus lane on a street.';

var descEtool8 = '<b>Accessible level of service at stops</b><br>Level of transit service accessible within walking distance from any location.<br>Displays the total number of transit opportunities per day at all stops.<br>Click on a stop to get a breakdown of all the lines at that stop sorted by their frequency.<br>Useful for analyzing what areas in a city or town do not have access to a reasonable level of service and what needs to be improved.';

var descEtool9 = '<b>Accessible level of service to and at train stations</b><br>The level of service on feeder buses near train stations and the level of service of trains at stations.<br>Also show level of transit service at any point of interest (PoI) and the level of service from this PoI to train stations.<br>Useful for analyzing the balance of feeder buses per train at train stations.<br>Also useful for analyzing the accessibility by transit of train service to neighborhoods and other locations of interest like job centers, hospitals, universities, etc…';

var descEtool10 = '<b>TransitTimeMap</b><br>Accessible area for a given duration of travel from/to a location by transit (or bike or walking).<br>Useful for analyzing access by transit to jobs, education, health services, train stops, municipal services, etc…<br>Also useful for comparing levels of  accessibility for different neighborhoods in a town or city.';

var startD = new Date(cfg_gtfsdate.slice(0,4), cfg_gtfsdate.slice(4,6)-1, cfg_gtfsdate.slice(6)); // js months are 0-11
var endD = new Date();
endD.setTime(startD.getTime() + 6*24*60*60*1000);
var servicePeriodE = '<br><br>Service Week Analyzed : '+startD.toDateString()+' to '+endD.toDateString();

var logos = '<br><br><img src="../docs/images/MIU_logo.jpg" alt="MIU logo" height="60px"><img src="../docs/images/YEE_logo.jpg" alt="YEE logo" height="60px">';

