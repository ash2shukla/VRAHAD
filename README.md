docker start KeyDB
docker start SessionDB

Start Niraadhaar server @ 8001

VRAHAD-> DB and REST-> KeyServer-> PostgresREST8000-> python manage.py runserver 8000
VRAHAD-> DB and REST-> SessionServer-> RedisServer8002 -> python manage.py runserver 8002
VRAHAD-> DB and REST-> python bioSampleServer.py 0.0.0.0:5000
VRAHAD-> Signup -> python manage.py runserver 9000

To demonstrate -


0. Connect Internet then Create Hotspot on Mobile and Connect Laptop on it.

1. Open browser go to http://localhost:9000
2. Enter TEST_EID, TEST_PASS
3. You will receive OTP on Mobile.
4. Enter OTP on Web Page do not submit.
5. Open BioSample App and Scan thumb there.
6. Submit.

7. Enter Aadhaar number 123456789012
8. Enter OTP
9. Open BioSample App and Scan thumb there and Submit

## EPGA-Init runs in VRAHAD-> DB and REST-> KeyServer-> PostgresREST8000-> HCenter-> views.py
