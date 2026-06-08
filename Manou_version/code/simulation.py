import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# ============================================================
# 1. Parameters
# ============================================================

N_layers = 100

hp = 0.1e-3        # papierdikte [m]
ha = 0.015e-3      # luchtlaagdikte [m]

rho_p = 800        # papierdichtheid [kg/m^3]
rho_a = 1.2        # luchtdichtheid [kg/m^3]

A = 1e-4           # effectief contactoppervlak [m^2]

# Effectieve materiaalparameters
E_p = 5e6          # papierstijfheid [Pa]


hp_ref = 0.1e-3
E_a_ref = 1000
n_air = 1.6

E_a = E_a_ref * (hp / hp_ref)**n_air

eta_p = 30         # papierdemping [Pa s]
eta_a = 2          # luchtdemping [Pa s]

# Impact
F0 = 1.0           # maximale kracht [N]
tc = 3e-3          # contacttijd [s]

# Simulatie
T = 0.03           # totale simulatietijd [s]

# ============================================================
# 2. Bouw gelaagde stapel
# ============================================================

thickness = []
rho = []
E = []
eta = []

for _ in range(N_layers):
    thickness.append(hp)
    rho.append(rho_p)
    E.append(E_p)
    eta.append(eta_p)

    thickness.append(ha)
    rho.append(rho_a)
    E.append(E_a)
    eta.append(eta_a)

thickness = np.array(thickness)
rho = np.array(rho)
E = np.array(E)
eta = np.array(eta)

N = len(thickness)
h_total = np.sum(thickness)

x = np.zeros(N + 1)
x[1:] = np.cumsum(thickness)
x_norm = x / h_total

# Massa's op knopen
m = np.zeros(N + 1)

for i in range(N):
    layer_mass = rho[i] * A * thickness[i]
    m[i] += 0.5 * layer_mass
    m[i + 1] += 0.5 * layer_mass

# Veer- en demperconstanten per laag
k = E * A / thickness
b = eta * A / thickness

# ============================================================
# 3. Impactkracht
# ============================================================

def impact_force(t):
    """
    Halve sinusvormige krachtpuls.
    Na tc is het contact voorbij.
    """
    if 0 <= t <= tc:
        return F0 * np.sin(np.pi * t / tc)
    return 0.0

# ============================================================
# 4. ODE-systeem
# ============================================================

def rhs(t, y):
    u = y[:N+1].copy()
    v = y[N+1:].copy()

    # Harde ondergrond:
    # onderste node staat vast
    u[-1] = 0.0
    v[-1] = 0.0

    F = np.zeros(N + 1)

    # Interne laagkrachten
    for i in range(N):
        du = u[i + 1] - u[i]
        dv = v[i + 1] - v[i]

        force = k[i] * du + b[i] * dv

        F[i] += force
        F[i + 1] -= force

    # Impactkracht op bovenkant
    F[0] += impact_force(t)

    a = F / m

    # Onderste node blijft vast
    a[-1] = 0.0
    v[-1] = 0.0

    return np.concatenate([v, a])

# ============================================================
# 5. Los het systeem op
# ============================================================

y0 = np.zeros(2 * (N + 1))

t_eval = np.linspace(0, T, 3000)

sol = solve_ivp(
    rhs,
    t_span=(0, T),
    y0=y0,
    t_eval=t_eval,
    method="Radau",
    rtol=1e-6,
    atol=1e-9
)

if not sol.success:
    print("Solver warning:")
    print(sol.message)

time = sol.t
u_all = sol.y[:N+1, :]

# Forceer voor output ook exact vaste onderkant
u_all[-1, :] = 0.0

top_signal = u_all[0, :]

# Omdat de laatste node vast is, meten we vlak boven de onderkant
near_bottom_signal = u_all[-2, :]

# ============================================================
# 6. Snelheid schatten
# ============================================================

# Let op: dit is grof. Door reflecties is argmax niet ideaal.
# Dit gebruikt eerste overschrijding van een kleine drempel.

threshold_top = 0.05 * np.max(np.abs(top_signal))
threshold_bottom = 0.05 * np.max(np.abs(near_bottom_signal))

top_indices = np.where(np.abs(top_signal) > threshold_top)[0]
bottom_indices = np.where(np.abs(near_bottom_signal) > threshold_bottom)[0]

if len(top_indices) > 0 and len(bottom_indices) > 0:
    t_top = time[top_indices[0]]
    t_bottom = time[bottom_indices[0]]
    dt_arrival = t_bottom - t_top
    c_est = h_total / dt_arrival if dt_arrival > 0 else np.nan
else:
    t_top = np.nan
    t_bottom = np.nan
    c_est = np.nan

print(f"Totale stapelhoogte: {h_total*1000:.3f} mm")
print(f"Aankomsttijd boven:  {t_top*1000:.3f} ms")
print(f"Aankomsttijd onder:  {t_bottom*1000:.3f} ms")
print(f"Geschatte snelheid: {c_est:.2f} m/s")

# ============================================================
# 7. Plot signalen
# ============================================================

plt.figure()
plt.plot(time * 1000, top_signal * 1e6, label="bovenkant x=0")
plt.plot(time * 1000, near_bottom_signal * 1e6, label="vlak boven onderkant")
plt.xlabel("tijd [ms]")
plt.ylabel("verplaatsing [µm]")
plt.legend()
plt.title("Compressiegolf door papierstapel")
plt.grid(True)
plt.show()

# ============================================================
# 8. Golfprofielen op verschillende tijden
# ============================================================

plt.figure()

plot_times_ms = [0.5, 1, 2, 3, 5, 8, 12, 20]

for t_ms in plot_times_ms:
    idx = np.argmin(np.abs(time - t_ms * 1e-3))
    plt.plot(x_norm, u_all[:, idx] * 1e6, label=f"{time[idx]*1000:.1f} ms")

plt.xlabel("genormaliseerde positie x")
plt.ylabel("verplaatsing [µm]")
plt.legend()
plt.title("Golfprofiel door de stapel")
plt.grid(True)
plt.show()

from matplotlib.animation import FuncAnimation

# ============================================================
# 9. Animatie van psi(x,t)
# ============================================================

psi = u_all  # psi[x_index, time_index]

fig, ax = plt.subplots()

line, = ax.plot(x_norm, psi[:, 0] * 1e6)

ax.set_xlabel("genormaliseerde positie x")
ax.set_ylabel(r"$\psi(x,t)$ [µm]")
ax.set_title("Compressiegolf door de papierstapel")

ylim = np.max(np.abs(psi)) * 1e6
if ylim == 0:
    ylim = 1

ax.set_ylim(-ylim, ylim)
ax.grid(True)

time_text = ax.text(
    0.02, 0.95, "",
    transform=ax.transAxes,
    verticalalignment="top"
)

# niet elke tijdstap plotten, anders wordt het traag
frame_indices = np.linspace(0, len(time) - 1, 300).astype(int)

def update(frame_number):
    idx = frame_indices[frame_number]
    line.set_ydata(psi[:, idx] * 1e6)
    time_text.set_text(f"t = {time[idx]*1000:.2f} ms")
    return line, time_text

ani = FuncAnimation(
    fig,
    update,
    frames=len(frame_indices),
    interval=30,
    blit=True
)
ani.save("papier_golf.gif", writer="pillow", fps=30)

plt.show()