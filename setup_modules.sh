python ./modules/dateUtils/setup.py sdist &
python ./modules/stationDatetimeUtils/setup.py sdist &
python ./modules/station/setup.py sdist &
python ./modules/stationMap/setup.py sdist
wait
echo "installing package dateUtils..."
pip install ./modules/dateUtils/dist/dateUtils-1.0.tar.gz

echo "installing package stationDatetimeUtils..."
pip install ./modules/stationDatetimeUtils/dist/stationDatetimeUtils-1.0.tar.gz

echo "installing package station..."
pip install ./modules/station/dist/station-1.0.tar.gz

echo "installing pakage stationMap..."
pip install ./modules/stationMap/dist/stationMap-1.0.tar.gz



