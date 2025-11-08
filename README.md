````markdown
# Kalman Filter — 1D Position Tracker (Streamlit)

An interactive demo of a **linear Kalman Filter** for a 1-D constant-velocity system.  
Use the sliders to tune **process noise** and **measurement noise** and see how the estimate balances **model vs. sensor** in real time.

---

## Live App

> 🔗 **Demo:** [kalman-filter-demo.streamlit.app](https://kalman-filter-demo-hcdt5td97xsusuxjjcmjes.streamlit.app/)

---

## Quick Start (Local)

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
````

---

## What This Demo Shows

* **Simulated truth**: an object moving in 1D with (nearly) constant velocity plus small acceleration jitter.
* **Noisy sensor**: a “GPS”-like measurement of position only.
* **Kalman Filter**: estimates both **position** and **velocity** from noisy measurements and a simple motion model.
* **Interactive tuning**: change noise levels and immediately see how the estimate responds.
* **Downloadable CSV**: export the generated time series for your own analysis.

---

## Model (State-Space)

We model the system in discrete time with state
[
x_k = \begin{bmatrix}\text{position}\ \text{velocity}\end{bmatrix}\in\mathbb{R}^2.
]

**Dynamics (constant-velocity with acceleration disturbance):**
[
x_{k+1} = A,x_k + w_k,\qquad
A = \begin{bmatrix} 1 & \Delta t [4pt] 0 & 1 \end{bmatrix}.
]

The process noise (w_k \sim \mathcal{N}(0,,Q)) captures unmodeled acceleration. In this demo,
[
Q = \sigma_{\text{acc}}^{2}, G G^\top,\qquad
G = \begin{bmatrix} \tfrac{1}{2},\Delta t^{2} [4pt] \Delta t \end{bmatrix}.
]

**Measurement (position-only):**
[
z_k = H,x_k + v_k,\qquad
H = \begin{bmatrix} 1 & 0 \end{bmatrix},\qquad
v_k \sim \mathcal{N}(0,,R),\quad R=\sigma_{\text{gps}}^{2}.
]

---

## Kalman Filter (Predict–Update)

**Predict**
[
\hat{x}*{k|k-1} = A,\hat{x}*{k-1|k-1},\qquad
P_{k|k-1} = A,P_{k-1|k-1},A^\top + Q.
]

**Update**
[
\begin{aligned}
y_k &= z_k - H,\hat{x}*{k|k-1} &&\text{(innovation)}\
S_k &= H,P*{k|k-1},H^\top + R &&\text{(innovation covariance)}\
K_k &= P_{k|k-1},H^\top,S_k^{-1} &&\text{(Kalman gain)}\
\hat{x}*{k|k} &= \hat{x}*{k|k-1} + K_k,y_k &&\text{(state update)}\
P_{k|k} &= (I - K_k H),P_{k|k-1} &&\text{(covariance update).}
\end{aligned}
]

---

## App Controls → Model Parameters

* **Total time (s)** & **Time step (\Delta t)** — simulation horizon and discretization.
* **Initial velocity (m/s)** — sets (x_0 = \begin{bmatrix}0 \ v_0\end{bmatrix}).
* **Random seed** — reproducibility for process/measurement noise.
* **Process accel noise (\sigma_{\text{acc}})** — sets (Q = \sigma_{\text{acc}}^{2},GG^\top).

  * Higher ⇒ **trust the model less** ⇒ estimate reacts more to measurements (less smooth).
* **Measurement noise (\sigma_{\text{gps}})** — sets (R = \sigma_{\text{gps}}^{2}).

  * Higher ⇒ **trust the sensor less** ⇒ estimate follows the model (smoother, more lag).

---

## Reading the Plot

* **Blue** — ground truth position.
* **Orange dots** — noisy position measurements.
* **Green** — Kalman Filter position estimate (smooth yet responsive).
* **RMSE (position)** — shown above the chart; use it to gauge the effect of tuning.

**Typical behavior**

* With **high (\sigma_{\text{gps}})**: measurements are noisy → the estimate is smoother and lags slightly.
* With **high (\sigma_{\text{acc}})**: model is assumed shakier → the estimate becomes more reactive to measurements.

---

## When to Use This Filter (and When Not To)

* ✔️ Linear dynamics, Gaussian noise, frequent measurements.
* ➖ If dynamics are **nonlinear** (e.g., range–bearing, bearings-only), prefer **EKF/UKF**.
* ➖ If noise is **heavy-tailed** or outliers are common, consider robust filters or adaptive (Q/R).

**Extensions you could add here**

* Velocity & innovation plots; covariance bands ((\pm 2\sigma)).
* Time-varying (R) (adaptive sensor trust).
* Higher-order motion models (constant-acceleration / jerk).
* 2D/3D tracking.

---

## Repo Layout

```
.
├─ streamlit_app.py         # the app (UI + simulation + filter)
├─ requirements.txt         # streamlit, numpy, pandas, plotly
└─ README.md                # this document
```

---

## Development Notes

* Simulation and filter are vectorized **NumPy**; the app uses `@st.cache_data` for responsive updates.
* Plotting uses **Plotly** (interactive zoom/pan).
* **CSV export** is provided for downstream analysis.

---

## License & Attribution

* **Author:** Onyero Walter Ofuzim — controls × data.
* **License:** *Choose one (e.g., MIT) and state it here.*
* **Citation:** If you reference this app in academic work, please cite this repository.

---

## Support / Questions

Open an Issue or reach out on LinkedIn. Happy filtering!

```
```
