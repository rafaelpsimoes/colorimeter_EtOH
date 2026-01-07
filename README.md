# Low-Cost Portable Colorimeter for Indirect Ethanol Determination

This repository provides the complete set of hardware designs, firmware, and data-analysis scripts required to replicate the portable colorimeter described in the manuscript:

**Low-Cost Portable Colorimeter for Indirect Determination of Ethanol Concentration via Dichromate Oxidation**

The repository is intended to ensure **full reproducibility**, **methodological transparency**, and **low-cost accessibility**, in accordance with the scope and recommendations of *Hardware* (MDPI). All files necessary for device construction, operation, and data processing are made publicly available.

---

## Purpose and Scope

The proposed system is an open-hardware analytical device designed for indirect ethanol determination in aqueous solutions and simple beverage matrices. The instrument combines low-cost optical components, a microcontroller-based acquisition system, and open-source computational analysis to emulate spectrophotometric measurements in the visible range.

This repository supports:
- replication of the hardware design;
- execution of the firmware for data acquisition;
- processing of raw optical data into absorbance-like spectra;
- construction of calibration curves;
- estimation of ethanol concentration in unknown samples.

---

## Analytical Principle

Ethanol concentration is determined **indirectly** via its oxidation in acidic medium in the presence of potassium dichromate. The reduction of dichromate ions (Cr₂O₇²⁻) to Cr³⁺ produces a characteristic color change, with an absorption band centered around **595 nm**. Within the linear range of the method, the color intensity is proportional to the ethanol concentration.

**Important limitation:** the device does not measure ethanol directly. The analytical signal originates from the oxidation reaction products, and other oxidizable species may interfere depending on the sample matrix. This limitation is explicitly discussed in the associated manuscript.

---

## Repository Structure
├── hardware/  
│ ├── pcb_eagle/ # PCB layout designed using Autodesk Eagle (single-layer)  
│ ├── pcb_graphic/ # Alternative PCB mask with wider traces for ultra-low-cost fabrication  
│ ├── enclosure_stl/ # 3D-printable enclosure files (STL)  
│ └── schematics/ # Electronic schematics and wiring diagrams (PDF)  
│  
├── firmware/  
│ └── espec.ino # Arduino firmware for wavelength and transmittance acquisition  
│  
├── software/  
│ ├── etoh_concentrations.py # Calibration curve construction and spectral analysis  
│ ├── etoh_sample.py # Ethanol concentration estimation for unknown samples  
│ └── example_data/ # Example input files and formatting templates  
│  
├── documentation/  
│ ├── assembly_guide.pdf # Device assembly instructions  
│ └── operating_guide.pdf # Operating workflow and data-processing description  
│  
└── README.md  

---

## PCB Design Options and Fabrication Accessibility

Two functionally equivalent PCB layouts are provided to accommodate different fabrication constraints:

1. **Standard PCB layout (Eagle):**  
   Designed using Autodesk Eagle and optimized for compact integration and fabrication through conventional low-cost PCB manufacturing services.

2. **Graphic-mask PCB layout (wide traces):**  
   Developed using general-purpose graphic design software, featuring wider and more widely spaced conductive traces. This version facilitates ultra-low-cost fabrication approaches, such as manual toner transfer or direct printing, increasing robustness against fabrication defects.

Both PCB versions implement the same electronic circuit and were validated using the same experimental workflow.

---

## Operating Workflow Overview

### Step 1 — Sample Preparation
Prepare:
- a **blank solution** (0% ethanol), used as reference;
- ethanol standards covering the linear range of the method;
- unknown samples prepared according to the protocol described in the manuscript.

### Step 2 — Data Acquisition (Firmware)
1. Upload the firmware `firmware/espec.ino` to an Arduino-compatible board using the Arduino IDE.
2. Run the acquisition routine and open the Serial Monitor.
3. Copy the serial output (wavelength and transmittance values) and save it as plain text files.

### Step 3 — Required Input Files for Python Scripts

The Python scripts operate on plain text files containing wavelength–transmittance data:

- `ref.txt`  
  Reference measurement corresponding to the **blank (0% ethanol)**.

- Calibration files  
  One file per ethanol standard concentration (e.g., `0_5.txt`, `1_0.txt`, `1_5.txt`).

- Sample file(s)  
  Files corresponding to unknown samples (e.g., `sample_01.txt`).

Examples of correct file structure and formatting are provided in `software/example_data/`.

### Step 4 — Data Processing and Analysis
- `etoh_concentrations.py`  
  Converts transmittance to absorbance-like signals, performs spectral fitting, constructs calibration curves, and exports calibration parameters.

- `etoh_sample.py`  
  Applies calibration parameters to unknown samples and estimates ethanol concentration.

The scripts generate processed data tables and graphical outputs (spectra, calibration plots, and concentration results), consistent with the figures and tables presented in the manuscript.

---

## Validation and Performance

The portable colorimeter was validated by comparison with a commercial UV–Vis spectrophotometer. The results demonstrate linear calibration behavior (R² ≈ 0.99 within the tested range) and acceptable relative errors for alcoholic beverage samples analyzed under controlled conditions.

Detailed validation results and statistical analyses are presented in the associated publication.

---

## Safety Considerations

- Potassium dichromate and acidic solutions are hazardous chemicals.
- Appropriate personal protective equipment (PPE) must be used.
- Chromium-containing waste must be disposed of according to institutional and local regulations.

---

## Data and File Availability

All hardware designs, firmware, and software required to replicate the device and reproduce the experimental workflow are provided as supplementary materials and are available in this public repository:

**GitHub repository:** https://github.com/rafaelpsimoes/colorimeter_EtOH

---

## How to Cite

If you use this repository or any of its contents (hardware designs, firmware, or software), please cite the associated manuscript.  
A `CITATION.cff` file is included to facilitate citation export directly from GitHub.

---

## Intended Use

This repository is provided to support transparency, reproducibility, and academic use of the hardware and software described in the associated manuscript.
