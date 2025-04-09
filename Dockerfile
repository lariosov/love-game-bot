FROM python:3.12-slim
WORKDIR /
COPY ./req.txt ./req.txt
RUN pip install --no-cache-dir --upgrade -r req.txt
COPY ./ ./
CMD ["python3", "bot.py"]