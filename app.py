import html

import streamlit as st

from edukasi import run_edukasi
from komunitas import run_komunitas
from konsultasi import run_konsultasi
from ml_app import run_ml_app


# ======================
# Page Configuration
# ======================
st.set_page_config(
    page_title="Audore",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ======================
# Constants
# ======================
PAGES = [
    "Home",
    "Audore Assistant",
    "Edukasi",
    "Konsultasi",
    "Komunitas",
]

FEATURES = {
    "Audore Assistant": {
        "description": (
            "Membantu mengidentifikasi kategori permasalahan caregiver "
            "berdasarkan keluhan yang disampaikan."
        ),
        "color": "#FFDDE7",
        "accent": "#FF7A98",
        "button_type": "secondary",
    },
    "Edukasi": {
        "description": (
            "Menyediakan informasi edukatif untuk mendukung pemahaman "
            "caregiver dalam pendampingan anak."
        ),
        "color": "#FFF0C9",
        "accent": "#F3B43F",
        "button_type": "secondary",
    },
    "Konsultasi": {
        "description": (
            "Membantu caregiver memperoleh arahan awal melalui layanan "
            "konsultasi yang tersedia."
        ),
        "color": "#EAF6FF",
        "accent": "#65A9F5",
        "button_type": "secondary",
    },
    "Komunitas": {
        "description": (
            "Menjadi ruang berbagi informasi dan dukungan antar-caregiver "
            "dalam komunitas Audore."
        ),
        "color": "#E9E1FF",
        "accent": "#8D73E6",
        "button_type": "secondary",
    },
}


# ======================
# Styling
# ======================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    html,
    body,
    .stApp,
    [data-testid="stAppViewContainer"] {
        color-scheme: light;
    }

    .stApp {
        background:
            radial-gradient(circle at top left, #FFF0F4 0%, transparent 30%),
            radial-gradient(circle at top right, #EAF6FF 0%, transparent 32%),
            radial-gradient(circle at bottom right, #EFE8FF 0%, transparent 34%),
            linear-gradient(180deg, #FFF9FA 0%, #F8FBFF 48%, #F4FCFF 100%);
        color: #2F2A38;
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }

    .block-container {
        max-width: 1180px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    footer {
        display: none !important;
    }

    section[data-testid="stSidebar"] {
        background:
            radial-gradient(circle at top left, #FFF0F4 0%, transparent 42%),
            radial-gradient(circle at bottom right, #EFE8FF 0%, transparent 38%),
            rgba(255, 255, 255, 0.92);
        border-right: 1px solid rgba(122, 90, 248, 0.12);
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1.1rem;
    }

    .sidebar-brand {
        background:
            radial-gradient(circle at top left, #FFDDE7 0%, transparent 48%),
            radial-gradient(circle at bottom right, #EAF6FF 0%, transparent 45%),
            linear-gradient(145deg, #FFFFFF 0%, #FFF9FA 100%);
        border: 1px solid rgba(122, 90, 248, 0.12);
        border-radius: 20px;
        padding: 1rem;
        margin-bottom: 0.75rem;
        box-shadow: 0 12px 28px rgba(88, 72, 124, 0.08);
    }

    .sidebar-brand h2 {
        color: #111111;
        font-size: 1.4rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: 0;
    }

    .sidebar-brand p {
        color: #6A6278;
        font-size: 0.84rem;
        line-height: 1.45;
        margin: 0.3rem 0 0 0;
    }

    .sidebar-profile {
        background: rgba(255, 255, 255, 0.78);
        border: 1px solid rgba(122, 90, 248, 0.10);
        border-radius: 16px;
        padding: 0.8rem 0.9rem;
        margin-bottom: 0.75rem;
    }

    .sidebar-profile-label {
        color: #8A819A;
        font-size: 0.76rem;
        margin-bottom: 0.2rem;
    }

    .sidebar-profile-name {
        color: #2F2A38;
        font-size: 1rem;
        font-weight: 800;
        margin-bottom: 0.1rem;
    }

    .sidebar-profile-role {
        color: #6A6278;
        font-size: 0.84rem;
    }

    .sidebar-menu-title {
        color: #6A6278;
        font-size: 0.82rem;
        font-weight: 800;
        margin: 0.25rem 0 0.25rem 0;
    }

    div[role="radiogroup"] {
        gap: 0.02rem;
    }

    div[role="radiogroup"] label {
        border-radius: 14px;
        padding: 0.16rem 0.3rem;
    }

    div[role="radiogroup"] label:hover {
        background: rgba(255, 221, 231, 0.45);
    }

    .login-shell {
        max-width: 1080px;
        margin: 1.3rem auto 0 auto;
    }

    .login-brand-card {
        min-height: 520px;
        background:
            radial-gradient(circle at top left, #FFDDE7 0%, transparent 40%),
            radial-gradient(circle at center right, #EAF6FF 0%, transparent 38%),
            radial-gradient(circle at bottom right, #E9E1FF 0%, transparent 42%),
            linear-gradient(145deg, #FFFFFF 0%, #F8FBFF 100%);
        border: 1px solid rgba(122, 90, 248, 0.12);
        border-radius: 28px;
        box-shadow: 0 24px 60px rgba(88, 72, 124, 0.14);
        padding: 2.4rem;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .login-badge {
        display: inline-block;
        width: fit-content;
        background: linear-gradient(90deg, #FFDDE7 0%, #EAF6FF 100%);
        color: #3A2E3F;
        border-radius: 999px;
        padding: 0.45rem 0.85rem;
        font-size: 0.86rem;
        font-weight: 700;
        margin-bottom: 1.2rem;
    }

    .login-brand-card h1 {
        color: #111111;
        font-size: 3rem;
        font-weight: 800;
        margin: 0 0 0.8rem 0;
        letter-spacing: 0;
    }

    .login-brand-card p {
        color: #5F5870;
        font-size: 1.05rem;
        line-height: 1.75;
        margin: 0;
    }

    .login-info-grid {
        display: grid;
        gap: 0.85rem;
        margin-top: 2rem;
    }

    .login-info-item {
        background: rgba(255, 255, 255, 0.72);
        border: 1px solid rgba(122, 90, 248, 0.10);
        border-radius: 18px;
        padding: 1rem 1.1rem;
        color: #514568;
        font-size: 0.94rem;
        line-height: 1.55;
    }

    div[data-testid="stForm"] {
        border: 0;
        padding: 0;
        box-shadow: none;
        background: transparent;
    }

    .login-form-title h2 {
        color: #111111;
        font-size: 1.75rem;
        font-weight: 800;
        margin: 0 0 0.35rem 0;
        letter-spacing: 0;
    }

    .login-form-title p {
        color: #6A6278;
        margin: 0 0 1.3rem 0;
        line-height: 1.6;
    }

    .auth-note {
        color: #6A6278 !important;
        font-size: 0.9rem;
        line-height: 1.55;
        margin-top: 0.9rem;
        margin-bottom: 0.25rem;
        text-align: center;
    }

    .home-hero {
        background:
            radial-gradient(circle at top left, #FFDDE7 0%, transparent 38%),
            radial-gradient(circle at top right, #EAF6FF 0%, transparent 36%),
            radial-gradient(circle at bottom right, #E9E1FF 0%, transparent 42%),
            linear-gradient(145deg, #FFFFFF 0%, #FFF9FA 100%);
        border: 1px solid rgba(122, 90, 248, 0.10);
        border-radius: 28px;
        box-shadow: 0 18px 42px rgba(88, 72, 124, 0.10);
        padding: 2rem 2.2rem;
        margin-bottom: 1.35rem;
    }

    .home-hero h1 {
        color: #111111;
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0 0 0.55rem 0;
        letter-spacing: 0;
    }

    .home-hero p {
        color: #5F5870;
        font-size: 1.02rem;
        line-height: 1.7;
        margin: 0;
    }

    .home-section-header {
        margin: 0.25rem 0 1.1rem 0;
    }

    .home-section-title {
        color: #111111;
        font-size: 1.72rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: 0;
    }

    .home-section-subtitle {
        color: #6A6278;
        font-size: 0.95rem;
        margin: 0.25rem 0 0 0;
        line-height: 1.55;
    }

    .feature-card-home {
        border: 1px solid rgba(122, 90, 248, 0.12);
        border-radius: 28px;
        box-shadow: 0 18px 42px rgba(88, 72, 124, 0.10);
        padding: 2rem 2.1rem;
        min-height: 15.5rem;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        margin-bottom: 0.9rem;
        transition: 0.2s ease;
    }

    .feature-card-home:hover {
        transform: translateY(-2px);
        box-shadow: 0 22px 50px rgba(88, 72, 124, 0.14);
        border-color: rgba(122, 90, 248, 0.20);
    }

    .feature-card-home.feature-pink {
        background:
            radial-gradient(circle at top left, #FFDDE7 0%, rgba(255, 221, 231, 0) 46%),
            radial-gradient(circle at bottom right, #EAF6FF 0%, rgba(234, 246, 255, 0) 48%),
            linear-gradient(145deg, #FFFFFF 0%, #FFF9FA 100%);
    }

    .feature-card-home.feature-yellow {
        background:
            radial-gradient(circle at top left, #FFF0C9 0%, rgba(255, 240, 201, 0) 46%),
            radial-gradient(circle at bottom right, #E9E1FF 0%, rgba(233, 225, 255, 0) 48%),
            linear-gradient(145deg, #FFFFFF 0%, #FFFCF2 100%);
    }

    .feature-card-home.feature-blue {
        background:
            radial-gradient(circle at top left, #EAF6FF 0%, rgba(234, 246, 255, 0) 46%),
            radial-gradient(circle at bottom right, #E9E1FF 0%, rgba(233, 225, 255, 0) 48%),
            linear-gradient(145deg, #FFFFFF 0%, #F8FBFF 100%);
    }

    .feature-card-home.feature-purple {
        background:
            radial-gradient(circle at top left, #E9E1FF 0%, rgba(233, 225, 255, 0) 46%),
            radial-gradient(circle at bottom right, #FFDDE7 0%, rgba(255, 221, 231, 0) 48%),
            linear-gradient(145deg, #FFFFFF 0%, #FBF8FF 100%);
    }

    .feature-badge {
        display: inline-block;
        width: fit-content;
        border-radius: 999px;
        color: #3A3444;
        font-size: 0.84rem;
        font-weight: 800;
        padding: 0.5rem 0.95rem;
        margin-bottom: 1.55rem;
    }

    .feature-pink .feature-badge {
        background: rgba(255, 221, 231, 0.90);
    }

    .feature-yellow .feature-badge {
        background: rgba(255, 240, 201, 0.95);
    }

    .feature-blue .feature-badge {
        background: rgba(234, 246, 255, 0.95);
    }

    .feature-purple .feature-badge {
        background: rgba(233, 225, 255, 0.95);
    }

    .feature-title {
        color: #2F2A38;
        font-size: 1.7rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: 0;
        line-height: 1.2;
    }

    .feature-description {
        color: #4F485D;
        font-size: 1rem;
        line-height: 1.72;
        margin: 1rem 0 0 0;
    }

    label,
    [data-testid="stWidgetLabel"],
    [data-testid="stWidgetLabel"] p,
    [data-testid="stMarkdownContainer"],
    [data-testid="stMarkdownContainer"] p {
        color: #2F2A38 !important;
    }

    div[data-testid="stTextInput"] label,
    div[data-testid="stTextInput"] label p,
    div[data-testid="stRadio"] label,
    div[data-testid="stRadio"] label p,
    div[data-testid="stSelectbox"] label,
    div[data-testid="stSelectbox"] label p {
        color: #2F2A38 !important;
    }

    div[data-testid="stTextInput"] input {
        background: #F1F7FF !important;
        color: #2F2A38 !important;
        border-radius: 14px !important;
        border: 1px solid rgba(122, 90, 248, 0.16) !important;
    }

    div[data-testid="stTextInput"] input::placeholder {
        color: #8A819A !important;
    }

    div[data-testid="stButton"] > button,
    div[data-testid="stFormSubmitButton"] > button {
        border-radius: 999px;
        font-weight: 700;
        min-height: 2.55rem;
        background: rgba(255, 255, 255, 0.92) !important;
        color: #514568 !important;
        border: 1px solid rgba(122, 90, 248, 0.18) !important;
        box-shadow: 0 10px 22px rgba(122, 90, 248, 0.12);
    }

    div[data-testid="stVerticalBlock"]:has(.feature-card-home) div[data-testid="stButton"] > button {
        min-height: 2.65rem;
        font-size: 0.98rem;
        border-radius: 999px !important;
        background:
            radial-gradient(circle at top left, rgba(255, 221, 231, 0.55) 0%, transparent 48%),
            radial-gradient(circle at bottom right, rgba(234, 246, 255, 0.62) 0%, transparent 48%),
            rgba(255, 255, 255, 0.90) !important;
        border: 1px solid rgba(122, 90, 248, 0.14) !important;
        box-shadow: 0 10px 22px rgba(88, 72, 124, 0.07) !important;
        color: #3A3444 !important;
    }

    div[data-testid="stButton"] > button:hover,
    div[data-testid="stFormSubmitButton"] > button:hover {
        background: #F8FBFF !important;
        color: #2F2A38 !important;
        border-color: rgba(122, 90, 248, 0.28) !important;
    }

    @media (max-width: 768px) {
        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .login-shell {
            margin-top: 0.6rem;
        }

        .login-brand-card {
            min-height: auto;
            padding: 1.6rem;
        }

        .login-brand-card h1 {
            font-size: 2.2rem;
        }

        .home-hero {
            padding: 1.6rem;
        }

        .home-hero h1 {
            font-size: 1.85rem;
        }

        .home-section-header {
            display: block;
        }

        .feature-panel {
            min-height: auto;
            padding: 1.35rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ======================
# Navigation Helpers
# ======================
def initialize_page_state():
    """Prepare authentication and active page values."""
    if "is_authenticated" not in st.session_state:
        st.session_state.is_authenticated = False

    if "auth_mode" not in st.session_state:
        st.session_state.auth_mode = "login"

    if "active_page" not in st.session_state:
        st.session_state.active_page = "Home"

    if "user_name" not in st.session_state:
        st.session_state.user_name = ""

    if "user_type" not in st.session_state:
        st.session_state.user_type = ""

    if "medical_role" not in st.session_state:
        st.session_state.medical_role = ""

    if "registered_users" not in st.session_state:
        st.session_state.registered_users = {}

    if st.session_state.active_page not in PAGES:
        st.session_state.active_page = "Home"


def authenticate_user(name, password, login_user_type):
    """Validate login using registered account and selected user type."""
    username = name.strip().lower()

    if not username or not password.strip():
        return False, "Nama dan password harus diisi."

    if username not in st.session_state.registered_users:
        return False, "Akun belum terdaftar. Silakan daftar terlebih dahulu."

    account = st.session_state.registered_users[username]

    if account["password"] != password:
        return False, "Password tidak sesuai."

    if account["user_type"] != login_user_type:
        return False, (
            f"Akun ini terdaftar sebagai {account['user_type']}, "
            f"bukan {login_user_type}."
        )

    return True, ""


def register_user(name, password, confirm_password, user_type, medical_role):
    """Register new user account in session state."""
    username = name.strip().lower()

    if not username or not password.strip() or not confirm_password.strip():
        return False, "Nama, password, dan konfirmasi password harus diisi."

    if password != confirm_password:
        return False, "Konfirmasi password tidak sesuai."

    if username in st.session_state.registered_users:
        return False, "Akun dengan nama tersebut sudah terdaftar."

    st.session_state.registered_users[username] = {
        "display_name": name.strip(),
        "password": password,
        "user_type": user_type,
        "medical_role": medical_role,
    }

    return True, ""


def go_to_page(page_name):
    """Move to the selected page and refresh the interface."""
    st.session_state.active_page = page_name
    st.rerun()


# ======================
# Authentication Page
# ======================
def render_login():
    """Render login and registration page before entering Audore."""
    st.markdown(
        """
        <style>
        section[data-testid="stSidebar"] {
            display: none !important;
        }

        .block-container {
            max-width: 1120px;
            padding-top: 1.2rem;
        }

        div[data-testid="stForm"] {
            min-height: 520px;
            background:
                radial-gradient(circle at top right, rgba(234, 246, 255, 0.65) 0%, transparent 42%),
                rgba(255, 255, 255, 0.94) !important;
            border: 1px solid rgba(122, 90, 248, 0.12) !important;
            border-radius: 28px !important;
            box-shadow: 0 24px 60px rgba(88, 72, 124, 0.10) !important;
            padding: 2.1rem !important;
        }

        div[data-testid="stForm"] > div {
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="login-shell">', unsafe_allow_html=True)

    left_col, right_col = st.columns([1.05, 0.95], gap="large")

    with left_col:
        st.markdown(
            """
            <div class="login-brand-card">
                <div class="login-badge">Audore Assistant</div>
                <h1>Audore</h1>
                <p>
                    Pendamping digital bagi caregiver anak dengan Autism
                    Spectrum Disorder.
                </p>
                <div class="login-info-grid">
                    <div class="login-info-item">
                        Akses caregiver untuk menggunakan fitur pendampingan,
                        edukasi, komunitas, dan penjadwalan konsultasi.
                    </div>
                    <div class="login-info-item">
                        Akses tenaga medis untuk melihat daftar pasien
                        konsultasi sesuai peran profesional.
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right_col:
        if st.session_state.auth_mode == "login":
            with st.form("login_form"):
                st.markdown(
                    """
                    <div class="login-form-title">
                        <h2>Masuk Akun</h2>
                        <p>Masukkan nama, password, dan jenis akun yang sudah terdaftar.</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                name = st.text_input("Nama", key="login_name")

                password = st.text_input(
                    "Password",
                    type="password",
                    key="login_password",
                )

                login_user_type = st.radio(
                    "Masuk sebagai",
                    ["Caregiver", "Tenaga Medis"],
                    horizontal=True,
                    key="login_user_type",
                )

                submitted = st.form_submit_button(
                    "Masuk",
                    use_container_width=True,
                )

                st.markdown(
                    """
                    <div class="auth-note">
                        Belum punya akun?
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                switch_to_register = st.form_submit_button(
                    "Daftar",
                    use_container_width=True,
                )

            if switch_to_register:
                st.session_state.auth_mode = "register"
                st.rerun()

            if submitted:
                is_valid, message = authenticate_user(
                    name,
                    password,
                    login_user_type,
                )

                if is_valid:
                    username = name.strip().lower()
                    account = st.session_state.registered_users[username]

                    st.session_state.is_authenticated = True
                    st.session_state.user_name = account["display_name"]
                    st.session_state.user_type = account["user_type"]
                    st.session_state.medical_role = account["medical_role"]

                    if account["user_type"] == "Tenaga Medis":
                        st.session_state.active_page = "Konsultasi"
                        st.session_state.halaman_konsultasi = "home"
                    else:
                        st.session_state.active_page = "Home"

                    st.rerun()

                st.error(message)

        else:
            with st.form("register_form"):
                st.markdown(
                    """
                    <div class="login-form-title">
                        <h2>Daftar Akun</h2>
                        <p>Buat akun baru untuk menggunakan fitur Audore.</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                register_name = st.text_input("Nama", key="register_name")

                register_password = st.text_input(
                    "Password",
                    type="password",
                    key="register_password",
                )

                confirm_password = st.text_input(
                    "Konfirmasi Password",
                    type="password",
                    key="confirm_password",
                )

                register_user_type = st.radio(
                    "Daftar sebagai",
                    ["Caregiver", "Tenaga Medis"],
                    horizontal=True,
                    key="register_user_type",
                )

                register_medical_role = ""
                if register_user_type == "Tenaga Medis":
                    register_medical_role = st.selectbox(
                        "Jenis Tenaga Medis",
                        [
                            "Psikolog",
                            "Dokter Spesialis Kedokteran Jiwa",
                        ],
                        key="register_medical_role",
                    )

                registered = st.form_submit_button(
                    "Daftar dan Masuk",
                    use_container_width=True,
                )

                st.markdown(
                    """
                    <div class="auth-note">
                        Sudah punya akun?
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                switch_to_login = st.form_submit_button(
                    "Masuk",
                    use_container_width=True,
                )

            if switch_to_login:
                st.session_state.auth_mode = "login"
                st.rerun()

            if registered:
                is_registered, message = register_user(
                    register_name,
                    register_password,
                    confirm_password,
                    register_user_type,
                    register_medical_role,
                )

                if is_registered:
                    st.session_state.is_authenticated = True
                    st.session_state.user_name = register_name.strip()
                    st.session_state.user_type = register_user_type
                    st.session_state.medical_role = register_medical_role

                    if register_user_type == "Tenaga Medis":
                        st.session_state.active_page = "Konsultasi"
                        st.session_state.halaman_konsultasi = "home"
                    else:
                        st.session_state.active_page = "Home"

                    st.success("Akun berhasil dibuat.")
                    st.rerun()

                st.error(message)

    st.markdown("</div>", unsafe_allow_html=True)


# ======================
# Sidebar
# ======================
def render_sidebar():
    """Render compact and styled sidebar navigation."""
    role_label = (
        st.session_state.medical_role
        if st.session_state.user_type == "Tenaga Medis"
        else "Caregiver"
    )

    safe_user_name = html.escape(st.session_state.user_name)
    safe_role_label = html.escape(role_label)

    st.sidebar.markdown(
        """
        <div class="sidebar-brand">
            <h2>Audore</h2>
            <p>Pendamping digital bagi caregiver anak dengan Autism Spectrum Disorder.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.markdown(
        f"""
        <div class="sidebar-profile">
            <div class="sidebar-profile-label">Profil pengguna</div>
            <div class="sidebar-profile-name">{safe_user_name}</div>
            <div class="sidebar-profile-role">{safe_role_label}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.markdown(
        '<div class="sidebar-menu-title">Menu</div>',
        unsafe_allow_html=True,
    )

    selected_page = st.sidebar.radio(
        "Menu",
        PAGES,
        index=PAGES.index(st.session_state.active_page),
        label_visibility="collapsed",
    )

    if selected_page != st.session_state.active_page:
        st.session_state.active_page = selected_page
        st.rerun()

    if st.sidebar.button("Keluar", use_container_width=True):
        st.session_state.is_authenticated = False
        st.session_state.active_page = "Home"
        st.session_state.user_name = ""
        st.session_state.user_type = ""
        st.session_state.medical_role = ""
        st.session_state.auth_mode = "login"
        st.rerun()


# ======================
# Page Components
# ======================
def render_feature_card(page_name):
    """Render one feature card with the button inside the same visual container."""
    feature = FEATURES[page_name]
    feature_meta = {
        "Audore Assistant": ("feature-pink", "Identifikasi"),
        "Edukasi": ("feature-yellow", "Edukasi ASD"),
        "Konsultasi": ("feature-blue", "Konsultasi"),
        "Komunitas": ("feature-purple", "Komunitas"),
    }[page_name]
    feature_style, feature_badge = feature_meta

    with st.container():
        st.markdown(
            f"""
            <div
                class="feature-card-home {feature_style}"
                style="--feature-color: {feature['color']}; --feature-accent: {feature['accent']};"
            >
                <div class="feature-badge">{feature_badge}</div>
                <div class="feature-title">{page_name}</div>
                <p class="feature-description">{feature['description']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button(
            "Buka",
            key=f"open_{page_name}",
            type=feature["button_type"],
            use_container_width=True,
        ):
            go_to_page(page_name)


def render_home():
    """Render Audore home page."""
    user_name = html.escape(st.session_state.user_name or "Pengguna")

    st.markdown(
        f"""
        <div class="home-hero">
            <div class="login-badge">Audore Assistant</div>
            <h1>Selamat Datang, {user_name}</h1>
            <p>
                Pilih fitur yang ingin digunakan untuk mendukung pendampingan,
                edukasi, konsultasi, dan komunikasi dalam komunitas Audore.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="home-section-header">
            <h2 class="home-section-title">Akses Fitur</h2>
            <p class="home-section-subtitle">
                Semua fitur utama tersedia dalam satu ruang kerja yang sederhana dan mudah digunakan.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    first_col, second_col = st.columns(2, gap="large")
    with first_col:
        render_feature_card("Audore Assistant")
    with second_col:
        render_feature_card("Edukasi")

    st.write("")

    third_col, fourth_col = st.columns(2, gap="large")
    with third_col:
        render_feature_card("Komunitas")
    with fourth_col:
        render_feature_card("Konsultasi")


# ======================
# Main Application
# ======================
def main():
    initialize_page_state()

    if not st.session_state.is_authenticated:
        render_login()
        return

    render_sidebar()

    active_page = st.session_state.active_page

    if active_page == "Home":
        render_home()
    elif active_page == "Audore Assistant":
        run_ml_app()
    elif active_page == "Edukasi":
        run_edukasi()
    elif active_page == "Konsultasi":
        run_konsultasi()
    elif active_page == "Komunitas":
        run_komunitas()


if __name__ == "__main__":
    main()
