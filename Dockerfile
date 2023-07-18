FROM debian:latest

RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get install -y texlive-full

# Breaking this apart because texlive-full takes a long time
RUN apt-get install -y poppler-utils python3 python3-pip python3-venv git curl \
    && rm /usr/lib/python3*/EXTERNALLY-MANAGED \
    && useradd -m latexhub \
    && mkdir /app /app/build /app/repos \
    && chown -R latexhub:latexhub /app

USER latexhub
WORKDIR /app/latexhub
COPY . .

RUN pip3 install -Ur requirements.txt

CMD ["python3", "-m", "flask", "--app", "src/app.py", "run", "--host", "0.0.0.0", "--port", "54321"]