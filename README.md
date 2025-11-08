# Kalman Filter — 1D Position Tracker (Streamlit)

An interactive demo of a **linear Kalman Filter** for a 1-D constant-velocity system.  
Tune **process noise** and **measurement noise** to see how the estimate balances **model vs sensor** in real time.

---

## 🚀 Live Demo

🔗 **App:** https://kalman-filter-demo-hcdt5td97xsusuxjjcmjes.streamlit.app/

---

## 🛠️ Run Locally

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## 📎 Summary

| Concept  | Description                        |
| -------- | ---------------------------------- |
| State    | Position + Velocity in 1D          |
| Sensor   | Noisy GPS-like position only       |
| Goal     | Estimate true motion despite noise |
| Controls | Tune model & sensor noise live     |

You can:

* See **truth vs noisy measurements vs filter estimate**
* Change noise and watch filter behavior update instantly
* Export CSV for analysis

## Repo structure

```
.
├─ streamlit_app.py
├─ explanation.ipynb
├─ requirements.txt
└─ README.md
```

## Dev notes

- Vectorized NumPy math
- Plotly/matplotlib for visualization
- CSV export included

## License

MIT — Onyero Walter Ofuzim
