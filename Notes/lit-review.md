# Incidents Literature Review

Topics:
 1. Transportation Incident Delay
 2. Spectral Analysis
 3. Timeseries Transportation analysis
 4. Transportation Road Reliability Metrics
 
## 1. Transportation Incident Delay

### Wood, Daniel Alden: A Framework for Measuring Passenger-Experienced Transit Reliability Using Automated Data.
*Wood, Daniel Alden. “A Framework for Measuring Passenger-Experienced Transit Reliability Using Automated Data.” Massachusetts Institute of Technology, 2015. http://dspace.mit.edu/handle/1721.1/99539.*

Reliability traditionally measured from an operational/not customer perspective, differences: 
> 1. Operational reliability is based on timetable adherence, whereas passenger reliability is based on travel time variability.
> 2. Operational reliability is usually measured at the route or line-level, whereas passenger reliability is experienced at the origin-destination pair level.
> 3. Passenger reliability is experienced for the entire journey, but operational measures capture only portions of the journey.

Reliability performance metric should enable:
1. incident identification
2. cross-facility comparison
3. analysis over time (before-after and trend)
4. capture sources of unreliability

Metric design objectives (Chapter 4):
1. Representative of the Passenger Experience
  - Include all sources of unreliability
  - Control for variation in passenger behaviour
  - Control for time of Day Variation in Average Travel Time
  - Exclude “Extreme” Delays (ex: 1 in 100 trips)
  - Calculated at OD-Pair Level
  - No Bias towards Particular Passenger Demographics
2.  Meaningful for Passengers and Non-Experts
  - Understandable (1 what value physically represents 2 how value relates to a journey)
  - Objective
  - Useful for planning journeys ("future focused", predict future performance)
3.  Comparable Across Different Services and Times of Day
  - Independent of local physical attributes (ex: scheduled journey time)
  - Absolute, not relative: reliability on Service A should represent same quality of service on Service B
4. Time Period Flexibility
  - Interval (time of day) and Period (Sample size/ day categories) flexibility
5. Scope Flexibility
  - Ability to recalculate metric for differing elements of service: OD, facility, trip segment
  
Reliability Buffer Time:
> Difference between the *N*th and 50th percentile (i.e. median) passenger travel times over a specific OD pair and time period

Why Median?
 - insensitive to outliers or the right tail of the distribution
 - median travel time  is  a  better  predictor  of  passenger behavior than the mean

Evaluation (pp. 57-59)



#### Follow Up
**RBT**
 - [ ] Joanne Chan. “Rail Transit OD Matrix Estimation and Journey Time Reliability Metrics Using Automated Fare Data Matrix”. MA thesis. Massachusetts Institute of Technology, 2007.
 - [ ] David Uniman. “Service Reliability Measurement Framework using Smart Card Data: Application to the London Underground”. MA thesis. Massachusetts Institute of Technology, 2009.  
 - [ ] Terence C Lam and Kenneth A Small. “The value of time and reliability: measurement from a value pricing experiment”. In: Transportation Research Part E: Logistics and Transportation Review 37.2 (2001), pp. 231–251
 
**Auto TT reliability**
 - [ ] John Bates et al. “The valuation of reliability for personal travel”. In: Transportation Research Part E: Logistics and Transportation Review 37.2 (2001), pp. 191–229.  
 - [X] Tim Lomax et al. “Selecting travel reliability measures”. In: Texas Transportation
Institute monograph (May 2003) (2003).
 - [x] Office of Operations Federal Highway Administration. Travel Time Reliability: Making It There On Time, All The Time. 2013. url: http://ops.fhwa.dot.gov/publications/tt_reliability/brochure/.

**Metric design**  
- [ ] Mark Abkowitz et al. Transit Service Reliability. Tech. rep. U.S. Dept. of Transportation, 1978.

## Lomax, Tim, and R. Margiotta. Selecting Travel Reliability Measures. 
http://lyle.smu.edu/emis/cmmi5/Ibarra/DeskTop/White_Papers/Reliability/Travel_Reliability.pdf
### Intro
>The terms “recurring” and “non-recurring” congestion are misnomers—variations in weather, traffic volume and a range of other factors can be termed “recurring” but have traditionally been included outside the “regular” congestion label. 

#### What Components should be included?
>Trip planning decisions can be informed by data that is targeted for the expected variation in travel time at their usual departure time. Measures that might be useful would typically focus on specific trip patterns or corridors and specific hours of the day—areawide or subregional measures grouped in long time blocks would be less useful for this purpose.  System or corridor evaluations, however, might be best identified with hour-to-hour, day-to-day and annual trend information. 

### Developing an approach

>**Traffic volume and speed will not be representative under some circumstances**—
During 
incident conditions, for example, vehicles leave the freeway and use alternate routes.  This 
not only results in fewer vehicles being counted
 by the monitoring systems, it also means the 
delay that those vehicles experience is not counted.  And since the diverted vehicles often use 
routes that are typically congested, the addition of those trips can mean significantly greater 
than normal delays.  In addition, some quality 
control procedures eliminate very low speed 
data due to accuracy problems with the detectors when speeds are below 5 mph. 

### Measure Overview

p14