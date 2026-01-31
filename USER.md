# USER.md - About Your Human

- **Name:** Eugene Lim
- **What to call them:** Eugene
- **Pronouns:** 
- **Timezone:** Asia/Singapore (SGT)
- **Notes:** Co-founder & COO of Dreamcore Private Limited (Singapore). Cares about systems + ops. Uses a Pixel 7a.
- **Spouse:** Mandy
- **Children:** two sons — Elliott (5 on 19 June 2026) and Everett (2 on 23 April 2026)

## Profile & Preferences
- **Roles & Scope:** Head of Operations, Customer Service, and Business Transformation at Dreamcore; operator of the HAVEN LAN café; covering both consumer and enterprise markets (custom PCs, gaming hardware, workstations, AI/compute solutions).
- **Systems‑minded & Data‑driven:** Focuses on why things work; relies heavily on spreadsheets and automations (Google Sheets, Apps Script, Excel Online, HubSpot, Trello, Calendly) to reduce human error, boost visibility, and save time.
- **Communication Style:** Prefers direct, plain‑spoken language with step‑by‑step reasoning, explicit assumptions, clear trade‑offs, and a recommended path forward; tolerates mild humor/snark; avoids fluff, filler, and vague explanations. Prefers continuous, timely responses without long pauses, as gaps make him worry.
- **Implementation Preference:** Favors full end‑to‑end solutions that fail loudly and are easy to debug over isolated snippets; prioritizes time savings and reliability over elegance. Prefers to avoid running console commands himself—ask him what to paste, and the assistant will handle execution thereafter (unless he explicitly asks for console access or it’s a high‑risk operation, in which case suggest he run it himself).
- **Personal Values:** Family‑first approach prioritizing stability, time, and long‑term security; protective of personal time and reduces after‑hours firefighting; values reliability, accountability, and pragmatic solutions.
- **SSH Key Management (Windows):** Prefers to use PuTTYgen for SSH key generation instead of console-based tools.


## Standing instructions

### Daily Singapore Morning Brief
- Send daily at **8:00 AM Asia/Singapore** to Eugene’s Telegram DM.
- **5 fixed sections** (always show all 5, even if empty):
  1. General/Top
  2. Politics/Public Policy
  3. Tech/Startups
  4. Entertainment/Culture
  5. What’s trending (social/news; label low-confidence if social)
- Each bullet: **what happened → why it matters (Dreamcore ops/systems angle) → 1 source link**.
- Preferred sources: **Straits Times + Mothership** first; add CNA/TODAY/official sources when better.
- Bottom: **Persistent Trends — Top 5**, track multi-day items and label **Day X**; placeholders OK when data is thin.
- Formatting: **old-bot single-line title** + **new-bot readability** (bold section headers, spacing). Use explicit “Why it matters:” with Dreamcore ops angle.

### Nightly Workflow Surprise Build
- Every night while Eugene sleeps: build **one small, testable workflow improvement** for Dreamcore.
- Scope: 1–3 hours.
- Create under: `nightly-builds/YYYY-MM-DD-<short-slug>/`
- Include README: what it does, why it matters, setup, test steps, rollback.
- Avoid destructive actions; don’t touch production systems.
- If rate-limited: serialize work + batch messages.

### Hydration reminders
- **Weekdays:** every hour **10:00–19:00**
- **Weekdays extra:** **21:00** and **23:00**
- **Weekends:** **10:00, 15:00, 18:00, 21:00, 23:00**
- Message: short + slightly witty.
