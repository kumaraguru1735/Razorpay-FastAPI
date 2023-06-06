FROM python:3.9
#Environmental Variables
ENV RAZORPAY_KEY = RAZORPAY_KEY
ENV RAZORPAY_PASS = RAZORPAY_PASS

COPY ./requirements.txt /api/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /api/requirements.txt
COPY ./api /api
WORKDIR /api
EXPOSE 5000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]