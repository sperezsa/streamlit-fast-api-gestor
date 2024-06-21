import streamlit as st
import requests
import pandas as pd
import json
from menu import menu_with_redirect




def get_patients(name):
    base_url = "http://fastapi:8000/patients/{}".format(name)
    resp = requests.get(base_url)
    return resp.json()

def post_patient(data):
    try:
        base_url = "http://fastapi:8000/patients"
        resp = requests.post(base_url, json = data)
        return resp.json()
    except Exception as e:
        st.error("Ocurrió un error inesperado:", e)

def del_patient(patient_id):
    base_url = "http://fastapi:8000/patients/{}".format(patient_id)
    resp = requests.delete(base_url)
    return resp.json()

def put_patient(data):
    try:
        base_url = "http://fastapi:8000/patients"
        resp = requests.put(base_url, json = data)
        return resp.json()
    except Exception as e:
        st.error("Ocurrió un error inesperado:", e)

def main():
    st.title(f"Hello {st.session_state.role}!")
    
   
    # Redirect to app.py if not logged in, otherwise show the navigation menu
    menu_with_redirect()

    st.title("This page is available to all users")
    st.markdown(f"You are currently logged with the role of {st.session_state.role}.")
    
    
    ##################
    # ALTA PACIENTE  #
    ##################    
    st.title("Alta paciente") 
    # Definir el formulario
    alta = st.form(key='f_paciente_alta', clear_on_submit=True)
    # Campos del formulario
    nombre = alta.text_input('Nombre:')
    correo = alta.text_input('Correo electrónico:')
    mensaje = alta.text_area('Mensaje:')  
    data = { "patient_id": 0,
            "username": nombre,
            "email": correo,
            "message": mensaje}
    
    # Botón de envío
    boton_pac_alta = alta.form_submit_button("Submit") 
    
    # Si se ha enviado el formulario
    if boton_pac_alta:
        results = post_patient(data)
        st.success("Alta ok")
        #comento esta línea donde muestra los result en formato json
        #st.json(results) 
        # Para mostrar los resultados en un df
        df = pd.DataFrame(results)
        st.dataframe(df)
        
    
    ######################
    # BÚSQUEDA PACIENTE  #
    ######################
    st.title("Búsqueda paciente")
    # Definir el formulario
    busq = st.form(key='f_paciente_busqueda', clear_on_submit=True)
    # Campos del formulario
    nombreb = busq.text_input('Nombre:')
    # Botón de envío
    boton_pac_busqueda = busq.form_submit_button("Submit") 

    # Si se ha enviado el formulario
    if boton_pac_busqueda:
        results = get_patients(nombreb)

        if results:
            #comento esta línea donde muestra los result en formato json
            #st.json(results)  
            
            # Para mostrar los resultados en un df
            df = pd.DataFrame(results)
            st.dataframe(df)
            
            # Con este bloque comentado es para crear un campo nuevo con el id 
            # del registro pensado para hacer una llamada para eliminar regristro
            # df["Detalle"] = ""             
            # for i in df.index: 
            #     record_id = df.loc[i, 'patient_id'] 
            #     df.loc[i, 'Detalle'] = str(record_id)
            # # Empleando st.table(df) pinta el listado pero para incluir enlaces necesito
            # # utilizar data_editor
            # st.data_editor(
            #     df,
            #     column_config={
            #         "Detalle": st.column_config.LinkColumn(
            #             "Paciente",
            #             help="Listado de pacientes",
            #             max_chars=100,
            #             # para mostrar el ID de cada paciente
            #             display_text= "(.*?)"
            #         )
            #     },
            #     hide_index=True,
            # )
                        
        else:
            st.info("No records found in the database.")  

    ######################
    # BORRADO  PACIENTE  #
    ######################    
    st.title("Borrado paciente")
    # Definir el formulario
    borrado = st.form(key='f_paciente_borrado', clear_on_submit=True)   
    # Campos del formulario
    patient_id = borrado.text_input('Patient_id:') 
    # Botón de envío
    boton_pac_borrado = borrado.form_submit_button("Submit") 
    
    # Si se ha enviado el formulario
    if boton_pac_borrado:
        results = del_patient(patient_id)
        st.success("Borrado ok")
        #comento esta línea donde muestra los result en formato json
        #st.json(results) 
        # Para mostrar los resultados en un df
        df = pd.DataFrame(results)
        st.dataframe(df)

    ###################
    # MODIF PACIENTE  #
    ###################    
    st.title("Modificación paciente")  
    # Definir el formulario
    modif = st.form(key='f_paciente_modif', clear_on_submit=True)  
    # Campos del formulario
    patient_id = modif.text_input('Id:')
    nombre = modif.text_input('Nombre:')
    correo = modif.text_input('Correo electrónico:')
    mensaje = modif.text_area('Mensaje:') 
    
    data = { "patient_id": patient_id,
            "username": nombre,
            "email": correo,
            "message": mensaje}
    
    # Botón de envío
    boton_pac_modif = modif.form_submit_button("Submit") 
    
    # Si se ha enviado el formulario
    if boton_pac_modif:
        results = put_patient(data)
        st.success("Modif ok")
        #comento esta línea donde muestra los result en formato json
        #st.json(results) 
        # Para mostrar los resultados en un df
        df = pd.DataFrame(results)
        st.dataframe(df)

         
if __name__ == '__main__':
    main()
