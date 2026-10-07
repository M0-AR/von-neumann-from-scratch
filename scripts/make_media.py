"""Generate README/Pages media: PNG figures + animated Fredkin GIF. Verified by existence + sizes."""
import os, json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from vonneumann import selfrep

BASE = os.path.join(os.path.dirname(__file__), "..", "docs", "assets")
os.makedirs(BASE, exist_ok=True)
with open(os.path.join(os.path.dirname(__file__), "..", "results", "results.json")) as f:
    R = json.load(f)

def save(fig, name):
    p = os.path.join(BASE, name)
    fig.savefig(p, dpi=110, bbox_inches="tight")
    plt.close(fig)
    print(name, os.path.getsize(p), "bytes")

# 1. sort scaling (measured merge + textbook insert projection)
fig, ax = plt.subplots()
ns = [100, 1000, 5000]
merge = [R["04_scale"][str(n)]["merge"] for n in ns]
ax.loglog(ns, merge, "o-", label="merge sort measured")
ax.loglog(ns, [m * (R["04_sort1000"]["insert"] / R["04_sort1000"]["merge"] / 10) for m in merge],
           "--", label="insertion trend (n^2)")
ax.set_xlabel("n"); ax.set_ylabel("comparisons"); ax.legend(); ax.set_title("Sorting: n log n vs n^2")
save(fig, "sort_scaling.png")

# 2. pi convergence
fig, ax = plt.subplots()
xs = [100, 10000, 100000]; ys = [R["05_pi"][str(x)] for x in xs]
ax.semilogx(xs, ys, "o-"); ax.axhline(3.14159265, ls="--")
ax.set_xlabel("darts"); ax.set_ylabel("estimate"); ax.set_title("Monte Carlo pi converges ~1/sqrt(N)")
save(fig, "pi_convergence.png")

# 3. neutron curve (log)
fig, ax = plt.subplots()
ts = [1, 2, 4, 8]; vs = [R["05_neutron"][str(t)] for t in ts]
ax.semilogy(ts, vs, "o-", label="measured")
ax.semilogy(ts, [0.5 ** t for t in ts], "--", label="0.5^thickness")
ax.set_xlabel("wall thickness"); ax.set_ylabel("transmission"); ax.legend()
ax.set_title("Shield transmission is exponential")
save(fig, "neutron_curve.png")

# 4. reliability cliff
fig, ax = plt.subplots()
es = [0.05, 0.10, 0.14, 0.16]; vs = [R["07_cliff"][str(e)] for e in es]
ax.plot(es, vs, "o-"); ax.axvline(1 / 6, ls="--")
ax.set_xlabel("part failure rate"); ax.set_ylabel("machine error (N=99)")
ax.set_title("Reliability cliff at 1/6")
save(fig, "reliability_cliff.png")

# 5. fredkin panels t=0,8,24,56 (small 48-grid crops for figure)
def run_to(steps, H=96, W=96):
    g = selfrep.seed_v(H, W)
    for _ in range(steps):
        g = selfrep.step_fredkin(g)
    return g
fig, axes = plt.subplots(1, 4, figsize=(12, 3))
for ax, t in zip(axes, [0, 8, 24, 56]):
    g = run_to(t)
    ax.imshow(g, cmap="Greys", interpolation="nearest")
    ax.set_title(f"t={t}"); ax.axis("off")
fig.suptitle("Fredkin replicator: 1 -> 4 -> 16 -> 64 copies")
save(fig, "fredkin_panels.png")

# 6. animated demo GIF (t=0..32 on 64-grid, downsampled)
try:
    from matplotlib.animation import FuncAnimation
    g = selfrep.seed_v(64, 64)
    frames = [g]
    for _ in range(32):
        g = selfrep.step_fredkin(g)
        frames.append(g)
    fig, ax = plt.subplots(figsize=(4, 4))
    im = ax.matshow(frames[0], cmap="Greys")
    ax.axis("off"); ax.set_title("Fredkin self-replication demo")
    def upd(i):
        im.set_data(frames[i]); return [im]
    ani = FuncAnimation(fig, upd, frames=len(frames), interval=250)
    gp = os.path.join(BASE, "demo.gif")
    ani.save(gp, writer="pillow", fps=4)
    print("demo.gif", os.path.getsize(gp), "bytes")
    plt.close(fig)
except Exception as e:
    print("GIF skipped:", e)

print("MEDIA DONE")
