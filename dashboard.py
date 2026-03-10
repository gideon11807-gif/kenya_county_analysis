# # # # # # # import streamlit as st
# # # # # # # import pandas as pd
# # # # # # # import numpy as np
# # # # # # # import matplotlib.pyplot as plt
# # # # # # # import matplotlib.ticker as mticker
# # # # # # # import matplotlib.patches as mpatches
# # # # # # # import plotly.express as px
# # # # # # # import json
# # # # # # # import urllib.request
# # # # # # # from scipy import stats

# # # # # # # st.set_page_config(page_title="Kenya County Budget Analysis", page_icon="🇰🇪", layout="wide")

# # # # # # # st.markdown("""
# # # # # # # <style>
# # # # # # #     @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500&display=swap');
# # # # # # #     html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
# # # # # # #     .stApp { background-color: #0a0f1e; color: #e8eaf0; }
# # # # # # #     h1, h2, h3 { font-family: 'Syne', sans-serif !important; }
# # # # # # #     .hero-title { font-family: 'Syne', sans-serif; font-size: 3rem; font-weight: 800; color: #ffffff; line-height: 1.1; margin-bottom: 0.3rem; }
# # # # # # #     .hero-sub { font-size: 1rem; color: #7a8aaa; margin-bottom: 2rem; font-weight: 300; letter-spacing: 0.05em; }
# # # # # # #     .metric-card { background: linear-gradient(135deg, #111827 0%, #1a2340 100%); border: 1px solid #1e2d4a; border-radius: 12px; padding: 1.4rem 1.6rem; margin-bottom: 1rem; }
# # # # # # #     .metric-label { font-size: 0.72rem; font-weight: 500; color: #5a6a8a; text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 0.4rem; }
# # # # # # #     .metric-value { font-family: 'Syne', sans-serif; font-size: 1.9rem; font-weight: 700; color: #ffffff; line-height: 1; }
# # # # # # #     .metric-accent { color: #3b82f6; } .metric-accent-green { color: #10b981; } .metric-accent-red { color: #ef4444; } .metric-accent-amber { color: #f59e0b; }
# # # # # # #     .section-header { font-family: 'Syne', sans-serif; font-size: 1.1rem; font-weight: 700; color: #ffffff; text-transform: uppercase; letter-spacing: 0.08em; border-left: 3px solid #3b82f6; padding-left: 0.8rem; margin-bottom: 1rem; margin-top: 2rem; }
# # # # # # #     .badge { display: inline-block; background: #1e3a5f; color: #60a5fa; font-size: 0.7rem; font-weight: 600; padding: 2px 10px; border-radius: 20px; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 0.5rem; }
# # # # # # #     .insight-box { background: linear-gradient(135deg, #0f1f3d 0%, #1a2340 100%); border: 1px solid #1e3a5f; border-left: 3px solid #f59e0b; border-radius: 8px; padding: 1rem 1.2rem; margin: 0.5rem 0; font-size: 0.9rem; color: #c8d4e8; line-height: 1.6; }
# # # # # # #     footer {visibility: hidden;} #MainMenu {visibility: hidden;} header {visibility: hidden;}
# # # # # # # </style>
# # # # # # # """, unsafe_allow_html=True)

# # # # # # # DARK_BG = '#0a0f1e'; CARD_BG = '#111827'; BLUE = '#3b82f6'; GREEN = '#10b981'
# # # # # # # RED = '#ef4444'; AMBER = '#f59e0b'; TEXT = '#e8eaf0'; MUTED = '#7a8aaa'
# # # # # # # REGION_COLORS = {
# # # # # # #     'Nairobi': '#3b82f6', 'Central': '#10b981', 'Coast': '#f59e0b',
# # # # # # #     'Eastern': '#8b5cf6', 'North Eastern': '#ef4444', 'Nyanza': '#06b6d4',
# # # # # # #     'Rift Valley': '#f97316', 'Western': '#ec4899',
# # # # # # # }

# # # # # # # def style_chart(fig, axes):
# # # # # # #     fig.patch.set_facecolor(DARK_BG)
# # # # # # #     if not hasattr(axes, '__iter__'): axes = [axes]
# # # # # # #     for ax in axes:
# # # # # # #         ax.set_facecolor(CARD_BG); ax.tick_params(colors=MUTED, labelsize=8)
# # # # # # #         ax.xaxis.label.set_color(MUTED); ax.yaxis.label.set_color(MUTED); ax.title.set_color(TEXT)
# # # # # # #         for spine in ax.spines.values(): spine.set_edgecolor('#1e2d4a')

# # # # # # # def gini_coefficient(values):
# # # # # # #     arr = np.sort(np.array(values, dtype=float)); n = len(arr); cumsum = np.cumsum(arr)
# # # # # # #     return (2 * np.sum(np.arange(1, n+1) * arr) - (n+1) * cumsum[-1]) / (n * cumsum[-1])

# # # # # # # @st.cache_data
# # # # # # # def load_data():
# # # # # # #     df = pd.read_csv('data/county_data.csv')
# # # # # # #     df['budget_per_person'] = (df['budget_billion'] * 1_000_000_000) / df['population_2024']
# # # # # # #     df['budget_per_person'] = df['budget_per_person'].round(0).astype(int)
# # # # # # #     return df

# # # # # # # @st.cache_data
# # # # # # # def load_geojson():
# # # # # # #     url = "https://raw.githubusercontent.com/mikelmaron/kenya-election-data/master/data/counties.geojson"
# # # # # # #     with urllib.request.urlopen(url) as response:
# # # # # # #         geojson = json.loads(response.read().decode())
# # # # # # #     for feature in geojson['features']:
# # # # # # #         feature['properties']['COUNTY_NAM'] = feature['properties']['COUNTY_NAM'].strip().title()
# # # # # # #     return geojson

# # # # # # # df = load_data()
# # # # # # # sorted_df = df.sort_values('budget_per_person', ascending=False).reset_index(drop=True)
# # # # # # # regional = df.groupby('region').agg(counties=('county','count'), total_pop=('population_2024','sum'), total_budget=('budget_billion','sum')).reset_index()
# # # # # # # regional['budget_per_person'] = ((regional['total_budget'] * 1e9) / regional['total_pop']).astype(int)
# # # # # # # regional = regional.sort_values('budget_per_person', ascending=False)
# # # # # # # gini = gini_coefficient(df['budget_per_person'])
# # # # # # # corr_bpp, pval_bpp = stats.pearsonr(df['population_2024'], df['budget_per_person'])
# # # # # # # corr_bp, _ = stats.pearsonr(df['population_2024'], df['budget_billion'])

# # # # # # # with st.sidebar:
# # # # # # #     st.markdown('<div style="font-family:Syne,sans-serif;font-size:1.1rem;font-weight:800;color:#fff;margin-bottom:1rem;">🇰🇪 Navigation</div>', unsafe_allow_html=True)
# # # # # # #     section = st.radio("Go to", ["📊 Overview","🗺️ Choropleth Map","📍 Regional Analysis","🔗 Correlation & Gini","🎯 Quintile Analysis","🔍 County Explorer","📋 Full Rankings"])
# # # # # # #     st.markdown("---")
# # # # # # #     st.markdown(f'<div style="color:{MUTED};font-size:0.75rem;">Data: KNBS 2024 Projections<br>Budget: FY 2023/24 Equitable Share<br>Counties: 47</div>', unsafe_allow_html=True)

# # # # # # # st.markdown('<div class="badge">FY 2023/24 · All 47 Counties</div>', unsafe_allow_html=True)
# # # # # # # st.markdown('<div class="hero-title">🇰🇪 Kenya County<br>Budget Analysis</div>', unsafe_allow_html=True)
# # # # # # # st.markdown('<div class="hero-sub">Equitable Share Allocations · KNBS 2024 Population Projections</div>', unsafe_allow_html=True)

# # # # # # # c1,c2,c3,c4,c5 = st.columns(5)
# # # # # # # with c1: st.markdown(f'<div class="metric-card"><div class="metric-label">Total Population</div><div class="metric-value metric-accent">{df["population_2024"].sum()/1e6:.1f}M</div></div>', unsafe_allow_html=True)
# # # # # # # with c2: st.markdown(f'<div class="metric-card"><div class="metric-label">Total Budget</div><div class="metric-value">KES {df["budget_billion"].sum():.1f}B</div></div>', unsafe_allow_html=True)
# # # # # # # with c3: st.markdown(f'<div class="metric-card"><div class="metric-label">National Avg / Person</div><div class="metric-value metric-accent-green">KES {int(df["budget_per_person"].mean()):,}</div></div>', unsafe_allow_html=True)
# # # # # # # with c4:
# # # # # # #     gap = sorted_df.iloc[0]['budget_per_person'] - sorted_df.iloc[-1]['budget_per_person']
# # # # # # #     st.markdown(f'<div class="metric-card"><div class="metric-label">Highest vs Lowest Gap</div><div class="metric-value metric-accent-red">KES {gap:,}</div></div>', unsafe_allow_html=True)
# # # # # # # with c5: st.markdown(f'<div class="metric-card"><div class="metric-label">Gini Coefficient</div><div class="metric-value metric-accent-amber">{gini:.3f}</div></div>', unsafe_allow_html=True)

# # # # # # # # ── OVERVIEW ─────────────────────────────────────────────────────────────────
# # # # # # # if "Overview" in section:
# # # # # # #     st.markdown('<div class="section-header">Budget Per Citizen — All 47 Counties</div>', unsafe_allow_html=True)
# # # # # # #     fig1, ax1 = plt.subplots(figsize=(18, 5)); style_chart(fig1, ax1)
# # # # # # #     median = sorted_df['budget_per_person'].median()
# # # # # # #     colors = [RED if v > median * 1.5 else BLUE for v in sorted_df['budget_per_person']]
# # # # # # #     ax1.bar(sorted_df['county'], sorted_df['budget_per_person'], color=colors, edgecolor=DARK_BG, linewidth=0.4, width=0.75)
# # # # # # #     ax1.axhline(df['budget_per_person'].mean(), color=AMBER, linestyle='--', linewidth=1.5, label=f"National Average: KES {int(df['budget_per_person'].mean()):,}")
# # # # # # #     ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
# # # # # # #     ax1.legend(facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=9)
# # # # # # #     ax1.set_ylabel('KES per Person', fontsize=9)
# # # # # # #     plt.xticks(rotation=90, fontsize=7.5, color=MUTED); plt.tight_layout(); st.pyplot(fig1); plt.close()

# # # # # # #     col_l, col_r = st.columns(2)
# # # # # # #     top10 = sorted_df.head(10); bot10 = sorted_df.tail(10).sort_values('budget_per_person')
# # # # # # #     with col_l:
# # # # # # #         st.markdown('<div class="section-header">Top 10 Counties</div>', unsafe_allow_html=True)
# # # # # # #         fig2, ax2 = plt.subplots(figsize=(7, 5)); style_chart(fig2, ax2)
# # # # # # #         ax2.barh(top10['county'], top10['budget_per_person'], color=GREEN, edgecolor=DARK_BG, linewidth=0.4)
# # # # # # #         ax2.set_title('Highest Budget Per Person', fontsize=11, fontweight='bold')
# # # # # # #         ax2.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
# # # # # # #         ax2.set_xlabel('KES per Person'); ax2.invert_yaxis(); ax2.tick_params(axis='y', labelsize=9, colors=TEXT)
# # # # # # #         plt.tight_layout(); st.pyplot(fig2); plt.close()
# # # # # # #     with col_r:
# # # # # # #         st.markdown('<div class="section-header">Bottom 10 Counties</div>', unsafe_allow_html=True)
# # # # # # #         fig3, ax3 = plt.subplots(figsize=(7, 5)); style_chart(fig3, ax3)
# # # # # # #         ax3.barh(bot10['county'], bot10['budget_per_person'], color=RED, edgecolor=DARK_BG, linewidth=0.4)
# # # # # # #         ax3.set_title('Lowest Budget Per Person', fontsize=11, fontweight='bold')
# # # # # # #         ax3.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
# # # # # # #         ax3.set_xlabel('KES per Person'); ax3.invert_yaxis(); ax3.tick_params(axis='y', labelsize=9, colors=TEXT)
# # # # # # #         plt.tight_layout(); st.pyplot(fig3); plt.close()

# # # # # # # # ── CHOROPLETH MAP ────────────────────────────────────────────────────────────
# # # # # # # elif "Choropleth" in section:
# # # # # # #     st.markdown('<div class="section-header">Kenya County Budget Per Citizen — Map View</div>', unsafe_allow_html=True)
# # # # # # #     try:
# # # # # # #         kenya_geojson = load_geojson()
# # # # # # #         fig_map = px.choropleth(
# # # # # # #             df,
# # # # # # #             geojson=kenya_geojson,
# # # # # # #             locations='county',
# # # # # # #             featureidkey='properties.COUNTY_NAM',
# # # # # # #             color='budget_per_person',
# # # # # # #             color_continuous_scale='RdYlGn',
# # # # # # #             hover_name='county',
# # # # # # #             hover_data={'budget_per_person': ':,', 'budget_billion': True, 'population_2024': ':,'},
# # # # # # #             labels={'budget_per_person': 'KES/Person', 'budget_billion': 'Budget (KES B)', 'population_2024': 'Population'},
# # # # # # #         )
# # # # # # #         fig_map.update_geos(fitbounds="locations", visible=False)
# # # # # # #         fig_map.update_layout(
# # # # # # #             paper_bgcolor='#0a0f1e', plot_bgcolor='#0a0f1e', font_color='#e8eaf0',
# # # # # # #             coloraxis_colorbar=dict(title='KES/Person', tickfont=dict(color='#e8eaf0'), titlefont=dict(color='#e8eaf0')),
# # # # # # #             margin=dict(l=0, r=0, t=20, b=0), height=600
# # # # # # #         )
# # # # # # #         st.plotly_chart(fig_map, use_container_width=True)
# # # # # # #         st.markdown('<div class="insight-box">🟢 <strong>Green</strong> = higher budget per person &nbsp;·&nbsp; 🔴 <strong>Red</strong> = lower budget per person<br>Hover over any county to see its exact budget, population and KES per person.</div>', unsafe_allow_html=True)
# # # # # # #     except Exception as e:
# # # # # # #         st.error(f"Could not load map: {e}")

# # # # # # # # ── REGIONAL ─────────────────────────────────────────────────────────────────
# # # # # # # elif "Regional" in section:
# # # # # # #     st.markdown('<div class="section-header">Regional Budget Per Person</div>', unsafe_allow_html=True)
# # # # # # #     colors_r = [REGION_COLORS[r] for r in regional['region']]
# # # # # # #     fig_r1, axes_r1 = plt.subplots(1, 2, figsize=(16, 5)); style_chart(fig_r1, axes_r1)
# # # # # # #     axes_r1[0].barh(regional['region'], regional['budget_per_person'], color=colors_r, edgecolor=DARK_BG, linewidth=0.4)
# # # # # # #     axes_r1[0].axvline(df['budget_per_person'].mean(), color=AMBER, linestyle='--', linewidth=1.2, label='National Avg')
# # # # # # #     axes_r1[0].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
# # # # # # #     axes_r1[0].set_title('Average Budget Per Person by Region', fontsize=11, fontweight='bold')
# # # # # # #     axes_r1[0].set_xlabel('KES per Person'); axes_r1[0].invert_yaxis()
# # # # # # #     axes_r1[0].tick_params(axis='y', labelsize=9, colors=TEXT)
# # # # # # #     axes_r1[0].legend(facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=8)
# # # # # # #     wedges, texts, autotexts = axes_r1[1].pie(regional['total_budget'], labels=regional['region'], autopct='%1.1f%%', colors=colors_r, startangle=90, pctdistance=0.75, textprops={'color': TEXT, 'fontsize': 8})
# # # # # # #     for at in autotexts: at.set_color(DARK_BG); at.set_fontsize(7)
# # # # # # #     axes_r1[1].set_title('Share of Total Budget by Region', fontsize=11, fontweight='bold')
# # # # # # #     plt.tight_layout(); st.pyplot(fig_r1); plt.close()

# # # # # # #     st.markdown('<div class="section-header">Within-Region Budget Spread</div>', unsafe_allow_html=True)
# # # # # # #     reg_min = df.groupby('region')['budget_per_person'].min().reset_index().rename(columns={'budget_per_person':'min_bpp'})
# # # # # # #     reg_max = df.groupby('region')['budget_per_person'].max().reset_index().rename(columns={'budget_per_person':'max_bpp'})
# # # # # # #     regional_ext = regional.merge(reg_min, on='region').merge(reg_max, on='region')
# # # # # # #     fig_r2, ax_r2 = plt.subplots(figsize=(14, 5)); style_chart(fig_r2, ax_r2)
# # # # # # #     ax_r2.barh(regional_ext['region'], regional_ext['max_bpp'] - regional_ext['min_bpp'], left=regional_ext['min_bpp'], color=colors_r, alpha=0.5, edgecolor=DARK_BG, linewidth=0.4, height=0.5)
# # # # # # #     ax_r2.scatter(regional_ext['budget_per_person'], regional_ext['region'], color=TEXT, s=50, zorder=5, label='Regional Avg/Person')
# # # # # # #     ax_r2.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
# # # # # # #     ax_r2.set_title('Budget/Person Range Within Each Region (min → max)', fontsize=11, fontweight='bold')
# # # # # # #     ax_r2.set_xlabel('KES per Person'); ax_r2.invert_yaxis(); ax_r2.tick_params(axis='y', labelsize=9, colors=TEXT)
# # # # # # #     ax_r2.legend(facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=8)
# # # # # # #     plt.tight_layout(); st.pyplot(fig_r2); plt.close()

# # # # # # #     st.markdown('<div class="section-header">Regional Summary Table</div>', unsafe_allow_html=True)
# # # # # # #     reg_table = regional[['region','counties','total_pop','total_budget','budget_per_person']].copy()
# # # # # # #     reg_table.columns = ['Region','Counties','Population','Budget (KES B)','Avg Budget/Person (KES)']
# # # # # # #     reg_table = reg_table.reset_index(drop=True); reg_table.index += 1
# # # # # # #     st.dataframe(reg_table, use_container_width=True)

# # # # # # # # ── CORRELATION & GINI ────────────────────────────────────────────────────────
# # # # # # # elif "Correlation" in section:
# # # # # # #     st.markdown('<div class="section-header">Gini Coefficient & Distribution</div>', unsafe_allow_html=True)
# # # # # # #     col_g1, col_g2 = st.columns([1, 2])
# # # # # # #     with col_g1:
# # # # # # #         st.markdown(f"""
# # # # # # #         <div class="metric-card" style="margin-top:1rem;">
# # # # # # #             <div class="metric-label">Gini Coefficient</div>
# # # # # # #             <div class="metric-value metric-accent-amber">{gini:.4f}</div>
# # # # # # #         </div>
# # # # # # #         <div class="insight-box">
# # # # # # #             A Gini of <strong>{gini:.3f}</strong> indicates <strong>{'high' if gini > 0.35 else 'moderate' if gini > 0.25 else 'low'} inequality</strong> in per-capita budget allocation.<br><br>
# # # # # # #             The top county (<strong>{sorted_df.iloc[0]['county']}</strong>) receives <strong>{sorted_df.iloc[0]['budget_per_person'] / sorted_df.iloc[-1]['budget_per_person']:.1f}x</strong> more per person than the bottom (<strong>{sorted_df.iloc[-1]['county']}</strong>).
# # # # # # #         </div>""", unsafe_allow_html=True)
# # # # # # #     with col_g2:
# # # # # # #         fig_g, axes_g = plt.subplots(1, 2, figsize=(12, 4)); style_chart(fig_g, axes_g)
# # # # # # #         sorted_vals = np.sort(df['budget_per_person'].values); n = len(sorted_vals)
# # # # # # #         lorenz_x = np.concatenate([[0], np.arange(1, n+1) / n])
# # # # # # #         lorenz_y = np.concatenate([[0], np.cumsum(sorted_vals) / sorted_vals.sum()])
# # # # # # #         axes_g[0].plot(lorenz_x, lorenz_y, color=BLUE, linewidth=2.5, label=f'Lorenz Curve (Gini={gini:.3f})')
# # # # # # #         axes_g[0].plot([0,1],[0,1], color=MUTED, linestyle='--', linewidth=1.2, label='Perfect Equality')
# # # # # # #         axes_g[0].fill_between(lorenz_x, lorenz_y, lorenz_x, alpha=0.15, color=RED)
# # # # # # #         axes_g[0].set_title('Lorenz Curve', fontsize=11, fontweight='bold')
# # # # # # #         axes_g[0].set_xlabel('Cumulative Share of Counties'); axes_g[0].set_ylabel('Cumulative Budget Share')
# # # # # # #         axes_g[0].legend(facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=8)
# # # # # # #         axes_g[1].hist(df['budget_per_person'], bins=12, color=BLUE, edgecolor=DARK_BG, linewidth=0.5, alpha=0.85)
# # # # # # #         axes_g[1].axvline(df['budget_per_person'].mean(), color=AMBER, linestyle='--', linewidth=1.5, label=f"Mean: KES {int(df['budget_per_person'].mean()):,}")
# # # # # # #         axes_g[1].axvline(df['budget_per_person'].median(), color=GREEN, linestyle='--', linewidth=1.5, label=f"Median: KES {int(df['budget_per_person'].median()):,}")
# # # # # # #         axes_g[1].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
# # # # # # #         axes_g[1].set_title('Budget/Person Distribution', fontsize=11, fontweight='bold')
# # # # # # #         axes_g[1].set_xlabel('KES per Person'); axes_g[1].set_ylabel('Number of Counties')
# # # # # # #         axes_g[1].legend(facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=8)
# # # # # # #         plt.tight_layout(); st.pyplot(fig_g); plt.close()

# # # # # # #     st.markdown('<div class="section-header">Correlation Analysis</div>', unsafe_allow_html=True)
# # # # # # #     col_c1, col_c2 = st.columns(2)
# # # # # # #     with col_c1: st.markdown(f'<div class="metric-card"><div class="metric-label">Population vs Absolute Budget</div><div class="metric-value metric-accent-green">r = {corr_bp:.3f}</div></div>', unsafe_allow_html=True)
# # # # # # #     with col_c2: st.markdown(f'<div class="metric-card"><div class="metric-label">Population vs Budget Per Person</div><div class="metric-value metric-accent-red">r = {corr_bpp:.3f}</div></div>', unsafe_allow_html=True)

# # # # # # #     colors_scatter = [REGION_COLORS[r] for r in df['region']]
# # # # # # #     fig_c, axes_c = plt.subplots(1, 2, figsize=(16, 5)); style_chart(fig_c, axes_c)
# # # # # # #     axes_c[0].scatter(df['population_2024']/1e6, df['budget_billion'], c=colors_scatter, s=70, alpha=0.85, edgecolors='#1e2d4a', linewidth=0.6)
# # # # # # #     m, b, *_ = stats.linregress(df['population_2024']/1e6, df['budget_billion'])
# # # # # # #     x_line = np.linspace(df['population_2024'].min()/1e6, df['population_2024'].max()/1e6, 100)
# # # # # # #     axes_c[0].plot(x_line, m*x_line+b, color=AMBER, linewidth=1.8, linestyle='--')
# # # # # # #     for _, row in df.iterrows():
# # # # # # #         if row['county'] in ['Nairobi','Lamu','Nakuru','Kiambu','Turkana']:
# # # # # # #             axes_c[0].annotate(row['county'], (row['population_2024']/1e6, row['budget_billion']), textcoords='offset points', xytext=(6,4), fontsize=7.5, color=TEXT)
# # # # # # #     legend_patches = [mpatches.Patch(color=v, label=k) for k, v in REGION_COLORS.items()]
# # # # # # #     axes_c[0].legend(handles=legend_patches, facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=7, ncol=2, loc='upper left')
# # # # # # #     axes_c[0].set_title('Population vs Absolute Budget', fontsize=11, fontweight='bold')
# # # # # # #     axes_c[0].set_xlabel('Population (millions)'); axes_c[0].set_ylabel('Budget (KES Billions)')
# # # # # # #     axes_c[1].scatter(df['population_2024']/1e6, df['budget_per_person'], c=colors_scatter, s=70, alpha=0.85, edgecolors='#1e2d4a', linewidth=0.6)
# # # # # # #     m2, b2, *_ = stats.linregress(df['population_2024']/1e6, df['budget_per_person'])
# # # # # # #     axes_c[1].plot(x_line, m2*x_line+b2, color=AMBER, linewidth=1.8, linestyle='--', label=f'r = {corr_bpp:.3f}')
# # # # # # #     for _, row in df.iterrows():
# # # # # # #         if row['county'] in ['Nairobi','Lamu','Nakuru','Kiambu','Marsabit']:
# # # # # # #             axes_c[1].annotate(row['county'], (row['population_2024']/1e6, row['budget_per_person']), textcoords='offset points', xytext=(6,4), fontsize=7.5, color=TEXT)
# # # # # # #     axes_c[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
# # # # # # #     axes_c[1].set_title('Population vs Budget Per Person', fontsize=11, fontweight='bold')
# # # # # # #     axes_c[1].set_xlabel('Population (millions)'); axes_c[1].set_ylabel('Budget Per Person (KES)')
# # # # # # #     axes_c[1].legend(facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=9)
# # # # # # #     plt.tight_layout(); st.pyplot(fig_c); plt.close()
# # # # # # #     st.markdown(f'<div class="insight-box">📌 <strong>Key finding:</strong> Larger counties receive significantly <em>less</em> per person (r = {corr_bpp:.3f}, p &lt; 0.001). The equitable share formula disproportionately benefits low-population counties like Lamu, Marsabit and Samburu, while high-density counties like Nairobi, Kiambu and Nakuru receive the least per citizen.</div>', unsafe_allow_html=True)

# # # # # # # # ── QUINTILE ──────────────────────────────────────────────────────────────────
# # # # # # # elif "Quintile" in section:
# # # # # # #     st.markdown('<div class="section-header">Quintile Analysis</div>', unsafe_allow_html=True)
# # # # # # #     df_q = df.copy()
# # # # # # #     df_q['quintile'] = pd.qcut(df_q['budget_per_person'], q=5, labels=['Q1 Bottom 20%','Q2','Q3 Middle','Q4','Q5 Top 20%'])
# # # # # # #     quintile_summary = df_q.groupby('quintile', observed=True).agg(counties=('county','count'), avg_bpp=('budget_per_person','mean'), counties_list=('county', lambda x: ', '.join(sorted(x)))).reset_index()
# # # # # # #     quintile_colors = [RED, '#f97316', AMBER, '#84cc16', GREEN]
# # # # # # #     fig_q, axes_q = plt.subplots(1, 2, figsize=(16, 5)); style_chart(fig_q, axes_q)
# # # # # # #     axes_q[0].bar(quintile_summary['quintile'], quintile_summary['avg_bpp'], color=quintile_colors, edgecolor=DARK_BG, linewidth=0.4)
# # # # # # #     axes_q[0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
# # # # # # #     axes_q[0].set_title('Average Budget Per Person by Quintile', fontsize=11, fontweight='bold')
# # # # # # #     axes_q[0].set_ylabel('KES per Person'); axes_q[0].tick_params(axis='x', labelsize=8, colors=TEXT)
# # # # # # #     region_order = regional['region'].tolist()
# # # # # # #     region_data = [df[df['region'] == r]['budget_per_person'].values for r in region_order]
# # # # # # #     bp = axes_q[1].boxplot(region_data, tick_labels=region_order, patch_artist=True, vert=True)
# # # # # # #     for patch, region in zip(bp['boxes'], region_order):
# # # # # # #         patch.set_facecolor(REGION_COLORS[region]); patch.set_alpha(0.7)
# # # # # # #     for element in ['whiskers','caps','medians','fliers']:
# # # # # # #         for item in bp[element]: item.set_color(TEXT)
# # # # # # #     axes_q[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
# # # # # # #     axes_q[1].set_title('Budget/Person Distribution by Region', fontsize=11, fontweight='bold')
# # # # # # #     axes_q[1].set_ylabel('KES per Person'); axes_q[1].tick_params(axis='x', rotation=30, labelsize=8, colors=TEXT)
# # # # # # #     plt.tight_layout(); st.pyplot(fig_q); plt.close()

# # # # # # #     st.markdown('<div class="section-header">Counties by Quintile</div>', unsafe_allow_html=True)
# # # # # # #     for i, (_, row) in enumerate(quintile_summary.iterrows()):
# # # # # # #         color = quintile_colors[i]
# # # # # # #         st.markdown(f'<div class="insight-box" style="border-left-color:{color}"><strong style="color:{color}">{row["quintile"]}</strong> &nbsp;·&nbsp; Avg: KES {int(row["avg_bpp"]):,}/person &nbsp;·&nbsp; {int(row["counties"])} counties<br><span style="color:#7a8aaa">{row["counties_list"]}</span></div>', unsafe_allow_html=True)

# # # # # # # # ── COUNTY EXPLORER ───────────────────────────────────────────────────────────
# # # # # # # elif "Explorer" in section:
# # # # # # #     st.markdown('<div class="section-header">County Explorer</div>', unsafe_allow_html=True)
# # # # # # #     col_s, col_info = st.columns([1, 2])
# # # # # # #     with col_s:
# # # # # # #         selected = st.selectbox('Select a County', options=sorted(df['county'].tolist()))
# # # # # # #     with col_info:
# # # # # # #         row = df[df['county'] == selected].iloc[0]
# # # # # # #         rank = sorted_df[sorted_df['county'] == selected].index[0] + 1
# # # # # # #         nat_avg = int(df['budget_per_person'].mean())
# # # # # # #         diff = int(row['budget_per_person']) - nat_avg
# # # # # # #         diff_str = f"+KES {diff:,}" if diff > 0 else f"-KES {abs(diff):,}"
# # # # # # #         diff_color = "metric-accent-green" if diff > 0 else "metric-accent-red"
# # # # # # #         reg_avg = int(regional[regional['region'] == row['region']]['budget_per_person'].values[0])
# # # # # # #         ca, cb2, cc, cd = st.columns(4)
# # # # # # #         with ca: st.markdown(f'<div class="metric-card"><div class="metric-label">Population</div><div class="metric-value" style="font-size:1.3rem">{int(row["population_2024"]):,}</div></div>', unsafe_allow_html=True)
# # # # # # #         with cb2: st.markdown(f'<div class="metric-card"><div class="metric-label">Budget</div><div class="metric-value" style="font-size:1.3rem">KES {row["budget_billion"]}B</div></div>', unsafe_allow_html=True)
# # # # # # #         with cc: st.markdown(f'<div class="metric-card"><div class="metric-label">Per Person · Rank #{rank}</div><div class="metric-value {diff_color}" style="font-size:1.3rem">KES {int(row["budget_per_person"]):,}</div></div>', unsafe_allow_html=True)
# # # # # # #         with cd: st.markdown(f'<div class="metric-card"><div class="metric-label">Region ({row["region"]})</div><div class="metric-value" style="font-size:1.3rem">KES {reg_avg:,}</div></div>', unsafe_allow_html=True)
# # # # # # #         st.markdown(f'<div class="insight-box"><strong>{selected}</strong> is ranked <strong>#{rank} of 47</strong> counties by budget per person. It is <strong>{diff_str}</strong> vs the national average of KES {nat_avg:,}/person, and sits in the <strong>{row["region"]}</strong> region (regional avg: KES {reg_avg:,}/person).</div>', unsafe_allow_html=True)

# # # # # # # # ── FULL RANKINGS ─────────────────────────────────────────────────────────────
# # # # # # # elif "Rankings" in section:
# # # # # # #     st.markdown('<div class="section-header">Full County Rankings</div>', unsafe_allow_html=True)
# # # # # # #     region_filter = st.multiselect('Filter by Region', options=sorted(df['region'].unique()), default=sorted(df['region'].unique()))
# # # # # # #     filtered = sorted_df[sorted_df['region'].isin(region_filter)]
# # # # # # #     table = filtered[['county','region','population_2024','budget_billion','budget_per_person']].copy()
# # # # # # #     table.columns = ['County','Region','Population (2024)','Budget (KES B)','Budget/Person (KES)']
# # # # # # #     table = table.reset_index(drop=True); table.index += 1
# # # # # # #     st.dataframe(table, use_container_width=True, height=600)
# # # # # # #     csv = table.to_csv().encode('utf-8')
# # # # # # #     st.download_button("⬇ Download as CSV", csv, "kenya_county_budget.csv", "text/csv")

# # # # # # import streamlit as st
# # # # # # import pandas as pd
# # # # # # import numpy as np
# # # # # # import matplotlib.pyplot as plt
# # # # # # import matplotlib.ticker as mticker
# # # # # # import matplotlib.patches as mpatches
# # # # # # import plotly.express as px
# # # # # # import json
# # # # # # import urllib.request
# # # # # # from scipy import stats

# # # # # # st.set_page_config(page_title="Kenya County Budget Analysis", page_icon="🇰🇪", layout="wide")

# # # # # # st.markdown("""
# # # # # # <style>
# # # # # #     @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500&display=swap');
# # # # # #     html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
# # # # # #     .stApp { background-color: #0a0f1e; color: #e8eaf0; }
# # # # # #     h1, h2, h3 { font-family: 'Syne', sans-serif !important; }
# # # # # #     .hero-title { font-family: 'Syne', sans-serif; font-size: 3rem; font-weight: 800; color: #ffffff; line-height: 1.1; margin-bottom: 0.3rem; }
# # # # # #     .hero-sub { font-size: 1rem; color: #7a8aaa; margin-bottom: 2rem; font-weight: 300; letter-spacing: 0.05em; }
# # # # # #     .metric-card { background: linear-gradient(135deg, #111827 0%, #1a2340 100%); border: 1px solid #1e2d4a; border-radius: 12px; padding: 1.4rem 1.6rem; margin-bottom: 1rem; }
# # # # # #     .metric-label { font-size: 0.72rem; font-weight: 500; color: #5a6a8a; text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 0.4rem; }
# # # # # #     .metric-value { font-family: 'Syne', sans-serif; font-size: 1.9rem; font-weight: 700; color: #ffffff; line-height: 1; }
# # # # # #     .metric-accent { color: #3b82f6; } .metric-accent-green { color: #10b981; } .metric-accent-red { color: #ef4444; } .metric-accent-amber { color: #f59e0b; }
# # # # # #     .section-header { font-family: 'Syne', sans-serif; font-size: 1.1rem; font-weight: 700; color: #ffffff; text-transform: uppercase; letter-spacing: 0.08em; border-left: 3px solid #3b82f6; padding-left: 0.8rem; margin-bottom: 1rem; margin-top: 2rem; }
# # # # # #     .badge { display: inline-block; background: #1e3a5f; color: #60a5fa; font-size: 0.7rem; font-weight: 600; padding: 2px 10px; border-radius: 20px; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 0.5rem; }
# # # # # #     .insight-box { background: linear-gradient(135deg, #0f1f3d 0%, #1a2340 100%); border: 1px solid #1e3a5f; border-left: 3px solid #f59e0b; border-radius: 8px; padding: 1rem 1.2rem; margin: 0.5rem 0; font-size: 0.9rem; color: #c8d4e8; line-height: 1.6; }
# # # # # #     footer {visibility: hidden;} #MainMenu {visibility: hidden;} header {visibility: hidden;}
# # # # # # </style>
# # # # # # """, unsafe_allow_html=True)

# # # # # # DARK_BG = '#0a0f1e'; CARD_BG = '#111827'; BLUE = '#3b82f6'; GREEN = '#10b981'
# # # # # # RED = '#ef4444'; AMBER = '#f59e0b'; TEXT = '#e8eaf0'; MUTED = '#7a8aaa'
# # # # # # REGION_COLORS = {
# # # # # #     'Nairobi': '#3b82f6', 'Central': '#10b981', 'Coast': '#f59e0b',
# # # # # #     'Eastern': '#8b5cf6', 'North Eastern': '#ef4444', 'Nyanza': '#06b6d4',
# # # # # #     'Rift Valley': '#f97316', 'Western': '#ec4899',
# # # # # # }

# # # # # # NAME_MAP = {
# # # # # #     'Tana River':     'Tana River',
# # # # # #     'Taita Taveta':   'Taita-Taveta',
# # # # # #     'Elgeyo Marakwet':'Elgeyo/Marakwet',
# # # # # #     "Murang'a":       'Muranga',
# # # # # #     'Trans Nzoia':    'Trans-Nzoia',
# # # # # #     'Homa Bay':       'Homa Bay',
# # # # # #     'Tharaka Nithi':  'Tharaka-Nithi',
# # # # # #     'West Pokot':     'West Pokot',
# # # # # #     'Uasin Gishu':    'Uasin Gishu',
# # # # # # }

# # # # # # def style_chart(fig, axes):
# # # # # #     fig.patch.set_facecolor(DARK_BG)
# # # # # #     if not hasattr(axes, '__iter__'): axes = [axes]
# # # # # #     for ax in axes:
# # # # # #         ax.set_facecolor(CARD_BG); ax.tick_params(colors=MUTED, labelsize=8)
# # # # # #         ax.xaxis.label.set_color(MUTED); ax.yaxis.label.set_color(MUTED); ax.title.set_color(TEXT)
# # # # # #         for spine in ax.spines.values(): spine.set_edgecolor('#1e2d4a')

# # # # # # def gini_coefficient(values):
# # # # # #     arr = np.sort(np.array(values, dtype=float)); n = len(arr); cumsum = np.cumsum(arr)
# # # # # #     return (2 * np.sum(np.arange(1, n+1) * arr) - (n+1) * cumsum[-1]) / (n * cumsum[-1])

# # # # # # @st.cache_data
# # # # # # def load_data():
# # # # # #     df = pd.read_csv('data/county_data.csv')
# # # # # #     df['budget_per_person'] = (df['budget_billion'] * 1_000_000_000) / df['population_2024']
# # # # # #     df['budget_per_person'] = df['budget_per_person'].round(0).astype(int)
# # # # # #     return df

# # # # # # @st.cache_data
# # # # # # def load_geojson():
# # # # # #     url = "https://raw.githubusercontent.com/mikelmaron/kenya-election-data/master/data/counties.geojson"
# # # # # #     with urllib.request.urlopen(url) as response:
# # # # # #         geojson = json.loads(response.read().decode())
# # # # # #     for feature in geojson['features']:
# # # # # #         name = feature['properties'].get('COUNTY_NAM', '')
# # # # # #         if name:
# # # # # #             feature['properties']['COUNTY_NAM'] = name.strip().title()
# # # # # #     return geojson

# # # # # # df = load_data()
# # # # # # sorted_df = df.sort_values('budget_per_person', ascending=False).reset_index(drop=True)
# # # # # # regional = df.groupby('region').agg(counties=('county','count'), total_pop=('population_2024','sum'), total_budget=('budget_billion','sum')).reset_index()
# # # # # # regional['budget_per_person'] = ((regional['total_budget'] * 1e9) / regional['total_pop']).astype(int)
# # # # # # regional = regional.sort_values('budget_per_person', ascending=False)
# # # # # # gini = gini_coefficient(df['budget_per_person'])
# # # # # # corr_bpp, pval_bpp = stats.pearsonr(df['population_2024'], df['budget_per_person'])
# # # # # # corr_bp, _ = stats.pearsonr(df['population_2024'], df['budget_billion'])

# # # # # # with st.sidebar:
# # # # # #     st.markdown('<div style="font-family:Syne,sans-serif;font-size:1.1rem;font-weight:800;color:#fff;margin-bottom:1rem;">🇰🇪 Navigation</div>', unsafe_allow_html=True)
# # # # # #     section = st.radio("Go to", ["📊 Overview","🗺️ Choropleth Map","📍 Regional Analysis","🔗 Correlation & Gini","🎯 Quintile Analysis","🔍 County Explorer","📋 Full Rankings"])
# # # # # #     st.markdown("---")
# # # # # #     st.markdown(f'<div style="color:{MUTED};font-size:0.75rem;">Data: KNBS 2024 Projections<br>Budget: FY 2023/24 Equitable Share<br>Counties: 47</div>', unsafe_allow_html=True)

# # # # # # st.markdown('<div class="badge">FY 2023/24 · All 47 Counties</div>', unsafe_allow_html=True)
# # # # # # st.markdown('<div class="hero-title">🇰🇪 Kenya County<br>Budget Analysis</div>', unsafe_allow_html=True)
# # # # # # st.markdown('<div class="hero-sub">Equitable Share Allocations · KNBS 2024 Population Projections</div>', unsafe_allow_html=True)

# # # # # # c1,c2,c3,c4,c5 = st.columns(5)
# # # # # # with c1: st.markdown(f'<div class="metric-card"><div class="metric-label">Total Population</div><div class="metric-value metric-accent">{df["population_2024"].sum()/1e6:.1f}M</div></div>', unsafe_allow_html=True)
# # # # # # with c2: st.markdown(f'<div class="metric-card"><div class="metric-label">Total Budget</div><div class="metric-value">KES {df["budget_billion"].sum():.1f}B</div></div>', unsafe_allow_html=True)
# # # # # # with c3: st.markdown(f'<div class="metric-card"><div class="metric-label">National Avg / Person</div><div class="metric-value metric-accent-green">KES {int(df["budget_per_person"].mean()):,}</div></div>', unsafe_allow_html=True)
# # # # # # with c4:
# # # # # #     gap = sorted_df.iloc[0]['budget_per_person'] - sorted_df.iloc[-1]['budget_per_person']
# # # # # #     st.markdown(f'<div class="metric-card"><div class="metric-label">Highest vs Lowest Gap</div><div class="metric-value metric-accent-red">KES {gap:,}</div></div>', unsafe_allow_html=True)
# # # # # # with c5: st.markdown(f'<div class="metric-card"><div class="metric-label">Gini Coefficient</div><div class="metric-value metric-accent-amber">{gini:.3f}</div></div>', unsafe_allow_html=True)

# # # # # # # ── OVERVIEW ─────────────────────────────────────────────────────────────────
# # # # # # if "Overview" in section:
# # # # # #     st.markdown('<div class="section-header">Budget Per Citizen — All 47 Counties</div>', unsafe_allow_html=True)
# # # # # #     fig1, ax1 = plt.subplots(figsize=(18, 5)); style_chart(fig1, ax1)
# # # # # #     median = sorted_df['budget_per_person'].median()
# # # # # #     colors = [RED if v > median * 1.5 else BLUE for v in sorted_df['budget_per_person']]
# # # # # #     ax1.bar(sorted_df['county'], sorted_df['budget_per_person'], color=colors, edgecolor=DARK_BG, linewidth=0.4, width=0.75)
# # # # # #     ax1.axhline(df['budget_per_person'].mean(), color=AMBER, linestyle='--', linewidth=1.5, label=f"National Average: KES {int(df['budget_per_person'].mean()):,}")
# # # # # #     ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
# # # # # #     ax1.legend(facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=9)
# # # # # #     ax1.set_ylabel('KES per Person', fontsize=9)
# # # # # #     plt.xticks(rotation=90, fontsize=7.5, color=MUTED); plt.tight_layout(); st.pyplot(fig1); plt.close()

# # # # # #     col_l, col_r = st.columns(2)
# # # # # #     top10 = sorted_df.head(10); bot10 = sorted_df.tail(10).sort_values('budget_per_person')
# # # # # #     with col_l:
# # # # # #         st.markdown('<div class="section-header">Top 10 Counties</div>', unsafe_allow_html=True)
# # # # # #         fig2, ax2 = plt.subplots(figsize=(7, 5)); style_chart(fig2, ax2)
# # # # # #         ax2.barh(top10['county'], top10['budget_per_person'], color=GREEN, edgecolor=DARK_BG, linewidth=0.4)
# # # # # #         ax2.set_title('Highest Budget Per Person', fontsize=11, fontweight='bold')
# # # # # #         ax2.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
# # # # # #         ax2.set_xlabel('KES per Person'); ax2.invert_yaxis(); ax2.tick_params(axis='y', labelsize=9, colors=TEXT)
# # # # # #         plt.tight_layout(); st.pyplot(fig2); plt.close()
# # # # # #     with col_r:
# # # # # #         st.markdown('<div class="section-header">Bottom 10 Counties</div>', unsafe_allow_html=True)
# # # # # #         fig3, ax3 = plt.subplots(figsize=(7, 5)); style_chart(fig3, ax3)
# # # # # #         ax3.barh(bot10['county'], bot10['budget_per_person'], color=RED, edgecolor=DARK_BG, linewidth=0.4)
# # # # # #         ax3.set_title('Lowest Budget Per Person', fontsize=11, fontweight='bold')
# # # # # #         ax3.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
# # # # # #         ax3.set_xlabel('KES per Person'); ax3.invert_yaxis(); ax3.tick_params(axis='y', labelsize=9, colors=TEXT)
# # # # # #         plt.tight_layout(); st.pyplot(fig3); plt.close()

# # # # # # # ── CHOROPLETH MAP ────────────────────────────────────────────────────────────
# # # # # # elif "Choropleth" in section:
# # # # # #     st.markdown('<div class="section-header">Kenya County Budget Per Citizen — Map View</div>', unsafe_allow_html=True)
# # # # # #     try:
# # # # # #         kenya_geojson = load_geojson()
# # # # # #         df_map = df.copy()
# # # # # #         df_map['county_mapped'] = df_map['county'].apply(lambda x: NAME_MAP.get(x, x))
# # # # # #         fig_map = px.choropleth(
# # # # # #             df_map,
# # # # # #             geojson=kenya_geojson,
# # # # # #             locations='county_mapped',
# # # # # #             featureidkey='properties.COUNTY_NAM',
# # # # # #             color='budget_per_person',
# # # # # #             color_continuous_scale='RdYlGn',
# # # # # #             hover_name='county',
# # # # # #             hover_data={
# # # # # #                 'county_mapped': False,
# # # # # #                 'budget_per_person': ':,',
# # # # # #                 'budget_billion': True,
# # # # # #                 'population_2024': ':,'
# # # # # #             },
# # # # # #             labels={
# # # # # #                 'budget_per_person': 'KES/Person',
# # # # # #                 'budget_billion': 'Budget (KES B)',
# # # # # #                 'population_2024': 'Population'
# # # # # #             },
# # # # # #         )
# # # # # #         fig_map.update_geos(fitbounds="locations", visible=False)
# # # # # #         fig_map.update_layout(
# # # # # #             paper_bgcolor='#0a0f1e', plot_bgcolor='#0a0f1e', font_color='#e8eaf0',
# # # # # #             coloraxis_colorbar=dict(
# # # # # #                 title=dict(text='KES/Person', font=dict(color='#e8eaf0')),
# # # # # #                 tickfont=dict(color='#e8eaf0'),
# # # # # #             ),
# # # # # #             margin=dict(l=0, r=0, t=20, b=0), height=600
# # # # # #         )
# # # # # #         st.plotly_chart(fig_map, use_container_width=True)
# # # # # #         st.markdown('<div class="insight-box">🟢 <strong>Green</strong> = higher budget per person &nbsp;·&nbsp; 🔴 <strong>Red</strong> = lower budget per person<br>Hover over any county to see its exact budget, population and KES per person.</div>', unsafe_allow_html=True)
# # # # # #     except Exception as e:
# # # # # #         st.error(f"Could not load map: {e}")

# # # # # # # ── REGIONAL ─────────────────────────────────────────────────────────────────
# # # # # # elif "Regional" in section:
# # # # # #     st.markdown('<div class="section-header">Regional Budget Per Person</div>', unsafe_allow_html=True)
# # # # # #     colors_r = [REGION_COLORS[r] for r in regional['region']]
# # # # # #     fig_r1, axes_r1 = plt.subplots(1, 2, figsize=(16, 5)); style_chart(fig_r1, axes_r1)
# # # # # #     axes_r1[0].barh(regional['region'], regional['budget_per_person'], color=colors_r, edgecolor=DARK_BG, linewidth=0.4)
# # # # # #     axes_r1[0].axvline(df['budget_per_person'].mean(), color=AMBER, linestyle='--', linewidth=1.2, label='National Avg')
# # # # # #     axes_r1[0].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
# # # # # #     axes_r1[0].set_title('Average Budget Per Person by Region', fontsize=11, fontweight='bold')
# # # # # #     axes_r1[0].set_xlabel('KES per Person'); axes_r1[0].invert_yaxis()
# # # # # #     axes_r1[0].tick_params(axis='y', labelsize=9, colors=TEXT)
# # # # # #     axes_r1[0].legend(facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=8)
# # # # # #     wedges, texts, autotexts = axes_r1[1].pie(regional['total_budget'], labels=regional['region'], autopct='%1.1f%%', colors=colors_r, startangle=90, pctdistance=0.75, textprops={'color': TEXT, 'fontsize': 8})
# # # # # #     for at in autotexts: at.set_color(DARK_BG); at.set_fontsize(7)
# # # # # #     axes_r1[1].set_title('Share of Total Budget by Region', fontsize=11, fontweight='bold')
# # # # # #     plt.tight_layout(); st.pyplot(fig_r1); plt.close()

# # # # # #     st.markdown('<div class="section-header">Within-Region Budget Spread</div>', unsafe_allow_html=True)
# # # # # #     reg_min = df.groupby('region')['budget_per_person'].min().reset_index().rename(columns={'budget_per_person':'min_bpp'})
# # # # # #     reg_max = df.groupby('region')['budget_per_person'].max().reset_index().rename(columns={'budget_per_person':'max_bpp'})
# # # # # #     regional_ext = regional.merge(reg_min, on='region').merge(reg_max, on='region')
# # # # # #     fig_r2, ax_r2 = plt.subplots(figsize=(14, 5)); style_chart(fig_r2, ax_r2)
# # # # # #     ax_r2.barh(regional_ext['region'], regional_ext['max_bpp'] - regional_ext['min_bpp'], left=regional_ext['min_bpp'], color=colors_r, alpha=0.5, edgecolor=DARK_BG, linewidth=0.4, height=0.5)
# # # # # #     ax_r2.scatter(regional_ext['budget_per_person'], regional_ext['region'], color=TEXT, s=50, zorder=5, label='Regional Avg/Person')
# # # # # #     ax_r2.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
# # # # # #     ax_r2.set_title('Budget/Person Range Within Each Region (min → max)', fontsize=11, fontweight='bold')
# # # # # #     ax_r2.set_xlabel('KES per Person'); ax_r2.invert_yaxis(); ax_r2.tick_params(axis='y', labelsize=9, colors=TEXT)
# # # # # #     ax_r2.legend(facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=8)
# # # # # #     plt.tight_layout(); st.pyplot(fig_r2); plt.close()

# # # # # #     st.markdown('<div class="section-header">Regional Summary Table</div>', unsafe_allow_html=True)
# # # # # #     reg_table = regional[['region','counties','total_pop','total_budget','budget_per_person']].copy()
# # # # # #     reg_table.columns = ['Region','Counties','Population','Budget (KES B)','Avg Budget/Person (KES)']
# # # # # #     reg_table = reg_table.reset_index(drop=True); reg_table.index += 1
# # # # # #     st.dataframe(reg_table, use_container_width=True)

# # # # # # # ── CORRELATION & GINI ────────────────────────────────────────────────────────
# # # # # # elif "Correlation" in section:
# # # # # #     st.markdown('<div class="section-header">Gini Coefficient & Distribution</div>', unsafe_allow_html=True)
# # # # # #     col_g1, col_g2 = st.columns([1, 2])
# # # # # #     with col_g1:
# # # # # #         st.markdown(f"""
# # # # # #         <div class="metric-card" style="margin-top:1rem;">
# # # # # #             <div class="metric-label">Gini Coefficient</div>
# # # # # #             <div class="metric-value metric-accent-amber">{gini:.4f}</div>
# # # # # #         </div>
# # # # # #         <div class="insight-box">
# # # # # #             A Gini of <strong>{gini:.3f}</strong> indicates <strong>{'high' if gini > 0.35 else 'moderate' if gini > 0.25 else 'low'} inequality</strong> in per-capita budget allocation.<br><br>
# # # # # #             The top county (<strong>{sorted_df.iloc[0]['county']}</strong>) receives <strong>{sorted_df.iloc[0]['budget_per_person'] / sorted_df.iloc[-1]['budget_per_person']:.1f}x</strong> more per person than the bottom (<strong>{sorted_df.iloc[-1]['county']}</strong>).
# # # # # #         </div>""", unsafe_allow_html=True)
# # # # # #     with col_g2:
# # # # # #         fig_g, axes_g = plt.subplots(1, 2, figsize=(12, 4)); style_chart(fig_g, axes_g)
# # # # # #         sorted_vals = np.sort(df['budget_per_person'].values); n = len(sorted_vals)
# # # # # #         lorenz_x = np.concatenate([[0], np.arange(1, n+1) / n])
# # # # # #         lorenz_y = np.concatenate([[0], np.cumsum(sorted_vals) / sorted_vals.sum()])
# # # # # #         axes_g[0].plot(lorenz_x, lorenz_y, color=BLUE, linewidth=2.5, label=f'Lorenz Curve (Gini={gini:.3f})')
# # # # # #         axes_g[0].plot([0,1],[0,1], color=MUTED, linestyle='--', linewidth=1.2, label='Perfect Equality')
# # # # # #         axes_g[0].fill_between(lorenz_x, lorenz_y, lorenz_x, alpha=0.15, color=RED)
# # # # # #         axes_g[0].set_title('Lorenz Curve', fontsize=11, fontweight='bold')
# # # # # #         axes_g[0].set_xlabel('Cumulative Share of Counties'); axes_g[0].set_ylabel('Cumulative Budget Share')
# # # # # #         axes_g[0].legend(facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=8)
# # # # # #         axes_g[1].hist(df['budget_per_person'], bins=12, color=BLUE, edgecolor=DARK_BG, linewidth=0.5, alpha=0.85)
# # # # # #         axes_g[1].axvline(df['budget_per_person'].mean(), color=AMBER, linestyle='--', linewidth=1.5, label=f"Mean: KES {int(df['budget_per_person'].mean()):,}")
# # # # # #         axes_g[1].axvline(df['budget_per_person'].median(), color=GREEN, linestyle='--', linewidth=1.5, label=f"Median: KES {int(df['budget_per_person'].median()):,}")
# # # # # #         axes_g[1].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
# # # # # #         axes_g[1].set_title('Budget/Person Distribution', fontsize=11, fontweight='bold')
# # # # # #         axes_g[1].set_xlabel('KES per Person'); axes_g[1].set_ylabel('Number of Counties')
# # # # # #         axes_g[1].legend(facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=8)
# # # # # #         plt.tight_layout(); st.pyplot(fig_g); plt.close()

# # # # # #     st.markdown('<div class="section-header">Correlation Analysis</div>', unsafe_allow_html=True)
# # # # # #     col_c1, col_c2 = st.columns(2)
# # # # # #     with col_c1: st.markdown(f'<div class="metric-card"><div class="metric-label">Population vs Absolute Budget</div><div class="metric-value metric-accent-green">r = {corr_bp:.3f}</div></div>', unsafe_allow_html=True)
# # # # # #     with col_c2: st.markdown(f'<div class="metric-card"><div class="metric-label">Population vs Budget Per Person</div><div class="metric-value metric-accent-red">r = {corr_bpp:.3f}</div></div>', unsafe_allow_html=True)

# # # # # #     colors_scatter = [REGION_COLORS[r] for r in df['region']]
# # # # # #     fig_c, axes_c = plt.subplots(1, 2, figsize=(16, 5)); style_chart(fig_c, axes_c)
# # # # # #     axes_c[0].scatter(df['population_2024']/1e6, df['budget_billion'], c=colors_scatter, s=70, alpha=0.85, edgecolors='#1e2d4a', linewidth=0.6)
# # # # # #     m, b, *_ = stats.linregress(df['population_2024']/1e6, df['budget_billion'])
# # # # # #     x_line = np.linspace(df['population_2024'].min()/1e6, df['population_2024'].max()/1e6, 100)
# # # # # #     axes_c[0].plot(x_line, m*x_line+b, color=AMBER, linewidth=1.8, linestyle='--')
# # # # # #     for _, row in df.iterrows():
# # # # # #         if row['county'] in ['Nairobi','Lamu','Nakuru','Kiambu','Turkana']:
# # # # # #             axes_c[0].annotate(row['county'], (row['population_2024']/1e6, row['budget_billion']), textcoords='offset points', xytext=(6,4), fontsize=7.5, color=TEXT)
# # # # # #     legend_patches = [mpatches.Patch(color=v, label=k) for k, v in REGION_COLORS.items()]
# # # # # #     axes_c[0].legend(handles=legend_patches, facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=7, ncol=2, loc='upper left')
# # # # # #     axes_c[0].set_title('Population vs Absolute Budget', fontsize=11, fontweight='bold')
# # # # # #     axes_c[0].set_xlabel('Population (millions)'); axes_c[0].set_ylabel('Budget (KES Billions)')
# # # # # #     axes_c[1].scatter(df['population_2024']/1e6, df['budget_per_person'], c=colors_scatter, s=70, alpha=0.85, edgecolors='#1e2d4a', linewidth=0.6)
# # # # # #     m2, b2, *_ = stats.linregress(df['population_2024']/1e6, df['budget_per_person'])
# # # # # #     axes_c[1].plot(x_line, m2*x_line+b2, color=AMBER, linewidth=1.8, linestyle='--', label=f'r = {corr_bpp:.3f}')
# # # # # #     for _, row in df.iterrows():
# # # # # #         if row['county'] in ['Nairobi','Lamu','Nakuru','Kiambu','Marsabit']:
# # # # # #             axes_c[1].annotate(row['county'], (row['population_2024']/1e6, row['budget_per_person']), textcoords='offset points', xytext=(6,4), fontsize=7.5, color=TEXT)
# # # # # #     axes_c[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
# # # # # #     axes_c[1].set_title('Population vs Budget Per Person', fontsize=11, fontweight='bold')
# # # # # #     axes_c[1].set_xlabel('Population (millions)'); axes_c[1].set_ylabel('Budget Per Person (KES)')
# # # # # #     axes_c[1].legend(facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=9)
# # # # # #     plt.tight_layout(); st.pyplot(fig_c); plt.close()
# # # # # #     st.markdown(f'<div class="insight-box">📌 <strong>Key finding:</strong> Larger counties receive significantly <em>less</em> per person (r = {corr_bpp:.3f}, p &lt; 0.001). The equitable share formula disproportionately benefits low-population counties like Lamu, Marsabit and Samburu, while high-density counties like Nairobi, Kiambu and Nakuru receive the least per citizen.</div>', unsafe_allow_html=True)

# # # # # # # ── QUINTILE ──────────────────────────────────────────────────────────────────
# # # # # # elif "Quintile" in section:
# # # # # #     st.markdown('<div class="section-header">Quintile Analysis</div>', unsafe_allow_html=True)
# # # # # #     df_q = df.copy()
# # # # # #     df_q['quintile'] = pd.qcut(df_q['budget_per_person'], q=5, labels=['Q1 Bottom 20%','Q2','Q3 Middle','Q4','Q5 Top 20%'])
# # # # # #     quintile_summary = df_q.groupby('quintile', observed=True).agg(counties=('county','count'), avg_bpp=('budget_per_person','mean'), counties_list=('county', lambda x: ', '.join(sorted(x)))).reset_index()
# # # # # #     quintile_colors = [RED, '#f97316', AMBER, '#84cc16', GREEN]
# # # # # #     fig_q, axes_q = plt.subplots(1, 2, figsize=(16, 5)); style_chart(fig_q, axes_q)
# # # # # #     axes_q[0].bar(quintile_summary['quintile'], quintile_summary['avg_bpp'], color=quintile_colors, edgecolor=DARK_BG, linewidth=0.4)
# # # # # #     axes_q[0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
# # # # # #     axes_q[0].set_title('Average Budget Per Person by Quintile', fontsize=11, fontweight='bold')
# # # # # #     axes_q[0].set_ylabel('KES per Person'); axes_q[0].tick_params(axis='x', labelsize=8, colors=TEXT)
# # # # # #     region_order = regional['region'].tolist()
# # # # # #     region_data = [df[df['region'] == r]['budget_per_person'].values for r in region_order]
# # # # # #     bp = axes_q[1].boxplot(region_data, tick_labels=region_order, patch_artist=True, vert=True)
# # # # # #     for patch, region in zip(bp['boxes'], region_order):
# # # # # #         patch.set_facecolor(REGION_COLORS[region]); patch.set_alpha(0.7)
# # # # # #     for element in ['whiskers','caps','medians','fliers']:
# # # # # #         for item in bp[element]: item.set_color(TEXT)
# # # # # #     axes_q[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
# # # # # #     axes_q[1].set_title('Budget/Person Distribution by Region', fontsize=11, fontweight='bold')
# # # # # #     axes_q[1].set_ylabel('KES per Person'); axes_q[1].tick_params(axis='x', rotation=30, labelsize=8, colors=TEXT)
# # # # # #     plt.tight_layout(); st.pyplot(fig_q); plt.close()

# # # # # #     st.markdown('<div class="section-header">Counties by Quintile</div>', unsafe_allow_html=True)
# # # # # #     for i, (_, row) in enumerate(quintile_summary.iterrows()):
# # # # # #         color = quintile_colors[i]
# # # # # #         st.markdown(f'<div class="insight-box" style="border-left-color:{color}"><strong style="color:{color}">{row["quintile"]}</strong> &nbsp;·&nbsp; Avg: KES {int(row["avg_bpp"]):,}/person &nbsp;·&nbsp; {int(row["counties"])} counties<br><span style="color:#7a8aaa">{row["counties_list"]}</span></div>', unsafe_allow_html=True)

# # # # # # # ── COUNTY EXPLORER ───────────────────────────────────────────────────────────
# # # # # # elif "Explorer" in section:
# # # # # #     st.markdown('<div class="section-header">County Explorer</div>', unsafe_allow_html=True)
# # # # # #     col_s, col_info = st.columns([1, 2])
# # # # # #     with col_s:
# # # # # #         selected = st.selectbox('Select a County', options=sorted(df['county'].tolist()))
# # # # # #     with col_info:
# # # # # #         row = df[df['county'] == selected].iloc[0]
# # # # # #         rank = sorted_df[sorted_df['county'] == selected].index[0] + 1
# # # # # #         nat_avg = int(df['budget_per_person'].mean())
# # # # # #         diff = int(row['budget_per_person']) - nat_avg
# # # # # #         diff_str = f"+KES {diff:,}" if diff > 0 else f"-KES {abs(diff):,}"
# # # # # #         diff_color = "metric-accent-green" if diff > 0 else "metric-accent-red"
# # # # # #         reg_avg = int(regional[regional['region'] == row['region']]['budget_per_person'].values[0])
# # # # # #         ca, cb2, cc, cd = st.columns(4)
# # # # # #         with ca: st.markdown(f'<div class="metric-card"><div class="metric-label">Population</div><div class="metric-value" style="font-size:1.3rem">{int(row["population_2024"]):,}</div></div>', unsafe_allow_html=True)
# # # # # #         with cb2: st.markdown(f'<div class="metric-card"><div class="metric-label">Budget</div><div class="metric-value" style="font-size:1.3rem">KES {row["budget_billion"]}B</div></div>', unsafe_allow_html=True)
# # # # # #         with cc: st.markdown(f'<div class="metric-card"><div class="metric-label">Per Person · Rank #{rank}</div><div class="metric-value {diff_color}" style="font-size:1.3rem">KES {int(row["budget_per_person"]):,}</div></div>', unsafe_allow_html=True)
# # # # # #         with cd: st.markdown(f'<div class="metric-card"><div class="metric-label">Region ({row["region"]})</div><div class="metric-value" style="font-size:1.3rem">KES {reg_avg:,}</div></div>', unsafe_allow_html=True)
# # # # # #         st.markdown(f'<div class="insight-box"><strong>{selected}</strong> is ranked <strong>#{rank} of 47</strong> counties by budget per person. It is <strong>{diff_str}</strong> vs the national average of KES {nat_avg:,}/person, and sits in the <strong>{row["region"]}</strong> region (regional avg: KES {reg_avg:,}/person).</div>', unsafe_allow_html=True)

# # # # # # # ── FULL RANKINGS ─────────────────────────────────────────────────────────────
# # # # # # elif "Rankings" in section:
# # # # # #     st.markdown('<div class="section-header">Full County Rankings</div>', unsafe_allow_html=True)
# # # # # #     region_filter = st.multiselect('Filter by Region', options=sorted(df['region'].unique()), default=sorted(df['region'].unique()))
# # # # # #     filtered = sorted_df[sorted_df['region'].isin(region_filter)]
# # # # # #     table = filtered[['county','region','population_2024','budget_billion','budget_per_person']].copy()
# # # # # #     table.columns = ['County','Region','Population (2024)','Budget (KES B)','Budget/Person (KES)']
# # # # # #     table = table.reset_index(drop=True); table.index += 1
# # # # # #     st.dataframe(table, use_container_width=True, height=600)
# # # # # #     csv = table.to_csv().encode('utf-8')
# # # # # #     st.download_button("⬇ Download as CSV", csv, "kenya_county_budget.csv", "text/csv")

# # # # # import streamlit as st
# # # # # import pandas as pd
# # # # # import numpy as np
# # # # # import matplotlib.pyplot as plt
# # # # # import matplotlib.ticker as mticker
# # # # # import matplotlib.patches as mpatches
# # # # # import plotly.express as px
# # # # # import json
# # # # # import urllib.request
# # # # # from scipy import stats

# # # # # st.set_page_config(page_title="Kenya County Budget Analysis", page_icon="🇰🇪", layout="wide")

# # # # # st.markdown("""
# # # # # <style>
# # # # #     @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500&display=swap');
# # # # #     html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
# # # # #     .stApp { background-color: #0a0f1e; color: #e8eaf0; }
# # # # #     h1, h2, h3 { font-family: 'Syne', sans-serif !important; }
# # # # #     .hero-title { font-family: 'Syne', sans-serif; font-size: 3rem; font-weight: 800; color: #ffffff; line-height: 1.1; margin-bottom: 0.3rem; }
# # # # #     .hero-sub { font-size: 1rem; color: #7a8aaa; margin-bottom: 2rem; font-weight: 300; letter-spacing: 0.05em; }
# # # # #     .metric-card { background: linear-gradient(135deg, #111827 0%, #1a2340 100%); border: 1px solid #1e2d4a; border-radius: 12px; padding: 1.4rem 1.6rem; margin-bottom: 1rem; }
# # # # #     .metric-label { font-size: 0.72rem; font-weight: 500; color: #5a6a8a; text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 0.4rem; }
# # # # #     .metric-value { font-family: 'Syne', sans-serif; font-size: 1.9rem; font-weight: 700; color: #ffffff; line-height: 1; }
# # # # #     .metric-accent { color: #3b82f6; } .metric-accent-green { color: #10b981; } .metric-accent-red { color: #ef4444; } .metric-accent-amber { color: #f59e0b; }
# # # # #     .section-header { font-family: 'Syne', sans-serif; font-size: 1.1rem; font-weight: 700; color: #ffffff; text-transform: uppercase; letter-spacing: 0.08em; border-left: 3px solid #3b82f6; padding-left: 0.8rem; margin-bottom: 1rem; margin-top: 2rem; }
# # # # #     .badge { display: inline-block; background: #1e3a5f; color: #60a5fa; font-size: 0.7rem; font-weight: 600; padding: 2px 10px; border-radius: 20px; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 0.5rem; }
# # # # #     .insight-box { background: linear-gradient(135deg, #0f1f3d 0%, #1a2340 100%); border: 1px solid #1e3a5f; border-left: 3px solid #f59e0b; border-radius: 8px; padding: 1rem 1.2rem; margin: 0.5rem 0; font-size: 0.9rem; color: #c8d4e8; line-height: 1.6; }
# # # # #     footer {visibility: hidden;} #MainMenu {visibility: hidden;} header {visibility: hidden;}
# # # # # </style>
# # # # # """, unsafe_allow_html=True)

# # # # # DARK_BG = '#0a0f1e'; CARD_BG = '#111827'; BLUE = '#3b82f6'; GREEN = '#10b981'
# # # # # RED = '#ef4444'; AMBER = '#f59e0b'; TEXT = '#e8eaf0'; MUTED = '#7a8aaa'
# # # # # REGION_COLORS = {
# # # # #     'Nairobi': '#3b82f6', 'Central': '#10b981', 'Coast': '#f59e0b',
# # # # #     'Eastern': '#8b5cf6', 'North Eastern': '#ef4444', 'Nyanza': '#06b6d4',
# # # # #     'Rift Valley': '#f97316', 'Western': '#ec4899',
# # # # # }

# # # # # NAME_MAP = {
# # # # #     'Tana River':     'Tana River',
# # # # #     'Taita Taveta':   'Taita-Taveta',
# # # # #     'Elgeyo Marakwet':'Elgeyo/Marakwet',
# # # # #     "Murang'a":       'Muranga',
# # # # #     'Trans Nzoia':    'Trans-Nzoia',
# # # # #     'Homa Bay':       'Homa Bay',
# # # # #     'Tharaka Nithi':  'Tharaka-Nithi',
# # # # #     'West Pokot':     'West Pokot',
# # # # #     'Uasin Gishu':    'Uasin Gishu',
# # # # # }

# # # # # def style_chart(fig, axes):
# # # # #     fig.patch.set_facecolor(DARK_BG)
# # # # #     if not hasattr(axes, '__iter__'): axes = [axes]
# # # # #     for ax in axes:
# # # # #         ax.set_facecolor(CARD_BG); ax.tick_params(colors=MUTED, labelsize=8)
# # # # #         ax.xaxis.label.set_color(MUTED); ax.yaxis.label.set_color(MUTED); ax.title.set_color(TEXT)
# # # # #         for spine in ax.spines.values(): spine.set_edgecolor('#1e2d4a')

# # # # # def gini_coefficient(values):
# # # # #     arr = np.sort(np.array(values, dtype=float)); n = len(arr); cumsum = np.cumsum(arr)
# # # # #     return (2 * np.sum(np.arange(1, n+1) * arr) - (n+1) * cumsum[-1]) / (n * cumsum[-1])

# # # # # @st.cache_data
# # # # # def load_data():
# # # # #     df = pd.read_csv('data/county_data.csv')
# # # # #     df['budget_per_person'] = (df['budget_billion'] * 1_000_000_000) / df['population_2024']
# # # # #     df['budget_per_person'] = df['budget_per_person'].round(0).astype(int)
# # # # #     return df

# # # # # @st.cache_data
# # # # # def load_geojson():
# # # # #     url = "https://raw.githubusercontent.com/mikelmaron/kenya-election-data/master/data/counties.geojson"
# # # # #     with urllib.request.urlopen(url) as response:
# # # # #         geojson = json.loads(response.read().decode())
# # # # #     for feature in geojson['features']:
# # # # #         name = feature['properties'].get('COUNTY_NAM', '')
# # # # #         if name:
# # # # #             feature['properties']['COUNTY_NAM'] = name.strip().title()
# # # # #     return geojson

# # # # # df = load_data()
# # # # # sorted_df = df.sort_values('budget_per_person', ascending=False).reset_index(drop=True)
# # # # # regional = df.groupby('region').agg(counties=('county','count'), total_pop=('population_2024','sum'), total_budget=('budget_billion','sum')).reset_index()
# # # # # regional['budget_per_person'] = ((regional['total_budget'] * 1e9) / regional['total_pop']).astype(int)
# # # # # regional = regional.sort_values('budget_per_person', ascending=False)
# # # # # gini = gini_coefficient(df['budget_per_person'])
# # # # # corr_bpp, pval_bpp = stats.pearsonr(df['population_2024'], df['budget_per_person'])
# # # # # corr_bp, _ = stats.pearsonr(df['population_2024'], df['budget_billion'])

# # # # # top_county = sorted_df.iloc[0]; bot_county = sorted_df.iloc[-1]

# # # # # SECTIONS = ["🏠 Home", "📊 Overview", "🗺️ Choropleth Map", "📍 Regional Analysis",
# # # # #             "🔗 Correlation & Gini", "🎯 Quintile Analysis", "🔍 County Explorer", "📋 Full Rankings"]

# # # # # with st.sidebar:
# # # # #     st.markdown('<div style="font-family:Syne,sans-serif;font-size:1.1rem;font-weight:800;color:#fff;margin-bottom:1rem;">🇰🇪 Navigation</div>', unsafe_allow_html=True)
# # # # #     section = st.radio("Go to", SECTIONS)
# # # # #     st.markdown("---")
# # # # #     st.markdown(f'<div style="color:{MUTED};font-size:0.75rem;">Data: KNBS 2024 Projections<br>Budget: FY 2023/24 Equitable Share<br>Counties: 47</div>', unsafe_allow_html=True)

# # # # # # ── HOME PAGE ─────────────────────────────────────────────────────────────────
# # # # # if "Home" in section:
# # # # #     st.markdown('<div class="badge">FY 2023/24 · All 47 Counties</div>', unsafe_allow_html=True)
# # # # #     st.markdown('<div class="hero-title">🇰🇪 Kenya County<br>Budget Analysis</div>', unsafe_allow_html=True)
# # # # #     st.markdown('<div class="hero-sub">Equitable Share Allocations · KNBS 2024 Population Projections</div>', unsafe_allow_html=True)

# # # # #     # ── 2-column metric grid ──
# # # # #     st.markdown('<div class="section-header">Key Metrics</div>', unsafe_allow_html=True)
# # # # #     m1, m2 = st.columns(2)
# # # # #     m3, m4 = st.columns(2)
# # # # #     with m1:
# # # # #         st.markdown(f"""
# # # # #         <div class="metric-card">
# # # # #             <div class="metric-label">📊 National Avg Budget / Person</div>
# # # # #             <div class="metric-value metric-accent-green">KES {int(df["budget_per_person"].mean()):,}</div>
# # # # #             <div style="color:{MUTED};font-size:0.78rem;margin-top:0.5rem;">Total budget: KES {df["budget_billion"].sum():.1f}B &nbsp;·&nbsp; Population: {df["population_2024"].sum()/1e6:.1f}M</div>
# # # # #         </div>""", unsafe_allow_html=True)
# # # # #     with m2:
# # # # #         st.markdown(f"""
# # # # #         <div class="metric-card">
# # # # #             <div class="metric-label">🏆 Highest Funded County</div>
# # # # #             <div class="metric-value metric-accent-green" style="font-size:1.6rem;">{top_county["county"]}</div>
# # # # #             <div style="color:#10b981;font-size:0.9rem;margin-top:0.5rem;font-weight:600;">KES {int(top_county["budget_per_person"]):,} per person &nbsp;·&nbsp; {top_county["region"]} Region</div>
# # # # #         </div>""", unsafe_allow_html=True)
# # # # #     with m3:
# # # # #         st.markdown(f"""
# # # # #         <div class="metric-card">
# # # # #             <div class="metric-label">📉 Lowest Funded County</div>
# # # # #             <div class="metric-value metric-accent-red" style="font-size:1.6rem;">{bot_county["county"]}</div>
# # # # #             <div style="color:#ef4444;font-size:0.9rem;margin-top:0.5rem;font-weight:600;">KES {int(bot_county["budget_per_person"]):,} per person &nbsp;·&nbsp; {bot_county["region"]} Region</div>
# # # # #         </div>""", unsafe_allow_html=True)
# # # # #     with m4:
# # # # #         inequality_level = "Low" if gini < 0.2 else "Moderate" if gini < 0.35 else "High"
# # # # #         gap_x = int(top_county["budget_per_person"] / bot_county["budget_per_person"])
# # # # #         st.markdown(f"""
# # # # #         <div class="metric-card">
# # # # #             <div class="metric-label">⚖️ Funding Inequality (Gini)</div>
# # # # #             <div class="metric-value metric-accent-amber">{gini:.3f}</div>
# # # # #             <div style="color:{MUTED};font-size:0.78rem;margin-top:0.5rem;">{inequality_level} inequality &nbsp;·&nbsp; Highest county gets <strong style="color:#f59e0b;">{gap_x}x</strong> more per person than lowest</div>
# # # # #         </div>""", unsafe_allow_html=True)

# # # # #     # ── Navigation buttons ──
# # # # #     st.markdown('<div class="section-header">Explore the Dashboard</div>', unsafe_allow_html=True)
# # # # #     NAV_ITEMS = [
# # # # #         ("📊", "Overview",          "Bar charts of all 47 counties ranked by budget per person",      "Overview"),
# # # # #         ("🗺️", "Choropleth Map",    "Interactive Kenya map colored by budget per citizen",            "Choropleth Map"),
# # # # #         ("📍", "Regional Analysis", "Compare 8 regions — budgets, pie charts & spread",              "Regional Analysis"),
# # # # #         ("🔗", "Correlation & Gini","Lorenz curve, Gini deep-dive & population scatter plots",       "Correlation & Gini"),
# # # # #         ("🎯", "Quintile Analysis", "Counties grouped into 5 funding bands with regional boxplots",  "Quintile Analysis"),
# # # # #         ("🔍", "County Explorer",   "Pick any county and see its rank, region & budget vs average",  "County Explorer"),
# # # # #         ("📋", "Full Rankings",     "Filterable table of all 47 counties with CSV download",         "Full Rankings"),
# # # # #     ]
# # # # #     row1 = st.columns(3)
# # # # #     row2 = st.columns(3)
# # # # #     row3 = st.columns(1)
# # # # #     rows = [row1[0], row1[1], row1[2], row2[0], row2[1], row2[2], row3[0]]
# # # # #     for col, (icon, title, desc, key) in zip(rows, NAV_ITEMS):
# # # # #         with col:
# # # # #             st.markdown(f"""
# # # # #             <div style="background:linear-gradient(135deg,#111827,#1a2340);border:1px solid #1e2d4a;
# # # # #                         border-radius:12px;padding:1.2rem 1.3rem;margin-bottom:0.8rem;
# # # # #                         transition:border-color 0.2s;">
# # # # #                 <div style="font-size:1.6rem;margin-bottom:0.4rem;">{icon}</div>
# # # # #                 <div style="font-family:Syne,sans-serif;font-size:0.95rem;font-weight:700;
# # # # #                             color:#fff;margin-bottom:0.3rem;">{title}</div>
# # # # #                 <div style="font-size:0.78rem;color:{MUTED};line-height:1.4;">{desc}</div>
# # # # #             </div>""", unsafe_allow_html=True)
# # # # #             if st.button(f"Open {title}", key=f"nav_{key}", use_container_width=True):
# # # # #                 st.session_state["nav_target"] = f"{'📊' if title=='Overview' else '🗺️' if title=='Choropleth Map' else '📍' if title=='Regional Analysis' else '🔗' if title=='Correlation & Gini' else '🎯' if title=='Quintile Analysis' else '🔍' if title=='County Explorer' else '📋'} {title}"
# # # # #                 st.rerun()

# # # # #     st.markdown(f"""
# # # # #     <div class="insight-box" style="margin-top:1rem;">
# # # # #         💡 <strong>Key finding:</strong> {top_county["county"]} receives <strong>KES {int(top_county["budget_per_person"]):,}/person</strong>
# # # # #         — {gap_x}x more than {bot_county["county"]} which gets <strong>KES {int(bot_county["budget_per_person"]):,}/person</strong>.
# # # # #         The Gini coefficient of <strong>{gini:.3f}</strong> reflects {inequality_level.lower()} inequality across all counties.
# # # # #     </div>""", unsafe_allow_html=True)

# # # # # # Handle nav button clicks
# # # # # if "nav_target" in st.session_state:
# # # # #     section = st.session_state.pop("nav_target")

# # # # # # ── OVERVIEW ─────────────────────────────────────────────────────────────────
# # # # # if "Overview" in section:
# # # # #     st.markdown('<div class="section-header">Budget Per Citizen — All 47 Counties</div>', unsafe_allow_html=True)
# # # # #     fig1, ax1 = plt.subplots(figsize=(18, 5)); style_chart(fig1, ax1)
# # # # #     median = sorted_df['budget_per_person'].median()
# # # # #     colors = [RED if v > median * 1.5 else BLUE for v in sorted_df['budget_per_person']]
# # # # #     ax1.bar(sorted_df['county'], sorted_df['budget_per_person'], color=colors, edgecolor=DARK_BG, linewidth=0.4, width=0.75)
# # # # #     ax1.axhline(df['budget_per_person'].mean(), color=AMBER, linestyle='--', linewidth=1.5, label=f"National Average: KES {int(df['budget_per_person'].mean()):,}")
# # # # #     ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
# # # # #     ax1.legend(facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=9)
# # # # #     ax1.set_ylabel('KES per Person', fontsize=9)
# # # # #     plt.xticks(rotation=90, fontsize=7.5, color=MUTED); plt.tight_layout(); st.pyplot(fig1); plt.close()

# # # # #     col_l, col_r = st.columns(2)
# # # # #     top10 = sorted_df.head(10); bot10 = sorted_df.tail(10).sort_values('budget_per_person')
# # # # #     with col_l:
# # # # #         st.markdown('<div class="section-header">Top 10 Counties</div>', unsafe_allow_html=True)
# # # # #         fig2, ax2 = plt.subplots(figsize=(7, 5)); style_chart(fig2, ax2)
# # # # #         ax2.barh(top10['county'], top10['budget_per_person'], color=GREEN, edgecolor=DARK_BG, linewidth=0.4)
# # # # #         ax2.set_title('Highest Budget Per Person', fontsize=11, fontweight='bold')
# # # # #         ax2.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
# # # # #         ax2.set_xlabel('KES per Person'); ax2.invert_yaxis(); ax2.tick_params(axis='y', labelsize=9, colors=TEXT)
# # # # #         plt.tight_layout(); st.pyplot(fig2); plt.close()
# # # # #     with col_r:
# # # # #         st.markdown('<div class="section-header">Bottom 10 Counties</div>', unsafe_allow_html=True)
# # # # #         fig3, ax3 = plt.subplots(figsize=(7, 5)); style_chart(fig3, ax3)
# # # # #         ax3.barh(bot10['county'], bot10['budget_per_person'], color=RED, edgecolor=DARK_BG, linewidth=0.4)
# # # # #         ax3.set_title('Lowest Budget Per Person', fontsize=11, fontweight='bold')
# # # # #         ax3.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
# # # # #         ax3.set_xlabel('KES per Person'); ax3.invert_yaxis(); ax3.tick_params(axis='y', labelsize=9, colors=TEXT)
# # # # #         plt.tight_layout(); st.pyplot(fig3); plt.close()

# # # # # # ── CHOROPLETH MAP ────────────────────────────────────────────────────────────
# # # # # elif "Choropleth" in section:
# # # # #     st.markdown('<div class="section-header">Kenya County Budget Per Citizen — Map View</div>', unsafe_allow_html=True)
# # # # #     try:
# # # # #         kenya_geojson = load_geojson()
# # # # #         df_map = df.copy()
# # # # #         df_map['county_mapped'] = df_map['county'].apply(lambda x: NAME_MAP.get(x, x))
# # # # #         fig_map = px.choropleth(
# # # # #             df_map,
# # # # #             geojson=kenya_geojson,
# # # # #             locations='county_mapped',
# # # # #             featureidkey='properties.COUNTY_NAM',
# # # # #             color='budget_per_person',
# # # # #             color_continuous_scale='RdYlGn',
# # # # #             hover_name='county',
# # # # #             hover_data={
# # # # #                 'county_mapped': False,
# # # # #                 'budget_per_person': ':,',
# # # # #                 'budget_billion': True,
# # # # #                 'population_2024': ':,'
# # # # #             },
# # # # #             labels={
# # # # #                 'budget_per_person': 'KES/Person',
# # # # #                 'budget_billion': 'Budget (KES B)',
# # # # #                 'population_2024': 'Population'
# # # # #             },
# # # # #         )
# # # # #         fig_map.update_geos(fitbounds="locations", visible=False)
# # # # #         fig_map.update_layout(
# # # # #             paper_bgcolor='#0a0f1e', plot_bgcolor='#0a0f1e', font_color='#e8eaf0',
# # # # #             coloraxis_colorbar=dict(
# # # # #                 title=dict(text='KES/Person', font=dict(color='#e8eaf0')),
# # # # #                 tickfont=dict(color='#e8eaf0'),
# # # # #                 bgcolor='#111827',
# # # # #                 outlinecolor='#1e2d4a',
# # # # #             ),
# # # # #             margin=dict(l=0, r=0, t=20, b=0), height=600
# # # # #         )
# # # # #         st.plotly_chart(fig_map, use_container_width=True)
# # # # #         st.markdown('<div class="insight-box">🟢 <strong>Green</strong> = higher budget per person &nbsp;·&nbsp; 🔴 <strong>Red</strong> = lower budget per person<br>Hover over any county to see its exact budget, population and KES per person.</div>', unsafe_allow_html=True)
# # # # #     except Exception as e:
# # # # #         st.error(f"Could not load map: {e}")

# # # # # # ── REGIONAL ─────────────────────────────────────────────────────────────────
# # # # # elif "Regional" in section:
# # # # #     st.markdown('<div class="section-header">Regional Budget Per Person</div>', unsafe_allow_html=True)
# # # # #     colors_r = [REGION_COLORS[r] for r in regional['region']]
# # # # #     fig_r1, axes_r1 = plt.subplots(1, 2, figsize=(16, 5)); style_chart(fig_r1, axes_r1)
# # # # #     axes_r1[0].barh(regional['region'], regional['budget_per_person'], color=colors_r, edgecolor=DARK_BG, linewidth=0.4)
# # # # #     axes_r1[0].axvline(df['budget_per_person'].mean(), color=AMBER, linestyle='--', linewidth=1.2, label='National Avg')
# # # # #     axes_r1[0].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
# # # # #     axes_r1[0].set_title('Average Budget Per Person by Region', fontsize=11, fontweight='bold')
# # # # #     axes_r1[0].set_xlabel('KES per Person'); axes_r1[0].invert_yaxis()
# # # # #     axes_r1[0].tick_params(axis='y', labelsize=9, colors=TEXT)
# # # # #     axes_r1[0].legend(facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=8)
# # # # #     wedges, texts, autotexts = axes_r1[1].pie(regional['total_budget'], labels=regional['region'], autopct='%1.1f%%', colors=colors_r, startangle=90, pctdistance=0.75, textprops={'color': TEXT, 'fontsize': 8})
# # # # #     for at in autotexts: at.set_color(DARK_BG); at.set_fontsize(7)
# # # # #     axes_r1[1].set_title('Share of Total Budget by Region', fontsize=11, fontweight='bold')
# # # # #     plt.tight_layout(); st.pyplot(fig_r1); plt.close()

# # # # #     st.markdown('<div class="section-header">Within-Region Budget Spread</div>', unsafe_allow_html=True)
# # # # #     reg_min = df.groupby('region')['budget_per_person'].min().reset_index().rename(columns={'budget_per_person':'min_bpp'})
# # # # #     reg_max = df.groupby('region')['budget_per_person'].max().reset_index().rename(columns={'budget_per_person':'max_bpp'})
# # # # #     regional_ext = regional.merge(reg_min, on='region').merge(reg_max, on='region')
# # # # #     fig_r2, ax_r2 = plt.subplots(figsize=(14, 5)); style_chart(fig_r2, ax_r2)
# # # # #     ax_r2.barh(regional_ext['region'], regional_ext['max_bpp'] - regional_ext['min_bpp'], left=regional_ext['min_bpp'], color=colors_r, alpha=0.5, edgecolor=DARK_BG, linewidth=0.4, height=0.5)
# # # # #     ax_r2.scatter(regional_ext['budget_per_person'], regional_ext['region'], color=TEXT, s=50, zorder=5, label='Regional Avg/Person')
# # # # #     ax_r2.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
# # # # #     ax_r2.set_title('Budget/Person Range Within Each Region (min → max)', fontsize=11, fontweight='bold')
# # # # #     ax_r2.set_xlabel('KES per Person'); ax_r2.invert_yaxis(); ax_r2.tick_params(axis='y', labelsize=9, colors=TEXT)
# # # # #     ax_r2.legend(facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=8)
# # # # #     plt.tight_layout(); st.pyplot(fig_r2); plt.close()

# # # # #     st.markdown('<div class="section-header">Regional Summary Table</div>', unsafe_allow_html=True)
# # # # #     reg_table = regional[['region','counties','total_pop','total_budget','budget_per_person']].copy()
# # # # #     reg_table.columns = ['Region','Counties','Population','Budget (KES B)','Avg Budget/Person (KES)']
# # # # #     reg_table = reg_table.reset_index(drop=True); reg_table.index += 1
# # # # #     st.dataframe(reg_table, use_container_width=True)

# # # # # # ── CORRELATION & GINI ────────────────────────────────────────────────────────
# # # # # elif "Correlation" in section:
# # # # #     st.markdown('<div class="section-header">Gini Coefficient & Distribution</div>', unsafe_allow_html=True)
# # # # #     col_g1, col_g2 = st.columns([1, 2])
# # # # #     with col_g1:
# # # # #         st.markdown(f"""
# # # # #         <div class="metric-card" style="margin-top:1rem;">
# # # # #             <div class="metric-label">Gini Coefficient</div>
# # # # #             <div class="metric-value metric-accent-amber">{gini:.4f}</div>
# # # # #         </div>
# # # # #         <div class="insight-box">
# # # # #             A Gini of <strong>{gini:.3f}</strong> indicates <strong>{'high' if gini > 0.35 else 'moderate' if gini > 0.25 else 'low'} inequality</strong> in per-capita budget allocation.<br><br>
# # # # #             The top county (<strong>{sorted_df.iloc[0]['county']}</strong>) receives <strong>{sorted_df.iloc[0]['budget_per_person'] / sorted_df.iloc[-1]['budget_per_person']:.1f}x</strong> more per person than the bottom (<strong>{sorted_df.iloc[-1]['county']}</strong>).
# # # # #         </div>""", unsafe_allow_html=True)
# # # # #     with col_g2:
# # # # #         fig_g, axes_g = plt.subplots(1, 2, figsize=(12, 4)); style_chart(fig_g, axes_g)
# # # # #         sorted_vals = np.sort(df['budget_per_person'].values); n = len(sorted_vals)
# # # # #         lorenz_x = np.concatenate([[0], np.arange(1, n+1) / n])
# # # # #         lorenz_y = np.concatenate([[0], np.cumsum(sorted_vals) / sorted_vals.sum()])
# # # # #         axes_g[0].plot(lorenz_x, lorenz_y, color=BLUE, linewidth=2.5, label=f'Lorenz Curve (Gini={gini:.3f})')
# # # # #         axes_g[0].plot([0,1],[0,1], color=MUTED, linestyle='--', linewidth=1.2, label='Perfect Equality')
# # # # #         axes_g[0].fill_between(lorenz_x, lorenz_y, lorenz_x, alpha=0.15, color=RED)
# # # # #         axes_g[0].set_title('Lorenz Curve', fontsize=11, fontweight='bold')
# # # # #         axes_g[0].set_xlabel('Cumulative Share of Counties'); axes_g[0].set_ylabel('Cumulative Budget Share')
# # # # #         axes_g[0].legend(facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=8)
# # # # #         axes_g[1].hist(df['budget_per_person'], bins=12, color=BLUE, edgecolor=DARK_BG, linewidth=0.5, alpha=0.85)
# # # # #         axes_g[1].axvline(df['budget_per_person'].mean(), color=AMBER, linestyle='--', linewidth=1.5, label=f"Mean: KES {int(df['budget_per_person'].mean()):,}")
# # # # #         axes_g[1].axvline(df['budget_per_person'].median(), color=GREEN, linestyle='--', linewidth=1.5, label=f"Median: KES {int(df['budget_per_person'].median()):,}")
# # # # #         axes_g[1].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
# # # # #         axes_g[1].set_title('Budget/Person Distribution', fontsize=11, fontweight='bold')
# # # # #         axes_g[1].set_xlabel('KES per Person'); axes_g[1].set_ylabel('Number of Counties')
# # # # #         axes_g[1].legend(facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=8)
# # # # #         plt.tight_layout(); st.pyplot(fig_g); plt.close()

# # # # #     st.markdown('<div class="section-header">Correlation Analysis</div>', unsafe_allow_html=True)
# # # # #     col_c1, col_c2 = st.columns(2)
# # # # #     with col_c1: st.markdown(f'<div class="metric-card"><div class="metric-label">Population vs Absolute Budget</div><div class="metric-value metric-accent-green">r = {corr_bp:.3f}</div></div>', unsafe_allow_html=True)
# # # # #     with col_c2: st.markdown(f'<div class="metric-card"><div class="metric-label">Population vs Budget Per Person</div><div class="metric-value metric-accent-red">r = {corr_bpp:.3f}</div></div>', unsafe_allow_html=True)

# # # # #     colors_scatter = [REGION_COLORS[r] for r in df['region']]
# # # # #     fig_c, axes_c = plt.subplots(1, 2, figsize=(16, 5)); style_chart(fig_c, axes_c)
# # # # #     axes_c[0].scatter(df['population_2024']/1e6, df['budget_billion'], c=colors_scatter, s=70, alpha=0.85, edgecolors='#1e2d4a', linewidth=0.6)
# # # # #     m, b, *_ = stats.linregress(df['population_2024']/1e6, df['budget_billion'])
# # # # #     x_line = np.linspace(df['population_2024'].min()/1e6, df['population_2024'].max()/1e6, 100)
# # # # #     axes_c[0].plot(x_line, m*x_line+b, color=AMBER, linewidth=1.8, linestyle='--')
# # # # #     for _, row in df.iterrows():
# # # # #         if row['county'] in ['Nairobi','Lamu','Nakuru','Kiambu','Turkana']:
# # # # #             axes_c[0].annotate(row['county'], (row['population_2024']/1e6, row['budget_billion']), textcoords='offset points', xytext=(6,4), fontsize=7.5, color=TEXT)
# # # # #     legend_patches = [mpatches.Patch(color=v, label=k) for k, v in REGION_COLORS.items()]
# # # # #     axes_c[0].legend(handles=legend_patches, facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=7, ncol=2, loc='upper left')
# # # # #     axes_c[0].set_title('Population vs Absolute Budget', fontsize=11, fontweight='bold')
# # # # #     axes_c[0].set_xlabel('Population (millions)'); axes_c[0].set_ylabel('Budget (KES Billions)')
# # # # #     axes_c[1].scatter(df['population_2024']/1e6, df['budget_per_person'], c=colors_scatter, s=70, alpha=0.85, edgecolors='#1e2d4a', linewidth=0.6)
# # # # #     m2, b2, *_ = stats.linregress(df['population_2024']/1e6, df['budget_per_person'])
# # # # #     axes_c[1].plot(x_line, m2*x_line+b2, color=AMBER, linewidth=1.8, linestyle='--', label=f'r = {corr_bpp:.3f}')
# # # # #     for _, row in df.iterrows():
# # # # #         if row['county'] in ['Nairobi','Lamu','Nakuru','Kiambu','Marsabit']:
# # # # #             axes_c[1].annotate(row['county'], (row['population_2024']/1e6, row['budget_per_person']), textcoords='offset points', xytext=(6,4), fontsize=7.5, color=TEXT)
# # # # #     axes_c[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
# # # # #     axes_c[1].set_title('Population vs Budget Per Person', fontsize=11, fontweight='bold')
# # # # #     axes_c[1].set_xlabel('Population (millions)'); axes_c[1].set_ylabel('Budget Per Person (KES)')
# # # # #     axes_c[1].legend(facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=9)
# # # # #     plt.tight_layout(); st.pyplot(fig_c); plt.close()
# # # # #     st.markdown(f'<div class="insight-box">📌 <strong>Key finding:</strong> Larger counties receive significantly <em>less</em> per person (r = {corr_bpp:.3f}, p &lt; 0.001). The equitable share formula disproportionately benefits low-population counties like Lamu, Marsabit and Samburu, while high-density counties like Nairobi, Kiambu and Nakuru receive the least per citizen.</div>', unsafe_allow_html=True)

# # # # # # ── QUINTILE ──────────────────────────────────────────────────────────────────
# # # # # elif "Quintile" in section:
# # # # #     st.markdown('<div class="section-header">Quintile Analysis</div>', unsafe_allow_html=True)
# # # # #     df_q = df.copy()
# # # # #     df_q['quintile'] = pd.qcut(df_q['budget_per_person'], q=5, labels=['Q1 Bottom 20%','Q2','Q3 Middle','Q4','Q5 Top 20%'])
# # # # #     quintile_summary = df_q.groupby('quintile', observed=True).agg(counties=('county','count'), avg_bpp=('budget_per_person','mean'), counties_list=('county', lambda x: ', '.join(sorted(x)))).reset_index()
# # # # #     quintile_colors = [RED, '#f97316', AMBER, '#84cc16', GREEN]
# # # # #     fig_q, axes_q = plt.subplots(1, 2, figsize=(16, 5)); style_chart(fig_q, axes_q)
# # # # #     axes_q[0].bar(quintile_summary['quintile'], quintile_summary['avg_bpp'], color=quintile_colors, edgecolor=DARK_BG, linewidth=0.4)
# # # # #     axes_q[0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
# # # # #     axes_q[0].set_title('Average Budget Per Person by Quintile', fontsize=11, fontweight='bold')
# # # # #     axes_q[0].set_ylabel('KES per Person'); axes_q[0].tick_params(axis='x', labelsize=8, colors=TEXT)
# # # # #     region_order = regional['region'].tolist()
# # # # #     region_data = [df[df['region'] == r]['budget_per_person'].values for r in region_order]
# # # # #     bp = axes_q[1].boxplot(region_data, tick_labels=region_order, patch_artist=True, vert=True)
# # # # #     for patch, region in zip(bp['boxes'], region_order):
# # # # #         patch.set_facecolor(REGION_COLORS[region]); patch.set_alpha(0.7)
# # # # #     for element in ['whiskers','caps','medians','fliers']:
# # # # #         for item in bp[element]: item.set_color(TEXT)
# # # # #     axes_q[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
# # # # #     axes_q[1].set_title('Budget/Person Distribution by Region', fontsize=11, fontweight='bold')
# # # # #     axes_q[1].set_ylabel('KES per Person'); axes_q[1].tick_params(axis='x', rotation=30, labelsize=8, colors=TEXT)
# # # # #     plt.tight_layout(); st.pyplot(fig_q); plt.close()

# # # # #     st.markdown('<div class="section-header">Counties by Quintile</div>', unsafe_allow_html=True)
# # # # #     for i, (_, row) in enumerate(quintile_summary.iterrows()):
# # # # #         color = quintile_colors[i]
# # # # #         st.markdown(f'<div class="insight-box" style="border-left-color:{color}"><strong style="color:{color}">{row["quintile"]}</strong> &nbsp;·&nbsp; Avg: KES {int(row["avg_bpp"]):,}/person &nbsp;·&nbsp; {int(row["counties"])} counties<br><span style="color:#7a8aaa">{row["counties_list"]}</span></div>', unsafe_allow_html=True)

# # # # # # ── COUNTY EXPLORER ───────────────────────────────────────────────────────────
# # # # # elif "Explorer" in section:
# # # # #     st.markdown('<div class="section-header">County Explorer</div>', unsafe_allow_html=True)
# # # # #     col_s, col_info = st.columns([1, 2])
# # # # #     with col_s:
# # # # #         selected = st.selectbox('Select a County', options=sorted(df['county'].tolist()))
# # # # #     with col_info:
# # # # #         row = df[df['county'] == selected].iloc[0]
# # # # #         rank = sorted_df[sorted_df['county'] == selected].index[0] + 1
# # # # #         nat_avg = int(df['budget_per_person'].mean())
# # # # #         diff = int(row['budget_per_person']) - nat_avg
# # # # #         diff_str = f"+KES {diff:,}" if diff > 0 else f"-KES {abs(diff):,}"
# # # # #         diff_color = "metric-accent-green" if diff > 0 else "metric-accent-red"
# # # # #         reg_avg = int(regional[regional['region'] == row['region']]['budget_per_person'].values[0])
# # # # #         ca, cb2, cc, cd = st.columns(4)
# # # # #         with ca: st.markdown(f'<div class="metric-card"><div class="metric-label">Population</div><div class="metric-value" style="font-size:1.3rem">{int(row["population_2024"]):,}</div></div>', unsafe_allow_html=True)
# # # # #         with cb2: st.markdown(f'<div class="metric-card"><div class="metric-label">Budget</div><div class="metric-value" style="font-size:1.3rem">KES {row["budget_billion"]}B</div></div>', unsafe_allow_html=True)
# # # # #         with cc: st.markdown(f'<div class="metric-card"><div class="metric-label">Per Person · Rank #{rank}</div><div class="metric-value {diff_color}" style="font-size:1.3rem">KES {int(row["budget_per_person"]):,}</div></div>', unsafe_allow_html=True)
# # # # #         with cd: st.markdown(f'<div class="metric-card"><div class="metric-label">Region ({row["region"]})</div><div class="metric-value" style="font-size:1.3rem">KES {reg_avg:,}</div></div>', unsafe_allow_html=True)
# # # # #         st.markdown(f'<div class="insight-box"><strong>{selected}</strong> is ranked <strong>#{rank} of 47</strong> counties by budget per person. It is <strong>{diff_str}</strong> vs the national average of KES {nat_avg:,}/person, and sits in the <strong>{row["region"]}</strong> region (regional avg: KES {reg_avg:,}/person).</div>', unsafe_allow_html=True)

# # # # # # ── FULL RANKINGS ─────────────────────────────────────────────────────────────
# # # # # elif "Rankings" in section:
# # # # #     st.markdown('<div class="section-header">Full County Rankings</div>', unsafe_allow_html=True)
# # # # #     region_filter = st.multiselect('Filter by Region', options=sorted(df['region'].unique()), default=sorted(df['region'].unique()))
# # # # #     filtered = sorted_df[sorted_df['region'].isin(region_filter)]
# # # # #     table = filtered[['county','region','population_2024','budget_billion','budget_per_person']].copy()
# # # # #     table.columns = ['County','Region','Population (2024)','Budget (KES B)','Budget/Person (KES)']
# # # # #     table = table.reset_index(drop=True); table.index += 1
# # # # #     st.dataframe(table, use_container_width=True, height=600)
# # # # #     csv = table.to_csv().encode('utf-8')
# # # # #     st.download_button("⬇ Download as CSV", csv, "kenya_county_budget.csv", "text/csv")

# # # # import streamlit as st
# # # # import pandas as pd
# # # # import numpy as np
# # # # import matplotlib.pyplot as plt
# # # # import matplotlib.ticker as mticker
# # # # import matplotlib.patches as mpatches
# # # # import plotly.express as px
# # # # import json
# # # # import urllib.request
# # # # from scipy import stats

# # # # st.set_page_config(page_title="Kenya County Budget Analysis", page_icon="🇰🇪", layout="wide")

# # # # st.markdown("""
# # # # <style>
# # # #     @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500&display=swap');
# # # #     html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
# # # #     .stApp { background-color: #0a0f1e; color: #e8eaf0; }
# # # #     h1, h2, h3 { font-family: 'Syne', sans-serif !important; }
# # # #     .hero-title { font-family: 'Syne', sans-serif; font-size: 3rem; font-weight: 800; color: #ffffff; line-height: 1.1; margin-bottom: 0.3rem; }
# # # #     .hero-sub { font-size: 1rem; color: #7a8aaa; margin-bottom: 2rem; font-weight: 300; letter-spacing: 0.05em; }
# # # #     .metric-card { background: linear-gradient(135deg, #111827 0%, #1a2340 100%); border: 1px solid #1e2d4a; border-radius: 12px; padding: 1.4rem 1.6rem; margin-bottom: 1rem; }
# # # #     .metric-label { font-size: 0.72rem; font-weight: 500; color: #5a6a8a; text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 0.4rem; }
# # # #     .metric-value { font-family: 'Syne', sans-serif; font-size: 1.9rem; font-weight: 700; color: #ffffff; line-height: 1; }
# # # #     .metric-accent { color: #3b82f6; } .metric-accent-green { color: #10b981; } .metric-accent-red { color: #ef4444; } .metric-accent-amber { color: #f59e0b; }
# # # #     .section-header { font-family: 'Syne', sans-serif; font-size: 1.1rem; font-weight: 700; color: #ffffff; text-transform: uppercase; letter-spacing: 0.08em; border-left: 3px solid #3b82f6; padding-left: 0.8rem; margin-bottom: 1rem; margin-top: 2rem; }
# # # #     .badge { display: inline-block; background: #1e3a5f; color: #60a5fa; font-size: 0.7rem; font-weight: 600; padding: 2px 10px; border-radius: 20px; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 0.5rem; }
# # # #     .insight-box { background: linear-gradient(135deg, #0f1f3d 0%, #1a2340 100%); border: 1px solid #1e3a5f; border-left: 3px solid #f59e0b; border-radius: 8px; padding: 1rem 1.2rem; margin: 0.5rem 0; font-size: 0.9rem; color: #c8d4e8; line-height: 1.6; }
# # # #     footer {visibility: hidden;} #MainMenu {visibility: hidden;} header {visibility: hidden;}
# # # # </style>
# # # # """, unsafe_allow_html=True)

# # # # DARK_BG = '#0a0f1e'; CARD_BG = '#111827'; BLUE = '#3b82f6'; GREEN = '#10b981'
# # # # RED = '#ef4444'; AMBER = '#f59e0b'; TEXT = '#e8eaf0'; MUTED = '#7a8aaa'
# # # # REGION_COLORS = {
# # # #     'Nairobi': '#3b82f6', 'Central': '#10b981', 'Coast': '#f59e0b',
# # # #     'Eastern': '#8b5cf6', 'North Eastern': '#ef4444', 'Nyanza': '#06b6d4',
# # # #     'Rift Valley': '#f97316', 'Western': '#ec4899',
# # # # }

# # # # NAME_MAP = {
# # # #     'Tana River':     'Tana River',
# # # #     'Taita Taveta':   'Taita-Taveta',
# # # #     'Elgeyo Marakwet':'Elgeyo/Marakwet',
# # # #     "Murang'a":       'Muranga',
# # # #     'Trans Nzoia':    'Trans-Nzoia',
# # # #     'Homa Bay':       'Homa Bay',
# # # #     'Tharaka Nithi':  'Tharaka-Nithi',
# # # #     'West Pokot':     'West Pokot',
# # # #     'Uasin Gishu':    'Uasin Gishu',
# # # # }

# # # # def style_chart(fig, axes):
# # # #     fig.patch.set_facecolor(DARK_BG)
# # # #     if not hasattr(axes, '__iter__'): axes = [axes]
# # # #     for ax in axes:
# # # #         ax.set_facecolor(CARD_BG); ax.tick_params(colors=MUTED, labelsize=8)
# # # #         ax.xaxis.label.set_color(MUTED); ax.yaxis.label.set_color(MUTED); ax.title.set_color(TEXT)
# # # #         for spine in ax.spines.values(): spine.set_edgecolor('#1e2d4a')

# # # # def gini_coefficient(values):
# # # #     arr = np.sort(np.array(values, dtype=float)); n = len(arr); cumsum = np.cumsum(arr)
# # # #     return (2 * np.sum(np.arange(1, n+1) * arr) - (n+1) * cumsum[-1]) / (n * cumsum[-1])

# # # # @st.cache_data
# # # # def load_data():
# # # #     df = pd.read_csv('data/county_data.csv')
# # # #     df['budget_per_person'] = (df['budget_billion'] * 1_000_000_000) / df['population_2024']
# # # #     df['budget_per_person'] = df['budget_per_person'].round(0).astype(int)
# # # #     return df

# # # # @st.cache_data
# # # # def load_geojson():
# # # #     url = "https://raw.githubusercontent.com/mikelmaron/kenya-election-data/master/data/counties.geojson"
# # # #     with urllib.request.urlopen(url) as response:
# # # #         geojson = json.loads(response.read().decode())
# # # #     for feature in geojson['features']:
# # # #         name = feature['properties'].get('COUNTY_NAM', '')
# # # #         if name:
# # # #             feature['properties']['COUNTY_NAM'] = name.strip().title()
# # # #     return geojson

# # # # df = load_data()
# # # # sorted_df = df.sort_values('budget_per_person', ascending=False).reset_index(drop=True)
# # # # regional = df.groupby('region').agg(counties=('county','count'), total_pop=('population_2024','sum'), total_budget=('budget_billion','sum')).reset_index()
# # # # regional['budget_per_person'] = ((regional['total_budget'] * 1e9) / regional['total_pop']).astype(int)
# # # # regional = regional.sort_values('budget_per_person', ascending=False)
# # # # gini = gini_coefficient(df['budget_per_person'])
# # # # corr_bpp, pval_bpp = stats.pearsonr(df['population_2024'], df['budget_per_person'])
# # # # corr_bp, _ = stats.pearsonr(df['population_2024'], df['budget_billion'])

# # # # top_county = sorted_df.iloc[0]; bot_county = sorted_df.iloc[-1]

# # # # SECTIONS = ["🏠 Home", "📊 Overview", "🗺️ Choropleth Map", "📍 Regional Analysis",
# # # #             "🔗 Correlation & Gini", "🎯 Quintile Analysis", "🔍 County Explorer", "📋 Full Rankings"]

# # # # # Resolve nav button clicks BEFORE sidebar renders
# # # # if "nav_target" in st.session_state:
# # # #     default_idx = SECTIONS.index(st.session_state["nav_target"]) if st.session_state["nav_target"] in SECTIONS else 0
# # # #     del st.session_state["nav_target"]
# # # # else:
# # # #     default_idx = 0

# # # # with st.sidebar:
# # # #     st.markdown('<div style="font-family:Syne,sans-serif;font-size:1.1rem;font-weight:800;color:#fff;margin-bottom:1rem;">🇰🇪 Navigation</div>', unsafe_allow_html=True)
# # # #     section = st.radio("Go to", SECTIONS, index=default_idx)
# # # #     st.markdown("---")
# # # #     st.markdown(f'<div style="color:{MUTED};font-size:0.75rem;">Data: KNBS 2024 Projections<br>Budget: FY 2023/24 Equitable Share<br>Counties: 47</div>', unsafe_allow_html=True)

# # # # # ── HOME PAGE ─────────────────────────────────────────────────────────────────
# # # # if "Home" in section:
# # # #     st.markdown('<div class="badge">FY 2023/24 · All 47 Counties</div>', unsafe_allow_html=True)
# # # #     st.markdown('<div class="hero-title">🇰🇪 Kenya County<br>Budget Analysis</div>', unsafe_allow_html=True)
# # # #     st.markdown('<div class="hero-sub">Equitable Share Allocations · KNBS 2024 Population Projections</div>', unsafe_allow_html=True)

# # # #     # ── 2-column metric grid ──
# # # #     st.markdown('<div class="section-header">Key Metrics</div>', unsafe_allow_html=True)
# # # #     m1, m2 = st.columns(2)
# # # #     m3, m4 = st.columns(2)
# # # #     with m1:
# # # #         st.markdown(f"""
# # # #         <div class="metric-card">
# # # #             <div class="metric-label">📊 National Avg Budget / Person</div>
# # # #             <div class="metric-value metric-accent-green">KES {int(df["budget_per_person"].mean()):,}</div>
# # # #             <div style="color:{MUTED};font-size:0.78rem;margin-top:0.5rem;">Total budget: KES {df["budget_billion"].sum():.1f}B &nbsp;·&nbsp; Population: {df["population_2024"].sum()/1e6:.1f}M</div>
# # # #         </div>""", unsafe_allow_html=True)
# # # #     with m2:
# # # #         st.markdown(f"""
# # # #         <div class="metric-card">
# # # #             <div class="metric-label">🏆 Highest Funded County</div>
# # # #             <div class="metric-value metric-accent-green" style="font-size:1.6rem;">{top_county["county"]}</div>
# # # #             <div style="color:#10b981;font-size:0.9rem;margin-top:0.5rem;font-weight:600;">KES {int(top_county["budget_per_person"]):,} per person &nbsp;·&nbsp; {top_county["region"]} Region</div>
# # # #         </div>""", unsafe_allow_html=True)
# # # #     with m3:
# # # #         st.markdown(f"""
# # # #         <div class="metric-card">
# # # #             <div class="metric-label">📉 Lowest Funded County</div>
# # # #             <div class="metric-value metric-accent-red" style="font-size:1.6rem;">{bot_county["county"]}</div>
# # # #             <div style="color:#ef4444;font-size:0.9rem;margin-top:0.5rem;font-weight:600;">KES {int(bot_county["budget_per_person"]):,} per person &nbsp;·&nbsp; {bot_county["region"]} Region</div>
# # # #         </div>""", unsafe_allow_html=True)
# # # #     with m4:
# # # #         inequality_level = "Low" if gini < 0.2 else "Moderate" if gini < 0.35 else "High"
# # # #         gap_x = int(top_county["budget_per_person"] / bot_county["budget_per_person"])
# # # #         st.markdown(f"""
# # # #         <div class="metric-card">
# # # #             <div class="metric-label">⚖️ Funding Inequality (Gini)</div>
# # # #             <div class="metric-value metric-accent-amber">{gini:.3f}</div>
# # # #             <div style="color:{MUTED};font-size:0.78rem;margin-top:0.5rem;">{inequality_level} inequality &nbsp;·&nbsp; Highest county gets <strong style="color:#f59e0b;">{gap_x}x</strong> more per person than lowest</div>
# # # #         </div>""", unsafe_allow_html=True)

# # # #     # ── Navigation buttons ──
# # # #     st.markdown('<div class="section-header">Explore the Dashboard</div>', unsafe_allow_html=True)
# # # #     NAV_ITEMS = [
# # # #         ("📊", "Overview",          "Bar charts of all 47 counties ranked by budget per person",      "Overview"),
# # # #         ("🗺️", "Choropleth Map",    "Interactive Kenya map colored by budget per citizen",            "Choropleth Map"),
# # # #         ("📍", "Regional Analysis", "Compare 8 regions — budgets, pie charts & spread",              "Regional Analysis"),
# # # #         ("🔗", "Correlation & Gini","Lorenz curve, Gini deep-dive & population scatter plots",       "Correlation & Gini"),
# # # #         ("🎯", "Quintile Analysis", "Counties grouped into 5 funding bands with regional boxplots",  "Quintile Analysis"),
# # # #         ("🔍", "County Explorer",   "Pick any county and see its rank, region & budget vs average",  "County Explorer"),
# # # #         ("📋", "Full Rankings",     "Filterable table of all 47 counties with CSV download",         "Full Rankings"),
# # # #     ]
# # # #     row1 = st.columns(3)
# # # #     row2 = st.columns(3)
# # # #     row3 = st.columns(1)
# # # #     rows = [row1[0], row1[1], row1[2], row2[0], row2[1], row2[2], row3[0]]
# # # #     for col, (icon, title, desc, key) in zip(rows, NAV_ITEMS):
# # # #         with col:
# # # #             st.markdown(f"""
# # # #             <div style="background:linear-gradient(135deg,#111827,#1a2340);border:1px solid #1e2d4a;
# # # #                         border-radius:12px;padding:1.2rem 1.3rem;margin-bottom:0.8rem;
# # # #                         transition:border-color 0.2s;">
# # # #                 <div style="font-size:1.6rem;margin-bottom:0.4rem;">{icon}</div>
# # # #                 <div style="font-family:Syne,sans-serif;font-size:0.95rem;font-weight:700;
# # # #                             color:#fff;margin-bottom:0.3rem;">{title}</div>
# # # #                 <div style="font-size:0.78rem;color:{MUTED};line-height:1.4;">{desc}</div>
# # # #             </div>""", unsafe_allow_html=True)
# # # #             if st.button(f"Open {title}", key=f"nav_{key}", use_container_width=True):
# # # #                 icon_map = {"Overview":"📊","Choropleth Map":"🗺️","Regional Analysis":"📍",
# # # #                             "Correlation & Gini":"🔗","Quintile Analysis":"🎯",
# # # #                             "County Explorer":"🔍","Full Rankings":"📋"}
# # # #                 st.session_state["nav_target"] = f"{icon_map[title]} {title}"
# # # #                 st.rerun()

# # # #     st.markdown(f"""
# # # #     <div class="insight-box" style="margin-top:1rem;">
# # # #         💡 <strong>Key finding:</strong> {top_county["county"]} receives <strong>KES {int(top_county["budget_per_person"]):,}/person</strong>
# # # #         — {gap_x}x more than {bot_county["county"]} which gets <strong>KES {int(bot_county["budget_per_person"]):,}/person</strong>.
# # # #         The Gini coefficient of <strong>{gini:.3f}</strong> reflects {inequality_level.lower()} inequality across all counties.
# # # #     </div>""", unsafe_allow_html=True)

# # # # # ── OVERVIEW ─────────────────────────────────────────────────────────────────
# # # # if "Overview" in section:
# # # #     st.markdown('<div class="section-header">Budget Per Citizen — All 47 Counties</div>', unsafe_allow_html=True)
# # # #     fig1, ax1 = plt.subplots(figsize=(18, 5)); style_chart(fig1, ax1)
# # # #     median = sorted_df['budget_per_person'].median()
# # # #     colors = [RED if v > median * 1.5 else BLUE for v in sorted_df['budget_per_person']]
# # # #     ax1.bar(sorted_df['county'], sorted_df['budget_per_person'], color=colors, edgecolor=DARK_BG, linewidth=0.4, width=0.75)
# # # #     ax1.axhline(df['budget_per_person'].mean(), color=AMBER, linestyle='--', linewidth=1.5, label=f"National Average: KES {int(df['budget_per_person'].mean()):,}")
# # # #     ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
# # # #     ax1.legend(facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=9)
# # # #     ax1.set_ylabel('KES per Person', fontsize=9)
# # # #     plt.xticks(rotation=90, fontsize=7.5, color=MUTED); plt.tight_layout(); st.pyplot(fig1); plt.close()

# # # #     col_l, col_r = st.columns(2)
# # # #     top10 = sorted_df.head(10); bot10 = sorted_df.tail(10).sort_values('budget_per_person')
# # # #     with col_l:
# # # #         st.markdown('<div class="section-header">Top 10 Counties</div>', unsafe_allow_html=True)
# # # #         fig2, ax2 = plt.subplots(figsize=(7, 5)); style_chart(fig2, ax2)
# # # #         ax2.barh(top10['county'], top10['budget_per_person'], color=GREEN, edgecolor=DARK_BG, linewidth=0.4)
# # # #         ax2.set_title('Highest Budget Per Person', fontsize=11, fontweight='bold')
# # # #         ax2.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
# # # #         ax2.set_xlabel('KES per Person'); ax2.invert_yaxis(); ax2.tick_params(axis='y', labelsize=9, colors=TEXT)
# # # #         plt.tight_layout(); st.pyplot(fig2); plt.close()
# # # #     with col_r:
# # # #         st.markdown('<div class="section-header">Bottom 10 Counties</div>', unsafe_allow_html=True)
# # # #         fig3, ax3 = plt.subplots(figsize=(7, 5)); style_chart(fig3, ax3)
# # # #         ax3.barh(bot10['county'], bot10['budget_per_person'], color=RED, edgecolor=DARK_BG, linewidth=0.4)
# # # #         ax3.set_title('Lowest Budget Per Person', fontsize=11, fontweight='bold')
# # # #         ax3.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
# # # #         ax3.set_xlabel('KES per Person'); ax3.invert_yaxis(); ax3.tick_params(axis='y', labelsize=9, colors=TEXT)
# # # #         plt.tight_layout(); st.pyplot(fig3); plt.close()

# # # # # ── CHOROPLETH MAP ────────────────────────────────────────────────────────────
# # # # elif "Choropleth" in section:
# # # #     st.markdown('<div class="section-header">Kenya County Budget Per Citizen — Map View</div>', unsafe_allow_html=True)
# # # #     try:
# # # #         kenya_geojson = load_geojson()
# # # #         df_map = df.copy()
# # # #         df_map['county_mapped'] = df_map['county'].apply(lambda x: NAME_MAP.get(x, x))
# # # #         fig_map = px.choropleth(
# # # #             df_map,
# # # #             geojson=kenya_geojson,
# # # #             locations='county_mapped',
# # # #             featureidkey='properties.COUNTY_NAM',
# # # #             color='budget_per_person',
# # # #             color_continuous_scale='RdYlGn',
# # # #             hover_name='county',
# # # #             hover_data={
# # # #                 'county_mapped': False,
# # # #                 'budget_per_person': ':,',
# # # #                 'budget_billion': True,
# # # #                 'population_2024': ':,'
# # # #             },
# # # #             labels={
# # # #                 'budget_per_person': 'KES/Person',
# # # #                 'budget_billion': 'Budget (KES B)',
# # # #                 'population_2024': 'Population'
# # # #             },
# # # #         )
# # # #         fig_map.update_geos(fitbounds="locations", visible=False)
# # # #         fig_map.update_layout(
# # # #             paper_bgcolor='#0a0f1e', plot_bgcolor='#0a0f1e', font_color='#e8eaf0',
# # # #             coloraxis_colorbar=dict(
# # # #                 title=dict(text='KES/Person', font=dict(color='#e8eaf0')),
# # # #                 tickfont=dict(color='#e8eaf0'),
# # # #                 bgcolor='#111827',
# # # #                 outlinecolor='#1e2d4a',
# # # #             ),
# # # #             margin=dict(l=0, r=0, t=20, b=0), height=600
# # # #         )
# # # #         st.plotly_chart(fig_map, use_container_width=True)
# # # #         st.markdown('<div class="insight-box">🟢 <strong>Green</strong> = higher budget per person &nbsp;·&nbsp; 🔴 <strong>Red</strong> = lower budget per person<br>Hover over any county to see its exact budget, population and KES per person.</div>', unsafe_allow_html=True)
# # # #     except Exception as e:
# # # #         st.error(f"Could not load map: {e}")

# # # # # ── REGIONAL ─────────────────────────────────────────────────────────────────
# # # # elif "Regional" in section:
# # # #     st.markdown('<div class="section-header">Regional Budget Per Person</div>', unsafe_allow_html=True)
# # # #     colors_r = [REGION_COLORS[r] for r in regional['region']]
# # # #     fig_r1, axes_r1 = plt.subplots(1, 2, figsize=(16, 5)); style_chart(fig_r1, axes_r1)
# # # #     axes_r1[0].barh(regional['region'], regional['budget_per_person'], color=colors_r, edgecolor=DARK_BG, linewidth=0.4)
# # # #     axes_r1[0].axvline(df['budget_per_person'].mean(), color=AMBER, linestyle='--', linewidth=1.2, label='National Avg')
# # # #     axes_r1[0].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
# # # #     axes_r1[0].set_title('Average Budget Per Person by Region', fontsize=11, fontweight='bold')
# # # #     axes_r1[0].set_xlabel('KES per Person'); axes_r1[0].invert_yaxis()
# # # #     axes_r1[0].tick_params(axis='y', labelsize=9, colors=TEXT)
# # # #     axes_r1[0].legend(facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=8)
# # # #     wedges, texts, autotexts = axes_r1[1].pie(regional['total_budget'], labels=regional['region'], autopct='%1.1f%%', colors=colors_r, startangle=90, pctdistance=0.75, textprops={'color': TEXT, 'fontsize': 8})
# # # #     for at in autotexts: at.set_color(DARK_BG); at.set_fontsize(7)
# # # #     axes_r1[1].set_title('Share of Total Budget by Region', fontsize=11, fontweight='bold')
# # # #     plt.tight_layout(); st.pyplot(fig_r1); plt.close()

# # # #     st.markdown('<div class="section-header">Within-Region Budget Spread</div>', unsafe_allow_html=True)
# # # #     reg_min = df.groupby('region')['budget_per_person'].min().reset_index().rename(columns={'budget_per_person':'min_bpp'})
# # # #     reg_max = df.groupby('region')['budget_per_person'].max().reset_index().rename(columns={'budget_per_person':'max_bpp'})
# # # #     regional_ext = regional.merge(reg_min, on='region').merge(reg_max, on='region')
# # # #     fig_r2, ax_r2 = plt.subplots(figsize=(14, 5)); style_chart(fig_r2, ax_r2)
# # # #     ax_r2.barh(regional_ext['region'], regional_ext['max_bpp'] - regional_ext['min_bpp'], left=regional_ext['min_bpp'], color=colors_r, alpha=0.5, edgecolor=DARK_BG, linewidth=0.4, height=0.5)
# # # #     ax_r2.scatter(regional_ext['budget_per_person'], regional_ext['region'], color=TEXT, s=50, zorder=5, label='Regional Avg/Person')
# # # #     ax_r2.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
# # # #     ax_r2.set_title('Budget/Person Range Within Each Region (min → max)', fontsize=11, fontweight='bold')
# # # #     ax_r2.set_xlabel('KES per Person'); ax_r2.invert_yaxis(); ax_r2.tick_params(axis='y', labelsize=9, colors=TEXT)
# # # #     ax_r2.legend(facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=8)
# # # #     plt.tight_layout(); st.pyplot(fig_r2); plt.close()

# # # #     st.markdown('<div class="section-header">Regional Summary Table</div>', unsafe_allow_html=True)
# # # #     reg_table = regional[['region','counties','total_pop','total_budget','budget_per_person']].copy()
# # # #     reg_table.columns = ['Region','Counties','Population','Budget (KES B)','Avg Budget/Person (KES)']
# # # #     reg_table = reg_table.reset_index(drop=True); reg_table.index += 1
# # # #     st.dataframe(reg_table, use_container_width=True)

# # # # # ── CORRELATION & GINI ────────────────────────────────────────────────────────
# # # # elif "Correlation" in section:
# # # #     st.markdown('<div class="section-header">Gini Coefficient & Distribution</div>', unsafe_allow_html=True)
# # # #     col_g1, col_g2 = st.columns([1, 2])
# # # #     with col_g1:
# # # #         st.markdown(f"""
# # # #         <div class="metric-card" style="margin-top:1rem;">
# # # #             <div class="metric-label">Gini Coefficient</div>
# # # #             <div class="metric-value metric-accent-amber">{gini:.4f}</div>
# # # #         </div>
# # # #         <div class="insight-box">
# # # #             A Gini of <strong>{gini:.3f}</strong> indicates <strong>{'high' if gini > 0.35 else 'moderate' if gini > 0.25 else 'low'} inequality</strong> in per-capita budget allocation.<br><br>
# # # #             The top county (<strong>{sorted_df.iloc[0]['county']}</strong>) receives <strong>{sorted_df.iloc[0]['budget_per_person'] / sorted_df.iloc[-1]['budget_per_person']:.1f}x</strong> more per person than the bottom (<strong>{sorted_df.iloc[-1]['county']}</strong>).
# # # #         </div>""", unsafe_allow_html=True)
# # # #     with col_g2:
# # # #         fig_g, axes_g = plt.subplots(1, 2, figsize=(12, 4)); style_chart(fig_g, axes_g)
# # # #         sorted_vals = np.sort(df['budget_per_person'].values); n = len(sorted_vals)
# # # #         lorenz_x = np.concatenate([[0], np.arange(1, n+1) / n])
# # # #         lorenz_y = np.concatenate([[0], np.cumsum(sorted_vals) / sorted_vals.sum()])
# # # #         axes_g[0].plot(lorenz_x, lorenz_y, color=BLUE, linewidth=2.5, label=f'Lorenz Curve (Gini={gini:.3f})')
# # # #         axes_g[0].plot([0,1],[0,1], color=MUTED, linestyle='--', linewidth=1.2, label='Perfect Equality')
# # # #         axes_g[0].fill_between(lorenz_x, lorenz_y, lorenz_x, alpha=0.15, color=RED)
# # # #         axes_g[0].set_title('Lorenz Curve', fontsize=11, fontweight='bold')
# # # #         axes_g[0].set_xlabel('Cumulative Share of Counties'); axes_g[0].set_ylabel('Cumulative Budget Share')
# # # #         axes_g[0].legend(facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=8)
# # # #         axes_g[1].hist(df['budget_per_person'], bins=12, color=BLUE, edgecolor=DARK_BG, linewidth=0.5, alpha=0.85)
# # # #         axes_g[1].axvline(df['budget_per_person'].mean(), color=AMBER, linestyle='--', linewidth=1.5, label=f"Mean: KES {int(df['budget_per_person'].mean()):,}")
# # # #         axes_g[1].axvline(df['budget_per_person'].median(), color=GREEN, linestyle='--', linewidth=1.5, label=f"Median: KES {int(df['budget_per_person'].median()):,}")
# # # #         axes_g[1].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
# # # #         axes_g[1].set_title('Budget/Person Distribution', fontsize=11, fontweight='bold')
# # # #         axes_g[1].set_xlabel('KES per Person'); axes_g[1].set_ylabel('Number of Counties')
# # # #         axes_g[1].legend(facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=8)
# # # #         plt.tight_layout(); st.pyplot(fig_g); plt.close()

# # # #     st.markdown('<div class="section-header">Correlation Analysis</div>', unsafe_allow_html=True)
# # # #     col_c1, col_c2 = st.columns(2)
# # # #     with col_c1: st.markdown(f'<div class="metric-card"><div class="metric-label">Population vs Absolute Budget</div><div class="metric-value metric-accent-green">r = {corr_bp:.3f}</div></div>', unsafe_allow_html=True)
# # # #     with col_c2: st.markdown(f'<div class="metric-card"><div class="metric-label">Population vs Budget Per Person</div><div class="metric-value metric-accent-red">r = {corr_bpp:.3f}</div></div>', unsafe_allow_html=True)

# # # #     colors_scatter = [REGION_COLORS[r] for r in df['region']]
# # # #     fig_c, axes_c = plt.subplots(1, 2, figsize=(16, 5)); style_chart(fig_c, axes_c)
# # # #     axes_c[0].scatter(df['population_2024']/1e6, df['budget_billion'], c=colors_scatter, s=70, alpha=0.85, edgecolors='#1e2d4a', linewidth=0.6)
# # # #     m, b, *_ = stats.linregress(df['population_2024']/1e6, df['budget_billion'])
# # # #     x_line = np.linspace(df['population_2024'].min()/1e6, df['population_2024'].max()/1e6, 100)
# # # #     axes_c[0].plot(x_line, m*x_line+b, color=AMBER, linewidth=1.8, linestyle='--')
# # # #     for _, row in df.iterrows():
# # # #         if row['county'] in ['Nairobi','Lamu','Nakuru','Kiambu','Turkana']:
# # # #             axes_c[0].annotate(row['county'], (row['population_2024']/1e6, row['budget_billion']), textcoords='offset points', xytext=(6,4), fontsize=7.5, color=TEXT)
# # # #     legend_patches = [mpatches.Patch(color=v, label=k) for k, v in REGION_COLORS.items()]
# # # #     axes_c[0].legend(handles=legend_patches, facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=7, ncol=2, loc='upper left')
# # # #     axes_c[0].set_title('Population vs Absolute Budget', fontsize=11, fontweight='bold')
# # # #     axes_c[0].set_xlabel('Population (millions)'); axes_c[0].set_ylabel('Budget (KES Billions)')
# # # #     axes_c[1].scatter(df['population_2024']/1e6, df['budget_per_person'], c=colors_scatter, s=70, alpha=0.85, edgecolors='#1e2d4a', linewidth=0.6)
# # # #     m2, b2, *_ = stats.linregress(df['population_2024']/1e6, df['budget_per_person'])
# # # #     axes_c[1].plot(x_line, m2*x_line+b2, color=AMBER, linewidth=1.8, linestyle='--', label=f'r = {corr_bpp:.3f}')
# # # #     for _, row in df.iterrows():
# # # #         if row['county'] in ['Nairobi','Lamu','Nakuru','Kiambu','Marsabit']:
# # # #             axes_c[1].annotate(row['county'], (row['population_2024']/1e6, row['budget_per_person']), textcoords='offset points', xytext=(6,4), fontsize=7.5, color=TEXT)
# # # #     axes_c[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
# # # #     axes_c[1].set_title('Population vs Budget Per Person', fontsize=11, fontweight='bold')
# # # #     axes_c[1].set_xlabel('Population (millions)'); axes_c[1].set_ylabel('Budget Per Person (KES)')
# # # #     axes_c[1].legend(facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=9)
# # # #     plt.tight_layout(); st.pyplot(fig_c); plt.close()
# # # #     st.markdown(f'<div class="insight-box">📌 <strong>Key finding:</strong> Larger counties receive significantly <em>less</em> per person (r = {corr_bpp:.3f}, p &lt; 0.001). The equitable share formula disproportionately benefits low-population counties like Lamu, Marsabit and Samburu, while high-density counties like Nairobi, Kiambu and Nakuru receive the least per citizen.</div>', unsafe_allow_html=True)

# # # # # ── QUINTILE ──────────────────────────────────────────────────────────────────
# # # # elif "Quintile" in section:
# # # #     st.markdown('<div class="section-header">Quintile Analysis</div>', unsafe_allow_html=True)
# # # #     df_q = df.copy()
# # # #     df_q['quintile'] = pd.qcut(df_q['budget_per_person'], q=5, labels=['Q1 Bottom 20%','Q2','Q3 Middle','Q4','Q5 Top 20%'])
# # # #     quintile_summary = df_q.groupby('quintile', observed=True).agg(counties=('county','count'), avg_bpp=('budget_per_person','mean'), counties_list=('county', lambda x: ', '.join(sorted(x)))).reset_index()
# # # #     quintile_colors = [RED, '#f97316', AMBER, '#84cc16', GREEN]
# # # #     fig_q, axes_q = plt.subplots(1, 2, figsize=(16, 5)); style_chart(fig_q, axes_q)
# # # #     axes_q[0].bar(quintile_summary['quintile'], quintile_summary['avg_bpp'], color=quintile_colors, edgecolor=DARK_BG, linewidth=0.4)
# # # #     axes_q[0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
# # # #     axes_q[0].set_title('Average Budget Per Person by Quintile', fontsize=11, fontweight='bold')
# # # #     axes_q[0].set_ylabel('KES per Person'); axes_q[0].tick_params(axis='x', labelsize=8, colors=TEXT)
# # # #     region_order = regional['region'].tolist()
# # # #     region_data = [df[df['region'] == r]['budget_per_person'].values for r in region_order]
# # # #     bp = axes_q[1].boxplot(region_data, tick_labels=region_order, patch_artist=True, vert=True)
# # # #     for patch, region in zip(bp['boxes'], region_order):
# # # #         patch.set_facecolor(REGION_COLORS[region]); patch.set_alpha(0.7)
# # # #     for element in ['whiskers','caps','medians','fliers']:
# # # #         for item in bp[element]: item.set_color(TEXT)
# # # #     axes_q[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
# # # #     axes_q[1].set_title('Budget/Person Distribution by Region', fontsize=11, fontweight='bold')
# # # #     axes_q[1].set_ylabel('KES per Person'); axes_q[1].tick_params(axis='x', rotation=30, labelsize=8, colors=TEXT)
# # # #     plt.tight_layout(); st.pyplot(fig_q); plt.close()

# # # #     st.markdown('<div class="section-header">Counties by Quintile</div>', unsafe_allow_html=True)
# # # #     for i, (_, row) in enumerate(quintile_summary.iterrows()):
# # # #         color = quintile_colors[i]
# # # #         st.markdown(f'<div class="insight-box" style="border-left-color:{color}"><strong style="color:{color}">{row["quintile"]}</strong> &nbsp;·&nbsp; Avg: KES {int(row["avg_bpp"]):,}/person &nbsp;·&nbsp; {int(row["counties"])} counties<br><span style="color:#7a8aaa">{row["counties_list"]}</span></div>', unsafe_allow_html=True)

# # # # # ── COUNTY EXPLORER ───────────────────────────────────────────────────────────
# # # # elif "Explorer" in section:
# # # #     st.markdown('<div class="section-header">County Explorer</div>', unsafe_allow_html=True)
# # # #     col_s, col_info = st.columns([1, 2])
# # # #     with col_s:
# # # #         selected = st.selectbox('Select a County', options=sorted(df['county'].tolist()))
# # # #     with col_info:
# # # #         row = df[df['county'] == selected].iloc[0]
# # # #         rank = sorted_df[sorted_df['county'] == selected].index[0] + 1
# # # #         nat_avg = int(df['budget_per_person'].mean())
# # # #         diff = int(row['budget_per_person']) - nat_avg
# # # #         diff_str = f"+KES {diff:,}" if diff > 0 else f"-KES {abs(diff):,}"
# # # #         diff_color = "metric-accent-green" if diff > 0 else "metric-accent-red"
# # # #         reg_avg = int(regional[regional['region'] == row['region']]['budget_per_person'].values[0])
# # # #         ca, cb2, cc, cd = st.columns(4)
# # # #         with ca: st.markdown(f'<div class="metric-card"><div class="metric-label">Population</div><div class="metric-value" style="font-size:1.3rem">{int(row["population_2024"]):,}</div></div>', unsafe_allow_html=True)
# # # #         with cb2: st.markdown(f'<div class="metric-card"><div class="metric-label">Budget</div><div class="metric-value" style="font-size:1.3rem">KES {row["budget_billion"]}B</div></div>', unsafe_allow_html=True)
# # # #         with cc: st.markdown(f'<div class="metric-card"><div class="metric-label">Per Person · Rank #{rank}</div><div class="metric-value {diff_color}" style="font-size:1.3rem">KES {int(row["budget_per_person"]):,}</div></div>', unsafe_allow_html=True)
# # # #         with cd: st.markdown(f'<div class="metric-card"><div class="metric-label">Region ({row["region"]})</div><div class="metric-value" style="font-size:1.3rem">KES {reg_avg:,}</div></div>', unsafe_allow_html=True)
# # # #         st.markdown(f'<div class="insight-box"><strong>{selected}</strong> is ranked <strong>#{rank} of 47</strong> counties by budget per person. It is <strong>{diff_str}</strong> vs the national average of KES {nat_avg:,}/person, and sits in the <strong>{row["region"]}</strong> region (regional avg: KES {reg_avg:,}/person).</div>', unsafe_allow_html=True)

# # # # # ── FULL RANKINGS ─────────────────────────────────────────────────────────────
# # # # elif "Rankings" in section:
# # # #     st.markdown('<div class="section-header">Full County Rankings</div>', unsafe_allow_html=True)
# # # #     region_filter = st.multiselect('Filter by Region', options=sorted(df['region'].unique()), default=sorted(df['region'].unique()))
# # # #     filtered = sorted_df[sorted_df['region'].isin(region_filter)]
# # # #     table = filtered[['county','region','population_2024','budget_billion','budget_per_person']].copy()
# # # #     table.columns = ['County','Region','Population (2024)','Budget (KES B)','Budget/Person (KES)']
# # # #     table = table.reset_index(drop=True); table.index += 1
# # # #     st.dataframe(table, use_container_width=True, height=600)
# # # #     csv = table.to_csv().encode('utf-8')
# # # #     st.download_button("⬇ Download as CSV", csv, "kenya_county_budget.csv", "text/csv")

# # # import streamlit as st
# # # import pandas as pd
# # # import numpy as np
# # # import matplotlib.pyplot as plt
# # # import matplotlib.ticker as mticker
# # # import matplotlib.patches as mpatches
# # # import plotly.express as px
# # # import json
# # # import urllib.request
# # # from scipy import stats

# # # st.set_page_config(page_title="Kenya County Budget Analysis", page_icon="🇰🇪", layout="wide")

# # # st.markdown("""
# # # <style>
# # #     @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500&display=swap');
# # #     html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
# # #     .stApp { background-color: #0a0f1e; color: #e8eaf0; }
# # #     h1, h2, h3 { font-family: 'Syne', sans-serif !important; }
# # #     .hero-title { font-family: 'Syne', sans-serif; font-size: 3rem; font-weight: 800; color: #ffffff; line-height: 1.1; margin-bottom: 0.3rem; }
# # #     .hero-sub { font-size: 1rem; color: #7a8aaa; margin-bottom: 2rem; font-weight: 300; letter-spacing: 0.05em; }
# # #     .metric-card { background: linear-gradient(135deg, #111827 0%, #1a2340 100%); border: 1px solid #1e2d4a; border-radius: 12px; padding: 1.4rem 1.6rem; margin-bottom: 1rem; }
# # #     .metric-label { font-size: 0.72rem; font-weight: 500; color: #5a6a8a; text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 0.4rem; }
# # #     .metric-value { font-family: 'Syne', sans-serif; font-size: 1.9rem; font-weight: 700; color: #ffffff; line-height: 1; }
# # #     .metric-accent { color: #3b82f6; } .metric-accent-green { color: #10b981; } .metric-accent-red { color: #ef4444; } .metric-accent-amber { color: #f59e0b; }
# # #     .section-header { font-family: 'Syne', sans-serif; font-size: 1.1rem; font-weight: 700; color: #ffffff; text-transform: uppercase; letter-spacing: 0.08em; border-left: 3px solid #3b82f6; padding-left: 0.8rem; margin-bottom: 1rem; margin-top: 2rem; }
# # #     .badge { display: inline-block; background: #1e3a5f; color: #60a5fa; font-size: 0.7rem; font-weight: 600; padding: 2px 10px; border-radius: 20px; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 0.5rem; }
# # #     .insight-box { background: linear-gradient(135deg, #0f1f3d 0%, #1a2340 100%); border: 1px solid #1e3a5f; border-left: 3px solid #f59e0b; border-radius: 8px; padding: 1rem 1.2rem; margin: 0.5rem 0; font-size: 0.9rem; color: #c8d4e8; line-height: 1.6; }
# # #     footer {visibility: hidden;} #MainMenu {visibility: hidden;} header {visibility: hidden;}
# # # </style>
# # # """, unsafe_allow_html=True)

# # # DARK_BG = '#0a0f1e'; CARD_BG = '#111827'; BLUE = '#3b82f6'; GREEN = '#10b981'
# # # RED = '#ef4444'; AMBER = '#f59e0b'; TEXT = '#e8eaf0'; MUTED = '#7a8aaa'
# # # REGION_COLORS = {
# # #     'Nairobi': '#3b82f6', 'Central': '#10b981', 'Coast': '#f59e0b',
# # #     'Eastern': '#8b5cf6', 'North Eastern': '#ef4444', 'Nyanza': '#06b6d4',
# # #     'Rift Valley': '#f97316', 'Western': '#ec4899',
# # # }

# # # NAME_MAP = {
# # #     'Tana River':     'Tana River',
# # #     'Taita Taveta':   'Taita-Taveta',
# # #     'Elgeyo Marakwet':'Elgeyo/Marakwet',
# # #     "Murang'a":       'Muranga',
# # #     'Trans Nzoia':    'Trans-Nzoia',
# # #     'Homa Bay':       'Homa Bay',
# # #     'Tharaka Nithi':  'Tharaka-Nithi',
# # #     'West Pokot':     'West Pokot',
# # #     'Uasin Gishu':    'Uasin Gishu',
# # # }

# # # def style_chart(fig, axes):
# # #     fig.patch.set_facecolor(DARK_BG)
# # #     if not hasattr(axes, '__iter__'): axes = [axes]
# # #     for ax in axes:
# # #         ax.set_facecolor(CARD_BG); ax.tick_params(colors=MUTED, labelsize=8)
# # #         ax.xaxis.label.set_color(MUTED); ax.yaxis.label.set_color(MUTED); ax.title.set_color(TEXT)
# # #         for spine in ax.spines.values(): spine.set_edgecolor('#1e2d4a')

# # # def gini_coefficient(values):
# # #     arr = np.sort(np.array(values, dtype=float)); n = len(arr); cumsum = np.cumsum(arr)
# # #     return (2 * np.sum(np.arange(1, n+1) * arr) - (n+1) * cumsum[-1]) / (n * cumsum[-1])

# # # @st.cache_data
# # # def load_data():
# # #     df = pd.read_csv('data/county_data.csv')
# # #     df['budget_per_person'] = (df['budget_billion'] * 1_000_000_000) / df['population_2024']
# # #     df['budget_per_person'] = df['budget_per_person'].round(0).astype(int)
# # #     return df

# # # @st.cache_data
# # # def load_geojson():
# # #     url = "https://raw.githubusercontent.com/mikelmaron/kenya-election-data/master/data/counties.geojson"
# # #     with urllib.request.urlopen(url) as response:
# # #         geojson = json.loads(response.read().decode())
# # #     for feature in geojson['features']:
# # #         name = feature['properties'].get('COUNTY_NAM', '')
# # #         if name:
# # #             feature['properties']['COUNTY_NAM'] = name.strip().title()
# # #     return geojson

# # # df = load_data()
# # # sorted_df = df.sort_values('budget_per_person', ascending=False).reset_index(drop=True)
# # # regional = df.groupby('region').agg(counties=('county','count'), total_pop=('population_2024','sum'), total_budget=('budget_billion','sum')).reset_index()
# # # regional['budget_per_person'] = ((regional['total_budget'] * 1e9) / regional['total_pop']).astype(int)
# # # regional = regional.sort_values('budget_per_person', ascending=False)
# # # gini = gini_coefficient(df['budget_per_person'])
# # # corr_bpp, pval_bpp = stats.pearsonr(df['population_2024'], df['budget_per_person'])
# # # corr_bp, _ = stats.pearsonr(df['population_2024'], df['budget_billion'])

# # # top_county = sorted_df.iloc[0]; bot_county = sorted_df.iloc[-1]

# # # SECTIONS = ["🏠 Home", "📊 Overview", "🗺️ Choropleth Map", "📍 Regional Analysis",
# # #             "🔗 Correlation & Gini", "🎯 Quintile Analysis", "🔍 County Explorer",
# # #             "🔀 County Comparison", "📈 Budget Trends", "📋 Full Rankings"]

# # # # Resolve nav button clicks BEFORE sidebar renders
# # # if "nav_target" in st.session_state:
# # #     default_idx = SECTIONS.index(st.session_state["nav_target"]) if st.session_state["nav_target"] in SECTIONS else 0
# # #     del st.session_state["nav_target"]
# # # else:
# # #     default_idx = 0

# # # with st.sidebar:
# # #     st.markdown('<div style="font-family:Syne,sans-serif;font-size:1.1rem;font-weight:800;color:#fff;margin-bottom:1rem;">🇰🇪 Navigation</div>', unsafe_allow_html=True)
# # #     section = st.radio("Go to", SECTIONS, index=default_idx)
# # #     st.markdown("---")
# # #     st.markdown(f'<div style="color:{MUTED};font-size:0.75rem;">Data: KNBS 2024 Projections<br>Budget: FY 2023/24 Equitable Share<br>Counties: 47</div>', unsafe_allow_html=True)

# # # # ── HOME PAGE ─────────────────────────────────────────────────────────────────
# # # if "Home" in section:
# # #     st.markdown('<div class="badge">FY 2023/24 · All 47 Counties</div>', unsafe_allow_html=True)
# # #     st.markdown('<div class="hero-title">🇰🇪 Kenya County<br>Budget Analysis</div>', unsafe_allow_html=True)
# # #     st.markdown('<div class="hero-sub">Equitable Share Allocations · KNBS 2024 Population Projections</div>', unsafe_allow_html=True)

# # #     # ── 2-column metric grid ──
# # #     st.markdown('<div class="section-header">Key Metrics</div>', unsafe_allow_html=True)
# # #     m1, m2 = st.columns(2)
# # #     m3, m4 = st.columns(2)
# # #     with m1:
# # #         st.markdown(f"""
# # #         <div class="metric-card">
# # #             <div class="metric-label">📊 National Avg Budget / Person</div>
# # #             <div class="metric-value metric-accent-green">KES {int(df["budget_per_person"].mean()):,}</div>
# # #             <div style="color:{MUTED};font-size:0.78rem;margin-top:0.5rem;">Total budget: KES {df["budget_billion"].sum():.1f}B &nbsp;·&nbsp; Population: {df["population_2024"].sum()/1e6:.1f}M</div>
# # #         </div>""", unsafe_allow_html=True)
# # #     with m2:
# # #         st.markdown(f"""
# # #         <div class="metric-card">
# # #             <div class="metric-label">🏆 Highest Funded County</div>
# # #             <div class="metric-value metric-accent-green" style="font-size:1.6rem;">{top_county["county"]}</div>
# # #             <div style="color:#10b981;font-size:0.9rem;margin-top:0.5rem;font-weight:600;">KES {int(top_county["budget_per_person"]):,} per person &nbsp;·&nbsp; {top_county["region"]} Region</div>
# # #         </div>""", unsafe_allow_html=True)
# # #     with m3:
# # #         st.markdown(f"""
# # #         <div class="metric-card">
# # #             <div class="metric-label">📉 Lowest Funded County</div>
# # #             <div class="metric-value metric-accent-red" style="font-size:1.6rem;">{bot_county["county"]}</div>
# # #             <div style="color:#ef4444;font-size:0.9rem;margin-top:0.5rem;font-weight:600;">KES {int(bot_county["budget_per_person"]):,} per person &nbsp;·&nbsp; {bot_county["region"]} Region</div>
# # #         </div>""", unsafe_allow_html=True)
# # #     with m4:
# # #         inequality_level = "Low" if gini < 0.2 else "Moderate" if gini < 0.35 else "High"
# # #         gap_x = int(top_county["budget_per_person"] / bot_county["budget_per_person"])
# # #         st.markdown(f"""
# # #         <div class="metric-card">
# # #             <div class="metric-label">⚖️ Funding Inequality (Gini)</div>
# # #             <div class="metric-value metric-accent-amber">{gini:.3f}</div>
# # #             <div style="color:{MUTED};font-size:0.78rem;margin-top:0.5rem;">{inequality_level} inequality &nbsp;·&nbsp; Highest county gets <strong style="color:#f59e0b;">{gap_x}x</strong> more per person than lowest</div>
# # #         </div>""", unsafe_allow_html=True)

# # #     # ── Navigation buttons ──
# # #     st.markdown('<div class="section-header">Explore the Dashboard</div>', unsafe_allow_html=True)
# # #     NAV_ITEMS = [
# # #         ("📊", "Overview",          "Bar charts of all 47 counties ranked by budget per person",      "Overview"),
# # #         ("🗺️", "Choropleth Map",    "Interactive Kenya map colored by budget per citizen",            "Choropleth Map"),
# # #         ("📍", "Regional Analysis", "Compare 8 regions — budgets, pie charts & spread",              "Regional Analysis"),
# # #         ("🔗", "Correlation & Gini","Lorenz curve, Gini deep-dive & population scatter plots",       "Correlation & Gini"),
# # #         ("🎯", "Quintile Analysis", "Counties grouped into 5 funding bands with regional boxplots",  "Quintile Analysis"),
# # #         ("🔍", "County Explorer",   "Pick any county — budget, poverty, health & school stats",      "County Explorer"),
# # #         ("🔀", "County Comparison", "Pick any 2 counties and compare them side by side",             "County Comparison"),
# # #         ("📈", "Budget Trends",     "Budget growth FY 2019/20 → 2023/24 by county & national",      "Budget Trends"),
# # #         ("📋", "Full Rankings",     "Filterable table of all 47 counties with CSV download",         "Full Rankings"),
# # #     ]
# # #     row1 = st.columns(3)
# # #     row2 = st.columns(3)
# # #     row3 = st.columns(3)
# # #     rows = [row1[0], row1[1], row1[2], row2[0], row2[1], row2[2], row3[0], row3[1], row3[2]]
# # #     for col, (icon, title, desc, key) in zip(rows, NAV_ITEMS):
# # #         with col:
# # #             st.markdown(f"""
# # #             <div style="background:linear-gradient(135deg,#111827,#1a2340);border:1px solid #1e2d4a;
# # #                         border-radius:12px;padding:1.2rem 1.3rem;margin-bottom:0.8rem;
# # #                         transition:border-color 0.2s;">
# # #                 <div style="font-size:1.6rem;margin-bottom:0.4rem;">{icon}</div>
# # #                 <div style="font-family:Syne,sans-serif;font-size:0.95rem;font-weight:700;
# # #                             color:#fff;margin-bottom:0.3rem;">{title}</div>
# # #                 <div style="font-size:0.78rem;color:{MUTED};line-height:1.4;">{desc}</div>
# # #             </div>""", unsafe_allow_html=True)
# # #             if st.button(f"Open {title}", key=f"nav_{key}", use_container_width=True):
# # #                 icon_map = {"Overview":"📊","Choropleth Map":"🗺️","Regional Analysis":"📍",
# # #                             "Correlation & Gini":"🔗","Quintile Analysis":"🎯",
# # #                             "County Explorer":"🔍","County Comparison":"🔀",
# # #                             "Budget Trends":"📈","Full Rankings":"📋"}
# # #                 st.session_state["nav_target"] = f"{icon_map[title]} {title}"
# # #                 st.rerun()

# # #     st.markdown(f"""
# # #     <div class="insight-box" style="margin-top:1rem;">
# # #         💡 <strong>Key finding:</strong> {top_county["county"]} receives <strong>KES {int(top_county["budget_per_person"]):,}/person</strong>
# # #         — {gap_x}x more than {bot_county["county"]} which gets <strong>KES {int(bot_county["budget_per_person"]):,}/person</strong>.
# # #         The Gini coefficient of <strong>{gini:.3f}</strong> reflects {inequality_level.lower()} inequality across all counties.
# # #     </div>""", unsafe_allow_html=True)

# # # # ── OVERVIEW ─────────────────────────────────────────────────────────────────
# # # if "Overview" in section:
# # #     st.markdown('<div class="section-header">Budget Per Citizen — All 47 Counties</div>', unsafe_allow_html=True)
# # #     fig1, ax1 = plt.subplots(figsize=(18, 5)); style_chart(fig1, ax1)
# # #     median = sorted_df['budget_per_person'].median()
# # #     colors = [RED if v > median * 1.5 else BLUE for v in sorted_df['budget_per_person']]
# # #     ax1.bar(sorted_df['county'], sorted_df['budget_per_person'], color=colors, edgecolor=DARK_BG, linewidth=0.4, width=0.75)
# # #     ax1.axhline(df['budget_per_person'].mean(), color=AMBER, linestyle='--', linewidth=1.5, label=f"National Average: KES {int(df['budget_per_person'].mean()):,}")
# # #     ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
# # #     ax1.legend(facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=9)
# # #     ax1.set_ylabel('KES per Person', fontsize=9)
# # #     plt.xticks(rotation=90, fontsize=7.5, color=MUTED); plt.tight_layout(); st.pyplot(fig1); plt.close()

# # #     col_l, col_r = st.columns(2)
# # #     top10 = sorted_df.head(10); bot10 = sorted_df.tail(10).sort_values('budget_per_person')
# # #     with col_l:
# # #         st.markdown('<div class="section-header">Top 10 Counties</div>', unsafe_allow_html=True)
# # #         fig2, ax2 = plt.subplots(figsize=(7, 5)); style_chart(fig2, ax2)
# # #         ax2.barh(top10['county'], top10['budget_per_person'], color=GREEN, edgecolor=DARK_BG, linewidth=0.4)
# # #         ax2.set_title('Highest Budget Per Person', fontsize=11, fontweight='bold')
# # #         ax2.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
# # #         ax2.set_xlabel('KES per Person'); ax2.invert_yaxis(); ax2.tick_params(axis='y', labelsize=9, colors=TEXT)
# # #         plt.tight_layout(); st.pyplot(fig2); plt.close()
# # #     with col_r:
# # #         st.markdown('<div class="section-header">Bottom 10 Counties</div>', unsafe_allow_html=True)
# # #         fig3, ax3 = plt.subplots(figsize=(7, 5)); style_chart(fig3, ax3)
# # #         ax3.barh(bot10['county'], bot10['budget_per_person'], color=RED, edgecolor=DARK_BG, linewidth=0.4)
# # #         ax3.set_title('Lowest Budget Per Person', fontsize=11, fontweight='bold')
# # #         ax3.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
# # #         ax3.set_xlabel('KES per Person'); ax3.invert_yaxis(); ax3.tick_params(axis='y', labelsize=9, colors=TEXT)
# # #         plt.tight_layout(); st.pyplot(fig3); plt.close()

# # # # ── CHOROPLETH MAP ────────────────────────────────────────────────────────────
# # # elif "Choropleth" in section:
# # #     st.markdown('<div class="section-header">Kenya County Budget Per Citizen — Map View</div>', unsafe_allow_html=True)
# # #     try:
# # #         kenya_geojson = load_geojson()
# # #         df_map = df.copy()
# # #         df_map['county_mapped'] = df_map['county'].apply(lambda x: NAME_MAP.get(x, x))
# # #         fig_map = px.choropleth(
# # #             df_map,
# # #             geojson=kenya_geojson,
# # #             locations='county_mapped',
# # #             featureidkey='properties.COUNTY_NAM',
# # #             color='budget_per_person',
# # #             color_continuous_scale='RdYlGn',
# # #             hover_name='county',
# # #             hover_data={
# # #                 'county_mapped': False,
# # #                 'budget_per_person': ':,',
# # #                 'budget_billion': True,
# # #                 'population_2024': ':,'
# # #             },
# # #             labels={
# # #                 'budget_per_person': 'KES/Person',
# # #                 'budget_billion': 'Budget (KES B)',
# # #                 'population_2024': 'Population'
# # #             },
# # #         )
# # #         fig_map.update_geos(fitbounds="locations", visible=False)
# # #         fig_map.update_layout(
# # #             paper_bgcolor='#0a0f1e', plot_bgcolor='#0a0f1e', font_color='#e8eaf0',
# # #             coloraxis_colorbar=dict(
# # #                 title=dict(text='KES/Person', font=dict(color='#e8eaf0')),
# # #                 tickfont=dict(color='#e8eaf0'),
# # #                 bgcolor='#111827',
# # #                 outlinecolor='#1e2d4a',
# # #             ),
# # #             margin=dict(l=0, r=0, t=20, b=0), height=600
# # #         )
# # #         st.plotly_chart(fig_map, use_container_width=True)
# # #         st.markdown('<div class="insight-box">🟢 <strong>Green</strong> = higher budget per person &nbsp;·&nbsp; 🔴 <strong>Red</strong> = lower budget per person<br>Hover over any county to see its exact budget, population and KES per person.</div>', unsafe_allow_html=True)
# # #     except Exception as e:
# # #         st.error(f"Could not load map: {e}")

# # # # ── REGIONAL ─────────────────────────────────────────────────────────────────
# # # elif "Regional" in section:
# # #     st.markdown('<div class="section-header">Regional Budget Per Person</div>', unsafe_allow_html=True)
# # #     colors_r = [REGION_COLORS[r] for r in regional['region']]
# # #     fig_r1, axes_r1 = plt.subplots(1, 2, figsize=(16, 5)); style_chart(fig_r1, axes_r1)
# # #     axes_r1[0].barh(regional['region'], regional['budget_per_person'], color=colors_r, edgecolor=DARK_BG, linewidth=0.4)
# # #     axes_r1[0].axvline(df['budget_per_person'].mean(), color=AMBER, linestyle='--', linewidth=1.2, label='National Avg')
# # #     axes_r1[0].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
# # #     axes_r1[0].set_title('Average Budget Per Person by Region', fontsize=11, fontweight='bold')
# # #     axes_r1[0].set_xlabel('KES per Person'); axes_r1[0].invert_yaxis()
# # #     axes_r1[0].tick_params(axis='y', labelsize=9, colors=TEXT)
# # #     axes_r1[0].legend(facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=8)
# # #     wedges, texts, autotexts = axes_r1[1].pie(regional['total_budget'], labels=regional['region'], autopct='%1.1f%%', colors=colors_r, startangle=90, pctdistance=0.75, textprops={'color': TEXT, 'fontsize': 8})
# # #     for at in autotexts: at.set_color(DARK_BG); at.set_fontsize(7)
# # #     axes_r1[1].set_title('Share of Total Budget by Region', fontsize=11, fontweight='bold')
# # #     plt.tight_layout(); st.pyplot(fig_r1); plt.close()

# # #     st.markdown('<div class="section-header">Within-Region Budget Spread</div>', unsafe_allow_html=True)
# # #     reg_min = df.groupby('region')['budget_per_person'].min().reset_index().rename(columns={'budget_per_person':'min_bpp'})
# # #     reg_max = df.groupby('region')['budget_per_person'].max().reset_index().rename(columns={'budget_per_person':'max_bpp'})
# # #     regional_ext = regional.merge(reg_min, on='region').merge(reg_max, on='region')
# # #     fig_r2, ax_r2 = plt.subplots(figsize=(14, 5)); style_chart(fig_r2, ax_r2)
# # #     ax_r2.barh(regional_ext['region'], regional_ext['max_bpp'] - regional_ext['min_bpp'], left=regional_ext['min_bpp'], color=colors_r, alpha=0.5, edgecolor=DARK_BG, linewidth=0.4, height=0.5)
# # #     ax_r2.scatter(regional_ext['budget_per_person'], regional_ext['region'], color=TEXT, s=50, zorder=5, label='Regional Avg/Person')
# # #     ax_r2.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
# # #     ax_r2.set_title('Budget/Person Range Within Each Region (min → max)', fontsize=11, fontweight='bold')
# # #     ax_r2.set_xlabel('KES per Person'); ax_r2.invert_yaxis(); ax_r2.tick_params(axis='y', labelsize=9, colors=TEXT)
# # #     ax_r2.legend(facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=8)
# # #     plt.tight_layout(); st.pyplot(fig_r2); plt.close()

# # #     st.markdown('<div class="section-header">Regional Summary Table</div>', unsafe_allow_html=True)
# # #     reg_table = regional[['region','counties','total_pop','total_budget','budget_per_person']].copy()
# # #     reg_table.columns = ['Region','Counties','Population','Budget (KES B)','Avg Budget/Person (KES)']
# # #     reg_table = reg_table.reset_index(drop=True); reg_table.index += 1
# # #     st.dataframe(reg_table, use_container_width=True)

# # # # ── CORRELATION & GINI ────────────────────────────────────────────────────────
# # # elif "Correlation" in section:
# # #     st.markdown('<div class="section-header">Gini Coefficient & Distribution</div>', unsafe_allow_html=True)
# # #     col_g1, col_g2 = st.columns([1, 2])
# # #     with col_g1:
# # #         st.markdown(f"""
# # #         <div class="metric-card" style="margin-top:1rem;">
# # #             <div class="metric-label">Gini Coefficient</div>
# # #             <div class="metric-value metric-accent-amber">{gini:.4f}</div>
# # #         </div>
# # #         <div class="insight-box">
# # #             A Gini of <strong>{gini:.3f}</strong> indicates <strong>{'high' if gini > 0.35 else 'moderate' if gini > 0.25 else 'low'} inequality</strong> in per-capita budget allocation.<br><br>
# # #             The top county (<strong>{sorted_df.iloc[0]['county']}</strong>) receives <strong>{sorted_df.iloc[0]['budget_per_person'] / sorted_df.iloc[-1]['budget_per_person']:.1f}x</strong> more per person than the bottom (<strong>{sorted_df.iloc[-1]['county']}</strong>).
# # #         </div>""", unsafe_allow_html=True)
# # #     with col_g2:
# # #         fig_g, axes_g = plt.subplots(1, 2, figsize=(12, 4)); style_chart(fig_g, axes_g)
# # #         sorted_vals = np.sort(df['budget_per_person'].values); n = len(sorted_vals)
# # #         lorenz_x = np.concatenate([[0], np.arange(1, n+1) / n])
# # #         lorenz_y = np.concatenate([[0], np.cumsum(sorted_vals) / sorted_vals.sum()])
# # #         axes_g[0].plot(lorenz_x, lorenz_y, color=BLUE, linewidth=2.5, label=f'Lorenz Curve (Gini={gini:.3f})')
# # #         axes_g[0].plot([0,1],[0,1], color=MUTED, linestyle='--', linewidth=1.2, label='Perfect Equality')
# # #         axes_g[0].fill_between(lorenz_x, lorenz_y, lorenz_x, alpha=0.15, color=RED)
# # #         axes_g[0].set_title('Lorenz Curve', fontsize=11, fontweight='bold')
# # #         axes_g[0].set_xlabel('Cumulative Share of Counties'); axes_g[0].set_ylabel('Cumulative Budget Share')
# # #         axes_g[0].legend(facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=8)
# # #         axes_g[1].hist(df['budget_per_person'], bins=12, color=BLUE, edgecolor=DARK_BG, linewidth=0.5, alpha=0.85)
# # #         axes_g[1].axvline(df['budget_per_person'].mean(), color=AMBER, linestyle='--', linewidth=1.5, label=f"Mean: KES {int(df['budget_per_person'].mean()):,}")
# # #         axes_g[1].axvline(df['budget_per_person'].median(), color=GREEN, linestyle='--', linewidth=1.5, label=f"Median: KES {int(df['budget_per_person'].median()):,}")
# # #         axes_g[1].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
# # #         axes_g[1].set_title('Budget/Person Distribution', fontsize=11, fontweight='bold')
# # #         axes_g[1].set_xlabel('KES per Person'); axes_g[1].set_ylabel('Number of Counties')
# # #         axes_g[1].legend(facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=8)
# # #         plt.tight_layout(); st.pyplot(fig_g); plt.close()

# # #     st.markdown('<div class="section-header">Correlation Analysis</div>', unsafe_allow_html=True)
# # #     col_c1, col_c2 = st.columns(2)
# # #     with col_c1: st.markdown(f'<div class="metric-card"><div class="metric-label">Population vs Absolute Budget</div><div class="metric-value metric-accent-green">r = {corr_bp:.3f}</div></div>', unsafe_allow_html=True)
# # #     with col_c2: st.markdown(f'<div class="metric-card"><div class="metric-label">Population vs Budget Per Person</div><div class="metric-value metric-accent-red">r = {corr_bpp:.3f}</div></div>', unsafe_allow_html=True)

# # #     colors_scatter = [REGION_COLORS[r] for r in df['region']]
# # #     fig_c, axes_c = plt.subplots(1, 2, figsize=(16, 5)); style_chart(fig_c, axes_c)
# # #     axes_c[0].scatter(df['population_2024']/1e6, df['budget_billion'], c=colors_scatter, s=70, alpha=0.85, edgecolors='#1e2d4a', linewidth=0.6)
# # #     m, b, *_ = stats.linregress(df['population_2024']/1e6, df['budget_billion'])
# # #     x_line = np.linspace(df['population_2024'].min()/1e6, df['population_2024'].max()/1e6, 100)
# # #     axes_c[0].plot(x_line, m*x_line+b, color=AMBER, linewidth=1.8, linestyle='--')
# # #     for _, row in df.iterrows():
# # #         if row['county'] in ['Nairobi','Lamu','Nakuru','Kiambu','Turkana']:
# # #             axes_c[0].annotate(row['county'], (row['population_2024']/1e6, row['budget_billion']), textcoords='offset points', xytext=(6,4), fontsize=7.5, color=TEXT)
# # #     legend_patches = [mpatches.Patch(color=v, label=k) for k, v in REGION_COLORS.items()]
# # #     axes_c[0].legend(handles=legend_patches, facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=7, ncol=2, loc='upper left')
# # #     axes_c[0].set_title('Population vs Absolute Budget', fontsize=11, fontweight='bold')
# # #     axes_c[0].set_xlabel('Population (millions)'); axes_c[0].set_ylabel('Budget (KES Billions)')
# # #     axes_c[1].scatter(df['population_2024']/1e6, df['budget_per_person'], c=colors_scatter, s=70, alpha=0.85, edgecolors='#1e2d4a', linewidth=0.6)
# # #     m2, b2, *_ = stats.linregress(df['population_2024']/1e6, df['budget_per_person'])
# # #     axes_c[1].plot(x_line, m2*x_line+b2, color=AMBER, linewidth=1.8, linestyle='--', label=f'r = {corr_bpp:.3f}')
# # #     for _, row in df.iterrows():
# # #         if row['county'] in ['Nairobi','Lamu','Nakuru','Kiambu','Marsabit']:
# # #             axes_c[1].annotate(row['county'], (row['population_2024']/1e6, row['budget_per_person']), textcoords='offset points', xytext=(6,4), fontsize=7.5, color=TEXT)
# # #     axes_c[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
# # #     axes_c[1].set_title('Population vs Budget Per Person', fontsize=11, fontweight='bold')
# # #     axes_c[1].set_xlabel('Population (millions)'); axes_c[1].set_ylabel('Budget Per Person (KES)')
# # #     axes_c[1].legend(facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=9)
# # #     plt.tight_layout(); st.pyplot(fig_c); plt.close()
# # #     st.markdown(f'<div class="insight-box">📌 <strong>Key finding:</strong> Larger counties receive significantly <em>less</em> per person (r = {corr_bpp:.3f}, p &lt; 0.001). The equitable share formula disproportionately benefits low-population counties like Lamu, Marsabit and Samburu, while high-density counties like Nairobi, Kiambu and Nakuru receive the least per citizen.</div>', unsafe_allow_html=True)

# # # # ── QUINTILE ──────────────────────────────────────────────────────────────────
# # # elif "Quintile" in section:
# # #     st.markdown('<div class="section-header">Quintile Analysis</div>', unsafe_allow_html=True)
# # #     df_q = df.copy()
# # #     df_q['quintile'] = pd.qcut(df_q['budget_per_person'], q=5, labels=['Q1 Bottom 20%','Q2','Q3 Middle','Q4','Q5 Top 20%'])
# # #     quintile_summary = df_q.groupby('quintile', observed=True).agg(counties=('county','count'), avg_bpp=('budget_per_person','mean'), counties_list=('county', lambda x: ', '.join(sorted(x)))).reset_index()
# # #     quintile_colors = [RED, '#f97316', AMBER, '#84cc16', GREEN]
# # #     fig_q, axes_q = plt.subplots(1, 2, figsize=(16, 5)); style_chart(fig_q, axes_q)
# # #     axes_q[0].bar(quintile_summary['quintile'], quintile_summary['avg_bpp'], color=quintile_colors, edgecolor=DARK_BG, linewidth=0.4)
# # #     axes_q[0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
# # #     axes_q[0].set_title('Average Budget Per Person by Quintile', fontsize=11, fontweight='bold')
# # #     axes_q[0].set_ylabel('KES per Person'); axes_q[0].tick_params(axis='x', labelsize=8, colors=TEXT)
# # #     region_order = regional['region'].tolist()
# # #     region_data = [df[df['region'] == r]['budget_per_person'].values for r in region_order]
# # #     bp = axes_q[1].boxplot(region_data, tick_labels=region_order, patch_artist=True, vert=True)
# # #     for patch, region in zip(bp['boxes'], region_order):
# # #         patch.set_facecolor(REGION_COLORS[region]); patch.set_alpha(0.7)
# # #     for element in ['whiskers','caps','medians','fliers']:
# # #         for item in bp[element]: item.set_color(TEXT)
# # #     axes_q[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
# # #     axes_q[1].set_title('Budget/Person Distribution by Region', fontsize=11, fontweight='bold')
# # #     axes_q[1].set_ylabel('KES per Person'); axes_q[1].tick_params(axis='x', rotation=30, labelsize=8, colors=TEXT)
# # #     plt.tight_layout(); st.pyplot(fig_q); plt.close()

# # #     st.markdown('<div class="section-header">Counties by Quintile</div>', unsafe_allow_html=True)
# # #     for i, (_, row) in enumerate(quintile_summary.iterrows()):
# # #         color = quintile_colors[i]
# # #         st.markdown(f'<div class="insight-box" style="border-left-color:{color}"><strong style="color:{color}">{row["quintile"]}</strong> &nbsp;·&nbsp; Avg: KES {int(row["avg_bpp"]):,}/person &nbsp;·&nbsp; {int(row["counties"])} counties<br><span style="color:#7a8aaa">{row["counties_list"]}</span></div>', unsafe_allow_html=True)

# # # # ── COUNTY EXPLORER ───────────────────────────────────────────────────────────
# # # elif "Explorer" in section:
# # #     st.markdown('<div class="section-header">County Explorer</div>', unsafe_allow_html=True)
# # #     col_s, col_info = st.columns([1, 2])
# # #     with col_s:
# # #         selected = st.selectbox('Select a County', options=sorted(df['county'].tolist()))
# # #     with col_info:
# # #         row = df[df['county'] == selected].iloc[0]
# # #         rank = sorted_df[sorted_df['county'] == selected].index[0] + 1
# # #         nat_avg = int(df['budget_per_person'].mean())
# # #         diff = int(row['budget_per_person']) - nat_avg
# # #         diff_str = f"+KES {diff:,}" if diff > 0 else f"-KES {abs(diff):,}"
# # #         diff_color = "metric-accent-green" if diff > 0 else "metric-accent-red"
# # #         reg_avg = int(regional[regional['region'] == row['region']]['budget_per_person'].values[0])
# # #         ca, cb2, cc, cd = st.columns(4)
# # #         with ca: st.markdown(f'<div class="metric-card"><div class="metric-label">Population</div><div class="metric-value" style="font-size:1.3rem">{int(row["population_2024"]):,}</div></div>', unsafe_allow_html=True)
# # #         with cb2: st.markdown(f'<div class="metric-card"><div class="metric-label">Budget</div><div class="metric-value" style="font-size:1.3rem">KES {row["budget_billion"]}B</div></div>', unsafe_allow_html=True)
# # #         with cc: st.markdown(f'<div class="metric-card"><div class="metric-label">Per Person · Rank #{rank}</div><div class="metric-value {diff_color}" style="font-size:1.3rem">KES {int(row["budget_per_person"]):,}</div></div>', unsafe_allow_html=True)
# # #         with cd: st.markdown(f'<div class="metric-card"><div class="metric-label">Region ({row["region"]})</div><div class="metric-value" style="font-size:1.3rem">KES {reg_avg:,}</div></div>', unsafe_allow_html=True)
# # #         st.markdown(f'<div class="insight-box"><strong>{selected}</strong> is ranked <strong>#{rank} of 47</strong> counties by budget per person. It is <strong>{diff_str}</strong> vs the national average of KES {nat_avg:,}/person, and sits in the <strong>{row["region"]}</strong> region (regional avg: KES {reg_avg:,}/person).</div>', unsafe_allow_html=True)

# # # # ── FULL RANKINGS ─────────────────────────────────────────────────────────────
# # # elif "Rankings" in section:
# # #     st.markdown('<div class="section-header">Full County Rankings</div>', unsafe_allow_html=True)
# # #     region_filter = st.multiselect('Filter by Region', options=sorted(df['region'].unique()), default=sorted(df['region'].unique()))
# # #     filtered = sorted_df[sorted_df['region'].isin(region_filter)]
# # #     table = filtered[['county','region','population_2024','budget_billion','budget_per_person']].copy()
# # #     table.columns = ['County','Region','Population (2024)','Budget (KES B)','Budget/Person (KES)']
# # #     table = table.reset_index(drop=True); table.index += 1
# # #     st.dataframe(table, use_container_width=True, height=600)
# # #     csv = table.to_csv().encode('utf-8')
# # #     st.download_button("⬇ Download as CSV", csv, "kenya_county_budget.csv", "text/csv")

# # # # ── COUNTY COMPARISON ─────────────────────────────────────────────────────────
# # # elif "Comparison" in section:
# # #     st.markdown('<div class="badge">Side-by-Side County Analysis</div>', unsafe_allow_html=True)
# # #     st.markdown('<div class="hero-title" style="font-size:2rem;">🔀 County Comparison Tool</div>', unsafe_allow_html=True)
# # #     st.markdown('<div class="hero-sub">Pick any two counties and compare their budgets, poverty, health and education stats</div>', unsafe_allow_html=True)

# # #     col_pick1, col_pick2 = st.columns(2)
# # #     county_list = sorted(df['county'].tolist())
# # #     with col_pick1:
# # #         c1_name = st.selectbox('County A', county_list, index=county_list.index('Nairobi'))
# # #     with col_pick2:
# # #         c2_name = st.selectbox('County B', county_list, index=county_list.index('Turkana'))

# # #     r1 = df[df['county'] == c1_name].iloc[0]
# # #     r2 = df[df['county'] == c2_name].iloc[0]
# # #     rank1 = sorted_df[sorted_df['county'] == c1_name].index[0] + 1
# # #     rank2 = sorted_df[sorted_df['county'] == c2_name].index[0] + 1

# # #     # ── Metric cards side by side ──
# # #     st.markdown('<div class="section-header">Key Metrics</div>', unsafe_allow_html=True)
# # #     METRICS = [
# # #         ("Budget / Person", f"KES {int(r1['budget_per_person']):,}", f"KES {int(r2['budget_per_person']):,}", "budget_per_person"),
# # #         ("Total Budget", f"KES {r1['budget_billion']}B", f"KES {r2['budget_billion']}B", "budget_billion"),
# # #         ("Population", f"{int(r1['population_2024']):,}", f"{int(r2['population_2024']):,}", "population_2024"),
# # #         ("Poverty Rate", f"{r1['poverty_rate_2022']}%", f"{r2['poverty_rate_2022']}%", "poverty_rate_2022"),
# # #         ("Pop Density", f"{int(r1['pop_density'])} /km²", f"{int(r2['pop_density'])} /km²", "pop_density"),
# # #         ("Health Facilities", f"{int(r1['health_facilities'])}", f"{int(r2['health_facilities'])}", "health_facilities"),
# # #         ("Schools per 10k", f"{r1['schools_per_10k']}", f"{r2['schools_per_10k']}", "schools_per_10k"),
# # #         ("Own Source Revenue", f"KES {r1['own_source_revenue']}B ({r1['osr_pct']}%)", f"KES {r2['own_source_revenue']}B ({r2['osr_pct']}%)", "own_source_revenue"),
# # #     ]

# # #     hdr_l, hdr_m, hdr_r = st.columns([2,2,2])
# # #     with hdr_l: st.markdown(f'<div style="font-family:Syne,sans-serif;font-size:1.1rem;font-weight:800;color:#3b82f6;text-align:center;padding:0.8rem;background:#111827;border-radius:8px;margin-bottom:0.5rem;">🔵 {c1_name}<br><span style="font-size:0.75rem;color:#7a8aaa;font-weight:400;">Rank #{rank1} of 47 · {r1["region"]}</span></div>', unsafe_allow_html=True)
# # #     with hdr_m: st.markdown(f'<div style="font-family:Syne,sans-serif;font-size:0.8rem;font-weight:600;color:#7a8aaa;text-align:center;padding:0.8rem;">METRIC</div>', unsafe_allow_html=True)
# # #     with hdr_r: st.markdown(f'<div style="font-family:Syne,sans-serif;font-size:1.1rem;font-weight:800;color:#f97316;text-align:center;padding:0.8rem;background:#111827;border-radius:8px;margin-bottom:0.5rem;">🟠 {c2_name}<br><span style="font-size:0.75rem;color:#7a8aaa;font-weight:400;">Rank #{rank2} of 47 · {r2["region"]}</span></div>', unsafe_allow_html=True)

# # #     for label, v1, v2, col in METRICS:
# # #         val1 = r1[col]; val2 = r2[col]
# # #         better_1 = val1 > val2 if col not in ['poverty_rate_2022'] else val1 < val2
# # #         c1_style = "color:#10b981;font-weight:700;" if better_1 else "color:#e8eaf0;"
# # #         c2_style = "color:#10b981;font-weight:700;" if not better_1 else "color:#e8eaf0;"
# # #         cl, cm, cr = st.columns([2,2,2])
# # #         with cl: st.markdown(f'<div style="background:#111827;border:1px solid #1e2d4a;border-radius:8px;padding:0.7rem 1rem;text-align:center;margin-bottom:0.4rem;{c1_style}font-size:1rem;">{v1}</div>', unsafe_allow_html=True)
# # #         with cm: st.markdown(f'<div style="text-align:center;padding:0.7rem;color:#5a6a8a;font-size:0.78rem;text-transform:uppercase;letter-spacing:0.08em;">{label}</div>', unsafe_allow_html=True)
# # #         with cr: st.markdown(f'<div style="background:#111827;border:1px solid #1e2d4a;border-radius:8px;padding:0.7rem 1rem;text-align:center;margin-bottom:0.4rem;{c2_style}font-size:1rem;">{v2}</div>', unsafe_allow_html=True)

# # #     # ── Bar chart comparison ──
# # #     st.markdown('<div class="section-header">Visual Comparison</div>', unsafe_allow_html=True)
# # #     compare_metrics = {
# # #         'Budget/Person (KES)':   ('budget_per_person', 1),
# # #         'Poverty Rate (%)':      ('poverty_rate_2022', 1),
# # #         'Health Facilities':     ('health_facilities', 1),
# # #         'Schools per 10k':       ('schools_per_10k', 1),
# # #         'Pop Density (/km²)':    ('pop_density', 1),
# # #         'Own Source Rev (KES B)':('own_source_revenue', 1),
# # #     }
# # #     labels = list(compare_metrics.keys())
# # #     def norm(col): 
# # #         mx = df[col].max()
# # #         return (r1[col]/mx*100, r2[col]/mx*100)

# # #     fig_cmp, axes_cmp = plt.subplots(2, 3, figsize=(16, 7))
# # #     style_chart(fig_cmp, axes_cmp.flatten())
# # #     for ax, (label, (col, _)) in zip(axes_cmp.flatten(), compare_metrics.items()):
# # #         vals = [r1[col], r2[col]]
# # #         names = [c1_name, c2_name]
# # #         bars = ax.bar(names, vals, color=['#3b82f6','#f97316'], edgecolor=DARK_BG, linewidth=0.4, width=0.5)
# # #         ax.set_title(label, fontsize=9, fontweight='bold', color=TEXT)
# # #         ax.tick_params(axis='x', labelsize=8, colors=TEXT)
# # #         for bar, val in zip(bars, vals):
# # #             ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()*1.02,
# # #                     f'{val:,.1f}', ha='center', va='bottom', fontsize=8, color=TEXT)
# # #     plt.tight_layout()
# # #     st.pyplot(fig_cmp); plt.close()

# # #     # ── Insight box ──
# # #     bpp_diff = abs(int(r1['budget_per_person']) - int(r2['budget_per_person']))
# # #     pov_diff = abs(r1['poverty_rate_2022'] - r2['poverty_rate_2022'])
# # #     winner_budget = c1_name if r1['budget_per_person'] > r2['budget_per_person'] else c2_name
# # #     higher_poverty = c1_name if r1['poverty_rate_2022'] > r2['poverty_rate_2022'] else c2_name
# # #     st.markdown(f'''<div class="insight-box">
# # #         💡 <strong>{winner_budget}</strong> receives <strong>KES {bpp_diff:,} more</strong> per person than {c2_name if winner_budget==c1_name else c1_name}.
# # #         &nbsp;·&nbsp; <strong>{higher_poverty}</strong> has a higher poverty rate by <strong>{pov_diff:.1f}%</strong>.
# # #         &nbsp;·&nbsp; <strong>{c1_name if r1["health_facilities"]>r2["health_facilities"] else c2_name}</strong> has more health facilities
# # #         ({max(int(r1["health_facilities"]),int(r2["health_facilities"]))} vs {min(int(r1["health_facilities"]),int(r2["health_facilities"]))}).
# # #     </div>''', unsafe_allow_html=True)

# # # # ── BUDGET TRENDS ─────────────────────────────────────────────────────────────
# # # elif "Trends" in section:
# # #     st.markdown('<div class="badge">FY 2019/20 → FY 2023/24</div>', unsafe_allow_html=True)
# # #     st.markdown('<div class="hero-title" style="font-size:2rem;">📈 Budget Trends</div>', unsafe_allow_html=True)
# # #     st.markdown('<div class="hero-sub">Equitable share growth over 5 financial years — real FY 2023/24 data, prior years from CRA allocations</div>', unsafe_allow_html=True)

# # #     FY_COLS = ['budget_fy1920','budget_fy2021','budget_fy2122','budget_fy2223','budget_billion']
# # #     FY_LABELS = ['FY 2019/20','FY 2020/21','FY 2021/22','FY 2022/23','FY 2023/24']
# # #     NATIONAL_TOTALS = [316.5, 316.5, 370.0, 370.0, 389.1]

# # #     # ── National trend ──
# # #     st.markdown('<div class="section-header">National Equitable Share Trend</div>', unsafe_allow_html=True)
# # #     fig_nat, ax_nat = plt.subplots(figsize=(14, 4))
# # #     style_chart(fig_nat, ax_nat)
# # #     ax_nat.plot(FY_LABELS, NATIONAL_TOTALS, color=BLUE, linewidth=3, marker='o', markersize=9, markerfacecolor=AMBER, markeredgecolor=DARK_BG, markeredgewidth=1.5)
# # #     for x, y in zip(FY_LABELS, NATIONAL_TOTALS):
# # #         ax_nat.annotate(f'KES {y}B', (x, y), textcoords='offset points', xytext=(0, 12), ha='center', fontsize=9, color=TEXT, fontweight='bold')
# # #     ax_nat.fill_between(FY_LABELS, NATIONAL_TOTALS, alpha=0.08, color=BLUE)
# # #     ax_nat.set_title('Total National Equitable Share to All 47 Counties', fontsize=11, fontweight='bold')
# # #     ax_nat.set_ylabel('KES Billions'); ax_nat.set_ylim(280, 420)
# # #     ax_nat.tick_params(axis='x', colors=TEXT); ax_nat.tick_params(axis='y', colors=MUTED)
# # #     growth = ((NATIONAL_TOTALS[-1] - NATIONAL_TOTALS[0]) / NATIONAL_TOTALS[0] * 100)
# # #     ax_nat.annotate(f'+{growth:.1f}% over 5 years', xy=(FY_LABELS[-1], NATIONAL_TOTALS[-1]),
# # #                     xytext=(-120, -30), textcoords='offset points',
# # #                     fontsize=9, color=GREEN, fontweight='bold',
# # #                     arrowprops=dict(arrowstyle='->', color=GREEN, lw=1.5))
# # #     plt.tight_layout(); st.pyplot(fig_nat); plt.close()

# # #     # ── County trend selector ──
# # #     st.markdown('<div class="section-header">County-Level Budget Trend</div>', unsafe_allow_html=True)
# # #     sel_counties = st.multiselect('Select counties to compare (max 6)', 
# # #                                    options=sorted(df['county'].tolist()),
# # #                                    default=['Nairobi','Turkana','Lamu','Kiambu','Mandera'])
# # #     if sel_counties:
# # #         sel_counties = sel_counties[:6]
# # #         fig_trend, ax_trend = plt.subplots(figsize=(14, 5))
# # #         style_chart(fig_trend, ax_trend)
# # #         palette = [BLUE, GREEN, AMBER, RED, '#8b5cf6', '#06b6d4']
# # #         for i, county in enumerate(sel_counties):
# # #             row = df[df['county'] == county].iloc[0]
# # #             vals = [row[c] for c in FY_COLS]
# # #             ax_trend.plot(FY_LABELS, vals, color=palette[i], linewidth=2.5, marker='o',
# # #                           markersize=7, label=county, markerfacecolor=DARK_BG, markeredgewidth=2)
# # #             ax_trend.annotate(f'  {county}', (FY_LABELS[-1], vals[-1]),
# # #                               fontsize=8, color=palette[i], va='center')
# # #         ax_trend.set_title('County Budget Allocation Trend (KES Billions)', fontsize=11, fontweight='bold')
# # #         ax_trend.set_ylabel('KES Billions')
# # #         ax_trend.legend(facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=8, loc='upper left')
# # #         ax_trend.tick_params(axis='x', colors=TEXT); ax_trend.tick_params(axis='y', colors=MUTED)
# # #         plt.tight_layout(); st.pyplot(fig_trend); plt.close()

# # #     # ── Budget per person trend ──
# # #     st.markdown('<div class="section-header">Budget Per Person Trend — Selected Counties</div>', unsafe_allow_html=True)
# # #     if sel_counties:
# # #         fig_bpp, ax_bpp = plt.subplots(figsize=(14, 5))
# # #         style_chart(fig_bpp, ax_bpp)
# # #         for i, county in enumerate(sel_counties):
# # #             row = df[df['county'] == county].iloc[0]
# # #             pop = row['population_2024']
# # #             bpp_vals = [(row[c] * 1e9 / pop) for c in FY_COLS]
# # #             ax_bpp.plot(FY_LABELS, bpp_vals, color=palette[i], linewidth=2.5, marker='s',
# # #                         markersize=6, label=county, markerfacecolor=DARK_BG, markeredgewidth=2)
# # #             ax_bpp.annotate(f'  {county}', (FY_LABELS[-1], bpp_vals[-1]),
# # #                             fontsize=8, color=palette[i], va='center')
# # #         nat_bpp = [t*1e9/df['population_2024'].sum() for t in NATIONAL_TOTALS]
# # #         ax_bpp.plot(FY_LABELS, nat_bpp, color=MUTED, linewidth=1.5, linestyle='--', label='National Avg')
# # #         ax_bpp.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
# # #         ax_bpp.set_title('Budget Per Person Trend (KES)', fontsize=11, fontweight='bold')
# # #         ax_bpp.set_ylabel('KES per Person')
# # #         ax_bpp.legend(facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=8, loc='upper left')
# # #         ax_bpp.tick_params(axis='x', colors=TEXT); ax_bpp.tick_params(axis='y', colors=MUTED)
# # #         plt.tight_layout(); st.pyplot(fig_bpp); plt.close()

# # #     # ── Top 5 fastest growing counties ──
# # #     st.markdown('<div class="section-header">Fastest Growing County Budgets (FY 19/20 → 23/24)</div>', unsafe_allow_html=True)
# # #     df['budget_growth_pct'] = ((df['budget_billion'] - df['budget_fy1920']) / df['budget_fy1920'] * 100).round(1)
# # #     top_growers = df.nlargest(10, 'budget_growth_pct')[['county','region','budget_fy1920','budget_billion','budget_growth_pct']]
# # #     fig_grw, ax_grw = plt.subplots(figsize=(14, 4))
# # #     style_chart(fig_grw, ax_grw)
# # #     colors_grw = [REGION_COLORS[r] for r in top_growers['region']]
# # #     ax_grw.barh(top_growers['county'], top_growers['budget_growth_pct'], color=colors_grw, edgecolor=DARK_BG, linewidth=0.4)
# # #     for i, (_, row) in enumerate(top_growers.iterrows()):
# # #         ax_grw.text(row['budget_growth_pct']+0.3, i, f"+{row['budget_growth_pct']}%", va='center', fontsize=8, color=TEXT)
# # #     legend_patches = [mpatches.Patch(color=v, label=k) for k, v in REGION_COLORS.items() if k in top_growers['region'].values]
# # #     ax_grw.legend(handles=legend_patches, facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=7, loc='lower right')
# # #     ax_grw.set_title('Top 10 Counties by Budget Growth % (5-Year)', fontsize=11, fontweight='bold')
# # #     ax_grw.set_xlabel('Growth %'); ax_grw.invert_yaxis()
# # #     ax_grw.tick_params(axis='y', labelsize=9, colors=TEXT)
# # #     plt.tight_layout(); st.pyplot(fig_grw); plt.close()

# # #     st.markdown(f'<div class="insight-box">📌 The national equitable share grew from <strong>KES 316.5B to KES 389.1B</strong> — a <strong>+{growth:.1f}% increase</strong> over 5 years. Note: FY 2019/20 and 2020/21 had the same allocation due to COVID-19 fiscal freeze. Growth resumed in FY 2021/22.</div>', unsafe_allow_html=True)

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

# # NAME_MAP = {
# #     'Tana River':     'Tana River',
# #     'Taita Taveta':   'Taita-Taveta',
# #     'Elgeyo Marakwet':'Elgeyo/Marakwet',
# #     "Murang'a":       'Muranga',
# #     'Trans Nzoia':    'Trans-Nzoia',
# #     'Homa Bay':       'Homa Bay',
# #     'Tharaka Nithi':  'Tharaka-Nithi',
# #     'West Pokot':     'West Pokot',
# #     'Uasin Gishu':    'Uasin Gishu',
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
# #         name = feature['properties'].get('COUNTY_NAM', '')
# #         if name:
# #             feature['properties']['COUNTY_NAM'] = name.strip().title()
# #     return geojson

# # df = load_data()
# # sorted_df = df.sort_values('budget_per_person', ascending=False).reset_index(drop=True)
# # regional = df.groupby('region').agg(counties=('county','count'), total_pop=('population_2024','sum'), total_budget=('budget_billion','sum')).reset_index()
# # regional['budget_per_person'] = ((regional['total_budget'] * 1e9) / regional['total_pop']).astype(int)
# # regional = regional.sort_values('budget_per_person', ascending=False)
# # gini = gini_coefficient(df['budget_per_person'])
# # corr_bpp, pval_bpp = stats.pearsonr(df['population_2024'], df['budget_per_person'])
# # corr_bp, _ = stats.pearsonr(df['population_2024'], df['budget_billion'])

# # top_county = sorted_df.iloc[0]; bot_county = sorted_df.iloc[-1]

# # SECTIONS = ["🏠 Home", "📊 Overview", "🗺️ Choropleth Map", "📍 Regional Analysis",
# #             "🔗 Correlation & Gini", "🎯 Quintile Analysis", "🔍 County Explorer",
# #             "🔀 County Comparison", "📈 Budget Trends", "📋 Full Rankings"]

# # # Resolve nav button clicks BEFORE sidebar renders
# # if "nav_target" in st.session_state:
# #     default_idx = SECTIONS.index(st.session_state["nav_target"]) if st.session_state["nav_target"] in SECTIONS else 0
# #     del st.session_state["nav_target"]
# # else:
# #     default_idx = 0

# # with st.sidebar:
# #     st.markdown('<div style="font-family:Syne,sans-serif;font-size:1.1rem;font-weight:800;color:#fff;margin-bottom:1rem;">🇰🇪 Navigation</div>', unsafe_allow_html=True)
# #     section = st.radio("Go to", SECTIONS, index=default_idx)
# #     st.markdown("---")
# #     st.markdown(f'<div style="color:{MUTED};font-size:0.75rem;">Data: KNBS 2024 Projections<br>Budget: FY 2023/24 Equitable Share<br>Counties: 47</div>', unsafe_allow_html=True)

# # # ── HOME PAGE ─────────────────────────────────────────────────────────────────
# # if "Home" in section:
# #     st.markdown('<div class="badge">FY 2023/24 · All 47 Counties</div>', unsafe_allow_html=True)
# #     st.markdown('<div class="hero-title">🇰🇪 Kenya County<br>Budget Analysis</div>', unsafe_allow_html=True)
# #     st.markdown('<div class="hero-sub">Equitable Share Allocations · KNBS 2024 Population Projections</div>', unsafe_allow_html=True)

# #     # ── 2-column metric grid ──
# #     st.markdown('<div class="section-header">Key Metrics</div>', unsafe_allow_html=True)
# #     m1, m2 = st.columns(2)
# #     m3, m4 = st.columns(2)
# #     with m1:
# #         st.markdown(f"""
# #         <div class="metric-card">
# #             <div class="metric-label">📊 National Avg Budget / Person</div>
# #             <div class="metric-value metric-accent-green">KES {int(df["budget_per_person"].mean()):,}</div>
# #             <div style="color:{MUTED};font-size:0.78rem;margin-top:0.5rem;">Total budget: KES {df["budget_billion"].sum():.1f}B &nbsp;·&nbsp; Population: {df["population_2024"].sum()/1e6:.1f}M</div>
# #         </div>""", unsafe_allow_html=True)
# #     with m2:
# #         st.markdown(f"""
# #         <div class="metric-card">
# #             <div class="metric-label">🏆 Highest Funded County</div>
# #             <div class="metric-value metric-accent-green" style="font-size:1.6rem;">{top_county["county"]}</div>
# #             <div style="color:#10b981;font-size:0.9rem;margin-top:0.5rem;font-weight:600;">KES {int(top_county["budget_per_person"]):,} per person &nbsp;·&nbsp; {top_county["region"]} Region</div>
# #         </div>""", unsafe_allow_html=True)
# #     with m3:
# #         st.markdown(f"""
# #         <div class="metric-card">
# #             <div class="metric-label">📉 Lowest Funded County</div>
# #             <div class="metric-value metric-accent-red" style="font-size:1.6rem;">{bot_county["county"]}</div>
# #             <div style="color:#ef4444;font-size:0.9rem;margin-top:0.5rem;font-weight:600;">KES {int(bot_county["budget_per_person"]):,} per person &nbsp;·&nbsp; {bot_county["region"]} Region</div>
# #         </div>""", unsafe_allow_html=True)
# #     with m4:
# #         inequality_level = "Low" if gini < 0.2 else "Moderate" if gini < 0.35 else "High"
# #         gap_x = int(top_county["budget_per_person"] / bot_county["budget_per_person"])
# #         st.markdown(f"""
# #         <div class="metric-card">
# #             <div class="metric-label">⚖️ Funding Inequality (Gini)</div>
# #             <div class="metric-value metric-accent-amber">{gini:.3f}</div>
# #             <div style="color:{MUTED};font-size:0.78rem;margin-top:0.5rem;">{inequality_level} inequality &nbsp;·&nbsp; Highest county gets <strong style="color:#f59e0b;">{gap_x}x</strong> more per person than lowest</div>
# #         </div>""", unsafe_allow_html=True)

# #     # ── Navigation buttons ──
# #     st.markdown('<div class="section-header">Explore the Dashboard</div>', unsafe_allow_html=True)
# #     NAV_ITEMS = [
# #         ("📊", "Overview",          "Bar charts of all 47 counties ranked by budget per person",      "Overview"),
# #         ("🗺️", "Choropleth Map",    "Interactive Kenya map colored by budget per citizen",            "Choropleth Map"),
# #         ("📍", "Regional Analysis", "Compare 8 regions — budgets, pie charts & spread",              "Regional Analysis"),
# #         ("🔗", "Correlation & Gini","Lorenz curve, Gini deep-dive & population scatter plots",       "Correlation & Gini"),
# #         ("🎯", "Quintile Analysis", "Counties grouped into 5 funding bands with regional boxplots",  "Quintile Analysis"),
# #         ("🔍", "County Explorer",   "Pick any county — budget, poverty, health & school stats",      "County Explorer"),
# #         ("🔀", "County Comparison", "Pick any 2 counties and compare them side by side",             "County Comparison"),
# #         ("📈", "Budget Trends",     "Budget growth FY 2019/20 → 2023/24 by county & national",      "Budget Trends"),
# #         ("📋", "Full Rankings",     "Filterable table of all 47 counties with CSV download",         "Full Rankings"),
# #     ]
# #     row1 = st.columns(3)
# #     row2 = st.columns(3)
# #     row3 = st.columns(3)
# #     rows = [row1[0], row1[1], row1[2], row2[0], row2[1], row2[2], row3[0], row3[1], row3[2]]
# #     for col, (icon, title, desc, key) in zip(rows, NAV_ITEMS):
# #         with col:
# #             st.markdown(f"""
# #             <div style="background:linear-gradient(135deg,#111827,#1a2340);border:1px solid #1e2d4a;
# #                         border-radius:12px;padding:1.2rem 1.3rem;margin-bottom:0.8rem;
# #                         transition:border-color 0.2s;">
# #                 <div style="font-size:1.6rem;margin-bottom:0.4rem;">{icon}</div>
# #                 <div style="font-family:Syne,sans-serif;font-size:0.95rem;font-weight:700;
# #                             color:#fff;margin-bottom:0.3rem;">{title}</div>
# #                 <div style="font-size:0.78rem;color:{MUTED};line-height:1.4;">{desc}</div>
# #             </div>""", unsafe_allow_html=True)
# #             if st.button(f"Open {title}", key=f"nav_{key}", use_container_width=True):
# #                 icon_map = {"Overview":"📊","Choropleth Map":"🗺️","Regional Analysis":"📍",
# #                             "Correlation & Gini":"🔗","Quintile Analysis":"🎯",
# #                             "County Explorer":"🔍","County Comparison":"🔀",
# #                             "Budget Trends":"📈","Full Rankings":"📋"}
# #                 st.session_state["nav_target"] = f"{icon_map[title]} {title}"
# #                 st.rerun()

# #     st.markdown(f"""
# #     <div class="insight-box" style="margin-top:1rem;">
# #         💡 <strong>Key finding:</strong> {top_county["county"]} receives <strong>KES {int(top_county["budget_per_person"]):,}/person</strong>
# #         — {gap_x}x more than {bot_county["county"]} which gets <strong>KES {int(bot_county["budget_per_person"]):,}/person</strong>.
# #         The Gini coefficient of <strong>{gini:.3f}</strong> reflects {inequality_level.lower()} inequality across all counties.
# #     </div>""", unsafe_allow_html=True)

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
# #         df_map = df.copy()
# #         df_map['county_mapped'] = df_map['county'].apply(lambda x: NAME_MAP.get(x, x))
# #         fig_map = px.choropleth(
# #             df_map,
# #             geojson=kenya_geojson,
# #             locations='county_mapped',
# #             featureidkey='properties.COUNTY_NAM',
# #             color='budget_per_person',
# #             color_continuous_scale='RdYlGn',
# #             hover_name='county',
# #             hover_data={
# #                 'county_mapped': False,
# #                 'budget_per_person': ':,',
# #                 'budget_billion': True,
# #                 'population_2024': ':,'
# #             },
# #             labels={
# #                 'budget_per_person': 'KES/Person',
# #                 'budget_billion': 'Budget (KES B)',
# #                 'population_2024': 'Population'
# #             },
# #         )
# #         fig_map.update_geos(fitbounds="locations", visible=False)
# #         fig_map.update_layout(
# #             paper_bgcolor='#0a0f1e', plot_bgcolor='#0a0f1e', font_color='#e8eaf0',
# #             coloraxis_colorbar=dict(
# #                 title=dict(text='KES/Person', font=dict(color='#e8eaf0')),
# #                 tickfont=dict(color='#e8eaf0'),
# #                 bgcolor='#111827',
# #                 outlinecolor='#1e2d4a',
# #             ),
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

# # # ── COUNTY COMPARISON ─────────────────────────────────────────────────────────
# # elif "Comparison" in section:
# #     st.markdown('<div class="badge">Side-by-Side County Analysis</div>', unsafe_allow_html=True)
# #     st.markdown('<div class="hero-title" style="font-size:2rem;">🔀 County Comparison Tool</div>', unsafe_allow_html=True)
# #     st.markdown('<div class="hero-sub">Pick any two counties and compare their budgets, poverty, health and education stats</div>', unsafe_allow_html=True)

# #     col_pick1, col_pick2 = st.columns(2)
# #     county_list = sorted(df['county'].tolist())
# #     with col_pick1:
# #         c1_name = st.selectbox('County A', county_list, index=county_list.index('Nairobi'))
# #     with col_pick2:
# #         c2_name = st.selectbox('County B', county_list, index=county_list.index('Turkana'))

# #     r1 = df[df['county'] == c1_name].iloc[0]
# #     r2 = df[df['county'] == c2_name].iloc[0]
# #     rank1 = sorted_df[sorted_df['county'] == c1_name].index[0] + 1
# #     rank2 = sorted_df[sorted_df['county'] == c2_name].index[0] + 1

# #     # ── Metric cards side by side ──
# #     st.markdown('<div class="section-header">Key Metrics</div>', unsafe_allow_html=True)
# #     METRICS = [
# #         ("Budget / Person", f"KES {int(r1['budget_per_person']):,}", f"KES {int(r2['budget_per_person']):,}", "budget_per_person"),
# #         ("Total Budget", f"KES {r1['budget_billion']}B", f"KES {r2['budget_billion']}B", "budget_billion"),
# #         ("Population", f"{int(r1['population_2024']):,}", f"{int(r2['population_2024']):,}", "population_2024"),
# #         ("Poverty Rate", f"{r1['poverty_rate_2022']}%", f"{r2['poverty_rate_2022']}%", "poverty_rate_2022"),
# #         ("Pop Density", f"{int(r1['pop_density'])} /km²", f"{int(r2['pop_density'])} /km²", "pop_density"),
# #         ("Health Facilities", f"{int(r1['health_facilities'])}", f"{int(r2['health_facilities'])}", "health_facilities"),
# #         ("Schools per 10k", f"{r1['schools_per_10k']}", f"{r2['schools_per_10k']}", "schools_per_10k"),
# #         ("Own Source Revenue", f"KES {r1['own_source_revenue']}B ({r1['osr_pct']}%)", f"KES {r2['own_source_revenue']}B ({r2['osr_pct']}%)", "own_source_revenue"),
# #     ]

# #     hdr_l, hdr_m, hdr_r = st.columns([2,2,2])
# #     with hdr_l: st.markdown(f'<div style="font-family:Syne,sans-serif;font-size:1.1rem;font-weight:800;color:#3b82f6;text-align:center;padding:0.8rem;background:#111827;border-radius:8px;margin-bottom:0.5rem;">🔵 {c1_name}<br><span style="font-size:0.75rem;color:#7a8aaa;font-weight:400;">Rank #{rank1} of 47 · {r1["region"]}</span></div>', unsafe_allow_html=True)
# #     with hdr_m: st.markdown(f'<div style="font-family:Syne,sans-serif;font-size:0.8rem;font-weight:600;color:#7a8aaa;text-align:center;padding:0.8rem;">METRIC</div>', unsafe_allow_html=True)
# #     with hdr_r: st.markdown(f'<div style="font-family:Syne,sans-serif;font-size:1.1rem;font-weight:800;color:#f97316;text-align:center;padding:0.8rem;background:#111827;border-radius:8px;margin-bottom:0.5rem;">🟠 {c2_name}<br><span style="font-size:0.75rem;color:#7a8aaa;font-weight:400;">Rank #{rank2} of 47 · {r2["region"]}</span></div>', unsafe_allow_html=True)

# #     for label, v1, v2, col in METRICS:
# #         val1 = r1[col]; val2 = r2[col]
# #         better_1 = val1 > val2 if col not in ['poverty_rate_2022'] else val1 < val2
# #         c1_style = "color:#10b981;font-weight:700;" if better_1 else "color:#e8eaf0;"
# #         c2_style = "color:#10b981;font-weight:700;" if not better_1 else "color:#e8eaf0;"
# #         cl, cm, cr = st.columns([2,2,2])
# #         with cl: st.markdown(f'<div style="background:#111827;border:1px solid #1e2d4a;border-radius:8px;padding:0.7rem 1rem;text-align:center;margin-bottom:0.4rem;{c1_style}font-size:1rem;">{v1}</div>', unsafe_allow_html=True)
# #         with cm: st.markdown(f'<div style="text-align:center;padding:0.7rem;color:#5a6a8a;font-size:0.78rem;text-transform:uppercase;letter-spacing:0.08em;">{label}</div>', unsafe_allow_html=True)
# #         with cr: st.markdown(f'<div style="background:#111827;border:1px solid #1e2d4a;border-radius:8px;padding:0.7rem 1rem;text-align:center;margin-bottom:0.4rem;{c2_style}font-size:1rem;">{v2}</div>', unsafe_allow_html=True)

# #     # ── Bar chart comparison ──
# #     st.markdown('<div class="section-header">Visual Comparison</div>', unsafe_allow_html=True)
# #     compare_metrics = {
# #         'Budget/Person (KES)':   ('budget_per_person', 1),
# #         'Poverty Rate (%)':      ('poverty_rate_2022', 1),
# #         'Health Facilities':     ('health_facilities', 1),
# #         'Schools per 10k':       ('schools_per_10k', 1),
# #         'Pop Density (/km²)':    ('pop_density', 1),
# #         'Own Source Rev (KES B)':('own_source_revenue', 1),
# #     }
# #     labels = list(compare_metrics.keys())
# #     def norm(col): 
# #         mx = df[col].max()
# #         return (r1[col]/mx*100, r2[col]/mx*100)

# #     fig_cmp, axes_cmp = plt.subplots(2, 3, figsize=(16, 7))
# #     style_chart(fig_cmp, axes_cmp.flatten())
# #     for ax, (label, (col, _)) in zip(axes_cmp.flatten(), compare_metrics.items()):
# #         vals = [r1[col], r2[col]]
# #         names = [c1_name, c2_name]
# #         bars = ax.bar(names, vals, color=['#3b82f6','#f97316'], edgecolor=DARK_BG, linewidth=0.4, width=0.5)
# #         ax.set_title(label, fontsize=9, fontweight='bold', color=TEXT)
# #         ax.tick_params(axis='x', labelsize=8, colors=TEXT)
# #         for bar, val in zip(bars, vals):
# #             ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()*1.02,
# #                     f'{val:,.1f}', ha='center', va='bottom', fontsize=8, color=TEXT)
# #     plt.tight_layout()
# #     st.pyplot(fig_cmp); plt.close()

# #     # ── Insight box ──
# #     bpp_diff = abs(int(r1['budget_per_person']) - int(r2['budget_per_person']))
# #     pov_diff = abs(r1['poverty_rate_2022'] - r2['poverty_rate_2022'])
# #     winner_budget = c1_name if r1['budget_per_person'] > r2['budget_per_person'] else c2_name
# #     higher_poverty = c1_name if r1['poverty_rate_2022'] > r2['poverty_rate_2022'] else c2_name
# #     st.markdown(f'''<div class="insight-box">
# #         💡 <strong>{winner_budget}</strong> receives <strong>KES {bpp_diff:,} more</strong> per person than {c2_name if winner_budget==c1_name else c1_name}.
# #         &nbsp;·&nbsp; <strong>{higher_poverty}</strong> has a higher poverty rate by <strong>{pov_diff:.1f}%</strong>.
# #         &nbsp;·&nbsp; <strong>{c1_name if r1["health_facilities"]>r2["health_facilities"] else c2_name}</strong> has more health facilities
# #         ({max(int(r1["health_facilities"]),int(r2["health_facilities"]))} vs {min(int(r1["health_facilities"]),int(r2["health_facilities"]))}).
# #     </div>''', unsafe_allow_html=True)

# # # ── BUDGET TRENDS ─────────────────────────────────────────────────────────────
# # elif "Trends" in section:
# #     st.markdown('<div class="badge">FY 2019/20 → FY 2023/24</div>', unsafe_allow_html=True)
# #     st.markdown('<div class="hero-title" style="font-size:2rem;">📈 Budget Trends</div>', unsafe_allow_html=True)
# #     st.markdown('<div class="hero-sub">Equitable share growth over 5 financial years — real FY 2023/24 data, prior years from CRA allocations</div>', unsafe_allow_html=True)

# #     FY_COLS = ['budget_fy1920','budget_fy2021','budget_fy2122','budget_fy2223','budget_billion']
# #     FY_LABELS = ['FY 2019/20','FY 2020/21','FY 2021/22','FY 2022/23','FY 2023/24']
# #     NATIONAL_TOTALS = [316.5, 316.5, 370.0, 370.0, 389.1]

# #     # ── National trend ──
# #     st.markdown('<div class="section-header">National Equitable Share Trend</div>', unsafe_allow_html=True)
# #     fig_nat, ax_nat = plt.subplots(figsize=(14, 4))
# #     style_chart(fig_nat, ax_nat)
# #     ax_nat.plot(FY_LABELS, NATIONAL_TOTALS, color=BLUE, linewidth=3, marker='o', markersize=9, markerfacecolor=AMBER, markeredgecolor=DARK_BG, markeredgewidth=1.5)
# #     for x, y in zip(FY_LABELS, NATIONAL_TOTALS):
# #         ax_nat.annotate(f'KES {y}B', (x, y), textcoords='offset points', xytext=(0, 12), ha='center', fontsize=9, color=TEXT, fontweight='bold')
# #     ax_nat.fill_between(FY_LABELS, NATIONAL_TOTALS, alpha=0.08, color=BLUE)
# #     ax_nat.set_title('Total National Equitable Share to All 47 Counties', fontsize=11, fontweight='bold')
# #     ax_nat.set_ylabel('KES Billions'); ax_nat.set_ylim(280, 420)
# #     ax_nat.tick_params(axis='x', colors=TEXT); ax_nat.tick_params(axis='y', colors=MUTED)
# #     growth = ((NATIONAL_TOTALS[-1] - NATIONAL_TOTALS[0]) / NATIONAL_TOTALS[0] * 100)
# #     ax_nat.annotate(f'+{growth:.1f}% over 5 years', xy=(FY_LABELS[-1], NATIONAL_TOTALS[-1]),
# #                     xytext=(-120, -30), textcoords='offset points',
# #                     fontsize=9, color=GREEN, fontweight='bold',
# #                     arrowprops=dict(arrowstyle='->', color=GREEN, lw=1.5))
# #     plt.tight_layout(); st.pyplot(fig_nat); plt.close()

# #     # ── County trend selector ──
# #     st.markdown('<div class="section-header">County-Level Budget Trend</div>', unsafe_allow_html=True)
# #     sel_counties = st.multiselect('Select counties to compare (max 6)', 
# #                                    options=sorted(df['county'].tolist()),
# #                                    default=['Nairobi','Turkana','Lamu','Kiambu','Mandera'])
# #     if sel_counties:
# #         sel_counties = sel_counties[:6]
# #         fig_trend, ax_trend = plt.subplots(figsize=(14, 5))
# #         style_chart(fig_trend, ax_trend)
# #         palette = [BLUE, GREEN, AMBER, RED, '#8b5cf6', '#06b6d4']
# #         for i, county in enumerate(sel_counties):
# #             row = df[df['county'] == county].iloc[0]
# #             vals = [row[c] for c in FY_COLS]
# #             ax_trend.plot(FY_LABELS, vals, color=palette[i], linewidth=2.5, marker='o',
# #                           markersize=7, label=county, markerfacecolor=DARK_BG, markeredgewidth=2)
# #             ax_trend.annotate(f'  {county}', (FY_LABELS[-1], vals[-1]),
# #                               fontsize=8, color=palette[i], va='center')
# #         ax_trend.set_title('County Budget Allocation Trend (KES Billions)', fontsize=11, fontweight='bold')
# #         ax_trend.set_ylabel('KES Billions')
# #         ax_trend.legend(facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=8, loc='upper left')
# #         ax_trend.tick_params(axis='x', colors=TEXT); ax_trend.tick_params(axis='y', colors=MUTED)
# #         plt.tight_layout(); st.pyplot(fig_trend); plt.close()

# #     # ── Budget per person trend ──
# #     st.markdown('<div class="section-header">Budget Per Person Trend — Selected Counties</div>', unsafe_allow_html=True)
# #     if sel_counties:
# #         fig_bpp, ax_bpp = plt.subplots(figsize=(14, 5))
# #         style_chart(fig_bpp, ax_bpp)
# #         for i, county in enumerate(sel_counties):
# #             row = df[df['county'] == county].iloc[0]
# #             pop = row['population_2024']
# #             bpp_vals = [(row[c] * 1e9 / pop) for c in FY_COLS]
# #             ax_bpp.plot(FY_LABELS, bpp_vals, color=palette[i], linewidth=2.5, marker='s',
# #                         markersize=6, label=county, markerfacecolor=DARK_BG, markeredgewidth=2)
# #             ax_bpp.annotate(f'  {county}', (FY_LABELS[-1], bpp_vals[-1]),
# #                             fontsize=8, color=palette[i], va='center')
# #         nat_bpp = [t*1e9/df['population_2024'].sum() for t in NATIONAL_TOTALS]
# #         ax_bpp.plot(FY_LABELS, nat_bpp, color=MUTED, linewidth=1.5, linestyle='--', label='National Avg')
# #         ax_bpp.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
# #         ax_bpp.set_title('Budget Per Person Trend (KES)', fontsize=11, fontweight='bold')
# #         ax_bpp.set_ylabel('KES per Person')
# #         ax_bpp.legend(facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=8, loc='upper left')
# #         ax_bpp.tick_params(axis='x', colors=TEXT); ax_bpp.tick_params(axis='y', colors=MUTED)
# #         plt.tight_layout(); st.pyplot(fig_bpp); plt.close()

# #     # ── Top 5 fastest growing counties ──
# #     st.markdown('<div class="section-header">Fastest Growing County Budgets (FY 19/20 → 23/24)</div>', unsafe_allow_html=True)
# #     df['budget_growth_pct'] = ((df['budget_billion'] - df['budget_fy1920']) / df['budget_fy1920'] * 100).round(1)
# #     top_growers = df.nlargest(10, 'budget_growth_pct')[['county','region','budget_fy1920','budget_billion','budget_growth_pct']]
# #     fig_grw, ax_grw = plt.subplots(figsize=(14, 4))
# #     style_chart(fig_grw, ax_grw)
# #     colors_grw = [REGION_COLORS[r] for r in top_growers['region']]
# #     ax_grw.barh(top_growers['county'], top_growers['budget_growth_pct'], color=colors_grw, edgecolor=DARK_BG, linewidth=0.4)
# #     for i, (_, row) in enumerate(top_growers.iterrows()):
# #         ax_grw.text(row['budget_growth_pct']+0.3, i, f"+{row['budget_growth_pct']}%", va='center', fontsize=8, color=TEXT)
# #     legend_patches = [mpatches.Patch(color=v, label=k) for k, v in REGION_COLORS.items() if k in top_growers['region'].values]
# #     ax_grw.legend(handles=legend_patches, facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=7, loc='lower right')
# #     ax_grw.set_title('Top 10 Counties by Budget Growth % (5-Year)', fontsize=11, fontweight='bold')
# #     ax_grw.set_xlabel('Growth %'); ax_grw.invert_yaxis()
# #     ax_grw.tick_params(axis='y', labelsize=9, colors=TEXT)
# #     plt.tight_layout(); st.pyplot(fig_grw); plt.close()

# #     st.markdown(f'<div class="insight-box">📌 The national equitable share grew from <strong>KES 316.5B to KES 389.1B</strong> — a <strong>+{growth:.1f}% increase</strong> over 5 years. Note: FY 2019/20 and 2020/21 had the same allocation due to COVID-19 fiscal freeze. Growth resumed in FY 2021/22.</div>', unsafe_allow_html=True)


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

# top_county = sorted_df.iloc[0]; bot_county = sorted_df.iloc[-1]

# SECTIONS = ["🏠 Home", "📊 Overview", "🗺️ Choropleth Map", "📍 Regional Analysis",
#             "🔗 Correlation & Gini", "🎯 Quintile Analysis", "🔍 County Explorer",
#             "🔀 County Comparison", "📈 Budget Trends", "📋 Full Rankings"]

# # Resolve nav button clicks BEFORE sidebar renders
# if "nav_target" in st.session_state:
#     default_idx = SECTIONS.index(st.session_state["nav_target"]) if st.session_state["nav_target"] in SECTIONS else 0
#     del st.session_state["nav_target"]
# else:
#     default_idx = 0

# with st.sidebar:
#     st.markdown('<div style="font-family:Syne,sans-serif;font-size:1.1rem;font-weight:800;color:#fff;margin-bottom:1rem;">🇰🇪 Navigation</div>', unsafe_allow_html=True)
#     section = st.radio("Go to", SECTIONS, index=default_idx)
#     st.markdown("---")
#     st.markdown(f'<div style="color:{MUTED};font-size:0.75rem;">Data: KNBS 2024 Projections<br>Budget: FY 2023/24 Equitable Share<br>Counties: 47</div>', unsafe_allow_html=True)

# # ── HOME PAGE ─────────────────────────────────────────────────────────────────
# if "Home" in section:
#     st.markdown('<div class="badge">FY 2023/24 · All 47 Counties</div>', unsafe_allow_html=True)
#     st.markdown('<div class="hero-title">🇰🇪 Kenya County<br>Budget Analysis</div>', unsafe_allow_html=True)
#     st.markdown('<div class="hero-sub">Equitable Share Allocations · KNBS 2024 Population Projections</div>', unsafe_allow_html=True)

#     # ── 2-column metric grid ──
#     st.markdown('<div class="section-header">Key Metrics</div>', unsafe_allow_html=True)
#     m1, m2 = st.columns(2)
#     m3, m4 = st.columns(2)
#     with m1:
#         st.markdown(f"""
#         <div class="metric-card">
#             <div class="metric-label">📊 National Avg Budget / Person</div>
#             <div class="metric-value metric-accent-green">KES {int(df["budget_per_person"].mean()):,}</div>
#             <div style="color:{MUTED};font-size:0.78rem;margin-top:0.5rem;">Total budget: KES {df["budget_billion"].sum():.1f}B &nbsp;·&nbsp; Population: {df["population_2024"].sum()/1e6:.1f}M</div>
#         </div>""", unsafe_allow_html=True)
#     with m2:
#         st.markdown(f"""
#         <div class="metric-card">
#             <div class="metric-label">🏆 Highest Funded County</div>
#             <div class="metric-value metric-accent-green" style="font-size:1.6rem;">{top_county["county"]}</div>
#             <div style="color:#10b981;font-size:0.9rem;margin-top:0.5rem;font-weight:600;">KES {int(top_county["budget_per_person"]):,} per person &nbsp;·&nbsp; {top_county["region"]} Region</div>
#         </div>""", unsafe_allow_html=True)
#     with m3:
#         st.markdown(f"""
#         <div class="metric-card">
#             <div class="metric-label">📉 Lowest Funded County</div>
#             <div class="metric-value metric-accent-red" style="font-size:1.6rem;">{bot_county["county"]}</div>
#             <div style="color:#ef4444;font-size:0.9rem;margin-top:0.5rem;font-weight:600;">KES {int(bot_county["budget_per_person"]):,} per person &nbsp;·&nbsp; {bot_county["region"]} Region</div>
#         </div>""", unsafe_allow_html=True)
#     with m4:
#         inequality_level = "Low" if gini < 0.2 else "Moderate" if gini < 0.35 else "High"
#         gap_x = int(top_county["budget_per_person"] / bot_county["budget_per_person"])
#         st.markdown(f"""
#         <div class="metric-card">
#             <div class="metric-label">⚖️ Funding Inequality (Gini)</div>
#             <div class="metric-value metric-accent-amber">{gini:.3f}</div>
#             <div style="color:{MUTED};font-size:0.78rem;margin-top:0.5rem;">{inequality_level} inequality &nbsp;·&nbsp; Highest county gets <strong style="color:#f59e0b;">{gap_x}x</strong> more per person than lowest</div>
#         </div>""", unsafe_allow_html=True)

#     # ── Navigation buttons ──
#     st.markdown('<div class="section-header">Explore the Dashboard</div>', unsafe_allow_html=True)
#     NAV_ITEMS = [
#         ("📊", "Overview",          "Bar charts of all 47 counties ranked by budget per person",      "Overview"),
#         ("🗺️", "Choropleth Map",    "Interactive Kenya map colored by budget per citizen",            "Choropleth Map"),
#         ("📍", "Regional Analysis", "Compare 8 regions — budgets, pie charts & spread",              "Regional Analysis"),
#         ("🔗", "Correlation & Gini","Lorenz curve, Gini deep-dive & population scatter plots",       "Correlation & Gini"),
#         ("🎯", "Quintile Analysis", "Counties grouped into 5 funding bands with regional boxplots",  "Quintile Analysis"),
#         ("🔍", "County Explorer",   "Pick any county — budget, poverty, health & school stats",      "County Explorer"),
#         ("🔀", "County Comparison", "Pick any 2 counties and compare them side by side",             "County Comparison"),
#         ("📈", "Budget Trends",     "Budget growth FY 2019/20 → 2023/24 by county & national",      "Budget Trends"),
#         ("📋", "Full Rankings",     "Filterable table of all 47 counties with CSV download",         "Full Rankings"),
#     ]
#     row1 = st.columns(3)
#     row2 = st.columns(3)
#     row3 = st.columns(3)
#     rows = [row1[0], row1[1], row1[2], row2[0], row2[1], row2[2], row3[0], row3[1], row3[2]]
#     for col, (icon, title, desc, key) in zip(rows, NAV_ITEMS):
#         with col:
#             st.markdown(f"""
#             <div style="background:linear-gradient(135deg,#111827,#1a2340);border:1px solid #1e2d4a;
#                         border-radius:12px;padding:1.2rem 1.3rem;margin-bottom:0.8rem;
#                         transition:border-color 0.2s;">
#                 <div style="font-size:1.6rem;margin-bottom:0.4rem;">{icon}</div>
#                 <div style="font-family:Syne,sans-serif;font-size:0.95rem;font-weight:700;
#                             color:#fff;margin-bottom:0.3rem;">{title}</div>
#                 <div style="font-size:0.78rem;color:{MUTED};line-height:1.4;">{desc}</div>
#             </div>""", unsafe_allow_html=True)
#             if st.button(f"Open {title}", key=f"nav_{key}", use_container_width=True):
#                 icon_map = {"Overview":"📊","Choropleth Map":"🗺️","Regional Analysis":"📍",
#                             "Correlation & Gini":"🔗","Quintile Analysis":"🎯",
#                             "County Explorer":"🔍","County Comparison":"🔀",
#                             "Budget Trends":"📈","Full Rankings":"📋"}
#                 st.session_state["nav_target"] = f"{icon_map[title]} {title}"
#                 st.rerun()

#     st.markdown(f"""
#     <div class="insight-box" style="margin-top:1rem;">
#         💡 <strong>Key finding:</strong> {top_county["county"]} receives <strong>KES {int(top_county["budget_per_person"]):,}/person</strong>
#         — {gap_x}x more than {bot_county["county"]} which gets <strong>KES {int(bot_county["budget_per_person"]):,}/person</strong>.
#         The Gini coefficient of <strong>{gini:.3f}</strong> reflects {inequality_level.lower()} inequality across all counties.
#     </div>""", unsafe_allow_html=True)

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
#     st.markdown('<div class="section-header">Kenya County Interactive Map</div>', unsafe_allow_html=True)

#     MAP_LAYERS = {
#         "💰 Budget Per Person":     ("budget_per_person",   "RdYlGn", "KES/Person"),
#         "📉 Poverty Rate (%)":      ("poverty_rate_2022",   "RdYlGn_r","Poverty %"),
#         "👥 Population Density":    ("pop_density",         "Blues",   "People/km²"),
#         "🏥 Health Facilities":     ("health_facilities",   "Greens",  "Facilities"),
#         "🏫 Schools per 10k":       ("schools_per_10k",     "Purples", "Schools/10k"),
#         "💵 Own Source Revenue":    ("own_source_revenue",  "Oranges", "KES Billions"),
#     }
#     layer_choice = st.radio("Map Layer", list(MAP_LAYERS.keys()), horizontal=True)
#     col_field, color_scale, cb_title = MAP_LAYERS[layer_choice]

#     try:
#         kenya_geojson = load_geojson()
#         df_map = df.copy()
#         df_map['county_mapped'] = df_map['county'].apply(lambda x: NAME_MAP.get(x, x))
#         fig_map = px.choropleth(
#             df_map,
#             geojson=kenya_geojson,
#             locations='county_mapped',
#             featureidkey='properties.COUNTY_NAM',
#             color=col_field,
#             color_continuous_scale=color_scale,
#             hover_name='county',
#             hover_data={
#                 'county_mapped': False,
#                 'budget_per_person': ':,',
#                 'poverty_rate_2022': True,
#                 'pop_density': True,
#                 'health_facilities': True,
#                 'population_2024': ':,'
#             },
#             labels={
#                 'budget_per_person': 'KES/Person',
#                 'poverty_rate_2022': 'Poverty %',
#                 'pop_density': 'Density/km²',
#                 'health_facilities': 'Health Facilities',
#                 'population_2024': 'Population'
#             },
#         )
#         fig_map.update_geos(fitbounds="locations", visible=False)
#         fig_map.update_layout(
#             paper_bgcolor='#0a0f1e', plot_bgcolor='#0a0f1e', font_color='#e8eaf0',
#             coloraxis_colorbar=dict(
#                 title=dict(text=cb_title, font=dict(color='#e8eaf0')),
#                 tickfont=dict(color='#e8eaf0'),
#                 bgcolor='#111827', outlinecolor='#1e2d4a',
#             ),
#             margin=dict(l=0, r=0, t=20, b=0), height=600
#         )
#         st.plotly_chart(fig_map, use_container_width=True)

#         # Layer-specific insight
#         insights = {
#             "💰 Budget Per Person":  "🟢 Green = higher budget per person · 🔴 Red = lower. Hover any county for full details.",
#             "📉 Poverty Rate (%)":   "🔴 Red = higher poverty rate · 🟢 Green = lower. Source: KNBS Poverty Report 2022.",
#             "👥 Population Density": "Darker blue = more densely populated. Nairobi leads at 6,318 people/km².",
#             "🏥 Health Facilities":  "Darker green = more health facilities. Includes hospitals, clinics and dispensaries.",
#             "🏫 Schools per 10k":    "Darker purple = more schools per 10,000 people. Source: KNBS County Abstracts 2023.",
#             "💵 Own Source Revenue": "Darker orange = higher own-source revenue (KES B). Shows county fiscal self-reliance.",
#         }
#         st.markdown(f'<div class="insight-box">📌 {insights[layer_choice]}</div>', unsafe_allow_html=True)
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
#     st.markdown('<div class="badge">Deep Dive</div>', unsafe_allow_html=True)
#     st.markdown('<div class="hero-title" style="font-size:2rem;">🔍 County Explorer</div>', unsafe_allow_html=True)
#     selected = st.selectbox('Select a County', options=sorted(df['county'].tolist()))
#     row = df[df['county'] == selected].iloc[0]
#     rank = sorted_df[sorted_df['county'] == selected].index[0] + 1
#     nat_avg = int(df['budget_per_person'].mean())
#     diff = int(row['budget_per_person']) - nat_avg
#     diff_str = f"+KES {diff:,}" if diff > 0 else f"-KES {abs(diff):,}"
#     diff_color = "metric-accent-green" if diff > 0 else "metric-accent-red"
#     reg_avg = int(regional[regional['region'] == row['region']]['budget_per_person'].values[0])

#     # Row 1 — Budget metrics
#     st.markdown('<div class="section-header">Budget & Finance</div>', unsafe_allow_html=True)
#     ca, cb2, cc, cd = st.columns(4)
#     with ca: st.markdown(f'<div class="metric-card"><div class="metric-label">Population 2024</div><div class="metric-value metric-accent">{int(row["population_2024"]):,}</div><div style="color:#7a8aaa;font-size:0.72rem;margin-top:0.3rem;">{int(row["pop_density"])} people/km²</div></div>', unsafe_allow_html=True)
#     with cb2: st.markdown(f'<div class="metric-card"><div class="metric-label">Total Budget</div><div class="metric-value">KES {row["budget_billion"]}B</div><div style="color:#7a8aaa;font-size:0.72rem;margin-top:0.3rem;">Own revenue: KES {row["own_source_revenue"]}B ({row["osr_pct"]}%)</div></div>', unsafe_allow_html=True)
#     with cc: st.markdown(f'<div class="metric-card"><div class="metric-label">Budget/Person · Rank #{rank}</div><div class="metric-value {diff_color}">KES {int(row["budget_per_person"]):,}</div><div style="color:#7a8aaa;font-size:0.72rem;margin-top:0.3rem;">{diff_str} vs national avg</div></div>', unsafe_allow_html=True)
#     with cd: st.markdown(f'<div class="metric-card"><div class="metric-label">Region · {row["region"]}</div><div class="metric-value">KES {reg_avg:,}</div><div style="color:#7a8aaa;font-size:0.72rem;margin-top:0.3rem;">Regional avg/person</div></div>', unsafe_allow_html=True)

#     # Row 2 — Development indicators
#     st.markdown('<div class="section-header">Development Indicators</div>', unsafe_allow_html=True)
#     d1, d2, d3, d4 = st.columns(4)
#     pov_nat = df["poverty_rate_2022"].mean()
#     pov_diff = row["poverty_rate_2022"] - pov_nat
#     pov_color = "metric-accent-red" if pov_diff > 0 else "metric-accent-green"
#     hlth_rank = df["health_facilities"].rank(ascending=False)[df["county"]==selected].values[0]
#     sch_rank = df["schools_per_10k"].rank(ascending=False)[df["county"]==selected].values[0]
#     with d1: st.markdown(f'<div class="metric-card"><div class="metric-label">Poverty Rate</div><div class="metric-value {pov_color}">{row["poverty_rate_2022"]}%</div><div style="color:#7a8aaa;font-size:0.72rem;margin-top:0.3rem;">National avg: {pov_nat:.1f}% · {("+" if pov_diff>0 else "")}{pov_diff:.1f}% vs avg</div></div>', unsafe_allow_html=True)
#     with d2: st.markdown(f'<div class="metric-card"><div class="metric-label">Health Facilities</div><div class="metric-value metric-accent-green">{int(row["health_facilities"])}</div><div style="color:#7a8aaa;font-size:0.72rem;margin-top:0.3rem;">Rank #{int(hlth_rank)} of 47 counties</div></div>', unsafe_allow_html=True)
#     with d3: st.markdown(f'<div class="metric-card"><div class="metric-label">Schools per 10k People</div><div class="metric-value metric-accent-amber">{row["schools_per_10k"]}</div><div style="color:#7a8aaa;font-size:0.72rem;margin-top:0.3rem;">Rank #{int(sch_rank)} of 47 counties</div></div>', unsafe_allow_html=True)
#     with d4: st.markdown(f'<div class="metric-card"><div class="metric-label">Land Area</div><div class="metric-value">{int(row["land_area_km2"]):,} km²</div><div style="color:#7a8aaa;font-size:0.72rem;margin-top:0.3rem;">{int(row["pop_density"])} people/km²</div></div>', unsafe_allow_html=True)

#     # Budget trend for this county
#     st.markdown('<div class="section-header">Budget Trend (5 Years)</div>', unsafe_allow_html=True)
#     FY_COLS = ["budget_fy1920","budget_fy2021","budget_fy2122","budget_fy2223","budget_billion"]
#     FY_LABELS = ["FY 19/20","FY 20/21","FY 21/22","FY 22/23","FY 23/24"]
#     county_vals = [row[c] for c in FY_COLS]
#     fig_exp, ax_exp = plt.subplots(figsize=(14, 3.5)); style_chart(fig_exp, ax_exp)
#     ax_exp.plot(FY_LABELS, county_vals, color=BLUE, linewidth=3, marker="o", markersize=9,
#                 markerfacecolor=AMBER, markeredgecolor=DARK_BG, markeredgewidth=1.5)
#     ax_exp.fill_between(FY_LABELS, county_vals, alpha=0.1, color=BLUE)
#     for x, y in zip(FY_LABELS, county_vals):
#         ax_exp.annotate(f"KES {y}B", (x, y), textcoords="offset points", xytext=(0,10),
#                         ha="center", fontsize=8.5, color=TEXT, fontweight="bold")
#     ax_exp.set_title(f"{selected} — Equitable Share Allocation Trend", fontsize=11, fontweight="bold")
#     ax_exp.set_ylabel("KES Billions"); ax_exp.tick_params(axis="x", colors=TEXT)
#     growth_pct = ((county_vals[-1]-county_vals[0])/county_vals[0]*100)
#     plt.tight_layout(); st.pyplot(fig_exp); plt.close()

#     st.markdown(f'''<div class="insight-box">
#         📌 <strong>{selected}</strong> is ranked <strong>#{rank} of 47</strong> by budget/person.
#         Budget grew <strong>+{growth_pct:.1f}%</strong> over 5 years (KES {county_vals[0]}B → KES {county_vals[-1]}B).
#         Poverty rate of <strong>{row["poverty_rate_2022"]}%</strong> is
#         <strong>{"above" if pov_diff > 0 else "below"} the national average</strong> by {abs(pov_diff):.1f}%.
#         The county has <strong>{int(row["health_facilities"])} health facilities</strong> and
#         <strong>{row["schools_per_10k"]} schools per 10,000</strong> people.
#     </div>''', unsafe_allow_html=True)

# # ── FULL RANKINGS ─────────────────────────────────────────────────────────────
# elif "Rankings" in section:
#     st.markdown('<div class="section-header">Full County Rankings</div>', unsafe_allow_html=True)
#     region_filter = st.multiselect('Filter by Region', options=sorted(df['region'].unique()), default=sorted(df['region'].unique()))
#     filtered = sorted_df[sorted_df['region'].isin(region_filter)]
#     table = filtered[['county','region','population_2024','budget_billion','budget_per_person','poverty_rate_2022','health_facilities','schools_per_10k','osr_pct']].copy()
#     table.columns = ['County','Region','Population (2024)','Budget (KES B)','Budget/Person (KES)','Poverty Rate (%)','Health Facilities','Schools/10k','Own Revenue (%)']
#     table = table.reset_index(drop=True); table.index += 1
#     st.dataframe(table, use_container_width=True, height=600)
#     csv = table.to_csv().encode('utf-8')
#     st.download_button("⬇ Download as CSV", csv, "kenya_county_budget.csv", "text/csv")

# # ── COUNTY COMPARISON ─────────────────────────────────────────────────────────
# elif "Comparison" in section:
#     st.markdown('<div class="badge">Side-by-Side County Analysis</div>', unsafe_allow_html=True)
#     st.markdown('<div class="hero-title" style="font-size:2rem;">🔀 County Comparison Tool</div>', unsafe_allow_html=True)
#     st.markdown('<div class="hero-sub">Pick any two counties and compare their budgets, poverty, health and education stats</div>', unsafe_allow_html=True)

#     col_pick1, col_pick2 = st.columns(2)
#     county_list = sorted(df['county'].tolist())
#     with col_pick1:
#         c1_name = st.selectbox('County A', county_list, index=county_list.index('Nairobi'))
#     with col_pick2:
#         c2_name = st.selectbox('County B', county_list, index=county_list.index('Turkana'))

#     r1 = df[df['county'] == c1_name].iloc[0]
#     r2 = df[df['county'] == c2_name].iloc[0]
#     rank1 = sorted_df[sorted_df['county'] == c1_name].index[0] + 1
#     rank2 = sorted_df[sorted_df['county'] == c2_name].index[0] + 1

#     # ── Metric cards side by side ──
#     st.markdown('<div class="section-header">Key Metrics</div>', unsafe_allow_html=True)
#     METRICS = [
#         ("Budget / Person", f"KES {int(r1['budget_per_person']):,}", f"KES {int(r2['budget_per_person']):,}", "budget_per_person"),
#         ("Total Budget", f"KES {r1['budget_billion']}B", f"KES {r2['budget_billion']}B", "budget_billion"),
#         ("Population", f"{int(r1['population_2024']):,}", f"{int(r2['population_2024']):,}", "population_2024"),
#         ("Poverty Rate", f"{r1['poverty_rate_2022']}%", f"{r2['poverty_rate_2022']}%", "poverty_rate_2022"),
#         ("Pop Density", f"{int(r1['pop_density'])} /km²", f"{int(r2['pop_density'])} /km²", "pop_density"),
#         ("Health Facilities", f"{int(r1['health_facilities'])}", f"{int(r2['health_facilities'])}", "health_facilities"),
#         ("Schools per 10k", f"{r1['schools_per_10k']}", f"{r2['schools_per_10k']}", "schools_per_10k"),
#         ("Own Source Revenue", f"KES {r1['own_source_revenue']}B ({r1['osr_pct']}%)", f"KES {r2['own_source_revenue']}B ({r2['osr_pct']}%)", "own_source_revenue"),
#     ]

#     hdr_l, hdr_m, hdr_r = st.columns([2,2,2])
#     with hdr_l: st.markdown(f'<div style="font-family:Syne,sans-serif;font-size:1.1rem;font-weight:800;color:#3b82f6;text-align:center;padding:0.8rem;background:#111827;border-radius:8px;margin-bottom:0.5rem;">🔵 {c1_name}<br><span style="font-size:0.75rem;color:#7a8aaa;font-weight:400;">Rank #{rank1} of 47 · {r1["region"]}</span></div>', unsafe_allow_html=True)
#     with hdr_m: st.markdown(f'<div style="font-family:Syne,sans-serif;font-size:0.8rem;font-weight:600;color:#7a8aaa;text-align:center;padding:0.8rem;">METRIC</div>', unsafe_allow_html=True)
#     with hdr_r: st.markdown(f'<div style="font-family:Syne,sans-serif;font-size:1.1rem;font-weight:800;color:#f97316;text-align:center;padding:0.8rem;background:#111827;border-radius:8px;margin-bottom:0.5rem;">🟠 {c2_name}<br><span style="font-size:0.75rem;color:#7a8aaa;font-weight:400;">Rank #{rank2} of 47 · {r2["region"]}</span></div>', unsafe_allow_html=True)

#     for label, v1, v2, col in METRICS:
#         val1 = r1[col]; val2 = r2[col]
#         better_1 = val1 > val2 if col not in ['poverty_rate_2022'] else val1 < val2
#         c1_style = "color:#10b981;font-weight:700;" if better_1 else "color:#e8eaf0;"
#         c2_style = "color:#10b981;font-weight:700;" if not better_1 else "color:#e8eaf0;"
#         cl, cm, cr = st.columns([2,2,2])
#         with cl: st.markdown(f'<div style="background:#111827;border:1px solid #1e2d4a;border-radius:8px;padding:0.7rem 1rem;text-align:center;margin-bottom:0.4rem;{c1_style}font-size:1rem;">{v1}</div>', unsafe_allow_html=True)
#         with cm: st.markdown(f'<div style="text-align:center;padding:0.7rem;color:#5a6a8a;font-size:0.78rem;text-transform:uppercase;letter-spacing:0.08em;">{label}</div>', unsafe_allow_html=True)
#         with cr: st.markdown(f'<div style="background:#111827;border:1px solid #1e2d4a;border-radius:8px;padding:0.7rem 1rem;text-align:center;margin-bottom:0.4rem;{c2_style}font-size:1rem;">{v2}</div>', unsafe_allow_html=True)

#     # ── Bar chart comparison ──
#     st.markdown('<div class="section-header">Visual Comparison</div>', unsafe_allow_html=True)
#     compare_metrics = {
#         'Budget/Person (KES)':   ('budget_per_person', 1),
#         'Poverty Rate (%)':      ('poverty_rate_2022', 1),
#         'Health Facilities':     ('health_facilities', 1),
#         'Schools per 10k':       ('schools_per_10k', 1),
#         'Pop Density (/km²)':    ('pop_density', 1),
#         'Own Source Rev (KES B)':('own_source_revenue', 1),
#     }
#     labels = list(compare_metrics.keys())
#     def norm(col): 
#         mx = df[col].max()
#         return (r1[col]/mx*100, r2[col]/mx*100)

#     fig_cmp, axes_cmp = plt.subplots(2, 3, figsize=(16, 7))
#     style_chart(fig_cmp, axes_cmp.flatten())
#     for ax, (label, (col, _)) in zip(axes_cmp.flatten(), compare_metrics.items()):
#         vals = [r1[col], r2[col]]
#         names = [c1_name, c2_name]
#         bars = ax.bar(names, vals, color=['#3b82f6','#f97316'], edgecolor=DARK_BG, linewidth=0.4, width=0.5)
#         ax.set_title(label, fontsize=9, fontweight='bold', color=TEXT)
#         ax.tick_params(axis='x', labelsize=8, colors=TEXT)
#         for bar, val in zip(bars, vals):
#             ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()*1.02,
#                     f'{val:,.1f}', ha='center', va='bottom', fontsize=8, color=TEXT)
#     plt.tight_layout()
#     st.pyplot(fig_cmp); plt.close()

#     # ── Insight box ──
#     bpp_diff = abs(int(r1['budget_per_person']) - int(r2['budget_per_person']))
#     pov_diff = abs(r1['poverty_rate_2022'] - r2['poverty_rate_2022'])
#     winner_budget = c1_name if r1['budget_per_person'] > r2['budget_per_person'] else c2_name
#     higher_poverty = c1_name if r1['poverty_rate_2022'] > r2['poverty_rate_2022'] else c2_name
#     st.markdown(f'''<div class="insight-box">
#         💡 <strong>{winner_budget}</strong> receives <strong>KES {bpp_diff:,} more</strong> per person than {c2_name if winner_budget==c1_name else c1_name}.
#         &nbsp;·&nbsp; <strong>{higher_poverty}</strong> has a higher poverty rate by <strong>{pov_diff:.1f}%</strong>.
#         &nbsp;·&nbsp; <strong>{c1_name if r1["health_facilities"]>r2["health_facilities"] else c2_name}</strong> has more health facilities
#         ({max(int(r1["health_facilities"]),int(r2["health_facilities"]))} vs {min(int(r1["health_facilities"]),int(r2["health_facilities"]))}).
#     </div>''', unsafe_allow_html=True)

# # ── BUDGET TRENDS ─────────────────────────────────────────────────────────────
# elif "Trends" in section:
#     st.markdown('<div class="badge">FY 2019/20 → FY 2023/24</div>', unsafe_allow_html=True)
#     st.markdown('<div class="hero-title" style="font-size:2rem;">📈 Budget Trends</div>', unsafe_allow_html=True)
#     st.markdown('<div class="hero-sub">Equitable share growth over 5 financial years — real FY 2023/24 data, prior years from CRA allocations</div>', unsafe_allow_html=True)

#     FY_COLS = ['budget_fy1920','budget_fy2021','budget_fy2122','budget_fy2223','budget_billion']
#     FY_LABELS = ['FY 2019/20','FY 2020/21','FY 2021/22','FY 2022/23','FY 2023/24']
#     NATIONAL_TOTALS = [316.5, 316.5, 370.0, 370.0, 389.1]

#     # ── National trend ──
#     st.markdown('<div class="section-header">National Equitable Share Trend</div>', unsafe_allow_html=True)
#     fig_nat, ax_nat = plt.subplots(figsize=(14, 4))
#     style_chart(fig_nat, ax_nat)
#     ax_nat.plot(FY_LABELS, NATIONAL_TOTALS, color=BLUE, linewidth=3, marker='o', markersize=9, markerfacecolor=AMBER, markeredgecolor=DARK_BG, markeredgewidth=1.5)
#     for x, y in zip(FY_LABELS, NATIONAL_TOTALS):
#         ax_nat.annotate(f'KES {y}B', (x, y), textcoords='offset points', xytext=(0, 12), ha='center', fontsize=9, color=TEXT, fontweight='bold')
#     ax_nat.fill_between(FY_LABELS, NATIONAL_TOTALS, alpha=0.08, color=BLUE)
#     ax_nat.set_title('Total National Equitable Share to All 47 Counties', fontsize=11, fontweight='bold')
#     ax_nat.set_ylabel('KES Billions'); ax_nat.set_ylim(280, 420)
#     ax_nat.tick_params(axis='x', colors=TEXT); ax_nat.tick_params(axis='y', colors=MUTED)
#     growth = ((NATIONAL_TOTALS[-1] - NATIONAL_TOTALS[0]) / NATIONAL_TOTALS[0] * 100)
#     ax_nat.annotate(f'+{growth:.1f}% over 5 years', xy=(FY_LABELS[-1], NATIONAL_TOTALS[-1]),
#                     xytext=(-120, -30), textcoords='offset points',
#                     fontsize=9, color=GREEN, fontweight='bold',
#                     arrowprops=dict(arrowstyle='->', color=GREEN, lw=1.5))
#     plt.tight_layout(); st.pyplot(fig_nat); plt.close()

#     # ── County trend selector ──
#     st.markdown('<div class="section-header">County-Level Budget Trend</div>', unsafe_allow_html=True)
#     sel_counties = st.multiselect('Select counties to compare (max 6)', 
#                                    options=sorted(df['county'].tolist()),
#                                    default=['Nairobi','Turkana','Lamu','Kiambu','Mandera'])
#     if sel_counties:
#         sel_counties = sel_counties[:6]
#         fig_trend, ax_trend = plt.subplots(figsize=(14, 5))
#         style_chart(fig_trend, ax_trend)
#         palette = [BLUE, GREEN, AMBER, RED, '#8b5cf6', '#06b6d4']
#         for i, county in enumerate(sel_counties):
#             row = df[df['county'] == county].iloc[0]
#             vals = [row[c] for c in FY_COLS]
#             ax_trend.plot(FY_LABELS, vals, color=palette[i], linewidth=2.5, marker='o',
#                           markersize=7, label=county, markerfacecolor=DARK_BG, markeredgewidth=2)
#             ax_trend.annotate(f'  {county}', (FY_LABELS[-1], vals[-1]),
#                               fontsize=8, color=palette[i], va='center')
#         ax_trend.set_title('County Budget Allocation Trend (KES Billions)', fontsize=11, fontweight='bold')
#         ax_trend.set_ylabel('KES Billions')
#         ax_trend.legend(facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=8, loc='upper left')
#         ax_trend.tick_params(axis='x', colors=TEXT); ax_trend.tick_params(axis='y', colors=MUTED)
#         plt.tight_layout(); st.pyplot(fig_trend); plt.close()

#     # ── Budget per person trend ──
#     st.markdown('<div class="section-header">Budget Per Person Trend — Selected Counties</div>', unsafe_allow_html=True)
#     if sel_counties:
#         fig_bpp, ax_bpp = plt.subplots(figsize=(14, 5))
#         style_chart(fig_bpp, ax_bpp)
#         for i, county in enumerate(sel_counties):
#             row = df[df['county'] == county].iloc[0]
#             pop = row['population_2024']
#             bpp_vals = [(row[c] * 1e9 / pop) for c in FY_COLS]
#             ax_bpp.plot(FY_LABELS, bpp_vals, color=palette[i], linewidth=2.5, marker='s',
#                         markersize=6, label=county, markerfacecolor=DARK_BG, markeredgewidth=2)
#             ax_bpp.annotate(f'  {county}', (FY_LABELS[-1], bpp_vals[-1]),
#                             fontsize=8, color=palette[i], va='center')
#         nat_bpp = [t*1e9/df['population_2024'].sum() for t in NATIONAL_TOTALS]
#         ax_bpp.plot(FY_LABELS, nat_bpp, color=MUTED, linewidth=1.5, linestyle='--', label='National Avg')
#         ax_bpp.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
#         ax_bpp.set_title('Budget Per Person Trend (KES)', fontsize=11, fontweight='bold')
#         ax_bpp.set_ylabel('KES per Person')
#         ax_bpp.legend(facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=8, loc='upper left')
#         ax_bpp.tick_params(axis='x', colors=TEXT); ax_bpp.tick_params(axis='y', colors=MUTED)
#         plt.tight_layout(); st.pyplot(fig_bpp); plt.close()

#     # ── Top 5 fastest growing counties ──
#     st.markdown('<div class="section-header">Fastest Growing County Budgets (FY 19/20 → 23/24)</div>', unsafe_allow_html=True)
#     df['budget_growth_pct'] = ((df['budget_billion'] - df['budget_fy1920']) / df['budget_fy1920'] * 100).round(1)
#     top_growers = df.nlargest(10, 'budget_growth_pct')[['county','region','budget_fy1920','budget_billion','budget_growth_pct']]
#     fig_grw, ax_grw = plt.subplots(figsize=(14, 4))
#     style_chart(fig_grw, ax_grw)
#     colors_grw = [REGION_COLORS[r] for r in top_growers['region']]
#     ax_grw.barh(top_growers['county'], top_growers['budget_growth_pct'], color=colors_grw, edgecolor=DARK_BG, linewidth=0.4)
#     for i, (_, row) in enumerate(top_growers.iterrows()):
#         ax_grw.text(row['budget_growth_pct']+0.3, i, f"+{row['budget_growth_pct']}%", va='center', fontsize=8, color=TEXT)
#     legend_patches = [mpatches.Patch(color=v, label=k) for k, v in REGION_COLORS.items() if k in top_growers['region'].values]
#     ax_grw.legend(handles=legend_patches, facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=7, loc='lower right')
#     ax_grw.set_title('Top 10 Counties by Budget Growth % (5-Year)', fontsize=11, fontweight='bold')
#     ax_grw.set_xlabel('Growth %'); ax_grw.invert_yaxis()
#     ax_grw.tick_params(axis='y', labelsize=9, colors=TEXT)
#     plt.tight_layout(); st.pyplot(fig_grw); plt.close()

#     st.markdown(f'<div class="insight-box">📌 The national equitable share grew from <strong>KES 316.5B to KES 389.1B</strong> — a <strong>+{growth:.1f}% increase</strong> over 5 years. Note: FY 2019/20 and 2020/21 had the same allocation due to COVID-19 fiscal freeze. Growth resumed in FY 2021/22.</div>', unsafe_allow_html=True)

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
            "🔗 Correlation & Gini", "🎯 Quintile Analysis", "🔍 County Explorer",
            "🔀 County Comparison", "📈 Budget Trends", "📋 Full Rankings"]

# ── Persistent section state — survives widget reruns on mobile ──
if "nav_target" in st.session_state:
    st.session_state["current_section"] = st.session_state.pop("nav_target")
if "current_section" not in st.session_state:
    st.session_state["current_section"] = "🏠 Home"

default_idx = SECTIONS.index(st.session_state["current_section"]) if st.session_state["current_section"] in SECTIONS else 0

with st.sidebar:
    st.markdown('<div style="font-family:Syne,sans-serif;font-size:1.1rem;font-weight:800;color:#fff;margin-bottom:1rem;">🇰🇪 Navigation</div>', unsafe_allow_html=True)
    section = st.radio("Go to", SECTIONS, index=default_idx, key="sidebar_radio")
    # Sync sidebar choice back to session state so it persists
    st.session_state["current_section"] = section
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
        ("🔍", "County Explorer",   "Pick any county — budget, poverty, health & school stats",      "County Explorer"),
        ("🔀", "County Comparison", "Pick any 2 counties and compare them side by side",             "County Comparison"),
        ("📈", "Budget Trends",     "Budget growth FY 2019/20 → 2023/24 by county & national",      "Budget Trends"),
        ("📋", "Full Rankings",     "Filterable table of all 47 counties with CSV download",         "Full Rankings"),
    ]
    row1 = st.columns(3)
    row2 = st.columns(3)
    row3 = st.columns(3)
    rows = [row1[0], row1[1], row1[2], row2[0], row2[1], row2[2], row3[0], row3[1], row3[2]]
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
                icon_map = {"Overview":"📊","Choropleth Map":"🗺️","Regional Analysis":"📍",
                            "Correlation & Gini":"🔗","Quintile Analysis":"🎯",
                            "County Explorer":"🔍","County Comparison":"🔀",
                            "Budget Trends":"📈","Full Rankings":"📋"}
                st.session_state["nav_target"] = f"{icon_map[title]} {title}"
                st.rerun()

    st.markdown(f"""
    <div class="insight-box" style="margin-top:1rem;">
        💡 <strong>Key finding:</strong> {top_county["county"]} receives <strong>KES {int(top_county["budget_per_person"]):,}/person</strong>
        — {gap_x}x more than {bot_county["county"]} which gets <strong>KES {int(bot_county["budget_per_person"]):,}/person</strong>.
        The Gini coefficient of <strong>{gini:.3f}</strong> reflects {inequality_level.lower()} inequality across all counties.
    </div>""", unsafe_allow_html=True)

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
    st.markdown('<div class="section-header">Kenya County Interactive Map</div>', unsafe_allow_html=True)

    MAP_LAYERS = {
        "💰 Budget Per Person":     ("budget_per_person",   "RdYlGn", "KES/Person"),
        "📉 Poverty Rate (%)":      ("poverty_rate_2022",   "RdYlGn_r","Poverty %"),
        "👥 Population Density":    ("pop_density",         "Blues",   "People/km²"),
        "🏥 Health Facilities":     ("health_facilities",   "Greens",  "Facilities"),
        "🏫 Schools per 10k":       ("schools_per_10k",     "Purples", "Schools/10k"),
        "💵 Own Source Revenue":    ("own_source_revenue",  "Oranges", "KES Billions"),
    }
    layer_choice = st.radio("Map Layer", list(MAP_LAYERS.keys()), horizontal=True)
    col_field, color_scale, cb_title = MAP_LAYERS[layer_choice]

    try:
        kenya_geojson = load_geojson()
        df_map = df.copy()
        df_map['county_mapped'] = df_map['county'].apply(lambda x: NAME_MAP.get(x, x))
        fig_map = px.choropleth(
            df_map,
            geojson=kenya_geojson,
            locations='county_mapped',
            featureidkey='properties.COUNTY_NAM',
            color=col_field,
            color_continuous_scale=color_scale,
            hover_name='county',
            hover_data={
                'county_mapped': False,
                'budget_per_person': ':,',
                'poverty_rate_2022': True,
                'pop_density': True,
                'health_facilities': True,
                'population_2024': ':,'
            },
            labels={
                'budget_per_person': 'KES/Person',
                'poverty_rate_2022': 'Poverty %',
                'pop_density': 'Density/km²',
                'health_facilities': 'Health Facilities',
                'population_2024': 'Population'
            },
        )
        fig_map.update_geos(fitbounds="locations", visible=False)
        fig_map.update_layout(
            paper_bgcolor='#0a0f1e', plot_bgcolor='#0a0f1e', font_color='#e8eaf0',
            coloraxis_colorbar=dict(
                title=dict(text=cb_title, font=dict(color='#e8eaf0')),
                tickfont=dict(color='#e8eaf0'),
                bgcolor='#111827', outlinecolor='#1e2d4a',
            ),
            margin=dict(l=0, r=0, t=20, b=0), height=600
        )
        st.plotly_chart(fig_map, use_container_width=True)

        # Layer-specific insight
        insights = {
            "💰 Budget Per Person":  "🟢 Green = higher budget per person · 🔴 Red = lower. Hover any county for full details.",
            "📉 Poverty Rate (%)":   "🔴 Red = higher poverty rate · 🟢 Green = lower. Source: KNBS Poverty Report 2022.",
            "👥 Population Density": "Darker blue = more densely populated. Nairobi leads at 6,318 people/km².",
            "🏥 Health Facilities":  "Darker green = more health facilities. Includes hospitals, clinics and dispensaries.",
            "🏫 Schools per 10k":    "Darker purple = more schools per 10,000 people. Source: KNBS County Abstracts 2023.",
            "💵 Own Source Revenue": "Darker orange = higher own-source revenue (KES B). Shows county fiscal self-reliance.",
        }
        st.markdown(f'<div class="insight-box">📌 {insights[layer_choice]}</div>', unsafe_allow_html=True)
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
    st.markdown('<div class="badge">Deep Dive</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-title" style="font-size:2rem;">🔍 County Explorer</div>', unsafe_allow_html=True)
    selected = st.selectbox('Select a County', options=sorted(df['county'].tolist()))
    row = df[df['county'] == selected].iloc[0]
    rank = sorted_df[sorted_df['county'] == selected].index[0] + 1
    nat_avg = int(df['budget_per_person'].mean())
    diff = int(row['budget_per_person']) - nat_avg
    diff_str = f"+KES {diff:,}" if diff > 0 else f"-KES {abs(diff):,}"
    diff_color = "metric-accent-green" if diff > 0 else "metric-accent-red"
    reg_avg = int(regional[regional['region'] == row['region']]['budget_per_person'].values[0])

    # Row 1 — Budget metrics
    st.markdown('<div class="section-header">Budget & Finance</div>', unsafe_allow_html=True)
    ca, cb2, cc, cd = st.columns(4)
    with ca: st.markdown(f'<div class="metric-card"><div class="metric-label">Population 2024</div><div class="metric-value metric-accent">{int(row["population_2024"]):,}</div><div style="color:#7a8aaa;font-size:0.72rem;margin-top:0.3rem;">{int(row["pop_density"])} people/km²</div></div>', unsafe_allow_html=True)
    with cb2: st.markdown(f'<div class="metric-card"><div class="metric-label">Total Budget</div><div class="metric-value">KES {row["budget_billion"]}B</div><div style="color:#7a8aaa;font-size:0.72rem;margin-top:0.3rem;">Own revenue: KES {row["own_source_revenue"]}B ({row["osr_pct"]}%)</div></div>', unsafe_allow_html=True)
    with cc: st.markdown(f'<div class="metric-card"><div class="metric-label">Budget/Person · Rank #{rank}</div><div class="metric-value {diff_color}">KES {int(row["budget_per_person"]):,}</div><div style="color:#7a8aaa;font-size:0.72rem;margin-top:0.3rem;">{diff_str} vs national avg</div></div>', unsafe_allow_html=True)
    with cd: st.markdown(f'<div class="metric-card"><div class="metric-label">Region · {row["region"]}</div><div class="metric-value">KES {reg_avg:,}</div><div style="color:#7a8aaa;font-size:0.72rem;margin-top:0.3rem;">Regional avg/person</div></div>', unsafe_allow_html=True)

    # Row 2 — Development indicators
    st.markdown('<div class="section-header">Development Indicators</div>', unsafe_allow_html=True)
    d1, d2, d3, d4 = st.columns(4)
    pov_nat = df["poverty_rate_2022"].mean()
    pov_diff = row["poverty_rate_2022"] - pov_nat
    pov_color = "metric-accent-red" if pov_diff > 0 else "metric-accent-green"
    hlth_rank = df["health_facilities"].rank(ascending=False)[df["county"]==selected].values[0]
    sch_rank = df["schools_per_10k"].rank(ascending=False)[df["county"]==selected].values[0]
    with d1: st.markdown(f'<div class="metric-card"><div class="metric-label">Poverty Rate</div><div class="metric-value {pov_color}">{row["poverty_rate_2022"]}%</div><div style="color:#7a8aaa;font-size:0.72rem;margin-top:0.3rem;">National avg: {pov_nat:.1f}% · {("+" if pov_diff>0 else "")}{pov_diff:.1f}% vs avg</div></div>', unsafe_allow_html=True)
    with d2: st.markdown(f'<div class="metric-card"><div class="metric-label">Health Facilities</div><div class="metric-value metric-accent-green">{int(row["health_facilities"])}</div><div style="color:#7a8aaa;font-size:0.72rem;margin-top:0.3rem;">Rank #{int(hlth_rank)} of 47 counties</div></div>', unsafe_allow_html=True)
    with d3: st.markdown(f'<div class="metric-card"><div class="metric-label">Schools per 10k People</div><div class="metric-value metric-accent-amber">{row["schools_per_10k"]}</div><div style="color:#7a8aaa;font-size:0.72rem;margin-top:0.3rem;">Rank #{int(sch_rank)} of 47 counties</div></div>', unsafe_allow_html=True)
    with d4: st.markdown(f'<div class="metric-card"><div class="metric-label">Land Area</div><div class="metric-value">{int(row["land_area_km2"]):,} km²</div><div style="color:#7a8aaa;font-size:0.72rem;margin-top:0.3rem;">{int(row["pop_density"])} people/km²</div></div>', unsafe_allow_html=True)

    # Budget trend for this county
    st.markdown('<div class="section-header">Budget Trend (5 Years)</div>', unsafe_allow_html=True)
    FY_COLS = ["budget_fy1920","budget_fy2021","budget_fy2122","budget_fy2223","budget_billion"]
    FY_LABELS = ["FY 19/20","FY 20/21","FY 21/22","FY 22/23","FY 23/24"]
    county_vals = [row[c] for c in FY_COLS]
    fig_exp, ax_exp = plt.subplots(figsize=(14, 3.5)); style_chart(fig_exp, ax_exp)
    ax_exp.plot(FY_LABELS, county_vals, color=BLUE, linewidth=3, marker="o", markersize=9,
                markerfacecolor=AMBER, markeredgecolor=DARK_BG, markeredgewidth=1.5)
    ax_exp.fill_between(FY_LABELS, county_vals, alpha=0.1, color=BLUE)
    for x, y in zip(FY_LABELS, county_vals):
        ax_exp.annotate(f"KES {y}B", (x, y), textcoords="offset points", xytext=(0,10),
                        ha="center", fontsize=8.5, color=TEXT, fontweight="bold")
    ax_exp.set_title(f"{selected} — Equitable Share Allocation Trend", fontsize=11, fontweight="bold")
    ax_exp.set_ylabel("KES Billions"); ax_exp.tick_params(axis="x", colors=TEXT)
    growth_pct = ((county_vals[-1]-county_vals[0])/county_vals[0]*100)
    plt.tight_layout(); st.pyplot(fig_exp); plt.close()

    st.markdown(f'''<div class="insight-box">
        📌 <strong>{selected}</strong> is ranked <strong>#{rank} of 47</strong> by budget/person.
        Budget grew <strong>+{growth_pct:.1f}%</strong> over 5 years (KES {county_vals[0]}B → KES {county_vals[-1]}B).
        Poverty rate of <strong>{row["poverty_rate_2022"]}%</strong> is
        <strong>{"above" if pov_diff > 0 else "below"} the national average</strong> by {abs(pov_diff):.1f}%.
        The county has <strong>{int(row["health_facilities"])} health facilities</strong> and
        <strong>{row["schools_per_10k"]} schools per 10,000</strong> people.
    </div>''', unsafe_allow_html=True)

# ── FULL RANKINGS ─────────────────────────────────────────────────────────────
elif "Rankings" in section:
    st.markdown('<div class="section-header">Full County Rankings</div>', unsafe_allow_html=True)
    region_filter = st.multiselect('Filter by Region', options=sorted(df['region'].unique()), default=sorted(df['region'].unique()))
    filtered = sorted_df[sorted_df['region'].isin(region_filter)]
    table = filtered[['county','region','population_2024','budget_billion','budget_per_person','poverty_rate_2022','health_facilities','schools_per_10k','osr_pct']].copy()
    table.columns = ['County','Region','Population (2024)','Budget (KES B)','Budget/Person (KES)','Poverty Rate (%)','Health Facilities','Schools/10k','Own Revenue (%)']
    table = table.reset_index(drop=True); table.index += 1
    st.dataframe(table, use_container_width=True, height=600)
    csv = table.to_csv().encode('utf-8')
    st.download_button("⬇ Download as CSV", csv, "kenya_county_budget.csv", "text/csv")

# ── COUNTY COMPARISON ─────────────────────────────────────────────────────────
elif "Comparison" in section:
    st.markdown('<div class="badge">Side-by-Side County Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-title" style="font-size:2rem;">🔀 County Comparison Tool</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Pick any two counties and compare their budgets, poverty, health and education stats</div>', unsafe_allow_html=True)

    col_pick1, col_pick2 = st.columns(2)
    county_list = sorted(df['county'].tolist())
    with col_pick1:
        c1_name = st.selectbox('County A', county_list, index=county_list.index('Nairobi'))
    with col_pick2:
        c2_name = st.selectbox('County B', county_list, index=county_list.index('Turkana'))

    r1 = df[df['county'] == c1_name].iloc[0]
    r2 = df[df['county'] == c2_name].iloc[0]
    rank1 = sorted_df[sorted_df['county'] == c1_name].index[0] + 1
    rank2 = sorted_df[sorted_df['county'] == c2_name].index[0] + 1

    # ── Metric cards side by side ──
    st.markdown('<div class="section-header">Key Metrics</div>', unsafe_allow_html=True)
    METRICS = [
        ("Budget / Person", f"KES {int(r1['budget_per_person']):,}", f"KES {int(r2['budget_per_person']):,}", "budget_per_person"),
        ("Total Budget", f"KES {r1['budget_billion']}B", f"KES {r2['budget_billion']}B", "budget_billion"),
        ("Population", f"{int(r1['population_2024']):,}", f"{int(r2['population_2024']):,}", "population_2024"),
        ("Poverty Rate", f"{r1['poverty_rate_2022']}%", f"{r2['poverty_rate_2022']}%", "poverty_rate_2022"),
        ("Pop Density", f"{int(r1['pop_density'])} /km²", f"{int(r2['pop_density'])} /km²", "pop_density"),
        ("Health Facilities", f"{int(r1['health_facilities'])}", f"{int(r2['health_facilities'])}", "health_facilities"),
        ("Schools per 10k", f"{r1['schools_per_10k']}", f"{r2['schools_per_10k']}", "schools_per_10k"),
        ("Own Source Revenue", f"KES {r1['own_source_revenue']}B ({r1['osr_pct']}%)", f"KES {r2['own_source_revenue']}B ({r2['osr_pct']}%)", "own_source_revenue"),
    ]

    hdr_l, hdr_m, hdr_r = st.columns([2,2,2])
    with hdr_l: st.markdown(f'<div style="font-family:Syne,sans-serif;font-size:1.1rem;font-weight:800;color:#3b82f6;text-align:center;padding:0.8rem;background:#111827;border-radius:8px;margin-bottom:0.5rem;">🔵 {c1_name}<br><span style="font-size:0.75rem;color:#7a8aaa;font-weight:400;">Rank #{rank1} of 47 · {r1["region"]}</span></div>', unsafe_allow_html=True)
    with hdr_m: st.markdown(f'<div style="font-family:Syne,sans-serif;font-size:0.8rem;font-weight:600;color:#7a8aaa;text-align:center;padding:0.8rem;">METRIC</div>', unsafe_allow_html=True)
    with hdr_r: st.markdown(f'<div style="font-family:Syne,sans-serif;font-size:1.1rem;font-weight:800;color:#f97316;text-align:center;padding:0.8rem;background:#111827;border-radius:8px;margin-bottom:0.5rem;">🟠 {c2_name}<br><span style="font-size:0.75rem;color:#7a8aaa;font-weight:400;">Rank #{rank2} of 47 · {r2["region"]}</span></div>', unsafe_allow_html=True)

    for label, v1, v2, col in METRICS:
        val1 = r1[col]; val2 = r2[col]
        better_1 = val1 > val2 if col not in ['poverty_rate_2022'] else val1 < val2
        c1_style = "color:#10b981;font-weight:700;" if better_1 else "color:#e8eaf0;"
        c2_style = "color:#10b981;font-weight:700;" if not better_1 else "color:#e8eaf0;"
        cl, cm, cr = st.columns([2,2,2])
        with cl: st.markdown(f'<div style="background:#111827;border:1px solid #1e2d4a;border-radius:8px;padding:0.7rem 1rem;text-align:center;margin-bottom:0.4rem;{c1_style}font-size:1rem;">{v1}</div>', unsafe_allow_html=True)
        with cm: st.markdown(f'<div style="text-align:center;padding:0.7rem;color:#5a6a8a;font-size:0.78rem;text-transform:uppercase;letter-spacing:0.08em;">{label}</div>', unsafe_allow_html=True)
        with cr: st.markdown(f'<div style="background:#111827;border:1px solid #1e2d4a;border-radius:8px;padding:0.7rem 1rem;text-align:center;margin-bottom:0.4rem;{c2_style}font-size:1rem;">{v2}</div>', unsafe_allow_html=True)

    # ── Bar chart comparison ──
    st.markdown('<div class="section-header">Visual Comparison</div>', unsafe_allow_html=True)
    compare_metrics = {
        'Budget/Person (KES)':   ('budget_per_person', 1),
        'Poverty Rate (%)':      ('poverty_rate_2022', 1),
        'Health Facilities':     ('health_facilities', 1),
        'Schools per 10k':       ('schools_per_10k', 1),
        'Pop Density (/km²)':    ('pop_density', 1),
        'Own Source Rev (KES B)':('own_source_revenue', 1),
    }
    labels = list(compare_metrics.keys())
    def norm(col): 
        mx = df[col].max()
        return (r1[col]/mx*100, r2[col]/mx*100)

    fig_cmp, axes_cmp = plt.subplots(2, 3, figsize=(16, 7))
    style_chart(fig_cmp, axes_cmp.flatten())
    for ax, (label, (col, _)) in zip(axes_cmp.flatten(), compare_metrics.items()):
        vals = [r1[col], r2[col]]
        names = [c1_name, c2_name]
        bars = ax.bar(names, vals, color=['#3b82f6','#f97316'], edgecolor=DARK_BG, linewidth=0.4, width=0.5)
        ax.set_title(label, fontsize=9, fontweight='bold', color=TEXT)
        ax.tick_params(axis='x', labelsize=8, colors=TEXT)
        for bar, val in zip(bars, vals):
            ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()*1.02,
                    f'{val:,.1f}', ha='center', va='bottom', fontsize=8, color=TEXT)
    plt.tight_layout()
    st.pyplot(fig_cmp); plt.close()

    # ── Insight box ──
    bpp_diff = abs(int(r1['budget_per_person']) - int(r2['budget_per_person']))
    pov_diff = abs(r1['poverty_rate_2022'] - r2['poverty_rate_2022'])
    winner_budget = c1_name if r1['budget_per_person'] > r2['budget_per_person'] else c2_name
    higher_poverty = c1_name if r1['poverty_rate_2022'] > r2['poverty_rate_2022'] else c2_name
    st.markdown(f'''<div class="insight-box">
        💡 <strong>{winner_budget}</strong> receives <strong>KES {bpp_diff:,} more</strong> per person than {c2_name if winner_budget==c1_name else c1_name}.
        &nbsp;·&nbsp; <strong>{higher_poverty}</strong> has a higher poverty rate by <strong>{pov_diff:.1f}%</strong>.
        &nbsp;·&nbsp; <strong>{c1_name if r1["health_facilities"]>r2["health_facilities"] else c2_name}</strong> has more health facilities
        ({max(int(r1["health_facilities"]),int(r2["health_facilities"]))} vs {min(int(r1["health_facilities"]),int(r2["health_facilities"]))}).
    </div>''', unsafe_allow_html=True)

# ── BUDGET TRENDS ─────────────────────────────────────────────────────────────
elif "Trends" in section:
    st.markdown('<div class="badge">FY 2019/20 → FY 2023/24</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-title" style="font-size:2rem;">📈 Budget Trends</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Equitable share growth over 5 financial years — real FY 2023/24 data, prior years from CRA allocations</div>', unsafe_allow_html=True)

    FY_COLS = ['budget_fy1920','budget_fy2021','budget_fy2122','budget_fy2223','budget_billion']
    FY_LABELS = ['FY 2019/20','FY 2020/21','FY 2021/22','FY 2022/23','FY 2023/24']
    NATIONAL_TOTALS = [316.5, 316.5, 370.0, 370.0, 389.1]

    # ── National trend ──
    st.markdown('<div class="section-header">National Equitable Share Trend</div>', unsafe_allow_html=True)
    fig_nat, ax_nat = plt.subplots(figsize=(14, 4))
    style_chart(fig_nat, ax_nat)
    ax_nat.plot(FY_LABELS, NATIONAL_TOTALS, color=BLUE, linewidth=3, marker='o', markersize=9, markerfacecolor=AMBER, markeredgecolor=DARK_BG, markeredgewidth=1.5)
    for x, y in zip(FY_LABELS, NATIONAL_TOTALS):
        ax_nat.annotate(f'KES {y}B', (x, y), textcoords='offset points', xytext=(0, 12), ha='center', fontsize=9, color=TEXT, fontweight='bold')
    ax_nat.fill_between(FY_LABELS, NATIONAL_TOTALS, alpha=0.08, color=BLUE)
    ax_nat.set_title('Total National Equitable Share to All 47 Counties', fontsize=11, fontweight='bold')
    ax_nat.set_ylabel('KES Billions'); ax_nat.set_ylim(280, 420)
    ax_nat.tick_params(axis='x', colors=TEXT); ax_nat.tick_params(axis='y', colors=MUTED)
    growth = ((NATIONAL_TOTALS[-1] - NATIONAL_TOTALS[0]) / NATIONAL_TOTALS[0] * 100)
    ax_nat.annotate(f'+{growth:.1f}% over 5 years', xy=(FY_LABELS[-1], NATIONAL_TOTALS[-1]),
                    xytext=(-120, -30), textcoords='offset points',
                    fontsize=9, color=GREEN, fontweight='bold',
                    arrowprops=dict(arrowstyle='->', color=GREEN, lw=1.5))
    plt.tight_layout(); st.pyplot(fig_nat); plt.close()

    # ── County trend selector ──
    st.markdown('<div class="section-header">County-Level Budget Trend</div>', unsafe_allow_html=True)
    sel_counties = st.multiselect('Select counties to compare (max 6)', 
                                   options=sorted(df['county'].tolist()),
                                   default=['Nairobi','Turkana','Lamu','Kiambu','Mandera'])
    if sel_counties:
        sel_counties = sel_counties[:6]
        fig_trend, ax_trend = plt.subplots(figsize=(14, 5))
        style_chart(fig_trend, ax_trend)
        palette = [BLUE, GREEN, AMBER, RED, '#8b5cf6', '#06b6d4']
        for i, county in enumerate(sel_counties):
            row = df[df['county'] == county].iloc[0]
            vals = [row[c] for c in FY_COLS]
            ax_trend.plot(FY_LABELS, vals, color=palette[i], linewidth=2.5, marker='o',
                          markersize=7, label=county, markerfacecolor=DARK_BG, markeredgewidth=2)
            ax_trend.annotate(f'  {county}', (FY_LABELS[-1], vals[-1]),
                              fontsize=8, color=palette[i], va='center')
        ax_trend.set_title('County Budget Allocation Trend (KES Billions)', fontsize=11, fontweight='bold')
        ax_trend.set_ylabel('KES Billions')
        ax_trend.legend(facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=8, loc='upper left')
        ax_trend.tick_params(axis='x', colors=TEXT); ax_trend.tick_params(axis='y', colors=MUTED)
        plt.tight_layout(); st.pyplot(fig_trend); plt.close()

    # ── Budget per person trend ──
    st.markdown('<div class="section-header">Budget Per Person Trend — Selected Counties</div>', unsafe_allow_html=True)
    if sel_counties:
        fig_bpp, ax_bpp = plt.subplots(figsize=(14, 5))
        style_chart(fig_bpp, ax_bpp)
        for i, county in enumerate(sel_counties):
            row = df[df['county'] == county].iloc[0]
            pop = row['population_2024']
            bpp_vals = [(row[c] * 1e9 / pop) for c in FY_COLS]
            ax_bpp.plot(FY_LABELS, bpp_vals, color=palette[i], linewidth=2.5, marker='s',
                        markersize=6, label=county, markerfacecolor=DARK_BG, markeredgewidth=2)
            ax_bpp.annotate(f'  {county}', (FY_LABELS[-1], bpp_vals[-1]),
                            fontsize=8, color=palette[i], va='center')
        nat_bpp = [t*1e9/df['population_2024'].sum() for t in NATIONAL_TOTALS]
        ax_bpp.plot(FY_LABELS, nat_bpp, color=MUTED, linewidth=1.5, linestyle='--', label='National Avg')
        ax_bpp.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
        ax_bpp.set_title('Budget Per Person Trend (KES)', fontsize=11, fontweight='bold')
        ax_bpp.set_ylabel('KES per Person')
        ax_bpp.legend(facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=8, loc='upper left')
        ax_bpp.tick_params(axis='x', colors=TEXT); ax_bpp.tick_params(axis='y', colors=MUTED)
        plt.tight_layout(); st.pyplot(fig_bpp); plt.close()

    # ── Top 5 fastest growing counties ──
    st.markdown('<div class="section-header">Fastest Growing County Budgets (FY 19/20 → 23/24)</div>', unsafe_allow_html=True)
    df['budget_growth_pct'] = ((df['budget_billion'] - df['budget_fy1920']) / df['budget_fy1920'] * 100).round(1)
    top_growers = df.nlargest(10, 'budget_growth_pct')[['county','region','budget_fy1920','budget_billion','budget_growth_pct']]
    fig_grw, ax_grw = plt.subplots(figsize=(14, 4))
    style_chart(fig_grw, ax_grw)
    colors_grw = [REGION_COLORS[r] for r in top_growers['region']]
    ax_grw.barh(top_growers['county'], top_growers['budget_growth_pct'], color=colors_grw, edgecolor=DARK_BG, linewidth=0.4)
    for i, (_, row) in enumerate(top_growers.iterrows()):
        ax_grw.text(row['budget_growth_pct']+0.3, i, f"+{row['budget_growth_pct']}%", va='center', fontsize=8, color=TEXT)
    legend_patches = [mpatches.Patch(color=v, label=k) for k, v in REGION_COLORS.items() if k in top_growers['region'].values]
    ax_grw.legend(handles=legend_patches, facecolor=CARD_BG, edgecolor='#1e2d4a', labelcolor=TEXT, fontsize=7, loc='lower right')
    ax_grw.set_title('Top 10 Counties by Budget Growth % (5-Year)', fontsize=11, fontweight='bold')
    ax_grw.set_xlabel('Growth %'); ax_grw.invert_yaxis()
    ax_grw.tick_params(axis='y', labelsize=9, colors=TEXT)
    plt.tight_layout(); st.pyplot(fig_grw); plt.close()

    st.markdown(f'<div class="insight-box">📌 The national equitable share grew from <strong>KES 316.5B to KES 389.1B</strong> — a <strong>+{growth:.1f}% increase</strong> over 5 years. Note: FY 2019/20 and 2020/21 had the same allocation due to COVID-19 fiscal freeze. Growth resumed in FY 2021/22.</div>', unsafe_allow_html=True)