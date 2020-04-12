import pgeocode
from  pypostalcode import PostalCodeDatabase
import ssl
#voir https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
ssl._create_default_https_context = ssl._create_unverified_context
nomi = pgeocode.Nominatim('ca')
print(nomi.query_postal_code('J7E').latitude)


pcdb = PostalCodeDatabase()

pc_canada = []
pc_quebec = []

for i in pcdb.find_postalcode(province=None):
    pc_canada.append(i)

for i in pcdb.find_postalcode(province='Quebec'):
    pc_quebec.append(i)

print('Canada ' + str(len(pc_canada)))
print('Quebec ' + str(len(pc_quebec)))



