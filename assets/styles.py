import streamlit as st


def load_css():
    st.markdown("""
<style>

/* =======================================================
   GOOGLE FONT
======================================================= */

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

*{
    font-family:'Poppins',sans-serif;
}

/* =======================================================
   MAIN APP
======================================================= */

.stApp{

    background:#f4f7fc;

    color:#1f2937;

}

/* =======================================================
   HEADINGS
======================================================= */

h1,h2,h3,h4,h5,h6{

    color:#111827 !important;

    font-weight:700;

}

p,label,span{

    color:#4b5563;

}

/* =======================================================
   HERO
======================================================= */

.hero{

    background:linear-gradient(
        135deg,
        #2563eb,
        #4f46e5
    );

    color:white;

    border-radius:22px;

    padding:28px 40px;

    margin-bottom:25px;

    box-shadow:
    0 15px 35px rgba(
        37,
        99,
        235,
        .25
    );

}

.hero h1{

    color:white !important;

    margin-bottom:12px;

    font-size:48px;

}

.hero p{

    color:#eef2ff !important;

    font-size:18px;

    line-height:1.7;

}

/* =======================================================
   DASHBOARD
======================================================= */

.metric-card{

    background:white;

    border-radius:20px;

    padding:20px;

    text-align:center;

    border:1px solid #e5e7eb;

    box-shadow:
    0 10px 30px rgba(
        0,
        0,
        0,
        .06
    );

    transition:.35s;

}

.metric-card:hover{

    transform:translateY(-6px);

    box-shadow:
    0 18px 35px rgba(
        37,
        99,
        235,
        .18
    );

}

.metric-number{

    font-size:32px;

    font-weight:700;

    color:#2563eb;

    margin-bottom:8px;

}

.metric-title{

    color:#6b7280;

    font-size:15px;

}

/* =======================================================
   SIDEBAR
======================================================= */

section[data-testid="stSidebar"]{

    background:white;

    border-right:1px solid #e5e7eb;

}

section[data-testid="stSidebar"] *{

    color:#1f2937 !important;

}

section[data-testid="stSidebar"] h1{

    color:#2563eb !important;

}

section[data-testid="stSidebar"] p{

    color:#6b7280 !important;

}

/* =======================================================
   BUTTONS
======================================================= */

.stButton>button{

    width:100%;

    height:48px;

    border:none;

    border-radius:12px;

    background:
    linear-gradient(
        90deg,
        #2563eb,
        #4f46e5
    );

    color:white !important;

    font-weight:600;

    transition:.3s;

}

.stButton>button:hover{

    transform:translateY(-2px);

    box-shadow:
    0 10px 20px rgba(
        37,
        99,
        235,
        .30
    );

}

/* =======================================================
   INPUT
======================================================= */

.stTextInput input{

    background:white !important;

    color:#111827 !important;

    border:1px solid #d1d5db;

    border-radius:12px;

    padding:12px;

}

.stTextInput input::placeholder{

    color:#9ca3af;

}
/* =======================================================
   CHAT
======================================================= */

.stChatMessage{

    background:white;

    border:1px solid #e5e7eb;

    border-radius:18px;

    padding:14px;

    margin-bottom:12px;

    box-shadow:
    0 4px 12px rgba(
        0,
        0,
        0,
        .05
    );

}

/* =======================================================
   INFO / SUCCESS / WARNING
======================================================= */

div[data-baseweb="notification"]{

    border-radius:16px;

    border:none;

}

div[data-baseweb="notification"] *{

    color:#111827 !important;

}

/* =======================================================
   METRICS
======================================================= */

div[data-testid="metric-container"]{

    background:white;

    border:1px solid #e5e7eb;

    border-radius:18px;

    padding:18px;

    box-shadow:
    0 6px 16px rgba(
        0,
        0,
        0,
        .06
    );

}

/* =======================================================
   DIVIDER
======================================================= */

hr{

    margin-top:28px;

    margin-bottom:28px;

}

/* =======================================================
   FOOTER
======================================================= */

.footer{

    margin-top:35px;

    padding:25px;

    text-align:center;

    color:#6b7280;

    border-top:1px solid #e5e7eb;

}

.footer h3,
.footer h4{

    color:#2563eb !important;

}

/* =======================================================
   SCROLLBAR
======================================================= */

::-webkit-scrollbar{

    width:8px;

}

::-webkit-scrollbar-track{

    background:#edf2f7;

}

::-webkit-scrollbar-thumb{

    background:#2563eb;

    border-radius:20px;

}

::-webkit-scrollbar-thumb:hover{

    background:#1d4ed8;

}

/* =======================================================
   RESPONSIVE
======================================================= */

@media(max-width:768px){

.hero{

    padding:22px;

}

.hero h1{

    font-size:34px;

}

.metric-number{

    font-size:26px;

}

.metric-card{

    margin-bottom:15px;

}

}

</style>
""",
        unsafe_allow_html=True,
    )
    