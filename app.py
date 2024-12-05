import streamlit as st
import os

### ---------------------------- Directory Setup -------------------------- ###
FILE_DIR = "FILE_DIR"
os.makedirs(FILE_DIR, exist_ok=True)


### ---------------------------- Session State -------------------------- ###
# Initialize session state for options and confirmation prompts
if 'show_option' not in st.session_state:
    st.session_state.show_option = True  # Set show_option as the default
if 'upload_option' not in st.session_state:
    st.session_state.upload_option = False
if 'create_option' not in st.session_state:
    st.session_state.create_option = False
if 'update_option' not in st.session_state:
    st.session_state.update_option = False
if 'delete_option' not in st.session_state:
    st.session_state.delete_option = False
if 'confirm_upload' not in st.session_state:
    st.session_state.confirm_upload = False
if 'confirm_create' not in st.session_state:
    st.session_state.confirm_create = False
if 'confirm_update' not in st.session_state:
    st.session_state.confirm_update = False
if 'confirm_delete' not in st.session_state:
    st.session_state.confirm_delete = False

# Function to reset options and show only the selected option
def reset_options():
    st.session_state.show_option = False
    st.session_state.upload_option = False
    st.session_state.create_option = False
    st.session_state.update_option = False
    st.session_state.delete_option = False
    st.session_state.confirm_upload = False
    st.session_state.confirm_create = False
    st.session_state.confirm_update = False
    st.session_state.confirm_delete = False



### ----------------------------Page Config-------------------------- ###
st.set_page_config(page_title="Ask-Orion.bot Management Dashboard", layout="wide")
st.markdown(
    """
    <style>
        /* General page styling */
        body {
            font-family: 'Arial', sans-serif;
        }
        
        /* Hide default Streamlit footer */
        footer {visibility: hidden;}

        /* Custom header styling */
        .main-header {
            font-size: 2rem;
            font-weight: bold;
            text-align: center;
            color: #ffffff;
            background-color: #4B4B4B;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }

        /* Button styling */
        .stButton > button {
            width: 100%;
            color: #ffffff;
            background-color: #0073e6;
            border-radius: 5px;
            padding: 10px;
            font-size: 1rem;
            font-weight: bold;
            border: none;
            transition: 0.3s;
        }
        .stButton > button:hover {
            background-color: #005bb5;
        }

        /* Sidebar styling */
        .sidebar .sidebar-content {
            background-color: #333;
            color: white;
            padding: 20px;
        }

        /* Text area styling */
        .stTextArea textarea {
            border: 1px solid #0073e6;
            border-radius: 5px;
        }

        /* Custom footer styling */
        .footer {
            font-size: 0.9rem;
            text-align: center;
            padding: 20px;
            color: #666;
            margin-top: 40px;
        }
    </style>
    """,
    unsafe_allow_html=True
)


### ----------------------------Sidebar-------------------------- ###
# Sidebar Navigation with Icons
st.sidebar.title("📂 Dashboard Navigation")
st.sidebar.header("📝 File Management")
st.sidebar.markdown("Use the options below to manage text files:")

# Sidebar Options with Session State
if st.sidebar.button("📘 Show Text Files"):
    reset_options()
    st.session_state.show_option = True
if st.sidebar.button("⬆️ Upload New Text File"):
    reset_options()
    st.session_state.upload_option = True
if st.sidebar.button("🆕 Create New Text File"):
    reset_options()
    st.session_state.create_option = True
if st.sidebar.button("🔍 Update Existing Text File"):
    reset_options()
    st.session_state.update_option = True
if st.sidebar.button("🚮 Delete Existing Text File"):
    reset_options()
    st.session_state.delete_option = True



### ----------------------------Main Page-------------------------- ###
# Main Title
st.markdown("<div class='main-header'>Ask-Orion.bot Management Dashboard</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.2rem;'>Create, upload, update, and delete files!</p>", unsafe_allow_html=True)


# Show Files (Default View)
if st.session_state.show_option:
    st.header("📘 Show Text Files")
    files = [f for f in os.listdir(FILE_DIR) if f.endswith(".txt")]
    if files:
        selected_file = st.selectbox("Select a file to view", files, key="show_selectbox")
        if selected_file:
            file_path = os.path.join(FILE_DIR, selected_file)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    file_content = f.read()
            except UnicodeDecodeError:
                with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                    file_content = f.read()

            st.subheader(f"📄 Content of {selected_file} (Read-only)")
            st.text_area("File Content", file_content, height=300, disabled=True, key="show_file_content")
    else:
        st.write("No files available.")


# Main Content for Uploading Files
if st.session_state.upload_option:
    st.header("⬆️ Upload New Text File")
    uploaded_files = st.file_uploader("Upload .txt files", type=["txt"], accept_multiple_files=True)
    if uploaded_files:
        st.session_state.confirm_upload = True

    # Upload Confirmation Card
    if st.session_state.confirm_upload:
        st.markdown(
            f"""
            <div style="border: 2px solid #0073e6; padding: 20px; border-radius: 10px; background-color: #e6f2ff; margin-top: 20px; text-align: center;">
                <h4 style="color: #0073e6; font-weight: bold;">Are you sure you want to upload these files?</h4>
                <p style="color: #333;">This action will add the selected files to the directory.</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        col1, col2 = st.columns([1, 1], gap="small")
        with col1:
            if st.button("✅ Yes, Upload"):
                for uploaded_file in uploaded_files:
                    file_path = os.path.join(FILE_DIR, uploaded_file.name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    st.success(f"File '{uploaded_file.name}' uploaded successfully!")
                reset_options()  # Reset options after successful upload
        with col2:
            if st.button("❌ Cancel"):
                st.error("Upload action canceled.")
                st.session_state.confirm_upload = False


# Main Content for Creating New File
if st.session_state.create_option:
    st.header("🆕 Create New Text File")
    new_file_name = st.text_input("Enter new file name (without .txt):")
    new_file_content = st.text_area("Enter file content:", height=300, key="create_file_content")
    if st.button("Create New File"):
        if new_file_name:
            st.session_state.confirm_create = True

    # Create Confirmation Card
    if st.session_state.confirm_create:
        st.markdown(
            f"""
            <div style="border: 2px solid #0073e6; padding: 20px; border-radius: 10px; background-color: #e6f2ff; margin-top: 20px; text-align: center;">
                <h4 style="color: #0073e6; font-weight: bold;">Are you sure you want to create the file '{new_file_name}.txt'?</h4>
                <p style="color: #333;">This action will add a new file to the directory.</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        col1, col2 = st.columns([1, 1], gap="small")
        with col1:
            if st.button("✅ Yes, Create"):
                file_path = os.path.join(FILE_DIR, f"{new_file_name}.txt")
                if not os.path.exists(file_path):
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_file_content)
                    st.success(f"File '{new_file_name}.txt' created successfully!")
                    reset_options()
                else:
                    st.warning("File already exists!")
                    st.session_state.confirm_create = False
        with col2:
            if st.button("❌ Cancel"):
                st.error("File creation canceled.")
                st.session_state.confirm_create = False


# Main Content for Updating Existing File
if st.session_state.update_option:
    st.header("🔍 Update Existing Text File")
    files = [f for f in os.listdir(FILE_DIR) if f.endswith(".txt")]
    if files:
        selected_file = st.selectbox("Select a file to update", files)
        if selected_file:
            file_path = os.path.join(FILE_DIR, selected_file)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    file_content = f.read()
            except UnicodeDecodeError:
                with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                    file_content = f.read()

            st.subheader(f"📝 Content of {selected_file}")
            new_content = st.text_area("Edit file content:", file_content, height=300, key="update_file_content")

            if st.button("Update File"):
                st.session_state.confirm_update = True

            # Update Confirmation Card
            if st.session_state.confirm_update:
                st.markdown(
                    f"""
                    <div style="border: 2px solid #0073e6; padding: 20px; border-radius: 10px; background-color: #e6f2ff; margin-top: 20px; text-align: center;">
                        <h4 style="color: #0073e6; font-weight: bold;">Are you sure you want to update the file '{selected_file}'?</h4>
                        <p style="color: #333;">This action will overwrite the existing content.</p>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
                col1, col2 = st.columns([1, 1], gap="small")
                with col1:
                    if st.button("✅ Yes, Update"):
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(new_content)
                        st.success(f"File '{selected_file}' updated successfully!")
                        reset_options()
                with col2:
                    if st.button("❌ Cancel"):
                        st.error("Update action canceled.")
                        st.session_state.confirm_update = False


# Main Content for Deleting Existing File
if st.session_state.delete_option:
    st.header("🚮 Delete Existing Text File")
    files = [f for f in os.listdir(FILE_DIR) if f.endswith(".txt")]
    if files:
        selected_file = st.selectbox("Select a file to delete", files, key="delete_selectbox")
        
        if selected_file:
            file_path = os.path.join(FILE_DIR, selected_file)
            
            # Display file content in read-only mode
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    file_content = f.read()
            except UnicodeDecodeError:
                with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                    file_content = f.read()

            st.subheader(f"📄 Content of {selected_file} (Read-only)")
            st.text_area("File Content", file_content, height=300, disabled=True, key="delete_file_content")

            if st.button("Delete File"):
                st.session_state.confirm_delete = True

            # Delete Confirmation Card
            if st.session_state.confirm_delete:
                st.markdown(
                    f"""
                    <div style="border: 2px solid #e60000; padding: 20px; border-radius: 10px; background-color: #ffe6e6; margin-top: 20px; text-align: center;">
                        <h4 style="color: #e60000; font-weight: bold;">Are you sure you want to delete the file '{selected_file}'?</h4>
                        <p style="color: #333;">This action cannot be undone.</p>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
                col1, col2 = st.columns([1, 1], gap="small")
                with col1:
                    if st.button("✅ Yes, Delete"):
                        os.remove(file_path)
                        st.success(f"File '{selected_file}' deleted successfully!")
                        reset_options()
                with col2:
                    if st.button("❌ Cancel"):
                        st.error("Delete action canceled.")
                        st.session_state.confirm_delete = False



### ----------------------------Footer -------------------------- ###
# Custom Footer
def footer():
    st.markdown(
        """
        <div class="footer">
            <hr style="margin-top:2rem; margin-bottom:2rem;">
            &copy; 2024 APE Paper.id
        </div>
        """,
        unsafe_allow_html=True,
    )

footer()
