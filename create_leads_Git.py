import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

DEMO_FOLDER = os.getenv("DEMO_FOLDER", ".")

leads_data = {
    "Company": [
        "Daniels Corporation",
        "BuildRight Construction",
        "Toronto General Hospital",
        "Hines Real Estate",
        "EllisDon Corporation"
    ],
    "Contact": [
        "Michael Chen",
        "Sarah Park",
        "James Liu",
        "Rebecca Torres",
        "David Kim"
    ],
    "Email": [
        "michael.chen@danielscorp.com",
        "spark@buildright.ca",
        "jliu@tgh.ca",
        "rtorres@hines.com",
        "dkim@ellisdon.com"
    ],
    "Notes": [
        "Architecture and development firm, GTA projects",
        "General contractor, commercial builds",
        "Healthcare facility, retrofit opportunity",
        "Large REIT, multiple commercial properties",
        "Major construction firm, nationwide projects"
    ]
}

df = pd.DataFrame(leads_data)
output_path = os.path.join(DEMO_FOLDER, "mitrex_leads_input.xlsx")
df.to_excel(output_path, index=False)
print(f"Input file created: {output_path}")
