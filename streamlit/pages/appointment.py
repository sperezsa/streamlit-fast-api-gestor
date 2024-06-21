import streamlit as st
import requests
import pandas as pd
import json
from menu import menu_with_redirect



def get_appointments(ident):
    base_url = "http://fastapi:8000/appointments/{}".format(ident)
    resp = requests.get(base_url)
    return resp.json()

def get_appointments_by_patient_id(ident):
    base_url = "http://fastapi:8000/appointments/{}/patients".format(ident)
    resp = requests.get(base_url)
    return resp.json()

def get_appointments_by_doc_id(ident):
    base_url = "http://fastapi:8000/appointments/{}/doctors".format(ident)
    resp = requests.get(base_url)
    return resp.json()


def main():
    st.title(f"Hello {st.session_state.role}!")
    
    
    # Redirect to app.py if not logged in, otherwise show the navigation menu
    menu_with_redirect()

    st.title("This page is available to all users")
    st.markdown(f"You are currently logged with the role of {st.session_state.role}.")
    

    #################################
    # BÚSQUEDA CITAS APPOINTMENT_ID #
    #################################
    st.title("Búsqueda citas por appointment_id")
    # Definir el formulario
    citas = st.form(key='f_cita_bus_appointment_id', clear_on_submit=True)
    # Campos del formulario
    c = citas.text_input('appointment_id:')
    # Botón de envío
    boton_cita_bus_1 = citas.form_submit_button("Submit") 

    # Si se ha enviado el formulario
    if boton_cita_bus_1:
        results = get_appointments(c)

        if results:
            #comento esta línea donde muestra los result en formato json
            #st.json(results)  
            
            # Para mostrar los resultados en un df
            df = pd.DataFrame(results)
            st.dataframe(df)
        else:
            st.info("No records found in the database.")  


    #############################
    # BÚSQUEDA CITAS PATIENT_ID #
    #############################
    st.title("Búsqueda citas por patient_id")
    # Definir el formulario
    citas = st.form(key='f_cita_bus_patient_id', clear_on_submit=True)
    # Campos del formulario
    c = citas.text_input('patient_id:')
    # Botón de envío
    boton_cita_bus_2 = citas.form_submit_button("Submit") 

    # Si se ha enviado el formulario
    if boton_cita_bus_2:
        results = get_appointments_by_patient_id(c)

        if results:
            #comento esta línea donde muestra los result en formato json
            #st.json(results)  
            
            # Para mostrar los resultados en un df
            df = pd.DataFrame(results)
            st.dataframe(df)
        else:
            st.info("No records found in the database.")  


    #########################
    # BÚSQUEDA CITAS DOC_ID #
    #########################
    st.title("Búsqueda citas por doc_id")
    # Definir el formulario
    citas = st.form(key='f_cita_bus_doc_id', clear_on_submit=True)
    # Campos del formulario
    c = citas.text_input('doc_id:')
    # Botón de envío
    boton_cita_bus_3 = citas.form_submit_button("Submit") 

    # Si se ha enviado el formulario
    if boton_cita_bus_3:
        results = get_appointments_by_doc_id(c)

        if results:
            #comento esta línea donde muestra los result en formato json
            #st.json(results)  
            
            # Para mostrar los resultados en un df
            df = pd.DataFrame(results)
            st.dataframe(df)
        else:
            st.info("No records found in the database.")  

            
if __name__ == '__main__':
    main()
