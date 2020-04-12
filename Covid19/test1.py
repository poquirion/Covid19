#voir https://www.latlong.net/category/provinces-40-60.html

import pgeocode
import pypostalcode
import pypostalcode
import ssl
#voir https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
ssl._create_default_https_context = ssl._create_unverified_context
nomi = pgeocode.Nominatim('ca')
#print(nomi.query_postal_code('J7E').latitude)

pcdb = pypostalcode.PostalCodeDatabase()

pc_canada = []
pc_quebec = []

#for i in pcdb.find_postalcode(province=None):
#    pc_canada.append(i)

for i in pcdb.find_postalcode(province='Quebec'):
    pc_quebec.append(i)
    print(i.postalcode)

myloc = pcdb['J7E']
print(myloc.latitude, ' ',myloc.longitude)

#print('Canada ' + str(len(pc_canada)))
#print('Quebec ' + str(len(pc_quebec)))

lat_long_file = '/data/Applications/GitScript/Covid19/LatLong.txt'

lat_long_file_handler = open(lat_long_file,'w')


lat_long_file_handler.close()


myconn = pypostalcode.ConnectionManager()
PC_FIND_ALL_PROVINCE = "SELECT distinct province from PostalCodes"
print(myconn.query(PC_FIND_ALL_PROVINCE))




