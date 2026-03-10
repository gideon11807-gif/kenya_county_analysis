# # # # import pandas as pd
# # # # import matplotlib.pyplot as plt

# # # # # Step 4: Load dataset
# # # # df = pd.read_csv("../data/county_data.csv")

# # # # # Show first rows
# # # # print("Dataset Preview:")
# # # # print(df.head())

# # # # # Step 5: Calculate budget per person
# # # # df["budget_per_person"] = (df["budget_billion"] * 1000000000) / df["population"]

# # # # print("\nBudget Per Person:")
# # # # print(df[["county", "budget_per_person"]])

# # # # # Step 6: Find counties with highest funding per citizen
# # # # sorted_df = df.sort_values("budget_per_person", ascending=False)

# # # # print("\nCounties Ranked by Budget Per Person:")
# # # # print(sorted_df[["county", "budget_per_person"]])

# # # # # Step 7: Visualization
# # # # plt.figure(figsize=(10,5))
# # # # plt.bar(df["county"], df["budget_per_person"])
# # # # plt.xticks(rotation=45)
# # # # plt.title("County Budget Per Citizen")
# # # # plt.xlabel("County")
# # # # plt.ylabel("Budget Per Person")
# # # # plt.show()

# # # import pandas as pd
# # # import matplotlib.pyplot as plt

# # # df = pd.read_csv("../data/county_data.csv")

# # # df["budget_per_person"] = (df["budget_billion"] * 1000000000) / df["population"]

# # # sorted_df = df.sort_values("budget_per_person", ascending=False)

# # # plt.figure(figsize=(10,5))
# # # plt.bar(sorted_df["county"], sorted_df["budget_per_person"])
# # # plt.xticks(rotation=45)
# # # plt.title("County Budget Per Citizen")
# # # plt.xlabel("County")
# # # plt.ylabel("Budget Per Person")
# # # plt.show()

# # import pandas as pd
# # import matplotlib.pyplot as plt

# # # Load dataset
# # df = pd.read_csv("data/county_data.csv")

# # # Calculate budget per citizen
# # df["budget_per_person"] = (df["budget_billion"] * 1000000000) / df["population"]

# # # Sort counties
# # sorted_df = df.sort_values("budget_per_person", ascending=False)

# # # Chart
# # plt.figure(figsize=(10,5))
# # plt.bar(sorted_df["county"], sorted_df["budget_per_person"])
# # plt.xticks(rotation=45)

# # plt.title("County Budget Per Citizen")
# # plt.xlabel("County")
# # plt.ylabel("Budget Per Person")

# # plt.show()

# import pandas as pd
# import matplotlib.pyplot as plt
# import matplotlib.ticker as mticker

# # ── Load dataset ────────────────────────────────────────────────────────────
# df = pd.read_csv('data/county_data.csv')

# print(f'Counties loaded: {len(df)}')
# print(f'Total population: {df["population_2024"].sum():,}')
# print(f'Total budget: KES {df["budget_billion"].sum():.1f} billion')
# print(df.head())

# # ── Calculate budget per person ─────────────────────────────────────────────
# df['budget_per_person'] = (df['budget_billion'] * 1_000_000_000) / df['population_2024']
# df['budget_per_person'] = df['budget_per_person'].round(0).astype(int)

# sorted_df = df.sort_values('budget_per_person', ascending=False).reset_index(drop=True)

# print('\nTop 5 counties by budget per person:')
# print(sorted_df[['county', 'population_2024', 'budget_billion', 'budget_per_person']].head())
# print('\nBottom 5 counties by budget per person:')
# print(sorted_df[['county', 'population_2024', 'budget_billion', 'budget_per_person']].tail())

# # ── Chart 1: All 47 counties ranked ─────────────────────────────────────────
# fig, ax = plt.subplots(figsize=(18, 6))

# colors = ['#c0392b' if v > sorted_df['budget_per_person'].median() * 1.5
#           else '#2980b9' for v in sorted_df['budget_per_person']]

# ax.bar(sorted_df['county'], sorted_df['budget_per_person'], color=colors, edgecolor='white', linewidth=0.5)
# ax.set_title('Kenya County Budget Per Citizen — FY 2023/24 Equitable Share', fontsize=14, fontweight='bold', pad=15)
# ax.set_xlabel('County', fontsize=11)
# ax.set_ylabel('Budget Per Person (KES)', fontsize=11)
# ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
# ax.axhline(sorted_df['budget_per_person'].mean(), color='orange', linestyle='--', linewidth=1.5,
#            label=f'National Average: KES {int(sorted_df["budget_per_person"].mean()):,}')
# ax.legend(fontsize=10)
# plt.xticks(rotation=90, fontsize=8)
# plt.tight_layout()
# plt.savefig('../dashboards/budget_per_person.png', dpi=150, bbox_inches='tight')
# plt.show()
# print('Chart 1 saved.')

# # ── Chart 2: Top 10 vs Bottom 10 ────────────────────────────────────────────
# top10 = sorted_df.head(10)
# bot10 = sorted_df.tail(10).sort_values('budget_per_person')

# fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# ax1.barh(top10['county'], top10['budget_per_person'], color='#27ae60')
# ax1.set_title('Top 10 — Highest Budget Per Person', fontweight='bold')
# ax1.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
# ax1.set_xlabel('KES per Person')
# ax1.invert_yaxis()

# ax2.barh(bot10['county'], bot10['budget_per_person'], color='#e74c3c')
# ax2.set_title('Bottom 10 — Lowest Budget Per Person', fontweight='bold')
# ax2.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
# ax2.set_xlabel('KES per Person')
# ax2.invert_yaxis()

# plt.suptitle('Kenya County Budget Per Citizen — FY 2023/24', fontsize=13, fontweight='bold')
# plt.tight_layout()
# plt.savefig('../dashboards/top_bottom_10.png', dpi=150, bbox_inches='tight')
# plt.show()
# print('Chart 2 saved.')

# # ── Chart 3: Budget vs Population scatter ───────────────────────────────────
# fig, ax = plt.subplots(figsize=(12, 7))

# scatter = ax.scatter(
#     df['population_2024'] / 1_000_000,
#     df['budget_billion'],
#     c=df['budget_per_person'],
#     cmap='RdYlGn',
#     s=80, alpha=0.85, edgecolors='grey', linewidth=0.5
# )

# for _, row in df.iterrows():
#     if row['county'] in ['Nairobi', 'Lamu', 'Turkana', 'Nakuru', 'Kiambu', 'Kakamega', 'Mombasa']:
#         ax.annotate(row['county'], (row['population_2024'] / 1_000_000, row['budget_billion']),
#                     textcoords='offset points', xytext=(6, 4), fontsize=8)

# cb = plt.colorbar(scatter, ax=ax)
# cb.set_label('Budget Per Person (KES)', fontsize=10)
# ax.set_title('County Budget vs Population — FY 2023/24', fontsize=13, fontweight='bold')
# ax.set_xlabel('Population (millions)', fontsize=11)
# ax.set_ylabel('Budget (KES Billions)', fontsize=11)
# plt.tight_layout()
# plt.savefig('../dashboards/budget_vs_population.png', dpi=150, bbox_inches='tight')
# plt.show()
# print('Chart 3 saved.')

# # ── Summary table ────────────────────────────────────────────────────────────
# summary = df[['county', 'population_2024', 'budget_billion', 'budget_per_person']].copy()
# summary.columns = ['County', 'Population (2024)', 'Budget (KES B)', 'Budget/Person (KES)']
# summary = summary.sort_values('Budget/Person (KES)', ascending=False).reset_index(drop=True)
# summary.index += 1

# print(f"\n{'─'*60}")
# print(f"  KENYA COUNTY BUDGET ANALYSIS — FY 2023/24")
# print(f"{'─'*60}")
# print(f"  Total Population : {df['population_2024'].sum():>15,}")
# print(f"  Total Budget     : KES {df['budget_billion'].sum():>8.1f} billion")
# print(f"  National Average : KES {df['budget_per_person'].mean():>8,.0f} per person")
# print(f"  Highest          : {sorted_df.iloc[0]['county']} — KES {sorted_df.iloc[0]['budget_per_person']:,}")
# print(f"  Lowest           : {sorted_df.iloc[-1]['county']} — KES {sorted_df.iloc[-1]['budget_per_person']:,}")
# print(f"{'─'*60}\n")
# print(summary.to_string())

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# ── Load dataset ────────────────────────────────────────────────────────────
df = pd.read_csv('data/county_data.csv')

print(f'Counties loaded: {len(df)}')
print(f'Total population: {df["population_2024"].sum():,}')
print(f'Total budget: KES {df["budget_billion"].sum():.1f} billion')
print(df.head())

# ── Calculate budget per person ─────────────────────────────────────────────
df['budget_per_person'] = (df['budget_billion'] * 1_000_000_000) / df['population_2024']
df['budget_per_person'] = df['budget_per_person'].round(0).astype(int)

sorted_df = df.sort_values('budget_per_person', ascending=False).reset_index(drop=True)

print('\nTop 5 counties by budget per person:')
print(sorted_df[['county', 'population_2024', 'budget_billion', 'budget_per_person']].head())
print('\nBottom 5 counties by budget per person:')
print(sorted_df[['county', 'population_2024', 'budget_billion', 'budget_per_person']].tail())

# ── Chart 1: All 47 counties ranked ─────────────────────────────────────────
fig, ax = plt.subplots(figsize=(18, 6))

colors = ['#c0392b' if v > sorted_df['budget_per_person'].median() * 1.5
          else '#2980b9' for v in sorted_df['budget_per_person']]

ax.bar(sorted_df['county'], sorted_df['budget_per_person'], color=colors, edgecolor='white', linewidth=0.5)
ax.set_title('Kenya County Budget Per Citizen — FY 2023/24 Equitable Share', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('County', fontsize=11)
ax.set_ylabel('Budget Per Person (KES)', fontsize=11)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
ax.axhline(sorted_df['budget_per_person'].mean(), color='orange', linestyle='--', linewidth=1.5,
           label=f'National Average: KES {int(sorted_df["budget_per_person"].mean()):,}')
ax.legend(fontsize=10)
plt.xticks(rotation=90, fontsize=8)
plt.tight_layout()
plt.savefig('dashboards/budget_per_person.png', dpi=150, bbox_inches='tight')
plt.show()
print('Chart 1 saved.')

# ── Chart 2: Top 10 vs Bottom 10 ────────────────────────────────────────────
top10 = sorted_df.head(10)
bot10 = sorted_df.tail(10).sort_values('budget_per_person')

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

ax1.barh(top10['county'], top10['budget_per_person'], color='#27ae60')
ax1.set_title('Top 10 — Highest Budget Per Person', fontweight='bold')
ax1.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
ax1.set_xlabel('KES per Person')
ax1.invert_yaxis()

ax2.barh(bot10['county'], bot10['budget_per_person'], color='#e74c3c')
ax2.set_title('Bottom 10 — Lowest Budget Per Person', fontweight='bold')
ax2.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
ax2.set_xlabel('KES per Person')
ax2.invert_yaxis()

plt.suptitle('Kenya County Budget Per Citizen — FY 2023/24', fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('dashboards/top_bottom_10.png', dpi=150, bbox_inches='tight')
plt.show()
print('Chart 2 saved.')

# ── Chart 3: Budget vs Population scatter ───────────────────────────────────
fig, ax = plt.subplots(figsize=(12, 7))

scatter = ax.scatter(
    df['population_2024'] / 1_000_000,
    df['budget_billion'],
    c=df['budget_per_person'],
    cmap='RdYlGn',
    s=80, alpha=0.85, edgecolors='grey', linewidth=0.5
)

for _, row in df.iterrows():
    if row['county'] in ['Nairobi', 'Lamu', 'Turkana', 'Nakuru', 'Kiambu', 'Kakamega', 'Mombasa']:
        ax.annotate(row['county'], (row['population_2024'] / 1_000_000, row['budget_billion']),
                    textcoords='offset points', xytext=(6, 4), fontsize=8)

cb = plt.colorbar(scatter, ax=ax)
cb.set_label('Budget Per Person (KES)', fontsize=10)
ax.set_title('County Budget vs Population — FY 2023/24', fontsize=13, fontweight='bold')
ax.set_xlabel('Population (millions)', fontsize=11)
ax.set_ylabel('Budget (KES Billions)', fontsize=11)
plt.tight_layout()
plt.savefig('dashboards/budget_vs_population.png', dpi=150, bbox_inches='tight')
plt.show()
print('Chart 3 saved.')

# ── Summary table ────────────────────────────────────────────────────────────
summary = df[['county', 'population_2024', 'budget_billion', 'budget_per_person']].copy()
summary.columns = ['County', 'Population (2024)', 'Budget (KES B)', 'Budget/Person (KES)']
summary = summary.sort_values('Budget/Person (KES)', ascending=False).reset_index(drop=True)
summary.index += 1

print(f"\n{'─'*60}")
print(f"  KENYA COUNTY BUDGET ANALYSIS — FY 2023/24")
print(f"{'─'*60}")
print(f"  Total Population : {df['population_2024'].sum():>15,}")
print(f"  Total Budget     : KES {df['budget_billion'].sum():>8.1f} billion")
print(f"  National Average : KES {df['budget_per_person'].mean():>8,.0f} per person")
print(f"  Highest          : {sorted_df.iloc[0]['county']} — KES {sorted_df.iloc[0]['budget_per_person']:,}")
print(f"  Lowest           : {sorted_df.iloc[-1]['county']} — KES {sorted_df.iloc[-1]['budget_per_person']:,}")
print(f"{'─'*60}\n")
print(summary.to_string())