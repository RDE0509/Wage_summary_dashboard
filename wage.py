import streamlit as st
import pandas as pd
import plotly.express as px

# Load the dataset
csv_path = "combined_wagebill.csv"
df = pd.read_csv(csv_path)

# Ensure column names are standardized
df.columns = df.columns.str.strip().str.upper()

# Ensure Wage column is numeric
df["WAGE"] = pd.to_numeric(df["WAGE"], errors='coerce')

# Convert DATE to datetime
# df["DATE"] = pd.to_datetime(df["DATE"], errors='coerce')
# df.dropna(subset=["DATE"], inplace=True)
# # df["MONTH"] = df["DATE"].dt.strftime("%b-%Y")  # Format as Jan-2024
# df["QUARTER"] = df["MONTH"].dt.to_period("Q")  # Format as Q1-2024

# Streamlit UI
st.set_page_config(page_title="Wage Summary Dashboard", layout="wide")
st.title("Wage Summary Dashboard")

# Filters
companies = df["COMPANY"].unique()
departments = df["DEPARTMENT"].unique()
months = df["DATE"].unique()
# quarters = df["QUARTER"].astype(str).unique()

selected_company = st.selectbox("Select Company", options=["All"] + list(companies))
selected_department = st.selectbox("Select Department", options=["All"] + list(departments))
selected_month = st.selectbox("Select Month", options=["All"] + list(months))
# selected_quarter = st.selectbox("Select Quarter", options=["All"] + list(quarters))

# Apply Filters
filtered_df = df.copy()
if selected_company != "All":
    filtered_df = filtered_df[filtered_df["COMPANY"] == selected_company]
if selected_department != "All":
    filtered_df = filtered_df[filtered_df["DEPARTMENT"] == selected_department]
if selected_month != "All":
    filtered_df = filtered_df[filtered_df["DATE"] == selected_month]
# if selected_quarter != "All":
#     filtered_df = filtered_df[filtered_df["QUARTER"].astype(str) == selected_quarter]

# KPI Cards
total_wage = filtered_df["WAGE"].sum()
total_companies = filtered_df["COMPANY"].nunique()
total_departments = filtered_df["DEPARTMENT"].nunique()

col1, col2, col3 = st.columns(3)
col1.metric(label="Total Wage Bill", value=f"${total_wage:,.2f}")
col2.metric(label="Total Companies", value=total_companies)
col3.metric(label="Total Departments", value=total_departments)

# Wage by Company (3D Pie Chart)
company_grouped = filtered_df.groupby("COMPANY")["WAGE"].sum().reset_index()
fig_company = px.pie(company_grouped, names="COMPANY", values="WAGE", title="Total Wage by Company", hole=0.3)
st.plotly_chart(fig_company, use_container_width=True)

# Wage by Department
department_grouped = filtered_df.groupby("DEPARTMENT")["WAGE"].sum().reset_index()
fig_department = px.bar(department_grouped, x="DEPARTMENT", y="WAGE", title="Total Wage by Department", text_auto=True)
st.plotly_chart(fig_department, use_container_width=True)

# Monthly Wage Trend
df_monthly = filtered_df.groupby("DATE")["WAGE"].sum().reset_index()
fig_monthly = px.line(df_monthly, x="DATE", y="WAGE", title="Monthly Wage", markers=True)
st.plotly_chart(fig_monthly, use_container_width=True)

# # Quarterly Wage Trend
# df_quarterly = filtered_df.groupby("QUARTER")["WAGE"].sum().reset_index()
# fig_quarterly = px.line(df_quarterly, x="QUARTER", y="WAGE", title="Quarterly Wage Trend", markers=True)
# st.plotly_chart(fig_quarterly, use_container_width=True)

# Month-over-Month Change
df_monthly["WAGE_CHANGE"] = df_monthly["WAGE"].pct_change() * 100
fig_mom = px.bar(df_monthly, x="DATE", y="WAGE_CHANGE", title="Month-over-Month Wage Change (%)", text_auto=True)
st.plotly_chart(fig_mom, use_container_width=True)

# Department Wage %
df_department_pct = filtered_df.groupby("DEPARTMENT")["WAGE"].sum().reset_index()
df_department_pct["PERCENTAGE"] = df_department_pct["WAGE"] / df_department_pct["WAGE"].sum() * 100
fig_dept_pct = px.pie(df_department_pct, names="DEPARTMENT", values="PERCENTAGE", title="Department Wage %")
st.plotly_chart(fig_dept_pct, use_container_width=True)

# Run the app using: streamlit run script.py
