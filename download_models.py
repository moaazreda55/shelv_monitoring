import gdown
import os

os.makedirs("models",exist_ok=True)


def download_model(file_id,name):
    # file_id = "1R5T6rIyy3hLfFbYQ7m7Z3JtJjZn1kQnT" shelv.pt
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url,f"models/{name}")


download_model("1v_e7Pssu9QLjk9M4VwampuXK5_0XZKSh","shelv.pt")
download_model("1sNVJkvPmDYym_C7WsBkfc-n04LxdtmnQ","product.pt")
# "12fv8hk5VjPAN5vjVkpgavC2PemekPq"
# "https://drive.google.com/file/d/1sNVJkvPmDYym_C7WsBkfc-n04LxdtmnQ"
# https://drive.google.com/file/d/1v_e7Pssu9QLjk9M4VwampuXK5_0XZKSh/view?usp=sharing
# https://drive.google.com/file/d/1sNVJkvPmDYym_C7WsBkfc-n04LxdtmnQ/view?usp=sharing