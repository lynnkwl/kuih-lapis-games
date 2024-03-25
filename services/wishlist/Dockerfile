FROM python:3-slim
WORKDIR /usr/src/app
COPY ./services/wishlist/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python", "./wishlist.py" ]