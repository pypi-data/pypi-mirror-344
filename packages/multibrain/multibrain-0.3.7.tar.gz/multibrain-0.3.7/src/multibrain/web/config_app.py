# src/multbrain/web/config_app.py

import streamlit as st
import toml


# Function to load config from file
def load_config(file_path):
    with open(file_path, "r") as f:
        return toml.load(f)


# Function to save config to file
def save_config(config, file_path):
    with open(file_path, "w") as f:
        toml.dump(config, f)


# Path to the config.toml file
config_file_path = "config.toml"

# Load the current configuration
config = load_config(config_file_path)

# Streamlit app title
st.title("Config Editor")

# Models section
st.header("Models")
config["models"]["summary_server"] = st.text_input(
    "Summary Server Model", value=config["models"]["summary_server"]
)

# Servers section
st.header("Servers")
config["servers"]["summary_server_host"] = st.text_input(
    "Summary Server Host", value=config["servers"]["summary_server_host"]
)

# Response Servers section
st.header("Response Servers")
if "response_servers" not in config:
    config["response_servers"] = []

num_response_servers = len(config["response_servers"])
num_response_servers = st.number_input(
    "Number of Response Servers (max 16)",
    min_value=0,
    max_value=16,
    value=num_response_servers,
)

for idx in range(num_response_servers):
    st.subheader(f"Response Server {idx + 1}")
    config["response_servers"][idx]["host"] = st.text_input(
        f"Host", value=config["response_servers"][idx].get("host", "")
    )
    config["response_servers"][idx]["model"] = st.text_input(
        f"Model", value=config["response_servers"][idx].get("model", "")
    )

# Ensure the list has exactly num_response_servers entries
config["response_servers"] = config["response_servers"][:num_response_servers]

# Save button to update the config.toml file
if st.button("Save"):
    save_config(config, config_file_path)
    st.success("Configuration saved successfully!")
