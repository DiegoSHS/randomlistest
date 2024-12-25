import streamlit as st
import random

def shuffle_and_divide_list(original_list, num_groups):
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
    related_groups = []
    for i, group in enumerate(groups):
        related_groups.append({
            "group": group,
            "related_element": elements_list[i]
        })
    return related_groups

st.title('Dividir Lista en Sublistas Aleatorias y Relacionarlas')

input_list = st.text_area('Ingrese la lista de elementos separada por comas:')
related_elements_list = st.text_area('Ingrese la lista de elementos relacionados separada por comas:')

if input_list:
    elements = [item.strip() for item in input_list.split(',') if item.strip()]
    st.subheader('Elementos añadidos:')
    for element in elements:
        st.write(f"• {element}")

if related_elements_list:
    related_elements = [item.strip() for item in related_elements_list.split(',') if item.strip()]
    st.subheader('Elementos relacionados añadidos:')
    for related_element in related_elements:
        st.write(f"• {related_element}")

if input_list and related_elements_list:
    num_groups = st.number_input('Ingrese el número de sublistas:', min_value=1, max_value=len(elements), value=2)
    
    if st.button('Procesar'):
        if elements and related_elements and num_groups > 0 and len(related_elements) == num_groups:
            groups = shuffle_and_divide_list(elements, num_groups)
            related_groups = relate_elements_to_groups(related_elements, groups)
            
            st.write(f'Número total de elementos: {len(elements)}')
            st.write(f'Número de sublistas: {num_groups}')
            
            for idx, related_group in enumerate(related_groups):
                st.write(f'Grupo {idx + 1}: {related_group["group"]}, Relacionado con: {related_group["related_element"]}')
        else:
            st.error('Asegúrese de que la lista de elementos relacionados tenga el mismo tamaño que el número de sublistas.')
else:
    st.warning('Ingrese ambas listas para proceder.')