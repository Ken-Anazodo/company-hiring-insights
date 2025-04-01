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

# Utility function to filter DataFrame
def filter_df(df, company_id):
    return df[df["company_id"] == company_id]


def get_roles_data(company_id):
    """Get job roles distribution for a company."""
    roles = filter_df(df_role, company_id).loc[:, ["job_family", "position_count", "wage_median"]]
    return roles.rename(columns={"job_family": "name", "position_count": "value"}).to_dict(orient="records")


def get_cities_data(company_id):
    """Get job postings distribution by city for a company."""
    filtered_df = filter_df(df_city, str(company_id))
    return filtered_df.loc[:, ["city", "position_count"]].rename(columns={"city": "name", "position_count": "value"}).to_dict(orient="records")


def get_total_job_openings(company_id):
    """Calculate total job openings for a company."""
    return filter_df(df_role, company_id)["position_count"].sum()


def get_top_roles_salary(company_id, top_n=3):
    """Get top N job roles with highest median salary for a company."""
    roles = filter_df(df_role, company_id).nlargest(top_n, "wage_median")
    return roles.loc[:, ["job_family", "wage_median"]].rename(columns={"job_family": "job", "wage_median": "salary"}).to_dict(orient="records")


def get_top_hiring_states(company_id, top_n=3):
    """Get top states where the company has job postings."""
    if "state_name" in df_city.columns:
        df_city["company_id"] = df_city["company_id"].astype(str)  # Ensure company_id is string
        company_id = str(company_id)  # Convert input to string
        filtered_df = filter_df(df_city, company_id)  # Use filter_df function

        if filtered_df.empty:
            return []  # Return empty list if no data is found
        
        state_totals = filtered_df.groupby("state_name", as_index=False)["position_count"].sum()

        return (
            state_totals.nlargest(min(top_n, len(state_totals)), "position_count")  # Prevent errors if fewer than top_n states exist
            .rename(columns={"state_name": "state", "position_count": "value"})
            .to_dict(orient="records")
        )
    
    return []



def get_total_job_openings_by_city():
    """Get total job openings by city."""
    city_totals = df_city.groupby("city", as_index=False)["position_count"].sum().nlargest(10, "position_count")
    return city_totals.rename(columns={"position_count": "value"}).to_dict(orient="records")


def get_total_job_openings_by_industry():
    """Get total job openings by industry."""
    industry_totals = df_role.merge(df_attr, on="company_id", how="left").groupby("industry_list", as_index=False)["position_count"].sum()
    return industry_totals.nlargest(10, "position_count").rename(columns={"position_count": "value"}).to_dict(orient="records")


def get_total_companies_hiring():
    """Get total number of unique companies hiring."""
    return df_attr["company_id"].nunique()


def get_total_cities_with_job_postings(company_id):
    """Get the total number of unique cities with job postings for a company."""
    total_cities = filter_df(df_city, str(company_id))["city"].nunique()
    print(f"DEBUG: Company ID = {company_id}, Total Cities = {total_cities}")  # Debugging
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
    print("DEBUG: Total cities:", json.dumps(total_cities_with_jobs))  # Debugging

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
        "top_hiring_states": top_hiring_states,
    })
