
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Kalman Filter — 1D Position Tracker", layout="wide")

st.title("Kalman Filter — 1D Position Tracker")
st.caption("Tune noise levels and see how the estimate balances model vs. measurements in real time.")

with st.sidebar:
    st.header("Simulation Settings")
    t_end = st.slider("Total time (s)", 5, 60, 20, 1)
    dt = st.slider("Time step dt (s)", 0.02, 0.5, 0.10, 0.01)
    v0 = st.slider("Initial velocity (m/s)", 0.0, 5.0, 1.0, 0.1)
    seed = st.number_input("Random seed", value=0, step=1, help="For reproducibility")

    st.header("Noise (tune these!)")
    q_acc = st.slider("Process accel noise σ_acc", 0.0, 1.5, 0.30, 0.05,
                      help="Higher ⇒ model less trusted (estimate follows measurements more).")
    r_gps = st.slider("Measurement noise σ_gps", 0.0, 2.0, 0.60, 0.05,
                      help="Higher ⇒ sensor less trusted (estimate follows model more).")

@st.cache_data(show_spinner=False)
def simulate(q_acc, r_gps, dt, t_end, v0, seed):
    t = np.arange(0, t_end + dt, dt)
    A = np.array([[1, dt],[0, 1]])
    G = np.array([[0.5*dt**2],[dt]])
    Q = (q_acc**2) * (G @ G.T)
    H = np.array([[1, 0]])
    R = np.array([[r_gps**2]])

    x_true = np.zeros((2, len(t)))
    x_true[:, 0] = [0.0, v0]
    rng = np.random.default_rng(int(seed))
    for k in range(1, len(t)):
        a_k = rng.normal(0, q_acc, size=(1,))
        x_true[:, k] = (A @ x_true[:, k-1]) + (G.flatten() * a_k)

    z = x_true[0, :] + rng.normal(0, r_gps, size=len(t))

    x_hat = np.zeros((2, len(t)))
    x_hat[:, 0] = [0.0, 0.0]
    P = np.eye(2) * 1.0
    I2 = np.eye(2)

    for k in range(1, len(t)):
        x_pred = A @ x_hat[:, k-1]
        P_pred = A @ P @ A.T + Q
        y = z[k] - (H @ x_pred)
        S = H @ P_pred @ H.T + R
        K = P_pred @ H.T @ np.linalg.inv(S)
        x_hat[:, k] = x_pred + (K @ y).ravel()
        P = (I2 - K @ H) @ P_pred

    df = pd.DataFrame({
        "t": t,
        "true_pos": x_true[0, :],
        "true_vel": x_true[1, :],
        "gps_meas": z,
        "kf_pos": x_hat[0, :],
        "kf_vel": x_hat[1, :],
    })
    return df

df = simulate(q_acc, r_gps, dt, t_end, v0, seed)

# Metrics
mse = float(np.mean((df["kf_pos"] - df["true_pos"])**2))
rmse = float(np.sqrt(mse))
st.metric("RMSE (position)", f"{rmse:.3f} m")

# Plotly figure
fig = go.Figure()
fig.add_trace(go.Scatter(x=df["t"], y=df["true_pos"], mode="lines", name="True position"))
fig.add_trace(go.Scatter(x=df["t"], y=df["gps_meas"], mode="markers", name="Noisy GPS",
                         opacity=0.6, marker=dict(size=5)))
fig.add_trace(go.Scatter(x=df["t"], y=df["kf_pos"], mode="lines", name="KF estimate"))
fig.update_layout(height=520, xaxis_title="Time (s)", yaxis_title="Position (m)",
                  legend=dict(orientation="h", y=-0.2))
st.plotly_chart(fig, use_container_width=True)

with st.expander("Download data (CSV)"):
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", csv, file_name="kalman_demo_data.csv", mime="text/csv")

with st.expander("How to read the plot & tune it"):
    st.markdown(
        "- **Blue** is the ground truth.\n"
        "- **Orange dots** are noisy position measurements.\n"
        "- **Green** is the Kalman estimate — smooth but responsive.\n\n"
        "**Tuning tips:**\n"
        "- Increase **σ_gps** → assume a noisier sensor → estimate trusts the model more (smoother, more lag).\n"
        "- Increase **σ_acc** → assume a shakier model → estimate trusts the measurements more (less smooth, more reactive)."
    )

st.caption("By Onyero Walter Ofuzim — controls × data. Source available in the linked repo.")
