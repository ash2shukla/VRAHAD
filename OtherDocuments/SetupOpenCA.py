from OpenCA import *
# Create OpenCA ROOT
createCA('root','OpenCA-ROOT','OpenCA-ROOT-pass',{'C':'IN','O':'OpenCA','OU':'ROOT','ST':'Uttar-Pradesh','L':'Ghaziabad','CN':'ROOT@OpenCA'})

# Create Intermedaite CAs
createCA('int','NirAadhaar-INT-CA','NirAadhaar-INT-CA-pass',{'C':'IN','O':'NirAadhaar','OU':'INT-CA','ST':'Uttar-Pradesh','L':'Ghaziabad','CN':'NirAadhaar-INT-CA@OpenCA-ROOT'})
createCA('int','Vrahad-INT-CA','Vrahad-INT-CA-pass',{'C':'IN','O':'Vrahad','OU':'INT-CA','ST':'Uttar-Pradesh','L':'Ghaziabad','CN':'Vrahad-INT-CA@OpenCA-ROOT'})

# Certify the Intermedaite CAs by OpenCA ROOT
signReqCA('OpenCA-ROOT','Vrahad-INT-CA','OpenCA-ROOT-pass','ca')
signReqCA('OpenCA-ROOT','NirAadhaar-INT-CA','OpenCA-ROOT-pass','ca')

# Create CSR for ASA (Vrahad ASA)
createCSR('Vrahad-SVR-ASA','Vrahad-SVR-ASA-pass',{'C':'IN','O':'Vrahad','OU':'ASA','ST':'Uttar-Pradesh','L':'Ghaziabad','CN':'Vrahad-SVR-ASA@NirAadhaar-INT-CA'})

# Certify the ASA
signReqCA('NirAadhaar-INT-CA','Vrahad-SVR-ASA.csr.pem','NirAadhaar-INT-CA-pass','svr')

# Create CSR for AUA (HealthCenter) ( TEST_CENTER AUA )
createCSR('TEST_CENTER-AUA','TEST_CENTER-AUA-pass',{'C':'IN','O':'Vrahad','OU':'HealthCenter','ST':'Uttar-Pradesh','L':'Ghaziabad','CN':'TEST_CENTER-AUA@NirAadhaar-INT-CA'})

# Certify the AUA
signReqCA('NirAadhaar-INT-CA','TEST_CENTER-AUA.csr.pem','NirAadhaar-INT-CA-pass','usr')

# Rename to
# USER.cert.pem -> TEST_CENTER-AUA-USER.cert.pem
# SERVER.cert.pem -> VRAHAD-SVR-ASA-SERVER.cert.pem
