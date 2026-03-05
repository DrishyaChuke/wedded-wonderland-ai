import streamlit as st
import openai
import time

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Wedded Wonderland · AI Content Engine",
    page_icon="💍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Brand CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Montserrat:wght@300;400;500;600&display=swap');

:root {
    --gold:       #C9A84C;
    --gold-light: #E8D5A3;
    --gold-dark:  #9A7B35;
    --cream:      #FAF7F2;
    --dark:       #1A1A1A;
    --mid:        #4A4A4A;
    --light:      #F2EDE4;
    --border:     #DDD0B8;
}

html, body, [class*="css"] {
    font-family: 'Montserrat', sans-serif;
    background-color: var(--cream);
    color: var(--dark);
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 4rem; max-width: 1100px; }

/* ── Hero header ── */
.hero {
    text-align: center;
    padding: 3rem 1rem 2rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 2.5rem;
}
.hero-tag {
    font-family: 'Montserrat', sans-serif;
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: var(--gold);
    margin-bottom: 0.75rem;
}
.hero h1 {
    font-family: 'Cormorant Garamond', serif;
    font-size: 3rem;
    font-weight: 300;
    color: var(--dark);
    line-height: 1.15;
    margin: 0 0 0.5rem;
}
.hero h1 span { color: var(--gold); font-style: italic; }
.hero-sub {
    font-size: 0.8rem;
    font-weight: 300;
    color: var(--mid);
    letter-spacing: 0.08em;
}

/* ── Tab bar ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 0;
    border-bottom: 1px solid var(--border);
    background: transparent;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Montserrat', sans-serif;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--mid);
    padding: 0.75rem 1.75rem;
    border: none;
    background: transparent;
}
.stTabs [aria-selected="true"] {
    color: var(--gold) !important;
    border-bottom: 2px solid var(--gold) !important;
    background: transparent !important;
}
.stTabs [data-baseweb="tab-panel"] { padding-top: 2rem; }

/* ── Cards ── */
.card {
    background: #fff;
    border: 1px solid var(--border);
    border-radius: 2px;
    padding: 2rem;
    margin-bottom: 1.5rem;
}
.card-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.3rem;
    font-weight: 400;
    color: var(--dark);
    margin-bottom: 0.25rem;
}
.card-sub {
    font-size: 0.7rem;
    color: var(--mid);
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid var(--light);
}

/* ── Output box ── */
.output-box {
    background: var(--light);
    border-left: 3px solid var(--gold);
    border-radius: 0 2px 2px 0;
    padding: 1.25rem 1.5rem;
    margin: 0.75rem 0;
    font-size: 0.85rem;
    line-height: 1.75;
    color: var(--dark);
    white-space: pre-wrap;
}
.output-label {
    font-size: 0.62rem;
    font-weight: 600;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--gold-dark);
    margin-bottom: 0.4rem;
}

/* ── Buttons ── */
.stButton > button {
    background: var(--gold) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 1px !important;
    font-family: 'Montserrat', sans-serif !important;
    font-size: 0.68rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
    padding: 0.65rem 2rem !important;
    transition: background 0.2s !important;
}
.stButton > button:hover {
    background: var(--gold-dark) !important;
}

/* ── Inputs ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
    border: 1px solid var(--border) !important;
    border-radius: 1px !important;
    background: #fff !important;
    font-family: 'Montserrat', sans-serif !important;
    font-size: 0.82rem !important;
    color: var(--dark) !important;
}
label {
    font-size: 0.68rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: var(--mid) !important;
}

/* ── ROI metric boxes ── */
.metric-row { display: flex; gap: 1rem; margin: 1.5rem 0; }
.metric-box {
    flex: 1;
    background: #fff;
    border: 1px solid var(--border);
    border-top: 3px solid var(--gold);
    padding: 1.25rem;
    text-align: center;
    border-radius: 0 0 2px 2px;
}
.metric-value {
    font-family: 'Cormorant Garamond', serif;
    font-size: 2.2rem;
    font-weight: 600;
    color: var(--gold-dark);
    line-height: 1;
}
.metric-label {
    font-size: 0.62rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--mid);
    margin-top: 0.4rem;
}

/* ── Divider ── */
.gold-divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 2rem 0;
}

/* ── Section label ── */
.section-label {
    font-size: 0.62rem;
    font-weight: 600;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: var(--gold);
    margin-bottom: 1.5rem;
}

/* ── Alert / info ── */
.info-bar {
    background: #fff8ee;
    border: 1px solid var(--gold-light);
    border-radius: 2px;
    padding: 0.75rem 1rem;
    font-size: 0.78rem;
    color: var(--mid);
    margin-bottom: 1.5rem;
}

/* Spinner color */
.stSpinner > div { border-top-color: var(--gold) !important; }
</style>
""", unsafe_allow_html=True)

# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-tag">✦ Powered by GPT-4 ✦</div>
    <h1>Wedded Wonderland<br><span>AI Content Engine</span></h1>
    <div class="hero-sub">Vendor Profiles &nbsp;·&nbsp; Blog Articles &nbsp;·&nbsp; ROI Calculator</div>
</div>
""", unsafe_allow_html=True)

# ── API Key input ─────────────────────────────────────────────────────────────
with st.expander("⚙️  Enter your OpenAI API Key", expanded=not st.session_state.get("api_key")):
    api_key_input = st.text_input(
        "OpenAI API Key",
        type="password",
        placeholder="sk-...",
        help="Your key is never stored. Get one at platform.openai.com",
    )
    if api_key_input:
        st.session_state["api_key"] = api_key_input
        st.success("✓ API key saved for this session")

def get_client():
    key = st.session_state.get("api_key", "")
    if not key:
        st.warning("Please enter your OpenAI API key above to generate content.")
        return None
    return openai.OpenAI(api_key=key)

def stream_gpt(system_prompt, user_prompt):
    client = get_client()
    if not client:
        return None
    try:
        with st.spinner("Generating…"):
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user",   "content": user_prompt},
                ],
                max_tokens=1200,
                temperature=0.78,
            )
        return response.choices[0].message.content
    except openai.AuthenticationError:
        st.error("Invalid API key. Please check and re-enter.")
    except openai.RateLimitError:
        st.error("Rate limit hit. Wait a moment and try again.")
    except Exception as e:
        st.error(f"Error: {e}")
    return None

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "💍  Vendor Profile Generator",
    "✍️  Blog Article Generator",
    "📊  ROI Calculator",
])

# ═══════════════════════════════════════════════════════════════════
# TAB 1 — VENDOR PROFILE GENERATOR
# ═══════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-label">✦ Vendor Profile Generator</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-bar">Transform basic vendor details into compelling directory listings, social bios, and SEO descriptions — instantly.</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Vendor Details</div><div class="card-sub">Fill in the basics</div>', unsafe_allow_html=True)
        business_name  = st.text_input("Business Name", placeholder="e.g. Bloom & Co. Florals")
        location       = st.text_input("Location", placeholder="e.g. Sydney, NSW")
        services       = st.text_area("Services Offered", placeholder="e.g. Bridal bouquets, ceremony arches, reception centrepieces, dried flower arrangements", height=90)
        style          = st.selectbox("Wedding Style", [
            "Luxury & Elegant", "Rustic & Bohemian", "Modern & Minimalist",
            "Romantic & Whimsical", "Destination & Tropical", "Garden & Floral",
            "Cultural & Traditional", "Eclectic & Maximalist"
        ])
        price_range    = st.selectbox("Price Range", [
            "Budget-Friendly ($)", "Mid-Range ($$)", "Premium ($$$)", "Luxury ($$$$)"
        ])
        unique_feature = st.text_input("One Unique Selling Point", placeholder="e.g. Only florist in Sydney using 100% locally grown blooms")
        generate_vendor = st.button("✦  Generate Vendor Content")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        if generate_vendor:
            if not all([business_name, location, services]):
                st.warning("Please fill in Business Name, Location, and Services.")
            else:
                system = """You are a luxury wedding brand copywriter for Wedded Wonderland — the world's leading destination wedding platform. 
Your writing is warm, aspirational, and elegant. You speak to high-net-worth couples seeking their dream wedding. 
Always write in second or third person about the vendor. Never use clichés like 'one-stop-shop' or 'passionate team'."""

                prompt = f"""Create vendor content for this wedding business listed on Wedded Wonderland:

Business: {business_name}
Location: {location}
Services: {services}
Style: {style}
Price Range: {price_range}
Unique Feature: {unique_feature}

Generate exactly these 4 sections with clear labels:

DIRECTORY LISTING (120 words): A compelling Wedded Wonderland profile description. Aspirational, story-led, luxury tone.

INSTAGRAM BIO (150 chars max): Punchy, emoji-friendly, includes location and a call to action.

SOCIAL CAPTION (3 options, each under 50 words): Ready-to-post Instagram captions with relevant hashtags.

SEO DESCRIPTION (80 words): Google-optimised paragraph naturally using keywords like 'wedding {services.split(',')[0].strip()} {location}'.
"""
                result = stream_gpt(system, prompt)
                if result:
                    sections = ["DIRECTORY LISTING", "INSTAGRAM BIO", "SOCIAL CAPTION", "SEO DESCRIPTION"]
                    current_section = None
                    current_text   = []
                    lines = result.split("\n")

                    output_map = {}
                    for line in lines:
                        matched = next((s for s in sections if s in line.upper()), None)
                        if matched:
                            if current_section:
                                output_map[current_section] = "\n".join(current_text).strip()
                            current_section = matched
                            current_text = []
                        elif current_section:
                            current_text.append(line)
                    if current_section:
                        output_map[current_section] = "\n".join(current_text).strip()

                    if output_map:
                        for section, text in output_map.items():
                            st.markdown(f'<div class="output-label">{section}</div><div class="output-box">{text}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="output-box">{result}</div>', unsafe_allow_html=True)

                    st.download_button(
                        "⬇  Download as .txt",
                        data=result,
                        file_name=f"{business_name.replace(' ','_')}_WW_content.txt",
                        mime="text/plain"
                    )
        else:
            st.markdown("""
            <div style="padding:3rem 1rem; text-align:center; color:#AAA;">
                <div style="font-size:2.5rem; margin-bottom:1rem;">💍</div>
                <div style="font-family:'Cormorant Garamond',serif; font-size:1.2rem; color:#C9A84C;">Fill in vendor details</div>
                <div style="font-size:0.75rem; margin-top:0.5rem;">Your generated content will appear here</div>
            </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════
# TAB 2 — BLOG ARTICLE GENERATOR
# ═══════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-label">✦ Blog Article Generator</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-bar">Generate SEO-optimised wedding articles for Wedded Wonderland\'s global content calendar in seconds.</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Article Brief</div><div class="card-sub">Define your content</div>', unsafe_allow_html=True)

        article_topic = st.text_input("Topic or Keyword", placeholder="e.g. Bali destination weddings 2025")
        destination   = st.text_input("Destination / Location Focus", placeholder="e.g. Ubud, Bali, Indonesia")
        audience      = st.selectbox("Target Audience", [
            "Couples Planning Their Wedding",
            "Wedding Vendors & Professionals",
            "Destination Wedding Planners",
            "International Couples",
            "Luxury Brides",
        ])
        tone          = st.selectbox("Tone", [
            "Romantic & Aspirational",
            "Practical & Helpful",
            "Luxurious & Editorial",
            "Fun & Conversational",
            "Expert & Authoritative",
        ])
        word_count    = st.select_slider("Target Word Count", options=[300, 400, 500, 600, 700, 800], value=500)
        cta_link      = st.text_input("Call-to-Action Link", placeholder="e.g. weddedwonderland.com/bali-vendors", value="weddedwonderland.com")
        generate_blog = st.button("✦  Generate Article")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        if generate_blog:
            if not article_topic:
                st.warning("Please enter a topic.")
            else:
                system = """You are the Senior Content Editor at Wedded Wonderland, the world's #1 luxury destination wedding platform with 3 million readers across 54 countries.
You write editorial wedding content that is beautiful, SEO-smart, and deeply useful to couples planning their dream wedding.
Your writing balances aspiration with practical advice. Always include the keyword naturally throughout."""

                prompt = f"""Write a {word_count}-word wedding blog article for Wedded Wonderland.

Topic: {article_topic}
Location Focus: {destination}
Audience: {audience}
Tone: {tone}
CTA Link: {cta_link}

Structure:
- HEADLINE: Compelling, SEO-friendly title
- INTRO: 2 sentences that hook the reader emotionally
- BODY: 3-4 subheadings with rich content, practical tips, and vivid imagery
- CLOSING: Warm sign-off with a clear CTA directing readers to {cta_link}

Use the keyword "{article_topic}" naturally 3-4 times. Do not use bullet points — write in flowing paragraphs."""

                result = stream_gpt(system, prompt)
                if result:
                    st.markdown(f'<div class="output-box" style="max-height:520px; overflow-y:auto;">{result}</div>', unsafe_allow_html=True)
                    st.download_button(
                        "⬇  Download Article as .txt",
                        data=result,
                        file_name=f"WW_article_{article_topic[:30].replace(' ','_')}.txt",
                        mime="text/plain"
                    )
        else:
            st.markdown("""
            <div style="padding:3rem 1rem; text-align:center; color:#AAA;">
                <div style="font-size:2.5rem; margin-bottom:1rem;">✍️</div>
                <div style="font-family:'Cormorant Garamond',serif; font-size:1.2rem; color:#C9A84C;">Define your article brief</div>
                <div style="font-size:0.75rem; margin-top:0.5rem;">Your generated article will appear here</div>
            </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════
# TAB 3 — ROI CALCULATOR
# ═══════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-label">✦ AI ROI Calculator</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-bar">Quantify the business impact of deploying this AI Content Engine across Wedded Wonderland\'s operations.</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Vendor Profile Savings</div><div class="card-sub">Directory listing operations</div>', unsafe_allow_html=True)
        vendors_per_month  = st.slider("New vendor profiles onboarded per month", 10, 500, 100, step=10)
        mins_per_profile   = st.slider("Minutes spent writing each profile manually", 15, 120, 45, step=5)
        copywriter_rate    = st.slider("Copywriter hourly rate (AUD $)", 30, 150, 65, step=5)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Blog Content Savings</div><div class="card-sub">Editorial & content marketing</div>', unsafe_allow_html=True)
        articles_per_week  = st.slider("Blog articles published per week", 1, 30, 10)
        mins_per_article   = st.slider("Minutes spent writing each article manually", 60, 300, 120, step=15)
        editor_rate        = st.slider("Editor / writer hourly rate (AUD $)", 40, 200, 85, step=5)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">AI Tool Costs</div><div class="card-sub">Estimated monthly spend</div>', unsafe_allow_html=True)
        api_cost_monthly   = st.slider("Estimated OpenAI API cost per month (AUD $)", 20, 500, 80, step=10)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        # ── Calculations ──
        profile_hours_saved  = (vendors_per_month * mins_per_profile) / 60
        profile_cost_saved   = profile_hours_saved * copywriter_rate

        articles_per_month   = articles_per_week * 4.33
        article_hours_saved  = (articles_per_month * mins_per_article) / 60
        article_cost_saved   = article_hours_saved * editor_rate

        total_hours_saved    = profile_hours_saved + article_hours_saved
        total_cost_saved     = profile_cost_saved + article_cost_saved
        net_roi              = total_cost_saved - api_cost_monthly
        roi_multiple         = total_cost_saved / api_cost_monthly if api_cost_monthly else 0
        annual_savings       = net_roi * 12

        st.markdown(f"""
        <div class="metric-row">
            <div class="metric-box">
                <div class="metric-value">{total_hours_saved:.0f}h</div>
                <div class="metric-label">Hours Saved / Month</div>
            </div>
            <div class="metric-box">
                <div class="metric-value">${total_cost_saved:,.0f}</div>
                <div class="metric-label">Labour Cost Saved / Month</div>
            </div>
        </div>
        <div class="metric-row">
            <div class="metric-box">
                <div class="metric-value">${net_roi:,.0f}</div>
                <div class="metric-label">Net Monthly ROI</div>
            </div>
            <div class="metric-box">
                <div class="metric-value">{roi_multiple:.1f}×</div>
                <div class="metric-label">Return on AI Spend</div>
            </div>
        </div>
        <div class="metric-row">
            <div class="metric-box" style="flex:1;">
                <div class="metric-value">${annual_savings:,.0f}</div>
                <div class="metric-label">Projected Annual Net Savings</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Summary</div><div class="card-sub">Business case</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="font-size:0.82rem; line-height:1.9; color:#4A4A4A;">
        By deploying the <strong>Wedded Wonderland AI Content Engine</strong>, the team can:<br><br>
        ✦ &nbsp;Generate <strong>{vendors_per_month} vendor profiles</strong> per month in minutes instead of {profile_hours_saved:.0f} hours<br>
        ✦ &nbsp;Publish <strong>{articles_per_month:.0f} blog articles</strong> per month with zero writer bottleneck<br>
        ✦ &nbsp;Free up <strong>{total_hours_saved:.0f} staff hours</strong> every month for high-value work<br>
        ✦ &nbsp;Save <strong>${total_cost_saved:,.0f}/month</strong> in labour costs against just <strong>${api_cost_monthly}/month</strong> in API spend<br>
        ✦ &nbsp;Deliver a <strong>{roi_multiple:.1f}× return</strong> on every dollar invested in AI tools<br><br>
        <em>This tool pays for itself within the first hour of use.</em>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding:3rem 0 1rem; border-top:1px solid #DDD0B8; margin-top:3rem;">
    <div style="font-family:'Cormorant Garamond',serif; font-size:1rem; color:#C9A84C; letter-spacing:0.1em;">
        Built for Wedded Wonderland · Gen AI Internship Application
    </div>
    <div style="font-size:0.65rem; color:#AAA; letter-spacing:0.15em; text-transform:uppercase; margin-top:0.5rem;">
        Drishya Lal Chuke · drishyachuke98@gmail.com
    </div>
</div>
""", unsafe_allow_html=True)
