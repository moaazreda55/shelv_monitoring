# shelv_monitoring

docker build -f base.Dockerfile -t electropi_img
docker build -f app.Dockerfile -t myapp_img
docker run -p 8500:8500 --name my_cont myapp_img

