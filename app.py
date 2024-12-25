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


def process_elements(elements, related_elements):
    num_groups = len(related_elements)
    if len(elements) < num_groups:
        st.error('La lista de elementos debe ser al menos del tamaño de la lista de elementos relacionados.')
    elif elements and related_elements and num_groups > 0 and len(related_elements) == num_groups:
        groups = shuffle_and_divide_list(elements, num_groups)
        related_groups = relate_elements_to_groups(related_elements, groups)

        st.write(f'Número total de elementos: {len(elements)}')
        st.write(f'Número de sublistas: {num_groups}')

        results = [{"Grupo": idx + 1, "Elementos": group, "Relacionado con": related_group["related_element"]}
                   for idx, (group, related_group) in enumerate(zip(groups, related_groups))]
        
        st.dataframe(results)
    else:
        st.error('Asegúrese de que la lista de elementos relacionados tenga el mismo tamaño que el número de sublistas.')


def main():
    st.title('Dividir Lista en Sublistas Aleatorias y Relacionarlas')
    st.subheader('Elementos añadidos:')
    elements = st.data_editor(["Default"], num_rows="dynamic", use_container_width=True, key='elements_editor')
    st.subheader('Elementos relacionados añadidos:')
    related_elements = st.data_editor(["Default1"], num_rows="dynamic", use_container_width=True, key='related_elements_editor')

    button_disabled = not (elements and related_elements)
    if st.button('Procesar', disabled=button_disabled, key='process_button'):
        process_elements(elements, related_elements)

    if button_disabled:
        st.warning('Ingrese ambas listas para proceder.')


if __name__ == "__main__":
    main()