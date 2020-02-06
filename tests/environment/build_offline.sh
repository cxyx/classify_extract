cp -r ~/.ssh .
image="dockerhub.datagrand.com/idps/classify_extract:dev_offline"
docker build --no-cache -f tests/environment/Dockerfile.offline -t ${image} . && docker push ${image}
rm -rf .ssh
