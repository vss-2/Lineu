FROM python:3.10-alpine
WORKDIR /Lineu

COPY . .

EXPOSE 5000

CMD ["/start.sh"]
