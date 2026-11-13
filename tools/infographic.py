"""Black-and-white comparison infographic of the four notebooks (1200×1500 PNG).

Usage: python tools/infographic.py [ru|en] [output.png]
Default output: assets/comparison_<lang>.png
"""
import sys, textwrap
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle

LANG = sys.argv[1] if len(sys.argv) > 1 else "ru"
OUT = sys.argv[2] if len(sys.argv) > 2 else f"assets/comparison_{LANG}.png"
plt.rcParams["font.family"] = ["Noto Sans", "DejaVu Sans"]
plt.rcParams["mathtext.fontset"] = "dejavusans"

T = {
"ru": dict(
    kicker="ЦИФРОВАЯ ОБРАБОТКА СИГНАЛОВ · 4 НОУТБУКА",
    title="Как связь побеждает шум",
    sub="Четыре техники, одна физика: размазать, связать, разделить, развернуть",
    cols=["CDMA", "LDPC", "LTE", "LoRa"],
    colsub=["расширение спектра", "код с проверками", "OFDM + турбокод", "чирп-модуляция"],
    rows=[
        ("ИДЕЯ", [
            "Каждый бит умножается на код из N = 1023 чипов",
            "Проверки чётности связывают биты; декодер гоняет LLR по графу",
            "Сотни узких поднесущих вместо одной широкой несущей",
            "Символ — сдвиг чирпа; dechirp делает из него тон",
        ]),
        ("ФОРМУЛА", [r"$\mathrm{SNR_{out}} = N\cdot\mathrm{SNR_{chip}}$",
                     r"$H\,\mathbf{c}^{T} = \mathbf{0}$",
                     r"$Y_k = H_k X_k + W_k$",
                     r"$x_s[n]\,x_0^*[n] = e^{j2\pi sn/N}$"]),
        ("ВЫИГРЫШ", ["30 дБ", "6,1 дБ", "7,5 дБ", "−22 дБ"]),
        ("", [
            "обработки при N = 1023",
            "кодирования при BER 10⁻⁴, R = 1/2",
            "турбокода при BER 10⁻⁴, R = 1/3",
            "SNR, на котором ещё идёт приём (SF12)",
        ]),
        ("ПРОТИВ ПОМЕХИ", [
            "Глушилку давит в N раз",
            "Сама — нет, нужен перемежитель",
            "Код восстанавливает поднесущие в провалах",
            "Тон размазывается по всем N бинам",
        ]),
        ("ЦЕНА", [
            "Полоса в N раз шире",
            "Вдвое больше бит + итеративный декодер",
            "Пик-фактор 11 дБ, 7 % на CP, синхронизация",
            "Скорость 0,3–5,5 кбит/с",
        ]),
        ("ГДЕ", ["GPS, 3G WCDMA", "5G NR, Wi-Fi, DVB-S2", "4G LTE; OFDM — ещё в 5G и Wi-Fi", "IoT, LoRaWAN"]),
        ("ОДНИМ СЛОВОМ", ["размазать", "связать", "разделить", "развернуть"]),
    ],
    foot="Каждое число — из симуляции на NumPy, сверено с теорией",
    repo="github.com/arsatyants/dsp-notebooks",
),
"en": dict(
    kicker="DIGITAL SIGNAL PROCESSING · 4 NOTEBOOKS",
    title="How radio beats the noise",
    sub="Four techniques, one physics: spread, link, split, sweep",
    cols=["CDMA", "LDPC", "LTE", "LoRa"],
    colsub=["spread spectrum", "parity-check code", "OFDM + turbo code", "chirp modulation"],
    rows=[
        ("IDEA", [
            "Every bit is multiplied by a code of N = 1023 chips",
            "Parity checks tie the bits together; the decoder passes LLRs on a graph",
            "Hundreds of narrow subcarriers instead of one wide carrier",
            "A symbol is a shifted chirp; dechirp turns it into a tone",
        ]),
        ("FORMULA", [r"$\mathrm{SNR_{out}} = N\cdot\mathrm{SNR_{chip}}$",
                     r"$H\,\mathbf{c}^{T} = \mathbf{0}$",
                     r"$Y_k = H_k X_k + W_k$",
                     r"$x_s[n]\,x_0^*[n] = e^{j2\pi sn/N}$"]),
        ("GAIN", ["30 dB", "6.1 dB", "7.5 dB", "−22 dB"]),
        ("", [
            "processing gain at N = 1023",
            "coding gain at BER 10⁻⁴, R = 1/2",
            "turbo gain at BER 10⁻⁴, R = 1/3",
            "SNR where reception still works (SF12)",
        ]),
        ("vs. JAMMING", [
            "Suppresses a jammer by a factor of N",
            "Doesn't by itself; needs an interleaver",
            "The code recovers subcarriers in fades",
            "A tone is smeared over all N bins",
        ]),
        ("COST", [
            "N times the bandwidth",
            "Twice the bits + an iterative decoder",
            "11 dB PAPR, 7 % CP, tight sync",
            "Data rate of 0.3–5.5 kbit/s",
        ]),
        ("WHERE", ["GPS, 3G WCDMA", "5G NR, Wi-Fi, DVB-S2", "4G LTE; OFDM also in 5G and Wi-Fi", "IoT, LoRaWAN"]),
        ("IN ONE WORD", ["spread", "link", "split", "sweep"]),
    ],
    foot="Every number comes from a NumPy simulation, checked against theory",
    repo="github.com/arsatyants/dsp-notebooks",
),
}[LANG]

INK, MID, LIGHT, PAPER = "#111111", "#6b6b6b", "#d9d9d9", "#ffffff"
W, H = 8.0, 10.0                         # inches → 1200×1500 px at 150 dpi
fig = plt.figure(figsize=(W, H), dpi=150, facecolor=PAPER)
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")

M = 0.45                                 # outer margin
# header
ax.add_patch(Rectangle((0, H - 1.75), W, 1.75, color=INK, zorder=0))
ax.text(M, H - 0.42, T["kicker"], color="#bdbdbd", fontsize=8.5, weight="bold", va="center")
ax.text(M, H - 0.92, T["title"], color=PAPER, fontsize=25, weight="bold", va="center")
ax.text(M, H - 1.4, T["sub"], color="#d0d0d0", fontsize=10.5, va="center")

# grid geometry
label_w = 1.15
x0 = M + label_w
cw = (W - M - x0) / 4
top = H - 1.95

# ---------- pictograms ----------
def pict(i, cx, cy, w, h):
    lw = 1.3
    if i == 0:      # CDMA: bit × chips
        rng = np.random.default_rng(3)
        ch = rng.choice([-1, 1], 24)
        xs = np.linspace(cx - w / 2, cx + w / 2, 25)
        ys = cy + 0.18 * h * np.r_[ch, ch[-1]]
        ax.step(xs, ys, where="post", color=INK, lw=lw)
        ax.plot([cx - w / 2, cx + w / 2], [cy + 0.42 * h] * 2, color=INK, lw=2.6)
    elif i == 1:    # LDPC: Tanner graph
        vx = np.linspace(cx - w / 2 + 0.08, cx + w / 2 - 0.08, 6); cxs = np.linspace(cx - w / 3, cx + w / 3, 3)
        edges = [(0, 0), (1, 0), (2, 0), (1, 1), (3, 1), (4, 1), (2, 2), (4, 2), (5, 2), (0, 1), (5, 0), (3, 2)]
        for v, c in edges:
            ax.plot([vx[v], cxs[c]], [cy + 0.3 * h, cy - 0.3 * h], color=MID, lw=0.8, zorder=1)
        for x in vx: ax.add_patch(Circle((x, cy + 0.3 * h), 0.055, color=INK, zorder=2))
        for x in cxs: ax.add_patch(Rectangle((x - 0.06, cy - 0.3 * h - 0.06), 0.12, 0.12, color=PAPER, ec=INK, lw=1.2, zorder=2))
    elif i == 2:    # OFDM: overlapping sincs
        f = np.linspace(-4, 4, 400)
        for k in range(-2, 3):
            ax.plot(cx + f * w / 8, cy - 0.35 * h + 0.75 * h * np.sinc(f - k), color=INK if k == 0 else MID, lw=lw if k == 0 else 0.9)
    else:           # LoRa: chirp sawtooth
        t = np.linspace(0, 1, 400)
        for j, s in enumerate([0.0, 0.6, 0.25]):
            fr = (s + t) % 1
            xx = cx - w / 2 + (j + t) * w / 3
            ax.plot(xx, cy - 0.5 * h + 1.0 * h * fr, color=INK, lw=lw)
        ax.plot([cx - w / 2, cx + w / 2], [cy - 0.5 * h - 0.05] * 2, color=MID, lw=0.8)

hdr_h = 1.05
for j in range(4):
    xl = x0 + j * cw
    pict(j, xl + cw / 2, top - 0.3, cw * 0.62, 0.42)
    ax.text(xl + cw / 2, top - 0.72, T["cols"][j], ha="center", va="center", fontsize=15, weight="bold", color=INK)
    ax.text(xl + cw / 2, top - 0.95, T["colsub"][j], ha="center", va="center", fontsize=7.8, color=MID)
y = top - hdr_h
ax.plot([M, W - M], [y, y], color=INK, lw=2)

# row heights
heights = {0: 1.3, 1: 0.55, 2: 0.55, 3: 0.6, 4: 0.88, 5: 0.88, 6: 0.66, 7: 0.72}
wrapw = 19 if LANG == "ru" else 20
for r, (label, cells) in enumerate(T["rows"]):
    h = heights[r]
    if r == 7:   # black band with the verbs
        ax.add_patch(Rectangle((M, y - h), W - 2 * M, h, color=INK, zorder=0, lw=0))
    if r == 2:   # big numbers band
        ax.add_patch(Rectangle((M, y - h - heights[3]), W - 2 * M, h + heights[3], color="#f2f2f2", zorder=0, lw=0))
    if label:
        ax.text(M + 0.02, y - (0.14 if r not in (2, 7) else h * 0.5), "\n".join(textwrap.wrap(label, 11)), fontsize=7.8, weight="bold",
                color=PAPER if r == 7 else INK, va="top" if r not in (2, 7) else "center", linespacing=1.3)
    for j, txt in enumerate(cells):
        xc = x0 + j * cw + cw / 2
        if r == 1:
            ax.text(xc, y - h / 2, txt, ha="center", va="center", fontsize=9.6, color=INK)
        elif r == 2:
            ax.text(xc, y - h * 0.5, txt, ha="center", va="center", fontsize=25, weight="bold", color=INK)
        elif r == 3:
            ax.text(xc, y - 0.04, "\n".join(textwrap.wrap(txt, 22 if LANG == "ru" else 24)), ha="center", va="top", fontsize=8.2, color=MID, linespacing=1.3)
        elif r == 7:
            ax.text(xc, y - h / 2, txt, ha="center", va="center", fontsize=15, weight="bold", color=PAPER, style="italic")
        else:
            ax.text(x0 + j * cw + 0.1, y - 0.12, "\n".join(textwrap.wrap(txt, wrapw)), ha="left", va="top",
                    fontsize=9.2, color=INK, linespacing=1.35, weight="bold" if r == 6 else "normal")
    y -= h
    if r not in (2, 6, 7):
        ax.plot([M, W - M], [y, y], color=INK if r in (1, 3) else LIGHT, lw=1.0 if r in (1, 3) else 0.8)
# column separators
yb = y + heights[7]
for j in range(1, 4):
    ax.plot([x0 + j * cw] * 2, [top - hdr_h + 0.0, yb], color=LIGHT, lw=0.8, zorder=0)
ax.plot([x0, x0], [top - 0.05, yb], color=LIGHT, lw=0.8, zorder=0)

# footer
ax.text(M, y - 0.38, T["foot"], fontsize=8.5, color=MID, va="center")
ax.text(W - M, y - 0.38, T["repo"], fontsize=9, color=INK, weight="bold", va="center", ha="right")
fig.savefig(OUT, dpi=150, facecolor=PAPER)
