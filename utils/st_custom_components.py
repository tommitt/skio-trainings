import asyncio
import time

import streamlit as st

from utils import st_session_state
from utils.settings import settings


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


def empty_space(n_lines):
    for _ in range(n_lines):
        st.write("&nbsp;")


def chronometer():
    """
    Manual chronometer wrapped in a expander container.
    The chronometer runs asynchronously to allow the rest of the app to be still responsive.
    """
    DECIMAL_SHOWN = 2
    TIMESTEP_SHOWN = 10 ** (-DECIMAL_SHOWN)
    TIMESTEP_REAL = TIMESTEP_SHOWN / 10

    async def run_chronometer(container):
        run_time = 0.0
        while (
            st.session_state["chrono_running"]
            and run_time < settings.max_time - TIMESTEP_REAL
        ):
            st.session_state["chrono_stop_ts"] = time.time()
            run_time = (
                st.session_state["chrono_stop_ts"] - st.session_state["chrono_start_ts"]
            )
            container.subheader(f"{run_time + TIMESTEP_SHOWN:.{DECIMAL_SHOWN}f}")
            await asyncio.sleep(TIMESTEP_REAL)

    if "chrono_running" not in st.session_state:
        st_session_state.init_chrono()

    with st.expander("Cronometro manuale"):
        col1_run, col2_run = st.columns(2)
        container = st.empty()
        col1_save, col2_save = st.columns(2)

    # buttons to run chronometer
    with col1_run:
        if st.button("Start", use_container_width=True):
            st.session_state["chrono_start_ts"] = time.time()
            st.session_state["chrono_running"] = True
            st.session_state["chrono_stop_ts"] = None

    with col2_run:
        if st.button("Stop", use_container_width=True):
            st.session_state["chrono_running"] = False

    # fill container when chrono is not running
    if not st.session_state["chrono_running"]:
        if not st.session_state["chrono_stop_ts"]:
            container.subheader(f"{0.0:.{DECIMAL_SHOWN}f}")
        else:
            run_time = round(
                st.session_state.chrono_stop_ts - st.session_state.chrono_start_ts, 2
            )
            container.subheader(f"{run_time:.{DECIMAL_SHOWN}f}")

    # buttons to save chronometer result
    with col1_save:
        if st.button(
            "Salva",
            disabled=(not st.session_state["chrono_stop_ts"]),
            use_container_width=True,
        ):
            st.session_state["running_time"] = run_time
            st.experimental_rerun()

    with col2_save:
        if st.button(
            "Cancella",
            disabled=(not st.session_state["chrono_stop_ts"]),
            use_container_width=True,
        ):
            st_session_state.init_chrono()
            st.experimental_rerun()

    # run chronometer asynchronously
    asyncio.run(run_chronometer(container))
