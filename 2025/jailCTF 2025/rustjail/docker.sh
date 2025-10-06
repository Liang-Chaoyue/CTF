#!/bin/bash
docker build -t rustjail .
docker run -d -p 5000:5000 --privileged --name rustjail rustjail
