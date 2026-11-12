# DSP Notebooks

Physics-first explainers of wireless signal processing, written as Jupyter notebooks. Each notebook takes one technique, works through the math behind it, and checks that math with a compact NumPy simulation. Every section prints the theoretical prediction next to the measured value.

The explanatory text in the notebooks is in Russian. The code, plots and formulas work in any language.

## Notebooks

| Notebook | Topic | What you'll see |
|---|---|---|
| [`cdma_sim.ipynb`](notebooks/cdma_sim.ipynb) | **CDMA / DSSS** | Spreading with m-sequences and Gold codes, processing gain, code acquisition via FFT, narrowband jammer suppression, two users sharing one band, BER vs. BPSK |
| [`ldpc_sim.ipynb`](notebooks/ldpc_sim.ipynb) | **LDPC codes** | Tanner graph, Gallager (3,6) code, channel LLRs, sum-product and min-sum decoding, EXIT-chart threshold, BER/FER waterfall vs. the Shannon limit |
| [`lte_sim.ipynb`](notebooks/lte_sim.ipynb) | **LTE downlink PHY** | OFDM and the cyclic prefix, 3GPP EPA/EVA/ETU channels, ISI/ICI vs. CP length, CRS pilots and channel estimation, Doppler ICI, QAM BER in AWGN and fading, the LTE turbo code (QPP interleaver, log-MAP / max-log-MAP), turbo vs. LDPC, frequency diversity, OFDM vs. SC-FDMA PAPR |
| [`lora_sim.ipynb`](notebooks/lora_sim.ipynb) | **LoRa / CSS** | Chirp modulation, dechirp + FFT demodulation, SER for SF7–SF12 against non-coherent M-ary orthogonal theory, link budget and time-on-air, CFO/timing recovery from up- and down-chirps, tone jamming, cross-SF quasi-orthogonality |

The notebooks refer to each other. For example, LoRa's processing gain is compared with DSSS, and the LTE turbo code is benchmarked against the LDPC code at the same rate and block length.

## Structure of each notebook

1. Intro: the physical problem and the key equations.
2. A single **parameters cell** (SNR, spreading factor, bandwidth, channel profile, …).
3. A self-contained **primitives cell** (modulators, channels, decoders), with no dependencies beyond NumPy/SciPy.
4. Numbered simulation sections. Each has plots and printed theory-vs-simulation checks.
5. A comparison with the other notebooks.
6. **"Что покрутить"** ("Things to try"): parameter changes that show where things break.

## Running

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
jupyter notebook notebooks/        # or open in VS Code
```

The notebooks are committed with their outputs, so you can read them on GitHub without running anything. To re-execute one from the command line:

```bash
jupyter nbconvert --to notebook --execute --inplace notebooks/lora_sim.ipynb
```

Approximate run times on a laptop CPU: CDMA and LoRa take under a minute. LDPC and LTE take a few minutes, mostly in the iterative-decoder BER sweeps.

## Requirements

Python 3.10+, `numpy`, `scipy`, `matplotlib`, plus `ipykernel` / `nbconvert` / `nbformat` for running them (see [`requirements.txt`](requirements.txt)).
