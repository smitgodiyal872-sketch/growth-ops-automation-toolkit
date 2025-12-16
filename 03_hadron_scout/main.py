import pandas as pd
import matplotlib.pyplot as plt

# 1. THE DATASET 
founders = ['Alex (DeFi)', 'Sarah (ZK-Tech)', 'Jay (NFTs)', 'Rohan (Infra)', 
            'Priya (Social)', 'Mike (Gaming)', 'Elena (DAO)', 'Sam (L2)']

data = {
    'Founder': founders,
    'Github_Commits': [120, 45, 80, 200, 15, 60, 90, 150], # Execution
    'Discord_Msgs': [500, 1200, 300, 150, 2000, 400, 800, 100], # Community Activity
    'Events_Attended': [2, 5, 1, 0, 4, 3, 3, 1], # Commitment
    'Vibe_Score': [85, 95, 70, 60, 98, 88, 92, 75] # The "Hadron Metric"
}

df = pd.DataFrame(data)

# 2. THE ALGORITHM 
df['Hadron_Score'] = (
    (df['Github_Commits'] * 2.0) + 
    (df['Discord_Msgs'] * 0.1) + 
    (df['Events_Attended'] * 20.0) + 
    (df['Vibe_Score'] * 1.5)
)

# Sort by Score to find the winners
df_sorted = df.sort_values(by='Hadron_Score', ascending=False).reset_index(drop=True)

# 3. THE DECISION ENGINE
# Top 3 get invited to Dubai. Rest get Waitlisted.
df_sorted['Status'] = ['Waitlist' for _ in range(len(df_sorted))]
df_sorted.loc[:2, 'Status'] = '✅ INVITE TO DUBAI'

# 4. VISUALIZATION 
print("--- HADRON SCOUT: DUBAI COHORT SELECTION ---")
print(df_sorted[['Founder', 'Hadron_Score', 'Status']])

plt.figure(figsize=(10, 6))
colors = ['#7000FF' if s == '✅ INVITE TO DUBAI' else 'gray' for s in df_sorted['Status']] 
plt.barh(df_sorted['Founder'], df_sorted['Hadron_Score'], color=colors)
plt.xlabel('Hadron Potential Score')
plt.title('The Hadron Scout: Automated Founder Filtering')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()
