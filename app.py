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


def display_elements(elements):
    st.subheader('Elementos añadidos:')
    st.data_editor({'Elementos': elements}, use_container_width=True)
    st.dataframe(elements, width=700, height=300)


def display_related_elements(related_elements):
    st.subheader('Elementos relacionados añadidos:')
    st.data_editor({'Elementos Relacionados': related_elements}, use_container_width=True)
    st.dataframe(related_elements, width=700, height=300)


def process_elements(elements, related_elements):
    num_groups = len(related_elements)
    if len(elements) < num_groups:
        st.error('La lista de elementos debe ser al menos del tamaño de la lista de elementos relacionados.')
    elif elements and related_elements and num_groups > 0 and len(related_elements) == num_groups:
        groups = shuffle_and_divide_list(elements, num_groups)
        related_groups = relate_elements_to_groups(related_elements, groups)

        st.write(f'Número total de elementos: {len(elements)}')
        st.write(f'Número de sublistas: {num_groups}')

        for idx, related_group in enumerate(related_groups):
            st.write(f'Grupo {idx + 1}: {related_group["group"]}, Relacionado con: {related_group["related_element"]}')
    else:
        st.error('Asegúrese de que la lista de elementos relacionados tenga el mismo tamaño que el número de sublistas.')


def main():
    st.title('Dividir Lista en Sublistas Aleatorias y Relacionarlas')

    elements = st.data_editor({'Elementos': []}, use_container_width=True)
    related_elements = st.data_editor({'Elementos Relacionados': []}, use_container_width=True)

    if elements and related_elements:
        display_elements(elements['Elementos'])
        display_related_elements(related_elements['Elementos Relacionados'])

        if st.button('Procesar'):
            process_elements(elements['Elementos'], related_elements['Elementos Relacionados'])
    else:
        st.warning('Ingrese ambas listas para proceder.')


if __name__ == "__main__":
    main()