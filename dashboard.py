# # import streamlit as st
# # import pandas as pd
# # import numpy as np
# # import matplotlib.pyplot as plt
# # import matplotlib.ticker as mticker
# # import matplotlib.patches as mpatches
# # import plotly.express as px
# # import json
# # import urllib.request
# # from scipy import stats

# # st.set_page_config(page_title="Kenya County Budget Analysis", page_icon="🇰🇪", layout="wide")

# # st.markdown("""
# # <style>
# #     @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500&display=swap');
# #     html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
# #     .stApp { background-color: #0a0f1e; color: #e8eaf0; }
# #     h1, h2, h3 { font-family: 'Syne', sans-serif !important; }
# #     .hero-title { font-family: 'Syne', sans-serif; font-size: 3rem; font-weight: 800; color: #ffffff; line-height: 1.1; margin-bottom: 0.3rem; }
# #     .hero-sub { font-size: 1rem; color: #7a8aaa; margin-bottom: 2rem; font-weight: 300; letter-spacing: 0.05em; }
# #     .metric-card { background: linear-gradient(135deg, #111827 0%, #1a2340 100%); border: 1px solid #1e2d4a; border-radius: 12px; padding: 1.4rem 1.6rem; margin-bottom: 1rem; }
# #     .metric-label { font-size: 0.72rem; font-weight: 500; color: #5a6a8a; text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 0.4rem; }
# #     .metric-value { font-family: 'Syne', sans-serif; font-size: 1.9rem; font-weight: 700; color: #ffffff; line-height: 1; }
# #     .metric-accent { color: #3b82f6; } .metric-accent-green { color: #10b981; } .metric-accent-red { color: #ef4444; } .metric-accent-amber { color: #f59e0b; }
# #     .section-header { font-family: 'Syne', sans-serif; font-size: 1.1rem; font-weight: 700; color: #ffffff; text-transform: uppercase; letter-spacing: 0.08em; border-left: 3px solid #3b82f6; padding-left: 0.8rem; margin-bottom: 1rem; margin-top: 2rem; }
# #     .badge { display: inline-block; background: #1e3a5f; color: #60a5fa; font-size: 0.7rem; font-weight: 600; padding: 2px 10px; border-radius: 20px; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 0.5rem; }
# #     .insight-box { background: linear-gradient(135deg, #0f1f3d 0%, #1a2340 100%); border: 1px solid #1e3a5f; border-left: 3px solid #f59e0b; border-radius: 8px; padding: 1rem 1.2rem; margin: 0.5rem 0; font-size: 0.9rem; color: #c8d4e8; line-height: 1.6; }
# #     footer {visibility: hidden;} #MainMenu {visibility: hidden;} header {visibility: hidden;}
# # </style>
# # """, unsafe_allow_html=True)

# # DARK_BG = '#0a0f1e'; CARD_BG = '#111827'; BLUE = '#3b82f6'; GREEN = '#10b981'
# # RED = '#ef4444'; AMBER = '#f59e0b'; TEXT = '#e8eaf0'; MUTED = '#7a8aaa'
# # REGION_COLORS = {
# #     'Nairobi': '#3b82f6', 'Central': '#10b981', 'Coast': '#f59e0b',
# #     'Eastern': '#8b5cf6', 'North Eastern': '#ef4444', 'Nyanza': '#06b6d4',
# #     'Rift Valley': '#f97316', 'Western': '#ec4899',
# # }

# # def style_chart(fig, axes):
# #     fig.patch.set_facecolor(DARK_BG)
# #     if not hasattr(axes, '__iter__'): axes = [axes]
# #     for ax in axes:
# #         ax.set_facecolor(CARD_BG); ax.tick_params(colors=MUTED, labelsize=8)
# #         ax.xaxis.label.set_color(MUTED); ax.yaxis.label.set_color(MUTED); ax.title.set_color(TEXT)
# #         for spine in ax.spines.values(): spine.set_edgecolor('#1e2d4a')

# # def gini_coefficient(values):
# #     arr = np.sort(np.array(values, dtype=float)); n = len(arr); cumsum = np.cumsum(arr)
# #     return (2 * np.sum(np.arange(1, n+1) * arr) - (n+1) * cumsum[-1]) / (n * cumsum[-1])

# # @st.cache_data
# # def load_data():
# #     df = pd.read_csv('data/county_data.csv')
# #     df['budget_per_person'] = (df['budget_billion'] * 1_000_000_000) / df['population_2024']
# #     df['budget_per_person'] = df['budget_per_person'].round(0).astype(int)
# #     return df

# # @st.cache_data
# # def load_geojson():
# #     url = "https://raw.githubusercontent.com/mikelmaron/kenya-election-data/master/data/counties.geojson"
# #     with urllib.request.urlopen(url) as response:
# #         geojson = json.loads(response.read().decode())
# #     for feature in geojson['features']:
# #         feature['properties']['COUNTY_NAM'] = feature['properties']['COUNTY_NAM'].strip().title()
# #     return geojson

# # df = load_data()
# # sorted_df = df.sort_values('budget_per_person', ascending=False).reset_index(drop=True)
# # regional = df.groupby('region').agg(counties=('county','count'), total_pop=('population_2024','sum'), total_budget=('budget_billion','sum')).reset_index()
# # regional['budget_per_person'] = ((regional['total_budget'] * 1e9) / regional['total_pop']).astype(int)
# # regional = regional.sort_values('budget_per_person', ascending=False)
# # gini = gini_coefficient(df['budget_per_person'])
# # corr_bpp, pval_bpp = stats.pearsonr(df['population_2024'], df['budget_per_person'])
# # corr_bp, _ = stats.pearsonr(df['population_2024'], df['budget_billion'])

# # with st.sidebar:
# #     st.markdown('<div style="font-family:Syne,sans-serif;font-size:1.1rem;font-weight:800;color:#fff;margin-bottom:1rem;">🇰🇪 Navigation</div>', unsafe_allow_html=True)
# #     section = st.radio("Go to", ["📊 Overview","🗺️ Choropleth Map","📍 Regional Analysis","🔗 Correlation & Gini","🎯 Quintile Analysis","🔍 County Explorer","📋 Full Rankings"])
# #     st.markdown("---")
# #     st.markdown(f'<div style="color:{MUTED};font-size:0.75rem;">Data: KNBS 2024 Projections<br>Budget: FY 2023/24 Equitable Share<br>Counties: 47</div>', unsafe_allow_html=True)

# # st.markdown('<div class="badge">FY 2023/24 · All 47 Counties</div>', unsafe_allow_html=True)
# # st.markdown('<div class="hero-title">🇰🇪 Kenya County<br>Budget Analysis</div>', unsafe_allow_html=True)
# # st.markdown('<div class="hero-sub">Equitable Share Allocations · KNBS 2024 Population Projections</div>', unsafe_allow_html=True)

# # c1,c2,c3,c4,c5 = st.columns(5)
# # with c1: st.markdown(f'<div class="metric-card"><div class="metric-label">Total Population</div><div class="metric-value metric-accent">{df["population_2024"].sum()/1e6:.1f}M</div></div>', unsafe_allow_html=True)
# # with c2: st.markdown(f'<div class="metric-card"><div class="metric-label">Total Budget</div><div class="metric-value">KES {df["budget_billion"].sum():.1f}B</div></div>', unsafe_allow_html=True)
# # with c3: st.markdown(f'<div class="metric-card"><div class="metric-label">National Avg / Person</div><div class="metric-value metric-accent-green">KES {int(df["budget_per_person"].mean()):,}</div></div>', unsafe_allow_html=True)
# # with c4:
# #     gap = sorted_df.iloc[0]['budget_per_person'] - sorted_df.iloc[-1]['budget_per_person']
# #     st.markdown(f'<div class="metric-card"><div class="metric-label">Highest vs Lowest Gap</div><div class="metric-value metric-accent-red">KES {gap:,}</div></div>', unsafe_allow_html=True)
# # with c5: st.markdown(f'<div class="metric-card"><div class="metric-label">Gini Coefficient</div><div class="metric-value metric-accent-amber">{gini:.3f}</div></div>', unsafe_allow_html=True)

# # # ── OVERVIEW ─────────────────────────────────────────────────────────────────
# # if "Overview" in section:
# #     st.markdown('<div class="section-header">Budget Per Citizen — All 47 Counties</div>', unsafe_allow_html=True)
# #     fig1, ax1 = plt.subplots(figsize=(18, 5)); style_chart(fig1, ax1)
# #     median = sorted_df['budget_per_person'].median()
# #     colors = [RED if v > median * 1.5 else BLUE for v in sorted_df['budget_per_person']]
# #     ax1.bar(sorted_df['county'], sorted_df['budget_per_person'], color=colors, edgecolor=DARK_BG, linewidth=0.4, width=0.75)
# #     ax1.axhline(df['budget_per_person'].mean(), color=AMBER, linestyle='--', linewidth=1.5, label=f"National Average: KES {int(df['budget_per_person'].mean()):,}")
# #     ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
# #     ax1.legend(facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=9)
# #     ax1.set_ylabel('KES per Person', fontsize=9)
# #     plt.xticks(rotation=90, fontsize=7.5, color=MUTED); plt.tight_layout(); st.pyplot(fig1); plt.close()

# #     col_l, col_r = st.columns(2)
# #     top10 = sorted_df.head(10); bot10 = sorted_df.tail(10).sort_values('budget_per_person')
# #     with col_l:
# #         st.markdown('<div class="section-header">Top 10 Counties</div>', unsafe_allow_html=True)
# #         fig2, ax2 = plt.subplots(figsize=(7, 5)); style_chart(fig2, ax2)
# #         ax2.barh(top10['county'], top10['budget_per_person'], color=GREEN, edgecolor=DARK_BG, linewidth=0.4)
# #         ax2.set_title('Highest Budget Per Person', fontsize=11, fontweight='bold')
# #         ax2.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
# #         ax2.set_xlabel('KES per Person'); ax2.invert_yaxis(); ax2.tick_params(axis='y', labelsize=9, colors=TEXT)
# #         plt.tight_layout(); st.pyplot(fig2); plt.close()
# #     with col_r:
# #         st.markdown('<div class="section-header">Bottom 10 Counties</div>', unsafe_allow_html=True)
# #         fig3, ax3 = plt.subplots(figsize=(7, 5)); style_chart(fig3, ax3)
# #         ax3.barh(bot10['county'], bot10['budget_per_person'], color=RED, edgecolor=DARK_BG, linewidth=0.4)
# #         ax3.set_title('Lowest Budget Per Person', fontsize=11, fontweight='bold')
# #         ax3.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
# #         ax3.set_xlabel('KES per Person'); ax3.invert_yaxis(); ax3.tick_params(axis='y', labelsize=9, colors=TEXT)
# #         plt.tight_layout(); st.pyplot(fig3); plt.close()

# # # ── CHOROPLETH MAP ────────────────────────────────────────────────────────────
# # elif "Choropleth" in section:
# #     st.markdown('<div class="section-header">Kenya County Budget Per Citizen — Map View</div>', unsafe_allow_html=True)
# #     try:
# #         kenya_geojson = load_geojson()
# #         fig_map = px.choropleth(
# #             df,
# #             geojson=kenya_geojson,
# #             locations='county',
# #             featureidkey='properties.COUNTY_NAM',
# #             color='budget_per_person',
# #             color_continuous_scale='RdYlGn',
# #             hover_name='county',
# #             hover_data={'budget_per_person': ':,', 'budget_billion': True, 'population_2024': ':,'},
# #             labels={'budget_per_person': 'KES/Person', 'budget_billion': 'Budget (KES B)', 'population_2024': 'Population'},
# #         )
# #         fig_map.update_geos(fitbounds="locations", visible=False)
# #         fig_map.update_layout(
# #             paper_bgcolor='#0a0f1e', plot_bgcolor='#0a0f1e', font_color='#e8eaf0',
# #             coloraxis_colorbar=dict(title='KES/Person', tickfont=dict(color='#e8eaf0'), titlefont=dict(color='#e8eaf0')),
# #             margin=dict(l=0, r=0, t=20, b=0), height=600
# #         )
# #         st.plotly_chart(fig_map, use_container_width=True)
# #         st.markdown('<div class="insight-box">🟢 <strong>Green</strong> = higher budget per person &nbsp;·&nbsp; 🔴 <strong>Red</strong> = lower budget per person<br>Hover over any county to see its exact budget, population and KES per person.</div>', unsafe_allow_html=True)
# #     except Exception as e:
# #         st.error(f"Could not load map: {e}")

# # # ── REGIONAL ─────────────────────────────────────────────────────────────────
# # elif "Regional" in section:
# #     st.markdown('<div class="section-header">Regional Budget Per Person</div>', unsafe_allow_html=True)
# #     colors_r = [REGION_COLORS[r] for r in regional['region']]
# #     fig_r1, axes_r1 = plt.subplots(1, 2, figsize=(16, 5)); style_chart(fig_r1, axes_r1)
# #     axes_r1[0].barh(regional['region'], regional['budget_per_person'], color=colors_r, edgecolor=DARK_BG, linewidth=0.4)
# #     axes_r1[0].axvline(df['budget_per_person'].mean(), color=AMBER, linestyle='--', linewidth=1.2, label='National Avg')
# #     axes_r1[0].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
# #     axes_r1[0].set_title('Average Budget Per Person by Region', fontsize=11, fontweight='bold')
# #     axes_r1[0].set_xlabel('KES per Person'); axes_r1[0].invert_yaxis()
# #     axes_r1[0].tick_params(axis='y', labelsize=9, colors=TEXT)
# #     axes_r1[0].legend(facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=8)
# #     wedges, texts, autotexts = axes_r1[1].pie(regional['total_budget'], labels=regional['region'], autopct='%1.1f%%', colors=colors_r, startangle=90, pctdistance=0.75, textprops={'color': TEXT, 'fontsize': 8})
# #     for at in autotexts: at.set_color(DARK_BG); at.set_fontsize(7)
# #     axes_r1[1].set_title('Share of Total Budget by Region', fontsize=11, fontweight='bold')
# #     plt.tight_layout(); st.pyplot(fig_r1); plt.close()

# #     st.markdown('<div class="section-header">Within-Region Budget Spread</div>', unsafe_allow_html=True)
# #     reg_min = df.groupby('region')['budget_per_person'].min().reset_index().rename(columns={'budget_per_person':'min_bpp'})
# #     reg_max = df.groupby('region')['budget_per_person'].max().reset_index().rename(columns={'budget_per_person':'max_bpp'})
# #     regional_ext = regional.merge(reg_min, on='region').merge(reg_max, on='region')
# #     fig_r2, ax_r2 = plt.subplots(figsize=(14, 5)); style_chart(fig_r2, ax_r2)
# #     ax_r2.barh(regional_ext['region'], regional_ext['max_bpp'] - regional_ext['min_bpp'], left=regional_ext['min_bpp'], color=colors_r, alpha=0.5, edgecolor=DARK_BG, linewidth=0.4, height=0.5)
# #     ax_r2.scatter(regional_ext['budget_per_person'], regional_ext['region'], color=TEXT, s=50, zorder=5, label='Regional Avg/Person')
# #     ax_r2.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
# #     ax_r2.set_title('Budget/Person Range Within Each Region (min → max)', fontsize=11, fontweight='bold')
# #     ax_r2.set_xlabel('KES per Person'); ax_r2.invert_yaxis(); ax_r2.tick_params(axis='y', labelsize=9, colors=TEXT)
# #     ax_r2.legend(facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=8)
# #     plt.tight_layout(); st.pyplot(fig_r2); plt.close()

# #     st.markdown('<div class="section-header">Regional Summary Table</div>', unsafe_allow_html=True)
# #     reg_table = regional[['region','counties','total_pop','total_budget','budget_per_person']].copy()
# #     reg_table.columns = ['Region','Counties','Population','Budget (KES B)','Avg Budget/Person (KES)']
# #     reg_table = reg_table.reset_index(drop=True); reg_table.index += 1
# #     st.dataframe(reg_table, use_container_width=True)

# # # ── CORRELATION & GINI ────────────────────────────────────────────────────────
# # elif "Correlation" in section:
# #     st.markdown('<div class="section-header">Gini Coefficient & Distribution</div>', unsafe_allow_html=True)
# #     col_g1, col_g2 = st.columns([1, 2])
# #     with col_g1:
# #         st.markdown(f"""
# #         <div class="metric-card" style="margin-top:1rem;">
# #             <div class="metric-label">Gini Coefficient</div>
# #             <div class="metric-value metric-accent-amber">{gini:.4f}</div>
# #         </div>
# #         <div class="insight-box">
# #             A Gini of <strong>{gini:.3f}</strong> indicates <strong>{'high' if gini > 0.35 else 'moderate' if gini > 0.25 else 'low'} inequality</strong> in per-capita budget allocation.<br><br>
# #             The top county (<strong>{sorted_df.iloc[0]['county']}</strong>) receives <strong>{sorted_df.iloc[0]['budget_per_person'] / sorted_df.iloc[-1]['budget_per_person']:.1f}x</strong> more per person than the bottom (<strong>{sorted_df.iloc[-1]['county']}</strong>).
# #         </div>""", unsafe_allow_html=True)
# #     with col_g2:
# #         fig_g, axes_g = plt.subplots(1, 2, figsize=(12, 4)); style_chart(fig_g, axes_g)
# #         sorted_vals = np.sort(df['budget_per_person'].values); n = len(sorted_vals)
# #         lorenz_x = np.concatenate([[0], np.arange(1, n+1) / n])
# #         lorenz_y = np.concatenate([[0], np.cumsum(sorted_vals) / sorted_vals.sum()])
# #         axes_g[0].plot(lorenz_x, lorenz_y, color=BLUE, linewidth=2.5, label=f'Lorenz Curve (Gini={gini:.3f})')
# #         axes_g[0].plot([0,1],[0,1], color=MUTED, linestyle='--', linewidth=1.2, label='Perfect Equality')
# #         axes_g[0].fill_between(lorenz_x, lorenz_y, lorenz_x, alpha=0.15, color=RED)
# #         axes_g[0].set_title('Lorenz Curve', fontsize=11, fontweight='bold')
# #         axes_g[0].set_xlabel('Cumulative Share of Counties'); axes_g[0].set_ylabel('Cumulative Budget Share')
# #         axes_g[0].legend(facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=8)
# #         axes_g[1].hist(df['budget_per_person'], bins=12, color=BLUE, edgecolor=DARK_BG, linewidth=0.5, alpha=0.85)
# #         axes_g[1].axvline(df['budget_per_person'].mean(), color=AMBER, linestyle='--', linewidth=1.5, label=f"Mean: KES {int(df['budget_per_person'].mean()):,}")
# #         axes_g[1].axvline(df['budget_per_person'].median(), color=GREEN, linestyle='--', linewidth=1.5, label=f"Median: KES {int(df['budget_per_person'].median()):,}")
# #         axes_g[1].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
# #         axes_g[1].set_title('Budget/Person Distribution', fontsize=11, fontweight='bold')
# #         axes_g[1].set_xlabel('KES per Person'); axes_g[1].set_ylabel('Number of Counties')
# #         axes_g[1].legend(facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=8)
# #         plt.tight_layout(); st.pyplot(fig_g); plt.close()

# #     st.markdown('<div class="section-header">Correlation Analysis</div>', unsafe_allow_html=True)
# #     col_c1, col_c2 = st.columns(2)
# #     with col_c1: st.markdown(f'<div class="metric-card"><div class="metric-label">Population vs Absolute Budget</div><div class="metric-value metric-accent-green">r = {corr_bp:.3f}</div></div>', unsafe_allow_html=True)
# #     with col_c2: st.markdown(f'<div class="metric-card"><div class="metric-label">Population vs Budget Per Person</div><div class="metric-value metric-accent-red">r = {corr_bpp:.3f}</div></div>', unsafe_allow_html=True)

# #     colors_scatter = [REGION_COLORS[r] for r in df['region']]
# #     fig_c, axes_c = plt.subplots(1, 2, figsize=(16, 5)); style_chart(fig_c, axes_c)
# #     axes_c[0].scatter(df['population_2024']/1e6, df['budget_billion'], c=colors_scatter, s=70, alpha=0.85, edgecolors='#1e2d4a', linewidth=0.6)
# #     m, b, *_ = stats.linregress(df['population_2024']/1e6, df['budget_billion'])
# #     x_line = np.linspace(df['population_2024'].min()/1e6, df['population_2024'].max()/1e6, 100)
# #     axes_c[0].plot(x_line, m*x_line+b, color=AMBER, linewidth=1.8, linestyle='--')
# #     for _, row in df.iterrows():
# #         if row['county'] in ['Nairobi','Lamu','Nakuru','Kiambu','Turkana']:
# #             axes_c[0].annotate(row['county'], (row['population_2024']/1e6, row['budget_billion']), textcoords='offset points', xytext=(6,4), fontsize=7.5, color=TEXT)
# #     legend_patches = [mpatches.Patch(color=v, label=k) for k, v in REGION_COLORS.items()]
# #     axes_c[0].legend(handles=legend_patches, facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=7, ncol=2, loc='upper left')
# #     axes_c[0].set_title('Population vs Absolute Budget', fontsize=11, fontweight='bold')
# #     axes_c[0].set_xlabel('Population (millions)'); axes_c[0].set_ylabel('Budget (KES Billions)')
# #     axes_c[1].scatter(df['population_2024']/1e6, df['budget_per_person'], c=colors_scatter, s=70, alpha=0.85, edgecolors='#1e2d4a', linewidth=0.6)
# #     m2, b2, *_ = stats.linregress(df['population_2024']/1e6, df['budget_per_person'])
# #     axes_c[1].plot(x_line, m2*x_line+b2, color=AMBER, linewidth=1.8, linestyle='--', label=f'r = {corr_bpp:.3f}')
# #     for _, row in df.iterrows():
# #         if row['county'] in ['Nairobi','Lamu','Nakuru','Kiambu','Marsabit']:
# #             axes_c[1].annotate(row['county'], (row['population_2024']/1e6, row['budget_per_person']), textcoords='offset points', xytext=(6,4), fontsize=7.5, color=TEXT)
# #     axes_c[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
# #     axes_c[1].set_title('Population vs Budget Per Person', fontsize=11, fontweight='bold')
# #     axes_c[1].set_xlabel('Population (millions)'); axes_c[1].set_ylabel('Budget Per Person (KES)')
# #     axes_c[1].legend(facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=9)
# #     plt.tight_layout(); st.pyplot(fig_c); plt.close()
# #     st.markdown(f'<div class="insight-box">📌 <strong>Key finding:</strong> Larger counties receive significantly <em>less</em> per person (r = {corr_bpp:.3f}, p &lt; 0.001). The equitable share formula disproportionately benefits low-population counties like Lamu, Marsabit and Samburu, while high-density counties like Nairobi, Kiambu and Nakuru receive the least per citizen.</div>', unsafe_allow_html=True)

# # # ── QUINTILE ──────────────────────────────────────────────────────────────────
# # elif "Quintile" in section:
# #     st.markdown('<div class="section-header">Quintile Analysis</div>', unsafe_allow_html=True)
# #     df_q = df.copy()
# #     df_q['quintile'] = pd.qcut(df_q['budget_per_person'], q=5, labels=['Q1 Bottom 20%','Q2','Q3 Middle','Q4','Q5 Top 20%'])
# #     quintile_summary = df_q.groupby('quintile', observed=True).agg(counties=('county','count'), avg_bpp=('budget_per_person','mean'), counties_list=('county', lambda x: ', '.join(sorted(x)))).reset_index()
# #     quintile_colors = [RED, '#f97316', AMBER, '#84cc16', GREEN]
# #     fig_q, axes_q = plt.subplots(1, 2, figsize=(16, 5)); style_chart(fig_q, axes_q)
# #     axes_q[0].bar(quintile_summary['quintile'], quintile_summary['avg_bpp'], color=quintile_colors, edgecolor=DARK_BG, linewidth=0.4)
# #     axes_q[0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
# #     axes_q[0].set_title('Average Budget Per Person by Quintile', fontsize=11, fontweight='bold')
# #     axes_q[0].set_ylabel('KES per Person'); axes_q[0].tick_params(axis='x', labelsize=8, colors=TEXT)
# #     region_order = regional['region'].tolist()
# #     region_data = [df[df['region'] == r]['budget_per_person'].values for r in region_order]
# #     bp = axes_q[1].boxplot(region_data, tick_labels=region_order, patch_artist=True, vert=True)
# #     for patch, region in zip(bp['boxes'], region_order):
# #         patch.set_facecolor(REGION_COLORS[region]); patch.set_alpha(0.7)
# #     for element in ['whiskers','caps','medians','fliers']:
# #         for item in bp[element]: item.set_color(TEXT)
# #     axes_q[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
# #     axes_q[1].set_title('Budget/Person Distribution by Region', fontsize=11, fontweight='bold')
# #     axes_q[1].set_ylabel('KES per Person'); axes_q[1].tick_params(axis='x', rotation=30, labelsize=8, colors=TEXT)
# #     plt.tight_layout(); st.pyplot(fig_q); plt.close()

# #     st.markdown('<div class="section-header">Counties by Quintile</div>', unsafe_allow_html=True)
# #     for i, (_, row) in enumerate(quintile_summary.iterrows()):
# #         color = quintile_colors[i]
# #         st.markdown(f'<div class="insight-box" style="border-left-color:{color}"><strong style="color:{color}">{row["quintile"]}</strong> &nbsp;·&nbsp; Avg: KES {int(row["avg_bpp"]):,}/person &nbsp;·&nbsp; {int(row["counties"])} counties<br><span style="color:#7a8aaa">{row["counties_list"]}</span></div>', unsafe_allow_html=True)

# # # ── COUNTY EXPLORER ───────────────────────────────────────────────────────────
# # elif "Explorer" in section:
# #     st.markdown('<div class="section-header">County Explorer</div>', unsafe_allow_html=True)
# #     col_s, col_info = st.columns([1, 2])
# #     with col_s:
# #         selected = st.selectbox('Select a County', options=sorted(df['county'].tolist()))
# #     with col_info:
# #         row = df[df['county'] == selected].iloc[0]
# #         rank = sorted_df[sorted_df['county'] == selected].index[0] + 1
# #         nat_avg = int(df['budget_per_person'].mean())
# #         diff = int(row['budget_per_person']) - nat_avg
# #         diff_str = f"+KES {diff:,}" if diff > 0 else f"-KES {abs(diff):,}"
# #         diff_color = "metric-accent-green" if diff > 0 else "metric-accent-red"
# #         reg_avg = int(regional[regional['region'] == row['region']]['budget_per_person'].values[0])
# #         ca, cb2, cc, cd = st.columns(4)
# #         with ca: st.markdown(f'<div class="metric-card"><div class="metric-label">Population</div><div class="metric-value" style="font-size:1.3rem">{int(row["population_2024"]):,}</div></div>', unsafe_allow_html=True)
# #         with cb2: st.markdown(f'<div class="metric-card"><div class="metric-label">Budget</div><div class="metric-value" style="font-size:1.3rem">KES {row["budget_billion"]}B</div></div>', unsafe_allow_html=True)
# #         with cc: st.markdown(f'<div class="metric-card"><div class="metric-label">Per Person · Rank #{rank}</div><div class="metric-value {diff_color}" style="font-size:1.3rem">KES {int(row["budget_per_person"]):,}</div></div>', unsafe_allow_html=True)
# #         with cd: st.markdown(f'<div class="metric-card"><div class="metric-label">Region ({row["region"]})</div><div class="metric-value" style="font-size:1.3rem">KES {reg_avg:,}</div></div>', unsafe_allow_html=True)
# #         st.markdown(f'<div class="insight-box"><strong>{selected}</strong> is ranked <strong>#{rank} of 47</strong> counties by budget per person. It is <strong>{diff_str}</strong> vs the national average of KES {nat_avg:,}/person, and sits in the <strong>{row["region"]}</strong> region (regional avg: KES {reg_avg:,}/person).</div>', unsafe_allow_html=True)

# # # ── FULL RANKINGS ─────────────────────────────────────────────────────────────
# # elif "Rankings" in section:
# #     st.markdown('<div class="section-header">Full County Rankings</div>', unsafe_allow_html=True)
# #     region_filter = st.multiselect('Filter by Region', options=sorted(df['region'].unique()), default=sorted(df['region'].unique()))
# #     filtered = sorted_df[sorted_df['region'].isin(region_filter)]
# #     table = filtered[['county','region','population_2024','budget_billion','budget_per_person']].copy()
# #     table.columns = ['County','Region','Population (2024)','Budget (KES B)','Budget/Person (KES)']
# #     table = table.reset_index(drop=True); table.index += 1
# #     st.dataframe(table, use_container_width=True, height=600)
# #     csv = table.to_csv().encode('utf-8')
# #     st.download_button("⬇ Download as CSV", csv, "kenya_county_budget.csv", "text/csv")

# import streamlit as st
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.ticker as mticker
# import matplotlib.patches as mpatches
# import plotly.express as px
# import json
# import urllib.request
# from scipy import stats

# st.set_page_config(page_title="Kenya County Budget Analysis", page_icon="🇰🇪", layout="wide")

# st.markdown("""
# <style>
#     @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500&display=swap');
#     html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
#     .stApp { background-color: #0a0f1e; color: #e8eaf0; }
#     h1, h2, h3 { font-family: 'Syne', sans-serif !important; }
#     .hero-title { font-family: 'Syne', sans-serif; font-size: 3rem; font-weight: 800; color: #ffffff; line-height: 1.1; margin-bottom: 0.3rem; }
#     .hero-sub { font-size: 1rem; color: #7a8aaa; margin-bottom: 2rem; font-weight: 300; letter-spacing: 0.05em; }
#     .metric-card { background: linear-gradient(135deg, #111827 0%, #1a2340 100%); border: 1px solid #1e2d4a; border-radius: 12px; padding: 1.4rem 1.6rem; margin-bottom: 1rem; }
#     .metric-label { font-size: 0.72rem; font-weight: 500; color: #5a6a8a; text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 0.4rem; }
#     .metric-value { font-family: 'Syne', sans-serif; font-size: 1.9rem; font-weight: 700; color: #ffffff; line-height: 1; }
#     .metric-accent { color: #3b82f6; } .metric-accent-green { color: #10b981; } .metric-accent-red { color: #ef4444; } .metric-accent-amber { color: #f59e0b; }
#     .section-header { font-family: 'Syne', sans-serif; font-size: 1.1rem; font-weight: 700; color: #ffffff; text-transform: uppercase; letter-spacing: 0.08em; border-left: 3px solid #3b82f6; padding-left: 0.8rem; margin-bottom: 1rem; margin-top: 2rem; }
#     .badge { display: inline-block; background: #1e3a5f; color: #60a5fa; font-size: 0.7rem; font-weight: 600; padding: 2px 10px; border-radius: 20px; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 0.5rem; }
#     .insight-box { background: linear-gradient(135deg, #0f1f3d 0%, #1a2340 100%); border: 1px solid #1e3a5f; border-left: 3px solid #f59e0b; border-radius: 8px; padding: 1rem 1.2rem; margin: 0.5rem 0; font-size: 0.9rem; color: #c8d4e8; line-height: 1.6; }
#     footer {visibility: hidden;} #MainMenu {visibility: hidden;} header {visibility: hidden;}
# </style>
# """, unsafe_allow_html=True)

# DARK_BG = '#0a0f1e'; CARD_BG = '#111827'; BLUE = '#3b82f6'; GREEN = '#10b981'
# RED = '#ef4444'; AMBER = '#f59e0b'; TEXT = '#e8eaf0'; MUTED = '#7a8aaa'
# REGION_COLORS = {
#     'Nairobi': '#3b82f6', 'Central': '#10b981', 'Coast': '#f59e0b',
#     'Eastern': '#8b5cf6', 'North Eastern': '#ef4444', 'Nyanza': '#06b6d4',
#     'Rift Valley': '#f97316', 'Western': '#ec4899',
# }

# NAME_MAP = {
#     'Tana River':     'Tana River',
#     'Taita Taveta':   'Taita-Taveta',
#     'Elgeyo Marakwet':'Elgeyo/Marakwet',
#     "Murang'a":       'Muranga',
#     'Trans Nzoia':    'Trans-Nzoia',
#     'Homa Bay':       'Homa Bay',
#     'Tharaka Nithi':  'Tharaka-Nithi',
#     'West Pokot':     'West Pokot',
#     'Uasin Gishu':    'Uasin Gishu',
# }

# def style_chart(fig, axes):
#     fig.patch.set_facecolor(DARK_BG)
#     if not hasattr(axes, '__iter__'): axes = [axes]
#     for ax in axes:
#         ax.set_facecolor(CARD_BG); ax.tick_params(colors=MUTED, labelsize=8)
#         ax.xaxis.label.set_color(MUTED); ax.yaxis.label.set_color(MUTED); ax.title.set_color(TEXT)
#         for spine in ax.spines.values(): spine.set_edgecolor('#1e2d4a')

# def gini_coefficient(values):
#     arr = np.sort(np.array(values, dtype=float)); n = len(arr); cumsum = np.cumsum(arr)
#     return (2 * np.sum(np.arange(1, n+1) * arr) - (n+1) * cumsum[-1]) / (n * cumsum[-1])

# @st.cache_data
# def load_data():
#     df = pd.read_csv('data/county_data.csv')
#     df['budget_per_person'] = (df['budget_billion'] * 1_000_000_000) / df['population_2024']
#     df['budget_per_person'] = df['budget_per_person'].round(0).astype(int)
#     return df

# @st.cache_data
# def load_geojson():
#     url = "https://raw.githubusercontent.com/mikelmaron/kenya-election-data/master/data/counties.geojson"
#     with urllib.request.urlopen(url) as response:
#         geojson = json.loads(response.read().decode())
#     for feature in geojson['features']:
#         name = feature['properties'].get('COUNTY_NAM', '')
#         if name:
#             feature['properties']['COUNTY_NAM'] = name.strip().title()
#     return geojson

# df = load_data()
# sorted_df = df.sort_values('budget_per_person', ascending=False).reset_index(drop=True)
# regional = df.groupby('region').agg(counties=('county','count'), total_pop=('population_2024','sum'), total_budget=('budget_billion','sum')).reset_index()
# regional['budget_per_person'] = ((regional['total_budget'] * 1e9) / regional['total_pop']).astype(int)
# regional = regional.sort_values('budget_per_person', ascending=False)
# gini = gini_coefficient(df['budget_per_person'])
# corr_bpp, pval_bpp = stats.pearsonr(df['population_2024'], df['budget_per_person'])
# corr_bp, _ = stats.pearsonr(df['population_2024'], df['budget_billion'])

# with st.sidebar:
#     st.markdown('<div style="font-family:Syne,sans-serif;font-size:1.1rem;font-weight:800;color:#fff;margin-bottom:1rem;">🇰🇪 Navigation</div>', unsafe_allow_html=True)
#     section = st.radio("Go to", ["📊 Overview","🗺️ Choropleth Map","📍 Regional Analysis","🔗 Correlation & Gini","🎯 Quintile Analysis","🔍 County Explorer","📋 Full Rankings"])
#     st.markdown("---")
#     st.markdown(f'<div style="color:{MUTED};font-size:0.75rem;">Data: KNBS 2024 Projections<br>Budget: FY 2023/24 Equitable Share<br>Counties: 47</div>', unsafe_allow_html=True)

# st.markdown('<div class="badge">FY 2023/24 · All 47 Counties</div>', unsafe_allow_html=True)
# st.markdown('<div class="hero-title">🇰🇪 Kenya County<br>Budget Analysis</div>', unsafe_allow_html=True)
# st.markdown('<div class="hero-sub">Equitable Share Allocations · KNBS 2024 Population Projections</div>', unsafe_allow_html=True)

# c1,c2,c3,c4,c5 = st.columns(5)
# with c1: st.markdown(f'<div class="metric-card"><div class="metric-label">Total Population</div><div class="metric-value metric-accent">{df["population_2024"].sum()/1e6:.1f}M</div></div>', unsafe_allow_html=True)
# with c2: st.markdown(f'<div class="metric-card"><div class="metric-label">Total Budget</div><div class="metric-value">KES {df["budget_billion"].sum():.1f}B</div></div>', unsafe_allow_html=True)
# with c3: st.markdown(f'<div class="metric-card"><div class="metric-label">National Avg / Person</div><div class="metric-value metric-accent-green">KES {int(df["budget_per_person"].mean()):,}</div></div>', unsafe_allow_html=True)
# with c4:
#     gap = sorted_df.iloc[0]['budget_per_person'] - sorted_df.iloc[-1]['budget_per_person']
#     st.markdown(f'<div class="metric-card"><div class="metric-label">Highest vs Lowest Gap</div><div class="metric-value metric-accent-red">KES {gap:,}</div></div>', unsafe_allow_html=True)
# with c5: st.markdown(f'<div class="metric-card"><div class="metric-label">Gini Coefficient</div><div class="metric-value metric-accent-amber">{gini:.3f}</div></div>', unsafe_allow_html=True)

# # ── OVERVIEW ─────────────────────────────────────────────────────────────────
# if "Overview" in section:
#     st.markdown('<div class="section-header">Budget Per Citizen — All 47 Counties</div>', unsafe_allow_html=True)
#     fig1, ax1 = plt.subplots(figsize=(18, 5)); style_chart(fig1, ax1)
#     median = sorted_df['budget_per_person'].median()
#     colors = [RED if v > median * 1.5 else BLUE for v in sorted_df['budget_per_person']]
#     ax1.bar(sorted_df['county'], sorted_df['budget_per_person'], color=colors, edgecolor=DARK_BG, linewidth=0.4, width=0.75)
#     ax1.axhline(df['budget_per_person'].mean(), color=AMBER, linestyle='--', linewidth=1.5, label=f"National Average: KES {int(df['budget_per_person'].mean()):,}")
#     ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
#     ax1.legend(facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=9)
#     ax1.set_ylabel('KES per Person', fontsize=9)
#     plt.xticks(rotation=90, fontsize=7.5, color=MUTED); plt.tight_layout(); st.pyplot(fig1); plt.close()

#     col_l, col_r = st.columns(2)
#     top10 = sorted_df.head(10); bot10 = sorted_df.tail(10).sort_values('budget_per_person')
#     with col_l:
#         st.markdown('<div class="section-header">Top 10 Counties</div>', unsafe_allow_html=True)
#         fig2, ax2 = plt.subplots(figsize=(7, 5)); style_chart(fig2, ax2)
#         ax2.barh(top10['county'], top10['budget_per_person'], color=GREEN, edgecolor=DARK_BG, linewidth=0.4)
#         ax2.set_title('Highest Budget Per Person', fontsize=11, fontweight='bold')
#         ax2.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
#         ax2.set_xlabel('KES per Person'); ax2.invert_yaxis(); ax2.tick_params(axis='y', labelsize=9, colors=TEXT)
#         plt.tight_layout(); st.pyplot(fig2); plt.close()
#     with col_r:
#         st.markdown('<div class="section-header">Bottom 10 Counties</div>', unsafe_allow_html=True)
#         fig3, ax3 = plt.subplots(figsize=(7, 5)); style_chart(fig3, ax3)
#         ax3.barh(bot10['county'], bot10['budget_per_person'], color=RED, edgecolor=DARK_BG, linewidth=0.4)
#         ax3.set_title('Lowest Budget Per Person', fontsize=11, fontweight='bold')
#         ax3.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
#         ax3.set_xlabel('KES per Person'); ax3.invert_yaxis(); ax3.tick_params(axis='y', labelsize=9, colors=TEXT)
#         plt.tight_layout(); st.pyplot(fig3); plt.close()

# # ── CHOROPLETH MAP ────────────────────────────────────────────────────────────
# elif "Choropleth" in section:
#     st.markdown('<div class="section-header">Kenya County Budget Per Citizen — Map View</div>', unsafe_allow_html=True)
#     try:
#         kenya_geojson = load_geojson()
#         df_map = df.copy()
#         df_map['county_mapped'] = df_map['county'].apply(lambda x: NAME_MAP.get(x, x))
#         fig_map = px.choropleth(
#             df_map,
#             geojson=kenya_geojson,
#             locations='county_mapped',
#             featureidkey='properties.COUNTY_NAM',
#             color='budget_per_person',
#             color_continuous_scale='RdYlGn',
#             hover_name='county',
#             hover_data={
#                 'county_mapped': False,
#                 'budget_per_person': ':,',
#                 'budget_billion': True,
#                 'population_2024': ':,'
#             },
#             labels={
#                 'budget_per_person': 'KES/Person',
#                 'budget_billion': 'Budget (KES B)',
#                 'population_2024': 'Population'
#             },
#         )
#         fig_map.update_geos(fitbounds="locations", visible=False)
#         fig_map.update_layout(
#             paper_bgcolor='#0a0f1e', plot_bgcolor='#0a0f1e', font_color='#e8eaf0',
#             coloraxis_colorbar=dict(
#                 title=dict(text='KES/Person', font=dict(color='#e8eaf0')),
#                 tickfont=dict(color='#e8eaf0'),
#             ),
#             margin=dict(l=0, r=0, t=20, b=0), height=600
#         )
#         st.plotly_chart(fig_map, use_container_width=True)
#         st.markdown('<div class="insight-box">🟢 <strong>Green</strong> = higher budget per person &nbsp;·&nbsp; 🔴 <strong>Red</strong> = lower budget per person<br>Hover over any county to see its exact budget, population and KES per person.</div>', unsafe_allow_html=True)
#     except Exception as e:
#         st.error(f"Could not load map: {e}")

# # ── REGIONAL ─────────────────────────────────────────────────────────────────
# elif "Regional" in section:
#     st.markdown('<div class="section-header">Regional Budget Per Person</div>', unsafe_allow_html=True)
#     colors_r = [REGION_COLORS[r] for r in regional['region']]
#     fig_r1, axes_r1 = plt.subplots(1, 2, figsize=(16, 5)); style_chart(fig_r1, axes_r1)
#     axes_r1[0].barh(regional['region'], regional['budget_per_person'], color=colors_r, edgecolor=DARK_BG, linewidth=0.4)
#     axes_r1[0].axvline(df['budget_per_person'].mean(), color=AMBER, linestyle='--', linewidth=1.2, label='National Avg')
#     axes_r1[0].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
#     axes_r1[0].set_title('Average Budget Per Person by Region', fontsize=11, fontweight='bold')
#     axes_r1[0].set_xlabel('KES per Person'); axes_r1[0].invert_yaxis()
#     axes_r1[0].tick_params(axis='y', labelsize=9, colors=TEXT)
#     axes_r1[0].legend(facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=8)
#     wedges, texts, autotexts = axes_r1[1].pie(regional['total_budget'], labels=regional['region'], autopct='%1.1f%%', colors=colors_r, startangle=90, pctdistance=0.75, textprops={'color': TEXT, 'fontsize': 8})
#     for at in autotexts: at.set_color(DARK_BG); at.set_fontsize(7)
#     axes_r1[1].set_title('Share of Total Budget by Region', fontsize=11, fontweight='bold')
#     plt.tight_layout(); st.pyplot(fig_r1); plt.close()

#     st.markdown('<div class="section-header">Within-Region Budget Spread</div>', unsafe_allow_html=True)
#     reg_min = df.groupby('region')['budget_per_person'].min().reset_index().rename(columns={'budget_per_person':'min_bpp'})
#     reg_max = df.groupby('region')['budget_per_person'].max().reset_index().rename(columns={'budget_per_person':'max_bpp'})
#     regional_ext = regional.merge(reg_min, on='region').merge(reg_max, on='region')
#     fig_r2, ax_r2 = plt.subplots(figsize=(14, 5)); style_chart(fig_r2, ax_r2)
#     ax_r2.barh(regional_ext['region'], regional_ext['max_bpp'] - regional_ext['min_bpp'], left=regional_ext['min_bpp'], color=colors_r, alpha=0.5, edgecolor=DARK_BG, linewidth=0.4, height=0.5)
#     ax_r2.scatter(regional_ext['budget_per_person'], regional_ext['region'], color=TEXT, s=50, zorder=5, label='Regional Avg/Person')
#     ax_r2.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
#     ax_r2.set_title('Budget/Person Range Within Each Region (min → max)', fontsize=11, fontweight='bold')
#     ax_r2.set_xlabel('KES per Person'); ax_r2.invert_yaxis(); ax_r2.tick_params(axis='y', labelsize=9, colors=TEXT)
#     ax_r2.legend(facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=8)
#     plt.tight_layout(); st.pyplot(fig_r2); plt.close()

#     st.markdown('<div class="section-header">Regional Summary Table</div>', unsafe_allow_html=True)
#     reg_table = regional[['region','counties','total_pop','total_budget','budget_per_person']].copy()
#     reg_table.columns = ['Region','Counties','Population','Budget (KES B)','Avg Budget/Person (KES)']
#     reg_table = reg_table.reset_index(drop=True); reg_table.index += 1
#     st.dataframe(reg_table, use_container_width=True)

# # ── CORRELATION & GINI ────────────────────────────────────────────────────────
# elif "Correlation" in section:
#     st.markdown('<div class="section-header">Gini Coefficient & Distribution</div>', unsafe_allow_html=True)
#     col_g1, col_g2 = st.columns([1, 2])
#     with col_g1:
#         st.markdown(f"""
#         <div class="metric-card" style="margin-top:1rem;">
#             <div class="metric-label">Gini Coefficient</div>
#             <div class="metric-value metric-accent-amber">{gini:.4f}</div>
#         </div>
#         <div class="insight-box">
#             A Gini of <strong>{gini:.3f}</strong> indicates <strong>{'high' if gini > 0.35 else 'moderate' if gini > 0.25 else 'low'} inequality</strong> in per-capita budget allocation.<br><br>
#             The top county (<strong>{sorted_df.iloc[0]['county']}</strong>) receives <strong>{sorted_df.iloc[0]['budget_per_person'] / sorted_df.iloc[-1]['budget_per_person']:.1f}x</strong> more per person than the bottom (<strong>{sorted_df.iloc[-1]['county']}</strong>).
#         </div>""", unsafe_allow_html=True)
#     with col_g2:
#         fig_g, axes_g = plt.subplots(1, 2, figsize=(12, 4)); style_chart(fig_g, axes_g)
#         sorted_vals = np.sort(df['budget_per_person'].values); n = len(sorted_vals)
#         lorenz_x = np.concatenate([[0], np.arange(1, n+1) / n])
#         lorenz_y = np.concatenate([[0], np.cumsum(sorted_vals) / sorted_vals.sum()])
#         axes_g[0].plot(lorenz_x, lorenz_y, color=BLUE, linewidth=2.5, label=f'Lorenz Curve (Gini={gini:.3f})')
#         axes_g[0].plot([0,1],[0,1], color=MUTED, linestyle='--', linewidth=1.2, label='Perfect Equality')
#         axes_g[0].fill_between(lorenz_x, lorenz_y, lorenz_x, alpha=0.15, color=RED)
#         axes_g[0].set_title('Lorenz Curve', fontsize=11, fontweight='bold')
#         axes_g[0].set_xlabel('Cumulative Share of Counties'); axes_g[0].set_ylabel('Cumulative Budget Share')
#         axes_g[0].legend(facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=8)
#         axes_g[1].hist(df['budget_per_person'], bins=12, color=BLUE, edgecolor=DARK_BG, linewidth=0.5, alpha=0.85)
#         axes_g[1].axvline(df['budget_per_person'].mean(), color=AMBER, linestyle='--', linewidth=1.5, label=f"Mean: KES {int(df['budget_per_person'].mean()):,}")
#         axes_g[1].axvline(df['budget_per_person'].median(), color=GREEN, linestyle='--', linewidth=1.5, label=f"Median: KES {int(df['budget_per_person'].median()):,}")
#         axes_g[1].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
#         axes_g[1].set_title('Budget/Person Distribution', fontsize=11, fontweight='bold')
#         axes_g[1].set_xlabel('KES per Person'); axes_g[1].set_ylabel('Number of Counties')
#         axes_g[1].legend(facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=8)
#         plt.tight_layout(); st.pyplot(fig_g); plt.close()

#     st.markdown('<div class="section-header">Correlation Analysis</div>', unsafe_allow_html=True)
#     col_c1, col_c2 = st.columns(2)
#     with col_c1: st.markdown(f'<div class="metric-card"><div class="metric-label">Population vs Absolute Budget</div><div class="metric-value metric-accent-green">r = {corr_bp:.3f}</div></div>', unsafe_allow_html=True)
#     with col_c2: st.markdown(f'<div class="metric-card"><div class="metric-label">Population vs Budget Per Person</div><div class="metric-value metric-accent-red">r = {corr_bpp:.3f}</div></div>', unsafe_allow_html=True)

#     colors_scatter = [REGION_COLORS[r] for r in df['region']]
#     fig_c, axes_c = plt.subplots(1, 2, figsize=(16, 5)); style_chart(fig_c, axes_c)
#     axes_c[0].scatter(df['population_2024']/1e6, df['budget_billion'], c=colors_scatter, s=70, alpha=0.85, edgecolors='#1e2d4a', linewidth=0.6)
#     m, b, *_ = stats.linregress(df['population_2024']/1e6, df['budget_billion'])
#     x_line = np.linspace(df['population_2024'].min()/1e6, df['population_2024'].max()/1e6, 100)
#     axes_c[0].plot(x_line, m*x_line+b, color=AMBER, linewidth=1.8, linestyle='--')
#     for _, row in df.iterrows():
#         if row['county'] in ['Nairobi','Lamu','Nakuru','Kiambu','Turkana']:
#             axes_c[0].annotate(row['county'], (row['population_2024']/1e6, row['budget_billion']), textcoords='offset points', xytext=(6,4), fontsize=7.5, color=TEXT)
#     legend_patches = [mpatches.Patch(color=v, label=k) for k, v in REGION_COLORS.items()]
#     axes_c[0].legend(handles=legend_patches, facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=7, ncol=2, loc='upper left')
#     axes_c[0].set_title('Population vs Absolute Budget', fontsize=11, fontweight='bold')
#     axes_c[0].set_xlabel('Population (millions)'); axes_c[0].set_ylabel('Budget (KES Billions)')
#     axes_c[1].scatter(df['population_2024']/1e6, df['budget_per_person'], c=colors_scatter, s=70, alpha=0.85, edgecolors='#1e2d4a', linewidth=0.6)
#     m2, b2, *_ = stats.linregress(df['population_2024']/1e6, df['budget_per_person'])
#     axes_c[1].plot(x_line, m2*x_line+b2, color=AMBER, linewidth=1.8, linestyle='--', label=f'r = {corr_bpp:.3f}')
#     for _, row in df.iterrows():
#         if row['county'] in ['Nairobi','Lamu','Nakuru','Kiambu','Marsabit']:
#             axes_c[1].annotate(row['county'], (row['population_2024']/1e6, row['budget_per_person']), textcoords='offset points', xytext=(6,4), fontsize=7.5, color=TEXT)
#     axes_c[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
#     axes_c[1].set_title('Population vs Budget Per Person', fontsize=11, fontweight='bold')
#     axes_c[1].set_xlabel('Population (millions)'); axes_c[1].set_ylabel('Budget Per Person (KES)')
#     axes_c[1].legend(facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=9)
#     plt.tight_layout(); st.pyplot(fig_c); plt.close()
#     st.markdown(f'<div class="insight-box">📌 <strong>Key finding:</strong> Larger counties receive significantly <em>less</em> per person (r = {corr_bpp:.3f}, p &lt; 0.001). The equitable share formula disproportionately benefits low-population counties like Lamu, Marsabit and Samburu, while high-density counties like Nairobi, Kiambu and Nakuru receive the least per citizen.</div>', unsafe_allow_html=True)

# # ── QUINTILE ──────────────────────────────────────────────────────────────────
# elif "Quintile" in section:
#     st.markdown('<div class="section-header">Quintile Analysis</div>', unsafe_allow_html=True)
#     df_q = df.copy()
#     df_q['quintile'] = pd.qcut(df_q['budget_per_person'], q=5, labels=['Q1 Bottom 20%','Q2','Q3 Middle','Q4','Q5 Top 20%'])
#     quintile_summary = df_q.groupby('quintile', observed=True).agg(counties=('county','count'), avg_bpp=('budget_per_person','mean'), counties_list=('county', lambda x: ', '.join(sorted(x)))).reset_index()
#     quintile_colors = [RED, '#f97316', AMBER, '#84cc16', GREEN]
#     fig_q, axes_q = plt.subplots(1, 2, figsize=(16, 5)); style_chart(fig_q, axes_q)
#     axes_q[0].bar(quintile_summary['quintile'], quintile_summary['avg_bpp'], color=quintile_colors, edgecolor=DARK_BG, linewidth=0.4)
#     axes_q[0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
#     axes_q[0].set_title('Average Budget Per Person by Quintile', fontsize=11, fontweight='bold')
#     axes_q[0].set_ylabel('KES per Person'); axes_q[0].tick_params(axis='x', labelsize=8, colors=TEXT)
#     region_order = regional['region'].tolist()
#     region_data = [df[df['region'] == r]['budget_per_person'].values for r in region_order]
#     bp = axes_q[1].boxplot(region_data, tick_labels=region_order, patch_artist=True, vert=True)
#     for patch, region in zip(bp['boxes'], region_order):
#         patch.set_facecolor(REGION_COLORS[region]); patch.set_alpha(0.7)
#     for element in ['whiskers','caps','medians','fliers']:
#         for item in bp[element]: item.set_color(TEXT)
#     axes_q[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
#     axes_q[1].set_title('Budget/Person Distribution by Region', fontsize=11, fontweight='bold')
#     axes_q[1].set_ylabel('KES per Person'); axes_q[1].tick_params(axis='x', rotation=30, labelsize=8, colors=TEXT)
#     plt.tight_layout(); st.pyplot(fig_q); plt.close()

#     st.markdown('<div class="section-header">Counties by Quintile</div>', unsafe_allow_html=True)
#     for i, (_, row) in enumerate(quintile_summary.iterrows()):
#         color = quintile_colors[i]
#         st.markdown(f'<div class="insight-box" style="border-left-color:{color}"><strong style="color:{color}">{row["quintile"]}</strong> &nbsp;·&nbsp; Avg: KES {int(row["avg_bpp"]):,}/person &nbsp;·&nbsp; {int(row["counties"])} counties<br><span style="color:#7a8aaa">{row["counties_list"]}</span></div>', unsafe_allow_html=True)

# # ── COUNTY EXPLORER ───────────────────────────────────────────────────────────
# elif "Explorer" in section:
#     st.markdown('<div class="section-header">County Explorer</div>', unsafe_allow_html=True)
#     col_s, col_info = st.columns([1, 2])
#     with col_s:
#         selected = st.selectbox('Select a County', options=sorted(df['county'].tolist()))
#     with col_info:
#         row = df[df['county'] == selected].iloc[0]
#         rank = sorted_df[sorted_df['county'] == selected].index[0] + 1
#         nat_avg = int(df['budget_per_person'].mean())
#         diff = int(row['budget_per_person']) - nat_avg
#         diff_str = f"+KES {diff:,}" if diff > 0 else f"-KES {abs(diff):,}"
#         diff_color = "metric-accent-green" if diff > 0 else "metric-accent-red"
#         reg_avg = int(regional[regional['region'] == row['region']]['budget_per_person'].values[0])
#         ca, cb2, cc, cd = st.columns(4)
#         with ca: st.markdown(f'<div class="metric-card"><div class="metric-label">Population</div><div class="metric-value" style="font-size:1.3rem">{int(row["population_2024"]):,}</div></div>', unsafe_allow_html=True)
#         with cb2: st.markdown(f'<div class="metric-card"><div class="metric-label">Budget</div><div class="metric-value" style="font-size:1.3rem">KES {row["budget_billion"]}B</div></div>', unsafe_allow_html=True)
#         with cc: st.markdown(f'<div class="metric-card"><div class="metric-label">Per Person · Rank #{rank}</div><div class="metric-value {diff_color}" style="font-size:1.3rem">KES {int(row["budget_per_person"]):,}</div></div>', unsafe_allow_html=True)
#         with cd: st.markdown(f'<div class="metric-card"><div class="metric-label">Region ({row["region"]})</div><div class="metric-value" style="font-size:1.3rem">KES {reg_avg:,}</div></div>', unsafe_allow_html=True)
#         st.markdown(f'<div class="insight-box"><strong>{selected}</strong> is ranked <strong>#{rank} of 47</strong> counties by budget per person. It is <strong>{diff_str}</strong> vs the national average of KES {nat_avg:,}/person, and sits in the <strong>{row["region"]}</strong> region (regional avg: KES {reg_avg:,}/person).</div>', unsafe_allow_html=True)

# # ── FULL RANKINGS ─────────────────────────────────────────────────────────────
# elif "Rankings" in section:
#     st.markdown('<div class="section-header">Full County Rankings</div>', unsafe_allow_html=True)
#     region_filter = st.multiselect('Filter by Region', options=sorted(df['region'].unique()), default=sorted(df['region'].unique()))
#     filtered = sorted_df[sorted_df['region'].isin(region_filter)]
#     table = filtered[['county','region','population_2024','budget_billion','budget_per_person']].copy()
#     table.columns = ['County','Region','Population (2024)','Budget (KES B)','Budget/Person (KES)']
#     table = table.reset_index(drop=True); table.index += 1
#     st.dataframe(table, use_container_width=True, height=600)
#     csv = table.to_csv().encode('utf-8')
#     st.download_button("⬇ Download as CSV", csv, "kenya_county_budget.csv", "text/csv")

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.patches as mpatches
import plotly.express as px
import json
import urllib.request
from scipy import stats

st.set_page_config(page_title="Kenya County Budget Analysis", page_icon="🇰🇪", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500&display=swap');
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
    .stApp { background-color: #0a0f1e; color: #e8eaf0; }
    h1, h2, h3 { font-family: 'Syne', sans-serif !important; }
    .hero-title { font-family: 'Syne', sans-serif; font-size: 3rem; font-weight: 800; color: #ffffff; line-height: 1.1; margin-bottom: 0.3rem; }
    .hero-sub { font-size: 1rem; color: #7a8aaa; margin-bottom: 2rem; font-weight: 300; letter-spacing: 0.05em; }
    .metric-card { background: linear-gradient(135deg, #111827 0%, #1a2340 100%); border: 1px solid #1e2d4a; border-radius: 12px; padding: 1.4rem 1.6rem; margin-bottom: 1rem; }
    .metric-label { font-size: 0.72rem; font-weight: 500; color: #5a6a8a; text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 0.4rem; }
    .metric-value { font-family: 'Syne', sans-serif; font-size: 1.9rem; font-weight: 700; color: #ffffff; line-height: 1; }
    .metric-accent { color: #3b82f6; } .metric-accent-green { color: #10b981; } .metric-accent-red { color: #ef4444; } .metric-accent-amber { color: #f59e0b; }
    .section-header { font-family: 'Syne', sans-serif; font-size: 1.1rem; font-weight: 700; color: #ffffff; text-transform: uppercase; letter-spacing: 0.08em; border-left: 3px solid #3b82f6; padding-left: 0.8rem; margin-bottom: 1rem; margin-top: 2rem; }
    .badge { display: inline-block; background: #1e3a5f; color: #60a5fa; font-size: 0.7rem; font-weight: 600; padding: 2px 10px; border-radius: 20px; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 0.5rem; }
    .insight-box { background: linear-gradient(135deg, #0f1f3d 0%, #1a2340 100%); border: 1px solid #1e3a5f; border-left: 3px solid #f59e0b; border-radius: 8px; padding: 1rem 1.2rem; margin: 0.5rem 0; font-size: 0.9rem; color: #c8d4e8; line-height: 1.6; }
    footer {visibility: hidden;} #MainMenu {visibility: hidden;} header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

DARK_BG = '#0a0f1e'; CARD_BG = '#111827'; BLUE = '#3b82f6'; GREEN = '#10b981'
RED = '#ef4444'; AMBER = '#f59e0b'; TEXT = '#e8eaf0'; MUTED = '#7a8aaa'
REGION_COLORS = {
    'Nairobi': '#3b82f6', 'Central': '#10b981', 'Coast': '#f59e0b',
    'Eastern': '#8b5cf6', 'North Eastern': '#ef4444', 'Nyanza': '#06b6d4',
    'Rift Valley': '#f97316', 'Western': '#ec4899',
}

NAME_MAP = {
    'Tana River':     'Tana River',
    'Taita Taveta':   'Taita-Taveta',
    'Elgeyo Marakwet':'Elgeyo/Marakwet',
    "Murang'a":       'Muranga',
    'Trans Nzoia':    'Trans-Nzoia',
    'Homa Bay':       'Homa Bay',
    'Tharaka Nithi':  'Tharaka-Nithi',
    'West Pokot':     'West Pokot',
    'Uasin Gishu':    'Uasin Gishu',
}

def style_chart(fig, axes):
    fig.patch.set_facecolor(DARK_BG)
    if not hasattr(axes, '__iter__'): axes = [axes]
    for ax in axes:
        ax.set_facecolor(CARD_BG); ax.tick_params(colors=MUTED, labelsize=8)
        ax.xaxis.label.set_color(MUTED); ax.yaxis.label.set_color(MUTED); ax.title.set_color(TEXT)
        for spine in ax.spines.values(): spine.set_edgecolor('#1e2d4a')

def gini_coefficient(values):
    arr = np.sort(np.array(values, dtype=float)); n = len(arr); cumsum = np.cumsum(arr)
    return (2 * np.sum(np.arange(1, n+1) * arr) - (n+1) * cumsum[-1]) / (n * cumsum[-1])

@st.cache_data
def load_data():
    df = pd.read_csv('data/county_data.csv')
    df['budget_per_person'] = (df['budget_billion'] * 1_000_000_000) / df['population_2024']
    df['budget_per_person'] = df['budget_per_person'].round(0).astype(int)
    return df

@st.cache_data
def load_geojson():
    url = "https://raw.githubusercontent.com/mikelmaron/kenya-election-data/master/data/counties.geojson"
    with urllib.request.urlopen(url) as response:
        geojson = json.loads(response.read().decode())
    for feature in geojson['features']:
        name = feature['properties'].get('COUNTY_NAM', '')
        if name:
            feature['properties']['COUNTY_NAM'] = name.strip().title()
    return geojson

df = load_data()
sorted_df = df.sort_values('budget_per_person', ascending=False).reset_index(drop=True)
regional = df.groupby('region').agg(counties=('county','count'), total_pop=('population_2024','sum'), total_budget=('budget_billion','sum')).reset_index()
regional['budget_per_person'] = ((regional['total_budget'] * 1e9) / regional['total_pop']).astype(int)
regional = regional.sort_values('budget_per_person', ascending=False)
gini = gini_coefficient(df['budget_per_person'])
corr_bpp, pval_bpp = stats.pearsonr(df['population_2024'], df['budget_per_person'])
corr_bp, _ = stats.pearsonr(df['population_2024'], df['budget_billion'])

top_county = sorted_df.iloc[0]; bot_county = sorted_df.iloc[-1]

SECTIONS = ["🏠 Home", "📊 Overview", "🗺️ Choropleth Map", "📍 Regional Analysis",
            "🔗 Correlation & Gini", "🎯 Quintile Analysis", "🔍 County Explorer", "📋 Full Rankings"]

with st.sidebar:
    st.markdown('<div style="font-family:Syne,sans-serif;font-size:1.1rem;font-weight:800;color:#fff;margin-bottom:1rem;">🇰🇪 Navigation</div>', unsafe_allow_html=True)
    section = st.radio("Go to", SECTIONS)
    st.markdown("---")
    st.markdown(f'<div style="color:{MUTED};font-size:0.75rem;">Data: KNBS 2024 Projections<br>Budget: FY 2023/24 Equitable Share<br>Counties: 47</div>', unsafe_allow_html=True)

# ── HOME PAGE ─────────────────────────────────────────────────────────────────
if "Home" in section:
    st.markdown('<div class="badge">FY 2023/24 · All 47 Counties</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-title">🇰🇪 Kenya County<br>Budget Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Equitable Share Allocations · KNBS 2024 Population Projections</div>', unsafe_allow_html=True)

    # ── 2-column metric grid ──
    st.markdown('<div class="section-header">Key Metrics</div>', unsafe_allow_html=True)
    m1, m2 = st.columns(2)
    m3, m4 = st.columns(2)
    with m1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">📊 National Avg Budget / Person</div>
            <div class="metric-value metric-accent-green">KES {int(df["budget_per_person"].mean()):,}</div>
            <div style="color:{MUTED};font-size:0.78rem;margin-top:0.5rem;">Total budget: KES {df["budget_billion"].sum():.1f}B &nbsp;·&nbsp; Population: {df["population_2024"].sum()/1e6:.1f}M</div>
        </div>""", unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">🏆 Highest Funded County</div>
            <div class="metric-value metric-accent-green" style="font-size:1.6rem;">{top_county["county"]}</div>
            <div style="color:#10b981;font-size:0.9rem;margin-top:0.5rem;font-weight:600;">KES {int(top_county["budget_per_person"]):,} per person &nbsp;·&nbsp; {top_county["region"]} Region</div>
        </div>""", unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">📉 Lowest Funded County</div>
            <div class="metric-value metric-accent-red" style="font-size:1.6rem;">{bot_county["county"]}</div>
            <div style="color:#ef4444;font-size:0.9rem;margin-top:0.5rem;font-weight:600;">KES {int(bot_county["budget_per_person"]):,} per person &nbsp;·&nbsp; {bot_county["region"]} Region</div>
        </div>""", unsafe_allow_html=True)
    with m4:
        inequality_level = "Low" if gini < 0.2 else "Moderate" if gini < 0.35 else "High"
        gap_x = int(top_county["budget_per_person"] / bot_county["budget_per_person"])
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">⚖️ Funding Inequality (Gini)</div>
            <div class="metric-value metric-accent-amber">{gini:.3f}</div>
            <div style="color:{MUTED};font-size:0.78rem;margin-top:0.5rem;">{inequality_level} inequality &nbsp;·&nbsp; Highest county gets <strong style="color:#f59e0b;">{gap_x}x</strong> more per person than lowest</div>
        </div>""", unsafe_allow_html=True)

    # ── Navigation buttons ──
    st.markdown('<div class="section-header">Explore the Dashboard</div>', unsafe_allow_html=True)
    NAV_ITEMS = [
        ("📊", "Overview",          "Bar charts of all 47 counties ranked by budget per person",      "Overview"),
        ("🗺️", "Choropleth Map",    "Interactive Kenya map colored by budget per citizen",            "Choropleth Map"),
        ("📍", "Regional Analysis", "Compare 8 regions — budgets, pie charts & spread",              "Regional Analysis"),
        ("🔗", "Correlation & Gini","Lorenz curve, Gini deep-dive & population scatter plots",       "Correlation & Gini"),
        ("🎯", "Quintile Analysis", "Counties grouped into 5 funding bands with regional boxplots",  "Quintile Analysis"),
        ("🔍", "County Explorer",   "Pick any county and see its rank, region & budget vs average",  "County Explorer"),
        ("📋", "Full Rankings",     "Filterable table of all 47 counties with CSV download",         "Full Rankings"),
    ]
    row1 = st.columns(3)
    row2 = st.columns(3)
    row3 = st.columns(1)
    rows = [row1[0], row1[1], row1[2], row2[0], row2[1], row2[2], row3[0]]
    for col, (icon, title, desc, key) in zip(rows, NAV_ITEMS):
        with col:
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#111827,#1a2340);border:1px solid #1e2d4a;
                        border-radius:12px;padding:1.2rem 1.3rem;margin-bottom:0.8rem;
                        transition:border-color 0.2s;">
                <div style="font-size:1.6rem;margin-bottom:0.4rem;">{icon}</div>
                <div style="font-family:Syne,sans-serif;font-size:0.95rem;font-weight:700;
                            color:#fff;margin-bottom:0.3rem;">{title}</div>
                <div style="font-size:0.78rem;color:{MUTED};line-height:1.4;">{desc}</div>
            </div>""", unsafe_allow_html=True)
            if st.button(f"Open {title}", key=f"nav_{key}", use_container_width=True):
                st.session_state["nav_target"] = f"{'📊' if title=='Overview' else '🗺️' if title=='Choropleth Map' else '📍' if title=='Regional Analysis' else '🔗' if title=='Correlation & Gini' else '🎯' if title=='Quintile Analysis' else '🔍' if title=='County Explorer' else '📋'} {title}"
                st.rerun()

    st.markdown(f"""
    <div class="insight-box" style="margin-top:1rem;">
        💡 <strong>Key finding:</strong> {top_county["county"]} receives <strong>KES {int(top_county["budget_per_person"]):,}/person</strong>
        — {gap_x}x more than {bot_county["county"]} which gets <strong>KES {int(bot_county["budget_per_person"]):,}/person</strong>.
        The Gini coefficient of <strong>{gini:.3f}</strong> reflects {inequality_level.lower()} inequality across all counties.
    </div>""", unsafe_allow_html=True)

# Handle nav button clicks
if "nav_target" in st.session_state:
    section = st.session_state.pop("nav_target")

# ── OVERVIEW ─────────────────────────────────────────────────────────────────
if "Overview" in section:
    st.markdown('<div class="section-header">Budget Per Citizen — All 47 Counties</div>', unsafe_allow_html=True)
    fig1, ax1 = plt.subplots(figsize=(18, 5)); style_chart(fig1, ax1)
    median = sorted_df['budget_per_person'].median()
    colors = [RED if v > median * 1.5 else BLUE for v in sorted_df['budget_per_person']]
    ax1.bar(sorted_df['county'], sorted_df['budget_per_person'], color=colors, edgecolor=DARK_BG, linewidth=0.4, width=0.75)
    ax1.axhline(df['budget_per_person'].mean(), color=AMBER, linestyle='--', linewidth=1.5, label=f"National Average: KES {int(df['budget_per_person'].mean()):,}")
    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
    ax1.legend(facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=9)
    ax1.set_ylabel('KES per Person', fontsize=9)
    plt.xticks(rotation=90, fontsize=7.5, color=MUTED); plt.tight_layout(); st.pyplot(fig1); plt.close()

    col_l, col_r = st.columns(2)
    top10 = sorted_df.head(10); bot10 = sorted_df.tail(10).sort_values('budget_per_person')
    with col_l:
        st.markdown('<div class="section-header">Top 10 Counties</div>', unsafe_allow_html=True)
        fig2, ax2 = plt.subplots(figsize=(7, 5)); style_chart(fig2, ax2)
        ax2.barh(top10['county'], top10['budget_per_person'], color=GREEN, edgecolor=DARK_BG, linewidth=0.4)
        ax2.set_title('Highest Budget Per Person', fontsize=11, fontweight='bold')
        ax2.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
        ax2.set_xlabel('KES per Person'); ax2.invert_yaxis(); ax2.tick_params(axis='y', labelsize=9, colors=TEXT)
        plt.tight_layout(); st.pyplot(fig2); plt.close()
    with col_r:
        st.markdown('<div class="section-header">Bottom 10 Counties</div>', unsafe_allow_html=True)
        fig3, ax3 = plt.subplots(figsize=(7, 5)); style_chart(fig3, ax3)
        ax3.barh(bot10['county'], bot10['budget_per_person'], color=RED, edgecolor=DARK_BG, linewidth=0.4)
        ax3.set_title('Lowest Budget Per Person', fontsize=11, fontweight='bold')
        ax3.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
        ax3.set_xlabel('KES per Person'); ax3.invert_yaxis(); ax3.tick_params(axis='y', labelsize=9, colors=TEXT)
        plt.tight_layout(); st.pyplot(fig3); plt.close()

# ── CHOROPLETH MAP ────────────────────────────────────────────────────────────
elif "Choropleth" in section:
    st.markdown('<div class="section-header">Kenya County Budget Per Citizen — Map View</div>', unsafe_allow_html=True)
    try:
        kenya_geojson = load_geojson()
        df_map = df.copy()
        df_map['county_mapped'] = df_map['county'].apply(lambda x: NAME_MAP.get(x, x))
        fig_map = px.choropleth(
            df_map,
            geojson=kenya_geojson,
            locations='county_mapped',
            featureidkey='properties.COUNTY_NAM',
            color='budget_per_person',
            color_continuous_scale='RdYlGn',
            hover_name='county',
            hover_data={
                'county_mapped': False,
                'budget_per_person': ':,',
                'budget_billion': True,
                'population_2024': ':,'
            },
            labels={
                'budget_per_person': 'KES/Person',
                'budget_billion': 'Budget (KES B)',
                'population_2024': 'Population'
            },
        )
        fig_map.update_geos(fitbounds="locations", visible=False)
        fig_map.update_layout(
            paper_bgcolor='#0a0f1e', plot_bgcolor='#0a0f1e', font_color='#e8eaf0',
            coloraxis_colorbar=dict(
                title=dict(text='KES/Person', font=dict(color='#e8eaf0')),
                tickfont=dict(color='#e8eaf0'),
                bgcolor='#111827',
                outlinecolor='#1e2d4a',
            ),
            margin=dict(l=0, r=0, t=20, b=0), height=600
        )
        st.plotly_chart(fig_map, use_container_width=True)
        st.markdown('<div class="insight-box">🟢 <strong>Green</strong> = higher budget per person &nbsp;·&nbsp; 🔴 <strong>Red</strong> = lower budget per person<br>Hover over any county to see its exact budget, population and KES per person.</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Could not load map: {e}")

# ── REGIONAL ─────────────────────────────────────────────────────────────────
elif "Regional" in section:
    st.markdown('<div class="section-header">Regional Budget Per Person</div>', unsafe_allow_html=True)
    colors_r = [REGION_COLORS[r] for r in regional['region']]
    fig_r1, axes_r1 = plt.subplots(1, 2, figsize=(16, 5)); style_chart(fig_r1, axes_r1)
    axes_r1[0].barh(regional['region'], regional['budget_per_person'], color=colors_r, edgecolor=DARK_BG, linewidth=0.4)
    axes_r1[0].axvline(df['budget_per_person'].mean(), color=AMBER, linestyle='--', linewidth=1.2, label='National Avg')
    axes_r1[0].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
    axes_r1[0].set_title('Average Budget Per Person by Region', fontsize=11, fontweight='bold')
    axes_r1[0].set_xlabel('KES per Person'); axes_r1[0].invert_yaxis()
    axes_r1[0].tick_params(axis='y', labelsize=9, colors=TEXT)
    axes_r1[0].legend(facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=8)
    wedges, texts, autotexts = axes_r1[1].pie(regional['total_budget'], labels=regional['region'], autopct='%1.1f%%', colors=colors_r, startangle=90, pctdistance=0.75, textprops={'color': TEXT, 'fontsize': 8})
    for at in autotexts: at.set_color(DARK_BG); at.set_fontsize(7)
    axes_r1[1].set_title('Share of Total Budget by Region', fontsize=11, fontweight='bold')
    plt.tight_layout(); st.pyplot(fig_r1); plt.close()

    st.markdown('<div class="section-header">Within-Region Budget Spread</div>', unsafe_allow_html=True)
    reg_min = df.groupby('region')['budget_per_person'].min().reset_index().rename(columns={'budget_per_person':'min_bpp'})
    reg_max = df.groupby('region')['budget_per_person'].max().reset_index().rename(columns={'budget_per_person':'max_bpp'})
    regional_ext = regional.merge(reg_min, on='region').merge(reg_max, on='region')
    fig_r2, ax_r2 = plt.subplots(figsize=(14, 5)); style_chart(fig_r2, ax_r2)
    ax_r2.barh(regional_ext['region'], regional_ext['max_bpp'] - regional_ext['min_bpp'], left=regional_ext['min_bpp'], color=colors_r, alpha=0.5, edgecolor=DARK_BG, linewidth=0.4, height=0.5)
    ax_r2.scatter(regional_ext['budget_per_person'], regional_ext['region'], color=TEXT, s=50, zorder=5, label='Regional Avg/Person')
    ax_r2.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
    ax_r2.set_title('Budget/Person Range Within Each Region (min → max)', fontsize=11, fontweight='bold')
    ax_r2.set_xlabel('KES per Person'); ax_r2.invert_yaxis(); ax_r2.tick_params(axis='y', labelsize=9, colors=TEXT)
    ax_r2.legend(facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=8)
    plt.tight_layout(); st.pyplot(fig_r2); plt.close()

    st.markdown('<div class="section-header">Regional Summary Table</div>', unsafe_allow_html=True)
    reg_table = regional[['region','counties','total_pop','total_budget','budget_per_person']].copy()
    reg_table.columns = ['Region','Counties','Population','Budget (KES B)','Avg Budget/Person (KES)']
    reg_table = reg_table.reset_index(drop=True); reg_table.index += 1
    st.dataframe(reg_table, use_container_width=True)

# ── CORRELATION & GINI ────────────────────────────────────────────────────────
elif "Correlation" in section:
    st.markdown('<div class="section-header">Gini Coefficient & Distribution</div>', unsafe_allow_html=True)
    col_g1, col_g2 = st.columns([1, 2])
    with col_g1:
        st.markdown(f"""
        <div class="metric-card" style="margin-top:1rem;">
            <div class="metric-label">Gini Coefficient</div>
            <div class="metric-value metric-accent-amber">{gini:.4f}</div>
        </div>
        <div class="insight-box">
            A Gini of <strong>{gini:.3f}</strong> indicates <strong>{'high' if gini > 0.35 else 'moderate' if gini > 0.25 else 'low'} inequality</strong> in per-capita budget allocation.<br><br>
            The top county (<strong>{sorted_df.iloc[0]['county']}</strong>) receives <strong>{sorted_df.iloc[0]['budget_per_person'] / sorted_df.iloc[-1]['budget_per_person']:.1f}x</strong> more per person than the bottom (<strong>{sorted_df.iloc[-1]['county']}</strong>).
        </div>""", unsafe_allow_html=True)
    with col_g2:
        fig_g, axes_g = plt.subplots(1, 2, figsize=(12, 4)); style_chart(fig_g, axes_g)
        sorted_vals = np.sort(df['budget_per_person'].values); n = len(sorted_vals)
        lorenz_x = np.concatenate([[0], np.arange(1, n+1) / n])
        lorenz_y = np.concatenate([[0], np.cumsum(sorted_vals) / sorted_vals.sum()])
        axes_g[0].plot(lorenz_x, lorenz_y, color=BLUE, linewidth=2.5, label=f'Lorenz Curve (Gini={gini:.3f})')
        axes_g[0].plot([0,1],[0,1], color=MUTED, linestyle='--', linewidth=1.2, label='Perfect Equality')
        axes_g[0].fill_between(lorenz_x, lorenz_y, lorenz_x, alpha=0.15, color=RED)
        axes_g[0].set_title('Lorenz Curve', fontsize=11, fontweight='bold')
        axes_g[0].set_xlabel('Cumulative Share of Counties'); axes_g[0].set_ylabel('Cumulative Budget Share')
        axes_g[0].legend(facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=8)
        axes_g[1].hist(df['budget_per_person'], bins=12, color=BLUE, edgecolor=DARK_BG, linewidth=0.5, alpha=0.85)
        axes_g[1].axvline(df['budget_per_person'].mean(), color=AMBER, linestyle='--', linewidth=1.5, label=f"Mean: KES {int(df['budget_per_person'].mean()):,}")
        axes_g[1].axvline(df['budget_per_person'].median(), color=GREEN, linestyle='--', linewidth=1.5, label=f"Median: KES {int(df['budget_per_person'].median()):,}")
        axes_g[1].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
        axes_g[1].set_title('Budget/Person Distribution', fontsize=11, fontweight='bold')
        axes_g[1].set_xlabel('KES per Person'); axes_g[1].set_ylabel('Number of Counties')
        axes_g[1].legend(facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=8)
        plt.tight_layout(); st.pyplot(fig_g); plt.close()

    st.markdown('<div class="section-header">Correlation Analysis</div>', unsafe_allow_html=True)
    col_c1, col_c2 = st.columns(2)
    with col_c1: st.markdown(f'<div class="metric-card"><div class="metric-label">Population vs Absolute Budget</div><div class="metric-value metric-accent-green">r = {corr_bp:.3f}</div></div>', unsafe_allow_html=True)
    with col_c2: st.markdown(f'<div class="metric-card"><div class="metric-label">Population vs Budget Per Person</div><div class="metric-value metric-accent-red">r = {corr_bpp:.3f}</div></div>', unsafe_allow_html=True)

    colors_scatter = [REGION_COLORS[r] for r in df['region']]
    fig_c, axes_c = plt.subplots(1, 2, figsize=(16, 5)); style_chart(fig_c, axes_c)
    axes_c[0].scatter(df['population_2024']/1e6, df['budget_billion'], c=colors_scatter, s=70, alpha=0.85, edgecolors='#1e2d4a', linewidth=0.6)
    m, b, *_ = stats.linregress(df['population_2024']/1e6, df['budget_billion'])
    x_line = np.linspace(df['population_2024'].min()/1e6, df['population_2024'].max()/1e6, 100)
    axes_c[0].plot(x_line, m*x_line+b, color=AMBER, linewidth=1.8, linestyle='--')
    for _, row in df.iterrows():
        if row['county'] in ['Nairobi','Lamu','Nakuru','Kiambu','Turkana']:
            axes_c[0].annotate(row['county'], (row['population_2024']/1e6, row['budget_billion']), textcoords='offset points', xytext=(6,4), fontsize=7.5, color=TEXT)
    legend_patches = [mpatches.Patch(color=v, label=k) for k, v in REGION_COLORS.items()]
    axes_c[0].legend(handles=legend_patches, facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=7, ncol=2, loc='upper left')
    axes_c[0].set_title('Population vs Absolute Budget', fontsize=11, fontweight='bold')
    axes_c[0].set_xlabel('Population (millions)'); axes_c[0].set_ylabel('Budget (KES Billions)')
    axes_c[1].scatter(df['population_2024']/1e6, df['budget_per_person'], c=colors_scatter, s=70, alpha=0.85, edgecolors='#1e2d4a', linewidth=0.6)
    m2, b2, *_ = stats.linregress(df['population_2024']/1e6, df['budget_per_person'])
    axes_c[1].plot(x_line, m2*x_line+b2, color=AMBER, linewidth=1.8, linestyle='--', label=f'r = {corr_bpp:.3f}')
    for _, row in df.iterrows():
        if row['county'] in ['Nairobi','Lamu','Nakuru','Kiambu','Marsabit']:
            axes_c[1].annotate(row['county'], (row['population_2024']/1e6, row['budget_per_person']), textcoords='offset points', xytext=(6,4), fontsize=7.5, color=TEXT)
    axes_c[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
    axes_c[1].set_title('Population vs Budget Per Person', fontsize=11, fontweight='bold')
    axes_c[1].set_xlabel('Population (millions)'); axes_c[1].set_ylabel('Budget Per Person (KES)')
    axes_c[1].legend(facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=9)
    plt.tight_layout(); st.pyplot(fig_c); plt.close()
    st.markdown(f'<div class="insight-box">📌 <strong>Key finding:</strong> Larger counties receive significantly <em>less</em> per person (r = {corr_bpp:.3f}, p &lt; 0.001). The equitable share formula disproportionately benefits low-population counties like Lamu, Marsabit and Samburu, while high-density counties like Nairobi, Kiambu and Nakuru receive the least per citizen.</div>', unsafe_allow_html=True)

# ── QUINTILE ──────────────────────────────────────────────────────────────────
elif "Quintile" in section:
    st.markdown('<div class="section-header">Quintile Analysis</div>', unsafe_allow_html=True)
    df_q = df.copy()
    df_q['quintile'] = pd.qcut(df_q['budget_per_person'], q=5, labels=['Q1 Bottom 20%','Q2','Q3 Middle','Q4','Q5 Top 20%'])
    quintile_summary = df_q.groupby('quintile', observed=True).agg(counties=('county','count'), avg_bpp=('budget_per_person','mean'), counties_list=('county', lambda x: ', '.join(sorted(x)))).reset_index()
    quintile_colors = [RED, '#f97316', AMBER, '#84cc16', GREEN]
    fig_q, axes_q = plt.subplots(1, 2, figsize=(16, 5)); style_chart(fig_q, axes_q)
    axes_q[0].bar(quintile_summary['quintile'], quintile_summary['avg_bpp'], color=quintile_colors, edgecolor=DARK_BG, linewidth=0.4)
    axes_q[0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
    axes_q[0].set_title('Average Budget Per Person by Quintile', fontsize=11, fontweight='bold')
    axes_q[0].set_ylabel('KES per Person'); axes_q[0].tick_params(axis='x', labelsize=8, colors=TEXT)
    region_order = regional['region'].tolist()
    region_data = [df[df['region'] == r]['budget_per_person'].values for r in region_order]
    bp = axes_q[1].boxplot(region_data, tick_labels=region_order, patch_artist=True, vert=True)
    for patch, region in zip(bp['boxes'], region_order):
        patch.set_facecolor(REGION_COLORS[region]); patch.set_alpha(0.7)
    for element in ['whiskers','caps','medians','fliers']:
        for item in bp[element]: item.set_color(TEXT)
    axes_q[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
    axes_q[1].set_title('Budget/Person Distribution by Region', fontsize=11, fontweight='bold')
    axes_q[1].set_ylabel('KES per Person'); axes_q[1].tick_params(axis='x', rotation=30, labelsize=8, colors=TEXT)
    plt.tight_layout(); st.pyplot(fig_q); plt.close()

    st.markdown('<div class="section-header">Counties by Quintile</div>', unsafe_allow_html=True)
    for i, (_, row) in enumerate(quintile_summary.iterrows()):
        color = quintile_colors[i]
        st.markdown(f'<div class="insight-box" style="border-left-color:{color}"><strong style="color:{color}">{row["quintile"]}</strong> &nbsp;·&nbsp; Avg: KES {int(row["avg_bpp"]):,}/person &nbsp;·&nbsp; {int(row["counties"])} counties<br><span style="color:#7a8aaa">{row["counties_list"]}</span></div>', unsafe_allow_html=True)

# ── COUNTY EXPLORER ───────────────────────────────────────────────────────────
elif "Explorer" in section:
    st.markdown('<div class="section-header">County Explorer</div>', unsafe_allow_html=True)
    col_s, col_info = st.columns([1, 2])
    with col_s:
        selected = st.selectbox('Select a County', options=sorted(df['county'].tolist()))
    with col_info:
        row = df[df['county'] == selected].iloc[0]
        rank = sorted_df[sorted_df['county'] == selected].index[0] + 1
        nat_avg = int(df['budget_per_person'].mean())
        diff = int(row['budget_per_person']) - nat_avg
        diff_str = f"+KES {diff:,}" if diff > 0 else f"-KES {abs(diff):,}"
        diff_color = "metric-accent-green" if diff > 0 else "metric-accent-red"
        reg_avg = int(regional[regional['region'] == row['region']]['budget_per_person'].values[0])
        ca, cb2, cc, cd = st.columns(4)
        with ca: st.markdown(f'<div class="metric-card"><div class="metric-label">Population</div><div class="metric-value" style="font-size:1.3rem">{int(row["population_2024"]):,}</div></div>', unsafe_allow_html=True)
        with cb2: st.markdown(f'<div class="metric-card"><div class="metric-label">Budget</div><div class="metric-value" style="font-size:1.3rem">KES {row["budget_billion"]}B</div></div>', unsafe_allow_html=True)
        with cc: st.markdown(f'<div class="metric-card"><div class="metric-label">Per Person · Rank #{rank}</div><div class="metric-value {diff_color}" style="font-size:1.3rem">KES {int(row["budget_per_person"]):,}</div></div>', unsafe_allow_html=True)
        with cd: st.markdown(f'<div class="metric-card"><div class="metric-label">Region ({row["region"]})</div><div class="metric-value" style="font-size:1.3rem">KES {reg_avg:,}</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="insight-box"><strong>{selected}</strong> is ranked <strong>#{rank} of 47</strong> counties by budget per person. It is <strong>{diff_str}</strong> vs the national average of KES {nat_avg:,}/person, and sits in the <strong>{row["region"]}</strong> region (regional avg: KES {reg_avg:,}/person).</div>', unsafe_allow_html=True)

# ── FULL RANKINGS ─────────────────────────────────────────────────────────────
elif "Rankings" in section:
    st.markdown('<div class="section-header">Full County Rankings</div>', unsafe_allow_html=True)
    region_filter = st.multiselect('Filter by Region', options=sorted(df['region'].unique()), default=sorted(df['region'].unique()))
    filtered = sorted_df[sorted_df['region'].isin(region_filter)]
    table = filtered[['county','region','population_2024','budget_billion','budget_per_person']].copy()
    table.columns = ['County','Region','Population (2024)','Budget (KES B)','Budget/Person (KES)']
    table = table.reset_index(drop=True); table.index += 1
    st.dataframe(table, use_container_width=True, height=600)
    csv = table.to_csv().encode('utf-8')
    st.download_button("⬇ Download as CSV", csv, "kenya_county_budget.csv", "text/csv")
