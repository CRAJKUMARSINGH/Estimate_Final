#!/usr/bin/env python3
"""
UNIFIED Construction Estimation System
Consolidated version with all improvements integrated cleanly
- Enhanced Excel Import with Format Preservation
- Real-time Calculations
- Database Integration
- Template System
- Advanced Analytics
"""

import streamlit as st
import pandas as pd
import numpy as np
import openpyxl
from openpyxl import load_workbook, Workbook
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from datetime import datetime
import sqlite3
import json
import io
import re
import math
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Optional, Tuple
import tempfile
import os
from pathlib import Path

# Set page config - MUST be first Streamlit command
st.set_page_config(
    page_title="Construction Estimation System - Unified",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ====================================================