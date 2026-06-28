import os
import json
import time
import pandas as pd
import anthropic
import webbrowser

DEMO_FOLDER = "Desired Folder to store files write name or document directory here"

client = anthropic.Anthropic(api_key="ANTHROPIC_API_KEY")

def enrich_lead(company, contact, email, notes):
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        messages=[{
            "role": "user",
            "content": f"""You are a B2B lead enrichment agent for Mitrex, the largest solar building materials manufacturer in North America. Their ideal customers are architects, building owners, general contractors, and engineers in sectors like healthcare, universities, airports, and real estate.

Raw lead:
Company: {company}
Contact: {contact}
Email: {email}
Notes: {notes}

Return a JSON object with these exact fields:
- industry (string)
- company_size (exactly: Small, Medium, or Large)
- estimated_employees (string)
- location (string)
- lead_score (integer 0-100)
- tier (exactly: Hot, Warm, or Cold)
- assigned_to (Cory Fry for Hot, Alborz Razavi for Warm, Nurture Sequence for Cold)
- next_action (string)
- email_subject (string)
- email_body (string, under 100 words, personalized to their industry)
- cadence (array of exactly 3 objects, each with: day (integer), type (Email or LinkedIn), subject (string), message (string under 80 words))
  - If Hot: days 1, 7, 14
  - If Warm: days 1, 21, 42
  - If Cold: days 1, 30, 90

Return JSON only. No markdown. No code blocks. No extra text."""
        }]
    )
    text = response.content[0].text.strip()
    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()
    return json.loads(text)

def get_tier_color(tier):
    if tier == "Hot":
        return "#FF6B35"
    elif tier == "Warm":
        return "#E8A24A"
    return "#888888"

def get_score_bg(score):
    if score >= 70:
        return "#FF6B35"
    elif score >= 40:
        return "#E8A24A"
    return "#888888"

def generate_html(results):
    cards_html = ""
    for r in results:
        tier = r.get("tier", "Cold")
        score = r.get("lead_score", 0)
        tier_color = get_tier_color(tier)
        score_bg = get_score_bg(score)
        contact = r.get("Contact", "")
        initials = "".join([n[0] for n in contact.split() if n])

        cadence_html = ""
        cadence = r.get("cadence", [])
        for i, step in enumerate(cadence):
            border = "margin-bottom:14px;" if i < len(cadence) - 1 else ""
            cadence_html += f"""
            <div style="display:flex; gap:12px; align-items:flex-start; {border}">
                <div style="flex-shrink:0; width:36px; height:36px; border-radius:50%; background:{tier_color}22; border:1px solid {tier_color}44; display:flex; align-items:center; justify-content:center; font-size:11px; font-weight:500; color:{tier_color};">D{step.get('day','')}</div>
                <div style="flex:1;">
                    <div style="font-size:13px; font-weight:500; color:#1a1a1a; margin-bottom:2px;">{step.get('subject','')}</div>
                    <div style="font-size:12px; color:#666; line-height:1.5;">{step.get('message','')}</div>
                    <span style="display:inline-block; margin-top:4px; font-size:11px; padding:2px 8px; border-radius:20px; background:#f0f0f0; color:#666;">{step.get('type','Email')}</span>
                </div>
            </div>"""
            if i < len(cadence) - 1:
                cadence_html += '<div style="width:1px; height:10px; background:#e0e0e0; margin:0 18px;"></div>'

        cards_html += f"""
        <div style="background:white; border:0.5px solid #e0e0e0; border-left:3px solid {tier_color}; border-radius:12px; padding:20px; margin-bottom:16px;">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:16px;">
                <div style="display:flex; gap:12px; align-items:center;">
                    <div style="width:40px; height:40px; border-radius:50%; background:#f5f5f5; display:flex; align-items:center; justify-content:center; font-size:14px; font-weight:500; color:#333; border:0.5px solid #e0e0e0;">{initials}</div>
                    <div>
                        <div style="font-size:15px; font-weight:500; color:#1a1a1a;">{r.get('Company','')}</div>
                        <div style="font-size:13px; color:#666;">{contact} · {r.get('Email','')}</div>
                        <div style="font-size:12px; color:#888; margin-top:1px;">{r.get('industry','')}&nbsp;·&nbsp;{r.get('location','')}&nbsp;·&nbsp;{r.get('estimated_employees','')} employees</div>
                    </div>
                </div>
                <div style="text-align:center; flex-shrink:0;">
                    <div style="width:52px; height:52px; border-radius:50%; background:{score_bg}; display:flex; align-items:center; justify-content:center; font-size:18px; font-weight:500; color:white;">{score}</div>
                    <div style="font-size:11px; color:#888; margin-top:4px;">score</div>
                </div>
            </div>
            <div style="display:grid; grid-template-columns:repeat(3,1fr); gap:8px; margin-bottom:16px;">
                <div style="background:#f8f8f8; border-radius:8px; padding:10px 12px;">
                    <div style="font-size:11px; color:#888; margin-bottom:3px;">Tier</div>
                    <div style="font-size:14px; font-weight:500; color:{tier_color};">{tier}</div>
                </div>
                <div style="background:#f8f8f8; border-radius:8px; padding:10px 12px;">
                    <div style="font-size:11px; color:#888; margin-bottom:3px;">Assigned to</div>
                    <div style="font-size:13px; font-weight:500; color:#1a1a1a;">{r.get('assigned_to','')}</div>
                </div>
                <div style="background:#f8f8f8; border-radius:8px; padding:10px 12px;">
                    <div style="font-size:11px; color:#888; margin-bottom:3px;">Status</div>
                    <div style="font-size:13px; font-weight:500; color:#1a1a1a;">New · AI Enriched</div>
                </div>
            </div>
            <div style="margin-bottom:16px;">
                <div style="font-size:11px; color:#888; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:8px;">Outreach email</div>
                <div style="background:#f8f8f8; border-radius:8px; padding:14px; border:0.5px solid #e0e0e0;">
                    <div style="font-size:12px; font-weight:500; color:#1a1a1a; margin-bottom:6px;">Subject: {r.get('email_subject','')}</div>
                    <div style="font-size:12px; color:#555; line-height:1.6;">{r.get('email_body','')}</div>
                </div>
            </div>
            <div>
                <div style="font-size:11px; color:#888; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:12px;">Email drip cadence</div>
                {cadence_html}
            </div>
        </div>"""

    hot = sum(1 for r in results if r.get("tier") == "Hot")
    warm = sum(1 for r in results if r.get("tier") == "Warm")
    cold = sum(1 for r in results if r.get("tier") == "Cold")
    avg_score = round(sum(r.get("lead_score", 0) for r in results) / len(results)) if results else 0

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Mitrex PRM Engine</title>
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f5f5f5; color: #1a1a1a; }}
</style>
</head>
<body>
<div style="background:#1a1a1a; padding:28px 32px;">
    <div style="font-size:11px; color:#FF6B35; letter-spacing:2px; text-transform:uppercase; margin-bottom:6px;">Powered by Claude API &middot; Multi-step agentic workflow</div>
    <div style="font-size:22px; font-weight:500; color:white; margin-bottom:4px;">Mitrex Lead Enrichment and PRM Engine</div>
    <div style="font-size:13px; color:#888;">Raw leads in &rarr; enriched, scored, assigned, and email cadence ready for Salesforce</div>
</div>
<div style="max-width:860px; margin:0 auto; padding:28px 20px;">
    <div style="display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin-bottom:24px;">
        <div style="background:white; border:0.5px solid #e0e0e0; border-radius:8px; padding:16px;">
            <div style="font-size:12px; color:#888; margin-bottom:4px;">Total leads</div>
            <div style="font-size:28px; font-weight:500;">{len(results)}</div>
        </div>
        <div style="background:white; border:0.5px solid #e0e0e0; border-radius:8px; padding:16px;">
            <div style="font-size:12px; color:#888; margin-bottom:4px;">Hot leads</div>
            <div style="font-size:28px; font-weight:500; color:#FF6B35;">{hot}</div>
        </div>
        <div style="background:white; border:0.5px solid #e0e0e0; border-radius:8px; padding:16px;">
            <div style="font-size:12px; color:#888; margin-bottom:4px;">Warm leads</div>
            <div style="font-size:28px; font-weight:500; color:#E8A24A;">{warm}</div>
        </div>
        <div style="background:white; border:0.5px solid #e0e0e0; border-radius:8px; padding:16px;">
            <div style="font-size:12px; color:#888; margin-bottom:4px;">Avg score</div>
            <div style="font-size:28px; font-weight:500;">{avg_score}</div>
        </div>
    </div>
    {cards_html}
    <div style="text-align:center; padding:20px; color:#aaa; font-size:12px;">
        Mitrex Lead Enrichment and PRM Engine &middot; Powered by Claude API &middot; {len(results)} leads processed
    </div>
</div>
</body>
</html>"""

    html_path = os.path.join(DEMO_FOLDER, "mitrex_output.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Visual report saved to: {html_path}")
    webbrowser.open(f"file://{html_path}")

def run_excel_pipeline():
    print("\n" + "="*60)
    print("MITREX LEAD ENRICHMENT AND PRM ENGINE")
    print("Processing leads from Excel...")
    print("="*60)

    input_path = os.path.join(DEMO_FOLDER, "mitrex_leads_input.xlsx")
    df = pd.read_excel(input_path)
    results = []

    for index, row in df.iterrows():
        company = row.get("Company", "")
        contact = row.get("Contact", "")
        email = row.get("Email", "")
        notes = row.get("Notes", "")
        print(f"\nProcessing lead {index + 1}/{len(df)}: {company}")
        try:
            enriched = enrich_lead(company, contact, email, notes)
            enriched["Company"] = company
            enriched["Contact"] = contact
            enriched["Email"] = email
            enriched["Notes"] = notes
            results.append(enriched)
            print(f"Done - Score: {enriched.get('lead_score')}/100 | Tier: {enriched.get('tier')} | Assigned: {enriched.get('assigned_to')}")
            time.sleep(1)
        except Exception as e:
            print(f"Error processing {company}: {e}")

    flat_results = [{k: v for k, v in r.items() if k != "cadence"} for r in results]
    output_df = pd.DataFrame(flat_results)
    output_path = os.path.join(DEMO_FOLDER, "mitrex_leads_output.xlsx")
    output_df.to_excel(output_path, index=False)

    generate_html(results)

    print("\n" + "="*60)
    print("PIPELINE COMPLETE")
    print(f"{len(results)} leads enriched, scored, and assigned")
    print(f"Excel saved to: {output_path}")
    print(f"Visual report saved to: {os.path.join(DEMO_FOLDER, 'mitrex_output.html')}")
    print("="*60)

if __name__ == "__main__":
    run_excel_pipeline()
