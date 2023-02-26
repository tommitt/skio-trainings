import streamlit as st


def button_withResponseMessage(
    button_text,
    button_disabled,
    on_click,
    args,
    error_message=None,
    warning_message=None,
    container=None,
):
    placeholder = container if container else st
    button = placeholder.button(
        button_text, disabled=button_disabled, use_container_width=True
    )
    if button:
        response = on_click(*args)
        if response == -1:
            if error_message:
                st.error(error_message)
            if warning_message:
                st.warning(warning_message)
        else:
            st.experimental_rerun()
