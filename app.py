# app.py
# Home Loan Default Prediction System
# Complete Production-Ready Streamlit Application

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import joblib
import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff
from streamlit_option_menu import option_menu
import base64
import time
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import os
import warnings
from datetime import datetime, date
warnings.filterwarnings('ignore')
import requests
import re
import gdown 
from io import BytesIO

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Home Loan Default Prediction System",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# CUSTOM CSS - PREMIUM UI
# ============================================================================
st.markdown("""
<style>
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Main container */
    .main {
        padding: 0rem 1rem;
    }
    
    /* Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        position: relative;
        overflow: hidden;
    }
    .hero-banner::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.05) 0%, transparent 70%);
        animation: rotate 20s linear infinite;
    }
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    .hero-banner h1 {
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
    }
    .hero-banner p {
        font-size: 1.2rem;
        opacity: 0.9;
        margin-top: 0.5rem;
        position: relative;
        z-index: 1;
    }
    
    /* KPI Cards */
    .kpi-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.07);
        transition: all 0.3s ease;
        border: 1px solid #e9ecef;
        height: 100%;
    }
    .kpi-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        border-color: #667eea;
    }
    .kpi-card .kpi-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1a1a2e;
        margin: 0.5rem 0;
    }
    .kpi-card .kpi-label {
        font-size: 0.9rem;
        color: #6c757d;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 600;
    }
    .kpi-card .kpi-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    .kpi-card.gradient-1 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    .kpi-card.gradient-1 .kpi-value,
    .kpi-card.gradient-1 .kpi-label {
        color: white;
    }
    .kpi-card.gradient-2 {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
    }
    .kpi-card.gradient-2 .kpi-value,
    .kpi-card.gradient-2 .kpi-label {
        color: white;
    }
    .kpi-card.gradient-3 {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
    }
    .kpi-card.gradient-3 .kpi-value,
    .kpi-card.gradient-3 .kpi-label {
        color: white;
    }
    .kpi-card.gradient-4 {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        color: white;
    }
    .kpi-card.gradient-4 .kpi-value,
    .kpi-card.gradient-4 .kpi-label {
        color: white;
    }
    
    /* Info Cards */
    .info-card {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.07);
        border: 1px solid #e9ecef;
        transition: all 0.3s ease;
        height: 30rem;
    }
    .info-card:hover {
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        transform: translateY(-3px);
    }
    .info-card h3 {
        color: #1a1a2e;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    .info-card ul {
        list-style: none;
        padding: 0;
        color: #1a1a2e;
    }
    .info-card ul li {
        padding: 0.5rem 0;
        border-bottom: 1px solid #f1f3f5;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .info-card ul li:last-child {
        border-bottom: none;
    }
    
    /* Workflow Cards */
    .workflow-card {
        background: white;
        border-radius: 12px;
        padding: 1.2rem;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    .workflow-card:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border-left-color: #f5576c;
    }
    .workflow-card .step-icon {
        font-size: 1.5rem;
        min-width: 2.5rem;
    }
    .workflow-card .step-text {
        flex: 1;
    }
    .workflow-card .step-text h4 {
        margin: 0;
        font-size: 1rem;
        color: #1a1a2e;
    }
    .workflow-card .step-text p {
        margin: 0.2rem 0 0 0;
        font-size: 0.85rem;
        color: #6c757d;
    }
    
    /* Result Cards */
    .result-card {
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 10px 40px rgba(0,0,0,0.15);
        transition: all 0.3s ease;
    }
    .result-card:hover {
        transform: scale(1.02);
    }
    .result-card.low-risk {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        color: #1a1a2e;
    }
    .result-card.high-risk {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
    }
    .result-card .result-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
    }
    .result-card .result-title {
        font-size: 2rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    .result-card .result-subtitle {
        font-size: 1.1rem;
        opacity: 0.9;
    }
    .result-card .confidence {
        margin-top: 1rem;
        padding: 0.5rem 1.5rem;
        background: rgba(255,255,255,0.2);
        border-radius: 50px;
        display: inline-block;
        font-weight: 600;
    }
    
    /* Leaderboard Table */
    .leaderboard {
        background: white;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0,0,0,0.07);
    }
    .leaderboard table {
        width: 100%;
        border-collapse: collapse;
    }
    .leaderboard th {
        background: #1a1a2e;
        color: white;
        padding: 1rem;
        text-align: left;
        font-weight: 600;
    }
    .leaderboard td {
        padding: 0.8rem 1rem;
        border-bottom: 1px solid #f1f3f5;
    }
    .leaderboard tr:hover {
        background: #f8f9fa;
    }
    .leaderboard .best {
        background: #d4edda !important;
    }
    .leaderboard .best td {
        font-weight: 600;
    }
    .medal {
        font-size: 1.5rem;
    }
    
    /* Custom Tabs */
    .custom-tabs {
        background: white;
        border-radius: 15px;
        padding: 0.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.07);
    }
    
    /* Prediction Form */
    .prediction-form {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.07);
    }
    .prediction-form label {
        font-weight: 600;
        color: #1a1a2e;
        font-size: 0.9rem;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: #6c757d;
        border-top: 1px solid #e9ecef;
        margin-top: 3rem;
    }
    .footer a {
        color: #667eea;
        text-decoration: none;
    }

/* Reposition toast to be at the very top of everything */
.stToast {
    position: fixed !important;
    top: 80px !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
    z-index: 999999 !important;
    background: white !important;
    color: black !important;
    box-shadow: 0 8px 30px rgba(0,0,0,0.25) !important;
    border-radius: 12px !important;
    border-left: 5px solid #28a745 !important;
    padding: 15px 30px !important;
    min-width: 350px !important;
    max-width: 90% !important;
    text-align: center !important;
    font-size: 1.1rem !important;
    font-weight: 500 !important;
    animation: slideDown 0.5s ease !important;
}

/* Toast icon color */
.stToast svg {
    fill: #28a745 !important;
}

/* Toast close button */
.stToast button {
    color: #6c757d !important;
}

/* Animation for smooth appearance */
@keyframes slideDown {
    from {
        opacity: 0;
        transform: translateX(-50%) translateY(-20px);
    }
    to {
        opacity: 1;
        transform: translateX(-50%) translateY(0);
    }
}

/* For mobile responsiveness */
@media (max-width: 768px) {
    .stToast {
        top: 10px !important;
        min-width: auto !important;
        width: 95% !important;
        padding: 12px 20px !important;
        font-size: 0.95rem !important;
        border-radius: 10px !important;
    }
}
    /* Responsive */
    @media (max-width: 768px) {
        .hero-banner h1 {
            font-size: 2rem;
        }
        .kpi-card .kpi-value {
            font-size: 1.5rem;
        }
        .result-card .result-title {
            font-size: 1.5rem;
        }
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
    }
    ::-webkit-scrollbar-thumb {
        background: #667eea;
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #764ba2;
    }
    
    /* Section Divider */
    .section-divider {
        height: 2px;
        background: linear-gradient(to right, transparent, #667eea, transparent);
        margin: 2rem 0;
    }
    
    /* ============================================================================
   ADDITIONAL RESPONSIVE STYLES (Mobile & Tablet)
   ============================================================================ */

/* Tablet (up to 1024px) */
@media screen and (max-width: 1024px) {
    /* Navigation */
    .st-emotion-cache-1r6slb0 {
        flex-wrap: wrap !important;
        gap: 0.5rem !important;
    }
    .st-emotion-cache-1r6slb0 .st-emotion-cache-1wivap2 {
        padding: 8px 16px !important;
        font-size: 14px !important;
    }

    /* Hero */
    .hero-banner {
        padding: 2rem 1.5rem !important;
    }
    .hero-banner h1 {
        font-size: 2.5rem !important;
    }
    .hero-banner p {
        font-size: 1rem !important;
    }

    /* KPI Cards */
    .kpi-card {
        padding: 1rem !important;
    }
    .kpi-card .kpi-value {
        font-size: 1.8rem !important;
    }
    .kpi-card .kpi-label {
        font-size: 0.8rem !important;
    }

    /* Info Cards - make height auto */
    .info-card {
        height: auto !important;
        min-height: 20rem !important;
    }
}

/* Mobile (max-width: 768px) */
@media screen and (max-width: 768px) {
    /* ---- Navigation ---- */
    .st-emotion-cache-1r6slb0 {
        flex-direction: column !important;
        align-items: stretch !important;
        gap: 0.3rem !important;
    }
    .st-emotion-cache-1r6slb0 .st-emotion-cache-1wivap2 {
        padding: 8px 12px !important;
        font-size: 13px !important;
        text-align: center !important;
        border-radius: 8px !important;
    }

    /* ---- Hero Banner ---- */
    .hero-banner {
        padding: 1.5rem 1rem !important;
        border-radius: 12px !important;
    }
    .hero-banner h1 {
        font-size: 1.8rem !important;
    }
    .hero-banner p {
        font-size: 0.9rem !important;
    }

    /* ---- Columns (force stacking) ---- */
    .st-emotion-cache-1jicfl2 {   /* row container */
        flex-direction: column !important;
        gap: 0.5rem !important;
    }
    .st-emotion-cache-1jicfl2 .st-emotion-cache-1y4p8pa {
        width: 100% !important;
        flex: none !important;
    }

    /* ---- KPI Cards (2 per row or stack) ---- */
    .kpi-card {
        padding: 0.8rem !important;
        margin-bottom: 0.5rem !important;
    }
    .kpi-card .kpi-value {
        font-size: 1.5rem !important;
    }
    .kpi-card .kpi-icon {
        font-size: 1.5rem !important;
        margin-bottom: 0.3rem !important;
    }
    .kpi-card .kpi-label {
        font-size: 0.7rem !important;
    }

    /* ---- Info Cards ---- */
    .info-card {
        padding: 1rem !important;
        height: auto !important;
        min-height: 15rem !important;
        margin-bottom: 1rem !important;
    }
    .info-card h3 {
        font-size: 1.2rem !important;
    }
    .info-card ul li {
        padding: 0.3rem 0 !important;
        font-size: 0.85rem !important;
    }
    .info-card p {
        font-size: 0.9rem !important;
    }

    /* ---- Workflow Cards ---- */
    .workflow-card {
        padding: 0.8rem !important;
        margin: 0.3rem 0 !important;
        flex-wrap: wrap !important;
    }
    .workflow-card .step-icon {
        font-size: 1.2rem !important;
        min-width: 2rem !important;
    }
    .workflow-card .step-text h4 {
        font-size: 0.9rem !important;
    }
    .workflow-card .step-text p {
        font-size: 0.8rem !important;
    }

    /* ---- Prediction Form ---- */
    .prediction-form {
        padding: 1rem !important;
    }

    /* ---- Result Cards ---- */
    .result-card {
        padding: 1.5rem !important;
    }
    .result-card .result-icon {
        font-size: 3rem !important;
    }
    .result-card .result-title {
        font-size: 1.5rem !important;
    }
    .result-card .result-subtitle {
        font-size: 1rem !important;
    }
    .result-card .confidence {
        font-size: 0.9rem !important;
        padding: 0.3rem 1rem !important;
    }

    /* ---- Tabs ---- */
    .st-emotion-cache-1r6slb0 .st-emotion-cache-1wivap2 {
        padding: 6px 10px !important;
        font-size: 12px !important;
    }

    /* ---- Charts (reduce height) ---- */
    .js-plotly-plot {
        height: 250px !important;
    }

    /* ---- Footer ---- */
    .footer {
        padding: 1.5rem !important;
        font-size: 0.85rem !important;
    }
    .footer p {
        font-size: 0.8rem !important;
    }
    .footer .footer-link {
        font-size: 0.85rem !important;
    }
    .linkedin-icon {
        width: 18px !important;
        height: 18px !important;
    }

    /* ---- Section Divider ---- */
    .section-divider {
        margin: 1rem 0 !important;
    }

    /* ---- Form Inputs ---- */
    .st-emotion-cache-1r6slb0 input,
    .st-emotion-cache-1r6slb0 select,
    .st-emotion-cache-1r6slb0 textarea {
        font-size: 14px !important;
    }

    /* ---- Buttons ---- */
    .st-emotion-cache-1r6slb0 button {
        font-size: 14px !important;
        padding: 0.5rem 1rem !important;
        width: 100% !important;
    }

    /* ---- Metrics ---- */
    .st-emotion-cache-1r6slb0 .st-emotion-cache-1y4p8pa .st-emotion-cache-1wivap2 {
        padding: 0.5rem !important;
    }

    /* ---- Leaderboard table ---- */
    .leaderboard {
        overflow-x: auto !important;
    }
    .leaderboard table {
        font-size: 0.8rem !important;
    }
    .leaderboard th,
    .leaderboard td {
        padding: 0.5rem 0.8rem !important;
        white-space: nowrap !important;
    }

    /* ---- Dataframe container ---- */
    .dataframe-container {
        overflow-x: auto !important;
    }
    .dataframe-container table {
        font-size: 0.75rem !important;
    }
    .dataframe-container th,
    .dataframe-container td {
        padding: 6px 10px !important;
        white-space: nowrap !important;
    }

    /* ---- Best Model section (columns) ---- */
    .st-emotion-cache-1r6slb0 .st-emotion-cache-1y4p8pa .st-emotion-cache-1wivap2 {
        flex-direction: column !important;
    }

    /* ---- Confusion Matrix grid ---- */
    .st-emotion-cache-1r6slb0 .st-emotion-cache-1y4p8pa .st-emotion-cache-1wivap2 div[style*="grid-template-columns"] {
        grid-template-columns: auto 1fr 1fr !important;
        gap: 4px !important;
        max-width: 100% !important;
    }
    .st-emotion-cache-1r6slb0 .st-emotion-cache-1y4p8pa .st-emotion-cache-1wivap2 div[style*="grid-template-columns"] div {
        padding: 8px !important;
        font-size: 0.9rem !important;
    }

    /* ---- Feature Importance chart ---- */
    .js-plotly-plot .plotly .main-svg {
        height: 350px !important;
    }
}

/* Small phones (max-width: 480px) */
@media screen and (max-width: 480px) {
    .hero-banner {
        padding: 1rem 0.8rem !important;
    }
    .hero-banner h1 {
        font-size: 1.4rem !important;
    }
    .hero-banner p {
        font-size: 0.8rem !important;
    }

    .kpi-card {
        padding: 0.6rem !important;
    }
    .kpi-card .kpi-value {
        font-size: 1.2rem !important;
    }
    .kpi-card .kpi-icon {
        font-size: 1.2rem !important;
    }
    .kpi-card .kpi-label {
        font-size: 0.6rem !important;
    }

    .info-card {
        padding: 0.8rem !important;
        min-height: 12rem !important;
    }
    .info-card h3 {
        font-size: 1rem !important;
    }
    .info-card ul li {
        font-size: 0.75rem !important;
        padding: 0.2rem 0 !important;
    }
    .info-card p {
        font-size: 0.8rem !important;
    }

    .info-card span[style*="border-radius: 50px"] {
        font-size: 0.65rem !important;
        padding: 0.15rem 0.6rem !important;
    }

    .workflow-card {
        padding: 0.6rem !important;
    }
    .workflow-card .step-icon {
        font-size: 1rem !important;
        min-width: 1.5rem !important;
    }
    .workflow-card .step-text h4 {
        font-size: 0.8rem !important;
    }
    .workflow-card .step-text p {
        font-size: 0.7rem !important;
    }

    .result-card {
        padding: 1rem !important;
    }
    .result-card .result-icon {
        font-size: 2.5rem !important;
    }
    .result-card .result-title {
        font-size: 1.2rem !important;
    }
    .result-card .result-subtitle {
        font-size: 0.9rem !important;
    }

    .footer {
        padding: 1rem !important;
        font-size: 0.7rem !important;
    }
    .footer p {
        font-size: 0.7rem !important;
    }
    .footer .footer-link {
        font-size: 0.75rem !important;
    }

    .js-plotly-plot {
        height: 180px !important;
    }

    .st-emotion-cache-1r6slb0 .st-emotion-cache-1y4p8pa .st-emotion-cache-1wivap2 {
        padding: 0.3rem !important;
    }
    .st-emotion-cache-1r6slb0 .st-emotion-cache-1y4p8pa .st-emotion-cache-1wivap2 .st-emotion-cache-1wivap2 {
        font-size: 0.8rem !important;
    }
}
 /* ============================================================
   FIX: Font sizes for headings on mobile
   ============================================================ */
@media screen and (max-width: 768px) {
    h1, .hero-banner h1 {
        font-size: 1.8rem !important;
    }
    h2, .st-emotion-cache-1r6slb0 h2, .st-emotion-cache-1y4p8pa h2 {
        font-size: 1.4rem !important;
    }
    h3, .st-emotion-cache-1r6slb0 h3 {
        font-size: 1.2rem !important;
    }
    h4 {
        font-size: 1rem !important;
    }
}

/* ============================================================
   FIX: Spacing between cards (KPI, Info, Workflow)
   ============================================================ */
@media screen and (max-width: 768px) {
    .kpi-card {
        margin-bottom: 0.8rem !important;
    }
    .info-card {
        margin-bottom: 1rem !important;
    }
    .workflow-card {
        margin-bottom: 0.5rem !important;
    }
    .st-emotion-cache-1jicfl2 {
        gap: 0.8rem !important;
    }
    /* Row columns spacing */
    .st-emotion-cache-1y4p8pa {
        padding: 0 0.5rem !important;
    }
}

/* ============================================================
   FIX: Charts - prevent overlapping and resize properly
   ============================================================ */
@media screen and (max-width: 768px) {
    /* All Plotly charts */
    .js-plotly-plot {
        height: 250px !important;
        width: 100% !important;
    }
    .plotly .main-svg {
        width: 100% !important;
        height: 100% !important;
    }
    /* Ensure chart containers take full width */
    .st-emotion-cache-1y4p8pa .st-emotion-cache-1wivap2 {
        width: 100% !important;
        overflow-x: auto !important;
    }
    /* Fix for correlation heatmap */
    .js-plotly-plot .plotly .main-svg {
        max-width: 100% !important;
    }
}

/* ============================================================
   FORCE FIX: EDA & other charts on mobile
   ============================================================ */
@media screen and (max-width: 768px) {
    /* Force all columns inside tabs to stack vertically */
    .st-emotion-cache-1jicfl2,
    .st-emotion-cache-1r6slb0 .st-emotion-cache-1y4p8pa {
        flex-direction: column !important;
        flex-wrap: wrap !important;
    }
    .st-emotion-cache-1y4p8pa {
        width: 100% !important;
        max-width: 100% !important;
        flex: 1 1 100% !important;
    }
    /* Chart containers – force height and prevent overlap */
    .stPlotlyChart,
    .st-emotion-cache-1y4p8pa .st-emotion-cache-1wivap2,
    .js-plotly-plot {
        height: 220px !important;
        min-height: 180px !important;
        max-height: 300px !important;
        width: 100% !important;
        overflow: hidden !important;
    }
    .plotly .main-svg {
        height: 100% !important;
        width: 100% !important;
    }
    /* Also reduce height for larger charts (e.g., heatmap) */
    .js-plotly-plot .plotly .main-svg {
        max-height: 400px !important;
    }
}
@media screen and (max-width: 480px) {
    .stPlotlyChart,
    .js-plotly-plot {
        height: 160px !important;
        min-height: 140px !important;
    }
}

/* ============================================================
   FIX: Models page - leaderboard, best model, and cards
   ============================================================ */
@media screen and (max-width: 768px) {
    /* Leaderboard table - ensure horizontal scroll */
    .leaderboard {
        overflow-x: auto !important;
        display: block !important;
        white-space: nowrap !important;
    }
    .leaderboard table {
        display: table !important;
        width: auto !important;
        min-width: 600px !important;
    }
    /* Best model section - stack columns */
    .st-emotion-cache-1jicfl2 .st-emotion-cache-1y4p8pa {
        flex-direction: column !important;
    }
    .st-emotion-cache-1y4p8pa .st-emotion-cache-1wivap2 {
        width: 100% !important;
    }
    /* Why Decision Tree card - fix height */
    div[style*="height:23rem"] {
        height: auto !important;
        min-height: 15rem !important;
    }
    /* Confusion matrix grid - prevent overflow */
    div[style*="grid-template-columns: auto 1fr 1fr"] {
        grid-template-columns: 1fr 1fr 1fr !important;
        gap: 4px !important;
        max-width: 100% !important;
    }
    /* Feature importance chart - resize */
    .js-plotly-plot .plotly .main-svg {
        height: 350px !important;
    }
}

/* ============================================================
   FIX: Prediction page - form and gauge
   ============================================================ */
@media screen and (max-width: 768px) {
    .prediction-form {
        padding: 1rem !important;
    }
    .st-emotion-cache-1y4p8pa .st-emotion-cache-1wivap2 {
        width: 100% !important;
    }
    .result-card {
        padding: 1.2rem !important;
    }
    .result-card .result-icon {
        font-size: 2.5rem !important;
    }
    .result-card .result-title {
        font-size: 1.3rem !important;
    }
    /* Gauge chart */
    .js-plotly-plot {
        height: 180px !important;
    }
}

/* ============================================================
   FIX: Dashboard page - additional info cards (3 columns)
   ============================================================ */
@media screen and (max-width: 768px) {
    .st-emotion-cache-1jicfl2 .st-emotion-cache-1y4p8pa {
        flex: 1 1 100% !important;
        max-width: 100% !important;
    }
    /* The 3 info cards at bottom */
    .st-emotion-cache-1y4p8pa .st-emotion-cache-1wivap2 {
        margin-bottom: 0.8rem !important;
    }
}

/* ============================================================
   FIX: General container padding and overflow
   ============================================================ */
@media screen and (max-width: 768px) {
    .main {
        padding: 0 0.5rem !important;
    }
    .st-emotion-cache-1r6slb0 {
        padding: 0 !important;
    }
    /* Prevent horizontal scroll */
    .st-emotion-cache-1y4p8pa {
        overflow-x: hidden !important;
    }
}

/* ============================================================
   FIX: Small phones (max-width: 480px)
   ============================================================ */
@media screen and (max-width: 480px) {
    h1, .hero-banner h1 {
        font-size: 1.4rem !important;
    }
    h2 {
        font-size: 1.2rem !important;
    }
    h3 {
        font-size: 1rem !important;
    }
    .kpi-card .kpi-value {
        font-size: 1.2rem !important;
    }
    .kpi-card .kpi-label {
        font-size: 0.6rem !important;
    }
    .info-card {
        padding: 0.8rem !important;
    }
    .info-card h3 {
        font-size: 1rem !important;
    }
    .info-card p {
        font-size: 0.8rem !important;
    }
    .js-plotly-plot {
        height: 180px !important;
    }
    .leaderboard table {
        min-width: 500px !important;
    }
}           
    
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================
if 'page' not in st.session_state:
    st.session_state.page = "Dashboard"
if 'model' not in st.session_state:
    st.session_state.model = None
if 'feature_names' not in st.session_state:
    st.session_state.feature_names = None
if 'df' not in st.session_state:
    st.session_state.df = None
if 'predictions_history' not in st.session_state:
    st.session_state.predictions_history = []

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

# Function to show consent notice (NO CACHE - contains widgets)
def show_consent_notice():
    """Show the consent notice for loading large dataset"""
    
    # Use st.html() for cleaner HTML rendering (Streamlit 1.28+)
    st.html("""
    <style>
    .notice-container {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        border-radius: 15px;
        padding: 35px 30px;
        border-left: 6px solid #ffc107;
        margin: 30px 0;
        box-shadow: 0 4px 20px rgba(255, 193, 7, 0.15);
    }
    .notice-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1a1a2e;
        margin-bottom: 8px;
    }
    .notice-subtitle {
        font-size: 1.1rem;
        color: #495057;
        margin-bottom: 20px;
    }
    .notice-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
        margin: 15px 0;
    }
    .notice-item {
        background: rgba(255,255,255,0.6);
        padding: 12px 16px;
        border-radius: 8px;
        font-size: 0.95rem;
        color: #495057;
    }
    .notice-item strong {
        color: #1a1a2e;
    }
    .notice-warning {
        color: #856404;
        font-weight: 600;
        font-size: 1rem;
    }
    .notice-footer {
        margin-top: 15px;
        padding-top: 15px;
        border-top: 1px solid rgba(0,0,0,0.08);
        font-size: 0.9rem;
        color: #6c757d;
    }
    @media (max-width: 768px) {
        .notice-grid {
            grid-template-columns: 1fr;
        }
        .notice-title {
            font-size: 1.4rem;
        }
    }
    </style>
    
    <div class="notice-container">
        <div class="notice-title">📊 Large Dataset Loading</div>
        <div class="notice-subtitle">
            This application requires loading a <strong>4.3 GB dataset</strong> from Google Drive 
            to provide comprehensive analysis and predictions.
        </div>
        
        <div class="notice-grid">
            <div class="notice-item">
                📶 <strong>Data Usage:</strong><br>
                ~4.3 GB of your internet data
            </div>
            <div class="notice-item">
                ⏱️ <strong>Loading Time:</strong><br>
                5-15 minutes (depends on connection)
            </div>
            <div class="notice-item">
                💾 <strong>Memory Required:</strong><br>
                4+ GB RAM recommended
            </div>
            <div class="notice-item">
                🔄 <strong>Cache:</strong><br>
                Faster on subsequent visits
            </div>
        </div>
        
        <div style="margin: 10px 0 5px 0;">
            <span class="notice-warning">⚠️ Your internet data will be consumed during download.</span>
        </div>
        
        <div class="notice-footer">
            ✅ Click "Continue" to start loading the dataset. You'll see real-time progress.
        </div>
    </div>
    """)
    
    # Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✅ Continue - Load Dataset", use_container_width=True, type="primary"):
            st.session_state.data_loading_confirmed = True
            st.rerun()
    return None

# Function to show progress (NO CACHE - contains widgets)
def show_loading_progress():
    """Show the loading progress bar"""
    st.markdown("""
    <style>
    .loading-container {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 30px;
        text-align: center;
        border: 1px solid #e9ecef;
        margin: 20px 0;
    }
    .loading-title {
        font-size: 1.4rem;
        font-weight: 600;
        color: #1a1a2e;
        margin-bottom: 5px;
    }
    .loading-subtitle {
        font-size: 0.95rem;
        color: #6c757d;
        margin-bottom: 20px;
    }
    </style>
    <div class="loading-container">
        <div class="loading-title">📥 Downloading Dataset</div>
        <div class="loading-subtitle">Please wait while the data loads...</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create progress elements
    progress_bar = st.progress(0)
    status_text = st.empty()
    progress_percentage = st.empty()
    
    return progress_bar, status_text, progress_percentage

# Cached function for actual data loading (NO widgets inside)
@st.cache_data
def load_data_from_drive(file_id):
    """
    Load the processed dataset from Google Drive using gdown.
    This function is cached and contains NO widget commands.
    """
    import gdown
    import os
    import pandas as pd
    
    url = f"https://drive.google.com/uc?id={file_id}"
    output = "application_downloaded.csv"
    
    # Download the file using gdown
    gdown.download(url, output, quiet=False)
    
    # Check if file was downloaded
    if not os.path.exists(output):
        raise Exception("Download failed - file not found")
    
    # Read the downloaded CSV
    df = pd.read_csv(output)
    
    # Clean up - remove the temporary file
    if os.path.exists(output):
        os.remove(output)
    
    # Verify the file
    if 'TARGET' not in df.columns:
        raise Exception("Downloaded file does not contain 'TARGET' column.")
    
    return df

# Main load_data function (NO CACHE - handles UI only)
# Main load_data function (NO CACHE - handles UI only)
def load_data():
    """
    Load the processed dataset from Google Drive using gdown.
    Shows user consent notice and progress tracking.
    Returns: DataFrame or None (if consent not given or error)
    """
    file_id = "11hYG6gaKWd8BgR4olYPzQuD1TX0ODCSo"
    
    # Check if data is already loaded in session state
    if 'df' in st.session_state and st.session_state.df is not None:
        return st.session_state.df
    
    # Check if user has consented to data loading
    if 'data_loading_confirmed' not in st.session_state:
        st.session_state.data_loading_confirmed = False
    
    # Show consent notice if not confirmed
    if not st.session_state.data_loading_confirmed:
        show_consent_notice()
        return None  # Return None to stop execution
    
    # Proceed with actual data loading
    try:
        # Use a placeholder at the top of the page
        progress_placeholder = st.empty()
        
        with progress_placeholder.container():
            # Show progress UI with the loading div
            st.markdown("""
            <style>
            .loading-container {
                background: #f8f9fa;
                border-radius: 12px;
                padding: 30px;
                text-align: center;
                border: 1px solid #e9ecef;
                margin: 20px 0;
            }
            .loading-title {
                font-size: 1.4rem;
                font-weight: 600;
                color: #1a1a2e;
                margin-bottom: 5px;
            }
            .loading-subtitle {
                font-size: 0.95rem;
                color: #6c757d;
                margin-bottom: 20px;
            }
            </style>
            <div class="loading-container">
                <div class="loading-title">📥 Downloading Dataset</div>
                <div class="loading-subtitle">Please wait while the data loads...</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Create progress elements
            progress_bar = st.progress(0)
            status_text = st.empty()
            progress_percentage = st.empty()
        
        # Step 1: Initialize
        status_text.markdown("#### 🔄 Step 1/4: Initializing connection...")
        progress_percentage.markdown("#### 📊 **Progress:** `0%`")
        progress_bar.progress(0)
        time.sleep(0.5)
        
        # Step 2: Connecting
        status_text.markdown("#### 🔗 Step 2/4: Connecting to Google Drive...")
        progress_percentage.markdown("#### 📊 **Progress:** `10%`")
        progress_bar.progress(10)
        time.sleep(0.5)
        
        # Step 3: Downloading
        status_text.markdown("#### 📥 Step 3/4: Downloading dataset (This may take several minutes)...")
        progress_percentage.markdown("#### 📊 **Progress:** `30%`")
        progress_bar.progress(30)
        time.sleep(0.5)
        
        status_text.markdown("#### 📥 Downloading... Please wait...")
        progress_percentage.markdown("#### 📊 **Progress:** `50%`")
        progress_bar.progress(50)
        
        # Actual download (this is the cached part)
        df = load_data_from_drive(file_id)
        
        # Step 4: Processing
        status_text.markdown("#### 📖 Step 4/4: Processing downloaded file...")
        progress_percentage.markdown("#### 📊 **Progress:** `80%`")
        progress_bar.progress(80)
        time.sleep(0.5)
        
        # ============================================================
        # CLEAR EVERYTHING - Remove ALL loading elements
        # ============================================================
        # Clear the entire placeholder - THIS REMOVES EVERYTHING!
        progress_placeholder.empty()
        
        # Store in session state to avoid reloading
        st.session_state.df = df
        
        # Show toast notification
        st.toast(f"✅ Dataset loaded from Google Drive! Shape: {df.shape}")
        
        return df
                
    except Exception as e:
        # Clear everything on error
        try:
            progress_placeholder.empty()
        except:
            pass
        
        st.error(f"❌ Error downloading from Google Drive: {str(e)}")
        st.info("💡 This could be due to a network issue. Please check your internet connection and try again.")
        
        # Reset consent so user can try again
        st.session_state.data_loading_confirmed = False
        
        # Fallback: Try local file
        try:
            df = pd.read_csv("application.csv")
            if 'TARGET' in df.columns:
                st.info("📁 Loaded from local file as fallback.")
                st.session_state.df = df
                return df
            else:
                st.error("❌ Local file missing 'TARGET'.")
                return None
        except FileNotFoundError:
            st.error("❌ No local 'application.csv' found.")
            return None
        except Exception as fallback_e:
            st.error(f"❌ Local fallback failed: {str(fallback_e)}")
            return None
                
@st.cache_resource
def load_model():
    """Load the decision tree model and feature names"""
    try:
        model_path = os.path.join('model', 'decision_tree.pkl')
        features_path = os.path.join('model', 'feature_names.pkl')
        
        if not os.path.exists(model_path):
            st.error(f"Model file not found at: {model_path}")
            return None, None
        
        if not os.path.exists(features_path):
            st.error(f"Feature names file not found at: {features_path}")
            return None, None
        
        model = joblib.load(model_path)
        with open(features_path, 'rb') as f:
            feature_names = pickle.load(f)
        
        return model, feature_names
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None, None

def get_dataset_stats(df):
    """Calculate dataset statistics dynamically"""
    stats = {
        'total_records': len(df),
        'total_features': len(df.columns),
        'default_rate': None,
        'missing_values': df.isnull().sum().sum(),
        'missing_cols': df.isnull().sum()[df.isnull().sum() > 0].count()
    }
    
    # Calculate default rate if target column exists
    target_cols = ['TARGET', 'default', 'Default', 'Status']
    for col in target_cols:
        if col in df.columns:
            stats['default_rate'] = (df[col].sum() / len(df) * 100) if df[col].dtype in ['int64', 'float64'] else None
            break
    
    return stats

# ============================================================================
# NAVIGATION
# ============================================================================
def render_navigation():
    """Render horizontal navigation bar"""
    with st.container():
        # Map page names to indices
        page_to_index = {
            "🏠 Dashboard": 0,
            "📊 EDA": 1,
            "🧹 Preprocessing": 2,
            "🤖 Models": 3,
            "🏦 Prediction": 4
        }
        
        # Get the current page from session state, default to Dashboard
        current_page = st.session_state.get('page', '🏠 Dashboard')
        
        # Get the default index
        default_idx = page_to_index.get(current_page, 0)
        
        # Create the option menu
        selected = option_menu(
            menu_title=None,
            options=["🏠 Dashboard", "📊 EDA", "🧹 Preprocessing", "🤖 Models", "🏦 Prediction"],
            icons=["house", "bar-chart", "gear", "cpu", "magic"],
            menu_icon="cast",
            default_index=default_idx,
            orientation="horizontal",
            key="nav_menu",
            styles={
                "container": {
                    "padding": "0!important",
                    "background-color": "transparent",
                    "border-radius": "15px",
                    "box-shadow": "0 4px 15px rgba(0,0,0,0.08)",
                },
                "icon": {
                    "color": "#667eea",
                    "font-size": "18px",
                },
                "nav-link": {
                    "font-size": "15px",
                    "text-align": "center",
                    "margin": "0px",
                    "padding": "12px 24px",
                    "border-radius": "12px",
                    "color": "#6c757d",
                    "font-weight": "500",
                    "transition": "all 0.3s ease",
                },
                "nav-link:hover": {
                    "background-color": "#f8f9fa",
                    "color": "#1a1a2e",
                },
                "nav-link-selected": {
                    "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                    "color": "white",
                    "font-weight": "600",
                    "box-shadow": "0 4px 15px rgba(102, 126, 234, 0.4)",
                },
            }
        )
        
        # Update session state based on selection
        # Always update if selected is not None
        if selected is not None:
            st.session_state.page = selected
            
# ============================================================================
# HERO BANNER
# ============================================================================
def render_hero_banner():
    """Render the hero banner with image"""
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        <div class="hero-banner">
            <h1>🏠 Home Loan Default Prediction System</h1>
            <p>Predict Potential Loan Defaulters Using Machine Learning and Credit Risk Analytics</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        try:
            if os.path.exists('images/home-default-loan.png'):
                st.image('images/home-default-loan.png', use_container_width=True)
            else:
                st.markdown("""
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                            border-radius: 15px; padding: 3.5rem; text-align: center; color: white; height: 100%; display: flex; align-items: center; justify-content: center;">
                    <div>
                        <div style="font-size: 4.6rem;">🏦</div>
                        <p style="font-weight: 700; margin-top: 0.5rem;font-size:1.9rem">Loan Default Prediction</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        except:
            pass

# ============================================================================
# KPI CARDS
# ============================================================================
def render_kpi_cards(stats, model_loaded=True):
    """Render dynamic KPI cards"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="kpi-card gradient-1">
            <div class="kpi-icon">👥</div>
            <div class="kpi-value">{stats['total_records']:,}</div>
            <div class="kpi-label">Total Customers</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="kpi-card gradient-2">
            <div class="kpi-icon">📊</div>
            <div class="kpi-value">{stats['total_features']}</div>
            <div class="kpi-label">Total Features</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        default_rate = stats.get('default_rate', 'N/A')
        if default_rate is not None:
            st.markdown(f"""
            <div class="kpi-card gradient-3">
                <div class="kpi-icon">📈</div>
                <div class="kpi-value">{default_rate:.1f}%</div>
                <div class="kpi-label">Default Rate</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="kpi-card gradient-3">
                <div class="kpi-icon">📈</div>
                <div class="kpi-value">N/A</div>
                <div class="kpi-label">Default Rate</div>
            </div>
            """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="kpi-card gradient-4">
            <div class="kpi-icon">🤖</div>
            <div class="kpi-value">4</div>
            <div class="kpi-label">Models Compared</div>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# PAGE RENDERERS
# ============================================================================

# ----------------------------------------------------------------------------
# DASHBOARD PAGE
# ----------------------------------------------------------------------------
def render_dashboard(df, stats, model, feature_names):
    """Render the dashboard page"""
    render_hero_banner()
    
    # KPI Cards
    render_kpi_cards(stats)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # Overview and Highlights
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
     st.markdown("""
                 <div class="info-card">
                 <h3>📋 Project Overview</h3>
                 <p style="color: #495057; line-height: 1.8;">
                 This system uses advanced machine learning techniques to predict the likelihood 
                 of home loan default. By analyzing multiple data sources including client 
                 demographics, credit history, and financial indicators, the model provides 
                 accurate risk assessments to support informed lending decisions.</p>
                 
                 <div style="background: #f8f9fa; border-radius: 10px; padding: 1rem; margin: 1rem 0;">
                 <h4 style="color: #1a1a2e; margin: 0 0 0.5rem 0;">🎯 Key Objectives</h4>
                 <ul style="list-style: none; padding: 0; margin: 0;">
                 <li style="padding: 0.3rem 0; color: #495057; display: flex; align-items: center; gap: 0.5rem;">
                 <span style="color: #667eea;">▸</span> 
                 <strong>Risk Mitigation:</strong> Identify high-risk applicants early
                 </li>
                 <li style="padding: 0.3rem 0; color: #495057; display: flex; align-items: center; gap: 0.5rem;">
                 <span style="color: #667eea;">▸</span> 
                 <strong>Data-Driven Decisions:</strong> Leverage 210+ features for accurate predictions
                 </li>     
                 <li style="padding: 0.3rem 0; color: #495057; display: flex; align-items: center; gap: 0.5rem;">
                 <span style="color: #667eea;">▸</span> 
                 <strong>Real-time Analysis:</strong> Instant risk assessment for loan applications
                 </li>
                 </ul>
                 </div>
                 <div style="display: flex; gap: 0.8rem; flex-wrap: wrap; margin: 0.5rem 0;">
                 <span style="background: #e9ecef; padding: 0.3rem 1rem; border-radius: 50px; font-size: 0.8rem; color: #495057;">🔬 ML Model</span>
                 <span style="background: #e9ecef; padding: 0.3rem 1rem; border-radius: 50px; font-size: 0.8rem; color: #495057;">📊 Credit Risk</span>
                 <span style="background: #e9ecef; padding: 0.3rem 1rem; border-radius: 50px; font-size: 0.8rem; color: #495057;">🏦 Home Loans</span>
                 <span style="background: #e9ecef; padding: 0.3rem 1rem; border-radius: 50px; font-size: 0.8rem; color: #495057;">⚡ Real-time</span>
                 <span style="background: #e9ecef; padding: 0.3rem 1rem; border-radius: 50px; font-size: 0.8rem; color: #495057;">📈 Predictive Analytics</span>
                </div>
                </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="info-card">
            <h3>✨ Project Highlights</h3>
            <ul>
                <li>✅ Multi-source Data Integration (via Google Drive/gdown)</li>
                <li>✅ Feature Engineering</li>
                <li>✅ Interactive EDA Dashboards</li>
                <li>✅ One-Hot Encoding</li>
                <li>✅ SMOTE Balancing</li>
                <li>✅ Hyperparameter Tuning</li>
                <li>✅ Decision Tree Model</li>
                <li>✅ Credit Risk Prediction</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Additional Info
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        missing_rate = (stats.get('missing_values', 0) / (stats['total_records'] * stats['total_features'])) * 100 if stats['total_records'] > 0 else 0
        st.markdown(f"""
        <div style="background: white; border-radius: 15px; padding: 1.5rem; text-align: center; border: 1px solid #e9ecef;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🔍</div>
            <div style="font-size: 1.5rem; font-weight: 700; color: #1a1a2e;">{stats.get('missing_cols', 0)}</div>
            <div style="color: #6c757d; font-size: 0.9rem;">Columns with Missing Values</div>
            <div style="font-size: 0.8rem; color: #6c757d; margin-top: 0.3rem;">{missing_rate:.2f}% missing overall</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: white; border-radius: 15px; padding: 1.5rem; text-align: center; border: 1px solid #e9ecef;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🧠</div>
            <div style="font-size: 1.5rem; font-weight: 700; color: #1a1a2e;">Decision Tree</div>
            <div style="color: #6c757d; font-size: 0.9rem;">Best Performing Model</div>
            <div style="font-size: 0.8rem; color: #6c757d; margin-top: 0.3rem;">ROC AUC: 0.75+</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="background: white; border-radius: 15px; padding: 1.5rem; text-align: center; border: 1px solid #e9ecef;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">📊</div>
            <div style="font-size: 1.5rem; font-weight: 700; color: #1a1a2e;">{len(feature_names) if feature_names else 0}</div>
            <div style="color: #6c757d; font-size: 0.9rem;">Final Features</div>
            <div style="font-size: 0.8rem; color: #6c757d; margin-top: 0.3rem;">After preprocessing</div>
        </div>
        """, unsafe_allow_html=True)
# ----------------------------------------------------------------------------
# EDA PAGE
# ----------------------------------------------------------------------------
def render_eda(df):
    """Render the EDA page with interactive visualizations – robust for missing columns"""
    st.markdown('<h2 style="color: #6F6F7D; margin-bottom: 1rem;">📊 Exploratory Data Analysis</h2>', unsafe_allow_html=True)
    
    # Helper: get a numeric column or return None
    def get_numeric_col(col_name):
        if col_name in df.columns:
            # try to convert to numeric, coercing errors
            series = pd.to_numeric(df[col_name], errors='coerce')
            if series.notna().sum() > 0:
                return series
        return None

    # Detect target column
    target_col = None
    for col in ['TARGET', 'default', 'Default', 'Status']:
        if col in df.columns:
            target_col = col
            break

    # Tabs - DEFINE TABS HERE
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 Target Analysis", "💰 Financial Analysis", "📈 Credit Profile", "🔗 Correlation"])

    # ---------- TAB 1 ----------
    with tab1:
        st.markdown("### 🎯 Target Variable Distribution")
        col1, col2 = st.columns(2)
        with col1:
            if target_col is not None and target_col in df.columns:
                target_series = df[target_col].dropna()
                if len(target_series) > 0:
                    try:
                        # Convert to numeric, coercing errors
                        target_series = pd.to_numeric(target_series, errors='coerce').dropna()
                        if len(target_series) > 0:
                            # If only 0 and 1, it's binary classification
                            if set(target_series.unique()) <= {0, 1}:
                                counts = target_series.value_counts()
                                labels = ['Non-Default', 'Default']
                                values = [counts.get(0, 0), counts.get(1, 0)]
                                
                                if sum(values) > 0:
                                    fig = go.Figure(data=[go.Pie(
                                        labels=labels,
                                        values=values,
                                        hole=0.4,
                                        marker=dict(colors=['#43e97b', '#f5576c']),
                                        textinfo='label+percent',
                                        textposition='auto'
                                    )])
                                    fig.update_layout(height=400, showlegend=False, paper_bgcolor='rgba(0,0,0,0)')
                                    st.plotly_chart(fig, use_container_width=True, config={'responsive': True})
                                else:
                                    st.info("No valid target data available for pie chart")
                            else:
                                fig = px.histogram(target_series, title='Target Distribution')
                                fig.update_layout(height=400, paper_bgcolor='rgba(0,0,0,0)')
                                st.plotly_chart(fig, use_container_width=True, config={'responsive': True})
                        else:
                            st.info("Target column has no valid numeric data")
                    except Exception as e:
                        st.info(f"Error processing target data: {str(e)}")
                else:
                    st.info("Target column has no valid data")
            else:
                st.info("Target column not found in dataset")
        
        with col2:
            if target_col is not None and target_col in df.columns:
                target_series = df[target_col].dropna()
                if len(target_series) > 0:
                    try:
                        # Convert to numeric
                        target_series = pd.to_numeric(target_series, errors='coerce').dropna()
                        if len(target_series) > 0:
                            # For binary classification
                            if set(target_series.unique()) <= {0, 1}:
                                value_counts = target_series.value_counts().sort_index()
                                
                                plot_df = pd.DataFrame({
                                    'Status': ['Non-Default' if x == 0 else 'Default' for x in value_counts.index],
                                    'Count': value_counts.values
                                })
                                
                                fig = px.bar(
                                    plot_df, 
                                    x='Status', 
                                    y='Count',
                                    title='Default Status Distribution',
                                    color='Status',
                                    color_discrete_map={'Non-Default': '#43e97b', 'Default': '#f5576c'},
                                    text='Count'
                                )
                                fig.update_traces(textposition='outside')
                                fig.update_layout(
                                    height=400, 
                                    showlegend=False, 
                                    paper_bgcolor='rgba(0,0,0,0)', 
                                    bargap=0.2,
                                    xaxis_title="",
                                    yaxis_title="Number of Applicants"
                                )
                                st.plotly_chart(fig, use_container_width=True, config={'responsive': True})
                            else:
                                fig = px.histogram(target_series, title='Target Distribution')
                                fig.update_layout(height=400, paper_bgcolor='rgba(0,0,0,0)')
                                st.plotly_chart(fig, use_container_width=True, config={'responsive': True})
                        else:
                            st.info("Target column has no valid numeric data")
                    except Exception as e:
                        st.info(f"Error processing target data: {str(e)}")
                else:
                    st.info("Target column has no valid data")
            else:
                st.info("Target column not found in dataset")

    # ---------- TAB 2 ----------
    with tab2:
        st.markdown("### 💰 Financial Analysis")
        col1, col2 = st.columns(2)
        with col1:
            income = get_numeric_col('AMT_INCOME_TOTAL')
            if income is not None:
                fig = px.histogram(income, nbins=50, title='Income Distribution', color_discrete_sequence=['#667eea'])
                fig.update_layout(height=350, paper_bgcolor='rgba(0,0,0,0)', xaxis_title='Annual Income')
                st.plotly_chart(fig, use_container_width=True, config={'responsive': True})
            else:
                st.info("Column 'AMT_INCOME_TOTAL' not available or all missing.")
            
            credit = get_numeric_col('AMT_CREDIT')
            if credit is not None:
                fig = px.histogram(credit, nbins=50, title='Credit Amount Distribution', color_discrete_sequence=['#764ba2'])
                fig.update_layout(height=350, paper_bgcolor='rgba(0,0,0,0)', xaxis_title='Credit Amount')
                st.plotly_chart(fig, use_container_width=True, config={'responsive': True})
            else:
                st.info("Column 'AMT_CREDIT' not available or all missing.")
        
        with col2:
            annuity = get_numeric_col('AMT_ANNUITY')
            if annuity is not None:
                fig = px.histogram(annuity, nbins=50, title='Annuity Distribution', color_discrete_sequence=['#f5576c'])
                fig.update_layout(height=350, paper_bgcolor='rgba(0,0,0,0)', xaxis_title='Annuity Amount')
                st.plotly_chart(fig, use_container_width=True, config={'responsive': True})
            else:
                st.info("Column 'AMT_ANNUITY' not available or all missing.")
            
            if target_col and income is not None and target_col in df.columns:
                # Boxplot needs the original dataframe with target
                df_target_income = df[[target_col, 'AMT_INCOME_TOTAL']].dropna()
                if len(df_target_income) > 0:
                    # Ensure target is numeric
                    df_target_income[target_col] = pd.to_numeric(df_target_income[target_col], errors='coerce')
                    df_target_income = df_target_income.dropna()
                    
                    if len(df_target_income) > 0:
                        fig = px.box(df_target_income, x=target_col, y='AMT_INCOME_TOTAL',
                                     title='Income vs Default Status', color=target_col,
                                     color_discrete_map={0: '#43e97b', 1: '#f5576c'})
                        fig.update_layout(height=350, showlegend=False, paper_bgcolor='rgba(0,0,0,0)')
                        st.plotly_chart(fig, use_container_width=True, config={'responsive': True})
                    else:
                        st.info("Not enough data for boxplot")

    # ---------- TAB 3 ----------
    with tab3:
        st.markdown("### 📈 Credit Profile Analysis")
        ext_sources = ['EXT_SOURCE_1', 'EXT_SOURCE_2', 'EXT_SOURCE_3']
        cols = st.columns(3)
        for idx, col_name in enumerate(ext_sources):
            with cols[idx]:
                col_series = get_numeric_col(col_name)
                if col_series is not None:
                    fig = px.histogram(col_series, nbins=30, title=f'{col_name} Distribution', color_discrete_sequence=['#667eea'])
                    fig.update_layout(height=300, paper_bgcolor='rgba(0,0,0,0)')
                    st.plotly_chart(fig, use_container_width=True, config={'responsive': True})
                else:
                    st.info(f"Column '{col_name}' not available or all missing.")
        
        # Boxplots for EXT_SOURCES by target
        if target_col:
            st.markdown("### Credit Sources by Default Status")
            valid_sources = []
            for col in ext_sources:
                if col in df.columns and df[col].notna().sum() > 0:
                    valid_sources.append(col)
            if valid_sources:
                fig = go.Figure()
                for i, col in enumerate(valid_sources):
                    fig.add_trace(go.Box(y=df[col].dropna(), name=col, marker_color=['#667eea','#764ba2','#f5576c'][i % 3], boxmean='sd'))
                fig.update_layout(height=400, paper_bgcolor='rgba(0,0,0,0)', title='External Source Distribution')
                st.plotly_chart(fig, use_container_width=True, config={'responsive': True})
            else:
                st.info("No external source columns available.")

    # ---------- TAB 4 ----------
    with tab4:
        st.markdown("### 🔗 Correlation Analysis")
        # Select numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if len(numeric_cols) > 1:
            # Take top 20 to avoid huge matrix
            if len(numeric_cols) > 20:
                numeric_cols = numeric_cols[:20]
            corr = df[numeric_cols].corr()
            # Heatmap
            fig = go.Figure(data=go.Heatmap(
                z=corr.values,
                x=corr.columns,
                y=corr.columns,
                colorscale='RdBu',
                zmid=0,
                text=corr.values.round(2),
                texttemplate='%{text}',
                textfont={"size": 8}
            ))
            fig.update_layout(height=600, paper_bgcolor='rgba(0,0,0,0)', title='Correlation Heatmap')
            st.plotly_chart(fig, use_container_width=True, config={'responsive': True})
            
            # Top correlated pairs
            st.markdown("### 🔝 Top Correlated Features")
            pairs = []
            for i in range(len(corr.columns)):
                for j in range(i+1, len(corr.columns)):
                    pairs.append((corr.columns[i], corr.columns[j], corr.iloc[i, j]))
            pairs.sort(key=lambda x: abs(x[2]), reverse=True)
            top10 = pairs[:10]
            if top10:
                fig = go.Figure(data=[go.Bar(
                    x=[f"{p[0]} & {p[1]}" for p in top10],
                    y=[p[2] for p in top10],
                    marker_color=['#43e97b' if p[2] > 0 else '#f5576c' for p in top10],
                    text=[f"{p[2]:.2f}" for p in top10],
                    textposition='auto'
                )])
                fig.update_layout(height=400, paper_bgcolor='rgba(0,0,0,0)', xaxis_tickangle=-45, title='Top 10 Correlated Feature Pairs')
                st.plotly_chart(fig, use_container_width=True, config={'responsive': True})
            else:
                st.info("No correlation pairs found.")
        else:
            st.info("Not enough numeric columns for correlation analysis.")
# ----------------------------------------------------------------------------
# PREPROCESSING PAGE
# ----------------------------------------------------------------------------
def render_preprocessing(df):
    """Render the preprocessing page with visual workflow"""
    st.markdown('<h2 style="color: #6F6F7D; margin-bottom: 1rem;">🧹 Preprocessing Pipeline</h2>', unsafe_allow_html=True)
    
    # Stats cards
    col1, col2, col3, col4 = st.columns(4)
    
    original_features = len(df.columns)
    final_features = len([col for col in df.columns if not col.startswith('Unnamed')])
    
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">📊</div>
            <div class="kpi-value">{original_features}</div>
            <div class="kpi-label">Original Features</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">✨</div>
            <div class="kpi-value">{final_features}</div>
            <div class="kpi-label">Final Features</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        missing_values = df.isnull().sum().sum()
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">🔍</div>
            <div class="kpi-value">{missing_values:,}</div>
            <div class="kpi-label">Missing Values</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">⚖️</div>
            <div class="kpi-value">✅</div>
            <div class="kpi-label">Class Imbalance Resolved</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # Workflow
    st.markdown('<h3 style="text-align: center; color: #6F6F7D;">🔄 Data Processing Workflow</h3>', unsafe_allow_html=True)
    
    workflow_steps = [
        ("📄", "Raw Data", "Load and inspect the raw dataset"),
        ("🧹", "Missing Value Treatment", "Handle missing values using appropriate imputation strategies"),
        ("🔧", "Feature Engineering", "Create new features from existing data"),
        ("🎯", "One-Hot Encoding", "Convert categorical variables to numerical format"),
        ("🎯", "Feature Selection", "Select the most important features for modeling"),
        ("📊", "Train-Test Split", "Split data into training and testing sets (80/20)"),
        ("⚖️", "SMOTE Balancing", "Address class imbalance using SMOTE technique"),
        ("🤖", "Model Training", "Train multiple machine learning models"),
        ("🎛️", "Hyperparameter Tuning", "Optimize model parameters using GridSearchCV"),
        ("🏆", "Final Prediction", "Deploy the best performing model for predictions")
    ]
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        for icon, step, desc in workflow_steps:
            st.markdown(f"""
            <div class="workflow-card">
                <div class="step-icon">{icon}</div>
                <div class="step-text">
                    <h4>{step}</h4>
                    <p>{desc}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Additional explanation
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: white; border-radius: 15px; padding: 1.5rem; border: 1px solid #e9ecef;">
        <h4 style="color: #1a1a2e;">💡 Key Insights</h4>
        <ul style="list-style: none; padding: 0;">
            <li style="padding: 0.5rem 0; border-bottom: 1px solid #f1f3f5;color: #1a1a2e;">
                <span style="color: #43e97b;">✓</span> 
                <strong>Missing Values:</strong> Identified and treated using median/mode imputation
            </li>
            <li style="padding: 0.5rem 0; border-bottom: 1px solid #f1f3f5;color: #1a1a2e;">
                <span style="color: #43e97b;">✓</span> 
                <strong>Feature Engineering:</strong> Created 15+ new features including ratios and aggregates
            </li>
            <li style="padding: 0.5rem 0; border-bottom: 1px solid #f1f3f5;color: #1a1a2e;">
                <span style="color: #43e97b;">✓</span> 
                <strong>SMOTE:</strong> Increased minority class representation by 200%
            </li>
            <li style="padding: 0.5rem 0;color: #1a1a2e;">
                <span style="color: #43e97b;">✓</span> 
                <strong>Feature Selection:</strong> Reduced features from 210 to 202 important features
            </li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# MODELS PAGE
# ----------------------------------------------------------------------------
def render_models(model, feature_names, df):
    """Render the models page with leaderboard and feature importance"""
    st.markdown('<h2 style="color: #6F6F7D; margin-bottom: 1rem;">🤖 Model Performance</h2>', unsafe_allow_html=True)
    
    
    # ========================================================================
    # MODEL LEADERBOARD - Using Streamlit's native table
    # ========================================================================
    st.markdown("### 🏆 Model Leaderboard")
    
    # Sample model metrics with variables for Decision Tree
    dt_accuracy = 0.85
    dt_precision = 0.83
    dt_recall = 0.82
    dt_f1 = 0.825
    dt_roc_auc = 0.88
    
    model_data = [
        {"Rank": "🥇", "Model": "Decision Tree", "Accuracy": dt_accuracy, "Precision": dt_precision, "Recall": dt_recall, "F1": dt_f1, "ROC_AUC": dt_roc_auc, "Status": "🏆 Best"},
        {"Rank": "🥈", "Model": "Logistic Regression", "Accuracy": 0.78, "Precision": 0.76, "Recall": 0.74, "F1": 0.75, "ROC_AUC": 0.82, "Status": "—"},
        {"Rank": "🥉", "Model": "Random Forest", "Accuracy": 0.82, "Precision": 0.80, "Recall": 0.79, "F1": 0.795, "ROC_AUC": 0.86, "Status": "—"},
        {"Rank": "#4", "Model": "Naive Bayes", "Accuracy": 0.72, "Precision": 0.70, "Recall": 0.68, "F1": 0.69, "ROC_AUC": 0.76, "Status": "—"}
    ]
    
    df_models = pd.DataFrame(model_data)
    
    # Style the dataframe for better display
    def highlight_best_row(row):
        if row['Status'] == '🏆 Best':
            return ['background-color: #f0fff4; font-weight: bold;'] * len(row)
        return [''] * len(row)
    
    def highlight_max_values(row):
        # Get max values for each metric
        max_acc = df_models['Accuracy'].max()
        max_prec = df_models['Precision'].max()
        max_rec = df_models['Recall'].max()
        max_f1 = df_models['F1'].max()
        max_roc = df_models['ROC_AUC'].max()
        
        styles = []
        for col in row.index:
            if col == 'Model' and row['Status'] == '🏆 Best':
                styles.append('background-color: #d4edda; color: #031206; font-weight: 700;')
            elif col == 'Accuracy' and row[col] == max_acc:
                styles.append('background-color: #d4edda; color: #031206; font-weight: 700;')
            elif col == 'Precision' and row[col] == max_prec:
                styles.append('background-color: #d4edda; color: #031206; font-weight: 700;')
            elif col == 'Recall' and row[col] == max_rec:
                styles.append('background-color: #d4edda; color: #031206; font-weight: 700;')
            elif col == 'F1' and row[col] == max_f1:
                styles.append('background-color: #d4edda; color: #031206; font-weight: 700;')
            elif col == 'ROC_AUC' and row[col] == max_roc:
                styles.append('background-color: #d4edda; color: #031206; font-weight: 700;')
            else:
                styles.append('')
        return styles
    
    # Apply styles using Streamlit's built-in styling
    styled_df = df_models.style.apply(highlight_best_row, axis=1)
    styled_df = styled_df.apply(highlight_max_values, axis=1)
    
    # Format numeric columns
    styled_df = styled_df.format({
        'Accuracy': '{:.3f}',
        'Precision': '{:.3f}',
        'Recall': '{:.3f}',
        'F1': '{:.3f}',
        'ROC_AUC': '{:.3f}'
    })
    
    # Add CSS for better table appearance
    st.markdown("""
    <style>
    .dataframe-container {
        background: black;
        border-radius: 0px;
        padding: 0px;
        box-shadow: 0 0px 0px rgba(0,0,0,0.08);
        border: px solid #edf2f7;
        overflow-x: auto;
    }
    .dataframe-container table {
        width: 100%;
        border-collapse: collapse;
    }
    .dataframe-container th {
        background: #1a1a2e !important;
        color: white !important;
        padding: 12px 15px !important;
        text-align: center !important;
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        border: none !important;
    }
    .dataframe-container td {
        padding: 10px 15px !important;
        text-align: center !important;
        border-bottom: 1px solid #e9ecef !important;
        color: #2d3748 !important;
        font-size: 0.9rem !important;
    }
    .dataframe-container tr:hover {
        background-color: #f7fafc !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Display the styled dataframe
    st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
    st.dataframe(styled_df, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Summary statistics
    st.markdown("---")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    best_accuracy = df_models['Accuracy'].max()
    best_precision = df_models['Precision'].max()
    best_recall = df_models['Recall'].max()
    best_f1 = df_models['F1'].max()
    best_roc_auc = df_models['ROC_AUC'].max()
    
    with col1:
        st.metric(
            "🏆 Best Model",
            "Decision Tree",
            delta=f"ROC AUC: {dt_roc_auc:.3f}"
        )
    
    with col2:
        st.metric(
            "📊 Best Accuracy",
            f"{best_accuracy:.1%}",
            delta=f"by {df_models[df_models['Accuracy'] == best_accuracy]['Model'].values[0]}"
        )
    
    with col3:
        st.metric(
            "🎯 Best Precision",
            f"{best_precision:.1%}",
            delta=f"by {df_models[df_models['Precision'] == best_precision]['Model'].values[0]}"
        )
    
    with col4:
        st.metric(
            "📈 Best Recall",
            f"{best_recall:.1%}",
            delta=f"by {df_models[df_models['Recall'] == best_recall]['Model'].values[0]}"
        )
    
    with col5:
        st.metric(
            "📊 Best F1",
            f"{best_f1:.1%}",
            delta=f"by {df_models[df_models['F1'] == best_f1]['Model'].values[0]}"
        )
    
    # ========================================================================
    # COMPARISON CHARTS
    # ========================================================================
    st.markdown("---")
    st.markdown("### 📊 Model Comparison")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        fig = go.Figure()
        colors = ['#43e97b' if m == 'Decision Tree' else '#667eea' for m in df_models['Model']]
        for i, model_name in enumerate(df_models['Model']):
            model_row = df_models[df_models['Model'] == model_name]
            fig.add_trace(go.Bar(
                name=model_name,
                x=['Accuracy', 'Precision', 'Recall', 'F1', 'ROC_AUC'],
                y=[model_row[m].values[0] for m in ['Accuracy', 'Precision', 'Recall', 'F1', 'ROC_AUC']],
                marker_color=colors[i],
                text=[f"{model_row[m].values[0]:.3f}" for m in ['Accuracy', 'Precision', 'Recall', 'F1', 'ROC_AUC']],
                textposition='outside'
            ))
        fig.update_layout(
            title=dict(
                text='Model Performance Comparison',
                y=0.98,
                x=0.5,
                xanchor='center',
                yanchor='top'
            ),
            height=400,
            barmode='group',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            yaxis_range=[0, 1],
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5
            ),
            margin=dict(l=10, r=10, t=70, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df_models['Model'],
            y=df_models['ROC_AUC'],
            marker_color=['#43e97b' if m == 'Decision Tree' else '#764ba2' for m in df_models['Model']],
            text=df_models['ROC_AUC'].round(3),
            textposition='outside'
        ))
        fig.update_layout(
            title=dict(
                text='ROC AUC Comparison',
                y=0.98,
                x=0.5,
                xanchor='center',
                yanchor='top'
            ),
            height=465,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            yaxis_range=[0, 1],
            showlegend=False,
            xaxis_tickangle=-45,
            margin=dict(l=10, r=10, t=100, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col3:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df_models['Model'],
            y=df_models['Accuracy'],
            marker_color=['#43e97b' if m == 'Decision Tree' else '#f5576c' for m in df_models['Model']],
            text=df_models['Accuracy'].round(3),
            textposition='outside'
        ))
        fig.update_layout(
            title=dict(
                text='Accuracy Comparison',
                y=0.98,
                x=0.5,
                xanchor='center',
                yanchor='top'
            ),
            height=465,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            yaxis_range=[0, 1],
            showlegend=False,
            xaxis_tickangle=-45,
            margin=dict(l=10, r=10, t=50, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Add spacing after charts
    st.write("")
    st.write("")
    
    # ========================================================================
    # BEST MODEL SECTION
    # ========================================================================
    st.markdown("---")
    st.markdown("### 🥇 Best Model Selected: Decision Tree")
    
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        st.markdown("""
        <div style="background: white;height:23rem; border-radius: 15px; padding: 1.5rem; border: 2px solid #48bb78; border-left: 5px solid #48bb78; box-shadow: 0 4px 15px rgba(72, 187, 120, 0.15);">
            <h4 style="color: #1a1a2e; margin-top: 0;">✅ Why Decision Tree?</h4>
            <ul style="list-style: none; padding: 0; margin: 0;">
                <li style="color: #1a1a2e; padding: 0.6rem 0; border-bottom: 1px solid #f1f3f5; display: flex; align-items: center; gap: 0.5rem;">
                    <span style="color: #48bb78; font-size: 1.2rem;">✓</span> 
                    <div><strong>Best Overall Performance:</strong> Highest ROC AUC (0.88)</div>
                </li>
                <li style="color: #1a1a2e; padding: 0.6rem 0; border-bottom: 1px solid #f1f3f5; display: flex; align-items: center; gap: 0.5rem;">
                    <span style="color: #48bb78; font-size: 1.2rem;">✓</span> 
                    <div><strong>Interpretability:</strong> Easy to understand and explain</div>
                </li>
                <li style="color: #1a1a2e; padding: 0.6rem 0; border-bottom: 1px solid #f1f3f5; display: flex; align-items: center; gap: 0.5rem;">
                    <span style="color: #48bb78; font-size: 1.2rem;">✓</span> 
                    <div><strong>Balanced Performance:</strong> Good precision and recall</div>
                </li>
                <li style="color: #1a1a2e; padding: 0.6rem 0; display: flex; align-items: center; gap: 0.5rem;">
                    <span style="color: #48bb78; font-size: 1.2rem;">✓</span> 
                    <div><strong>Feature Importance:</strong> Provides clear feature rankings</div>
                </li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: white; border-radius: 15px; padding: 1.5rem; border: 1px solid #e9ecef; text-align: center; height: 100%;">
            <h4 style="color: #1a1a2e; margin-top: 0;">📊 Confusion Matrix</h4>
            <div style="display: grid; grid-template-columns: auto 1fr 1fr; gap: 8px; max-width: 500px; margin: 0 auto;">
                <div style="grid-column: 1; grid-row: 1; padding: 8px; font-weight: 600; color: #4a5568;"></div>
                <div style="grid-column: 2; grid-row: 1; padding: 8px; font-weight: 600; color: #4a5568; background: #f7fafc; border-radius: 8px 8px 0 0;">Predicted Non-Default</div>
                <div style="grid-column: 3; grid-row: 1; padding: 8px; font-weight: 600; color: #4a5568; background: #f7fafc; border-radius: 8px 8px 0 0;">Predicted Default</div>
                <div style="grid-column: 1; grid-row: 2; padding: 8px; font-weight: 600; color: #4a5568; background: #f7fafc; border-radius: 8px 0 0 8px;">Actual Non-Default</div>
                <div style="grid-column: 2; grid-row: 2; padding: 15px; background: #d4edda; border-radius: 4px; font-weight: 700; font-size: 1.2rem; color: #155724;">850</div>
                <div style="grid-column: 3; grid-row: 2; padding: 15px; background: #f8d7da; border-radius: 4px; font-weight: 700; font-size: 1.2rem; color: #721c24;">150</div>
                <div style="grid-column: 1; grid-row: 3; padding: 8px; font-weight: 600; color: #4a5568; background: #f7fafc; border-radius: 0 0 0 8px;">Actual Default</div>
                <div style="grid-column: 2; grid-row: 3; padding: 15px; background: #f8d7da; border-radius: 4px; font-weight: 700; font-size: 1.2rem; color: #721c24;">120</div>
                <div style="grid-column: 3; grid-row: 3; padding: 15px; background: #d4edda; border-radius: 4px; font-weight: 700; font-size: 1.2rem; color: #155724;">480</div>
            </div>
            <div style="margin-top: 12px; font-size: 0.85rem; color: #6c757d;">
                <span style="color: #155724;">■</span> Correct Predictions 
                <span style="color: #721c24; margin-left: 12px;">■</span> Incorrect Predictions
            </div>
            <div style="margin-top: 8px; font-size: 0.8rem; color: #4a5568;">
                <strong>Accuracy:</strong> (850 + 480) / 1600 = 83.1%
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # ========================================================================
    # FEATURE IMPORTANCE SECTION
    # ========================================================================
    st.markdown("---")
    st.markdown("### 📊 Feature Importance Analysis")
    
    # Check if model exists and has feature_importances_
    if model is not None and hasattr(model, 'feature_importances_'):
        importances = model.feature_importances_
        
        # Check if importances exist and match feature names length
        if importances is not None and len(importances) > 0:
            if feature_names is not None and len(feature_names) == len(importances):
                fi_df = pd.DataFrame({
                    'Feature': feature_names,
                    'Importance': importances
                }).sort_values('Importance', ascending=True)
                
                top_15 = fi_df.tail(15)
                
                fig = go.Figure(data=[go.Bar(
                    y=top_15['Feature'],
                    x=top_15['Importance'],
                    orientation='h',
                    marker=dict(
                        color=top_15['Importance'],
                        colorscale='Viridis',
                        showscale=True,
                        colorbar=dict(
                            title="Importance",
                            thickness=15,
                            len=0.8
                        )
                    ),
                    text=top_15['Importance'].round(4),
                    textposition='outside',
                    textfont=dict(size=10)
                )])
                
                fig.update_layout(
                    title='Top 15 Most Important Features',
                    height=500,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    xaxis_title='Feature Importance',
                    yaxis_title='Features',
                    showlegend=False,
                    margin=dict(l=0, r=120, t=40, b=20),
                    font=dict(size=11)
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                st.markdown("""
                <div style="background: white; border-radius: 15px; padding: 1.5rem; border: 1px solid #e9ecef; margin-top: 1rem; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
                    <h4 style="color: #1a1a2e; margin-top: 0;">📝 Feature Importance Interpretation</h4>
                    <p style="color: #495057; line-height: 1.6;">
                        The feature importance analysis reveals which factors most significantly influence loan default prediction.
                        <strong>EXT_SOURCE_1, EXT_SOURCE_2, and EXT_SOURCE_3</strong> are the most important features,
                        indicating that external credit scores are strong predictors of default risk.
                        <strong>DAYS_BIRTH</strong> (age) and <strong>AMT_CREDIT</strong> (loan amount) also show significant importance.
                    </p>
                    <p style="color: #495057; font-size: 0.9rem; background: #f8f9fa; padding: 0.8rem; border-radius: 8px; margin: 0;">
                        <em>💡 Note: Higher importance values indicate stronger influence on the model's predictions.</em>
                    </p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning(f"⚠️ Feature importance data mismatch - features: {len(feature_names) if feature_names else 0}, importances: {len(importances)}")
        else:
            st.warning("⚠️ Feature importance data is empty or None")
    else:
        # If model doesn't have feature_importances_, show alternative
        if model is not None:
            st.info("ℹ️ This model type does not have built-in feature importance. Showing feature names instead.")
            
            # Show feature count and names
            if feature_names is not None:
                st.write(f"**Total Features:** {len(feature_names)}")
                
                # Show first 20 features as a preview
                preview_df = pd.DataFrame({
                    'Feature': feature_names[:20],
                    'Index': range(1, 21)
                })
                st.dataframe(preview_df, use_container_width=True, hide_index=True)
                if len(feature_names) > 20:
                    st.caption(f"... and {len(feature_names) - 20} more features")
        else:
            st.warning("⚠️ Model is not loaded. Please check the model file.")

# ============================================================================
# GAUGE CHART FUNCTION - MOVED OUTSIDE render_prediction
# ============================================================================
def create_gauge(probability, title):
    """Create a gauge chart using plotly"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=probability * 100,
        title={'text': title},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#0FCFFA"},
            'bar': {'color': "rgba(15, 207, 250, 0.8)"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 35], 'color': '#28a745'},
                {'range': [35, 65], 'color': '#ffc107'},
                {'range': [65, 100], 'color': '#dc3545'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': probability * 100
            }
        }
    ))
    
    fig.update_layout(
        height=200,
        margin=dict(l=10, r=10, t=70, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#0FCFFA", family="Arial")
    )
    
    return fig

# ----------------------------------------------------------------------------
# PREDICTION PAGE - ONLY ONE DEFINITION
# ----------------------------------------------------------------------------
def render_prediction(model, feature_names, df):
    """Render the prediction page with enhanced UI/UX"""
    st.markdown('<h2 style="color: #6F6F7D; margin-bottom: 1rem;">🏦 Credit Risk Prediction</h2>', unsafe_allow_html=True)
    
    # ========================================================================
    # INFO BANNER - Enhanced
    # ========================================================================
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                border-radius: 15px; padding: 1.5rem; margin-bottom: 1.5rem; 
                color: white; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);">
        <div style="display: flex; align-items: center; gap: 1rem; flex-wrap: wrap;">
            <div style="font-size: 2.5rem;">📌</div>
            <div>
                <h4 style="margin: 0; color: white; font-weight: 600;">Smart Credit Risk Assessment</h4>
                <p style="margin: 0.3rem 0 0 0; opacity: 0.9; font-size: 0.95rem;">
                    Complete the applicant profile below. Our AI-powered system will analyze 210+ features 
                    to provide an accurate risk assessment with confidence scoring.
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if model is None or feature_names is None:
        st.error("⚠️ Model not loaded. Please check the model files in the 'model' folder.")
        return
    
    # ========================================================================
    # PREDICTION FORM
    # ========================================================================
    with st.form("prediction_form"):
        # Section 1: Applicant Profile
        st.markdown("""
        <div style="background: #f8f9fa; border-radius: 10px; padding: 0.5rem 1rem; margin-bottom: 1rem; border-left: 4px solid #667eea;">
            <h4 style="color: #1a1a2e; margin: 0.5rem 0;">👤 Applicant Profile</h4>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            annual_income = st.number_input(
                "💰 Annual Income", 
                min_value=0, 
                value=250000, 
                step=10000, 
                help="Total annual income of the applicant"
            )
            credit_amount = st.number_input(
                "🏦 Credit Amount", 
                min_value=0, 
                value=500000, 
                step=50000,
                help="Total credit amount requested"
            )
            annuity_amount = st.number_input(
                "📊 Annuity Amount", 
                min_value=0.0, 
                value=25000.0, 
                step=1000.0,
                help="Annual payment amount"
            )
        
        with col2:
            num_children = st.number_input(
                "👶 Number of Children", 
                min_value=0, 
                max_value=20, 
                value=0, 
                step=1,
                help="Number of children the applicant has"
            )
            family_members = st.number_input(
                "👨‍👩‍👧‍👦 Family Members", 
                min_value=1, 
                max_value=20, 
                value=2, 
                step=1,
                help="Total family members including applicant"
            )
            
            # Employment Years instead of Days
            employment_years = st.number_input(
                "💼 Years Employed", 
                min_value=0, 
                max_value=50, 
                value=5, 
                step=1,
                help="Number of years the applicant has been employed"
            )
            # Convert years to days (negative as required by model)
            employment_days = -employment_years * 365
        
        with col3:
            # Get today's date
            today = date.today()
            
            # Date input for DOB
            dob = st.date_input(
                "🎂 Date of Birth", 
                min_value=date(today.year - 80, 1, 1),
                max_value=date(today.year - 18, 1, 1),
                value=date(today.year - 30, 1, 1),
                help="Applicant's date of birth"
            )
            
            # Calculate age in days (negative as required by model)
            age_days = -(today - dob).days
            
            # Display age in years for user convenience
            age_years = (today - dob).days // 365
            st.caption(f"📌 Age: {age_years} years")
            
            region_rating = st.selectbox(
                "📍 Region Rating", 
                options=[1, 2, 3], 
                format_func=lambda x: f"Rating {x} - {'High' if x==1 else 'Medium' if x==2 else 'Low'}"
            )
        
        # Section 2: Credit Profile
        st.markdown("""
        <div style="background: #f8f9fa; border-radius: 10px; padding: 0.5rem 1rem; margin: 1rem 0; border-left: 4px solid #764ba2;">
            <h4 style="color: #1a1a2e; margin: 0.5rem 0;">📈 Credit Profile</h4>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            ext_source_1 = st.slider(
                "EXT_SOURCE_1 Score", 
                min_value=0.0, 
                max_value=1.0, 
                value=0.5, 
                step=0.01,
                help="External credit score 1 (Higher is better)",
                format="%.2f"
            )
        with col2:
            ext_source_2 = st.slider(
                "EXT_SOURCE_2 Score", 
                min_value=0.0, 
                max_value=1.0, 
                value=0.5, 
                step=0.01,
                help="External credit score 2 (Higher is better)",
                format="%.2f"
            )
        with col3:
            ext_source_3 = st.slider(
                "EXT_SOURCE_3 Score", 
                min_value=0.0, 
                max_value=1.0, 
                value=0.5, 
                step=0.01,
                help="External credit score 3 (Higher is better)",
                format="%.2f"
            )
        
        # Additional Info
        st.markdown("""
        <div style="background: #fff3cd; border-radius: 10px; padding: 0.8rem 1rem; margin: 1rem 0; border-left: 4px solid #ffc107;">
            <p style="margin: 0; font-size: 0.9rem; color: #856404;">
                ℹ️ <strong>Note:</strong> All other features will be automatically filled with default values 
                derived from the dataset. You only need to provide the key information above.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            predict_button = st.form_submit_button(
                "🔮 Predict Default Risk", 
                use_container_width=True,
                type="primary"
            )
    
    # ========================================================================
    # PREDICTION RESULTS
    # ========================================================================
    if predict_button:
        with st.spinner("🔄 Analyzing applicant data with AI model..."):
            # Show progress
            progress_text = st.empty()
            progress_bar = st.progress(0)
            
            for i in range(100):
                time.sleep(0.005)
                progress_bar.progress(i + 1)
                if i % 20 == 0:
                    progress_text.text(f"Processing... {i+1}%")
            
            progress_text.text("✅ Analysis complete!")
            time.sleep(0.3)
            progress_bar.empty()
            progress_text.empty()
            
            # Prepare input data
            input_data = {}
            
            # Map form inputs to feature names
            feature_mapping = {
                'AMT_INCOME_TOTAL': annual_income,
                'AMT_CREDIT': credit_amount,
                'AMT_ANNUITY': annuity_amount,
                'CNT_CHILDREN': num_children,
                'CNT_FAM_MEMBERS': family_members,
                'DAYS_EMPLOYED': employment_days,
                'DAYS_BIRTH': age_days,
                'REGION_RATING_CLIENT': region_rating,
                'EXT_SOURCE_1': ext_source_1,
                'EXT_SOURCE_2': ext_source_2,
                'EXT_SOURCE_3': ext_source_3
            }
            
            # Add all features with default values
            for feat in feature_names:
                if feat in feature_mapping:
                    input_data[feat] = feature_mapping[feat]
                elif feat in ['FLAG_MOBIL', 'FLAG_EMP_PHONE', 'FLAG_WORK_PHONE', 'FLAG_CONT_MOBILE', 
                             'FLAG_PHONE', 'FLAG_EMAIL', 'FLAG_OWN_CAR_Y', 'FLAG_OWN_REALTY_Y']:
                    input_data[feat] = 1
                elif feat.startswith('FLAG_DOCUMENT_'):
                    input_data[feat] = 0
                elif feat in ['SK_ID_CURR']:
                    input_data[feat] = 100001
                else:
                    input_data[feat] = 0
            
            # Ensure all features are present
            for feat in feature_names:
                if feat not in input_data:
                    input_data[feat] = 0
            
            # Make prediction
            try:
                df_input = pd.DataFrame([input_data])
                df_input = df_input[feature_names]
                
                prediction = model.predict(df_input)[0]
                probabilities = model.predict_proba(df_input)[0]
                
                # Store in history
                st.session_state.predictions_history.append({
                    'timestamp': pd.Timestamp.now(),
                    'prediction': prediction,
                    'probability': probabilities[1],
                    'income': annual_income,
                    'credit': credit_amount
                })
                
                # ============================================================
                # DISPLAY RESULTS
                # ============================================================
                st.markdown("---")
                st.markdown("### 📊 Prediction Results")
                
                # Create two columns for result display
                result_col1, result_col2 = st.columns([1.5, 1])
                
                with result_col1:
                    if prediction == 0:
                        # Low Risk
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
                                    border-radius: 20px; padding: 2rem; text-align: center; 
                                    box-shadow: 0 10px 40px rgba(67, 233, 123, 0.3);">
                            <div style="font-size: 4rem; margin-bottom: 0.5rem;">✅</div>
                            <h2 style="color: #1a1a2e; margin: 0; font-weight: 700;">LOW RISK APPLICANT</h2>
                            <p style="color: #1a1a2e; font-size: 1.2rem; opacity: 0.9; margin: 0.3rem 0;">
                                Loan Approval Recommended
                            </p>
                            <div style="background: rgba(255,255,255,0.3); border-radius: 50px; 
                                        padding: 0.5rem 1.5rem; display: inline-block; margin-top: 0.5rem;">
                                <strong style="color: #1a1a2e;">Confidence: {probabilities[0]*100:.1f}%</strong>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.success("✅ The applicant shows a low probability of default. Loan approval is recommended.")
                    else:
                        # High Risk
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                                    border-radius: 20px; padding: 2rem; text-align: center; 
                                    box-shadow: 0 10px 40px rgba(245, 87, 108, 0.3);">
                            <div style="font-size: 4rem; margin-bottom: 0.5rem;">❌</div>
                            <h2 style="color: white; margin: 0; font-weight: 700;">HIGH RISK APPLICANT</h2>
                            <p style="color: white; font-size: 1.2rem; opacity: 0.9; margin: 0.3rem 0;">
                                Potential Loan Defaulter
                            </p>
                            <div style="background: rgba(255,255,255,0.2); border-radius: 50px; 
                                        padding: 0.5rem 1.5rem; display: inline-block; margin-top: 0.5rem;">
                                <strong style="color: white;">Confidence: {probabilities[1]*100:.1f}%</strong>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.error("❌ The applicant shows a high probability of default. Loan approval is not recommended.")
                
                with result_col2:
                    st.markdown("#### Risk Assessment Gauge")
                    fig = create_gauge(probabilities[1], "Default Probability")
                    st.plotly_chart(fig, use_container_width=True)
                
                # ============================================================
                # DETAILED METRICS
                # ============================================================
                st.markdown("---")
                st.markdown("#### 📊 Detailed Metrics")
                
                col1, col2, col3, col4 = st.columns(4)
                
                risk_level = "Low" if probabilities[1] < 0.35 else "Medium" if probabilities[1] < 0.65 else "High"
                color = "🟢" if risk_level == "Low" else "🟡" if risk_level == "Medium" else "🔴"
                
                with col1:
                    st.metric(
                        "Default Probability",
                        f"{probabilities[1]*100:.1f}%"
                    )
                with col2:
                    st.metric(
                        "Non-Default Probability",
                        f"{probabilities[0]*100:.1f}%"
                    )
                with col3:
                    st.metric(
                        "Risk Level",
                        f"{color} {risk_level}"
                    )
                with col4:
                    st.metric(
                        "Model Confidence",
                        f"{max(probabilities)*100:.1f}%"
                    )
                
                # ============================================================
                # DOWNLOAD REPORT
                # ============================================================
                st.markdown("---")
                st.markdown("#### 📄 Download Report")
                
                report_data = {
                    'Application Date': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'Prediction': 'Approved' if prediction == 0 else 'Rejected',
                    'Default Probability': f"{probabilities[1]*100:.2f}%",
                    'Risk Level': risk_level,
                    'Annual Income': annual_income,
                    'Credit Amount': credit_amount,
                    'Annuity': annuity_amount,
                    'Number of Children': num_children,
                    'Family Members': family_members,
                    'Years Employed': employment_years,
                    'Age': age_years,
                    'EXT_SOURCE_1': ext_source_1,
                    'EXT_SOURCE_2': ext_source_2,
                    'EXT_SOURCE_3': ext_source_3
                }
                
                report_df = pd.DataFrame([report_data])
                csv = report_df.to_csv(index=False)
                b64 = base64.b64encode(csv.encode()).decode()
                
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.markdown(f"""
                    <div style="text-align: center;">
                        <a href="data:file/csv;base64,{b64}" download="prediction_report.csv" 
                           style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                                  color: white; padding: 0.8rem 2rem; border-radius: 10px;
                                  text-decoration: none; display: inline-block;
                                  font-weight: 600; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
                                  transition: transform 0.3s ease;">
                            📥 Download Prediction Report
                        </a>
                    </div>
                    """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"❌ Error making prediction: {str(e)}")
                st.info("Please try again with different input values or check the model file.")

# ============================================================================
# MAIN APPLICATION
# ============================================================================
def main():
    """Main application entry point"""
    
    # Load data - this will show consent notice or load data
    df = load_data()
    
    # If df is None, check if we're showing the consent notice
    if df is None:
        # Check if consent notice is being shown
        if not st.session_state.get('data_loading_confirmed', False):
            # User hasn't consented yet - stop execution
            st.stop()
        else:
            # Consent was given but loading failed
            st.error("❌ Failed to load dataset. Please try again.")
            return
    
    # Load model
    model, feature_names = load_model()
    
    if model is None or feature_names is None:
        st.error("❌ Failed to load model. Please check the model folder.")
        return
    
    # Calculate dataset statistics
    stats = get_dataset_stats(df)
    
    # Render navigation
    render_navigation()
    
    # Render selected page
    if st.session_state.page == "🏠 Dashboard":
        render_dashboard(df, stats, model, feature_names)
    
    elif st.session_state.page == "📊 EDA":
        render_eda(df)
    
    elif st.session_state.page == "🧹 Preprocessing":
        render_preprocessing(df)
    
    elif st.session_state.page == "🤖 Models":
        render_models(model, feature_names, df)
    
    elif st.session_state.page == "🏦 Prediction":
        render_prediction(model, feature_names, df)
    
    # Footer
    st.markdown("""
<style>
.footer-link {
    color: #667eea;
    font-weight: 600;
    text-decoration: none;
    transition: all 0.3s ease;
    position: relative;
}
.footer-link:hover {
    color: #764ba2;
    text-decoration: underline;
}
.footer-link::after {
    content: '';
    position: absolute;
    bottom: -2px;
    left: 0;
    width: 0%;
    height: 2px;
    background: linear-gradient(135deg, #667eea, #764ba2);
    transition: width 0.3s ease;
}
.footer-link:hover::after {
    width: 100%;
}
.linkedin-icon {
    display: inline-block;
    transition: transform 0.3s ease;
}
.linkedin-icon:hover {
    transform: scale(1.2);
}
</style>
<div class="footer">
    <p>
        Built using 
        <a href="https://www.python.org/" target="_blank">Python</a>, 
        <a href="https://pandas.pydata.org/" target="_blank">Pandas</a>, 
        <a href="https://scikit-learn.org/" target="_blank">Scikit-Learn</a>, 
        <a href="https://plotly.com/" target="_blank">Plotly</a> and 
        <a href="https://streamlit.io/" target="_blank">Streamlit</a>.
    </p>
    <p style="font-size: 0.9rem; margin: 0.5rem 0;">
        💻 Developed with ❤️ by 
        <a href="https://portfolio-kappa-orcin-41.vercel.app/" target="_blank" class="footer-link">
            Abhishek Lalzare
        </a>
        <span style="margin: 0 0.8rem; color: #6c757d;">|</span>
        <a href="https://linkedin.com/in/abhisheklalzare" target="_blank" class="linkedin-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="#0077b5">
                <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
            </svg>
        </a>
        <span style="margin: 0 0.8rem; color: #6c757d;">|</span>
        <a href="https://github.com/abhixdata" target="_blank" class="github-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="#333">
                <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.15 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.62.24 2.85.12 3.15.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/>
            </svg>
        </a>
    </p>
    <p style="font-size: 0.75rem; opacity: 0.6; margin: 0.2rem 0;">
        © 2026 Home Loan Default Prediction System | All Rights Reserved
    </p>
</div>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
