FROM electropi_img:latest

WORKDIR /app

COPY . .

RUN python download_models.py

CMD [ "streamlit" ,"run","streamlit_app.py"]