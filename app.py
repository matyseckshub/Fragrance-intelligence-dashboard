import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Load your completed dataset
df = pd.read_csv("/Users/matyseck/Desktop/fragrance_intelligence_master.csv")

st.set_page_config(page_title="Fragrance Intelligence", layout="wide")
st.title("Luxury Fragrance & Cultural Intelligence Dashboard 🧪")

# 2. Metric Cards for quick high-level insights
col1, col2, col3 = st.columns(3)
col1.metric("Total Fragrances Analyzed", len(df))
col2.metric("Highest Rated Fragrance", df.loc[df['rating'].idxmax()]['name'])
col3.metric("Most Viral (TikTok Views)", f"{df['tiktok_views_est'].max():,}")

st.markdown("---")

# 3. Interactive Scatter Plot: Price vs Quality
st.subheader("🤑 Financial Intelligence: Does Price Dictate Quality?")
fig_price = px.scatter(
    df, 
    x="price_usd_100ml", 
    y="rating", 
    color="style_category",
    hover_name="name",
    size="vote_count",
    labels={"price_usd_100ml": "Price per 100ml (USD)", "rating": "Fragrantica Rating"},
    title="Price vs. Consumer Rating (Bubble size represents total vote count)"
)
st.plotly_chart(fig_price, use_container_width=True)

# 4. Interactive Scatter Plot: Sentiment Matrix
st.subheader("🎭 Psychological Intelligence: Crowd-Pleasers vs. Cult Divisiveness")
fig_polar = px.scatter(
    df,
    x="appreciation_score",
    y="polarisation_score",
    hover_name="name",
    color="style_category",
    labels={"appreciation_score": "Appreciation Score %", "polarisation_score": "Polarization Score %"},
    title="The Sentiment Grid"
)
st.plotly_chart(fig_polar, use_container_width=True)

# 5. Raw Data Explorer
st.subheader("📊 Raw Intelligence Data Grid")
st.dataframe(df)
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

st.title("Luxury Fragrance Intelligence Dashboard")

# Load Dataset
csv_path = os.path.expanduser("~/Desktop/fragrance_intelligence_master.csv")
df = pd.read_csv(csv_path)

# Define your exact custom palette globally for the web app
user_palette = ["#EC6530", "#FFAE6E", "#FFE3E3", "#9FA1FF", "#D51C39", "#FFE394"]

# Create an interactive selector for your tabs
tab1, tab2, tab3 = st.tabs(["Market Matrix", "Note Popularity", "Target Personas"])

with tab1:
    st.subheader("Quality Perception vs. Cultural Attention")
    category_summary = df.groupby('style_category').agg({'rating': 'mean', 'tiktok_views_est': 'mean'}).reset_index()
    category_summary = category_summary.sort_values(by='rating', ascending=False).reset_index(drop=True)
    
    fig, ax1 = plt.subplots(figsize=(10, 5))
    bars = sns.barplot(data=category_summary, x='style_category', y='rating', hue='style_category', palette=user_palette, legend=False, ax=ax1)
    ax1.set_ylim(3.5, 4.4)
    
    # Value labels on top of bars
    for bar in bars.patches:
        ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.01, f'{bar.get_height():.2f}', ha="center", va="bottom", fontsize=9, fontweight='bold')
        
    ax2 = ax1.twinx()
    sns.lineplot(data=category_summary, x='style_category', y=category_summary['tiktok_views_est']/1e6, color='#4A5568', marker='o', linewidth=3, ax=ax2, sort=False)
    ax2.grid(False)
    
    st.pyplot(fig)

with tab2:
    st.subheader("Top 10 Most Frequent Raw Notes")
    # Note frequency counting logic...
    # (Renders your horizontal Pareto chart inside the live web framework)

with tab3:
    st.subheader("Data-Engineered Segment Clusters")
    # Scatter plot logic...
    import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import warnings
from collections import Counter

# Mute minor backend layout warnings
warnings.filterwarnings('ignore')
sns.set_theme(style="whitegrid")

# 1. STREAMLIT APP ENGINE CONFIG
st.set_page_config(page_title="Fragrance Market Intelligence Labs", layout="wide")
st.title("🧪 Fragrance Preference Intelligence Platform")
st.markdown("---")

# 2. DATA ACQUISITION LAYER
csv_path = os.path.expanduser("~/Desktop/fragrance_intelligence_master.csv")
if not os.path.exists(csv_path):
    st.error(f"❌ Error: Could not find your master database at {csv_path}. Please place your CSV file on your Desktop.")
    st.stop()

df = pd.read_csv(csv_path)

# Your exact custom branding hex palette
user_palette = ["#EC6530", "#FFAE6E", "#FFE3E3", "#9FA1FF", "#D51C39", "#FFE394"]

# Dynamic fallback mechanism for column validation
persona_col = next((c for c in df.columns if 'persona' in c.lower()), None)
if persona_col is None:
    persona_col = 'style_category' if 'style_category' in df.columns else df.columns[1]

# 3. EXECUTIVE KPIS LAYER
col1, col2, col3, col4 = st.columns(4)
col1.metric("Database Sample Size", f"{len(df)} Iconic Fragrances")
col2.metric("Most Viral Family", "Gourmand (166M Avg Views)")
col3.metric("Highest Consumer Satisfaction", "Woody / Spicy (4.21/5)")
col4.metric("Top Formula Anchor Ingredients", "Jasmine / Vanilla")

st.markdown("---")

# 4. TAB-BASED SEPARATION INTERFACE
tab1, tab2, tab3 = st.tabs([
    "📈 Market Matrix (Quality vs. Hype)", 
    "🌿 Note Popularity (Ingredient Matrix)", 
    "🎭 Target Customer Segments"
])

# ==========================================
# TAB 1: MARKET MATRIX INTERACTIVE PANEL
# ==========================================
with tab1:
    st.header("Quality Perception vs. Cultural Attention")
    st.markdown("###### How consumer ratings directly weigh against digital trend velocity across product families.")
    
    category_summary = df.groupby('style_category').agg({'rating': 'mean', 'tiktok_views_est': 'mean'}).reset_index()
    category_summary = category_summary.sort_values(by='rating', ascending=False).reset_index(drop=True)
    
    fig1, ax1 = plt.subplots(figsize=(11, 5))
    bars = sns.barplot(
        data=category_summary, x='style_category', y='rating', 
        hue='style_category', palette=user_palette, alpha=0.9, legend=False, ax=ax1
    )
    ax1.set_ylim(3.5, 4.4)
    ax1.set_ylabel('Average Rating (out of 5)', fontweight='bold')
    ax1.set_xlabel('Style Category', fontweight='bold')
    
    # Render value figures on top of the category bars
    for bar in bars.patches:
        h = bar.get_height()
        if h > 0:
            ax1.text(
                bar.get_x() + bar.get_width()/2., h + 0.01, f'{h:.2f}', 
                ha="center", va="bottom", fontsize=9, fontweight='bold', color='#2C3E50'
            )
            
    ax2 = ax1.twinx()
    sns.lineplot(
        data=category_summary, x='style_category', y=category_summary['tiktok_views_est']/1e6, 
        color='#4A5568', marker='o', linewidth=3, markersize=8, ax=ax2, sort=False
    )
    ax2.set_ylabel('Average TikTok Views (Millions)', fontweight='bold', color='#4A5568')
    ax2.tick_params(axis='y', labelcolor='#4A5568')
    ax2.grid(False)
    
    st.pyplot(fig1)

# ==========================================
# TAB 2: NOTE POPULARITY FREQUENCY PANEL
# ==========================================
with tab2:
    st.header("Olfactive Component Frequency Matrix")
    st.markdown("###### Text parsing results counting the recurrence of raw ingredients inside formula profiles.")
    
    note_cols = [c for c in ['top_notes', 'heart_notes', 'base_notes'] if c in df.columns]
    if note_cols:
        all_notes = []
        for col in note_cols:
            for val in df[col].dropna():
                all_notes.extend([n.strip() for n in str(val).split(',')])
        
        if all_notes:
            note_counts = Counter(all_notes).most_common(10)
            note_df = pd.DataFrame(note_counts, columns=['Note', 'Frequency'])
            
            fig2, ax_notes = plt.subplots(figsize=(10, 5))
            sns.barplot(
                x='Frequency', y='Note', data=note_df, 
                hue='Note', palette=user_palette, legend=False, ax=ax_notes
            )
            ax_notes.set_title('Top 10 Most Frequent Raw Notes Across Dataset', fontsize=12, fontweight='bold')
            ax_notes.set_xlabel('Total Documented Occurrences in Formulas', fontweight='bold')
            ax_notes.set_ylabel('Raw Ingredient Label', fontweight='bold')
            
            st.pyplot(fig2)
        else:
            st.info("ℹ️ No note strings available in your dataset columns to parse.")
    else:
        st.warning("⚠️ Could not locate note columns ('top_notes', 'heart_notes', 'base_notes') in your CSV file.")

# ==========================================
# TAB 3: TARGET PERSONAS CLUSTERING PANEL
# ==========================================
with tab3:
    st.header("Algorithmic Market Mapping")
    st.markdown("###### Multi-dimensional evaluation checking pricing limits against dynamic social validation signals.")
    
    fig3, ax_scatter = plt.subplots(figsize=(11, 5.5))
    
    x_var = 'price_usd_100ml' if 'price_usd_100ml' in df.columns else df.select_dtypes(include=['number']).columns[0]
    y_var = 'tiktok_views_est' if 'tiktok_views_est' in df.columns else df.select_dtypes(include=['number']).columns[1]
    size_var = 'rating' if 'rating' in df.columns else None
    
    sns.scatterplot(
        data=df, x=x_var, y=y_var, hue=persona_col, size=size_var,
        sizes=(30, 200), palette=user_palette, alpha=0.85, ax=ax_scatter
    )
    ax_scatter.set_yscale('symlog', linthresh=1e6)
    ax_scatter.set_xlabel(f'{x_var.replace("_", " ").title()} (USD)', fontweight='bold')
    ax_scatter.set_ylabel(f'{y_var.replace("_", " ").title()} (Log Scale)', fontweight='bold')
    
    # Fix legend formatting and positioning
    ax_scatter.legend(title=persona_col.replace('_', ' ').title(), bbox_to_anchor=(1.02, 1), loc='upper left')
    
    st.pyplot(fig3)

# 5. DATA ENGINE VIEW LAYER
st.markdown("---")
st.subheader("📋 Complete Structured Analytics Ledger")
st.dataframe(df[['name', 'brand', 'style_category', 'price_usd_100ml', 'rating']].dropna())