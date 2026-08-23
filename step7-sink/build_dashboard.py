"""
build_dashboard.py
===================
ITU AI Readiness Hackathon (KSA) — Fintech track
STEP 7 of the Y.3172 pipeline: "SINK" (inference target)

WHAT THIS DOES
--------------
Generates dashboard.html: a single, self-contained, offline-capable HTML
file — no server, no dependencies, just open it in a browser. This is
where the whole pipeline's output finally reaches a real person.

DESIGN DECISION (mirrors Step 6's routing, on purpose)
-------------------------------------------------------
Step 6 (Distributor) already decided that a regulator, a sandbox team,
and a compliance officer should each get a different slice of the
decision. A single undifferentiated dashboard for everyone would throw
that work away. So this Sink has a ROLE SELECTOR: pick your role, see
only your packet — Public / Regulator / Sandbox Team / Compliance.

Also bilingual (English / Arabic) for the interface chrome and all 16
sector names — a direct, concrete answer to ITU AI Readiness
Dimension 6 ("Human Interface"): availability of the AI-supported
interface in the local language, not just English.

Charts are embedded as base64 directly in the HTML, so the file is fully
portable (works even if moved out of the repo folder structure) — good
for a live demo.

OUTPUT: ./output/dashboard.html
"""

import base64
import os

import pandas as pd

IN_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(IN_DIR, "output")
os.makedirs(OUT_DIR, exist_ok=True)

DECISIONS_PATH = os.path.join(IN_DIR, "policy_decisions.csv")

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


def img_b64(filename: str) -> str:
    with open(os.path.join(IN_DIR, filename), "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def bilingual(en: str, ar: str) -> str:
    return f'<span class="en">{en}</span><span class="ar">{ar}</span>'


def sector_cell(name: str) -> str:
    ar = SECTOR_AR.get(name, name)
    return f'<span class="en">{name}</span><span class="ar">{ar}</span>'


def build_regulator_table(df: pd.DataFrame) -> str:
    flagged = df[df["LAYER4_disclosure_required"]].sort_values("EndIndex")
    rows = ""
    for _, r in flagged.iterrows():
        rows += (
            f"<tr><td>{sector_cell(r['Sector'])}</td>"
            f"<td>{r['ConsecutiveSlowYears']}</td>"
            f"<td>{r['EndIndex']:.1f}</td></tr>\n"
        )
    return rows


def build_sandbox_table(df: pd.DataFrame) -> str:
    flagged = df[df["LAYER2_sandbox_pilot"]].sort_values("EndIndex")
    rows = ""
    for _, r in flagged.iterrows():
        rows += (
            f"<tr><td>{sector_cell(r['Sector'])}</td>"
            f"<td>{bilingual('Jan-Feb 2024 (ahead of Ramadan)', 'يناير-فبراير 2024 (قبل رمضان)')}</td></tr>\n"
        )
    return rows


def main():
    df = pd.read_csv(DECISIONS_PATH)
    n_slow = int((df["LAYER1_context_review"]).sum())
    n_total = len(df)

    chart2_b64 = img_b64("chart2_growth_ranking.png")
    chart6_b64 = img_b64("chart6_policy_flowchart.png")
    chart7_b64 = img_b64("chart7_routing_diagram.png")

    regulator_rows = build_regulator_table(df)
    sandbox_rows = build_sandbox_table(df)

    html = f"""<!DOCTYPE html>
<html lang="en" id="html-root">
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
  }}
  * {{ box-sizing: border-box; }}
  body {{ margin:0; font-family: Tahoma, "Segoe UI", Arial, sans-serif; background: var(--sand); color: var(--ink); }}
  h1, h2, h3 {{ font-family: Georgia, "Times New Roman", serif; margin: 0 0 8px; }}
  body.lang-ar .en {{ display:none; }}
  body:not(.lang-ar) .ar {{ display:none; }}
  body.lang-ar .ar {{ font-family: Tahoma, Arial, sans-serif; }}
  header.top {{ background: var(--green); color: white; padding: 22px 32px; position:relative; }}
  .pipeline {{ font-size: 12.5px; opacity: 0.85; letter-spacing: 0.5px; margin-bottom: 8px; }}
  .pipeline .current {{ font-weight: bold; text-decoration: underline; }}
  header.top h1 {{ font-size: 26px; margin-bottom: 4px; }}
  .subtitle {{ opacity: 0.92; font-size: 13.5px; }}
  .lang-toggle {{ position:absolute; top: 20px; right: 28px; }}
  .lang-toggle button {{ background: rgba(255,255,255,0.15); border:1px solid rgba(255,255,255,0.45);
    color:white; padding:7px 16px; border-radius: 20px; cursor:pointer; font-size:13px; }}
  .lang-toggle button:hover {{ background: rgba(255,255,255,0.28); }}
  nav.roles {{ display:flex; gap: 2px; background: #e9e5db; }}
  nav.roles button {{ flex:1; padding: 15px 8px; border:none; background: #e9e5db; cursor:pointer;
    font-size:14px; font-weight:600; color:#555; border-top: 4px solid transparent; transition: 0.15s; }}
  nav.roles button.active {{ background:#fff; color: var(--ink); }}
  nav.roles button[data-role="public"].active {{ border-top-color: var(--green); }}
  nav.roles button[data-role="regulator"].active {{ border-top-color: var(--moderate); }}
  nav.roles button[data-role="sandbox"].active {{ border-top-color: var(--rapid); }}
  nav.roles button[data-role="compliance"].active {{ border-top-color: var(--slow); }}
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
  .callout {{ border-left: 4px solid var(--gold); background: #fdf8ee; padding: 14px 18px; margin: 16px 0; font-size:14px; border-radius: 0 6px 6px 0; }}
  .role-tag {{ display:inline-block; font-size:11px; font-weight:700; letter-spacing:0.5px; text-transform:uppercase;
    padding: 4px 10px; border-radius: 20px; color:white; margin-bottom: 10px; }}
  .role-tag.regulator {{ background: var(--moderate); }}
  .role-tag.sandbox {{ background: var(--rapid); }}
  .role-tag.compliance {{ background: var(--slow); }}
  .role-tag.public {{ background: var(--green); }}
  img.chart {{ max-width:100%; border-radius:8px; margin: 14px 0; border:1px solid #eee; }}
  footer {{ text-align:center; padding: 22px; font-size: 12px; color:#999; }}
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
      "مراقبة المدفوعات غير النقدية في السعودية &mdash; هاكاثون جاهزية الذكاء الاصطناعي")}</div>
</header>

<nav class="roles">
  <button data-role="public" class="active" onclick="showRole('public')" id="tab-public">{bilingual("Public", "عام")}</button>
  <button data-role="regulator" onclick="showRole('regulator')" id="tab-regulator">{bilingual("Regulator", "الجهة التنظيمية")}</button>
  <button data-role="sandbox" onclick="showRole('sandbox')" id="tab-sandbox">{bilingual("Sandbox Team", "فريق الاختبار")}</button>
  <button data-role="compliance" onclick="showRole('compliance')" id="tab-compliance">{bilingual("Compliance", "الامتثال")}</button>
</nav>

<main>

  <section class="panel active" id="panel-public">
    <span class="role-tag public">{bilingual("Public view", "عرض عام")}</span>
    <h2>{bilingual("Where is Saudi Arabia's cashless push actually reaching?", "إلى أين وصل التحول نحو الاقتصاد اللامادي فعلياً؟")}</h2>
    <p>{bilingual(
        f"National electronic-payment share reached 79% in 2024 &mdash; but that single number hides real variation. Of {n_total} economic sectors analyzed using Saudi Central Bank (SAMA) open data (2019&ndash;2023), {n_slow} have consistently lagged behind, none more than Jewelry.",
        f"بلغت نسبة المدفوعات الإلكترونية الوطنية 79% عام 2024 &mdash; لكن هذا الرقم الواحد يخفي تبايناً حقيقياً. من أصل {n_total} قطاعاً تم تحليلها باستخدام بيانات البنك المركزي السعودي المفتوحة (2019-2023)، تأخر {n_slow} قطاعاً باستمرار، وأبرزها قطاع المجوهرات."
    )}</p>
    <div class="stat"><span class="num">{n_slow} / {n_total}</span><span class="lbl">{bilingual("sectors flagged as slow adopters", "قطاعات صُنّفت كبطيئة التبني")}</span></div>
    <div class="stat"><span class="num">3&times;</span><span class="lbl">{bilingual("independent checks agreed (growth, correlation, clustering)", "طرق تحليل مستقلة متفقة")}</span></div>
    <div class="stat"><span class="num">0</span><span class="lbl">{bilingual("enforcement actions triggered by this data alone", "إجراءات تنفيذية بُنيت على هذه البيانات وحدها")}</span></div>
    <img class="chart" src="data:image/png;base64,{chart2_b64}" alt="Sector growth ranking chart">
  </section>

  <section class="panel" id="panel-regulator">
    <span class="role-tag regulator">{bilingual("Regulator view &mdash; SAMA / FSDP", "عرض الجهة التنظيمية")}</span>
    <h2>{bilingual("Sectors requiring public disclosure", "القطاعات التي تتطلب الإفصاح العلني")}</h2>
    <p>{bilingual(
        "Sectors with 2 or more consecutive years in the bottom growth tier, per Step 5 Policy Layer 4.",
        "القطاعات التي أمضت سنتين متتاليتين أو أكثر ضمن الفئة الأدنى للنمو، وفق الطبقة الرابعة من سياسة الخطوة 5."
    )}</p>
    <table>
      <tr><th>{bilingual("Sector", "القطاع")}</th><th>{bilingual("Consecutive slow years", "سنوات التأخر المتتالية")}</th><th>{bilingual("Index, Dec 2023", "المؤشر، ديسمبر 2023")}</th></tr>
      {regulator_rows}
    </table>
  </section>

  <section class="panel" id="panel-sandbox">
    <span class="role-tag sandbox">{bilingual("Sandbox team view &mdash; Fintech Saudi", "عرض فريق ساندبوكس")}</span>
    <h2>{bilingual("Sectors referred for a support pilot", "القطاعات المُحالة لبرنامج تجريبي")}</h2>
    <p>{bilingual(
        "Referred per Step 5 Policy Layer 2 &mdash; timed ahead of a known high-spending window, not launched at random.",
        "مُحالة وفق الطبقة الثانية من السياسة &mdash; بتوقيت يسبق موسم إنفاق معروف، وليس عشوائياً."
    )}</p>
    <table>
      <tr><th>{bilingual("Sector", "القطاع")}</th><th>{bilingual("Recommended pilot window", "التوقيت المقترح للبرنامج")}</th></tr>
      {sandbox_rows}
    </table>
  </section>

  <section class="panel" id="panel-compliance">
    <span class="role-tag compliance">{bilingual("Compliance view &mdash; SAMA AML/CTF", "عرض الامتثال")}</span>
    <h2>{bilingual("AML/CTF gate: assurance record", "بوابة مكافحة غسل الأموال: سجل التوكيد")}</h2>
    <div class="callout">{bilingual(
        f"All {n_total} sectors reviewed remained <strong>DORMANT</strong> on the AML/CTF gate. By design, sector-level cluster membership alone can never trigger this gate &mdash; it requires independent, transaction-level evidence this dataset does not contain, reviewed by a human officer.",
        f"جميع القطاعات البالغ عددها {n_total} بقيت <strong>خامدة</strong> على بوابة مكافحة غسل الأموال. وفق التصميم، لا يمكن لعضوية القطاع في تصنيف معين وحدها أن تُفعّل هذه البوابة أبداً &mdash; إذ تتطلب أدلة مستقلة على مستوى المعاملات لا تحتوي عليها هذه البيانات، وتخضع لمراجعة مسؤول امتثال بشري."
    )}</div>
    <img class="chart" src="data:image/png;base64,{chart6_b64}" alt="Policy decision flowchart">
  </section>

</main>

<div style="max-width:960px;margin:0 auto;padding:0 20px 30px;">
  <img class="chart" src="data:image/png;base64,{chart7_b64}" alt="Distributor routing diagram" style="border-radius:10px;">
</div>

<footer>{bilingual(
    "Step 7 &mdash; Sink &middot; ITU AI Readiness Hackathon, Kingdom of Saudi Arabia",
    "الخطوة 7 &mdash; الوجهة النهائية &middot; هاكاثون جاهزية الذكاء الاصطناعي، المملكة العربية السعودية"
)}</footer>

<script>
function showRole(role) {{
  document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
  document.getElementById('panel-' + role).classList.add('active');
  document.querySelectorAll('nav.roles button').forEach(b => b.classList.remove('active'));
  document.getElementById('tab-' + role).classList.add('active');
}}
function toggleLang() {{
  const body = document.body;
  const btn = document.getElementById('langBtn');
  const nowAr = body.classList.toggle('lang-ar');
  btn.textContent = nowAr ? 'English' : 'العربية';
}}
</script>

</body>
</html>
"""

    out_path = os.path.join(OUT_DIR, "dashboard.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Wrote {out_path} ({os.path.getsize(out_path)/1024:.0f} KB, fully self-contained)")


if __name__ == "__main__":
    main()
