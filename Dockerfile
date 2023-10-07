FROM python:3.11.5

ADD . /data

WORKDIR /data

# 只能改清华源了，不然速度太慢了。
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

CMD ["python", "main.py"]