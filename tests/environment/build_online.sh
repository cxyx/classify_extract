cp -r ~/.ssh .
image="dockerhub.datagrand.com/idps/classify_extract:dev_online"
docker build --no-cache -f tests/environment/Dockerfile.online -t ${image} . && docker push ${image}
rm -rf .ssh
