#!/usr/bin/env bash
sh tests/environment/build_online.sh
build_status=$?
if [ $build_status -ne 0 ]
then
    echo "build dev_online image fail"
    exit 1
else
    echo "build dev_online image success"
fi

sh tests/environment/build_offline.sh
build_status=$?
if [ $build_status -ne 0 ]
then
    echo "build dev_offline image fail"
    exit 1
else
    echo "build dev_offline image success"
fi

docker ps -a | grep classify_extract_online | awk '{print $1}' | xargs -I {} docker rm -f {}
docker run -tid --name classify_extract_online  dockerhub.datagrand.com/idps/classify_extract:dev_online bash
docker exec classify_extract_online bash -c "cd /classify_extract && python tests/environment/run_test_cases.py"
test_status=$?
docker cp classify_extract_online:/classify_extract/tests/environment/TestReport.html $ROOT_PATH/TestReport.html
docker rm -f classify_extract_online
if [ $test_status -ne 0 ]
then
    echo "test job fail"
    exit 1
fi

