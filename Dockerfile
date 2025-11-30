FROM ubuntu:24.04

# idk if pip is still required but might as well
# just install python and requests library
RUN apt-get update && apt-get upgrade -y && apt install python3 python3-pip python3-requests -y

WORKDIR /bot
COPY . /bot

CMD python3 framework.py
