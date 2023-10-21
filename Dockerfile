FROM 3.11.6-bullseye

ADD . /data

# apt改用清华源
ADD ./sources.list /etc/apt/sources.list

WORKDIR /data

RUN apt clean && apt autoclean && rm -rf /etc/apt/sources.list.d/* && apt update -y && apt upgrade -y && apt install -y vim

RUN apt install -y libx11-xcb1 && apt install -y libsm6 libxext6  libgl1

# Pip改清华源
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

CMD ["python", "main.py"]