This server provides a minimalistic REST for KeyDB ( PostgreSQL in dev. / PostgresXL in production )

PostgreSQL is managed by the Django's models.

KeyDB has following tables:
	1. Fingerprints for storing unique ID for all the authorized systems of HCenter which are submitted by the HCenterSPOC.

	# SPOCID will be given at time of registering which will have a password associated to it

	Fingerprints use all default APIs except pyzipcode

	2. HealthCenter for storing information of a health center where users will go to sign up

	3. HCenterSPOC for storing information of SPOC. It contains a passhash which will be used to verify the SPOC whenever he is trying to register a system

	4. HCenterEmployees for storing information of Employees assigned by HCenterSPOC for work.

	Each Table contains a JSON attribute by the name of "Data" which can be used to insert some specific informations. ( Used so that we won't have to alter schema on every little change in workflow )

*** INCOMPLETE ***
