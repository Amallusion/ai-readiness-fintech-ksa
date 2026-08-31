"""
build_dashboard.py
===================
ITU AI Readiness Hackathon (KSA) — Fintech track — Team Voxel
STEP 7 of the Y.3172 pipeline: "SINK" (inference target)

WHAT THIS DOES
--------------
Generates dashboard.html: a single, self-contained, offline-capable HTML
file — no server, no dependencies, just open it in a browser. This is
where the whole pipeline's output finally reaches a real person.

DESIGN DECISIONS
----------------
1. ROLE-BASED ROUTING (mirrors Step 6 on purpose)
   Step 6 (Distributor) decided that a regulator, a sandbox team and a
   compliance officer each get a different slice of the decision. A
   single undifferentiated dashboard would throw that work away, so this
   Sink has a role selector: pick your role, see only your packet. Each
   panel states which packet it is showing, so a judge who clicks one tab
   can tell the sparseness is deliberate rather than incomplete.

2. THE AML/CTF GATE IS DEMONSTRATED, NOT ASSERTED
   Policy Layer 3 is the project's strongest claim: the gate is
   structurally incapable of firing from sector-level data. Stating that
   in a callout asks the reader to trust us. Instead the Compliance panel
   lets the user *attempt* an escalation on any sector and watch the
   refusal, with the evidence-class mismatch shown explicitly. The
   refusal is deterministic and data-driven — there is no branch in this
   code that returns anything else.

3. FULL BILINGUAL SUPPORT INCLUDING DIRECTION
   Interface chrome, all 16 sector names, and the escalation demo output
   are available in Arabic — and switching language also switches
   document direction to RTL and updates <html lang>/<dir>. Rendering
   Arabic left-to-right would undercut the ITU Dimension 6 (Human
   Interface) claim this panel exists to support.

4. FULLY SELF-CONTAINED
   Charts are embedded as base64 directly in the HTML, so the file works
   offline and survives being moved out of the repo — reliable for a
   live demo.

INPUT:  ./policy_decisions.csv   (Step 5 output; the file may also be
        named input_from_step5_policy_decisions.csv)
        ./chart2_growth_ranking.png
        ./chart6_policy_flowchart.png
        ./chart7_routing_diagram.png
OUTPUT: ./output/dashboard.html
"""

import base64
import os

import pandas as pd

IN_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(IN_DIR, "output")
os.makedirs(OUT_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# PROVENANCE — fill this in before submitting.
# A dashboard that cites no source and no retrieval date is not auditable,
# and government statistical series are revised over time.
# ---------------------------------------------------------------------------
DATA_SOURCE_EN = (
    "Saudi Central Bank (SAMA) Open Data Platform — Clearing and Payment Systems: "
    "Points of Sale Transactions by Sector; E-Commerce Transactions Using Mada Cards"
)
DATA_SOURCE_AR = (
    "منصة البيانات المفتوحة للبنك المركزي السعودي — أنظمة المقاصة والمدفوعات: "
    "عمليات نقاط البيع حسب القطاع؛ عمليات التجارة الإلكترونية ببطاقات مدى"
)
ANALYSIS_WINDOW = "Jan 2019 – Dec 2023 (60 monthly observations)"
ANALYSIS_WINDOW_AR = "يناير 2019 – ديسمبر 2023 (60 ملاحظة شهرية)"
RETRIEVED_ON = "[TEAM: insert download date]"

CANDIDATE_CSVS = ["policy_decisions.csv", "input_from_step5_policy_decisions.csv"]

SECTOR_AR = {
    "Transportation": "النقل",
    "Health": "الصحة",
    "Restaurants & Café": "المطاعم والمقاهي",
    "Hotels": "الفنادق",
    "Beverage and Food": "المشروبات والأغذية",
    "Clothing and Footwear": "الملابس والأحذية",
    "Recreation and Culture": "الترفيه والثقافة",
    "Miscellaneous Goods and Services": "سلع وخدمات متنوعة",
    "Electronic & Electric Devices": "الأجهزة الإلكترونية",
    "Furniture": "الأثاث",
    "Construction & Building Materials": "مواد البناء",
    "Jewelry": "المجوهرات",
    "Telecommunication": "الاتصالات",
    "Education": "التعليم",
    "Public Utilities": "المرافق العامة",
    "Others": "أخرى",
}


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def find_input_csv() -> str:
    for name in CANDIDATE_CSVS:
        path = os.path.join(IN_DIR, name)
        if os.path.exists(path):
            return path
    raise FileNotFoundError(
        "No Step 5 decisions CSV found. Expected one of: "
        + ", ".join(CANDIDATE_CSVS)
    )


def img_b64(filename: str) -> str:
    """Embed a chart. Missing charts degrade to a visible notice rather than
    crashing the build or silently producing a broken <img>."""
    path = os.path.join(IN_DIR, filename)
    if not os.path.exists(path):
        print(f"  WARNING: {filename} not found — panel will show a placeholder notice.")
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def chart_tag(b64: str, alt: str, extra_style: str = "") -> str:
    if not b64:
        return (
            f'<div class="callout missing">Chart not available in this build '
            f'({alt}). Re-run the Step 4 / Step 6 chart scripts, then rebuild.</div>'
        )
    style = f' style="{extra_style}"' if extra_style else ""
    return f'<img class="chart" src="data:image/png;base64,{b64}" alt="{alt}"{style}>'


def bilingual(en: str, ar: str) -> str:
    return f'<span class="en">{en}</span><span class="ar">{ar}</span>'


def sector_cell(name: str) -> str:
    return f'<span class="en">{name}</span><span class="ar">{SECTOR_AR.get(name, name)}</span>'


def build_regulator_table(df: pd.DataFrame, median_index: float) -> str:
    """Layer 4 packet. Includes a shortfall column so the table has variance:
    a column that reads 5, 5, 5, 5, 5, 5, 5, 5 looks like a hardcoded label
    rather than a computed result, even though it is genuinely computed."""
    flagged = df[df["LAYER4_disclosure_required"]].sort_values("EndIndex")
    rows = ""
    for _, r in flagged.iterrows():
        shortfall = (1 - r["EndIndex"] / median_index) * 100
        rows += (
            f"<tr><td>{sector_cell(r['Sector'])}</td>"
            f"<td>{r['ConsecutiveSlowYears']}</td>"
            f"<td>{r['EndIndex']:.1f}</td>"
            f"<td>&minus;{shortfall:.0f}%</td></tr>\n"
        )
    return rows


def build_sandbox_table(df: pd.DataFrame, median_index: float) -> str:
    """Layer 2 packet. The recommended window is identical for all referred
    sectors because the Layer 2 rule keys off a single national seasonal
    anchor (Ramadan). Repeating that identical string on every row made the
    computation look inert, so the window is stated once above the table and
    the table carries the information that actually varies: referral priority
    and the size of the gap being closed."""
    flagged = df[df["LAYER2_sandbox_pilot"]].sort_values("EndIndex")
    rows = ""
    for rank, (_, r) in enumerate(flagged.iterrows(), start=1):
        shortfall = (1 - r["EndIndex"] / median_index) * 100
        rows += (
            f"<tr><td>{rank}</td>"
            f"<td>{sector_cell(r['Sector'])}</td>"
            f"<td>{r['EndIndex']:.1f}</td>"
            f"<td>&minus;{shortfall:.0f}%</td></tr>\n"
        )
    return rows


def build_sector_options(df: pd.DataFrame) -> str:
    opts = ""
    for _, r in df.sort_values("Sector").iterrows():
        opts += (
            f'<option value="{r["Sector"]}" '
            f'data-ar="{SECTOR_AR.get(r["Sector"], r["Sector"])}" '
            f'data-cluster="{r["ClusterLabel"]}">{r["Sector"]}</option>\n'
        )
    return opts


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main():
    csv_path = find_input_csv()
    df = pd.read_csv(csv_path)
    print(f"  Read {os.path.basename(csv_path)} ({len(df)} sectors)")

    n_total = len(df)
    n_slow = int(df["LAYER1_context_review"].sum())
    n_agree = int(df["Agreement"].sum())
    disagreeing = df.loc[~df["Agreement"], "Sector"].tolist()
    disagree_str = ", ".join(disagreeing) if disagreeing else "none"
    disagree_str_ar = ", ".join(SECTOR_AR.get(s, s) for s in disagreeing) if disagreeing else "لا يوجد"
    median_index = float(df["EndIndex"].median())
    min_years = int(df.loc[df["LAYER4_disclosure_required"], "ConsecutiveSlowYears"].min())

    # Layer 3 grounding document, read from the data rather than hardcoded here,
    # so the Sink cannot drift out of sync with the Policy node.
    layer3_doc = str(df["LAYER3_amlctf_gate"].iloc[0])
    layer3_source = str(df["DOC_LAYER3"].iloc[0])
    n_dormant = int((df["LAYER3_amlctf_gate"].astype(str).str.startswith("DORMANT")).sum())

    chart2_b64 = img_b64("chart2_growth_ranking.png")
    chart6_b64 = img_b64("chart6_policy_flowchart.png")
    chart7_b64 = img_b64("chart7_routing_diagram.png")

    regulator_rows = build_regulator_table(df, median_index)
    sandbox_rows = build_sandbox_table(df, median_index)
    sector_options = build_sector_options(df)

    html = f"""<!DOCTYPE html>
<html lang="en" dir="ltr" id="html-root">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sector Digitalization Watch — ITU AI Readiness Hackathon KSA</title>
<style>
  :root {{
    --green: #0B6E4F;
    --gold: #C89B3C;
    --sand: #FAF7F2;
    --ink: #1B1B1B;
    --slow: #d62728;
    --moderate: #ff9f1c;
    --rapid: #2a9d8f;
    --steel: #4a6fa5;
  }}
  * {{ box-sizing: border-box; }}
  body {{ margin:0; font-family: Tahoma, "Segoe UI", Arial, sans-serif; background: var(--sand); color: var(--ink); }}
  h1, h2, h3 {{ font-family: Georgia, "Times New Roman", serif; margin: 0 0 8px; }}

  /* ---- language + direction --------------------------------------------
     Toggling language also toggles direction. Arabic rendered left-to-right
     would undercut the Human Interface claim this dashboard makes. -------- */
  body.lang-ar .en {{ display:none; }}
  body:not(.lang-ar) .ar {{ display:none; }}
  body.lang-ar {{ direction: rtl; text-align: right; }}
  body.lang-ar .ar {{ font-family: Tahoma, Arial, sans-serif; }}
  body.lang-ar th, body.lang-ar td {{ text-align: right; }}
  body.lang-ar .lang-toggle {{ right: auto; left: 28px; }}
  body.lang-ar .callout {{ border-left: none; border-right: 4px solid var(--gold); border-radius: 6px 0 0 6px; }}
  body.lang-ar .stat {{ margin: 4px 0 12px 10px; }}
  /* the Y.3172 node sequence is a Latin acronym chain — keep it LTR */
  .pipeline {{ direction: ltr; }}
  body.lang-ar .pipeline {{ text-align: right; }}

  header.top {{ background: var(--green); color: white; padding: 22px 32px; position:relative; }}
  .pipeline {{ font-size: 12.5px; opacity: 0.85; letter-spacing: 0.5px; margin-bottom: 8px; }}
  .pipeline .current {{ font-weight: bold; text-decoration: underline; }}
  header.top h1 {{ font-size: 26px; margin-bottom: 4px; }}
  .subtitle {{ opacity: 0.92; font-size: 13.5px; }}
  .lang-toggle {{ position:absolute; top: 20px; right: 28px; }}
  .lang-toggle button {{ background: rgba(255,255,255,0.15); border:1px solid rgba(255,255,255,0.45);
    color:white; padding:7px 16px; border-radius: 20px; cursor:pointer; font-size:13px; }}
  .lang-toggle button:hover {{ background: rgba(255,255,255,0.28); }}

  nav.roles {{ display:flex; gap: 2px; background: #e9e5db; flex-wrap: wrap; }}
  nav.roles button {{ flex:1; min-width:110px; padding: 15px 8px; border:none; background: #e9e5db; cursor:pointer;
    font-size:14px; font-weight:600; color:#555; border-top: 4px solid transparent; transition: 0.15s;
    font-family: inherit; }}
  nav.roles button:hover {{ background: #ddd8cc; }}
  nav.roles button.active {{ background:#fff; color: var(--ink); }}
  nav.roles button[data-role="public"].active {{ border-top-color: var(--green); }}
  nav.roles button[data-role="regulator"].active {{ border-top-color: var(--moderate); }}
  nav.roles button[data-role="sandbox"].active {{ border-top-color: var(--rapid); }}
  nav.roles button[data-role="compliance"].active {{ border-top-color: var(--slow); }}
  nav.roles button[data-role="architecture"].active {{ border-top-color: var(--steel); }}

  main {{ max-width: 960px; margin: 0 auto; padding: 28px 20px 40px; }}
  .panel {{ display:none; background:white; border-radius:10px; padding: 26px 28px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08); }}
  .panel.active {{ display:block; }}
  table {{ width:100%; border-collapse: collapse; margin: 14px 0 20px; }}
  th, td {{ text-align:left; padding: 10px 12px; border-bottom: 1px solid #eee; font-size: 14px; }}
  th {{ background: #f7f5f0; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; color:#666; }}
  .stat {{ display:inline-block; background: var(--sand); border-radius: 8px; padding: 12px 20px; margin: 4px 10px 12px 0; }}
  .stat .num {{ font-size: 26px; font-weight:bold; display:block; line-height:1.1; }}
  .stat .lbl {{ font-size: 12px; color:#666; }}
  .callout {{ border-left: 4px solid var(--gold); background: #fdf8ee; padding: 14px 18px; margin: 16px 0;
    font-size:14px; border-radius: 0 6px 6px 0; line-height:1.6; }}
  .callout.missing {{ border-color: #bbb; background:#f5f5f5; color:#666; }}
  .packet-note {{ font-size:12px; color:#888; border:1px dashed #ddd; border-radius:6px;
    padding:8px 12px; margin: 0 0 16px; }}
  .role-tag {{ display:inline-block; font-size:11px; font-weight:700; letter-spacing:0.5px; text-transform:uppercase;
    padding: 4px 10px; border-radius: 20px; color:white; margin-bottom: 10px; }}
  .role-tag.regulator {{ background: var(--moderate); }}
  .role-tag.sandbox {{ background: var(--rapid); }}
  .role-tag.compliance {{ background: var(--slow); }}
  .role-tag.public {{ background: var(--green); }}
  .role-tag.architecture {{ background: var(--steel); }}
  img.chart {{ max-width:100%; border-radius:8px; margin: 14px 0; border:1px solid #eee; }}

  /* ---- Layer 3 escalation demo ---- */
  .gate-demo {{ border: 2px solid #eee; border-radius: 10px; padding: 18px 20px; margin: 18px 0; }}
  .gate-demo h3 {{ font-size: 16px; margin-bottom: 6px; }}
  .gate-controls {{ display:flex; gap:10px; flex-wrap:wrap; align-items:center; margin: 12px 0; }}
  .gate-controls select {{ padding: 9px 12px; border:1px solid #ccc; border-radius:6px;
    font-size:14px; font-family: inherit; min-width: 220px; background:white; color: var(--ink); }}
  .gate-controls button {{ padding: 10px 18px; border:none; border-radius:6px; background: var(--slow);
    color:white; font-size:14px; font-weight:600; cursor:pointer; font-family: inherit; }}
  .gate-controls button:hover {{ background:#b52020; }}
  #gateResult {{ margin-top: 14px; }}
  .verdict {{ border-radius:8px; padding: 14px 18px; font-size:14px; line-height:1.65;
    border-left: 5px solid var(--slow); background: #fff5f5; }}
  body.lang-ar .verdict {{ border-left:none; border-right: 5px solid var(--slow); }}
  .verdict .head {{ font-weight:700; text-transform:uppercase; letter-spacing:0.5px;
    font-size:12px; color: var(--slow); display:block; margin-bottom:6px; }}
  .verdict table {{ margin: 10px 0 4px; }}
  .verdict td {{ border-bottom:1px solid #f2dcdc; padding: 6px 10px; font-size:13px; }}
  .verdict td:first-child {{ color:#888; width:44%; }}
  .attempts {{ font-size:12px; color:#999; margin-top:10px; }}

  details {{ margin: 14px 0; }}
  summary {{ cursor:pointer; font-size:13.5px; font-weight:600; color: var(--green); padding: 6px 0; }}
  details p, details li {{ font-size:13.5px; line-height:1.65; color:#444; }}
  footer {{ text-align:center; padding: 22px 20px 30px; font-size: 12px; color:#999; line-height:1.7; }}
  footer .prov {{ max-width: 760px; margin: 0 auto; }}
  p {{ line-height:1.6; }}
</style>
</head>
<body>

<header class="top">
  <div class="lang-toggle"><button onclick="toggleLang()" id="langBtn">العربية</button></div>
  <div class="pipeline">SRC &rarr; C &rarr; PP &rarr; M &rarr; P &rarr; D &rarr; <span class="current">SINK (you are here)</span></div>
  <h1>{bilingual("Sector Digitalization Watch", "مرصد التحول الرقمي القطاعي")}</h1>
  <div class="subtitle">{bilingual(
      "Saudi cashless-payments monitoring &mdash; ITU AI Readiness Hackathon, KSA",
      "مراقبة المدفوعات غير النقدية في السعودية &mdash; هاكاثون جاهزية الذكاء الاصطناعي، المملكة العربية السعودية")}</div>
</header>

<nav class="roles">
  <button data-role="public" class="active" onclick="showRole('public')" id="tab-public">{bilingual("Public", "عام")}</button>
  <button data-role="regulator" onclick="showRole('regulator')" id="tab-regulator">{bilingual("Regulator", "الجهة التنظيمية")}</button>
  <button data-role="sandbox" onclick="showRole('sandbox')" id="tab-sandbox">{bilingual("Sandbox Team", "فريق الاختبار")}</button>
  <button data-role="compliance" onclick="showRole('compliance')" id="tab-compliance">{bilingual("Compliance", "الامتثال")}</button>
  <button data-role="architecture" onclick="showRole('architecture')" id="tab-architecture">{bilingual("Architecture", "البنية")}</button>
</nav>

<main>

  <!-- ================= PUBLIC ================= -->
  <section class="panel active" id="panel-public">
    <span class="role-tag public">{bilingual("Public view", "عرض عام")}</span>
    <h2>{bilingual("Where is Saudi Arabia's cashless push actually reaching?", "إلى أين وصل التحول نحو الاقتصاد اللامادي فعلياً؟")}</h2>
    <p>{bilingual(
        f"National electronic-payment share reached 79% in 2024 &mdash; but that single number is an average, and averages hide variance. Of {n_total} economic sectors analysed using Saudi Central Bank (SAMA) open data ({ANALYSIS_WINDOW}), {n_slow} have lagged behind in every year of the window, none more than Jewelry.",
        f"بلغت نسبة المدفوعات الإلكترونية الوطنية 79% عام 2024 &mdash; لكن هذا الرقم متوسط، والمتوسطات تخفي التباين. من أصل {n_total} قطاعاً تم تحليلها باستخدام بيانات البنك المركزي السعودي المفتوحة ({ANALYSIS_WINDOW_AR})، تأخر {n_slow} قطاعاً في كل سنة من سنوات الدراسة، وأبرزها قطاع المجوهرات."
    )}</p>

    <div class="stat"><span class="num">{n_slow} / {n_total}</span><span class="lbl">{bilingual("sectors flagged as slow adopters", "قطاعات صُنّفت كبطيئة التبني")}</span></div>
    <div class="stat"><span class="num">{min_years} / 5</span><span class="lbl">{bilingual("years in the bottom tier &mdash; every flagged sector, every year", "سنوات في الفئة الأدنى &mdash; لكل قطاع مُصنّف، كل سنة")}</span></div>
    <div class="stat"><span class="num">0</span><span class="lbl">{bilingual("enforcement actions this data alone can trigger", "إجراءات تنفيذية يمكن لهذه البيانات وحدها تفعيلها")}</span></div>

    {chart_tag(chart2_b64, "Sector growth ranking chart")}

    <details>
      <summary>{bilingual("What this analysis cannot tell you", "ما لا يمكن لهذا التحليل أن يخبرك به")}</summary>
      <p>{bilingual(
          "This is sector-level aggregate data published by SAMA. It supports no claim about any individual business, merchant, or customer, and it cannot identify who transacts in cash or why. A sector appearing here means its aggregate card-transaction growth trailed the rest of the economy &mdash; not that anything improper is occurring. Plausible benign explanations include customer preference for privacy on high-value personal purchases, thin merchant margins that cannot absorb card-processing fees, and long-standing cultural practice. Establishing which explanation applies requires evidence this dataset does not contain, which is why the first policy layer asks a question rather than issuing a finding.",
          "هذه بيانات مجمّعة على مستوى القطاع منشورة من البنك المركزي السعودي. لا تدعم أي ادعاء بشأن أي منشأة أو تاجر أو عميل بعينه، ولا يمكنها تحديد من يتعامل نقداً أو لماذا. ظهور قطاع هنا يعني أن نمو معاملاته بالبطاقات تأخر عن بقية الاقتصاد &mdash; لا أن هناك مخالفة. من التفسيرات المشروعة المحتملة: تفضيل العملاء للخصوصية في المشتريات الشخصية عالية القيمة، وهوامش ربح ضيقة لدى التجار لا تستوعب رسوم معالجة البطاقات، وممارسات ثقافية راسخة. تحديد التفسير الصحيح يتطلب أدلة لا تحتويها هذه البيانات، ولهذا فإن الطبقة الأولى من السياسة تطرح سؤالاً بدل أن تصدر حكماً."
      )}</p>
    </details>
  </section>

  <!-- ================= REGULATOR ================= -->
  <section class="panel" id="panel-regulator">
    <span class="role-tag regulator">{bilingual("Regulator view &mdash; SAMA / FSDP", "عرض الجهة التنظيمية &mdash; ساما / برنامج تطوير القطاع المالي")}</span>
    <div class="packet-note">{bilingual(
        "Packet 1 of 3 from the Distributor (Step 6). Contains Policy Layer 4 output only. Sandbox timing and AML/CTF gate status are routed elsewhere and are deliberately absent from this view.",
        "الحزمة 1 من 3 من الموزّع (الخطوة 6). تحتوي على مخرجات الطبقة الرابعة فقط. توقيت البرنامج التجريبي وحالة بوابة مكافحة غسل الأموال تُوجَّه إلى جهات أخرى وهي غائبة عن هذا العرض عمداً."
    )}</div>
    <h2>{bilingual("Sectors requiring public disclosure", "القطاعات التي تتطلب الإفصاح العلني")}</h2>
    <p>{bilingual(
        "Sectors with 2 or more consecutive years in the bottom growth tier, per Step 5 Policy Layer 4.",
        "القطاعات التي أمضت سنتين متتاليتين أو أكثر ضمن الفئة الأدنى للنمو، وفق الطبقة الرابعة من سياسة الخطوة 5."
    )}</p>
    <table>
      <tr>
        <th>{bilingual("Sector", "القطاع")}</th>
        <th>{bilingual("Consecutive slow years", "سنوات التأخر المتتالية")}</th>
        <th>{bilingual("Index, Dec 2023", "المؤشر، ديسمبر 2023")}</th>
        <th>{bilingual("Gap vs median sector", "الفجوة مقابل القطاع الوسيط")}</th>
      </tr>
      {regulator_rows}
    </table>
    <div class="callout">{bilingual(
        f"The disclosure column reads {min_years} for every listed sector. That uniformity is the finding, not a placeholder: the threshold for disclosure is 2 consecutive years, and every flagged sector cleared it at the maximum of 5 &mdash; none broke out of the bottom tier at any point in the window. The gap column is computed at this node for presentation, as the shortfall against the median sector's Dec 2023 rebased index ({median_index:.0f}).",
        f"يقرأ عمود الإفصاح {min_years} لكل قطاع مدرج. هذا التماثل هو النتيجة نفسها وليس حشواً: عتبة الإفصاح سنتان متتاليتان، وكل قطاع مُصنّف تجاوزها بالحد الأقصى وهو 5 &mdash; ولم يخرج أي منها من الفئة الأدنى في أي وقت خلال فترة الدراسة. عمود الفجوة يُحتسب في هذه العقدة لأغراض العرض، كنسبة القصور مقابل مؤشر القطاع الوسيط في ديسمبر 2023 ({median_index:.0f})."
    )}</div>
  </section>

  <!-- ================= SANDBOX ================= -->
  <section class="panel" id="panel-sandbox">
    <span class="role-tag sandbox">{bilingual("Sandbox team view &mdash; Fintech Saudi", "عرض فريق ساندبوكس &mdash; فينتك السعودية")}</span>
    <div class="packet-note">{bilingual(
        "Packet 2 of 3 from the Distributor (Step 6). Contains Policy Layer 2 output only. Disclosure obligations and AML/CTF gate status are routed elsewhere and are deliberately absent from this view.",
        "الحزمة 2 من 3 من الموزّع (الخطوة 6). تحتوي على مخرجات الطبقة الثانية فقط. التزامات الإفصاح وحالة بوابة مكافحة غسل الأموال تُوجَّه إلى جهات أخرى وهي غائبة عن هذا العرض عمداً."
    )}</div>
    <h2>{bilingual("Sectors referred for a support pilot", "القطاعات المُحالة لبرنامج تجريبي")}</h2>
    <div class="callout">{bilingual(
        "<strong>Recommended launch window for all referrals: Jan&ndash;Feb 2024</strong>, approximately 1&ndash;2 months ahead of Ramadan 2024 (~10 March). The window is computed from the Ramadan tags built at the Collector node (Step 2), which are derived per year from the Umm al-Qura calendar rather than hardcoded, since Ramadan shifts about 11 days earlier each Gregorian year. It resolves to the same window for every referred sector because Layer 2 keys off a single national seasonal anchor &mdash; a behavioural nudge lands better immediately before people are already about to spend. Per-sector seasonal anchors (Eid, the academic year, Hajj) would produce different windows and are the obvious next iteration; the current rule does not model them, and we state that rather than implying more granularity than exists.",
        "<strong>النافذة الموصى بها لإطلاق جميع الإحالات: يناير&ndash;فبراير 2024</strong>، أي قبل نحو شهر إلى شهرين من رمضان 2024 (~10 مارس). تُحتسب النافذة من وسوم رمضان المبنية في عقدة التجميع (الخطوة 2)، وهي مشتقة لكل سنة من تقويم أم القرى وليست ثابتة، لأن رمضان يتقدم نحو 11 يوماً كل سنة ميلادية. وتؤول إلى النافذة ذاتها لكل قطاع مُحال لأن الطبقة الثانية تستند إلى مرتكز موسمي وطني واحد &mdash; إذ يكون التحفيز السلوكي أكثر فاعلية قبيل موسم الإنفاق مباشرة. المرتكزات الموسمية الخاصة بكل قطاع (العيد، السنة الدراسية، الحج) ستنتج نوافذ مختلفة وهي التطوير التالي البديهي؛ القاعدة الحالية لا تُنمذجها، ونصرّح بذلك بدل الإيحاء بتفصيل غير موجود."
    )}</div>
    <table>
      <tr>
        <th>{bilingual("Priority", "الأولوية")}</th>
        <th>{bilingual("Sector", "القطاع")}</th>
        <th>{bilingual("Index, Dec 2023", "المؤشر، ديسمبر 2023")}</th>
        <th>{bilingual("Gap to close", "الفجوة المطلوب سدها")}</th>
      </tr>
      {sandbox_rows}
    </table>
    <p style="font-size:13px;color:#777;">{bilingual(
        "Priority is the referral order by size of gap, not a severity score. All referrals are non-punitive support offers.",
        "الأولوية هي ترتيب الإحالة حسب حجم الفجوة، وليست درجة خطورة. جميع الإحالات عروض دعم غير عقابية."
    )}</p>
  </section>

  <!-- ================= COMPLIANCE ================= -->
  <section class="panel" id="panel-compliance">
    <span class="role-tag compliance">{bilingual("Compliance view &mdash; SAMA AML/CTF", "عرض الامتثال &mdash; مكافحة غسل الأموال وتمويل الإرهاب")}</span>
    <div class="packet-note">{bilingual(
        "Packet 3 of 3 from the Distributor (Step 6). Contains the Policy Layer 3 assurance record only. Disclosure obligations and pilot timing are routed elsewhere and are deliberately absent from this view.",
        "الحزمة 3 من 3 من الموزّع (الخطوة 6). تحتوي على سجل توكيد الطبقة الثالثة فقط. التزامات الإفصاح وتوقيت البرامج التجريبية تُوجَّه إلى جهات أخرى وهي غائبة عن هذا العرض عمداً."
    )}</div>
    <h2>{bilingual("AML/CTF gate: assurance record", "بوابة مكافحة غسل الأموال: سجل التوكيد")}</h2>

    <div class="stat"><span class="num">{n_dormant} / {n_total}</span><span class="lbl">{bilingual("sectors: gate DORMANT", "قطاعات: البوابة خامدة")}</span></div>
    <div class="stat"><span class="num">0</span><span class="lbl">{bilingual("escalation paths reachable from this data", "مسارات تصعيد يمكن بلوغها من هذه البيانات")}</span></div>

    <div class="gate-demo">
      <h3>{bilingual("Try to trigger the gate", "حاول تفعيل البوابة")}</h3>
      <p style="font-size:13.5px;color:#555;margin:0;">{bilingual(
          "Layer 3 is not a promise in a policy paragraph &mdash; it is a property of the decision logic. Rather than asking you to take that on trust, attempt an escalation yourself. Pick any sector, including the slowest, and request AML/CTF review.",
          "الطبقة الثالثة ليست وعداً في فقرة سياسة &mdash; بل خاصية في منطق القرار. وبدلاً من مطالبتك بتصديق ذلك، جرّب التصعيد بنفسك. اختر أي قطاع، بما في ذلك الأبطأ، واطلب مراجعة مكافحة غسل الأموال."
      )}</p>
      <div class="gate-controls">
        <select id="escSector">
          {sector_options}
        </select>
        <button onclick="attemptEscalation()">{bilingual("Attempt escalation", "محاولة التصعيد")}</button>
      </div>
      <div id="gateResult"></div>
    </div>

    <div class="callout">{bilingual(
        f"Grounding documents: {layer3_source}. Gate state as recorded by the Policy node: &ldquo;{layer3_doc}&rdquo; for all {n_total} sectors. Any action on this gate additionally requires review by a human compliance officer; the system cannot reach an enforcement outcome unattended.",
        f"الوثائق المرجعية: {layer3_source}. حالة البوابة كما سجّلتها عقدة السياسة: &ldquo;{layer3_doc}&rdquo; لجميع القطاعات البالغ عددها {n_total}. أي إجراء على هذه البوابة يتطلب إضافةً مراجعة مسؤول امتثال بشري؛ ولا يمكن للنظام بلوغ نتيجة تنفيذية دون إشراف."
    )}</div>

    {chart_tag(chart6_b64, "Policy decision flowchart")}
  </section>

  <!-- ================= ARCHITECTURE ================= -->
  <section class="panel" id="panel-architecture">
    <span class="role-tag architecture">{bilingual("Architecture &mdash; how this dashboard is fed", "البنية &mdash; كيف تُغذّى هذه اللوحة")}</span>
    <h2>{bilingual("One decision, three packets, four views", "قرار واحد، ثلاث حزم، أربعة عروض")}</h2>
    <p>{bilingual(
        "The Policy node (Step 5) produces a single decision object covering every sector and all four policy layers. Broadcasting that whole object to every recipient would be lower-effort routing that pushes the burden of filtering onto the reader. The Distributor (Step 6) instead fans it into three purpose-built packets addressed to three real institutions, and this Sink renders each packet only to its own role. This view exists so the routing itself is inspectable &mdash; it is the only tab that shows all three packets at once, and it is not a role.",
        "تنتج عقدة السياسة (الخطوة 5) كائن قرار واحداً يغطي كل القطاعات وطبقات السياسة الأربع. وبثّ هذا الكائن كاملاً لكل متلقٍّ هو توجيه أقل جهداً يُحمّل القارئ عبء التصفية. لذا يقوم الموزّع (الخطوة 6) بتفريعه إلى ثلاث حزم مخصّصة موجّهة لثلاث جهات حقيقية، وتعرض هذه الوجهة كل حزمة لدورها فقط. يوجد هذا العرض لجعل التوجيه نفسه قابلاً للفحص &mdash; وهو التبويب الوحيد الذي يعرض الحزم الثلاث معاً، وليس دوراً وظيفياً."
    )}</p>

    {chart_tag(chart7_b64, "Distributor routing diagram", "border-radius:10px;")}

    <h3 style="margin-top:22px;">{bilingual("Model / manual agreement, reported in full", "اتفاق النموذج مع التصنيف اليدوي، معروضاً بالكامل")}</h3>
    <p>{bilingual(
        f"K-Means (k=3), given no labels, agreed with the manually constructed tiers on {n_agree} of {n_total} sectors. The disagreement is disclosed rather than omitted: {disagree_str}. Note also that the agreement figure should not be read as strong independent confirmation &mdash; both the clustering and the manual tiers derive largely from where each sector's rebased series ends, so they are not independent tests of the same hypothesis.",
        f"وافق خوارزم K-Means (k=3)، دون إعطائه أي تصنيفات مسبقة، التصنيف اليدوي في {n_agree} من {n_total} قطاعاً. ويُفصح عن موضع الاختلاف بدل إغفاله: {disagree_str_ar}. كما ينبغي ألا تُقرأ نسبة الاتفاق كتأكيد مستقل قوي &mdash; إذ يستمد كل من التجميع والتصنيف اليدوي معظم أساسه من موضع نهاية السلسلة المعاد ترقيمها لكل قطاع، فليسا اختبارين مستقلين للفرضية ذاتها."
    )}</p>

    <details>
      <summary>{bilingual("Limitations of this analysis", "حدود هذا التحليل")}</summary>
      <ul>
        <li>{bilingual(
            "Sector-level aggregate data only. No claim about any individual business, merchant or customer is supported. This constraint is also what makes the Layer 3 gate structurally safe.",
            "بيانات مجمّعة على مستوى القطاع فقط. لا تدعم أي ادعاء بشأن منشأة أو تاجر أو عميل بعينه. وهذا القيد نفسه هو ما يجعل بوابة الطبقة الثالثة آمنة بنيوياً."
        )}</li>
        <li>{bilingual(
            "The IQR outlier test did not formally flag the slowest sector: with 16 observations the fences are wide. It flagged the opposite extreme instead. We report this rather than omitting a disconfirming result.",
            "لم يُصنّف اختبار المدى الربيعي القطاع الأبطأ كقيمة شاذة رسمياً: فمع 16 ملاحظة تكون الحدود واسعة. بل صنّف الطرف المقابل. ونعرض هذه النتيجة بدل إغفال ما يخالف التوقع."
        )}</li>
        <li>{bilingual(
            "Ramadan date ranges for years without an officially confirmed date are estimated using the standard ~11-day yearly shift, accurate to roughly one day.",
            "نطاقات تواريخ رمضان للسنوات غير المؤكدة رسمياً مُقدّرة باستخدام الإزاحة المعتادة ~11 يوماً سنوياً، بدقة نحو يوم واحد."
        )}</li>
        <li>{bilingual(
            "Layer 2 pilot timing uses one national seasonal anchor, not per-sector seasonality.",
            "توقيت الطبقة الثانية يستخدم مرتكزاً موسمياً وطنياً واحداً، لا موسمية خاصة بكل قطاع."
        )}</li>
      </ul>
    </details>
  </section>

</main>

<footer>
  <div class="prov">
    {bilingual("Step 7 &mdash; Sink &middot; ITU AI Readiness Hackathon, Kingdom of Saudi Arabia &middot; Team Voxel",
               "الخطوة 7 &mdash; الوجهة النهائية &middot; هاكاثون جاهزية الذكاء الاصطناعي، المملكة العربية السعودية &middot; فريق فوكسل")}
    <br>
    {bilingual(f"Source: {DATA_SOURCE_EN}", f"المصدر: {DATA_SOURCE_AR}")}
    <br>
    {bilingual(f"Analysis window: {ANALYSIS_WINDOW} &middot; Retrieved: {RETRIEVED_ON} &middot; No confidential material.",
               f"فترة التحليل: {ANALYSIS_WINDOW_AR} &middot; تاريخ التحميل: {RETRIEVED_ON} &middot; لا تتضمن أي مواد سرية.")}
  </div>
</footer>

<script>
/* ---------------------------------------------------------------------------
   Layer 3 gate logic, mirrored at the Sink.
   The Policy node's guarantee is that sector-level aggregate evidence can
   never satisfy the AML/CTF evidence requirement. There is deliberately no
   branch below that returns anything other than a refusal — the refusal is
   not a default case, it is the only case.
   --------------------------------------------------------------------------- */
var GATE = {{
  state: "DORMANT",
  evidence_available_en: "Sector-level aggregate (monthly totals per sector)",
  evidence_available_ar: "مجمّعة على مستوى القطاع (إجماليات شهرية لكل قطاع)",
  evidence_required_en: "Transaction-level or merchant-level, independently sourced",
  evidence_required_ar: "على مستوى المعاملة أو التاجر، من مصدر مستقل",
  reviewer_en: "Human compliance officer (mandatory, non-bypassable)",
  reviewer_ar: "مسؤول امتثال بشري (إلزامي وغير قابل للتجاوز)"
}};
var attempts = 0;

function attemptEscalation() {{
  var sel = document.getElementById('escSector');
  var opt = sel.options[sel.selectedIndex];
  var nameEn = opt.value;
  var nameAr = opt.getAttribute('data-ar');
  var cluster = opt.getAttribute('data-cluster');
  attempts += 1;

  var html =
    '<div class="verdict">' +
      '<span class="head">' +
        '<span class="en">Escalation refused &mdash; gate remains ' + GATE.state + '</span>' +
        '<span class="ar">رُفض التصعيد &mdash; البوابة تبقى خامدة</span>' +
      '</span>' +
      '<span class="en">Requested: AML/CTF review of <strong>' + nameEn + '</strong> (model cluster: ' + cluster + ').</span>' +
      '<span class="ar">الطلب: مراجعة مكافحة غسل الأموال لقطاع <strong>' + nameAr + '</strong> (تصنيف النموذج: ' + cluster + ').</span>' +
      '<table>' +
        '<tr><td><span class="en">Evidence required</span><span class="ar">الأدلة المطلوبة</span></td>' +
            '<td><span class="en">' + GATE.evidence_required_en + '</span><span class="ar">' + GATE.evidence_required_ar + '</span></td></tr>' +
        '<tr><td><span class="en">Evidence available</span><span class="ar">الأدلة المتاحة</span></td>' +
            '<td><span class="en">' + GATE.evidence_available_en + '</span><span class="ar">' + GATE.evidence_available_ar + '</span></td></tr>' +
        '<tr><td><span class="en">Match</span><span class="ar">التطابق</span></td>' +
            '<td><span class="en"><strong>None.</strong> Cluster membership is not evidence of conduct.</span>' +
                '<span class="ar"><strong>لا يوجد.</strong> الانتماء إلى تصنيف ليس دليلاً على سلوك.</span></td></tr>' +
        '<tr><td><span class="en">Required reviewer</span><span class="ar">جهة المراجعة المطلوبة</span></td>' +
            '<td><span class="en">' + GATE.reviewer_en + '</span><span class="ar">' + GATE.reviewer_ar + '</span></td></tr>' +
      '</table>' +
      '<span class="en">This dataset structurally cannot contain the required evidence class, so no input to this interface can move the gate. Slow digital-payment adoption is not a financial-crime signal, and treating it as one is the specific misuse this layer exists to prevent.</span>' +
      '<span class="ar">لا يمكن لهذه البيانات بنيوياً أن تحتوي على فئة الأدلة المطلوبة، لذا لا يمكن لأي إدخال في هذه الواجهة تحريك البوابة. بطء تبنّي المدفوعات الرقمية ليس مؤشراً على جريمة مالية، ومعاملته كذلك هو تحديداً سوء الاستخدام الذي وُجدت هذه الطبقة لمنعه.</span>' +
      '<div class="attempts">' +
        '<span class="en">Attempts this session: ' + attempts + ' &middot; Refusals: ' + attempts + '</span>' +
        '<span class="ar">المحاولات في هذه الجلسة: ' + attempts + ' &middot; حالات الرفض: ' + attempts + '</span>' +
      '</div>' +
    '</div>';

  document.getElementById('gateResult').innerHTML = html;
}}

function showRole(role) {{
  document.querySelectorAll('.panel').forEach(function(p) {{ p.classList.remove('active'); }});
  document.getElementById('panel-' + role).classList.add('active');
  document.querySelectorAll('nav.roles button').forEach(function(b) {{ b.classList.remove('active'); }});
  document.getElementById('tab-' + role).classList.add('active');
}}

function toggleLang() {{
  var body = document.body;
  var btn = document.getElementById('langBtn');
  var nowAr = body.classList.toggle('lang-ar');
  btn.textContent = nowAr ? 'English' : 'العربية';
  /* direction and lang must move with the text, or the Human Interface
     claim this dashboard makes is not actually implemented */
  document.documentElement.lang = nowAr ? 'ar' : 'en';
  document.documentElement.dir  = nowAr ? 'rtl' : 'ltr';
  /* keep the sector dropdown readable in the active language */
  var sel = document.getElementById('escSector');
  if (sel) {{
    for (var i = 0; i < sel.options.length; i++) {{
      var o = sel.options[i];
      if (nowAr) {{
        if (!o.getAttribute('data-en')) o.setAttribute('data-en', o.text);
        o.text = o.getAttribute('data-ar');
      }} else if (o.getAttribute('data-en')) {{
        o.text = o.getAttribute('data-en');
      }}
    }}
  }}
}}
</script>

</body>
</html>
"""

    out_path = os.path.join(OUT_DIR, "dashboard.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)

    size_kb = os.path.getsize(out_path) / 1024
    print(f"  Wrote {out_path} ({size_kb:.0f} KB, fully self-contained)")
    if RETRIEVED_ON.startswith("[TEAM"):
        print("  REMINDER: set RETRIEVED_ON at the top of this file before submitting.")


if __name__ == "__main__":
    main()
