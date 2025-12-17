/** @jsxImportSource https://esm.sh/react */

// The "Val Town Scout" - Built by Smit Godiyal
// Purpose: Automatically rank startup applications based on weighted logic.

export default async function(req: Request): Promise<Response> {
  // 1. Mock Data (Simulating a list of startup applicants)
  const startups = [
    { name: "Nexus (DeFi)", devSpeed: 90, design: 70, traction: 2000 },
    { name: "Vortex (L2)", devSpeed: 40, design: 60, traction: 500 },
    { name: "Nova (Consumer)", devSpeed: 85, design: 95, traction: 8000 },
    { name: "Echo (Infra)", devSpeed: 95, design: 50, traction: 150 },
    { name: "Glitch (Gaming)", devSpeed: 60, design: 88, traction: 1200 },
  ];

  // 2. The Logic (The Scoring Engine)
  // Formula: Dev Speed (50%) + Design (30%) + Traction (20%)
  const scored = startups.map(s => {
    // Normalizing traction (dividing by 100 so it doesn't skew the score too much)
    const score = (s.devSpeed * 0.5) + (s.design * 0.3) + ((s.traction / 100) * 0.2);
    return { ...s, score: score.toFixed(1) };
  }).sort((a, b) => Number(b.score) - Number(a.score)); // Sort highest to lowest

  // 3. The Output (HTML Table)
  const html = `
  <html>
  <head>
    <title>Smit's Deal Flow Scorer</title>
    <style>
      body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; padding: 40px; background: #f4f4f5; max-width: 800px; margin: auto; }
      h1 { color: #18181b; margin-bottom: 10px; }
      p { color: #52525b; margin-bottom: 30px; }
      .card { background: white; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); overflow: hidden; }
      table { width: 100%; border-collapse: collapse; }
      th { background: #f8fafc; color: #64748b; font-size: 12px; text-transform: uppercase; letter-spacing: 1px; padding: 16px; text-align: left; font-weight: 600; }
      td { padding: 16px; border-bottom: 1px solid #f1f5f9; color: #334155; }
      tr:last-child td { border-bottom: none; }
      tr:nth-child(1) { background-color: #ecfdf5; } /* Top Rank Green */
      tr:nth-child(1) td { color: #047857; font-weight: bold; }
      .badge { background: #e2e8f0; padding: 4px 8px; border-radius: 4px; font-size: 12px; }
    </style>
  </head>
  <body>
    <h1>🚀 Val Town Deal Flow Scorer</h1>
    <p>Automated ranking logic built by <b>Smit Godiyal</b> (Day 4 Build).</p>
    
    <div class="card">
      <table>
        <tr>
          <th>Startup Name</th>
          <th>Dev Speed (50%)</th>
          <th>Design (30%)</th>
          <th>Final Score</th>
        </tr>
        ${scored.map(s => `
          <tr>
            <td>${s.name}</td>
            <td>${s.devSpeed}/100</td>
            <td>${s.design}/100</td>
            <td>${s.score}</td>
          </tr>
        `).join('')}
      </table>
    </div>
    <br>
    <small style="color: #94a3b8;">Pitching: Automating Ops for Val Town.</small>
  </body>
  </html>
  `;

  return new Response(html, { headers: { "Content-Type": "text/html" } });
}
