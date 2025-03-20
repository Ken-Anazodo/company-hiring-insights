import re
import json
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pandas as pd

templates = Jinja2Templates(directory="pkg/templates")
router = APIRouter()

# Load datasets
try:
    df_attr = pd.read_csv("pkg/static/company_data/company_attributes.csv")
    df_city = pd.read_csv("pkg/static/company_data/job_post_by_city.csv")
    df_role = pd.read_csv("pkg/static/company_data/job_post_by_job_family.csv")

    # Normalize company names (strip spaces & convert to lowercase)
    df_attr["company_name"] = df_attr["company_name"].str.strip().str.lower()
    
    # Clean up "industry_list" column and replace NaN with "Unknown"
    df_attr["industry_list"] = (
        df_attr["industry_list"]
        .astype(str)  # Convert everything to string
        .fillna("Unknown")  # Handle missing values
        .apply(lambda x: re.sub(r'[\{\}""]', '', x) if x not in ["nan", ""] else "Unknown")  # Remove {}, "", and fix NaN
    )

except Exception as e:
    print(f"Error loading dataset: {e}")

# Create mappings
company_id_to_name = df_attr.set_index("company_id")["company_name"].to_dict()
company_name_to_id = {v: k for k, v in company_id_to_name.items()}
company_attr = df_attr.set_index("company_id").to_dict(orient="index")

def get_roles_data(company_id):
    """Get job roles distribution for a company."""
    roles = df_role[df_role["company_id"] == company_id]
    return [{"name": row["job_family"], "value": row["position_count"], "wage_median": row["wage_median"]} for _, row in roles.iterrows()]



def get_cities_data(company_id):
    """Get job postings distribution by city for a company."""
    df_city["company_id"] = df_city["company_id"].astype(str)  # Ensure company_id column is string
    company_id = str(company_id)  
    filtered_df = df_city[df_city["company_id"] == company_id]
    return [{"name": row["city"], "value": row["position_count"]} for _, row in filtered_df.iterrows()]


def get_total_job_openings(company_id):
    """Calculate total job openings for a company."""
    return df_role[df_role["company_id"] == company_id]["position_count"].sum()



def get_top_roles_salary(company_id, top_n=3):
    """Get top N job roles with highest median salary for a company."""
    roles = df_role[df_role["company_id"] == company_id].sort_values(by="wage_median", ascending=False)
    return [{"job": row["job_family"], "salary": row["wage_median"]} for _, row in roles.head(top_n).iterrows()]



def get_top_hiring_states(company_id, top_n=3):
    """Get top states where the company has job postings."""
    if "state_name" in df_city.columns:  # Correct column name
        df_city["company_id"] = df_city["company_id"].astype(str)  # Ensure correct type
        company_id = str(company_id)
        state_totals = (df_city[df_city["company_id"] == company_id].groupby("state_name")["position_count"].sum().reset_index())
        state_totals = state_totals.sort_values(by="position_count", ascending=False).head(top_n)
        return [{"state": row["state_name"], "value": row["position_count"]} for _, row in state_totals.iterrows()]
    return []


def get_total_job_openings_by_city():
    """Get total job openings by city (Which city has the highest demand?)."""
    city_totals = df_city.groupby("city")["position_count"].sum().reset_index()
    city_totals = city_totals.sort_values(by="position_count", ascending=False)
    return [{"name": row["city"], "value": row["position_count"]} for _, row in city_totals.iterrows()]



def get_total_job_openings_by_industry():
    """Get total job openings by industry."""
    merged_df = df_role.merge(df_attr, on="company_id", how="left")
    industry_totals = merged_df.groupby("industry_list")["position_count"].sum().reset_index()
    industry_totals = industry_totals.sort_values(by="position_count", ascending=False)
    return [{"industry": row["industry_list"], "value": row["position_count"]} for _, row in industry_totals.iterrows()]



def get_total_companies_hiring():
    """Get total number of unique companies hiring."""
    return df_attr["company_id"].nunique()



def get_total_cities_with_job_postings(company_id):
    """Get the total number of unique cities with job postings for a company."""
    df_city["company_id"] = df_city["company_id"].astype(str)  # Ensure company_id is string
    company_id = str(company_id)  # Convert input to string
    filtered_df = df_city[df_city["company_id"] == company_id]
    total_cities = filtered_df["city"].nunique()
    print(f"DEBUG: Company ID = {company_id}, Matching Rows = {len(filtered_df)}, Total Cities = {total_cities}")  # Debugging
    return total_cities



@router.get("/company/{company_name}/", response_class=HTMLResponse)
def get_company_profile(request: Request, company_name: str):
    company_name_cleaned = company_name.strip().lower()
    company_id = company_name_to_id.get(company_name_cleaned)

    if company_id is None:
        raise HTTPException(status_code=404, detail="Company not found")

    data = company_attr.get(company_id, {})
    roles_data = get_roles_data(company_id)
    cities_data = get_cities_data(company_id)
    total_openings = get_total_job_openings(company_id)
    top_roles_salary = get_top_roles_salary(company_id)
    top_hiring_states = get_top_hiring_states(company_id)
    total_cities_with_jobs = get_total_cities_with_job_postings(company_id)

    # Global insights
    job_openings_by_industry = get_total_job_openings_by_industry()
    total_companies_hiring = get_total_companies_hiring()
    job_openings_by_city = get_total_job_openings_by_city()
    print("DEBUG: Total cites:", json.dumps(total_cities_with_jobs))  # Debugging


    return templates.TemplateResponse("company_profile.html", {
        "request": request,
        "company_name": company_name_cleaned,
        "company_names": list(company_name_to_id.keys()),
        "industry": data.get("industry_list", "Unknown"),
        "location": f"{data.get('city', 'Unknown')}, {data.get('state', 'Unknown')}",
        "founded": data.get("founded", "Unknown"),
        "website": data.get('website', 'Unknown').lower(),
        "total_openings": total_openings,
        "roles_data": roles_data,
        "cities_data": cities_data,
        "top_roles_salary": top_roles_salary,
        "job_openings_by_industry": job_openings_by_industry,
        "total_companies_hiring": total_companies_hiring,
        "job_openings_by_city": job_openings_by_city,
        "total_cities_with_jobs": total_cities_with_jobs,
        "top_hiring_states" : top_hiring_states,
    })
