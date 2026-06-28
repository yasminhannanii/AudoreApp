import streamlit as st
import pandas as pd


def apply_consultation_style():
    """Apply Audore visual style to the consultation module."""
    st.markdown(
        """
        <style>
        .consultation-hero {
            background:
                radial-gradient(circle at top left, #FFDDE7 0%, transparent 38%),
                radial-gradient(circle at bottom right, #E9E1FF 0%, transparent 42%),
                rgba(255, 255, 255, 0.88);
            border: 1px solid rgba(122, 90, 248, 0.10);
            border-radius: 28px;
            box-shadow: 0 24px 58px rgba(88, 72, 124, 0.12);
            padding: 2.4rem 2.6rem;
            margin-bottom: 1rem;
        }

        .consultation-hero h1 {
            color: #111111;
            font-size: 2.45rem;
            font-weight: 800;
            margin: 0 0 0.45rem 0;
            letter-spacing: 0;
        }

        .consultation-hero p {
            color: #5F5870;
            font-size: 1.05rem;
            line-height: 1.7;
            margin: 0;
        }

        .consultation-kicker {
            display: inline-block;
            background: rgba(255, 255, 255, 0.76);
            border: 1px solid rgba(122, 90, 248, 0.14);
            border-radius: 999px;
            color: #514568;
            font-size: 0.86rem;
            font-weight: 700;
            padding: 0.42rem 0.85rem;
            margin-bottom: 1rem;
        }

        .consultation-summary-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.85rem;
            margin-top: 1.6rem;
        }

        .consultation-summary-item {
            background: rgba(255, 255, 255, 0.74);
            border: 1px solid rgba(122, 90, 248, 0.10);
            border-radius: 18px;
            padding: 1rem 1.1rem;
        }

        .consultation-summary-item strong {
            display: block;
            color: #111111;
            font-size: 1rem;
            margin-bottom: 0.28rem;
        }

        .consultation-summary-item span {
            color: #6A6278;
            font-size: 0.9rem;
            line-height: 1.5;
        }

        .consultation-section-heading {
            margin: 1.5rem 0 0.8rem 0;
        }

        .consultation-section-heading h2 {
            color: #111111;
            font-size: 1.35rem;
            font-weight: 800;
            margin: 0;
        }

        .consultation-section-heading p {
            color: #6A6278;
            font-size: 0.95rem;
            margin: 0.25rem 0 0 0;
        }

        .consultation-card-panel {
            position: relative;
            overflow: hidden;
            background: rgba(255, 255, 255, 0.88);
            border: 1px solid rgba(122, 90, 248, 0.10);
            border-radius: 22px;
            padding: 1.35rem;
            min-height: 14.2rem;
            box-shadow: 0 18px 38px rgba(88, 72, 124, 0.10);
        }

        .consultation-card-panel::before {
            content: "";
            position: absolute;
            inset: 0 0 auto 0;
            height: 5rem;
        }

        .consultation-card-panel > * {
            position: relative;
            z-index: 1;
        }

        .consultation-card-pink::before {
            background:
                radial-gradient(circle at top left, rgba(229, 214, 206, 0.78) 0%, transparent 48%),
                linear-gradient(135deg, #F8F3F0 0%, rgba(255, 255, 255, 0.50) 100%);
        }

        .consultation-card-green::before {
            background:
                radial-gradient(circle at top left, rgba(229, 214, 206, 0.78) 0%, transparent 48%),
                linear-gradient(135deg, #F8F3F0 0%, rgba(255, 255, 255, 0.50) 100%);
        }

        .consultation-card-top {
            display: flex;
            gap: 0.9rem;
            align-items: flex-start;
            margin-bottom: 1.6rem;
        }

        .consultation-icon {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 2.65rem;
            height: 2.65rem;
            border-radius: 16px;
            background: rgba(255, 255, 255, 0.74);
            border: 1px solid rgba(255, 255, 255, 0.82);
            color: #6B5B52;
            font-size: 0.82rem;
            font-weight: 800;
        }

        .consultation-tag {
            display: inline-block;
            background: rgba(255, 255, 255, 0.66);
            border: 1px solid rgba(255, 255, 255, 0.78);
            border-radius: 999px;
            color: #6B5B52;
            font-size: 0.76rem;
            font-weight: 700;
            padding: 0.3rem 0.68rem;
            margin-bottom: 0.52rem;
        }

        .consultation-accent {
            width: 2.7rem;
            height: 0.28rem;
            border-radius: 999px;
            margin: 0 0 0.82rem 0;
        }

        .consultation-card-title {
            color: #2F2A38;
            font-size: 1.28rem;
            font-weight: 800;
            margin: 0;
            letter-spacing: 0;
            line-height: 1.25;
        }

        .consultation-card-description {
            color: #5F5870;
            font-size: 0.94rem;
            line-height: 1.6;
            margin: 0.35rem 0 1rem 0;
            min-height: 4.5rem;
        }

        .consultation-chip-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.45rem;
            margin-top: 0.8rem;
        }

        .consultation-chip-row span {
            background: rgba(255, 255, 255, 0.68);
            border: 1px solid rgba(122, 90, 248, 0.08);
            border-radius: 999px;
            color: #7A6A61;
            font-size: 0.8rem;
            font-weight: 600;
            padding: 0.38rem 0.7rem;
        }

        .consultation-soft-card {
            background:
                radial-gradient(circle at top left, rgba(255, 221, 231, 0.72) 0%, transparent 42%),
                radial-gradient(circle at bottom right, rgba(221, 248, 234, 0.72) 0%, transparent 42%),
                rgba(255, 255, 255, 0.88);
            border: 1px solid rgba(122, 90, 248, 0.10);
            border-radius: 24px;
            box-shadow: 0 18px 42px rgba(88, 72, 124, 0.10);
            padding: 1.55rem;
            margin: 0.75rem 0 1.1rem 0;
        }

        .consultation-soft-card h2 {
            color: #111111;
            font-size: 1.45rem;
            font-weight: 800;
            margin: 0 0 0.45rem 0;
            letter-spacing: 0;
        }

        .consultation-soft-card p {
            color: #5F5870;
            line-height: 1.65;
            margin: 0;
        }

        .consultation-detail-card {
            background: rgba(255, 255, 255, 0.86);
            border: 1px solid rgba(122, 90, 248, 0.10);
            border-radius: 22px;
            box-shadow: 0 16px 34px rgba(88, 72, 124, 0.09);
            padding: 1.35rem 1.45rem;
            margin-top: 1rem;
        }

        .consultation-detail-card strong {
            color: #2F2A38;
        }

        div[data-testid="stButton"] > button {
            border-radius: 999px;
            font-weight: 700;
            min-height: 2.65rem;
            box-shadow: 0 10px 22px rgba(122, 90, 248, 0.12);
        }

        div[data-testid="stButton"] > button[kind="secondary"] {
            background: rgba(255, 255, 255, 0.92);
            color: #3A2E3F;
            border: 1px solid rgba(122, 90, 248, 0.18);
        }

        div[data-testid="stVerticalBlockBorderWrapper"] {
            border: none !important;
            background: transparent !important;
        }

        @media (max-width: 760px) {
            .consultation-hero {
                padding: 1.7rem;
                border-radius: 22px;
            }

            .consultation-hero h1 {
                font-size: 2rem;
            }

            .consultation-summary-grid {
                grid-template-columns: 1fr;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def initialize_consultation_state():
    """Prepare consultation session data."""
    if "halaman_konsultasi" not in st.session_state:
        st.session_state.halaman_konsultasi = "home"

    if "dokter" not in st.session_state:
        st.session_state.dokter = ""

    if "jenis_layanan" not in st.session_state:
        st.session_state.jenis_layanan = ""

    if "daftar_konsultasi" not in st.session_state:
        st.session_state.daftar_konsultasi = []


def add_consultation(service_type, doctor, date, time):
    """Add consultation booking to session state."""
    patient_name = st.session_state.get("user_name", "Pengguna")

    consultation = {
        "Nama Pasien": patient_name,
        "Layanan": service_type,
        "Tenaga Profesional": doctor,
        "Tanggal": str(date),
        "Jam": time,
        "Status": "Terjadwal",
    }

    st.session_state.daftar_konsultasi.append(consultation)


def render_consultation_home():
    """Render consultation service selection for caregiver."""
    user_name = st.session_state.get("user_name", "Pengguna")

    st.markdown(
        f"""
        <div class="consultation-hero">
            <div class="consultation-kicker">Konsultasi Audore</div>
            <h1>Ruang Konsultasi, {user_name}</h1>
            <p>
                Pilih layanan profesional yang sesuai untuk membantu menjaga
                kesehatan mental caregiver selama proses pendampingan anak.
            </p>
            <div class="consultation-summary-grid">
                <div class="consultation-summary-item">
                    <strong>Layanan</strong>
                    <span>Psikolog klinis dan dokter spesialis kedokteran jiwa.</span>
                </div>
                <div class="consultation-summary-item">
                    <strong>Alur</strong>
                    <span>Pilih layanan, pilih tenaga profesional, lalu atur jadwal.</span>
                </div>
                <div class="consultation-summary-item">
                    <strong>Status</strong>
                    <span>Jadwal tersimpan di daftar konsultasi Audore.</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="consultation-section-heading">
            <h2>Rekomendasi Layanan</h2>
            <p>Gunakan pilihan berikut sesuai kebutuhan pendampingan Anda.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2, gap="large")

    with col1:
        with st.container():
            st.markdown(
                """
                <div class="consultation-card-panel consultation-card-pink">
                    <div class="consultation-card-top">
                        <div class="consultation-icon">01</div>
                        <div>
                            <div class="consultation-tag">Dukungan psikologis</div>
                        </div>
                    </div>
                    <div class="consultation-accent" style="background:#CDB8AD;"></div>
                    <div class="consultation-card-title">Psikolog Klinis Dewasa</div>
                    <p class="consultation-card-description">
                        Konsultasi terkait stres, kecemasan, kelelahan emosional,
                        dan strategi regulasi diri selama mendampingi anak ASD.
                    </p>
                    <div class="consultation-chip-row">
                        <span>Stres caregiver</span>
                        <span>Regulasi emosi</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if st.button(
                "Pilih Psikolog",
                key="pilih_psikolog",
                type="secondary",
                use_container_width=True,
            ):
                st.session_state.halaman_konsultasi = "psikolog"
                st.rerun()

    with col2:
        with st.container():
            st.markdown(
                """
                <div class="consultation-card-panel consultation-card-green">
                    <div class="consultation-card-top">
                        <div class="consultation-icon">02</div>
                        <div>
                            <div class="consultation-tag">Evaluasi medis</div>
                        </div>
                    </div>
                    <div class="consultation-accent" style="background:#CDB8AD;"></div>
                    <div class="consultation-card-title">Dokter Spesialis Kedokteran Jiwa</div>
                    <p class="consultation-card-description">
                        Konsultasi terkait kondisi kesehatan mental yang memerlukan
                        evaluasi medis, diagnosis, dan terapi sesuai kebutuhan.
                    </p>
                    <div class="consultation-chip-row">
                        <span>Evaluasi klinis</span>
                        <span>Terapi medis</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if st.button(
                "Pilih Psikiater",
                key="pilih_psikiater",
                type="secondary",
                use_container_width=True,
            ):
                st.session_state.halaman_konsultasi = "psikiater"
                st.rerun()


def render_psychologist_selection():
    """Render psychologist selection."""
    if st.button("Kembali", type="secondary"):
        st.session_state.halaman_konsultasi = "home"
        st.rerun()

    st.markdown(
        """
        <div class="consultation-soft-card">
            <div class="consultation-kicker">Pilih Profesional</div>
            <h2>Psikolog Klinis Dewasa</h2>
            <p>
                Pilih psikolog yang ingin ditemui, lalu lanjutkan ke pengaturan
                tanggal dan jam konsultasi.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    doctor = st.selectbox(
        "Pilih Psikolog",
        [
            "Rafael, M.Psi.",
            "Anaya, M.Psi.",
            "Bara, M.Psi.",
        ],
    )

    if st.button("Lanjut", type="secondary", use_container_width=True):
        st.session_state.dokter = doctor
        st.session_state.jenis_layanan = "Psikolog"
        st.session_state.halaman_konsultasi = "jadwal"
        st.rerun()


def render_psychiatrist_selection():
    """Render psychiatrist selection."""
    if st.button("Kembali", type="secondary"):
        st.session_state.halaman_konsultasi = "home"
        st.rerun()

    st.markdown(
        """
        <div class="consultation-soft-card">
            <div class="consultation-kicker">Pilih Profesional</div>
            <h2>Dokter Spesialis Kedokteran Jiwa</h2>
            <p>
                Pilih dokter yang ingin ditemui, lalu lanjutkan ke pengaturan
                tanggal dan jam konsultasi.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    doctor = st.selectbox(
        "Pilih Dokter",
        [
            "dr. Tanya, Sp.KJ",
            "dr. Khanaya, Sp.KJ",
            "dr. Fiona, Sp.KJ",
        ],
    )

    if st.button("Lanjut", type="secondary", use_container_width=True):
        st.session_state.dokter = doctor
        st.session_state.jenis_layanan = "Dokter Spesialis Kedokteran Jiwa"
        st.session_state.halaman_konsultasi = "jadwal"
        st.rerun()


def render_schedule_page():
    """Render consultation schedule page."""
    if st.button("Kembali", type="secondary"):
        st.session_state.halaman_konsultasi = "home"
        st.rerun()

    doctor = st.session_state.get("dokter", "")
    service_type = st.session_state.get("jenis_layanan", "")

    st.markdown(
        f"""
        <div class="consultation-soft-card">
            <div class="consultation-kicker">Atur Jadwal</div>
            <h2>Jadwal Konsultasi</h2>
            <p>
                Tenaga profesional: <strong>{doctor}</strong><br>
                Layanan: <strong>{service_type}</strong>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    date = st.date_input("Pilih Tanggal")

    time = st.selectbox(
        "Pilih Jam",
        [
            "09:00",
            "10:00",
            "11:00",
            "13:00",
            "14:00",
            "15:00",
        ],
    )

    if st.button("Konfirmasi Jadwal", type="secondary", use_container_width=True):
        add_consultation(service_type, doctor, date, time)

        st.success(
            f"""
            Konsultasi berhasil dijadwalkan.

            Nama Pasien: {st.session_state.get("user_name", "Pengguna")}

            Tenaga Profesional: {doctor}

            Tanggal: {date}

            Jam: {time}
            """
        )


def render_medical_dashboard():
    """Render consultation list for medical users."""
    user_name = st.session_state.get("user_name", "Tenaga Medis")
    medical_role = st.session_state.get("medical_role", "Tenaga Medis")

    st.markdown(
        f"""
        <div class="consultation-hero">
            <div class="consultation-kicker">Dashboard Konsultasi</div>
            <h1>Daftar Pasien Konsultasi</h1>
            <p>
                Selamat datang, {user_name}. Halaman ini menampilkan jadwal
                pasien sesuai peran login Anda sebagai {medical_role}.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    consultations = st.session_state.get("daftar_konsultasi", [])

    if not consultations:
        st.info("Belum ada pasien yang menjadwalkan konsultasi.")
        return

    data = pd.DataFrame(consultations)

    if medical_role == "Psikolog":
        data = data[data["Layanan"] == "Psikolog"]

    if medical_role == "Dokter Spesialis Kedokteran Jiwa":
        data = data[data["Layanan"] == "Dokter Spesialis Kedokteran Jiwa"]

    if data.empty:
        st.info("Belum ada jadwal konsultasi untuk peran ini.")
        return

    st.markdown(
        """
        <div class="consultation-section-heading">
            <h2>Ringkasan Jadwal</h2>
            <p>Daftar konsultasi yang sudah dijadwalkan oleh pengguna.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.dataframe(data, use_container_width=True, hide_index=True)

    st.markdown(
        """
        <div class="consultation-section-heading">
            <h2>Detail Pasien</h2>
            <p>Pilih satu pasien untuk melihat informasi jadwal konsultasi.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    selected_patient = st.selectbox(
        "Pilih pasien",
        data["Nama Pasien"].tolist(),
    )

    selected_data = data[data["Nama Pasien"] == selected_patient].iloc[0]

    st.markdown(
        f"""
        <div class="consultation-detail-card">
            <p><strong>Nama Pasien:</strong> {selected_data["Nama Pasien"]}</p>
            <p><strong>Layanan:</strong> {selected_data["Layanan"]}</p>
            <p><strong>Tenaga Profesional:</strong> {selected_data["Tenaga Profesional"]}</p>
            <p><strong>Tanggal:</strong> {selected_data["Tanggal"]}</p>
            <p><strong>Jam:</strong> {selected_data["Jam"]}</p>
            <p><strong>Status:</strong> {selected_data["Status"]}</p>
        </div>
        """
        ,
        unsafe_allow_html=True,
    )


def render_caregiver_consultation():
    """Render consultation workflow for caregiver users."""
    if st.session_state.halaman_konsultasi == "home":
        render_consultation_home()
    elif st.session_state.halaman_konsultasi == "psikolog":
        render_psychologist_selection()
    elif st.session_state.halaman_konsultasi == "psikiater":
        render_psychiatrist_selection()
    elif st.session_state.halaman_konsultasi == "jadwal":
        render_schedule_page()


def run_konsultasi():
    apply_consultation_style()
    initialize_consultation_state()

    user_type = st.session_state.get("user_type", "Caregiver")

    if user_type == "Tenaga Medis":
        render_medical_dashboard()
    else:
        render_caregiver_consultation()
