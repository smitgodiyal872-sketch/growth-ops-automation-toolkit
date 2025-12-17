# 04. Val Town Deal Flow Scorer ⚡️

### **The Context**
Built for **Day 4** of the `#100DaysOfGrowthOps` challenge.
Targeting: **Val Town** (@stevekrouse).

### **The Problem**
Traditional Ops scripts run locally on Python. This creates friction when sharing tools with a remote team. I wanted to test if I could build a "Growth Ops" tool that runs entirely in the cloud, instantly accessible via a URL.

### **The Solution**
I ported the logic from my "Hadron Scout" (Python) into **TypeScript** and deployed it on **Val Town**.
* **Input:** Mock Startup Data (Traction, Speed, Design).
* **Logic:** Weighted Algorithm (50% Speed, 30% Design, 20% Traction).
* **Output:** A live-rendered HTML Leaderboard.

### **Why Val Town?**
It allows Growth Engineers to ship internal tools (dashboards, emailers, scrapers) without setting up servers. It is "Ops at the Speed of Code."

### **Tech Stack**
* **Language:** TypeScript
* **Platform:** Val Town (Serverless)
* **Frontend:** Raw HTML/CSS (Server-Side Rendered)

---
*Part of the "100 Days of Growth Ops" Challenge by Smit Godiyal.*
