import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Function to calculate peak oxygenation (StO2_peak)
def calculate_peak_oxygenation(skin_contribution, adipose_contribution, macrovasc_contribution, arterioles_contribution, venules_contribution, capillary_contribution, myoglobin_ratio):
    # Tissue layer contributions
    muscle_contribution = 100 - (skin_contribution + adipose_contribution)  # Remaining contribution for muscle layer

    # Oxygenation levels
    adipose_oxygenation = 70
    skin_oxygenation_peak = 80
    macro_arterial_oxygenation = 98
    macro_venous_oxygenation = 60
    arterioles_oxygenation = 95
    venules_oxygenation = 70
    capillaries_oxygenation = 75
    myoglobin_oxygenation = 95

    # Normalize microcirculation components to ensure total = 100%
    total_micro_circulation = arterioles_contribution + venules_contribution + capillary_contribution
    if total_micro_circulation != 100:
        scale_factor = 100 / total_micro_circulation
        arterioles_contribution *= scale_factor
        venules_contribution *= scale_factor
        capillary_contribution *= scale_factor

    # Split capillary contribution into capillaries and myoglobin
    capillary_myoglobin_contribution = capillary_contribution * (myoglobin_ratio / 100)
    capillaries_only_contribution = capillary_contribution * (1 - myoglobin_ratio / 100)

    # Signals from each component
    macrovasc_signal = (macrovasc_contribution / 100) * ((macro_arterial_oxygenation + macro_venous_oxygenation) / 2)
    arterioles_signal = (arterioles_contribution / 100) * arterioles_oxygenation
    venules_signal = (venules_contribution / 100) * venules_oxygenation
    capillary_signal = (capillaries_only_contribution / 100) * capillaries_oxygenation
    myoglobin_signal = (capillary_myoglobin_contribution / 100) * myoglobin_oxygenation

    muscle_signal = macrovasc_signal + arterioles_signal + venules_signal + capillary_signal + myoglobin_signal

    # Add skin and adipose contributions
    skin_signal = (skin_contribution / 100) * skin_oxygenation_peak
    adipose_signal = (adipose_contribution / 100) * adipose_oxygenation

    total_signal = muscle_signal * (muscle_contribution / 100) + skin_signal + adipose_signal
    return min(total_signal, 100)

# Function to calculate minimum oxygenation (StO2_min)
def calculate_min_oxygenation(skin_contribution, adipose_contribution, macrovasc_contribution, arterioles_contribution, venules_contribution, capillary_contribution, myoglobin_ratio):
    # Tissue layer contributions
    muscle_contribution = 100 - (skin_contribution + adipose_contribution)  # Remaining contribution for muscle layer

    # Oxygenation levels
    adipose_oxygenation = 70
    skin_oxygenation_min = 10
    macro_arterial_oxygenation = 98
    macro_venous_oxygenation = 25
    arterioles_oxygenation = 50
    venules_oxygenation = 5
    capillaries_oxygenation = 10
    myoglobin_oxygenation = 0

    # Normalize microcirculation components to ensure total = 100%
    total_micro_circulation = arterioles_contribution + venules_contribution + capillary_contribution
    if total_micro_circulation != 100:
        scale_factor = 100 / total_micro_circulation
        arterioles_contribution *= scale_factor
        venules_contribution *= scale_factor
        capillary_contribution *= scale_factor

    # Split capillary contribution into capillaries and myoglobin
    capillary_myoglobin_contribution = capillary_contribution * (myoglobin_ratio / 100)
    capillaries_only_contribution = capillary_contribution * (1 - myoglobin_ratio / 100)

    # Signals from each component
    macrovasc_signal = (macrovasc_contribution / 100) * ((macro_arterial_oxygenation + macro_venous_oxygenation) / 2)
    arterioles_signal = (arterioles_contribution / 100) * arterioles_oxygenation
    venules_signal = (venules_contribution / 100) * venules_oxygenation
    capillary_signal = (capillaries_only_contribution / 100) * capillaries_oxygenation
    myoglobin_signal = (capillary_myoglobin_contribution / 100) * myoglobin_oxygenation

    muscle_signal = macrovasc_signal + arterioles_signal + venules_signal + capillary_signal + myoglobin_signal

    # Add skin and adipose contributions
    skin_signal = (skin_contribution / 100) * skin_oxygenation_min
    adipose_signal = (adipose_contribution / 100) * adipose_oxygenation

    total_signal = muscle_signal * (muscle_contribution / 100) + skin_signal + adipose_signal
    return min(total_signal, 100)

# Hardcoded data from provided table
example_data = pd.DataFrame({
    "Time": [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 310, 320, 330, 340, 350, 360, 370, 380, 390, 400, 410, 420, 430, 440, 450, 460, 470, 480, 490, 500, 510, 520, 530, 540, 550],
    "Oxygenation": [61, 62, 62, 63, 64, 65, 65, 64, 62, 59, 56, 54, 51, 48, 46, 43, 41, 38, 36, 34, 32, 30, 28, 27, 25, 24, 22, 21, 19, 18, 17, 17, 16, 16, 15, 14, 14, 14, 13, 13, 13, 14, 14, 15, 30, 52, 62, 66, 70, 72, 73, 74, 74, 74, 73]
})

# Streamlit interface
st.title('Oxygenation Range Simulation')

# Section: Skin Layer
with st.expander("Skin Layer"):
    skin_contribution = st.slider(
        "Skin Layer Contribution (%), oxygenation is set at 80'%' at rest and 10'%' at end of occlusion:",
        0, 50, 1, step=1,
        help="Skin contribution as a percentage of total signal."
    )

# Section: Adipose Layer
with st.expander("Adipose Layer"):
    adipose_contribution = st.slider(
        "Adipose Layer Contribution (%), oxygenation is set at 70'%':",
        0, 100, 1, step=1,
        help="Adipose tissue contribution as a percentage of total signal."
    )

# Section: Macrovasculature
with st.expander("Macrovasculature"):
    macrovasc_contribution = st.slider(
        "Macrovasculature signal Contribution (%):",
        0, 40, 0, step=1,
        help="Contribution from arteries (98%) and veins (60% at rest, 25% at end of occlusion)."
    )

# Section: Muscle Layer
with st.expander("Muscle Layer"):
    arterioles_contribution = st.slider(
        "Arterioles Contribution (%), oxygenation is set at 95% at rest and 50% at occlusion:",
        5, 50, 10, step=1,
        help="Arterioles contribution as a percentage of microcirculation."
    )
    venules_contribution = st.slider(
        "Venules Contribution (%), oxygenation is set at 70% at rest and 5% at occlusion:",
        5, 50, 10, step=1,
        help="Venules contribution as a percentage of microcirculation."
    )
    capillary_contribution = st.slider(
        "Capillaries Contribution (%), oxygenation is set at 75% at rest and 10% at occlusion::",
        5, 50, 80, step=1,
        help="Capillaries contribution as a percentage of microcirculation."
    )
    myoglobin_ratio = st.slider(
        "Myoglobin Contribution (%), oxygenation is set at 95% at rest and 0% at occlusion::",
        0, 100, 70, step=1,
        help="Percentage of capillaries contribution allocated to myoglobin."
    )

# Calculate peak and minimum oxygenation
peak_oxygenation = calculate_peak_oxygenation(
    skin_contribution, adipose_contribution, macrovasc_contribution,
    arterioles_contribution, venules_contribution, capillary_contribution, myoglobin_ratio
)
min_oxygenation = calculate_min_oxygenation(
    skin_contribution, adipose_contribution, macrovasc_contribution,
    arterioles_contribution, venules_contribution, capillary_contribution, myoglobin_ratio
)

# Adjust the oxygenation values to match the new peak and minimum
original_min = example_data['Oxygenation'].min()
original_max = example_data['Oxygenation'].max()

# Normalize the data to a 0-1 range
normalized_oxygenation = (example_data['Oxygenation'] - original_min) / (original_max - original_min)

# Scale to the new range defined by min_oxygenation and peak_oxygenation
adjusted_oxygenation = normalized_oxygenation * (peak_oxygenation - min_oxygenation) + min_oxygenation
example_data['Adjusted_Oxygenation'] = adjusted_oxygenation

# Display results
st.write(f"**Expected Peak Oxygenation (StO2 Peak):** {peak_oxygenation:.2f}%")
st.write(f"**Expected Minimum Oxygenation (StO2 Minimum):** {min_oxygenation:.2f}%")

# Plot oxygenation range including adjusted data
plt.figure(figsize=(10, 6))
plt.axhline(y=peak_oxygenation, color='g', linestyle='--', label=f'Peak Oxygenation = {peak_oxygenation:.2f}%')
plt.axhline(y=min_oxygenation, color='r', linestyle='--', label=f'Minimum Oxygenation = {min_oxygenation:.2f}%')
plt.plot(example_data['Time'], example_data['Adjusted_Oxygenation'], label="Oxygenation", color="b")
plt.ylim(0, 100)  # Keep the y-axis fixed to 0-100
plt.title("Oxygenation Range Simulation")
plt.ylabel("Oxygenation (%)")
plt.xlabel("Time")
plt.legend()
st.pyplot(plt)
