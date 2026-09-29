# Demo Script & Presentation Guide (2 Minutes)

## Step-by-Step Presentation Guide

1. **Launch App (0:00 - 0:15):**
   - Run `streamlit run app.py` in PowerShell.
   - Point out Header, Disclaimer, and Visual Pipeline Diagram.

2. **Run Legitimate Signature Demo (0:15 - 0:40):**
   - Click sidebar preset: `?? Legitimate`.
   - Show status banner: `VERIFICATION ACCEPTED` (Green).
   - Point out Error Rate (0.00%) vs Threshold (5.00%).

3. **Run Signature Forgery Demo (0:40 - 1:05):**
   - Click sidebar preset: `?? Forged`.
   - Show status banner: `THREAT DETECTED ? FORGED SIGNATURE`.
   - Point out SHA-256 mismatch and high error rate.

4. **Run Impersonation & Replay Demos (1:05 - 1:35):**
   - Click `?? Impersonate` -> `THREAT DETECTED`.
   - Click `?? Replay` -> `THREAT DETECTED ? REPLAY ATTACK`.

5. **Run Channel Noise & Unauthorized Verifier (1:35 - 2:00):**
   - Click `? Channel Noise` -> Show noise trend chart.
   - Click `?? Unauthorized` -> Show access rejection.
   - Download JSON/CSV Audit Report.
