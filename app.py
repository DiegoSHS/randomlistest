import streamlit as st
import random
import os
import requests
import base64
from PIL import Image, UnidentifiedImageError
from PIL.ImageFile import ImageFile
import io

def shuffle_and_divide_list(original_list, num_groups):
    if not isinstance(original_list, list) or not isinstance(num_groups, int):
        raise ValueError("Invalid input types for shuffle_and_divide_list")
    
    random.shuffle(original_list)
    group_size = len(original_list) // num_groups
    remainder = len(original_list) % num_groups

    groups = []
    start_index = 0

    for i in range(num_groups):
        extra = 1 if i < remainder else 0
        end_index = start_index + group_size + extra
        groups.append(original_list[start_index:end_index])
        start_index = end_index

    return groups

def relate_elements_to_groups(elements_list, groups):
    if not isinstance(elements_list, list) or not isinstance(groups, list):
        raise ValueError("Invalid input types for relate_elements_to_groups")
    
    related_groups = []
    for i, group in enumerate(groups):
        related_groups.append({
            "group": group,
            "related_element": elements_list[i]
        })
    return related_groups

def format_image(image: ImageFile):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = buffered.getvalue()
    image_base64 = base64.b64encode(img_str).decode('utf-8')
    return image_base64

def send_image_to_api(img_str):
    json_data = {"image": img_str}
    response = requests.post("https://nextjsocr.vercel.app/ocr", json=json_data)
    response.raise_for_status()
    print(response.json())
    return response.json().get("text", "")

def extract_text_from_image(image: ImageFile):
    try:
        img_str = format_image(image)
        text = send_image_to_api(img_str)
        return text
    except Exception as e:
        st.error(f'Error al extraer texto de la imagen: {str(e)}')
        return ""

def process_elements(elements, related_elements):
    if not all(isinstance(el, str) for el in elements):
        st.error('Todos los elementos deben ser cadenas.')
        return

    if not all(isinstance(rel_el, str) for rel_el in related_elements):
        st.error('Todos los elementos relacionados deben ser cadenas.')
        return

    num_groups = len(related_elements)
    if len(elements) < num_groups:
        st.error('La lista de elementos debe ser al menos del tamaño de la lista de elementos relacionados.')
    elif elements and related_elements and num_groups > 0 and len(related_elements) == num_groups:
        groups = shuffle_and_divide_list(elements, num_groups)
        related_groups = relate_elements_to_groups(related_elements, groups)

        st.subheader('Resultados')

        results = [{"Grupo": idx + 1, "Elementos": group, "Relacionado con": related_group["related_element"]}
                   for idx, (group, related_group) in enumerate(zip(groups, related_groups))]
        
        st.dataframe(results)
    else:
        st.error('Asegúrese de que la lista de elementos relacionados tenga el mismo tamaño que el número de sublistas.')

def main():
    st.title('Dividir Lista en Sublistas Aleatorias y Relacionarlas')
    st.subheader('Foto')
    enable = st.checkbox("Enable camera")
    picture = st.camera_input("Take a picture", disabled=not enable)

    if picture:
        st.image(picture)
        try:
            image = Image.open(picture.getvalue())
            text = extract_text_from_image(image)
            st.subheader('Texto extraído de la imagen')
            st.text(text)
        except UnidentifiedImageError:
            st.error('La imagen cargada no es válida.')
        
    st.subheader('Elementos añadidos')
    elements = st.data_editor(["Default"], num_rows="dynamic", use_container_width=True, key='elements_editor')
    st.subheader('Elementos relacionados añadidos')
    related_elements = st.data_editor(["Default1"], num_rows="dynamic", use_container_width=True, key='related_elements_editor')

    button_disabled = not (elements and related_elements)
    if st.button('Procesar', disabled=button_disabled, key='process_button'):
        process_elements(elements, related_elements)

    if button_disabled:
        st.warning('Ingrese ambas listas para proceder.')

if __name__ == "__main__":
    main()