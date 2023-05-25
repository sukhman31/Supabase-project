import streamlit as st
from supabase import create_client, Client

@st.cache_resource
def init_connection():
    url = st.secrets["supabase_url"]
    key = st.secrets["supabase_key"]
    return create_client(url, key)

supabase = init_connection()
email_id = ''

with st.form("login"):
    email_id = st.text_input('Email ID')
    password = st.text_input('Password')

    col1,col2 = st.columns(2)

    if col1.form_submit_button('Sign Up'):
        res = supabase.auth.sign_up({
            "email": email_id,
            "password": password,
        })
        st.write("Confirm your email address")
    if col2.form_submit_button('Log in'):
        data = supabase.auth.sign_in_with_password({"email": email_id, "password": password})

if email_id != '':
    with st.form("add note"):
        note = st.text_input('Note')

        if st.form_submit_button('Add note'):
            count, data = supabase.table("todo_list").insert({"email": email_id, "value": note}).execute()
        
    if st.button('View notes'):
        data,count = supabase.table("todo_list").select("*").eq("email", email_id).execute()
        
        for message in data[1]:
            st.write(message['value'])