twitter.zip: hills.txt twython requests
	zip -r twitter.zip *

hills.txt:
	curl http://geonames.usgs.gov/docs/stategaz/NationalFile_20160401.zip | funzip | gawk 'BEGIN {FS="|"} $$2 ~ /\<Hill\>/ && $$3 == "Summit" {print} NR==1 {print}' > hills.txt

twython:
	pip install twython -t .

requests:
	pip install requests -t .
