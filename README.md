# BigDataInnovationTeam: Incidents
*Analyzing impacts of traffic incidents on road congestion*

## Goal
Processing useful information from the City's incident logs to quantify traffic delays from incidents

### 1. Transforming incident data
Ultimately we want the following information:  
 - [ ] start time
 - [ ] end time
 - [ ] geographic location
 - [ ] type of incident
 - [ ] lane closures
 - [ ] updates for finer-grained analyses of impacts
 
### 2. Comparing with Traffic Speeds
By matching incident location and time to traffic data from 3rd party vendors and bluetooth we want to estimate 
the delay from loss of capacity due to an incident. This requires merging the incident data with traffic speed 
data as well as volume data to understand the aggregate vehicle-delay. 

## Contents 

```shell
Baseline/        # Producing baseline graphs of travel times on City Highways
csv wrangling/   # Processing incident log text
Notes/           # Literature review notes
Plotting/        # Python 
R/               # R code from previous student
User Cost/       # Quantifying user cost impacts
```
