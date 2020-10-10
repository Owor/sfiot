#FROM phusion/baseimage:0.10.1
From debian:stretch



# ...put your own build instructions here...
WORKDIR /app
COPY ./socket_lib /app/socket_lib
COPY ./lora-sx1276 /app/lora-sx1276


# install debian packages
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update -qq \
 && apt-get install --no-install-recommends -y \
    openssh-client \
    python3 \
    python3-dev \
    python3-pip \
    python3-setuptools \
    python3-virtualenv \
    python3-wheel \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*


# RUN pip3 install pandas

# RUN apt-get update  
# RUN apt-get install nano
# #RUN sudo -H pip3 install pandas
# RUN apt-get install net-tools
# RUN apt-get install procps -y

WORKDIR /app/socket_lib
CMD ["python3","script.py","in"," port"]