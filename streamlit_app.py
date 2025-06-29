import streamlit as st
from PIL import Image
import numpy as np
import cv2
from ultralytics import YOLO


SHELF_MODEL_PATH = "models/shelv.pt"
PRODUCT_MODEL_PATH = "models/product.pt"


shelf_model = YOLO(SHELF_MODEL_PATH)
product_model = YOLO(PRODUCT_MODEL_PATH)


st.title("Shelf & Product Detector App")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])


if uploaded_file:
    
    image = Image.open(uploaded_file).convert("RGB")
    image_np = np.array(image)
    output_img = image_np.copy()

    
    shelf_result = shelf_model(image_np)
    product_result = product_model(image_np)

    
    shelf_polys = shelf_result[0].obb.xyxyxyxy.cpu().numpy() if shelf_result[0].obb else []
    product_boxes = product_result[0].boxes.xyxy.cpu().numpy() if product_result[0].boxes else []

    product_widths = [box[2] - box[0] for box in product_boxes]
    avg_product_width = np.mean(product_widths) if product_widths else 0
    product_count = 0

    shelf_analysis = []

    for i, poly in enumerate(shelf_polys):
        shelf_num = i + 1
        polygon = poly.reshape((-1, 1, 2)).astype(np.int32)

        
        x_coords = poly[:, 0]
        y_coords = poly[:, 1]
        min_x, max_x = x_coords.min(), x_coords.max()
        min_y, max_y = y_coords.min(), y_coords.max()
        shelf_width = max_x - min_x

        
        cv2.polylines(output_img, [polygon], isClosed=True, color=(255, 0, 0), thickness=22)
        cv2.putText(output_img, f"Shelf {shelf_num}", (int(min_x), int(min_y - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), thickness=21)

        
        shelf_products = []
        total_product_width = 0

        for box in product_boxes:
            x1, y1, x2, y2 = box
            prod_mid_y = (y1 + y2) / 2
            if min_y <= prod_mid_y <= max_y:
                shelf_products.append(box)
                product_count += 1

                
                pt1 = tuple(box[:2].astype(int))
                pt2 = tuple(box[2:].astype(int))
                cv2.rectangle(output_img, pt1, pt2, color=(0, 255, 0), thickness=22)

                
                box_width = x2 - x1
                total_product_width += box_width

        
        free_space = max(shelf_width - total_product_width, 0)
        est_extra_products = int(free_space / avg_product_width) if avg_product_width > 0 else 0

        shelf_analysis.append({
            "Shelf": shelf_num,
            "Products on shelf": len(shelf_products),
            "Shelf width (px)": round(shelf_width, 1),
            "Used width (px)": round(total_product_width, 1),
            "Free width (px)": round(free_space, 1),
            "Avg product width (px)": round(avg_product_width, 1),
            "Est. extra products": est_extra_products
        })

    
    st.image(output_img, caption="📦 Shelves (Blue), Products (Green), Labels (White)", use_container_width=True)

    
    st.markdown("### 🧠 Shelf Capacity Analysis")
    st.write(f"🗄️ **Total Shelves Detected**: `{len(shelf_polys)}`")
    st.write(f"📦 **Total Products Detected**: `{product_count}`")
    st.write(f"📐 **Average Product Width**: `{round(avg_product_width, 1)} px`")

    for s in shelf_analysis:
        st.markdown(f"**Shelf {s['Shelf']}**")
        st.write(f"- Products on shelf: `{s['Products on shelf']}`")
        st.write(f"- Shelf width: `{s['Shelf width (px)']} px`")
        st.write(f"- Used width: `{s['Used width (px)']} px`")
        st.write(f"- Free width: `{s['Free width (px)']} px`")
        st.write(f"- Estimated extra products that can fit: `{s['Est. extra products']}`")
        st.markdown("---")


