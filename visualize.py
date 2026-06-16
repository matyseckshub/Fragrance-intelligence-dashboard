import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

# Mute all terminal warnings to keep your console completely clean
warnings.filterwarnings('ignore')

# Set clean style profiles
sns.set_theme(style="whitegrid")

# 1. READ DATABASE FILE DIRECTLY FROM DESKTOP
csv_path = os.path.expanduser("~/Desktop/fragrance_intelligence_master.csv")
df = pd.read_csv(csv_path)

# AUTOMATIC COLUMN FINDER: Finds any column containing the word 'persona'
persona_col = None
for col in df.columns:
    if 'persona' in col.lower():
        persona_col = col
        break

if persona_col is None:
    persona_col = 'style_category' if 'style_category' in df.columns else df.columns[1]

# ==========================================================
# CHART 1: QUALITY HIERARCHY VS. SOCIAL ATTENTION FOOTPRINT
# ==========================================================
if 'style_category' in df.columns and 'rating' in df.columns and 'tiktok_views_est' in df.columns:
    category_summary = df.groupby('style_category').agg({'rating': 'mean', 'tiktok_views_est': 'mean'}).reset_index()
    
    # Sort categories to match your original narrative flow
    category_summary = category_summary.sort_values(by='rating', ascending=False).reset_index(drop=True)

    # Apply your exact preferred hex color palette
    user_palette = ["#EC6530", "#FFAE6E", "#FFE3E3", "#9FA1FF", "#D51C39", "#FFE394"]
    # Ensure palette length matches data rows
    if len(category_summary) > len(user_palette):
        user_palette = user_palette * 2
    user_palette = user_palette[:len(category_summary)]

    fig, ax1 = plt.subplots(figsize=(11, 6))
    
    # Draw bars with unique colors from your palette
    bars = sns.barplot(
        data=category_summary, 
        x='style_category', 
        y='rating', 
        hue='style_category', 
        palette=user_palette, 
        alpha=0.9, 
        legend=False,
        ax=ax1
    )
    
    # Add exact numeric values on top of the bars for immediate scannability
    for bar in bars.patches:
        height = bar.get_height()
        if height > 0:
            ax1.text(
                bar.get_x() + bar.get_width()/2.,
                height + 0.01,
                f'{height:.2f}',
                ha="center", va="bottom", fontsize=10, fontweight='bold', color='#2C3E50'
            )

    ax1.set_ylim(3.5, 4.4)
    ax1.set_ylabel('Average Rating (out of 5)', fontweight='bold', labelpad=10)
    ax1.set_xlabel('Style Category', fontweight='bold', labelpad=10)

    # Secondary Axis for Hype Line
    ax2 = ax1.twinx()
    sns.lineplot(
        data=category_summary, 
        x='style_category', 
        y=category_summary['tiktok_views_est']/1e6, 
        color='#4A5568', # Muted deep gray line so your color bars remain the main focus
        marker='o', 
        linewidth=3, 
        markersize=8,
        ax=ax2, 
        sort=False
    )
    ax2.set_ylabel('Average TikTok Views (Millions)', fontweight='bold', color='#4A5568', labelpad=10)
    ax2.tick_params(axis='y', labelcolor='#4A5568')
    ax2.grid(False) # Turn off overlapping secondary gridlines

    plt.title('Market Matrix: Quality Perception vs. Cultural Attention', fontsize=14, fontweight='bold', pad=25)
    plt.tight_layout()
    plt.savefig(os.path.expanduser("~/Desktop/Python_style_hierarchy.png"), dpi=300)
    plt.close()

# ==========================================================
# CHART 2: NOTE FREQUENCY PARETO DISTRIBUTION
# ==========================================================
note_cols = [c for c in ['top_notes', 'heart_notes', 'base_notes'] if c in df.columns]
if note_cols:
    from collections import Counter
    all_notes = []
    for col in note_cols:
        for val in df[col].dropna():
            all_notes.extend([n.strip() for n in str(val).split(',')])

    if all_notes:
        note_counts = Counter(all_notes).most_common(10)
        note_df = pd.DataFrame(note_counts, columns=['Note', 'Frequency'])

        plt.figure(figsize=(10, 5))
        sns.barplot(x='Frequency', y='Note', data=note_df, hue='Note', palette=user_palette, legend=False)
        plt.title('Top 10 Most Frequent Raw Notes Across Dataset', fontsize=14, fontweight='bold', pad=15)
        plt.xlabel('Occurrences in Formulas', fontweight='bold')
        plt.ylabel('Raw Material Ingredient', fontweight='bold')
        plt.tight_layout()
        plt.savefig(os.path.expanduser("~/Desktop/Python_note_popularity.png"), dpi=300)
        plt.close()

# ==========================================================
# CHART 3: CONSUMER PERSONAS TARGET SEGMENTATION MAP
# ==========================================================
plt.figure(figsize=(11, 6.5))

x_var = 'price_usd_100ml' if 'price_usd_100ml' in df.columns else df.select_dtypes(include=['number']).columns[0]
y_var = 'tiktok_views_est' if 'tiktok_views_est' in df.columns else df.select_dtypes(include=['number']).columns[1]
size_var = 'rating' if 'rating' in df.columns else None

sns.scatterplot(
    data=df, 
    x=x_var, 
    y=y_var, 
    hue=persona_col, 
    size=size_var,
    sizes=(40, 240),
    palette=user_palette,
    alpha=0.85
)
plt.yscale('symlog', linthresh=1e6)
plt.title('Data-Engineered Consumer Segmentation Map', fontsize=14, fontweight='bold', pad=15)
plt.xlabel(f'{x_var.replace("_", " ").title()} (USD)', fontweight='bold')
plt.ylabel(f'{y_var.replace("_", " ").title()} (Log Scale)', fontweight='bold')
plt.legend(title=persona_col.replace('_', ' ').title(), bbox_to_anchor=(1.02, 1), loc='upper left')
plt.tight_layout()
plt.savefig(os.path.expanduser("~/Desktop/Python_consumer_personas.png"), dpi=300)
plt.close()

print("\n SUCCESS: 3 Custom-Branded Data Visualizations Saved to Desktop!")
