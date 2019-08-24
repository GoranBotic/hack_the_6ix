theFile=$(realpath ../Tester-7bfaa3d48b57.json)
sudo docker run --rm -p 4500:4500 -v $theFile:/code/cred.json backend