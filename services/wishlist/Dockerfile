FROM python:3-slim
WORKDIR /usr/src/app/services/wishlist
COPY services/wishlist/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY services/wishlist/wishlist.py .
CMD [ "python", "wishlist.py" ]

