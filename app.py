import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Supermarket Sales Analysis",
    page_icon="🛒",
    layout="wide",
)

DATA_PATH = Path(__file__).parent / "data" / "supermarket_sales.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH, parse_dates=["Date"])
    # Recalculate sales so the project demonstrates the requested data-analysis step.
    df["Calculated Sales"] = df["Quantity"] * df["Unit Price"]
    df["Sales Check"] = (df["Sales"] - df["Calculated Sales"]).abs() < 0.01
    return df

df = load_data()

st.title("🛒 Supermarket Sales Analysis")
st.caption("Data Analytics Project • 500 supermarket sales transactions")

# Sidebar filters
st.sidebar.header("Filters")
branches = st.sidebar.multiselect(
    "Branch", sorted(df["Branch"].unique()), default=sorted(df["Branch"].unique())
)
categories = st.sidebar.multiselect(
    "Category", sorted(df["Category"].unique()), default=sorted(df["Category"].unique())
)
customer_types = st.sidebar.multiselect(
    "Customer Type", sorted(df["Customer Type"].unique()), default=sorted(df["Customer Type"].unique())
)
payments = st.sidebar.multiselect(
    "Payment Method", sorted(df["Payment"].unique()), default=sorted(df["Payment"].unique())
)

filtered = df[
    df["Branch"].isin(branches)
    & df["Category"].isin(categories)
    & df["Customer Type"].isin(customer_types)
    & df["Payment"].isin(payments)
].copy()

# KPI cards
total_sales = filtered["Sales"].sum()
transactions = len(filtered)
avg_sale = filtered["Sales"].mean() if transactions else 0
avg_rating = filtered["Rating"].mean() if transactions else 0
quantity = filtered["Quantity"].sum()

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Sales", f"₹{total_sales:,.2f}")
c2.metric("Transactions", f"{transactions:,}")
c3.metric("Average Sale", f"₹{avg_sale:,.2f}")
c4.metric("Average Rating", f"{avg_rating:.2f}/5")
c5.metric("Units Sold", f"{quantity:,}")

st.divider()

tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "🔎 Live Analysis", "📋 Data"])

with tab1:
    col1, col2 = st.columns(2)

    with col1:
        product_sales = (
            filtered.groupby("Product", as_index=False)["Sales"]
            .sum().sort_values("Sales", ascending=False)
        )
        fig = px.bar(
            product_sales.head(10),
            x="Sales", y="Product", orientation="h",
            title="Top 10 Products by Sales",
            text_auto=".2f"
        )
        fig.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        category_sales = (
            filtered.groupby("Category", as_index=False)["Sales"]
            .sum().sort_values("Sales", ascending=False)
        )
        fig = px.pie(
            category_sales, names="Category", values="Sales",
            title="Sales by Category", hole=0.35
        )
        st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        branch_sales = (
            filtered.groupby(["Branch", "City"], as_index=False)["Sales"]
            .sum().sort_values("Sales", ascending=False)
        )
        branch_sales["Branch-City"] = branch_sales["Branch"] + " - " + branch_sales["City"]
        fig = px.bar(
            branch_sales, x="Branch-City", y="Sales",
            title="Sales by Branch", text_auto=".2f"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        payment_counts = filtered["Payment"].value_counts().reset_index()
        payment_counts.columns = ["Payment", "Transactions"]
        fig = px.bar(
            payment_counts, x="Payment", y="Transactions",
            title="Transactions by Payment Method", text_auto=True
        )
        st.plotly_chart(fig, use_container_width=True)

    monthly = (
        filtered.assign(Month=filtered["Date"].dt.to_period("M").astype(str))
        .groupby("Month", as_index=False)["Sales"].sum()
    )
    fig = px.line(
        monthly, x="Month", y="Sales", markers=True,
        title="Monthly Sales Trend"
    )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Live Analysis")

    p = filtered.groupby("Product")["Sales"].sum().sort_values(ascending=False)
    b = filtered.groupby(["Branch", "City"])["Sales"].sum().sort_values(ascending=False)
    cat = filtered.groupby("Category")["Sales"].sum().sort_values(ascending=False)
    pay = filtered["Payment"].value_counts()
    cust = filtered.groupby("Customer Type")["Sales"].mean()

    if len(filtered):
        top_product = p.index[0]
        top_branch = b.index[0]
        top_category = cat.index[0]
        top_payment = pay.index[0]
        avg_rating_live = filtered["Rating"].mean()

        st.markdown(f"**Which product generates the highest sales?**  \n"
                    f"**{top_product} — ₹{p.iloc[0]:,.2f}**")
        st.markdown(f"**Which branch performs best?**  \n"
                    f"**Branch {top_branch[0]} ({top_branch[1]}) — ₹{b.iloc[0]:,.2f}**")
        st.markdown(f"**Which category sells the most?**  \n"
                    f"**{top_category} — ₹{cat.iloc[0]:,.2f}**")
        st.markdown(f"**What is the most popular payment method?**  \n"
                    f"**{top_payment} — {pay.iloc[0]} transactions**")
        st.markdown("**Do Members spend more than Normal customers?**")
        for customer_type, value in cust.items():
            st.write(f"- {customer_type}: average transaction ₹{value:,.2f}")
        st.markdown(f"**What is the average customer rating?**  \n"
                    f"**{avg_rating_live:.2f} out of 5**")

        st.subheader("Business Decisions")
        st.write(
            "Keep adequate stock for high-selling products and categories, "
            "study the strong-performing branch, monitor payment preferences, "
            "and use customer spending/rating patterns to improve service and offers."
        )

        st.subheader("Data Quality Check")
        good = int(filtered["Sales Check"].sum())
        st.write(f"{good} of {len(filtered)} displayed transactions satisfy "
                 f"Sales = Quantity × Unit Price within ₹0.01.")

with tab3:
    st.subheader("Filtered Transactions")
    st.dataframe(
        filtered.sort_values("Date", ascending=False),
        use_container_width=True,
        hide_index=True
    )

st.divider()
st.subheader("Project Methodology")
st.markdown("""
1. Load the supermarket sales dataset.
2. Check the data and validate the Sales calculation.
3. Calculate Sales = Quantity × Unit Price.
4. Group and summarize sales by product, branch, category, payment method and customer type.
5. Create charts for comparison.
6. Convert the results into business decisions.
""")
st.caption("Source: SUPER MARKET DATA.pdf supplied with this project.")
