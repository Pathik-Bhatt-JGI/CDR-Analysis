# ================================================================
#  CDR FORENSICS PRO  v9.1 — COMPACT NAV
#  Premium Cyber Intelligence & Digital Forensics Platform
#  Top navigation bar with reduced spacing
# ================================================================

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random, math, hashlib, requests, re, io
import numpy as np
from collections import Counter

st.set_page_config(
    page_title="CDR Forensics Pro",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  SVG ICONS
# ─────────────────────────────────────────────
ANDROID_SVG = """<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="64" height="64"><path d="M6 18c0 .55.45 1 1 1h1v3.5c0 .83.67 1.5 1.5 1.5s1.5-.67 1.5-1.5V19h2v3.5c0 .83.67 1.5 1.5 1.5s1.5-.67 1.5-1.5V19h1c.55 0 1-.45 1-1V8H6v10zm-2.5-10C2.67 8 2 8.67 2 9.5v7c0 .83.67 1.5 1.5 1.5S5 17.33 5 16.5v-7C5 8.67 4.33 8 3.5 8zm17 0c-.83 0-1.5.67-1.5 1.5v7c0 .83.67 1.5 1.5 1.5s1.5-.67 1.5-1.5v-7c0-.83-.67-1.5-1.5-1.5zm-4.97-5.84l1.3-1.3c.2-.2.2-.51 0-.71-.2-.2-.51-.2-.71 0l-1.48 1.48A5.84 5.84 0 0 0 12 1.5c-.96 0-1.86.23-2.66.63L7.85.65a.499.499 0 1 0-.71.71l1.31 1.31A5.969 5.969 0 0 0 6 7h12a5.96 5.96 0 0 0-2.47-4.84zM10 5H9V4h1v1zm5 0h-1V4h1v1z"/></svg>"""
APPLE_SVG   = """<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" fill="currentColor" width="64" height="64"><path d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.8-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M13 3.5c.73-.83 1.94-1.46 2.94-1.5.13 1.17-.34 2.35-1.04 3.19-.69.85-1.83 1.51-2.95 1.42-.15-1.15.41-2.35 1.05-3.11z"/></svg>"""
TOWER_SVG   = """<svg viewBox="0 0 24 24" fill="currentColor" width="28" height="28"><path d="M1.75 7.18L0 5.43C2.64 2.61 6.22 1 10 1s7.36 1.61 10 4.43l-1.75 1.75C16.16 4.77 13.18 3.5 10 3.5S3.84 4.77 1.75 7.18zm4.48 4.48L4.48 9.91C6.14 8.1 8.46 7 11.01 7S15.88 8.1 17.54 9.91l-1.75 1.75C14.5 10.23 12.83 9.5 11 9.5c-1.83 0-3.5.73-4.77 2.16zM11 13c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm-1 9h2v-3.27c.44-.14.85-.35 1.22-.63L17 20l1-1.73L14.2 16.7c.15-.55.2-1.12.1-1.7h3.7v-2H14.3c-.38-1.1-1.2-2-2.3-2.35V10h-2v.65C8.9 11 8.08 11.9 7.7 13H4v2h3.7c-.1.58-.05 1.15.1 1.7L5 18.27 6 20l3.78-1.9c.37.28.78.49 1.22.63V22z"/></svg>"""
UPLOAD_SVG  = """<svg viewBox="0 0 24 24" fill="currentColor" width="28" height="28"><path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm4 18H6V4h7v5h5v11zM8 15.01l1.41 1.41L11 14.84V19h2v-4.16l1.59 1.59L16 15.01 12.01 11 8 15.01z"/></svg>"""
DASHBOARD_SVG="""<svg viewBox="0 0 24 24" fill="currentColor" width="28" height="28"><path d="M3 13h8V3H3v10zm0 8h8v-6H3v6zm10 0h8V11h-8v10zm0-18v6h8V3h-8z"/></svg>"""
MAP_SVG     = """<svg viewBox="0 0 24 24" fill="currentColor" width="28" height="28"><path d="M20.5 3l-.16.03L15 5.1 9 3 3.36 4.9c-.21.07-.36.25-.36.48V20.5c0 .28.22.5.5.5l.16-.03L9 18.9l6 2.1 5.64-1.9c.21-.07.36-.25.36-.48V3.5c0-.28-.22-.5-.5-.5zM15 19l-6-2.11V5l6 2.11V19z"/></svg>"""
RECORDS_SVG = """<svg viewBox="0 0 24 24" fill="currentColor" width="28" height="28"><path d="M20 3H4v10c0 2.21 1.79 4 4 4h6c2.21 0 4-1.79 4-4v-3h2c1.11 0 2-.89 2-2V5c0-1.11-.89-2-2-2zm0 5h-2V5h2v3zM4 19h16v2H4z"/></svg>"""
CONTACTS_SVG= """<svg viewBox="0 0 24 24" fill="currentColor" width="28" height="28"><path d="M20 0H4v2h16V0zm0 4H4v2h16V4zm0 4H4v13c0 1.66 1.34 3 3 3h10c1.66 0 3-1.34 3-3V8zm-8 2.5c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm6 9.5H6v-.75C6 17.56 8.69 16 12 16s6 1.56 6 2.75V21z"/></svg>"""

# ─────────────────────────────────────────────
#  STATIC DATABASES
# ─────────────────────────────────────────────
MCC_DB = {
    "404":{"country":"India","flag":"IN","region":"South Asia"},
    "405":{"country":"India","flag":"IN","region":"South Asia"},
    "310":{"country":"United States","flag":"US","region":"North America"},
    "311":{"country":"United States","flag":"US","region":"North America"},
    "234":{"country":"United Kingdom","flag":"GB","region":"Europe"},
    "208":{"country":"France","flag":"FR","region":"Europe"},
    "262":{"country":"Germany","flag":"DE","region":"Europe"},
    "724":{"country":"Brazil","flag":"BR","region":"South America"},
    "460":{"country":"China","flag":"CN","region":"Asia"},
    "440":{"country":"Japan","flag":"JP","region":"Asia"},
    "505":{"country":"Australia","flag":"AU","region":"Oceania"},
    "302":{"country":"Canada","flag":"CA","region":"North America"},
    "410":{"country":"Pakistan","flag":"PK","region":"South Asia"},
    "413":{"country":"Sri Lanka","flag":"LK","region":"South Asia"},
    "420":{"country":"Saudi Arabia","flag":"SA","region":"Middle East"},
    "424":{"country":"UAE","flag":"AE","region":"Middle East"},
    "525":{"country":"Singapore","flag":"SG","region":"Southeast Asia"},
    "502":{"country":"Malaysia","flag":"MY","region":"Southeast Asia"},
    "602":{"country":"Egypt","flag":"EG","region":"Africa"},
}
MNC_DB = {
    "404":{"10":"Bharti Airtel","20":"Vodafone IN","45":"Aircel","98":"BSNL","07":"BSNL","00":"BSNL","50":"Reliance Jio","70":"IDEA"},
    "405":{"840":"Reliance Jio","800":"Bharti Airtel","801":"Bharti Airtel","025":"Vodafone","030":"Vodafone","029":"IDEA","799":"BSNL"},
    "310":{"410":"AT&T","260":"T-Mobile","012":"Verizon"},
    "234":{"10":"O2 UK","20":"Three UK","30":"EE","15":"Vodafone UK"},
}
MCC_CENTERS = {
    "404":{"lat":20.5937,"lng":78.9629},"405":{"lat":20.5937,"lng":78.9629},
    "310":{"lat":37.0902,"lng":-95.7129},"234":{"lat":55.3781,"lng":-3.4360},
}
CALL_LABELS = {
    "MO_VOICE":"Outgoing Call","MT_VOICE":"Incoming Call",
    "MO_SMS":"Outgoing SMS","MT_SMS":"Incoming SMS",
    "MO_DATA":"Data Session","MT_DATA":"Data Session"
}
TYPE_COLORS = {
    "MO_VOICE":"#00FFB3","MT_VOICE":"#00B8FF",
    "MO_SMS":"#7B61FF","MT_SMS":"#FF6B35",
    "MO_DATA":"#FFD700","MT_DATA":"#FF3366"
}
NAV_OPTIONS = [
    "Device Selection","Tower Data Entry","Upload Bill PDF",
    "Dashboard","Analytics","Tower Map","All Records",
    "Contact Manager","Forensic Report",
]

NAV_ICONS = {
    "Device Selection": "",
    "Tower Data Entry": "",
    "Upload Bill PDF": "",
    "Dashboard": "",
    "Analytics": "",
    "Tower Map": "",
    "All Records": "",
    "Contact Manager": "",
    "Forensic Report": "",
}

AVATAR_GRADIENTS = [
    "linear-gradient(135deg,#00FFB3,#00B8FF)",
    "linear-gradient(135deg,#FF6B35,#FFD700)",
    "linear-gradient(135deg,#7B61FF,#00FFB3)",
    "linear-gradient(135deg,#00B8FF,#7B61FF)",
    "linear-gradient(135deg,#FFD700,#FF6B35)",
    "linear-gradient(135deg,#FF3366,#7B61FF)",
    "linear-gradient(135deg,#00FFB3,#7B61FF)",
    "linear-gradient(135deg,#00B8FF,#FF3366)",
]

# ─────────────────────────────────────────────
#  HELPERS (unchanged)
# ─────────────────────────────────────────────
def mcc_info(mcc):
    return MCC_DB.get(str(mcc).strip(), {"country":"Unknown","flag":"--","region":"Unknown"})

def mnc_info(mcc, mnc):
    ops = MNC_DB.get(str(mcc).strip(), {})
    m = str(mnc).strip()
    return ops.get(m, ops.get(m.lstrip("0"), f"Operator {mcc}/{mnc}"))

def fmt_dur(s):
    try: s = int(float(s))
    except: return "—"
    if s <= 0: return "—"
    d, rem = divmod(s, 86400)
    h, rem2 = divmod(rem, 3600)
    m, sc  = divmod(rem2, 60)
    if d > 0:
        return f"{d}d {h}h {m}m" if h > 0 else f"{d}d {m}m {sc}s"
    if h > 0:
        return f"{h}h {m}m {sc}s"
    if m > 0:
        return f"{m}m {sc}s"
    return f"{sc}s"

def fmt_dur_hms(s):
    try: s = int(float(s))
    except: return "00:00:00"
    if s <= 0: return "00:00:00"
    d, rem = divmod(s, 86400)
    h, rem2 = divmod(rem, 3600)
    m, sc  = divmod(rem2, 60)
    if d > 0:
        return f"{d}:{h:02d}:{m:02d}:{sc:02d}"
    return f"{h:02d}:{m:02d}:{sc:02d}"

def luhn(n):
    try:
        digits = [int(d) for d in str(n) if d.isdigit()]
        s = 0
        for i,d in enumerate(reversed(digits)):
            if i%2==1: d*=2;
            if d>9: d-=9
            s+=d
        return s%10==0
    except: return None

def _cache_key(mcc,mnc,lac,cell_id): return f"{mcc}_{mnc}_{lac}_{cell_id}"

def get_tower_location(mcc, mnc, lac, cell_id, radio="GSM"):
    key = _cache_key(mcc,mnc,lac,cell_id)
    if "tower_cache" not in st.session_state: st.session_state["tower_cache"]={}
    if key in st.session_state["tower_cache"]: return st.session_state["tower_cache"][key]
    api_key = st.session_state.get("ocid_key","").strip()
    if api_key:
        if api_key.startswith("pk."):
            try:
                r = requests.post("https://us1.unwiredlabs.com/v2/process.php",
                    json={"token":api_key,"radio":radio.lower(),"mcc":int(mcc),"mnc":int(mnc),"cells":[{"lac":int(lac),"cid":int(cell_id),"psc":0}]},timeout=5)
                d=r.json()
                if d.get("status")=="ok":
                    res={"lat":d["lat"],"lng":d["lon"],"range":d.get("accuracy",500),"source":"UnwiredLabs [Live]","found":True}
                    st.session_state["tower_cache"][key]=res; return res
            except: pass
        else:
            try:
                r=requests.get("https://opencellid.org/cell/get",params={"key":api_key,"mcc":int(mcc),"mnc":int(mnc),"lac":int(lac),"cellid":int(cell_id),"format":"json"},timeout=5)
                d=r.json()
                if "lat" in d:
                    res={"lat":float(d["lat"]),"lng":float(d["lon"]),"range":d.get("range",300),"source":"OpenCelliD [Live]","found":True}
                    st.session_state["tower_cache"][key]=res; return res
            except: pass
    try:
        r=requests.post("https://location.services.mozilla.com/v1/geolocate?key=test",
            json={"cellTowers":[{"radioType":radio.lower(),"mobileCountryCode":int(mcc),"mobileNetworkCode":int(mnc),"locationAreaCode":int(lac),"cellId":int(cell_id)}]},timeout=5)
        d=r.json()
        if "location" in d:
            res={"lat":d["location"]["lat"],"lng":d["location"]["lng"],"range":d.get("accuracy",800),"source":"Mozilla Location [Live]","found":True}
            st.session_state["tower_cache"][key]=res; return res
    except: pass
    center=MCC_CENTERS.get(str(mcc),{"lat":20.0,"lng":77.0})
    seed=int(hashlib.md5(f"{mcc}{mnc}{lac}{cell_id}".encode()).hexdigest(),16)
    rng=random.Random(seed)
    res={"lat":round(center["lat"]+rng.uniform(-0.5,0.5),5),"lng":round(center["lng"]+rng.uniform(-1.0,1.0),5),"range":2000,"source":"Estimated [Fallback]","found":False}
    st.session_state["tower_cache"][key]=res; return res

def decode_plmn(plmn_str):
    plmn=re.sub(r'\D','',str(plmn_str))
    if len(plmn)>=5: return plmn[:3],plmn[3:]
    return None,None

def navigate_to(page_name):
    for opt in NAV_OPTIONS:
        if page_name.lower() in opt.lower():
            st.session_state["main_nav"] = opt
            st.session_state["_main_nav_radio"] = opt
            break

def get_contacts():
    return st.session_state.get("contact_book", {})

def contact_name(number):
    book = get_contacts()
    n = str(number).strip()
    return book.get(n, n)

def set_contact(number, name):
    if "contact_book" not in st.session_state:
        st.session_state["contact_book"] = {}
    st.session_state["contact_book"][str(number).strip()] = name.strip()

def delete_contact(number):
    book = st.session_state.get("contact_book", {})
    book.pop(str(number).strip(), None)
    st.session_state["contact_book"] = book

def _avatar_gradient(num_or_name):
    idx = int(hashlib.md5(str(num_or_name).encode()).hexdigest(), 16) % len(AVATAR_GRADIENTS)
    return AVATAR_GRADIENTS[idx]

# ─────────────────────────────────────────────
#  BILL PDF PARSER  v4 (unchanged)
# ─────────────────────────────────────────────
def _normalize_phone(num_str):
    n = re.sub(r'[\s\-\.\(\)]','',str(num_str).strip())
    if re.match(r'^\+91\d{10}$',n): return n
    if re.match(r'^91\d{10}$',n):   return '+91'+n[2:]
    if re.match(r'^0\d{10}$',n):    return '+91'+n[1:]
    if re.match(r'^[6-9]\d{9}$',n): return '+91'+n
    if re.match(r'^\+\d{7,15}$',n): return n
    if re.match(r'^[X0\*]{4,}\d{3,}$',n,re.I): return n
    return n if len(re.sub(r'\D','',n))>=7 else ''

def _parse_duration_to_sec(dur_str):
    s = str(dur_str).strip()
    if not s or s in ('-','—','N/A','n/a'): return 0
    m = re.match(r'^(\d+)[:\.](\d{2})[:\.](\d{2})$', s)
    if m: return int(m.group(1))*3600 + int(m.group(2))*60 + int(m.group(3))
    m = re.match(r'^(\d{1,3})[:\.](\d{2})$', s)
    if m:
        a,b = int(m.group(1)), int(m.group(2))
        if b < 60:  return a*60 + b
    m = re.match(r'^(\d+)\s*m(?:in)?\s*(\d+)\s*s(?:ec)?$', s, re.I)
    if m: return int(m.group(1))*60 + int(m.group(2))
    m = re.match(r'^(\d+)\s*m(?:in)?s?$', s, re.I)
    if m: return int(m.group(1))*60
    m = re.match(r'^(\d+)\s*s(?:ec)?s?$', s, re.I)
    if m: return int(m.group(1))
    m = re.match(r'^(\d+)$', s)
    if m:
        v = int(m.group(1))
        return v if v <= 86400 else 0
    return 0

def _parse_datetime(date_str, time_str):
    date_str = re.sub(r'[-\.]', '/', date_str.strip())
    time_str = re.sub(r'\.', ':', time_str.strip())
    fmts = [
        "%d/%m/%Y %H:%M:%S","%d/%m/%y %H:%M:%S","%Y/%m/%d %H:%M:%S",
        "%d/%m/%Y %H:%M","%d/%m/%y %H:%M","%Y/%m/%d %H:%M",
        "%d/%b/%Y %H:%M:%S","%d/%b/%y %H:%M:%S","%d/%b/%Y %H:%M","%d/%b/%y %H:%M",
        "%m/%d/%Y %H:%M:%S","%m/%d/%y %H:%M:%S","%m/%d/%Y %H:%M","%m/%d/%y %H:%M",
        "%d/%m/%Y %I:%M:%S %p","%d/%m/%y %I:%M %p","%Y/%m/%d %I:%M:%S %p","%Y/%m/%d %I:%M %p",
    ]
    combined = f"{date_str} {time_str}".strip()
    for fmt in fmts:
        try: return datetime.strptime(combined, fmt)
        except: pass
    return None

def _detect_operator(text):
    t = text[:3000].lower()
    if 'airtel' in t:   return 'airtel'
    if 'jio' in t:      return 'jio'
    if 'vodafone' in t: return 'vodafone'
    if 'idea' in t or ' vi ' in t: return 'idea'
    if 'bsnl' in t:     return 'bsnl'
    return 'unknown'

def _detect_call_type(type_str, ctx='', duration_sec=0):
    if duration_sec > 0:
        t = (str(type_str)+' '+str(ctx)).lower()
        if any(k in t for k in ['in','mt','received','incoming','terminated']):
            return 'MT_VOICE'
        return 'MO_VOICE'
    t = (str(type_str)+' '+str(ctx)).lower()
    if any(k in t for k in ['sms','message','text','msg']):
        if any(k in t for k in ['out','mo','sent','originated']): return 'MO_SMS'
        return 'MT_SMS'
    if any(k in t for k in ['data','gprs','internet','3g','4g','lte']):
        return 'MO_DATA'
    if any(k in t for k in ['out','mo','made','dialed','originated','local out','std out','isd out','roam out']):
        return 'MO_VOICE'
    if any(k in t for k in ['in','mt','received','incoming','terminated','local in','std in']):
        return 'MT_VOICE'
    return 'MO_VOICE'

def _parse_generic_robust(lines):
    records = []
    seen_keys = set()
    INDIA_P = re.compile(
        r'(\d{1,2}[-/][A-Za-z]{3}[-/]\d{2,4})'
        r'\s+'
        r'(\d{2}:\d{2}:\d{2})'
        r'\s+'
        r'(\d{10,13})'
        r'\s+'
        r'(\d{1,6})'
        r'(?:\s+\d{1,6})?'
        r'(?:\s+[\d.]+)?',
        re.IGNORECASE
    )
    p0_count = 0
    for line in lines:
        if len(line.strip()) < 10: continue
        lw = line.lower()
        if any(k in lw for k in ['subtotal','grand total','voice total','usage total']): continue
        if sum(1 for k in ['date','time','number','usage','amount','billed','free','chargeable'] if k in lw) >= 4:
            if not re.search(r'\d{2}:\d{2}:\d{2}', line): continue
        m = INDIA_P.search(line)
        if not m: continue
        date_s, time_s, phone_s, dur_s = m.group(1), m.group(2), m.group(3), m.group(4)
        ts = _parse_datetime(date_s, time_s)
        if not ts: continue
        phone = _normalize_phone(phone_s)
        if not phone: continue
        dur = int(dur_s)
        if dur > 86400: dur = 0
        key = f"{ts.strftime('%Y%m%d%H%M%S')}_{phone}"
        if key in seen_keys: continue
        seen_keys.add(key)
        ct = _detect_call_type('', line, dur)
        records.append({'timestamp':ts,'called_number':phone,'call_type':ct,'duration_sec':dur,'raw_line':line.strip()[:120]})
        p0_count += 1
    if p0_count > 0:
        return records
    HEADER_KW = ['date','time','number','duration','called','type','call','usage']
    header_idx = None
    for i,line in enumerate(lines[:80]):
        lw = line.lower()
        if sum(1 for k in HEADER_KW if k in lw) >= 2:
            header_idx = i; break
    if header_idx is not None:
        hline = lines[header_idx].lower()
        def col_of(k):
            p = hline.find(k)
            return p if p >= 0 else None
        date_c = col_of('date') or 0
        time_c = col_of('time') or (date_c+12)
        num_c  = col_of('number') or col_of('called') or (time_c+10)
        type_c = col_of('type') or col_of('call') or (num_c+15)
        dur_c  = col_of('duration') or (type_c+20)
        for line in lines[header_idx+1:]:
            if len(line.strip()) < 8: continue
            if any(k in line.lower() for k in ['total','subtotal','---','===','page','summary']): continue
            try:
                def ex(l,s,w=18): return l[s:s+w].strip() if len(l)>s else ''
                d_s=ex(line,date_c,12); t_s=ex(line,time_c,10)
                n_s=ex(line,num_c,15);  ty_s=ex(line,type_c,22); du_s=ex(line,dur_c,12)
                if not re.search(r'\d{1,4}[/\-\.]\d{1,2}[/\-\.]\d{1,4}',d_s): continue
                if not re.search(r'\d{1,2}[:.]\d{2}',t_s): continue
                ts=_parse_datetime(d_s,t_s)
                if not ts: continue
                num_clean=re.sub(r'[\s\-]','',n_s)
                if len(re.sub(r'\D','',num_clean))<5: continue
                dur=_parse_duration_to_sec(du_s)
                ct=_detect_call_type(ty_s,line,dur)
                phone=_normalize_phone(num_clean)
                if not phone: continue
                records.append({'timestamp':ts,'called_number':phone,'call_type':ct,'duration_sec':dur,'raw_line':line.strip()[:100]})
            except: continue
    DATE_P = r'(\d{1,2}[/\-\.]\d{1,2}[/\-\.]\d{2,4}|\d{4}[/\-\.]\d{2}[/\-\.]\d{2}|\d{1,2}[/\-\.][A-Za-z]{3}[/\-\.]\d{2,4})'
    TIME_P = r'(\d{1,2}[:.]\d{2}(?:[:.]\d{2})?(?:\s*[AaPp][Mm])?)'
    NUM_P  = r'(\+?91\d{10}|0\d{10}|[6-9]\d{9}|\+\d{9,14}|[X0\*]{4,}\d{3,})'
    for line in lines:
        if len(line.strip()) < 15: continue
        if any(k in line.lower() for k in ['total','subtotal','grand total','page ','---','===']): continue
        dm = re.search(DATE_P, line, re.I)
        if not dm: continue
        rest = line[dm.end():]
        tm = re.search(TIME_P, rest)
        if not tm: continue
        rest2 = rest[tm.end():]
        nm = re.search(NUM_P, rest2)
        if not nm:
            nm = re.search(r'(\d{10,13})', rest2)
        if not nm: continue
        num_clean = re.sub(r'[\s\-]','',nm.group(1))
        phone = _normalize_phone(num_clean)
        if not phone: continue
        rest3 = rest2[nm.end():]
        dur = 0
        dm2 = re.search(r'\b(\d{1,3}[:.]\d{2}[:.]\d{2})\b', rest3)
        if not dm2:
            dm2 = re.search(r'\b(\d{1,3}[:.]\d{2})\b', rest3)
        if dm2:
            dur = _parse_duration_to_sec(dm2.group(1))
        else:
            rest3_clean = re.sub(r'\b\d+\.\d+\b', '', rest3)
            nm3 = re.search(r'\b(\d{2,5})\b', rest3_clean)
            if nm3:
                v = int(nm3.group(1))
                dur = v if v <= 86400 else 0
        ts = _parse_datetime(dm.group(1), tm.group(1))
        if not ts: continue
        key = f"{ts.strftime('%Y%m%d%H%M%S')}_{phone}"
        if key in seen_keys: continue
        seen_keys.add(key)
        ct = _detect_call_type('', line, dur)
        records.append({'timestamp':ts,'called_number':phone,'call_type':ct,'duration_sec':dur,'raw_line':line.strip()[:100]})
    return records

def parse_pdf_bill(uploaded_file):
    text_pages=[]
    try:
        import pdfplumber
        uploaded_file.seek(0)
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                t=page.extract_text()
                if t: text_pages.append(t)
    except ImportError: pass
    except Exception: pass
    if not text_pages:
        try:
            import PyPDF2
            uploaded_file.seek(0)
            reader=PyPDF2.PdfReader(uploaded_file)
            text_pages=[p.extract_text() or '' for p in reader.pages]
        except: pass
    if not text_pages: return pd.DataFrame(),'',{'operator':'unknown','total_lines':0,'strategy':'no-text','final_records':0}
    full_text = "\n".join(text_pages)
    lines = full_text.split('\n')
    operator = _detect_operator(full_text)
    diag = {'operator':operator,'total_lines':len(lines),'strategy':'generic-robust-v4'}
    records = _parse_generic_robust(lines)
    diag['raw_matches'] = len(records)
    if not records:
        diag['final_records'] = 0
        return pd.DataFrame(), full_text, diag
    df = pd.DataFrame(records)
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df = df.dropna(subset=['timestamp'])
    df['duration_sec'] = pd.to_numeric(df['duration_sec'],errors='coerce').fillna(0).astype(int).clip(lower=0)
    df = df.sort_values('timestamp').drop_duplicates(subset=['timestamp','called_number']).reset_index(drop=True)
    df['call_id'] = [f'BILL{str(i+1).zfill(5)}' for i in range(len(df))]
    diag['final_records'] = len(df)
    diag['date_range'] = f"{df['timestamp'].min().date()} to {df['timestamp'].max().date()}" if len(df)>0 else 'N/A'
    diag['voice_count'] = int(df['call_type'].str.contains('VOICE',na=False).sum())
    diag['sms_count']   = int(df['call_type'].str.contains('SMS',na=False).sum())
    diag['total_dur']   = int(df['duration_sec'].sum())
    diag['types']       = df['call_type'].value_counts().to_dict()
    return df.reset_index(drop=True), full_text, diag

# ─────────────────────────────────────────────
#  REDESIGNED CSS — Cyber Intelligence Theme
# ─────────────────────────────────────────────
def inject_css():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@400;500;600;700&family=Exo+2:wght@300;400;500;600;700;800&display=swap');

:root {
  --bg:        #030508;
  --bg2:       #060C12;
  --bg3:       #0A1420;
  --bg4:       #0F1D2E;
  --panel:     #081018;
  --border:    rgba(0,255,179,0.08);
  --border2:   rgba(0,255,179,0.15);
  --border3:   rgba(0,255,179,0.25);
  --green:     #00FFB3;
  --green2:    #00CC8F;
  --cyan:      #00B8FF;
  --violet:    #7B61FF;
  --amber:     #FFD700;
  --red:       #FF3366;
  --orange:    #FF6B35;
  --t1:        #E8F0F8;
  --t2:        #7A95B0;
  --t3:        #3A5570;
  --t4:        #1E3348;
  --mono:      'Share Tech Mono', monospace;
  --display:   'Exo 2', sans-serif;
  --body:      'Rajdhani', sans-serif;
  --r1:        4px;
  --r2:        8px;
  --r3:        12px;
}

/* ── Reset & Base ── */
* { box-sizing: border-box; }
.stApp { background: var(--bg) !important; color: var(--t1); font-family: var(--body); }
#MainMenu, footer, header, .stDeployButton { display: none !important; }
.main .block-container { padding: 1.5rem 2rem 5rem; max-width: 1600px; }

/* ── Scrollbars ── */
::-webkit-scrollbar { width: 3px; height: 3px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--green2); border-radius: 2px; opacity: 0.4; }

/* ── Matrix animated background ── */
.stApp::before {
  content: '';
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background:
    radial-gradient(ellipse at 20% 50%, rgba(0,255,179,0.025) 0%, transparent 60%),
    radial-gradient(ellipse at 80% 20%, rgba(0,184,255,0.02) 0%, transparent 50%),
    radial-gradient(ellipse at 60% 80%, rgba(123,97,255,0.015) 0%, transparent 50%);
  pointer-events: none;
  z-index: 0;
}

/* Scanline effect */
.stApp::after {
  content: '';
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: repeating-linear-gradient(
    0deg,
    transparent,
    transparent 2px,
    rgba(0,255,179,0.006) 2px,
    rgba(0,255,179,0.006) 4px
  );
  pointer-events: none;
  z-index: 0;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
  background: var(--bg2) !important;
  border-right: 1px solid var(--border2) !important;
}
[data-testid="stSidebar"]::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 200px;
  background: linear-gradient(180deg, rgba(0,255,179,0.04) 0%, transparent 100%);
  pointer-events: none;
}

/* ── Hide Streamlit sidebar completely ── */
[data-testid="stSidebar"] {
  display: none !important;
}

[data-testid="collapsedControl"] {
  display: none !important;
}

[data-testid="stSidebarCollapseButton"] { 
  display: none !important; 
}

button[kind="header"] { 
  display: none !important; 
}

/* ── Typography ── */
h1,h2,h3,h4 {
  font-family: var(--display) !important;
  font-weight: 700 !important;
  letter-spacing: -0.01em;
  color: var(--t1) !important;
}

/* ── Sidebar Radio Navigation ── */
[data-testid="stSidebar"] .stRadio > div { gap: 2px; }
[data-testid="stSidebar"] .stRadio label {
  background: transparent !important;
  border: 1px solid transparent !important;
  border-radius: var(--r2) !important;
  padding: 8px 10px !important;
  cursor: pointer !important;
  transition: all 0.15s ease;
  margin: 1px 0;
}
[data-testid="stSidebar"] .stRadio label:hover {
  background: rgba(0,255,179,0.04) !important;
  border-color: var(--border) !important;
}
[data-testid="stSidebar"] .stRadio div[role="radio"] > div:first-child { display: none !important; }
[data-testid="stSidebar"] .stRadio div[role="radio"][aria-checked="true"] label {
  background: rgba(0,255,179,0.06) !important;
  border-color: var(--border2) !important;
}
[data-testid="stSidebar"] .stRadio div[role="radio"][aria-checked="true"] [data-testid="stMarkdownContainer"] {
  color: var(--green) !important;
}
[data-testid="stSidebar"] .stRadio label [data-testid="stMarkdownContainer"] {
  font-family: var(--body) !important;
  font-size: 0.82rem !important;
  font-weight: 500 !important;
  color: var(--t2) !important;
  letter-spacing: 0.03em;
}

/* ── Page Header ── */
.ph {
  padding: 24px 0 20px;
  border-bottom: 1px solid var(--border);
  margin-bottom: 28px;
  position: relative;
}
.ph::after {
  content: '';
  position: absolute;
  bottom: -1px; left: 0;
  width: 80px; height: 1px;
  background: var(--green);
}
.ph-eyebrow {
  font-family: var(--mono);
  font-size: 0.6rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--green);
  margin-bottom: 8px;
}
.ph-title {
  font-family: var(--display);
  font-size: 1.8rem;
  font-weight: 800;
  color: var(--t1);
  letter-spacing: -0.02em;
  margin-bottom: 6px;
  line-height: 1;
}
.ph-sub {
  font-family: var(--body);
  color: var(--t2);
  font-size: 0.85rem;
  line-height: 1.5;
}
.sh {
  font-family: var(--mono);
  font-size: 0.6rem;
  font-weight: 400;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--green);
  padding-bottom: 10px;
  border-bottom: 1px solid var(--border);
  margin-bottom: 14px;
  margin-top: 8px;
}

/* ── KPI Cards ── */
.kpi {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: var(--r2);
  padding: 16px 18px;
  position: relative;
  overflow: hidden;
  height: 100%;
}
.kpi::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--green), transparent);
  opacity: 0.3;
}
.kpi-label {
  font-family: var(--mono);
  font-size: 0.6rem;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--t3);
  margin-bottom: 10px;
}
.kpi-value {
  font-family: var(--display);
  font-size: 1.7rem;
  font-weight: 700;
  color: var(--t1);
  letter-spacing: -0.02em;
  line-height: 1;
}
.kpi-sub { font-family: var(--mono); font-size: 0.7rem; color: var(--t3); margin-top: 6px; }
.kpi.green .kpi-value { color: var(--green); }
.kpi.cyan  .kpi-value { color: var(--cyan); }
.kpi.amber .kpi-value { color: var(--amber); }
.kpi.red   .kpi-value { color: var(--red); }
.kpi.violet .kpi-value { color: var(--violet); }

/* ── Buttons ── */
.stButton > button {
  background: transparent !important;
  color: var(--green) !important;
  border: 1px solid var(--border2) !important;
  font-family: var(--mono) !important;
  font-size: 0.72rem !important;
  letter-spacing: 0.1em !important;
  text-transform: uppercase !important;
  border-radius: var(--r1) !important;
  padding: 0.5rem 1.2rem !important;
  transition: all 0.2s ease !important;
  position: relative !important;
}
.stButton > button:hover {
  background: rgba(0,255,179,0.06) !important;
  border-color: var(--green) !important;
  box-shadow: 0 0 20px rgba(0,255,179,0.1) !important;
}
.stDownloadButton > button {
  background: transparent !important;
  color: var(--cyan) !important;
  border: 1px solid rgba(0,184,255,0.25) !important;
  font-family: var(--mono) !important;
  font-size: 0.72rem !important;
  letter-spacing: 0.1em !important;
  border-radius: var(--r1) !important;
}
.stDownloadButton > button:hover {
  background: rgba(0,184,255,0.06) !important;
  border-color: var(--cyan) !important;
}

/* ── Inputs ── */
.stTextInput > div > div > input,
.stNumberInput > div > div > input {
  background: var(--bg3) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--r1) !important;
  color: var(--t1) !important;
  font-family: var(--mono) !important;
  font-size: 0.82rem !important;
  padding: 0.5rem 0.75rem !important;
  transition: border-color 0.2s;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
  border-color: var(--border3) !important;
  box-shadow: 0 0 12px rgba(0,255,179,0.08) !important;
}
.stSelectbox > div > div {
  background: var(--bg3) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--r1) !important;
  color: var(--t1) !important;
  font-family: var(--mono) !important;
  font-size: 0.82rem !important;
}
textarea {
  background: var(--bg3) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--r1) !important;
  color: var(--t1) !important;
  font-family: var(--mono) !important;
  font-size: 0.78rem !important;
}
[data-testid="stFileUploader"] > div {
  background: var(--bg2) !important;
  border: 1px dashed var(--border2) !important;
  border-radius: var(--r2) !important;
  padding: 28px !important;
}

/* ── Labels ── */
.stTextInput label, .stNumberInput label, .stSelectbox label,
.stTextArea label, .stDateInput label, .stTimeInput label,
.stCheckbox label, [data-testid="stWidgetLabel"] {
  font-family: var(--mono) !important;
  font-size: 0.62rem !important;
  letter-spacing: 0.12em !important;
  text-transform: uppercase !important;
  color: var(--t3) !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
  background: transparent !important;
  gap: 0 !important;
  border-bottom: 1px solid var(--border) !important;
  padding-bottom: 0 !important;
  margin-bottom: 24px !important;
  border-radius: 0 !important;
  border-top: none !important;
  border-left: none !important;
  border-right: none !important;
}
.stTabs [data-baseweb="tab"] {
  font-family: var(--mono) !important;
  font-size: 0.65rem !important;
  letter-spacing: 0.12em !important;
  text-transform: uppercase !important;
  color: var(--t3) !important;
  padding: 10px 20px !important;
  border-radius: 0 !important;
  background: transparent !important;
  border: none !important;
}
.stTabs [aria-selected="true"] {
  color: var(--green) !important;
  border-bottom: 1px solid var(--green) !important;
  background: transparent !important;
}
[data-testid="stExpander"] {
  border: 1px solid var(--border) !important;
  border-radius: var(--r2) !important;
  background: var(--bg2) !important;
}
.streamlit-expanderHeader {
  font-family: var(--mono) !important;
  font-size: 0.72rem !important;
  color: var(--t2) !important;
  letter-spacing: 0.08em !important;
}

/* ── Alert / Info boxes ── */
.abox {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-left: 2px solid;
  border-radius: 0 var(--r2) var(--r2) 0;
  padding: 12px 16px;
  margin: 10px 0;
  font-family: var(--mono);
  font-size: 0.75rem;
  line-height: 1.6;
  color: var(--t2);
}
.abox-green { border-left-color: var(--green); }
.abox-cyan  { border-left-color: var(--cyan); }
.abox-amber { border-left-color: var(--amber); }
.abox-red   { border-left-color: var(--red); }

/* ── Badges ── */
.bd {
  display: inline-flex;
  align-items: center;
  padding: 2px 8px;
  border-radius: 2px;
  font-family: var(--mono);
  font-size: 0.62rem;
  letter-spacing: 0.08em;
  background: var(--bg3);
  color: var(--t2);
  border: 1px solid var(--border);
}
.bd-g { color: var(--green); border-color: rgba(0,255,179,0.2); background: rgba(0,255,179,0.05); }
.bd-c { color: var(--cyan);  border-color: rgba(0,184,255,0.2); background: rgba(0,184,255,0.05); }
.bd-a { color: var(--amber); border-color: rgba(255,215,0,0.2);  background: rgba(255,215,0,0.05); }
.bd-r { color: var(--red);   border-color: rgba(255,51,102,0.2); background: rgba(255,51,102,0.05); }
.bd-v { color: var(--violet);border-color: rgba(123,97,255,0.2); background: rgba(123,97,255,0.05); }

/* ── Data table ── */
table.dt { width: 100%; border-collapse: collapse; font-size: 0.8rem; }
table.dt td {
  padding: 9px 0;
  border-bottom: 1px solid var(--border);
  color: var(--t2);
  font-family: var(--body);
}
table.dt th {
  padding: 9px 0;
  border-bottom: 1px solid var(--border);
  font-family: var(--mono);
  font-size: 0.58rem;
  color: var(--t3);
  font-weight: 400;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  text-align: left;
}
table.dt tr:last-child td { border-bottom: none; }
table.dt td:last-child { font-family: var(--mono); color: var(--t1); font-size: 0.78rem; }

/* ── Cards ── */
.panel {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: var(--r2);
  padding: 20px 22px;
  margin-bottom: 14px;
  position: relative;
  overflow: hidden;
}
.panel-title {
  font-family: var(--mono);
  font-size: 0.6rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--green);
  margin-bottom: 16px;
  padding-bottom: 10px;
  border-bottom: 1px solid var(--border);
}

/* ── Call cards ── */
.call-card {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: var(--r2);
  padding: 12px 16px;
  margin-bottom: 8px;
  transition: border-color 0.15s;
}
.call-card:hover { border-color: var(--border2); }

/* ── Record rows ── */
.rec-row {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 0;
  border-bottom: 1px solid var(--border);
  font-size: 0.78rem;
}
.rec-row:last-child { border-bottom: none; }
.rec-time { font-family: var(--mono); color: var(--t3); min-width: 130px; font-size: 0.7rem; }
.rec-num  { font-family: var(--mono); color: var(--t1); flex: 1; }
.rec-dur  { font-family: var(--mono); color: var(--amber); min-width: 75px; text-align: right; }
.rec-type { min-width: 85px; }

/* ── Stat pills ── */
.stat-pill {
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: var(--r2);
  padding: 12px 16px;
  min-width: 100px;
}
.stat-pill .sp-val { font-family: var(--display); font-size: 1.3rem; font-weight: 700; color: var(--t1); }
.stat-pill .sp-lbl { font-family: var(--mono); font-size: 0.55rem; color: var(--t3); text-transform: uppercase; letter-spacing: 1.5px; margin-top: 4px; }

/* ── Contact Manager ── */
.cm-card {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: var(--r2);
  padding: 0;
  margin-bottom: 10px;
  overflow: hidden;
  transition: border-color 0.2s;
}
.cm-card:hover { border-color: var(--border2); }
.cm-card-accent { height: 2px; width: 100%; }
.cm-card-body { padding: 14px 16px 12px; display: flex; align-items: center; gap: 12px; }
.cm-avatar {
  width: 42px; height: 42px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-family: var(--display); font-size: 0.9rem; font-weight: 700; color: #fff;
  flex-shrink: 0;
}
.cm-info { flex: 1; min-width: 0; }
.cm-name {
  font-family: var(--display);
  font-weight: 600; font-size: 0.9rem; color: var(--t1);
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis; margin-bottom: 2px;
}
.cm-number { font-family: var(--mono); font-size: 0.68rem; color: var(--t3); margin-bottom: 5px; }
.cm-meta { display: flex; gap: 6px; flex-wrap: wrap; }
.cm-chip {
  display: inline-flex; align-items: center; gap: 3px;
  background: var(--bg3); border: 1px solid var(--border);
  border-radius: 2px; padding: 1px 6px;
  font-family: var(--mono); font-size: 0.6rem; color: var(--t3);
}
.cm-chip.g { background: rgba(0,255,179,0.05); border-color: rgba(0,255,179,0.15); color: var(--green); }
.cm-chip.c { background: rgba(0,184,255,0.05); border-color: rgba(0,184,255,0.15); color: var(--cyan); }
.cm-chip.a { background: rgba(255,215,0,0.05);  border-color: rgba(255,215,0,0.15);  color: var(--amber); }
.cm-chip.r { background: rgba(255,51,102,0.05); border-color: rgba(255,51,102,0.15); color: var(--red); }

.cm-stats-bar { display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 20px; }
.cm-stat {
  background: var(--bg2); border: 1px solid var(--border);
  border-radius: var(--r2); padding: 12px 16px;
  display: flex; align-items: center; gap: 10px; flex: 1; min-width: 110px;
}
.cm-stat-val { font-family: var(--display); font-size: 1.1rem; font-weight: 700; color: var(--t1); }
.cm-stat-lbl { font-family: var(--mono); font-size: 0.55rem; color: var(--t3); text-transform: uppercase; letter-spacing: 1px; margin-top: 1px; }

.cm-add-panel {
  background: rgba(0,255,179,0.02);
  border: 1px solid var(--border2);
  border-radius: var(--r2);
  padding: 20px 22px 16px;
  margin-bottom: 22px;
}
.cm-add-title {
  font-family: var(--mono);
  font-size: 0.58rem; letter-spacing: 0.2em; text-transform: uppercase;
  color: var(--green); font-weight: 400; margin-bottom: 14px;
}
.cm-empty {
  text-align: center; padding: 60px 20px;
  border: 1px dashed var(--border); border-radius: var(--r2);
}
.cm-empty-title { font-family: var(--display); font-size: 0.9rem; font-weight: 600; color: var(--t2); margin-bottom: 6px; }
.cm-empty-sub { font-family: var(--body); font-size: 0.8rem; color: var(--t3); }
.cm-section-label {
  font-family: var(--mono); font-size: 0.58rem; letter-spacing: 0.18em; text-transform: uppercase;
  color: var(--t3); font-weight: 400; margin-bottom: 12px; margin-top: 4px;
  display: flex; align-items: center; gap: 10px;
}
.cm-section-label::after { content: ''; flex: 1; height: 1px; background: var(--border); }

/* ── Anomaly cards ── */
.anomaly-card {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-left: 2px solid;
  border-radius: 0 var(--r2) var(--r2) 0;
  padding: 14px 18px;
  margin-bottom: 8px;
}

/* ── Terminal style section headers ── */
.term-line {
  font-family: var(--mono);
  font-size: 0.72rem;
  color: var(--t3);
  margin-bottom: 8px;
}
.term-line::before { content: '> '; color: var(--green); }

/* ── Divider ── */
hr {
  border: none !important;
  border-top: 1px solid var(--border) !important;
  margin: 20px 0 !important;
}

/* ── Streamlit dataframe ── */
[data-testid="stDataFrame"] { border: 1px solid var(--border) !important; border-radius: var(--r2) !important; }

/* ── Responsive ── */
@media (max-width: 768px) {
  .main .block-container { padding: 0.75rem 0.75rem 5rem; }
  .ph-title { font-size: 1.3rem; }
  .kpi-value { font-size: 1.2rem; }
  [data-testid="stSidebar"] { width: 85vw !important; max-width: 280px; }
}
@media (max-width: 480px) {
  .ph-title { font-size: 1.1rem; }
  .stat-pill { min-width: 80px; padding: 10px 12px; }
}

/* ── Matrix rain animation ── */
@keyframes matrixRain {
  0%   { opacity: 0; transform: translateY(-20px); }
  10%  { opacity: 1; }
  90%  { opacity: 0.3; }
  100% { opacity: 0; transform: translateY(100vh); }
}
</style>
""", unsafe_allow_html=True)


def inject_sidebar_toggle_js():
    st.markdown("""
<script>
(function() {
  // Prevent sidebar from ever being hidden
  function fixSidebar() {
    // Get the sidebar
    const sidebar = document.querySelector('[data-testid="stSidebar"]');
    if (sidebar) {
      // Force it to always be visible
      sidebar.style.display = 'block';
      sidebar.style.visibility = 'visible';
      sidebar.style.opacity = '1';
      sidebar.removeAttribute('aria-hidden');
    }
    
    // Get the collapse button
    const collapseBtn = document.querySelector('[data-testid="collapsedControl"]');
    if (collapseBtn) {
      // Make it visible and clickable
      collapseBtn.style.display = 'flex';
      collapseBtn.style.visibility = 'visible';
      collapseBtn.style.opacity = '1';
      collapseBtn.style.pointerEvents = 'auto';
      collapseBtn.style.position = 'fixed';
      collapseBtn.style.top = '12px';
      collapseBtn.style.left = '12px';
      collapseBtn.style.zIndex = '99999';
    }
  }
  
  // Run immediately
  fixSidebar();
  
  // Watch for changes
  const observer = new MutationObserver(fixSidebar);
  observer.observe(document.body, { 
    childList: true, 
    subtree: true, 
    attributes: true
  });
  
  // Also check every 200ms
  setInterval(fixSidebar, 200);
})();
</script>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  DATA HELPERS (unchanged)
# ─────────────────────────────────────────────
def get_combined_df():
    frames=[]
    manual=st.session_state.get("records",[])
    if manual:
        df_m=pd.DataFrame(manual)
        df_m["timestamp"]=pd.to_datetime(df_m["timestamp"],errors="coerce")
        df_m["duration_sec"]=pd.to_numeric(df_m["duration_sec"],errors="coerce").fillna(0)
        frames.append(df_m)
    bill=st.session_state.get("bill_records",pd.DataFrame())
    if isinstance(bill,pd.DataFrame) and not bill.empty:
        df_b=bill.copy()
        df_b["timestamp"]=pd.to_datetime(df_b["timestamp"],errors="coerce")
        df_b["duration_sec"]=pd.to_numeric(df_b["duration_sec"],errors="coerce").fillna(0)
        for col,default in [("caller","Unknown"),("mcc","N/A"),("mnc","N/A"),("lac",0),("cell_id",0),
                             ("call_type","MO_VOICE"),("latitude",None),("longitude",None),("tower_source","Bill PDF")]:
            if col not in df_b.columns: df_b[col]=default
        if "callee" not in df_b.columns and "called_number" in df_b.columns:
            df_b["callee"]=df_b["called_number"]
        frames.append(df_b)
    if not frames: return pd.DataFrame()
    df=pd.concat(frames,ignore_index=True)
    df=df.dropna(subset=["timestamp"]).sort_values("timestamp").reset_index(drop=True)
    df["call_id"]=[f"REC{str(i+1).zfill(5)}" for i in range(len(df))]
    return df

def get_num_col(df):
    if "callee" in df.columns and df["callee"].notna().any(): return "callee"
    if "called_number" in df.columns: return "called_number"
    return None

def _dark_layout(**kwargs):
    base=dict(
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0,r=0,t=10,b=0),
        font=dict(family="Share Tech Mono", color="#3A5570", size=10),
        xaxis=dict(gridcolor="rgba(0,255,179,0.04)", linecolor="rgba(0,255,179,0.08)", tickfont=dict(color="#3A5570")),
        yaxis=dict(gridcolor="rgba(0,255,179,0.04)", linecolor="rgba(0,255,179,0.08)", tickfont=dict(color="#3A5570"))
    )
    base.update(kwargs)
    return base


# ─────────────────────────────────────────────
#  PAGE: DEVICE SELECTION
# ─────────────────────────────────────────────
def page_device_select():
    st.markdown("""
<div style="text-align:center;padding:56px 0 48px;position:relative">
  <div style="font-family:'Share Tech Mono',monospace;font-size:0.6rem;color:rgba(0,255,179,0.5);letter-spacing:0.25em;text-transform:uppercase;margin-bottom:20px">
    // CDR-FORENSICS-PRO :: SESSION INIT
  </div>
  <div style="font-family:'Exo 2',sans-serif;font-size:3rem;font-weight:800;line-height:0.95;color:#E8F0F8;margin-bottom:16px;letter-spacing:-0.03em">
    CDR<br><span style="color:#00FFB3">FORENSICS</span>
  </div>
  <div style="font-family:'Share Tech Mono',monospace;font-size:0.7rem;color:#3A5570;letter-spacing:0.1em;margin-bottom:8px">
    MULTIMEDIA & NETWORK FORENSICS INTELLIGENCE PLATFORM
  </div>
  <div style="font-family:'Rajdhani',sans-serif;color:#7A95B0;font-size:0.9rem;max-width:500px;margin:12px auto 0;line-height:1.7">
    Professional grade Call Detail Record analysis suite.<br>
    Configure session architecture to proceed.
  </div>
</div>
""", unsafe_allow_html=True)

    st.markdown('<div style="border-top:1px solid rgba(0,255,179,0.08);margin:0 0 32px"></div>', unsafe_allow_html=True)

    android_active = st.session_state.get("device_type") == "android"
    iphone_active  = st.session_state.get("device_type") == "iphone"

    c1, gap, c2 = st.columns([5, 1, 5])
    with c1:
        border_col = "rgba(0,255,179,0.4)" if android_active else "rgba(0,255,179,0.08)"
        bg_col = "rgba(0,255,179,0.04)" if android_active else "#060C12"
        sel_badge = '<div style="font-family:\'Share Tech Mono\',monospace;font-size:0.55rem;letter-spacing:0.18em;color:#00FFB3;border:1px solid rgba(0,255,179,0.3);padding:3px 10px;border-radius:2px;display:inline-block;margin-top:10px">ACTIVE SESSION</div>' if android_active else ''
        st.markdown(f"""
<div style="background:{bg_col};border:1px solid {border_col};border-radius:8px;padding:32px 24px;text-align:center">
  <div style="color:#00FFB3;margin-bottom:18px;opacity:{'1' if android_active else '0.6'}">{ANDROID_SVG}</div>
  <div style="font-family:'Exo 2',sans-serif;font-size:1.15rem;font-weight:700;color:#E8F0F8;margin-bottom:8px">ANDROID</div>
  <div style="font-family:'Rajdhani',sans-serif;font-size:0.82rem;color:#7A95B0;line-height:2;margin-bottom:16px">
    Identifier: <span style="color:#00FFB3;font-family:'Share Tech Mono',monospace">LAC</span> — Location Area Code<br>
    Protocols: GSM · UMTS · LTE · 5G NR<br>
    Diagnostic: <span style="font-family:'Share Tech Mono',monospace">*#*#4636#*#*</span><br>
    MCC/MNC displayed as separate fields
  </div>
  {sel_badge}
</div>""", unsafe_allow_html=True)
        st.button("Initialize Android Session", use_container_width=True, key="sel_android",
                  on_click=lambda y: st.session_state.update(device_type=y), args=("android",))

    with c2:
        border_col2 = "rgba(0,184,255,0.4)" if iphone_active else "rgba(0,255,179,0.08)"
        bg_col2 = "rgba(0,184,255,0.04)" if iphone_active else "#060C12"
        sel_badge2 = '<div style="font-family:\'Share Tech Mono\',monospace;font-size:0.55rem;letter-spacing:0.18em;color:#00B8FF;border:1px solid rgba(0,184,255,0.3);padding:3px 10px;border-radius:2px;display:inline-block;margin-top:10px">ACTIVE SESSION</div>' if iphone_active else ''
        st.markdown(f"""
<div style="background:{bg_col2};border:1px solid {border_col2};border-radius:8px;padding:32px 24px;text-align:center">
  <div style="color:#00B8FF;margin-bottom:18px;opacity:{'1' if iphone_active else '0.6'}">{APPLE_SVG}</div>
  <div style="font-family:'Exo 2',sans-serif;font-size:1.15rem;font-weight:700;color:#E8F0F8;margin-bottom:8px">iPHONE</div>
  <div style="font-family:'Rajdhani',sans-serif;font-size:0.82rem;color:#7A95B0;line-height:2;margin-bottom:16px">
    Identifier: <span style="color:#00B8FF;font-family:'Share Tech Mono',monospace">TAC</span> — Tracking Area Code<br>
    Protocols: LTE · 5G NR<br>
    Diagnostic: <span style="font-family:'Share Tech Mono',monospace">*3001#12345#*</span><br>
    PLMN = MCC(3 digits) + MNC(remaining)
  </div>
  {sel_badge2}
</div>""", unsafe_allow_html=True)
        st.button("Initialize iPhone Session", use_container_width=True, key="sel_iphone",
                  on_click=lambda: st.session_state.update(device_type="iphone"))

    if st.session_state.get("device_type"):
        dtype = st.session_state["device_type"]; is_and = dtype == "android"
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f'<div style="font-family:\'Share Tech Mono\',monospace;font-size:0.58rem;color:rgba(0,255,179,0.5);letter-spacing:0.2em;margin-bottom:14px">// SELECT MODULE</div>', unsafe_allow_html=True)
        n1, n2, n3 = st.columns(3)
        for col, icon, title, desc, page_key in [
            (n1, "◉", "TOWER DATA ENTRY", f"Input MCC · MNC · {'LAC' if is_and else 'TAC'} · Cell ID", "Tower Data Entry"),
            (n2, "◫", "BILL PDF UPLOAD", "Automated extraction from operator bills", "Upload Bill PDF"),
            (n3, "▦", "FORENSIC DASHBOARD", "Unified intelligence overview", "Dashboard"),
        ]:
            with col:
                st.markdown(f"""
<div style="background:#060C12;border:1px solid rgba(0,255,179,0.08);border-radius:8px;padding:18px 16px;margin-bottom:8px">
  <div style="font-family:'Exo 2',sans-serif;font-size:1.2rem;font-weight:300;color:rgba(0,255,179,0.4);margin-bottom:8px">{icon}</div>
  <div style="font-family:'Share Tech Mono',monospace;font-size:0.65rem;letter-spacing:0.1em;color:#E8F0F8;margin-bottom:6px">{title}</div>
  <div style="font-family:'Rajdhani',sans-serif;font-size:0.78rem;color:#3A5570">{desc}</div>
</div>""", unsafe_allow_html=True)
                st.button(f"Open {title.title().split()[0]}", use_container_width=True, key=f"go_{page_key[:4].lower()}",
                          on_click=navigate_to, args=(page_key,))


# ─────────────────────────────────────────────
#  PAGE: TOWER DATA ENTRY
# ─────────────────────────────────────────────
def page_tower_entry():
    dtype = st.session_state.get("device_type", "android"); is_android = dtype == "android"
    lac_label = "LAC" if is_android else "TAC"
    st.markdown(f'<div class="ph"><div class="ph-eyebrow">// {"ANDROID" if is_android else "iPHONE"} ACQUISITION MODE</div><div class="ph-title">Tower Network Entry</div><div class="ph-sub">Input cellular network identifiers to triangulate subscriber location via tower databases</div></div>', unsafe_allow_html=True)

    if not is_android:
        st.markdown(f'<div class="abox abox-cyan"><span style="color:var(--cyan)">PLMN DECODER:</span> PLMN = MCC (first 3 digits) + MNC (remaining digits). Example: <span style="color:var(--t1)">40410</span> decodes to MCC:404 / MNC:10 (Bharti Airtel, India)</div>', unsafe_allow_html=True)
        p1, p2 = st.columns([2, 3])
        with p1:
            plmn_input = st.text_input("PLMN String", placeholder="e.g. 40410", key="plmn_decode_input", max_chars=8)
        with p2:
            if plmn_input.strip():
                mcc_d, mnc_d = decode_plmn(plmn_input.strip())
                if mcc_d:
                    inf_d = mcc_info(mcc_d); op_d = mnc_info(mcc_d, mnc_d)
                    st.markdown(f'<div style="font-family:var(--mono);font-size:0.78rem;padding:12px 0;display:flex;gap:20px;flex-wrap:wrap"><div><span style="color:var(--t3)">MCC</span> <span style="color:var(--t1)">{mcc_d}</span></div><div><span style="color:var(--t3)">MNC</span> <span style="color:var(--t1)">{mnc_d}</span></div><div><span style="color:var(--t3)">COUNTRY</span> <span style="color:var(--t1)">{inf_d["country"]}</span></div><div><span style="color:var(--t3)">OPERATOR</span> <span style="color:var(--cyan)">{op_d}</span></div></div>', unsafe_allow_html=True)
                    if st.button("Apply Values", key="use_plmn"):
                        st.session_state["_plmn_mcc"] = mcc_d; st.session_state["_plmn_mnc"] = mnc_d; st.rerun()

    tabs = st.tabs(["  Single Entry  ", "  Bulk Import  ", "  Session Records  "])
    with tabs[0]:
        st.markdown('<div class="panel"><div class="panel-title">// NETWORK IDENTIFIER</div>', unsafe_allow_html=True)
        default_mcc = st.session_state.pop("_plmn_mcc", "404")
        default_mnc = st.session_state.pop("_plmn_mnc", "10")
        c1,c2,c3,c4,c5 = st.columns(5)
        with c1: mcc = st.text_input("MCC", value=default_mcc, max_chars=5)
        with c2: mnc = st.text_input("MNC", value=default_mnc, max_chars=5)
        with c3: lac = st.number_input(lac_label, 0, 16777215, 20100)
        with c4: cell_id = st.number_input("Cell ID", 0, 68719476735, 54321)
        with c5: radio = st.selectbox("Radio Standard", ["LTE","NR","GSM","UMTS"] if not is_android else ["GSM","UMTS","LTE","NR"])
        if mcc.strip():
            inf = mcc_info(mcc); op = mnc_info(mcc, mnc)
            with st.spinner("Querying tower location..."):
                loc = get_tower_location(mcc, mnc, lac, cell_id, radio)
            is_real = loc["found"]
            src_color = "var(--green)" if is_real else "var(--amber)"
            st.markdown(f"""
<div style="background:rgba(0,255,179,0.02);border:1px solid var(--border);border-radius:var(--r2);padding:12px 16px;margin-top:10px">
  <div style="display:flex;flex-wrap:wrap;gap:20px;font-family:var(--mono);font-size:0.72rem">
    <div><span style="color:var(--t3)">COUNTRY</span><br><span style="color:var(--t1)">{inf["country"]}</span></div>
    <div><span style="color:var(--t3)">OPERATOR</span><br><span style="color:var(--cyan)">{op}</span></div>
    <div><span style="color:var(--t3)">{lac_label} HEX</span><br><span style="color:var(--t1)">0x{int(lac):04X}</span></div>
    <div><span style="color:var(--t3)">CID HEX</span><br><span style="color:var(--t1)">0x{int(cell_id):04X}</span></div>
    <div><span style="color:var(--t3)">LATITUDE</span><br><span style="color:var(--amber)">{loc["lat"]}</span></div>
    <div><span style="color:var(--t3)">LONGITUDE</span><br><span style="color:var(--amber)">{loc["lng"]}</span></div>
    <div><span style="color:var(--t3)">SOURCE</span><br><span style="color:{src_color}">{loc["source"]}</span></div>
  </div>
</div>""", unsafe_allow_html=True)
            m_mini = folium.Map(location=[loc["lat"], loc["lng"]], zoom_start=14, tiles="CartoDB dark_matter")
            folium.CircleMarker([loc["lat"],loc["lng"]], radius=14, color="#00FFB3", fill=True,
                                fill_color="#7B61FF", fill_opacity=.6, weight=2).add_to(m_mini)
            st_folium(m_mini, width="stretch", height=200)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="panel"><div class="panel-title">// CALL RECORD</div>', unsafe_allow_html=True)
        c1,c2,c3,c4,c5 = st.columns(5)
        with c1: caller = st.text_input("Subscriber (Your Number)", placeholder="+91-98765-43210")
        with c2: callee = st.text_input("Correspondent Number", placeholder="+91-77665-54433")
        with c3: ct = st.selectbox("Event Type", list(CALL_LABELS.keys()), format_func=lambda x: CALL_LABELS.get(x, x))
        with c4: ts_date = st.date_input("Date", value=datetime.today())
        with c5: ts_time = st.time_input("Time", value=datetime.now().time())
        c6, c7, _ = st.columns([1,1,4])
        with c6: duration = st.number_input("Duration (seconds)", 0, 86400, 0 if "SMS" in ct else 120)
        with c7: call_drop = st.checkbox("Call Drop Event")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="panel"><div class="panel-title">// DEVICE IDENTITY — OPTIONAL</div>', unsafe_allow_html=True)
        c1,c2,c3,c4 = st.columns(4)
        with c1: imei = st.text_input("IMEI (15 digits)", max_chars=15)
        with c2: imsi = st.text_input("IMSI / ICCID")
        with c3: signal = st.number_input("Signal Level (dBm)", -120, -40, -75)
        with c4: roaming = st.checkbox("Roaming Active")
        st.markdown('</div>', unsafe_allow_html=True)

        b1, b2, _ = st.columns([1,1,5])
        with b1: add_btn = st.button("Commit Record", use_container_width=True)
        with b2:
            if st.button("Reset Form", use_container_width=True): st.rerun()
        if add_btn:
            if not mcc.strip():
                st.markdown('<div class="abox abox-red">MCC field is required to proceed.</div>', unsafe_allow_html=True)
            else:
                loc = get_tower_location(mcc, mnc, lac, cell_id, radio)
                row = {"call_id": f"CDR{str(len(st.session_state.get('records',[])) + 1).zfill(5)}",
                       "timestamp": datetime.combine(ts_date, ts_time).strftime("%Y-%m-%d %H:%M:%S"),
                       "caller": caller or "Unknown", "callee": callee or "Unknown", "call_type": ct,
                       "duration_sec": int(duration), "mcc": mcc.strip(), "mnc": mnc.strip(),
                       "lac": int(lac), "cell_id": int(cell_id), "radio_type": radio, "device_type": dtype,
                       "imei": imei or "N/A", "imsi": imsi or "N/A", "signal_dbm": int(signal),
                       "latitude": loc["lat"], "longitude": loc["lng"], "tower_range": loc["range"],
                       "tower_source": loc["source"], "roaming": roaming, "call_drop": call_drop,
                       "location_name": f"{mnc_info(mcc,mnc)} {lac_label}:{lac} CID:{cell_id}", "source": "manual"}
                if "records" not in st.session_state: st.session_state["records"] = []
                st.session_state["records"].append(row)
                st.markdown(f'<div class="abox abox-green">Record committed — GPS: {loc["lat"]}, {loc["lng"]} via {loc["source"]}</div>', unsafe_allow_html=True)
                st.rerun()

    with tabs[1]:
        st.markdown(f'<div class="abox abox-cyan"><span style="color:var(--cyan)">FORMAT:</span> one record per line<br><span style="color:var(--t3)">mcc, mnc, {lac_label.lower()}, cell_id, YYYY-MM-DD HH:MM:SS, duration_sec, caller, callee, call_type, radio_type</span></div>', unsafe_allow_html=True)
        bulk = st.text_area("Paste Records:", value="404,10,20100,54321,2024-11-01 09:15:00,245,+91-98765-43210,+91-99887-76655,MO_VOICE,LTE", height=180)
        imei_b = st.text_input("IMEI (apply to all)", "357839054237777", key="b_imei")
        if st.button("Process & Import All"):
            lines_b = [l.strip() for l in bulk.strip().split("\n") if l.strip()]
            added = 0; errs = []; pb = st.progress(0)
            for li, line in enumerate(lines_b):
                p = [x.strip() for x in line.split(",")]
                if len(p) < 6: errs.append(f"Line {li+1}: insufficient fields"); continue
                try:
                    mcc_b, mnc_b, lac_b, cid_b, ts_b, dur_b = p[0], p[1], p[2], p[3], p[4], p[5]
                    caller_b = p[6] if len(p) > 6 else "Unknown"; callee_b = p[7] if len(p) > 7 else "Unknown"
                    ct_b = p[8] if len(p) > 8 else "MO_VOICE"; radio_b = p[9] if len(p) > 9 else "LTE"
                    loc = get_tower_location(mcc_b, mnc_b, int(lac_b), int(cid_b), radio_b)
                    row = {"call_id": f"CDR{str(len(st.session_state.get('records',[])) + 1).zfill(5)}",
                           "timestamp": ts_b, "caller": caller_b, "callee": callee_b, "call_type": ct_b,
                           "duration_sec": int(dur_b), "mcc": mcc_b, "mnc": mnc_b, "lac": int(lac_b), "cell_id": int(cid_b),
                           "radio_type": radio_b, "device_type": dtype, "imei": imei_b, "imsi": "N/A", "signal_dbm": -80,
                           "latitude": loc["lat"], "longitude": loc["lng"], "tower_range": loc["range"],
                           "tower_source": loc["source"], "roaming": False, "call_drop": False,
                           "location_name": f"{mnc_info(mcc_b,mnc_b)} {lac_label}:{lac_b} CID:{cid_b}", "source": "bulk"}
                    if "records" not in st.session_state: st.session_state["records"] = []
                    st.session_state["records"].append(row); added += 1; pb.progress((li+1)/len(lines_b))
                except Exception as ex: errs.append(f"Line {li+1}: {ex}")
            pb.empty()
            if added: st.markdown(f'<div class="abox abox-green">{added} records imported successfully.</div>', unsafe_allow_html=True)
            for e in errs: st.markdown(f'<div class="abox abox-amber">{e}</div>', unsafe_allow_html=True)
            if added: st.rerun()

    with tabs[2]:
        recs = st.session_state.get("records", [])
        bill_recs = st.session_state.get("bill_records", pd.DataFrame())
        bill_count = len(bill_recs) if isinstance(bill_recs, pd.DataFrame) and not bill_recs.empty else 0
        st.markdown(f'<div style="font-family:var(--mono);color:var(--t3);font-size:0.72rem;margin-bottom:14px">{len(recs)} manual + {bill_count} from bill PDF = <span style="color:var(--green)">{len(recs)+bill_count}</span> total records</div>', unsafe_allow_html=True)
        if recs:
            df_v = pd.DataFrame(recs)
            c1, c2 = st.columns([1, 5])
            with c1:
                del_i = st.number_input("Delete row", 1, len(recs), 1)
                if st.button("Remove"): st.session_state["records"].pop(int(del_i)-1); st.rerun()
            show = [c for c in ["call_id","timestamp","caller","callee","call_type","duration_sec","mcc","mnc","lac","cell_id","radio_type","latitude","longitude","tower_source"] if c in df_v.columns]
            st.dataframe(df_v[show], use_container_width=True, height=360)
        else:
            st.markdown('<div class="abox abox-cyan">No manual records in current session.</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  PAGE: PDF BILL UPLOAD
# ─────────────────────────────────────────────
def page_bill_upload():
    st.markdown('<div class="ph"><div class="ph-eyebrow">// AUTOMATED EXTRACTION ENGINE v4</div><div class="ph-title">Bill PDF Ingestion</div><div class="ph-sub">Operator-aware parser · Airtel · Jio · BSNL · Vodafone · Vi · Duration-accurate</div></div>', unsafe_allow_html=True)

    try:
        import pdfplumber
        st.markdown('<div class="abox abox-green"><span style="color:var(--green)">PDFPLUMBER ACTIVE</span> — Primary extraction engine engaged. Optimal parse quality.</div>', unsafe_allow_html=True)
    except ImportError:
        st.markdown('<div class="abox abox-amber"><span style="color:var(--amber)">DEPENDENCY MISSING</span> — Install <span style="color:var(--t1)">pdfplumber</span> for enhanced extraction: <span style="color:var(--t1)">pip install pdfplumber</span></div>', unsafe_allow_html=True)

    uploaded = st.file_uploader("Upload Operator Bill PDF", type=["pdf"], label_visibility="collapsed")

    if uploaded:
        with st.spinner("Executing extraction pipeline..."):
            df_bill, raw_text, diag = parse_pdf_bill(uploaded)

        if diag:
            cols_d = st.columns(6)
            meta = [("Operator", diag.get('operator','?').upper()), ("Strategy", diag.get('strategy','?')),
                    ("Lines Scanned", str(diag.get('total_lines',0))), ("Raw Matches", str(diag.get('raw_matches',0))),
                    ("Final Records", str(diag.get('final_records',0))), ("Date Range", diag.get('date_range','N/A'))]
            for col, (k, v) in zip(cols_d, meta):
                with col:
                    st.markdown(f'<div style="background:var(--bg2);border:1px solid var(--border);border-radius:var(--r2);padding:10px;font-family:var(--mono)"><div style="color:var(--t3);font-size:0.58rem;letter-spacing:0.12em;text-transform:uppercase">{k}</div><div style="color:var(--green);font-weight:600;margin-top:4px;font-size:0.8rem">{v}</div></div>', unsafe_allow_html=True)

        if df_bill is None or df_bill.empty:
            st.markdown('<div class="abox abox-amber"><span style="color:var(--amber)">EXTRACTION FAILED</span> — No structured records could be parsed from the document.<br>Recommended: Install pdfplumber and retry.</div>', unsafe_allow_html=True)
            with st.expander("Raw extracted text"):
                st.text(raw_text[:5000] if raw_text else "No text content extracted.")
        else:
            st.session_state["bill_records"] = df_bill; st.session_state["bill_raw_text"] = raw_text
            n = len(df_bill)
            voice_cnt = int(df_bill["call_type"].str.contains("VOICE",na=False).sum())
            sms_cnt   = int(df_bill["call_type"].str.contains("SMS",  na=False).sum())
            data_cnt  = int(df_bill["call_type"].str.contains("DATA", na=False).sum())
            tot_dur   = int(df_bill["duration_sec"].sum())
            uniq_nums = df_bill["called_number"].nunique() if "called_number" in df_bill.columns else 0

            st.markdown(f"""
<div style="background:var(--bg2);border:1px solid var(--border2);border-radius:var(--r2);padding:28px;margin:20px 0;text-align:center;position:relative;overflow:hidden">
  <div style="position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,var(--green),transparent);opacity:0.5"></div>
  <div style="font-family:var(--display);font-size:1.1rem;font-weight:700;color:var(--t1);margin-bottom:10px">Extraction Complete — {n:,} Records Parsed</div>
  <div style="display:flex;justify-content:center;gap:10px;flex-wrap:wrap;margin-bottom:20px">
    <span class="bd bd-g">{voice_cnt} Voice</span>
    <span class="bd bd-v">{sms_cnt} SMS</span>
    <span class="bd bd-c">{data_cnt} Data</span>
    <span class="bd">{uniq_nums} Numbers</span>
    <span class="bd bd-a">{fmt_dur(tot_dur)} Total Duration</span>
  </div>""", unsafe_allow_html=True)
            ca, cb, cc = st.columns(3)
            with ca: st.button("Open Analytics", use_container_width=True, key="bill_to_analytics", on_click=navigate_to, args=("Analytics",))
            with cb: st.button("Generate Report", use_container_width=True, key="bill_to_report", on_click=navigate_to, args=("Forensic Report",))
            with cc: st.button("Open Dashboard", use_container_width=True, key="bill_to_dash", on_click=navigate_to, args=("Dashboard",))
            st.markdown("</div>", unsafe_allow_html=True)
            _bill_quick_stats(df_bill)

            with st.expander(f"Preview Extracted Records (showing {min(100,n)} of {n})"):
                prev_cols = [c for c in ["call_id","timestamp","called_number","call_type","duration_sec","raw_line"] if c in df_bill.columns]
                preview = df_bill[prev_cols].head(100).copy()
                if "duration_sec" in preview.columns:
                    preview["duration_hms"]   = preview["duration_sec"].apply(fmt_dur_hms)
                    preview["duration_human"] = preview["duration_sec"].apply(fmt_dur)
                st.dataframe(preview, use_container_width=True, height=380)

    elif st.session_state.get("bill_records") is not None and not st.session_state["bill_records"].empty:
        df_bill = st.session_state["bill_records"]
        st.markdown(f'<div class="abox abox-cyan">Session has {len(df_bill)} previously loaded bill records.</div>', unsafe_allow_html=True)
        ca, cb, cc, cd = st.columns(4)
        with ca: st.button("Analytics", use_container_width=True, key="e_ana", on_click=navigate_to, args=("Analytics",))
        with cb: st.button("Report", use_container_width=True, key="e_rep", on_click=navigate_to, args=("Forensic Report",))
        with cc: st.button("Dashboard", use_container_width=True, key="e_dash", on_click=navigate_to, args=("Dashboard",))
        with cd:
            if st.button("Purge Bill Data", use_container_width=True, key="clear_bill"):
                st.session_state.pop("bill_records", None); st.rerun()
        _bill_quick_stats(df_bill)

def _bill_quick_stats(df):
    if df.empty: return
    n = len(df); num_col = get_num_col(df)
    voice_df = df[df["call_type"].str.contains("VOICE",na=False)] if "call_type" in df.columns else df
    longest = voice_df.loc[voice_df["duration_sec"].idxmax()] if len(voice_df) > 0 and voice_df["duration_sec"].max() > 0 else None
    total_dur = int(df["duration_sec"].sum())
    nums = df[num_col].value_counts() if num_col else pd.Series()
    most_called = nums.index[0] if len(nums) else "N/A"
    most_called_cnt = nums.iloc[0] if len(nums) else 0

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sh">Extraction Summary</div>', unsafe_allow_html=True)
    c1,c2,c3,c4,c5 = st.columns(5)
    with c1: st.markdown(f'<div class="kpi"><div class="kpi-label">Total Records</div><div class="kpi-value">{n:,}</div></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="kpi amber"><div class="kpi-label">Total Talk Time</div><div class="kpi-value" style="font-size:1.2rem">{fmt_dur(total_dur)}</div></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="kpi cyan"><div class="kpi-label">Unique Numbers</div><div class="kpi-value">{df[num_col].nunique() if num_col else 0}</div></div>', unsafe_allow_html=True)
    with c4: st.markdown(f'<div class="kpi"><div class="kpi-label">Most Contacted</div><div class="kpi-value" style="font-size:1rem">{most_called_cnt}</div><div class="kpi-sub">{str(most_called)[-13:]}</div></div>', unsafe_allow_html=True)
    with c5:
        if longest is not None:
            st.markdown(f'<div class="kpi red"><div class="kpi-label">Longest Call</div><div class="kpi-value" style="font-size:1.1rem">{fmt_dur(longest["duration_sec"])}</div><div class="kpi-sub">{str(longest.get("called_number",""))[-13:]}</div></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="kpi"><div class="kpi-label">Longest Call</div><div class="kpi-value">—</div></div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  PAGE: DASHBOARD
# ─────────────────────────────────────────────
def page_dashboard():
    df = get_combined_df()
    st.markdown('<div class="ph"><div class="ph-eyebrow">// INTELLIGENCE OVERVIEW</div><div class="ph-title">Forensic Dashboard</div><div class="ph-sub">Unified CDR intelligence — cross-source analysis</div></div>', unsafe_allow_html=True)
    if df.empty:
        st.markdown('<div class="abox abox-cyan">No data ingested. Select a device type, enter tower data, or upload a bill PDF to begin.</div>', unsafe_allow_html=True)
        return

    n = len(df)
    vc = int(df["call_type"].str.contains("VOICE",na=False).sum()) if "call_type" in df.columns else 0
    sc = int(df["call_type"].str.contains("SMS",  na=False).sum()) if "call_type" in df.columns else 0
    dur = int(df["duration_sec"].sum())
    num_col = get_num_col(df)
    uc = df[num_col].nunique() if num_col else 0
    tw = df["cell_id"].nunique() if "cell_id" in df.columns else 0

    cols = st.columns(6)
    kpi_data = [
        ("Total Records", f"{n:,}", ""),
        ("Voice Events", f"{vc:,}", "cyan"),
        ("SMS Events", f"{sc:,}", "violet"),
        ("Talk Duration", fmt_dur(dur), "amber"),
        ("Unique Contacts", f"{uc}", "green"),
        ("Cell Towers", f"{tw}", ""),
    ]
    for col, (lbl, val, cls) in zip(cols, kpi_data):
        with col:
            st.markdown(f'<div class="kpi {cls}"><div class="kpi-label">{lbl}</div><div class="kpi-value" style="font-size:1.3rem">{val}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns([3, 2])
    with c1:
        st.markdown('<div class="sh">Call Volume Timeline</div>', unsafe_allow_html=True)
        daily = df.copy(); daily["period"] = daily["timestamp"].dt.date.astype(str)
        if "call_type" in daily.columns:
            grp = daily.groupby(["period","call_type"]).size().reset_index(name="n")
            fig = px.area(grp, x="period", y="n", color="call_type",
                          color_discrete_map=TYPE_COLORS, template="plotly_dark",
                          labels={"period":"Date","n":"Records","call_type":"Type"})
        else:
            grp = daily.groupby("period").size().reset_index(name="n")
            fig = px.area(grp, x="period", y="n", template="plotly_dark",
                          color_discrete_sequence=["#00FFB3"], labels={"period":"Date","n":"Records"})
        fig.update_layout(**_dark_layout(height=260, legend=dict(orientation="h",y=1.05,xanchor="right",x=1,font_size=9)))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown('<div class="sh">Traffic Composition</div>', unsafe_allow_html=True)
        if "call_type" in df.columns:
            tc = df["call_type"].value_counts()
            fig2 = go.Figure(go.Pie(
                labels=[CALL_LABELS.get(t,t) for t in tc.index],
                values=tc.values, hole=0.68,
                marker=dict(colors=[TYPE_COLORS.get(t,"#3A5570") for t in tc.index],
                            line=dict(color="#030508", width=2)),
                textinfo="label+percent", textfont=dict(size=9, color="#7A95B0")))
            fig2.update_layout(**_dark_layout(height=260, showlegend=False,
                annotations=[dict(text=f'<b style="font-size:18px">{n}</b>',
                             x=.5, y=.5, showarrow=False, font=dict(color="#00FFB3", size=22, family="Exo 2"))]))
            st.plotly_chart(fig2, use_container_width=True)

    c3, c4 = st.columns([3, 2])
    with c3:
        st.markdown('<div class="sh">Hourly Activity Heatmap</div>', unsafe_allow_html=True)
        df2 = df.copy(); df2["hr"] = df2["timestamp"].dt.hour; df2["dow"] = df2["timestamp"].dt.strftime("%a")
        hm = df2.groupby(["dow","hr"]).size().unstack(fill_value=0)
        hm = hm.reindex([d for d in ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"] if d in hm.index])
        if not hm.empty:
            fig3 = go.Figure(go.Heatmap(
                z=hm.values, x=[f"{h:02d}:00" for h in hm.columns], y=hm.index.tolist(),
                colorscale=[[0,"#030508"],[0.3,"#051C0A"],[0.65,"#00661A"],[1,"#00FFB3"]],
                showscale=True, colorbar=dict(thickness=6, tickfont=dict(size=8,color="#3A5570")),
                hovertemplate="<b>%{y}</b> %{x}<br>%{z} events<extra></extra>"))
            fig3.update_layout(**_dark_layout(height=220, margin=dict(l=0,r=40,t=10,b=0)))
            fig3.update_xaxes(tickangle=-45, tickfont=dict(size=8))
            st.plotly_chart(fig3, use_container_width=True)

    with c4:
        st.markdown('<div class="sh">Top Correspondents</div>', unsafe_allow_html=True)
        if num_col:
            top = df[num_col].value_counts().head(6)
            book = get_contacts()
            for i, (num, cnt) in enumerate(top.items()):
                pct = cnt / max(len(df), 1) * 100
                disp = book.get(str(num), str(num))
                st.markdown(f"""
<div style="margin-bottom:10px">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:3px">
    <span style="font-family:var(--mono);font-size:0.7rem;color:var(--t2)"><span style="color:var(--green)">#{i+1:02d}</span> {disp}</span>
    <span class="bd bd-g">{cnt}</span>
  </div>
  <div style="background:rgba(0,255,179,0.05);border-radius:2px;height:3px">
    <div style="width:{pct:.1f}%;background:linear-gradient(90deg,var(--green),var(--cyan));height:100%;border-radius:2px;transition:width 0.3s"></div>
  </div>
</div>""", unsafe_allow_html=True)

    night = df[(df["timestamp"].dt.hour < 5) | (df["timestamp"].dt.hour >= 23)]
    if len(night) > 0:
        st.markdown(f'<div class="abox abox-red" style="margin-top:14px">ALERT: {len(night)} anomalous events detected in 23:00–05:00 window.</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  PAGE: CONTACT MANAGER
# ─────────────────────────────────────────────
def page_contact_manager():
    st.markdown("""
<div class="ph">
  <div class="ph-eyebrow">// IDENTITY RESOLUTION LAYER</div>
  <div class="ph-title">Contact Intelligence</div>
  <div class="ph-sub">Assign identities to subscriber numbers — names propagate across all modules and generated reports</div>
</div>""", unsafe_allow_html=True)

    df = get_combined_df()
    book = get_contacts()
    num_col = get_num_col(df)

    total_contacts = len(book)
    mapped_records = 0
    if not df.empty and num_col and book:
        mapped_records = int(df[num_col].apply(lambda x: re.sub(r'[\s\-\.\(\)]','',str(x)) in book).sum())
    total_records = len(df)

    st.markdown(f"""
<div class="cm-stats-bar">
  <div class="cm-stat">
    <div style="font-family:var(--mono);font-size:0.9rem;color:var(--green)">ID</div>
    <div><div class="cm-stat-val">{total_contacts}</div><div class="cm-stat-lbl">Saved Contacts</div></div>
  </div>
  <div class="cm-stat">
    <div style="font-family:var(--mono);font-size:0.9rem;color:var(--cyan)">LK</div>
    <div><div class="cm-stat-val">{mapped_records}</div><div class="cm-stat-lbl">Mapped Records</div></div>
  </div>
  <div class="cm-stat">
    <div style="font-family:var(--mono);font-size:0.9rem;color:var(--amber)">DB</div>
    <div><div class="cm-stat-val">{total_records}</div><div class="cm-stat-lbl">Total CDRs</div></div>
  </div>
  <div class="cm-stat">
    <div style="font-family:var(--mono);font-size:0.9rem;color:var(--violet)">CV</div>
    <div><div class="cm-stat-val">{round(mapped_records/max(total_records,1)*100)}%</div><div class="cm-stat-lbl">ID Coverage</div></div>
  </div>
</div>
""", unsafe_allow_html=True)

    known_nums = []
    if not df.empty and num_col:
        known_nums = [str(n) for n in df[num_col].dropna().unique().tolist()[:100]]

    st.markdown("""<div class="cm-add-panel"><div class="cm-add-title">Add / Edit Contact Identity</div>""", unsafe_allow_html=True)
    
    # Define callbacks
    def on_pick_change():
        selected = st.session_state.get("cm_pick", "select")
        if selected != "select":
            st.session_state["cm_add_num"] = selected
    
    def on_save_click():
        n_clean = re.sub(r'[\s\-\.\(\)]', '', st.session_state.get("cm_add_num", "").strip())
        n_name  = st.session_state.get("cm_add_name", "").strip()
        if n_clean and n_name:
            set_contact(n_clean, n_name)
            st.session_state["cm_save_success"] = True
            st.session_state["cm_save_num"] = n_clean
            st.session_state["cm_save_name"] = n_name
            # Clear fields for next entry
            st.session_state["cm_add_num"] = ""
            st.session_state["cm_add_name"] = ""
            st.session_state["cm_pick"] = "select"
        else:
            st.session_state["cm_save_success"] = False
    
    col_a, col_b, col_c, col_d = st.columns([3, 3, 2, 1])
    
    with col_a:
        add_num = st.text_input("Subscriber Number", placeholder="+91XXXXXXXXXX", key="cm_add_num")
    with col_b:
        add_name = st.text_input("Identity Label", placeholder="Full name or alias", key="cm_add_name")
    with col_c:
        if known_nums:
            pick = st.selectbox("Dataset Numbers", ["select"] + known_nums, key="cm_pick", on_change=on_pick_change)
    with col_d:
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("SAVE", use_container_width=True, key="cm_save", on_click=on_save_click)

    # Show success or error message
    if st.session_state.get("cm_save_success"):
        n_clean = st.session_state.get("cm_save_num", "")
        n_name = st.session_state.get("cm_save_name", "")
        st.markdown(f'<div class="abox abox-green">Identity mapped: <span style="color:var(--t1)">{n_clean}</span> assigned to <span style="color:var(--green)">{n_name}</span></div>', unsafe_allow_html=True)
        st.session_state["cm_save_success"] = False
        st.rerun()
    elif st.session_state.get("cm_save_error"):
        st.markdown('<div class="abox abox-red">Both subscriber number and identity label are required.</div>', unsafe_allow_html=True)
        st.session_state["cm_save_error"] = False
    st.markdown("</div>", unsafe_allow_html=True)

    with st.expander("  Bulk CSV Import"):
        st.markdown('<div class="abox abox-cyan">One record per line: <span style="color:var(--t1)">number,name</span></div>', unsafe_allow_html=True)
        bulk_csv = st.text_area("CSV Data:", height=110, key="cm_bulk", placeholder="+919876543210,Ravi Kumar\n+918800112233,Priya Sharma")
        col_imp1, col_imp2 = st.columns([1, 5])
        with col_imp1:
            if st.button("Import", key="cm_bulk_import", use_container_width=True):
                added = 0
                for line in bulk_csv.strip().split("\n"):
                    parts = line.strip().split(",", 1)
                    if len(parts) == 2:
                        n_ = re.sub(r'[\s\-\.\(\)]', '', parts[0].strip())
                        nm_ = parts[1].strip()
                        if n_ and nm_:
                            set_contact(n_, nm_); added += 1
                if added:
                    st.markdown(f'<div class="abox abox-green">Imported {added} contact identities.</div>', unsafe_allow_html=True)
                    st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    if not book:
        st.markdown("""
<div class="cm-empty">
  <div style="font-family:var(--mono);font-size:0.7rem;color:var(--t3);margin-bottom:16px">[ NO IDENTITY RECORDS ]</div>
  <div class="cm-empty-title">Contact Database Empty</div>
  <div class="cm-empty-sub">Add subscriber identities above to enable name resolution across all platform views and forensic reports.</div>
</div>""", unsafe_allow_html=True)
    else:
        s1, s2 = st.columns([4, 1])
        with s1:
            srch = st.text_input("", placeholder="Search by name or number...", key="cm_search", label_visibility="collapsed")
        with s2:
            csv_export = "\n".join([f"{k},{v}" for k, v in book.items()])
            st.download_button("Export CSV", csv_export.encode(), "contacts.csv", "text/csv", key="cm_export", use_container_width=True)

        items = list(book.items())
        if srch:
            items = [(k,v) for k,v in items if srch.lower() in k.lower() or srch.lower() in v.lower()]

        st.markdown(f'<div class="cm-section-label">{len(items)} identity record{"s" if len(items)!=1 else ""}</div>', unsafe_allow_html=True)

        cols_per_row = 2
        for row_start in range(0, len(items), cols_per_row):
            row_items = items[row_start:row_start + cols_per_row]
            grid_cols = st.columns(cols_per_row)
            for ci, (num, name) in enumerate(row_items):
                with grid_cols[ci]:
                    count_str = "0 records"
                    dur_str = ""; voice_c = 0; sms_c = 0; night_c_ = 0; last_seen = ""
                    if not df.empty and num_col:
                        n_match = df[df[num_col].astype(str).str.replace(r'[\s\-\.\(\)]','',regex=True) == num]
                        if len(n_match) > 0:
                            count_str = f"{len(n_match)} records"
                            td = int(n_match["duration_sec"].sum())
                            if td > 0: dur_str = fmt_dur(td)
                            if "call_type" in n_match.columns:
                                voice_c = int(n_match["call_type"].str.contains("VOICE",na=False).sum())
                                sms_c   = int(n_match["call_type"].str.contains("SMS",  na=False).sum())
                            night_c_ = int(((n_match["timestamp"].dt.hour < 5) | (n_match["timestamp"].dt.hour >= 23)).sum())
                            last_ts = n_match["timestamp"].max()
                            if pd.notna(last_ts): last_seen = last_ts.strftime("%d %b %Y")

                    initials = "".join([w[0].upper() for w in name.split()[:2]])
                    grad = _avatar_gradient(num)
                    uid  = hashlib.md5(num.encode()).hexdigest()[:6]

                    chips = []
                    if voice_c:  chips.append(f'<span class="cm-chip c">{voice_c} CALLS</span>')
                    if sms_c:    chips.append(f'<span class="cm-chip g">{sms_c} SMS</span>')
                    if dur_str:  chips.append(f'<span class="cm-chip a">{dur_str}</span>')
                    if night_c_: chips.append(f'<span class="cm-chip r">{night_c_} NIGHT</span>')
                    if last_seen:chips.append(f'<span class="cm-chip">LAST {last_seen}</span>')
                    chips_html = " ".join(chips) if chips else f'<span class="cm-chip">{count_str}</span>'

                    st.markdown(f"""
<div class="cm-card">
  <div class="cm-card-accent" style="background:{grad}"></div>
  <div class="cm-card-body">
    <div class="cm-avatar" style="background:{grad}">{initials}</div>
    <div class="cm-info">
      <div class="cm-name">{name}</div>
      <div class="cm-number">{num}</div>
      <div class="cm-meta">{chips_html}</div>
    </div>
  </div>
</div>""", unsafe_allow_html=True)

                    act1, act2, act3 = st.columns([3, 1, 1])
                    with act1:
                        new_name = st.text_input("Rename", value=name, key=f"cm_rename_{uid}", label_visibility="collapsed", placeholder="Rename identity...")
                        if new_name != name and new_name.strip():
                            set_contact(num, new_name.strip()); st.rerun()
                    with act2:
                        if st.button("SAVE", key=f"cm_savebtn_{uid}", use_container_width=True):
                            val = st.session_state.get(f"cm_rename_{uid}", "").strip()
                            if val: set_contact(num, val); st.rerun()
                    with act3:
                        if st.button("DEL", key=f"cm_del_{uid}", use_container_width=True):
                            delete_contact(num); st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="cm-section-label">Danger Zone</div>', unsafe_allow_html=True)
        col_clr1, col_clr2 = st.columns([1, 5])
        with col_clr1:
            if st.button("PURGE ALL CONTACTS", key="cm_clear_all", use_container_width=True):
                st.session_state["contact_book"] = {}; st.rerun()


# ─────────────────────────────────────────────
#  PAGE: FULL ANALYTICS
# ─────────────────────────────────────────────
def page_analytics():
    df = get_combined_df()
    st.markdown('<div class="ph"><div class="ph-eyebrow">// DEEP FORENSIC ANALYSIS</div><div class="ph-title">Call Analytics</div><div class="ph-sub">Behavioral · temporal · duration · network · contact intelligence</div></div>', unsafe_allow_html=True)
    if df.empty:
        st.markdown('<div class="abox abox-cyan">No data available for analysis.</div>', unsafe_allow_html=True)
        return

    book = get_contacts()
    num_col = get_num_col(df)
    voice_df = df[df["duration_sec"] > 0].copy() if "duration_sec" in df.columns else df.copy()

    t1,t2,t3,t4,t5,t6,t7 = st.tabs(["  Top Records  ","  Duration  ","  Temporal  ","  Anomaly  ","  Contact Detail  ","  Network Graph  ","  Number Intel  "])

    with t1:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="sh">Longest Duration Calls</div>', unsafe_allow_html=True)
            if not voice_df.empty and voice_df["duration_sec"].max() > 0:
                top_dur = voice_df.nlargest(10, "duration_sec")
                for i, (_, r) in enumerate(top_dur.iterrows()):
                    callee_val = r.get("callee") or r.get("called_number","?")
                    disp_name = book.get(re.sub(r'[\s\-\.\(\)]','',str(callee_val)), str(callee_val))
                    ts_val = r["timestamp"].strftime("%d %b %Y  %H:%M:%S") if pd.notna(r["timestamp"]) else "?"
                    ct_label = CALL_LABELS.get(r.get("call_type","MO_VOICE"), "Call")
                    st.markdown(f"""
<div class="call-card">
  <div style="display:flex;justify-content:space-between;margin-bottom:5px">
    <span style="font-family:var(--mono);font-size:0.6rem;color:var(--green)">RANK #{i+1:02d}</span>
    <span class="bd bd-a">{fmt_dur_hms(r['duration_sec'])} &nbsp; {fmt_dur(r['duration_sec'])}</span>
  </div>
  <div style="font-family:var(--mono);color:var(--t1);font-size:0.82rem;margin-bottom:3px">{disp_name}</div>
  <div style="font-family:var(--body);color:var(--t3);font-size:0.72rem">{ts_val} &nbsp; {ct_label}</div>
</div>""", unsafe_allow_html=True)
            else:
                st.markdown('<div class="abox abox-amber">No duration data found in current dataset.</div>', unsafe_allow_html=True)

        with c2:
            st.markdown('<div class="sh">Most Frequent Correspondents</div>', unsafe_allow_html=True)
            if num_col:
                top_rep = df[num_col].value_counts().head(10)
                for i, (num, cnt) in enumerate(top_rep.items()):
                    n_df = df[df[num_col] == num]
                    total_d = int(n_df["duration_sec"].sum())
                    last_call = n_df["timestamp"].max()
                    sms_c  = int(n_df["call_type"].str.contains("SMS",  na=False).sum()) if "call_type" in n_df.columns else 0
                    voice_c= int(n_df["call_type"].str.contains("VOICE",na=False).sum()) if "call_type" in n_df.columns else 0
                    disp_name = book.get(re.sub(r'[\s\-\.\(\)]','',str(num)), str(num))
                    st.markdown(f"""
<div class="call-card">
  <div style="display:flex;justify-content:space-between;margin-bottom:5px">
    <span class="bd {'bd-r' if i==0 else ''}">#{i+1:02d}{' TOP' if i==0 else ''}</span>
    <span style="font-family:var(--mono);font-size:0.8rem;color:var(--green)">{cnt}x</span>
  </div>
  <div style="font-family:var(--mono);color:var(--t1);font-size:0.82rem;margin-bottom:3px">{disp_name}</div>
  <div style="font-family:var(--body);color:var(--t3);font-size:0.72rem">{fmt_dur(total_d)} · {voice_c} voice · {sms_c} sms · Last: {last_call.strftime("%d %b %Y") if pd.notna(last_call) else "?"}</div>
</div>""", unsafe_allow_html=True)

    with t2:
        if voice_df.empty or voice_df["duration_sec"].max() == 0:
            st.markdown('<div style="text-align:center;padding:60px"><div style="font-family:var(--mono);font-size:0.7rem;color:var(--t3)">// NO DURATION DATA AVAILABLE</div></div>', unsafe_allow_html=True)
        else:
            m1,m2,m3,m4,m5,m6 = st.columns(6)
            total_talk = int(voice_df["duration_sec"].sum())
            for col, (lbl, val) in zip([m1,m2,m3,m4,m5,m6], [
                ("Events w/ Duration", f"{len(voice_df):,}"),
                ("Mean Duration", fmt_dur(voice_df["duration_sec"].mean())),
                ("Median Duration", fmt_dur(voice_df["duration_sec"].median())),
                ("Longest Call", fmt_dur(voice_df["duration_sec"].max())),
                ("Total Talk Time", fmt_dur(total_talk)),
                ("Std Deviation", fmt_dur(voice_df["duration_sec"].std()))
            ]):
                with col:
                    st.markdown(f'<div class="kpi" style="padding:12px"><div class="kpi-label">{lbl}</div><div class="kpi-value" style="font-size:0.95rem">{val}</div></div>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            dur_unit = st.session_state.get("dur_unit_sel", "Seconds")
            pu1,pu2,pu3,_ = st.columns([1,1,1,5])
            with pu1:
                if st.button("Seconds", key="du_s", use_container_width=True): st.session_state["dur_unit_sel"] = "Seconds"; st.rerun()
            with pu2:
                if st.button("Minutes", key="du_m", use_container_width=True): st.session_state["dur_unit_sel"] = "Minutes"; st.rerun()
            with pu3:
                if st.button("HH:MM:SS", key="du_h", use_container_width=True): st.session_state["dur_unit_sel"] = "HH:MM:SS"; st.rerun()
            dur_unit = st.session_state.get("dur_unit_sel", "Seconds")

            c1, c2 = st.columns(2)
            with c1:
                st.markdown('<div class="sh">Duration Distribution</div>', unsafe_allow_html=True)
                plot_df = voice_df.copy()
                plot_df["dur_plot"] = plot_df["duration_sec"].apply(lambda x: round(x/60, 2) if dur_unit == "Minutes" else x)
                fig_h = px.histogram(plot_df, x="dur_plot", nbins=40, color_discrete_sequence=["#00FFB3"], template="plotly_dark",
                    labels={"dur_plot": f"Duration ({dur_unit})", "count": "Calls"})
                fig_h.update_layout(**_dark_layout(height=300, bargap=.04))
                st.plotly_chart(fig_h, use_container_width=True)

            with c2:
                st.markdown('<div class="sh">Top Numbers by Talk Time</div>', unsafe_allow_html=True)
                if num_col and num_col in voice_df.columns:
                    td = voice_df.groupby(num_col)["duration_sec"].sum().sort_values(ascending=False).head(12)
                    td_plot = td.apply(lambda x: round(x/60,1) if dur_unit == "Minutes" else x)
                    labels_td = [book.get(re.sub(r'[\s\-\.\(\)]','',str(n)),str(n))[-16:] for n in td.index]
                    fig_td = px.bar(x=td_plot.values, y=labels_td, orientation="h",
                        color=td_plot.values, color_continuous_scale=["#051C0A","#00661A","#00FFB3"], template="plotly_dark")
                    fig_td.update_layout(**_dark_layout(height=300, coloraxis_showscale=False, margin=dict(l=0,r=0,t=10,b=0)))
                    st.plotly_chart(fig_td, use_container_width=True)

            st.markdown('<div class="sh">Duration Bracket Analysis</div>', unsafe_allow_html=True)
            bins = [0,10,30,60,120,300,600,1800,3600,86400]
            labels_b = ["<10s","10-30s","30-60s","1-2m","2-5m","5-10m","10-30m","30-60m",">1h"]
            v2 = voice_df.copy(); v2["bucket"] = pd.cut(v2["duration_sec"], bins=bins, labels=labels_b)
            bc = v2["bucket"].value_counts().reindex(labels_b, fill_value=0)
            fig_b = go.Figure(go.Bar(
                x=bc.index, y=bc.values,
                marker=dict(color=bc.values, colorscale=[[0,"#030508"],[.5,"#005A15"],[1,"#00FFB3"]]),
                text=[f"{v/max(bc.sum(),1)*100:.1f}%" for v in bc.values], textposition="outside",
                textfont=dict(size=9, color="#3A5570")))
            fig_b.update_layout(**_dark_layout(height=260, showlegend=False))
            st.plotly_chart(fig_b, use_container_width=True)

    with t3:
        view_opts = [("T","Hour of Day","Peak call hours"), ("D","Day of Week","Weekday vs weekend"), ("M","Monthly Trend","Volume per month"), ("A","All Days","Day-by-day timeline")]
        if "temporal_view_idx" not in st.session_state: st.session_state["temporal_view_idx"] = 0
        st.markdown('<div style="font-family:var(--mono);font-size:0.58rem;color:var(--t3);letter-spacing:0.15em;margin-bottom:10px">// SELECT TEMPORAL VIEW</div>', unsafe_allow_html=True)
        sel_cols = st.columns(4)
        for ci, (icon, label, desc) in enumerate(view_opts):
            with sel_cols[ci]:
                is_sel = (st.session_state["temporal_view_idx"] == ci)
                border = "var(--green)" if is_sel else "var(--border)"
                bg = "rgba(0,255,179,0.04)" if is_sel else "var(--bg2)"
                tc = "var(--green)" if is_sel else "var(--t3)"
                st.markdown(f'<div style="background:{bg};border:1px solid {border};border-radius:var(--r2);padding:10px 12px;text-align:center;margin-bottom:4px"><div style="font-family:var(--mono);font-size:0.6rem;color:{tc};letter-spacing:0.15em">{icon}</div><div style="font-family:var(--display);font-size:0.78rem;font-weight:600;color:{"var(--t1)" if is_sel else "var(--t2)"};margin:2px 0">{label}</div><div style="font-family:var(--body);font-size:0.62rem;color:var(--t3)">{desc}</div></div>', unsafe_allow_html=True)
                if st.button("Select", key=f"tv_{ci}", use_container_width=True):
                    st.session_state["temporal_view_idx"] = ci; st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        total_days = max(1, (df["timestamp"].max()-df["timestamp"].min()).days)
        avg_per_day = len(df)/total_days
        peak_hour = df.groupby(df["timestamp"].dt.hour).size().idxmax() if len(df) > 0 else 0
        weekend_c = len(df[df["timestamp"].dt.dayofweek >= 5])
        night_c = len(df[(df["timestamp"].dt.hour < 5) | (df["timestamp"].dt.hour >= 23)])
        st.markdown(f'<div style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:20px"><div class="stat-pill"><span class="sp-val">{len(df):,}</span><span class="sp-lbl">Records</span></div><div class="stat-pill"><span class="sp-val" style="color:var(--green)">{avg_per_day:.1f}</span><span class="sp-lbl">Avg/Day</span></div><div class="stat-pill"><span class="sp-val" style="color:var(--amber)">{peak_hour:02d}:00</span><span class="sp-lbl">Peak Hour</span></div><div class="stat-pill"><span class="sp-val" style="color:var(--violet)">{weekend_c}</span><span class="sp-lbl">Weekend</span></div><div class="stat-pill"><span class="sp-val" style="color:var(--red)">{night_c}</span><span class="sp-lbl">Late Night</span></div><div class="stat-pill"><span class="sp-val" style="color:var(--cyan)">{total_days}</span><span class="sp-lbl">Days Span</span></div></div>', unsafe_allow_html=True)

        view_idx = st.session_state["temporal_view_idx"]
        view_t = view_opts[view_idx][1]

        if view_t == "Hour of Day":
            df3 = df.copy(); df3["hour"] = df3["timestamp"].dt.hour
            if "call_type" in df3.columns:
                hourly = df3.groupby(["hour","call_type"]).size().reset_index(name="n")
                fig_hr = px.bar(hourly, x="hour", y="n", color="call_type", color_discrete_map=TYPE_COLORS, template="plotly_dark", barmode="stack", labels={"hour":"Hour","n":"Records"})
            else:
                hourly = df3.groupby("hour").size().reset_index(name="n")
                fig_hr = px.bar(hourly, x="hour", y="n", color_discrete_sequence=["#00FFB3"], template="plotly_dark")
            fig_hr.add_vrect(x0=-.5, x1=4.5, fillcolor="rgba(255,51,102,0.05)", line_width=0, annotation_text="LATE NIGHT", annotation_font=dict(color="#FF3366",size=8))
            fig_hr.update_layout(**_dark_layout(height=320, legend=dict(orientation="h",y=1.05,font_size=9), xaxis=dict(dtick=1,tickangle=-45)))
            st.plotly_chart(fig_hr, use_container_width=True)

        elif view_t == "Day of Week":
            df3 = df.copy(); df3["dow"] = df3["timestamp"].dt.strftime("%a")
            dc = df3["dow"].value_counts().reindex(["Mon","Tue","Wed","Thu","Fri","Sat","Sun"], fill_value=0)
            colors_dow = ["#7B61FF" if d in ["Sat","Sun"] else "#00FFB3" for d in dc.index]
            fig_dw = go.Figure(go.Bar(x=dc.index, y=dc.values, marker_color=colors_dow, text=dc.values, textposition="outside", textfont=dict(size=9, color="#3A5570")))
            fig_dw.update_layout(**_dark_layout(height=300))
            st.plotly_chart(fig_dw, use_container_width=True)

        elif view_t == "Monthly Trend":
            df3 = df.copy(); df3["month"] = df3["timestamp"].dt.strftime("%Y-%m")
            monthly = df3.groupby("month").agg(calls=("call_id","count"),duration=("duration_sec","sum")).reset_index()
            monthly["duration_min"] = monthly["duration"].apply(lambda x: round(x/60,1))
            monthly["duration_human"] = monthly["duration"].apply(fmt_dur)
            fig_mo = go.Figure()
            fig_mo.add_trace(go.Bar(x=monthly["month"], y=monthly["calls"], name="Events", marker_color="#00FFB3", opacity=.7))
            fig_mo.add_trace(go.Scatter(x=monthly["month"], y=monthly["duration_min"], name="Duration (min)", line=dict(color="#FFD700", width=2), yaxis="y2", mode="lines+markers", marker=dict(size=5), customdata=monthly["duration_human"], hovertemplate="<b>%{x}</b><br>%{customdata}<extra></extra>"))
            fig_mo.update_layout(**_dark_layout(height=300, margin=dict(l=0,r=50,t=10,b=0), yaxis2=dict(overlaying="y",side="right"), legend=dict(orientation="h",y=1.1,font_size=9)))
            st.plotly_chart(fig_mo, use_container_width=True)

        elif view_t == "All Days":
            df3 = df.copy(); df3["date"] = df3["timestamp"].dt.date
            if "call_type" in df3.columns:
                grp = df3.groupby(["date","call_type"]).size().reset_index(name="n")
                fig = px.bar(grp, x="date", y="n", color="call_type", color_discrete_map=TYPE_COLORS, template="plotly_dark", barmode="stack")
            else:
                grp = df3.groupby("date").size().reset_index(name="n")
                fig = px.bar(grp, x="date", y="n", color_discrete_sequence=["#00FFB3"], template="plotly_dark")
            fig.update_layout(**_dark_layout(height=320, legend=dict(orientation="h",y=1.05,font_size=9)))
            st.plotly_chart(fig, use_container_width=True)

    with t4:
        st.markdown('<div class="sh">Forensic Anomaly Detection Engine</div>', unsafe_allow_html=True)
        anomalies = []
        night_df = df[(df["timestamp"].dt.hour < 5) | (df["timestamp"].dt.hour >= 23)].copy()
        if len(night_df) > 0:
            anomalies.append({"severity":"HIGH" if len(night_df)>=5 else "MEDIUM","type":"Late-Night Activity","count":len(night_df),"detail":f"{len(night_df)} events in 23:00–05:00 window.","df":night_df})
        if not voice_df.empty and voice_df["duration_sec"].max() > 0:
            flash = voice_df[(voice_df["duration_sec"] > 0) & (voice_df["duration_sec"] < 10)].copy()
            if len(flash) > 2:
                anomalies.append({"severity":"HIGH" if len(flash)>=8 else "MEDIUM","type":"Flash Calls (<10s)","count":len(flash),"detail":f"{len(flash)} calls under 10 seconds — potential signal/burner usage.","df":flash})
        if "call_drop" in df.columns:
            drops = df[df["call_drop"] == True].copy()
            if len(drops) > 3:
                anomalies.append({"severity":"MEDIUM","type":"Elevated Call Drop Rate","count":len(drops),"detail":f"{len(drops)} drop events recorded.","df":drops})
        if "roaming" in df.columns:
            roam = df[df["roaming"] == True].copy()
            if len(roam) > 0:
                anomalies.append({"severity":"HIGH","type":"Roaming Events Detected","count":len(roam),"detail":f"{len(roam)} events on foreign PLMN — possible cross-border activity.","df":roam})
        if len(df) > 5:
            df_burst = df.copy(); df_burst["date"] = df_burst["timestamp"].dt.date
            daily_counts = df_burst.groupby("date").size()
            mean_d = daily_counts.mean(); burst_days = daily_counts[daily_counts > mean_d*2.5]
            if len(burst_days) > 0:
                burst_df = df[df["timestamp"].dt.date.isin(burst_days.index)].copy()
                anomalies.append({"severity":"MEDIUM","type":"Burst Activity Detected","count":len(burst_days),"detail":f"{len(burst_days)} day(s) with 2.5x above average volume.","df":burst_df})
        if num_col:
            vc_a = df[num_col].value_counts(); single_use = vc_a[vc_a == 1]
            if len(single_use) > len(vc_a)*0.6:
                anomalies.append({"severity":"MEDIUM","type":"High Single-Use Number Ratio","count":len(single_use),"detail":f"{len(single_use)}/{len(vc_a)} numbers contacted exactly once — potential disposable number usage.","df":df[df[num_col].isin(single_use.index)].copy()})

        if not anomalies:
            st.markdown('<div class="abox abox-green">CLEAR — No significant anomaly patterns detected in current dataset.</div>', unsafe_allow_html=True)
        else:
            sev_s = {"CRITICAL":4,"HIGH":3,"MEDIUM":2,"LOW":1}
            ts = sum(sev_s.get(a["severity"],1) for a in anomalies)
            rp = min(100, int(ts/max(len(anomalies)*4,1)*100))
            rl = "CRITICAL" if rp>=75 else "HIGH" if rp>=50 else "MEDIUM" if rp>=25 else "LOW"
            rc = "#FF3366" if rl in ["CRITICAL","HIGH"] else "#FFD700" if rl=="MEDIUM" else "#00FFB3"

            r1_,r2_,r3_,r4_ = st.columns(4)
            with r1_: st.markdown(f'<div class="kpi"><div class="kpi-label">Threat Level</div><div class="kpi-value" style="color:{rc}">{rl}</div></div>', unsafe_allow_html=True)
            with r2_: st.markdown(f'<div class="kpi red"><div class="kpi-label">Anomalies</div><div class="kpi-value">{len(anomalies)}</div></div>', unsafe_allow_html=True)
            with r3_: st.markdown(f'<div class="kpi amber"><div class="kpi-label">Risk Score</div><div class="kpi-value">{rp}/100</div></div>', unsafe_allow_html=True)
            with r4_:
                hc = sum(1 for a in anomalies if a["severity"] in ["CRITICAL","HIGH"])
                st.markdown(f'<div class="kpi"><div class="kpi-label">High/Critical</div><div class="kpi-value" style="color:var(--red)">{hc}</div></div>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            sev_colors = {"CRITICAL":("#FF3366","rgba(255,51,102,0.04)"),"HIGH":("#FFD700","rgba(255,215,0,0.03)"),"MEDIUM":("#7B61FF","rgba(123,97,255,0.03)"),"LOW":("#00FFB3","rgba(0,255,179,0.03)")}
            for a in sorted(anomalies, key=lambda x: {"CRITICAL":0,"HIGH":1,"MEDIUM":2,"LOW":3}.get(x["severity"],3)):
                sc_col, sc_bg = sev_colors.get(a["severity"], ("#888","rgba(0,0,0,0)"))
                st.markdown(f'<div class="anomaly-card" style="background:{sc_bg};border-left-color:{sc_col}"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px"><div style="font-family:var(--display);font-size:0.88rem;font-weight:600;color:var(--t1)">{a["type"]}</div><div style="display:flex;gap:8px;align-items:center"><span style="font-family:var(--mono);font-size:0.65rem;color:var(--t3)">{a["count"]} records</span><span class="bd" style="color:{sc_col};border-color:{sc_col}30;background:{sc_col}10">{a["severity"]}</span></div></div><div style="font-family:var(--body);color:var(--t2);font-size:0.8rem">{a["detail"]}</div></div>', unsafe_allow_html=True)
                if "df" in a and not a["df"].empty:
                    with st.expander(f"Inspect {len(a['df'])} records"):
                        show_anom = a["df"].copy()
                        show_anom["Time"] = show_anom["timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S")
                        show_anom["Duration"] = show_anom["duration_sec"].apply(fmt_dur_hms)
                        show_anom["Type"] = show_anom["call_type"].map(CALL_LABELS).fillna(show_anom["call_type"])
                        nc_a = get_num_col(show_anom)
                        display_cols = ["Time"] + ([nc_a] if nc_a else []) + ["Duration","Type"]
                        st.dataframe(show_anom[display_cols].rename(columns={nc_a:"Number"} if nc_a else {}), use_container_width=True, height=min(380,len(show_anom)*36+40))
                        st.download_button(f"Export anomaly data", show_anom.to_csv(index=False).encode(), f"anomaly_{a['type'][:10].replace(' ','_')}.csv", "text/csv", key=f"dl_{a['type'][:10]}")

    with t5:
        st.markdown('<div class="sh">Per-Subscriber Call Detail</div>', unsafe_allow_html=True)
        if not num_col:
            st.markdown('<div class="abox abox-cyan">No contact data available.</div>', unsafe_allow_html=True)
        else:
            contacts_vc = df[num_col].value_counts()
            def fmt_contact_opt(x):
                name = book.get(re.sub(r'[\s\-\.\(\)]','',str(x)), None)
                cnt = contacts_vc.get(x, 0)
                dur_t = fmt_dur(int(df[df[num_col]==x]["duration_sec"].sum()))
                if name: return f"{name}  [{x}]  ({cnt}x · {dur_t})"
                return f"{x}  ({cnt}x · {dur_t})"
            sel_contact = st.selectbox("Select Subscriber", contacts_vc.index.tolist(), format_func=fmt_contact_opt)
            if sel_contact:
                cdf = df[df[num_col] == sel_contact].copy().sort_values("timestamp")
                disp_name = book.get(re.sub(r'[\s\-\.\(\)]','',str(sel_contact)), str(sel_contact))
                total_dur_c = int(cdf["duration_sec"].sum())
                voice_cnt_c = int(cdf["call_type"].str.contains("VOICE",na=False).sum()) if "call_type" in cdf.columns else 0
                sms_cnt_c   = int(cdf["call_type"].str.contains("SMS",  na=False).sum()) if "call_type" in cdf.columns else 0
                night_cnt_c = int(((cdf["timestamp"].dt.hour < 5) | (cdf["timestamp"].dt.hour >= 23)).sum())
                first_c = cdf["timestamp"].min(); last_c = cdf["timestamp"].max()
                span_c = (last_c-first_c).days

                st.markdown(f"""
<div class="panel">
  <div style="font-family:var(--mono);font-size:0.85rem;color:var(--cyan);margin-bottom:4px">{sel_contact}</div>
  {f'<div style="font-family:var(--display);font-size:0.78rem;color:var(--amber);margin-bottom:12px">{disp_name}</div>' if disp_name!=str(sel_contact) else ''}
  <div style="display:flex;flex-wrap:wrap;gap:20px;font-family:var(--mono);font-size:0.75rem">
    <div><span style="color:var(--t3)">RECORDS</span><br><b style="color:var(--t1);font-size:1.1rem">{len(cdf)}</b></div>
    <div><span style="color:var(--t3)">VOICE</span><br><b style="color:var(--cyan);font-size:1.1rem">{voice_cnt_c}</b></div>
    <div><span style="color:var(--t3)">SMS</span><br><b style="color:var(--green);font-size:1.1rem">{sms_cnt_c}</b></div>
    <div><span style="color:var(--t3)">DURATION</span><br><b style="color:var(--amber);font-size:1.1rem">{fmt_dur(total_dur_c)}</b></div>
    <div><span style="color:var(--t3)">LATE NIGHT</span><br><b style="color:var(--red);font-size:1.1rem">{night_cnt_c}</b></div>
    <div><span style="color:var(--t3)">FIRST CONTACT</span><br><b>{first_c.strftime("%d %b %Y") if pd.notna(first_c) else "?"}</b></div>
    <div><span style="color:var(--t3)">LAST CONTACT</span><br><b>{last_c.strftime("%d %b %Y") if pd.notna(last_c) else "?"}</b></div>
    <div><span style="color:var(--t3)">SPAN</span><br><b>{span_c}d</b></div>
  </div>
</div>""", unsafe_allow_html=True)

                cv1, cv2 = st.columns([1,6])
                with cv1: cview = st.selectbox("Filter", ["All","Late Night","Voice","SMS"], key="cview")
                cdf_show = cdf.copy()
                if cview == "Late Night": cdf_show = cdf_show[(cdf_show["timestamp"].dt.hour<5)|(cdf_show["timestamp"].dt.hour>=23)]
                elif cview == "Voice" and "call_type" in cdf_show.columns: cdf_show = cdf_show[cdf_show["call_type"].str.contains("VOICE",na=False)]
                elif cview == "SMS" and "call_type" in cdf_show.columns: cdf_show = cdf_show[cdf_show["call_type"].str.contains("SMS",na=False)]
                else: cdf_show = cdf_show.sort_values("timestamp", ascending=False)

                st.markdown('<div style="background:var(--bg2);border:1px solid var(--border);border-radius:var(--r2);padding:4px 14px;max-height:440px;overflow-y:auto">', unsafe_allow_html=True)
                for _, r in cdf_show.iterrows():
                    ts_s = r["timestamp"].strftime("%d %b %Y  %H:%M:%S") if pd.notna(r["timestamp"]) else "?"
                    hr = r["timestamp"].hour if pd.notna(r["timestamp"]) else 0
                    is_night = (hr < 5 or hr >= 23)
                    ct = r.get("call_type","MO_VOICE"); ct_label = CALL_LABELS.get(ct,ct); ct_color = TYPE_COLORS.get(ct,"#3A5570")
                    night_flag = " [NIGHT]" if is_night else ""
                    st.markdown(f'<div class="rec-row"><span class="rec-time" style="color:{"var(--red)" if is_night else "var(--t3)"}">{ts_s}{night_flag}</span><span class="rec-type"><span class="bd" style="color:{ct_color};border-color:{ct_color}30;background:{ct_color}10;font-size:0.6rem">{ct_label}</span></span><span class="rec-dur">{fmt_dur_hms(r["duration_sec"])}</span></div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

                st.markdown('<div class="sh" style="margin-top:14px">Contact Activity Timeline</div>', unsafe_allow_html=True)
                fig_ct = px.scatter(cdf, x="timestamp", y="duration_sec", color="call_type" if "call_type" in cdf.columns else None,
                    size="duration_sec", size_max=16, color_discrete_map=TYPE_COLORS, template="plotly_dark")
                fig_ct.update_layout(**_dark_layout(height=240, legend=dict(orientation="h",y=1.05,font_size=9)))
                st.plotly_chart(fig_ct, use_container_width=True)
                st.download_button(f"Export records for {sel_contact}", cdf.to_csv(index=False).encode(), f"calls_{re.sub(r'[^0-9]','',str(sel_contact))}.csv", "text/csv")

    with t6:
        st.markdown('<div class="sh">Communication Network Graph</div>', unsafe_allow_html=True)
        if not num_col:
            st.markdown('<div class="abox abox-cyan">No contact data available.</div>', unsafe_allow_html=True)
        else:
            src_col = "caller" if "caller" in df.columns else None
            if src_col:
                edges = df.groupby([src_col,num_col]).size().reset_index(name="w").sort_values("w",ascending=False).head(80)
            else:
                edges = df.groupby([num_col]).size().reset_index(name="w"); edges["src"] = "Subject"; src_col = "src"
            if edges.empty or len(edges) < 2:
                st.markdown('<div class="abox abox-cyan">Insufficient connections for graph visualization.</div>', unsafe_allow_html=True)
            else:
                all_nodes = list(set(edges[src_col].tolist()+edges[num_col].tolist()))
                nc = Counter()
                for _, r in edges.iterrows(): nc[r[src_col]] += r["w"]; nc[r[num_col]] += r["w"]
                mx_nc = max(nc.values()) if nc else 1
                hub = max(nc, key=nc.get)
                hub_nodes = [n for n in all_nodes if n != hub]
                n_contacts = max(len(hub_nodes), 1)
                angs = [2*math.pi*i/n_contacts for i in range(n_contacts)]
                pos = {hub:(0,0)}
                for i, n in enumerate(hub_nodes): pos[n] = (math.cos(angs[i]), math.sin(angs[i]))
                traces = []
                wmax = max(edges["w"].max(), 1)
                for _, r in edges.iterrows():
                    s = r[src_col]; t = r[num_col]
                    if s not in pos or t not in pos: continue
                    x0,y0 = pos[s]; x1,y1 = pos[t]
                    alpha = min(0.7, 0.1+r["w"]/wmax*0.6)
                    width = max(0.5, r["w"]/wmax*5)
                    traces.append(go.Scatter(x=[x0,x1,None], y=[y0,y1,None], mode="lines",
                        line=dict(width=width, color=f"rgba(0,255,179,{alpha:.2f})"), hoverinfo="none"))
                nx_ = [pos[n][0] for n in all_nodes]; ny_ = [pos[n][1] for n in all_nodes]
                sizes = [max(10, nc.get(n,1)/mx_nc*50) for n in all_nodes]
                colors = ["#FF3366" if n==hub else ("#FFD700" if nc.get(n,0)>mx_nc*0.3 else "#00FFB3") for n in all_nodes]
                labels_ = [book.get(re.sub(r'[\s\-\.\(\)]','',str(n)),str(n))[-12:] for n in all_nodes]
                hover_ = [f"<b>{book.get(re.sub(r'[\s\-\.\(\)]','',str(n)),str(n))}</b><br>{n}<br>{nc.get(n,0)} interactions" for n in all_nodes]
                node_tr = go.Scatter(x=nx_, y=ny_, mode="markers+text", text=labels_,
                    textposition="top center", textfont=dict(size=8, color="#3A5570", family="Share Tech Mono"),
                    marker=dict(size=sizes, color=colors, line=dict(width=1.5, color="#030508"), opacity=.9),
                    hovertext=hover_, hoverinfo="text")
                fig_n = go.Figure(data=traces+[node_tr])
                fig_n.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                    showlegend=False, hovermode="closest", margin=dict(l=0,r=0,t=0,b=0), height=480,
                    xaxis=dict(showgrid=False,zeroline=False,showticklabels=False,range=[-1.4,1.4]),
                    yaxis=dict(showgrid=False,zeroline=False,showticklabels=False,range=[-1.4,1.4]))
                st.plotly_chart(fig_n, use_container_width=True)
                st.markdown('<div style="font-family:var(--mono);font-size:0.62rem;color:var(--t3)"><span style="color:var(--red)">█</span> Hub &nbsp; <span style="color:var(--amber)">█</span> Frequent &nbsp; <span style="color:var(--green)">█</span> Other</div>', unsafe_allow_html=True)

    with t7:
        st.markdown('<div class="sh">Subscriber Intelligence Database</div>', unsafe_allow_html=True)
        if num_col:
            vc5 = df[num_col].value_counts()
            voice5 = df[df["call_type"].str.contains("VOICE",na=False)] if "call_type" in df.columns else df
            sms5   = df[df["call_type"].str.contains("SMS",  na=False)] if "call_type" in df.columns else pd.DataFrame()
            rows_intel = []
            for num in vc5.index[:50]:
                n_df = df[df[num_col] == num]
                v_df = voice5[voice5[num_col] == num] if not voice5.empty else pd.DataFrame()
                s_df = sms5[sms5[num_col] == num]   if not sms5.empty else pd.DataFrame()
                tot_d = int(n_df["duration_sec"].sum()); max_d = int(v_df["duration_sec"].max()) if not v_df.empty and len(v_df)>0 else 0
                avg_d = int(v_df["duration_sec"].mean()) if not v_df.empty and len(v_df)>0 else 0
                first = n_df["timestamp"].min().strftime("%d %b %Y") if pd.notna(n_df["timestamp"].min()) else "?"
                last  = n_df["timestamp"].max().strftime("%d %b %Y") if pd.notna(n_df["timestamp"].max()) else "?"
                span  = (n_df["timestamp"].max()-n_df["timestamp"].min()).days if len(n_df)>1 else 0
                night_c2 = int(((n_df["timestamp"].dt.hour<5)|(n_df["timestamp"].dt.hour>=23)).sum())
                name_tag = book.get(re.sub(r'[\s\-\.\(\)]','',str(num)), "")
                rows_intel.append({"Name":name_tag,"Number":num,"Total":len(n_df),"Voice":len(v_df),"SMS":len(s_df),
                    "Total Duration":fmt_dur(tot_d),"Longest":fmt_dur(max_d),"Avg Duration":fmt_dur(avg_d),
                    "First":first,"Last":last,"Span(days)":span,"Night Calls":night_c2})
            if rows_intel:
                intel_df = pd.DataFrame(rows_intel)
                st.dataframe(intel_df, use_container_width=True, height=500)
                e1,e2,_ = st.columns([1,1,5])
                with e1: st.download_button("Export CSV", intel_df.to_csv(index=False).encode(), "contact_intel.csv", "text/csv")
                with e2:
                    susp = intel_df[intel_df["Night Calls"]>0].sort_values("Night Calls",ascending=False)
                    if not susp.empty: st.download_button("Night Activity CSV", susp.to_csv(index=False).encode(), "night_contacts.csv", "text/csv")


# ─────────────────────────────────────────────
#  PAGE: TOWER MAP
# ─────────────────────────────────────────────
def page_map():
    df = get_combined_df()
    dtype = st.session_state.get("device_type","android"); is_android = dtype == "android"; lac_tac = "LAC" if is_android else "TAC"
    st.markdown(f'<div class="ph"><div class="ph-eyebrow">// GEOSPATIAL INTELLIGENCE</div><div class="ph-title">Tower Location Map</div><div class="ph-sub">Real GPS via {lac_tac} / CID · Movement path analysis · Coverage radius overlay</div></div>', unsafe_allow_html=True)
    if df.empty or "latitude" not in df.columns:
        st.markdown('<div class="abox abox-cyan">No location data. Add tower records to enable geospatial mapping.</div>', unsafe_allow_html=True); return
    dfm = df.dropna(subset=["latitude","longitude"])
    if dfm.empty:
        st.markdown('<div class="abox abox-amber">No valid GPS coordinates in current dataset.</div>', unsafe_allow_html=True); return

    c1,c2,c3 = st.columns(3)
    with c1: tile = st.selectbox("Map Layer", ["Dark Matter","Positron","OpenStreetMap"])
    with c2: trail = st.checkbox("Movement Trail", True)
    with c3: cov = st.checkbox("Coverage Overlay", True)

    tiles_map = {"Dark Matter":"CartoDB dark_matter","Positron":"CartoDB positron","OpenStreetMap":"OpenStreetMap"}
    clat = dfm["latitude"].mean(); clng = dfm["longitude"].mean()
    m = folium.Map(location=[clat,clng], zoom_start=12, tiles=tiles_map.get(tile,"CartoDB dark_matter"))
    agg_d = {"visits":("timestamp","count"),"dur":("duration_sec","sum"),"lac":("lac","first"),"cid":("cell_id","first"),"mcc_v":("mcc","first"),"mnc_v":("mnc","first")}
    for opt,src in [("t_src","tower_source"),("t_range","tower_range")]:
        if src in dfm.columns: agg_d[opt] = (src,"first")
    grp = dfm.groupby(["latitude","longitude"]).agg(**agg_d).reset_index()
    mxv = grp["visits"].max()
    for _, r in grp.iterrows():
        hot = r["visits"] > mxv*0.5; rad = 8+(r["visits"]/mxv)*28
        is_real = "Live" in str(r.get("t_src",""))
        op_v = mnc_info(r["mcc_v"],r["mnc_v"])
        popup_html = f'<div style="font-family:monospace;background:#030508;color:#E8F0F8;padding:12px;border-radius:6px;border:1px solid rgba(0,255,179,0.2);min-width:180px;font-size:11px"><b style="color:#00FFB3">CELL TOWER</b><hr style="border-color:rgba(0,255,179,0.1);margin:5px 0"><table style="width:100%"><tr><td style="color:#3A5570">{lac_tac}</td><td><b>{r["lac"]}</b></td></tr><tr><td style="color:#3A5570">CID</td><td><b>{r["cid"]}</b></td></tr><tr><td style="color:#3A5570">Operator</td><td style="color:#00FFB3">{op_v}</td></tr><tr><td style="color:#3A5570">Visits</td><td style="color:#00B8FF;font-weight:700">{r["visits"]}</td></tr></table></div>'
        pin = "#FF3366" if hot else ("#00FFB3" if is_real else "#FFD700")
        folium.CircleMarker(location=[r["latitude"],r["longitude"]], radius=rad, color=pin, fill=True,
            fill_color=pin, fill_opacity=.5, weight=2,
            popup=folium.Popup(popup_html,max_width=220),
            tooltip=f"{lac_tac}:{r['lac']} | {r['visits']} visits").add_to(m)
        if cov and is_real and r.get("t_range",0) > 0:
            folium.Circle([r["latitude"],r["longitude"]], radius=int(r.get("t_range",500)), color=pin,
                fill=True, fill_color=pin, fill_opacity=.03, weight=1, dash_array="6").add_to(m)
    if trail and len(dfm) > 1:
        pts = dfm.sort_values("timestamp")[["latitude","longitude"]].dropna().values.tolist()
        folium.PolyLine(pts, color="#00FFB3", weight=1.5, opacity=0.2, dash_array="6").add_to(m)
    st_folium(m, width="stretch", height=560)


# ─────────────────────────────────────────────
#  PAGE: FORENSIC REPORT
# ─────────────────────────────────────────────
def page_report():
    df = get_combined_df()
    dtype = st.session_state.get("device_type","android"); is_android = dtype == "android"; lac_tac = "LAC" if is_android else "TAC"
    st.markdown('<div class="ph"><div class="ph-eyebrow">// AUTO-GENERATED INTELLIGENCE DOCUMENT</div><div class="ph-title">Forensic Report</div><div class="ph-sub">Comprehensive CDR intelligence analysis · Restricted distribution</div></div>', unsafe_allow_html=True)
    if df.empty:
        st.markdown('<div class="abox abox-cyan">No data loaded. Ingest CDR data to generate report.</div>', unsafe_allow_html=True); return

    book = get_contacts()
    n = len(df)
    vc = int(df["call_type"].str.contains("VOICE",na=False).sum()) if "call_type" in df.columns else 0
    sc = int(df["call_type"].str.contains("SMS",  na=False).sum()) if "call_type" in df.columns else 0
    dc = int(df["call_type"].str.contains("DATA", na=False).sum()) if "call_type" in df.columns else 0
    dur = int(df["duration_sec"].sum())
    ds = df["timestamp"].min().strftime("%d %B %Y"); de = df["timestamp"].max().strftime("%d %B %Y")
    span = max(1,(df["timestamp"].max()-df["timestamp"].min()).days)
    num_col = get_num_col(df)
    uc = df[num_col].nunique() if num_col else 0
    tw = df["cell_id"].nunique() if "cell_id" in df.columns else 0
    lacs_u = df["lac"].nunique() if "lac" in df.columns else 0
    mcc_v = str(df["mcc"].iloc[0]) if "mcc" in df.columns else "N/A"
    mnc_v = str(df["mnc"].iloc[0]) if "mnc" in df.columns else "N/A"
    inf = mcc_info(mcc_v); op = mnc_info(mcc_v,mnc_v)
    imei_v = str(df["imei"].iloc[0]) if "imei" in df.columns else "N/A"
    caller_v = str(df["caller"].mode()[0]) if "caller" in df.columns else "N/A"
    night_c = len(df[(df["timestamp"].dt.hour<5)|(df["timestamp"].dt.hour>=23)])
    drop_c = len(df[df["call_drop"]==True]) if "call_drop" in df.columns else 0
    roam_c = len(df[df["roaming"]==True]) if "roaming" in df.columns else 0
    rid = hashlib.md5(f"{n}{ds}{de}".encode()).hexdigest()[:8].upper()
    lv_v = luhn(imei_v); lv_str = "VALID" if lv_v else "INVALID" if lv_v==False else "N/A"
    real_c = len(df[df["tower_source"].str.contains("Live",na=False)]) if "tower_source" in df.columns else 0
    radio_v = str(df["radio_type"].mode()[0]) if "radio_type" in df.columns else "N/A"
    avg_daily = n/span; diversity = round(uc/n,3) if n>0 else 0
    voice_df2 = df[df["duration_sec"]>0].copy()
    most_called = "N/A"; most_called_cnt = 0
    if num_col:
        mc_s = df[num_col].value_counts()
        if len(mc_s): most_called = mc_s.index[0]; most_called_cnt = mc_s.iloc[0]
    longest_dur = "—"; longest_num = "—"; longest_dur_hms = "—"
    if not voice_df2.empty and voice_df2["duration_sec"].max()>0:
        lr = voice_df2.loc[voice_df2["duration_sec"].idxmax()]
        longest_dur = fmt_dur(lr["duration_sec"]); longest_dur_hms = fmt_dur_hms(lr["duration_sec"])
        longest_num = str(lr.get("callee") or lr.get("called_number","?"))
    flash_c = len(voice_df2[(voice_df2["duration_sec"]>0)&(voice_df2["duration_sec"]<10)]) if not voice_df2.empty else 0
    anom = sum([night_c>2, drop_c>3, roam_c>0, flash_c>2])
    tlevel = "CRITICAL" if anom>=4 else "HIGH" if anom>=3 else "MEDIUM" if anom>=1 else "LOW"
    tl_col = "#FF3366" if tlevel in ["CRITICAL","HIGH"] else "#FFD700" if tlevel=="MEDIUM" else "#00FFB3"
    peak_hr = df.groupby(df["timestamp"].dt.hour).size().idxmax() if n>0 else 0
    peak_hr_str = f"{peak_hr:02d}:00–{peak_hr:02d}:59"
    mo_cnt = int(df["call_type"].str.startswith("MO").sum()) if "call_type" in df.columns else 0
    mt_cnt = int(df["call_type"].str.startswith("MT").sum()) if "call_type" in df.columns else 0
    initiation_ratio = round(mo_cnt/(mo_cnt+mt_cnt)*100) if (mo_cnt+mt_cnt)>0 else 0
    morning   = len(df[(df["timestamp"].dt.hour>=6)&(df["timestamp"].dt.hour<12)])
    afternoon = len(df[(df["timestamp"].dt.hour>=12)&(df["timestamp"].dt.hour<18)])
    evening   = len(df[(df["timestamp"].dt.hour>=18)&(df["timestamp"].dt.hour<23)])
    weekend_c = len(df[df["timestamp"].dt.dayofweek>=5])
    most_called_disp = book.get(re.sub(r'[\s\-\.\(\)]','',str(most_called)), str(most_called))
    longest_num_disp = book.get(re.sub(r'[\s\-\.\(\)]','',str(longest_num)), str(longest_num))

    # Report header
    st.markdown(f"""
<div style="background:var(--bg2);border:1px solid var(--border2);border-radius:var(--r2);padding:28px 32px;margin-bottom:20px;position:relative;overflow:hidden">
  <div style="position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,var(--green),var(--cyan),var(--violet))"></div>
  <div style="position:absolute;top:0;right:0;bottom:0;width:1px;background:linear-gradient(180deg,var(--green),transparent)"></div>
  <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:24px;flex-wrap:wrap;gap:12px">
    <div>
      <div style="font-family:var(--mono);font-size:0.58rem;color:var(--green);letter-spacing:0.2em;margin-bottom:8px">// CDR FORENSIC ANALYSIS REPORT</div>
      <div style="font-family:var(--display);font-size:1.6rem;font-weight:800;color:var(--t1);letter-spacing:-0.02em;line-height:1">INTELLIGENCE SUMMARY</div>
      <div style="font-family:var(--mono);font-size:0.6rem;color:var(--t3);margin-top:6px;letter-spacing:0.1em">MULTIMEDIA & NETWORK FORENSICS · RESTRICTED DISTRIBUTION</div>
    </div>
    <div style="text-align:right;font-family:var(--mono);font-size:0.7rem;color:var(--t3)">
      <div>REF: <span style="color:var(--t1)">#{rid}</span></div>
      <div style="margin-top:3px">{datetime.now().strftime("%d %b %Y  %H:%M")}</div>
      <div style="margin-top:3px">{'ANDROID' if is_android else 'iPHONE'} SESSION</div>
      <div style="margin-top:6px"><span class="bd bd-r">RESTRICTED</span></div>
    </div>
  </div>
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(110px,1fr));gap:8px">
    {''.join([f'<div style="background:rgba({r},{g},{b},0.05);border:1px solid rgba({r},{g},{b},0.12);border-radius:var(--r1);padding:10px 8px;text-align:center"><div style="font-family:var(--display);font-size:1rem;font-weight:700;color:rgb({r},{g},{b})">{val}</div><div style="font-family:var(--mono);color:var(--t3);font-size:0.52rem;text-transform:uppercase;letter-spacing:1.5px;margin-top:3px">{lbl}</div></div>' for r,g,b,val,lbl in [(0,255,179,f"{n:,}","Records"),(0,184,255,f"{vc:,}","Voice"),(123,97,255,f"{sc:,}","SMS"),(255,215,0,fmt_dur(dur),"Duration"),(255,51,102,longest_dur_hms,"Longest"),(int(tl_col[1:3],16),int(tl_col[3:5],16),int(tl_col[5:7],16),tlevel,"Threat")]])}
  </div>
</div>""", unsafe_allow_html=True)

    r1, r2 = st.columns(2)
    with r1:
        st.markdown(f"""
<div class="panel">
  <div class="panel-title">01 — SUBSCRIBER IDENTITY</div>
  <table class="dt">
    <tr><th>MSISDN</th><td style="color:var(--cyan)">{caller_v}</td></tr>
    <tr><th>IMEI</th><td>{imei_v}</td></tr>
    <tr><th>IMEI Luhn</th><td style="color:{'var(--green)' if lv_v else 'var(--red)'}">{lv_str}</td></tr>
    <tr><th>MCC / MNC</th><td>{mcc_v} / {mnc_v}</td></tr>
    <tr><th>Operator</th><td style="color:var(--cyan)">{op}</td></tr>
    <tr><th>Country</th><td>{inf["country"]} · {inf["region"]}</td></tr>
    <tr><th>Device Type</th><td><span class="bd">{'ANDROID' if is_android else 'iPHONE'}</span></td></tr>
    <tr><th>Radio Standard</th><td><span class="bd">{radio_v}</span></td></tr>
    <tr><th>Roaming</th><td style="color:{'var(--red)' if roam_c>0 else 'var(--green)'}">{roam_c} {'— DETECTED' if roam_c>0 else '— NONE'}</td></tr>
    <tr><th>Identity Records</th><td style="color:var(--green)">{len(book)}</td></tr>
  </table>
</div>""", unsafe_allow_html=True)

    with r2:
        st.markdown(f"""
<div class="panel">
  <div class="panel-title">02 — TRAFFIC SUMMARY</div>
  <table class="dt">
    <tr><th>Period</th><td>{ds} — {de}</td></tr>
    <tr><th>Span</th><td>{span} days</td></tr>
    <tr><th>Total Records</th><td style="color:var(--t1);font-weight:600">{n:,}</td></tr>
    <tr><th>Voice Events</th><td style="color:var(--cyan)">{vc:,}</td></tr>
    <tr><th>SMS Events</th><td style="color:var(--green)">{sc:,}</td></tr>
    <tr><th>Data Sessions</th><td>{dc:,}</td></tr>
    <tr><th>Talk Duration</th><td style="color:var(--amber)">{fmt_dur(dur)}</td></tr>
    <tr><th>Avg Records/Day</th><td>{avg_daily:.1f}</td></tr>
    <tr><th>Unique Contacts</th><td style="color:var(--cyan)">{uc}</td></tr>
    <tr><th>Contact Diversity</th><td>{diversity:.3f}</td></tr>
    <tr><th>Weekend / Weekday</th><td>{weekend_c} / {n-weekend_c}</td></tr>
    <tr><th>Unique {lac_tac}s</th><td>{lacs_u}</td></tr>
    <tr><th>Unique Cell IDs</th><td>{tw}</td></tr>
    <tr><th>Live GPS Towers</th><td style="color:var(--green)">{real_c}</td></tr>
  </table>
</div>""", unsafe_allow_html=True)

    st.markdown(f"""
<div class="panel">
  <div class="panel-title">03 — KEY CONTACT INTELLIGENCE</div>
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:16px;margin-bottom:20px">
    <div><div style="font-family:var(--mono);font-size:0.58rem;color:var(--t3);letter-spacing:0.15em;margin-bottom:6px">MOST CONTACTED</div><div style="font-family:var(--mono);color:var(--cyan);font-size:0.85rem">{most_called_disp}</div><div style="font-family:var(--body);color:var(--t3);font-size:0.72rem;margin-top:2px">{most_called_cnt} interactions</div></div>
    <div><div style="font-family:var(--mono);font-size:0.58rem;color:var(--t3);letter-spacing:0.15em;margin-bottom:6px">LONGEST CALL</div><div style="font-family:var(--mono);color:var(--amber);font-size:0.85rem">{longest_dur_hms}</div><div style="font-family:var(--body);color:var(--t3);font-size:0.72rem;margin-top:2px">{longest_dur} with {longest_num_disp[-16:]}</div></div>
    <div><div style="font-family:var(--mono);font-size:0.58rem;color:var(--t3);letter-spacing:0.15em;margin-bottom:6px">LATE-NIGHT EVENTS</div><div style="font-family:var(--mono);color:{'var(--red)' if night_c>0 else 'var(--green)'};font-size:0.85rem">{night_c} events</div><div style="font-family:var(--body);color:var(--t3);font-size:0.72rem;margin-top:2px">{'23:00–05:00 window' if night_c>0 else 'None detected'}</div></div>
  </div>
  <div style="font-family:var(--mono);font-size:0.58rem;color:var(--t3);letter-spacing:0.15em;margin-bottom:12px">TOP CORRESPONDENTS</div>""", unsafe_allow_html=True)

    if num_col:
        top5 = df[num_col].value_counts().head(5)
        for num, cnt in top5.items():
            pct = cnt/n*100; n_df2 = df[df[num_col]==num]; dur_t = fmt_dur(int(n_df2["duration_sec"].sum()))
            night_n = int(((n_df2["timestamp"].dt.hour<5)|(n_df2["timestamp"].dt.hour>=23)).sum())
            disp_name = book.get(re.sub(r'[\s\-\.\(\)]','',str(num)), str(num))
            night_badge = f'<span class="bd bd-r" style="font-size:0.58rem">{night_n} NIGHT</span>' if night_n>0 else ""
            st.markdown(f'<div style="display:flex;align-items:center;gap:10px;margin-bottom:8px"><div style="font-family:var(--mono);font-size:0.7rem;color:var(--t1);min-width:150px">{disp_name}</div><div style="flex:1;background:rgba(0,255,179,0.04);border-radius:2px;height:3px"><div style="width:{pct:.1f}%;background:linear-gradient(90deg,var(--green),var(--cyan));height:100%;border-radius:2px"></div></div><span class="bd">{cnt}x</span><span style="font-family:var(--mono);color:var(--amber);font-size:0.68rem;min-width:70px">{dur_t}</span>{night_badge}</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    anom_items = []
    if night_c > 2:  anom_items.append(("HIGH","Late-Night Activity",f"{night_c} calls between 23:00–05:00."))
    if drop_c > 3:   anom_items.append(("MEDIUM","Elevated Drop Rate",f"{drop_c} call drop events recorded."))
    if roam_c > 0:   anom_items.append(("HIGH","Roaming Detected",f"{roam_c} events on foreign PLMN."))
    if flash_c > 2:  anom_items.append(("HIGH","Flash Calls Detected",f"{flash_c} calls under 10 seconds."))
    sc_map_c = {"HIGH":"#FFD700","MEDIUM":"#7B61FF","LOW":"#00FFB3","CRITICAL":"#FF3366"}
    anom_html2 = "".join([f'<div style="display:flex;gap:12px;padding:9px 0;border-bottom:1px solid var(--border)"><div style="min-width:65px;font-family:var(--mono);font-size:0.58rem;font-weight:700;color:{sc_map_c.get(sev,"#888")};padding-top:2px;letter-spacing:0.08em">{sev}</div><div><div style="font-family:var(--display);font-weight:600;font-size:0.82rem;margin-bottom:2px;color:{sc_map_c.get(sev,"#888")}">{atype}</div><div style="font-family:var(--body);color:var(--t2);font-size:0.76rem">{detail}</div></div></div>' for sev,atype,detail in anom_items])
    if not anom_html2: anom_html2 = '<div style="font-family:var(--mono);color:var(--green);font-size:0.72rem;padding:8px 0">CLEAR — No significant anomalies detected.</div>'

    st.markdown(f"""
<div class="panel">
  <div style="display:flex;justify-content:space-between;align-items:center;padding-bottom:10px;border-bottom:1px solid var(--border);margin-bottom:14px">
    <div class="panel-title" style="margin-bottom:0">04 — THREAT ASSESSMENT</div>
    <span class="bd" style="color:{tl_col};border-color:{tl_col}30;background:{tl_col}10">THREAT: {tlevel}</span>
  </div>
  <div style="font-family:var(--body);color:var(--t2);font-size:0.82rem;margin-bottom:12px">{anom} anomaly pattern(s) identified — threat classification: <b style="color:{tl_col}">{tlevel}</b></div>
  {anom_html2}
</div>""", unsafe_allow_html=True)

    st.markdown(f"""
<div class="panel">
  <div class="panel-title">05 — BEHAVIORAL PROFILE</div>
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:16px">
    <div><div style="font-family:var(--mono);font-size:0.58rem;color:var(--t3);letter-spacing:0.15em;margin-bottom:6px">CALL INITIATION</div><div style="font-family:var(--display);color:var(--t1);font-size:1.1rem;font-weight:600">{initiation_ratio}%</div><div style="font-family:var(--body);color:var(--t3);font-size:0.7rem">Outgoing ({mo_cnt} MO / {mt_cnt} MT)</div></div>
    <div><div style="font-family:var(--mono);font-size:0.58rem;color:var(--t3);letter-spacing:0.15em;margin-bottom:6px">PEAK HOUR</div><div style="font-family:var(--mono);color:var(--amber);font-size:1rem;font-weight:600">{peak_hr_str}</div></div>
    <div><div style="font-family:var(--mono);font-size:0.58rem;color:var(--t3);letter-spacing:0.15em;margin-bottom:6px">TIME DISTRIBUTION</div><div style="font-family:var(--body);color:var(--t2);font-size:0.76rem;line-height:1.9">Morning: <b>{morning}</b> · Afternoon: <b>{afternoon}</b><br>Evening: <b>{evening}</b> · Night: <b style="color:{'var(--red)' if night_c>0 else 'var(--t2)'}">{night_c}</b></div></div>
    <div><div style="font-family:var(--mono);font-size:0.58rem;color:var(--t3);letter-spacing:0.15em;margin-bottom:6px">NETWORK FOOTPRINT</div><div style="font-family:var(--body);color:var(--t2);font-size:0.76rem;line-height:1.9">{lac_tac}s: <b>{lacs_u}</b> · CIDs: <b>{tw}</b><br>Flash: <b style="color:{'var(--red)' if flash_c>0 else 'var(--t2)'}">{flash_c}</b> · Diversity: <b style="color:var(--amber)">{diversity:.3f}</b></div></div>
  </div>
</div>""", unsafe_allow_html=True)

    st.markdown(f'<div class="abox abox-cyan" style="font-size:0.7rem">Legal Notice — For authorized forensic use only. Unauthorized access or distribution is prohibited. Report #{rid} · {datetime.now().strftime("%d %b %Y")}.</div>', unsafe_allow_html=True)

    e1, e2, e3, _ = st.columns([1,1,1,3])
    with e1:
        st.download_button("Export CSV", df.to_csv(index=False).encode(), f"CDR_{rid}.csv", "text/csv")
    with e2:
        txt = f"""CDR FORENSIC REPORT #{rid}\n{'='*52}\nPeriod: {ds} — {de} ({span} days)\nRecords: {n:,}\nVoice: {vc:,} | SMS: {sc:,} | Data: {dc:,}\nTalk Time: {fmt_dur(dur)}\nAvg/Day: {avg_daily:.1f}\nUnique Contacts: {uc}\nThreat Level: {tlevel}\n\nKEY CONTACTS\nMost Contacted: {most_called_disp} ({most_called_cnt}x)\nLongest Call: {longest_dur_hms} ({longest_dur}) -> {longest_num_disp}\n\nANOMALIES\nLate Night: {night_c} | Flash Calls: {flash_c} | Call Drops: {drop_c} | Roaming: {roam_c}\n\nBEHAVIORAL\nPeak Hour: {peak_hr_str}\nOutgoing: {initiation_ratio}% ({mo_cnt} MO / {mt_cnt} MT)\nMorning: {morning} | Afternoon: {afternoon} | Evening: {evening} | Night: {night_c}\nWeekend: {weekend_c}\n"""
        st.download_button("Export TXT", txt.encode(), f"Report_{rid}.txt", "text/plain")
    with e3:
        st.button("Open Analytics", use_container_width=True, key="rep_to_ana", on_click=navigate_to, args=("Analytics",))


# ─────────────────────────────────────────────
#  PAGE: ALL RECORDS
# ─────────────────────────────────────────────
def page_all_records():
    df = get_combined_df()
    st.markdown('<div class="ph"><div class="ph-eyebrow">// RAW DATA</div><div class="ph-title">All Records</div><div class="ph-sub">Complete CDR dataset — filter, search, and export</div></div>', unsafe_allow_html=True)
    if df.empty:
        st.markdown('<div class="abox abox-cyan">No records in current session.</div>', unsafe_allow_html=True); return

    book = get_contacts()
    c1,c2,c3,c4 = st.columns([2,2,2,2])
    with c1:
        ct_opts = ["All"] + sorted(df["call_type"].unique().tolist()) if "call_type" in df.columns else ["All"]
        ft = st.selectbox("Event Type", ct_opts)
    with c2:
        mn_v, mx_v = df["timestamp"].min().date(), df["timestamp"].max().date()
        dr = st.date_input("Date Range", value=(mn_v,mx_v), min_value=mn_v, max_value=mx_v)
    with c3: q = st.text_input("Search", placeholder="Number / name / type")
    with c4: view_opt = st.selectbox("Duration Format", ["Seconds","Minutes","HH:MM:SS"], key="allrec_dur")

    filt = df.copy()
    if ft != "All" and "call_type" in filt.columns: filt = filt[filt["call_type"] == ft]
    if len(dr) == 2: filt = filt[(filt["timestamp"].dt.date >= dr[0]) & (filt["timestamp"].dt.date <= dr[1])]
    if q: filt = filt[filt.apply(lambda r: q.lower() in str(r.to_dict()).lower(), axis=1)]

    num_col = get_num_col(filt)
    if num_col and book:
        filt["Contact Name"] = filt[num_col].apply(lambda x: book.get(re.sub(r'[\s\-\.\(\)]','',str(x)), ""))
    if view_opt == "Minutes": filt["duration_display"] = filt["duration_sec"].apply(lambda x: round(x/60,2))
    elif view_opt == "HH:MM:SS": filt["duration_display"] = filt["duration_sec"].apply(fmt_dur_hms)
    else: filt["duration_display"] = filt["duration_sec"]

    st.markdown(f'<div style="font-family:var(--mono);color:var(--t3);font-size:0.7rem;margin-bottom:10px"><span style="color:var(--green)">{len(filt):,}</span> / {len(df):,} records matching filter</div>', unsafe_allow_html=True)
    e1, _ = st.columns([1,7])
    with e1: st.download_button("Export CSV", filt.to_csv(index=False).encode(), "records.csv", "text/csv")
    base_cols = [c for c in ["call_id","Contact Name","timestamp","caller","callee","called_number","call_type","duration_display","mcc","mnc","lac","cell_id","radio_type","latitude","longitude","tower_source"] if c in filt.columns]
    st.dataframe(filt[base_cols].rename(columns={"duration_display":f"Duration ({view_opt})"}), use_container_width=True, height=540)


# ─────────────────────────────────────────────
#  TOP NAVIGATION BAR (Replaces Sidebar)
# ─────────────────────────────────────────────
def build_top_nav():
    """Build top navigation bar with dropdown menu"""
    
    # Initialize session state
    if "main_nav" not in st.session_state:
        st.session_state["main_nav"] = NAV_OPTIONS[0]
    if st.session_state["main_nav"] not in NAV_OPTIONS:
        st.session_state["main_nav"] = NAV_OPTIONS[0]
    
    # Top bar HTML/CSS
    st.markdown("""
    <style>
    .top-nav-bar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: linear-gradient(90deg, rgba(6,12,18,0.95) 0%, rgba(10,20,35,0.9) 100%);
        border-bottom: 1px solid rgba(0,255,179,0.15);
        padding: 8px 20px;
        margin: -16px -16px 12px -16px;
        gap: 20px;
        flex-wrap: wrap;
    }
    .top-nav-brand {
        display: flex;
        align-items: center;
        gap: 10px;
        font-family: 'Exo 2', sans-serif;
        font-weight: 800;
        color: #E8F0F8;
        font-size: 0.9rem;
        letter-spacing: 0.05em;
    }
    .top-nav-brand svg {
        width: 24px;
        height: 24px;
    }
    .top-nav-menu {
        display: flex;
        gap: 10px;
        align-items: center;
        flex: 1;
    }
    .nav-dropdown {
        min-width: 200px;
    }
    .nav-stats {
        display: flex;
        gap: 15px;
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.7rem;
        color: var(--t3);
    }
    .nav-stat-item {
        display: flex;
        align-items: center;
        gap: 5px;
    }
    .nav-stat-value {
        color: var(--green);
        font-weight: bold;
    }
    </style>
    <div class="top-nav-bar">
        <div class="top-nav-brand">
            <svg viewBox="0 0 24 24" fill="#00FFB3"><path d="M1.75 7.18L0 5.43C2.64 2.61 6.22 1 10 1s7.36 1.61 10 4.43l-1.75 1.75C16.16 4.77 13.18 3.5 10 3.5S3.84 4.77 1.75 7.18zm4.48 4.48L4.48 9.91C6.14 8.1 8.46 7 11.01 7S15.88 8.1 17.54 9.91l-1.75 1.75C14.5 10.23 12.83 9.5 11 9.5c-1.83 0-3.5.73-4.77 2.16zM11 13c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm-1 9h2v-3.27c.44-.14.85-.35 1.22-.63L17 20l1-1.73L14.2 16.7c.15-.55.2-1.12.1-1.7h3.7v-2H14.3c-.38-1.1-1.2-2-2.3-2.35V10h-2v.65C8.9 11 8.08 11.9 7.7 13H4v2h3.7c-.1.58-.05 1.15.1 1.7L5 18.27 6 20l3.78-1.9c.37.28.78.49 1.22.63V22z"/></svg>
            CDR FORENSICS
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation controls in columns
    col1, col2, col3, col4 = st.columns([2, 2, 1.5, 1.5])
    
    with col1:
        selected = st.selectbox(
            "Navigate to:",
            NAV_OPTIONS,
            index=NAV_OPTIONS.index(st.session_state["main_nav"]),
            key="top_nav_select",
            label_visibility="collapsed"
        )
        st.session_state["main_nav"] = selected
    
    with col2:
        dtype = st.session_state.get("device_type")
        if dtype:
            is_and = dtype == "android"
            mode_text = "ANDROID MODE" if is_and else "iPHONE MODE"
            mode_color = "#00FFB3" if is_and else "#00B8FF"
            st.markdown(f'<div style="background:rgba({("0,255,179" if is_and else "0,184,255")},0.1);border:1px solid rgba({("0,255,179" if is_and else "0,184,255")},0.3);border-radius:6px;padding:8px 12px;font-family:var(--mono);font-size:0.65rem;color:{mode_color};text-align:center;font-weight:bold">{mode_text}</div>', unsafe_allow_html=True)
    
    with col3:
        api_key = st.text_input(
            "API Key",
            value=st.session_state.get("ocid_key",""),
            placeholder="OpenCelliD token",
            type="password",
            label_visibility="collapsed"
        )
        if api_key:
            st.session_state["ocid_key"] = api_key
    
    with col4:
        if st.button("Clear Session", use_container_width=True, key="clear_session_btn"):
            for k in ["records","bill_records","tower_cache","bill_raw_text","contact_book"]:
                st.session_state.pop(k, None)
            st.rerun()
    
    # Session stats bar
    st.markdown('<div style="margin: 8px 0; height: 1px; background: rgba(0,255,179,0.08)"></div>', unsafe_allow_html=True)
    manual = len(st.session_state.get("records",[]))
    bill = len(st.session_state.get("bill_records", pd.DataFrame())) if isinstance(st.session_state.get("bill_records"), pd.DataFrame) else 0
    towers = len(st.session_state.get("tower_cache",{}))
    book_cnt = len(st.session_state.get("contact_book",{}))
    
    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.metric("Manual Records", manual, delta=None)
    with s2:
        st.metric("Bill Records", bill, delta=None)
    with s3:
        st.metric("Tower Cache", towers, delta=None)
    with s4:
        st.metric("Identities", book_cnt, delta=None)
    
    st.markdown('<div style="margin: 8px 0; height: 1px; background: rgba(0,255,179,0.08)"></div>', unsafe_allow_html=True)
    
    return st.session_state["main_nav"]


def main():
    inject_css()
    inject_sidebar_toggle_js()
    page = build_top_nav()

    if   "Device Selection" in page: page_device_select()
    elif "Tower Data"       in page: page_tower_entry()
    elif "Upload Bill"      in page: page_bill_upload()
    elif "Dashboard"        in page: page_dashboard()
    elif "Analytics"        in page: page_analytics()
    elif "Tower Map"        in page: page_map()
    elif "All Records"      in page: page_all_records()
    elif "Contact Manager"  in page: page_contact_manager()
    elif "Forensic Report"  in page: page_report()


if __name__ == "__main__":
    main()