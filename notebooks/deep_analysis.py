import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.patches as mpatches
from scipy import stats

# ── Setup ────────────────────────────────────────────────────────────────────
DARK_BG = '#0a0f1e'
CARD_BG  = '#111827'
BLUE     = '#3b82f6'
GREEN    = '#10b981'
RED      = '#ef4444'
AMBER    = '#f59e0b'
PURPLE   = '#8b5cf6'
TEXT     = '#e8eaf0'
MUTED    = '#7a8aaa'

REGION_COLORS = {
    'Nairobi':       '#3b82f6',
    'Central':       '#10b981',
    'Coast':         '#f59e0b',
    'Eastern':       '#8b5cf6',
    'North Eastern': '#ef4444',
    'Nyanza':        '#06b6d4',
    'Rift Valley':   '#f97316',
    'Western':       '#ec4899',
}

def style_chart(fig, axes):
    fig.patch.set_facecolor(DARK_BG)
    if not hasattr(axes, '__iter__'):
        axes = [axes]
    for ax in axes:
        ax.set_facecolor(CARD_BG)
        ax.tick_params(colors=MUTED, labelsize=8)
        ax.xaxis.label.set_color(MUTED)
        ax.yaxis.label.set_color(MUTED)
        ax.title.set_color(TEXT)
        for spine in ax.spines.values():
            spine.set_edgecolor('#1e2d4a')

plt.rcParams['figure.facecolor'] = DARK_BG
plt.rcParams['savefig.facecolor'] = DARK_BG

# ── Load & prepare data ───────────────────────────────────────────────────────
df = pd.read_csv('data/county_data.csv')
df['budget_per_person'] = (df['budget_billion'] * 1_000_000_000) / df['population_2024']
df['budget_per_person'] = df['budget_per_person'].round(0).astype(int)
sorted_df = df.sort_values('budget_per_person', ascending=False).reset_index(drop=True)

print("=" * 60)
print("  KENYA COUNTY BUDGET — DEEP ANALYSIS")
print("  FY 2023/24 | All 47 Counties")
print("=" * 60)
print(f"  Counties     : {len(df)}")
print(f"  Population   : {df['population_2024'].sum():,}")
print(f"  Total Budget : KES {df['budget_billion'].sum():.1f} billion")
print(f"  Avg/Person   : KES {df['budget_per_person'].mean():,.0f}")
print(f"  Median/Person: KES {df['budget_per_person'].median():,.0f}")
print(f"  Std Dev      : KES {df['budget_per_person'].std():,.0f}")
print("=" * 60)


# ════════════════════════════════════════════════════════════════
# SECTION 1 — GINI COEFFICIENT
# ════════════════════════════════════════════════════════════════
def gini_coefficient(values):
    """Calculate Gini coefficient for a distribution."""
    arr = np.sort(np.array(values, dtype=float))
    n = len(arr)
    cumsum = np.cumsum(arr)
    return (2 * np.sum((np.arange(1, n + 1)) * arr) - (n + 1) * cumsum[-1]) / (n * cumsum[-1])

gini = gini_coefficient(df['budget_per_person'])
print(f"\n📊 GINI COEFFICIENT (Budget Per Person): {gini:.4f}")
print(f"   → {'High inequality' if gini > 0.35 else 'Moderate inequality' if gini > 0.25 else 'Low inequality'}")
print(f"   (0 = perfect equality, 1 = total inequality)")

# Lorenz curve
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
style_chart(fig, axes)

sorted_vals = np.sort(df['budget_per_person'].values)
n = len(sorted_vals)
lorenz_x = np.concatenate([[0], np.arange(1, n + 1) / n])
lorenz_y = np.concatenate([[0], np.cumsum(sorted_vals) / sorted_vals.sum()])

axes[0].plot(lorenz_x, lorenz_y, color=BLUE, linewidth=2.5, label=f'Lorenz Curve (Gini = {gini:.3f})')
axes[0].plot([0, 1], [0, 1], color=MUTED, linestyle='--', linewidth=1.2, label='Perfect Equality')
axes[0].fill_between(lorenz_x, lorenz_y, lorenz_x, alpha=0.15, color=RED)
axes[0].set_title('Lorenz Curve — Budget Per Person Inequality', fontsize=11, fontweight='bold')
axes[0].set_xlabel('Cumulative Share of Counties')
axes[0].set_ylabel('Cumulative Share of Budget/Person')
axes[0].legend(facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=9)
axes[0].set_xlim(0, 1); axes[0].set_ylim(0, 1)

# Distribution histogram
axes[1].hist(df['budget_per_person'], bins=12, color=BLUE, edgecolor=DARK_BG, linewidth=0.5, alpha=0.85)
axes[1].axvline(df['budget_per_person'].mean(), color=AMBER, linestyle='--', linewidth=1.5, label=f"Mean: KES {int(df['budget_per_person'].mean()):,}")
axes[1].axvline(df['budget_per_person'].median(), color=GREEN, linestyle='--', linewidth=1.5, label=f"Median: KES {int(df['budget_per_person'].median()):,}")
axes[1].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
axes[1].set_title('Distribution of Budget Per Person', fontsize=11, fontweight='bold')
axes[1].set_xlabel('KES per Person')
axes[1].set_ylabel('Number of Counties')
axes[1].legend(facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=9)

plt.tight_layout()
plt.savefig('dashboards/gini_analysis.png', dpi=150, bbox_inches='tight')
plt.show()
print("✅ Chart saved: dashboards/gini_analysis.png")


# ════════════════════════════════════════════════════════════════
# SECTION 2 — REGIONAL ANALYSIS
# ════════════════════════════════════════════════════════════════
print("\n\n📍 REGIONAL ANALYSIS")
print("-" * 60)

regional = df.groupby('region').agg(
    counties        = ('county', 'count'),
    total_pop       = ('population_2024', 'sum'),
    total_budget    = ('budget_billion', 'sum'),
    avg_bpp         = ('budget_per_person', 'mean'),
    min_bpp         = ('budget_per_person', 'min'),
    max_bpp         = ('budget_per_person', 'max'),
).reset_index()

regional['budget_per_person'] = ((regional['total_budget'] * 1e9) / regional['total_pop']).astype(int)
regional = regional.sort_values('budget_per_person', ascending=False)

print(regional[['region', 'counties', 'total_pop', 'total_budget', 'budget_per_person']].to_string(index=False))

fig, axes = plt.subplots(1, 3, figsize=(18, 5))
style_chart(fig, axes)

# Regional budget per person
colors_r = [REGION_COLORS[r] for r in regional['region']]
axes[0].barh(regional['region'], regional['budget_per_person'], color=colors_r, edgecolor=DARK_BG, linewidth=0.4)
axes[0].axvline(df['budget_per_person'].mean(), color=AMBER, linestyle='--', linewidth=1.2, label='National Avg')
axes[0].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
axes[0].set_title('Budget Per Person by Region', fontsize=11, fontweight='bold')
axes[0].set_xlabel('KES per Person')
axes[0].invert_yaxis()
axes[0].tick_params(axis='y', labelsize=9, colors=TEXT)
axes[0].legend(facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=8)

# Regional total budget share (pie)
wedge_colors = [REGION_COLORS[r] for r in regional['region']]
wedges, texts, autotexts = axes[1].pie(
    regional['total_budget'],
    labels=regional['region'],
    autopct='%1.1f%%',
    colors=wedge_colors,
    startangle=90,
    pctdistance=0.75,
    textprops={'color': TEXT, 'fontsize': 7.5}
)
for at in autotexts:
    at.set_color(DARK_BG)
    at.set_fontsize(7)
axes[1].set_title('Share of Total Budget by Region', fontsize=11, fontweight='bold')

# Min-max range per region (spread)
axes[2].barh(regional['region'], regional['max_bpp'] - regional['min_bpp'],
             left=regional['min_bpp'], color=colors_r, alpha=0.6, edgecolor=DARK_BG, linewidth=0.4, height=0.5)
axes[2].scatter(regional['budget_per_person'], regional['region'], color=TEXT, s=40, zorder=5, label='Regional Avg')
axes[2].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
axes[2].set_title('Budget/Person Range Within Each Region', fontsize=11, fontweight='bold')
axes[2].set_xlabel('KES per Person (min → max)')
axes[2].invert_yaxis()
axes[2].tick_params(axis='y', labelsize=9, colors=TEXT)
axes[2].legend(facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=8)

plt.tight_layout()
plt.savefig('dashboards/regional_analysis.png', dpi=150, bbox_inches='tight')
plt.show()
print("✅ Chart saved: dashboards/regional_analysis.png")


# ════════════════════════════════════════════════════════════════
# SECTION 3 — CORRELATION ANALYSIS
# ════════════════════════════════════════════════════════════════
print("\n\n🔗 CORRELATION ANALYSIS")
print("-" * 60)

corr_bp, pval_bp = stats.pearsonr(df['population_2024'], df['budget_billion'])
corr_bpp, pval_bpp = stats.pearsonr(df['population_2024'], df['budget_per_person'])

print(f"Population vs Absolute Budget   : r = {corr_bp:.3f}  (p = {pval_bp:.4f}) {'✅ significant' if pval_bp < 0.05 else '❌ not significant'}")
print(f"Population vs Budget Per Person : r = {corr_bpp:.3f}  (p = {pval_bpp:.4f}) {'✅ significant' if pval_bpp < 0.05 else '❌ not significant'}")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
style_chart(fig, axes)

# Scatter 1: Population vs Absolute Budget
colors_scatter = [REGION_COLORS[r] for r in df['region']]
axes[0].scatter(df['population_2024'] / 1e6, df['budget_billion'],
                c=colors_scatter, s=70, alpha=0.85, edgecolors='#1e2d4a', linewidth=0.6)

# Regression line
m, b, r, p, se = stats.linregress(df['population_2024'] / 1e6, df['budget_billion'])
x_line = np.linspace(df['population_2024'].min() / 1e6, df['population_2024'].max() / 1e6, 100)
axes[0].plot(x_line, m * x_line + b, color=AMBER, linewidth=1.8, linestyle='--', label=f'r = {corr_bp:.3f}')

for _, row in df.iterrows():
    if row['county'] in ['Nairobi', 'Lamu', 'Nakuru', 'Kiambu', 'Turkana']:
        axes[0].annotate(row['county'], (row['population_2024'] / 1e6, row['budget_billion']),
                         textcoords='offset points', xytext=(6, 4), fontsize=7.5, color=TEXT)

axes[0].set_title('Population vs Absolute Budget', fontsize=11, fontweight='bold')
axes[0].set_xlabel('Population (millions)')
axes[0].set_ylabel('Budget (KES Billions)')
axes[0].legend(facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=9)

legend_patches = [mpatches.Patch(color=v, label=k) for k, v in REGION_COLORS.items()]
axes[0].legend(handles=legend_patches, facecolor=CARD_BG, edgecolor='#1e2d4a',
               labelcolor=TEXT, fontsize=7, ncol=2, loc='upper left')

# Scatter 2: Population vs Budget Per Person
axes[1].scatter(df['population_2024'] / 1e6, df['budget_per_person'],
                c=colors_scatter, s=70, alpha=0.85, edgecolors='#1e2d4a', linewidth=0.6)

m2, b2, r2, p2, _ = stats.linregress(df['population_2024'] / 1e6, df['budget_per_person'])
axes[1].plot(x_line, m2 * x_line + b2, color=AMBER, linewidth=1.8, linestyle='--', label=f'r = {corr_bpp:.3f}')

for _, row in df.iterrows():
    if row['county'] in ['Nairobi', 'Lamu', 'Nakuru', 'Kiambu', 'Marsabit']:
        axes[1].annotate(row['county'], (row['population_2024'] / 1e6, row['budget_per_person']),
                         textcoords='offset points', xytext=(6, 4), fontsize=7.5, color=TEXT)

axes[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
axes[1].set_title('Population vs Budget Per Person', fontsize=11, fontweight='bold')
axes[1].set_xlabel('Population (millions)')
axes[1].set_ylabel('Budget Per Person (KES)')
axes[1].legend(facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=9)

plt.tight_layout()
plt.savefig('dashboards/correlation_analysis.png', dpi=150, bbox_inches='tight')
plt.show()
print("✅ Chart saved: dashboards/correlation_analysis.png")


# ════════════════════════════════════════════════════════════════
# SECTION 4 — OUTLIER & QUINTILE ANALYSIS
# ════════════════════════════════════════════════════════════════
print("\n\n🎯 QUINTILE ANALYSIS (Budget Per Person)")
print("-" * 60)

df['quintile'] = pd.qcut(df['budget_per_person'], q=5,
                          labels=['Q1 Bottom 20%', 'Q2', 'Q3 Middle', 'Q4', 'Q5 Top 20%'])

quintile_summary = df.groupby('quintile', observed=True).agg(
    counties=('county', 'count'),
    avg_bpp=('budget_per_person', 'mean'),
    counties_list=('county', lambda x: ', '.join(sorted(x)))
).reset_index()

for _, row in quintile_summary.iterrows():
    print(f"\n  {row['quintile']} | Avg: KES {int(row['avg_bpp']):,} | {row['counties']} counties")
    print(f"  → {row['counties_list']}")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
style_chart(fig, axes)

quintile_colors = [RED, '#f97316', AMBER, '#84cc16', GREEN]

axes[0].bar(quintile_summary['quintile'], quintile_summary['avg_bpp'],
            color=quintile_colors, edgecolor=DARK_BG, linewidth=0.4)
axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
axes[0].set_title('Average Budget Per Person by Quintile', fontsize=11, fontweight='bold')
axes[0].set_ylabel('KES per Person')
axes[0].tick_params(axis='x', labelsize=8, colors=TEXT)

# Boxplot per region
region_order = regional.sort_values('budget_per_person', ascending=False)['region'].tolist()
region_data = [df[df['region'] == r]['budget_per_person'].values for r in region_order]
bp = axes[1].boxplot(region_data, labels=region_order, patch_artist=True, vert=True)

for patch, region in zip(bp['boxes'], region_order):
    patch.set_facecolor(REGION_COLORS[region])
    patch.set_alpha(0.7)
for element in ['whiskers', 'caps', 'medians', 'fliers']:
    for item in bp[element]:
        item.set_color(TEXT)

axes[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
axes[1].set_title('Budget Per Person Distribution by Region', fontsize=11, fontweight='bold')
axes[1].set_ylabel('KES per Person')
axes[1].tick_params(axis='x', rotation=30, labelsize=8, colors=TEXT)

plt.tight_layout()
plt.savefig('dashboards/quintile_analysis.png', dpi=150, bbox_inches='tight')
plt.show()
print("✅ Chart saved: dashboards/quintile_analysis.png")


# ════════════════════════════════════════════════════════════════
# FINAL SUMMARY
# ════════════════════════════════════════════════════════════════
print("\n\n" + "=" * 60)
print("  KEY FINDINGS SUMMARY")
print("=" * 60)
print(f"  1. Gini coefficient of {gini:.3f} indicates {'high' if gini > 0.35 else 'moderate'} inequality")
print(f"     in per-capita budget allocation across counties.")
print(f"  2. Population vs budget/person correlation: r = {corr_bpp:.3f}")
print(f"     → Larger counties receive {'less' if corr_bpp < 0 else 'more'} per person.")
print(f"  3. {regional.iloc[0]['region']} region has the highest avg budget/person")
print(f"     at KES {regional.iloc[0]['budget_per_person']:,}.")
print(f"  4. {regional.iloc[-1]['region']} region has the lowest avg budget/person")
print(f"     at KES {regional.iloc[-1]['budget_per_person']:,}.")
print(f"  5. Top county ({sorted_df.iloc[0]['county']}) gets {sorted_df.iloc[0]['budget_per_person'] / sorted_df.iloc[-1]['budget_per_person']:.1f}x")
print(f"     more per person than bottom ({sorted_df.iloc[-1]['county']}).")
print("=" * 60)