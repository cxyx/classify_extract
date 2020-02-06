#!/usr/bin/env bash
tag_suffix=$1
tag="release_offline_"${tag_suffix}
source docker/ci_docker.conf

image="dockerhub.datagrand.com/"${DEFAULT_DOCKER_NAMESPACE}"/${DOCKER_IMAGE_NAME}:"${tag}

cp -r ~/.ssh .
docker build -f docker/Dockerfile.offline -t ${image} . && docker push ${image}
rm -rf .ssh

git clone --depth=1 ssh://git@git.datagrand.com:58422/idps/idps_global.git
cat idps_global/conf/namespace/classify_extract.txt | while read project_namespace; do
    is_ignore=0
    for ignore_namespace in $IGNORE_NAMESPACE_LIST; do
        if [ $ignore_namespace == $project_namespace ]; then
            is_ignore=1
            echo "ignore namespace: "$project_namespace
            break
        fi
    done
    if [ $is_ignore != 1 ]; then
        echo "rename to namespace: "$project_namespace
        project_image="dockerhub.datagrand.com/"${project_namespace}"/${DOCKER_IMAGE_NAME}:"${tag}
        docker tag ${image} ${project_image}
        docker push ${project_image}
    fi
done
rm -rf idps_global

