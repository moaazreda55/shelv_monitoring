# shelv_monitoring

docker build -f base.Dockerfile -t electropi_img .
docker build -f app.Dockerfile -t app_img .
docker run -p 8501:8501 --name my_container app_img 

