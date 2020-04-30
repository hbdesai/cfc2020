# cfc2020
An application for the COVID-19 Treatment Global Clinical Trials - Implementation and access details.

These sets of files for an application to show on Google map the locations of COVID-19 Treatment Global Trials. The clinical trial data is downloaded from NIH's Clinical Trial site. To get full set of data including the address the data has to be downloaded, their API response only provides limited data, and does not include location address nor the longitude and latitude data. For now worked around it with a manual step to download to a file. Using python script geocode-addresses.py we embed the latitude and longitude data using Google's Geocoding APIs. The GeocodedLocations is a cache of previously geocoded addresses which are used for processing daily updated data file after downloading. 

Command to geocode a newly downloaded data file is:
>python geocode-addresses.py SearchResults.xml ClinicalTrialsData.xml t

where SearchResults.xml is a newly downloaded data file as input
      ClinicalTrialsData.xml is the output file with geocoded addresses
      t (true for logging)

The ClinicalTrialsData.xml is manually uploaded on the Cloud object storage bucket. (Currently to IBM COS bucket and AWS S3 bucket)

IBM Cloud Hosting -
<br>URL: https://s3.us-east.cloud-object-storage.appdomain.cloud/cfc2020-covid-19-treatment-global-clinical-trials/locations.html

Additionally (AWS Cloud Hosting) -
<br>URL: https://cfc2020.s3.us-east-2.amazonaws.com/c19d-atf/globalclinicaltrials/locations.html
