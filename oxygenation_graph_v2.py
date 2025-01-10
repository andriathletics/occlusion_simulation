import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Function to calculate peak oxygenation (StO2_peak)
def calculate_peak_oxygenation(macrovasc_contribution, adipose_contribution, skin_contribution, myoglobin_min_contribution, myoglobin_max_contribution, arterioles_contribution, venules_contribution):
    muscle_contribution = 100 - (adipose_contribution + skin_contribution)  # Remaining contribution for muscle layer

    adipose_oxygenation = 70  # Adipose oxygenation is always 70%
    skin_oxygenation_peak = 80  # Skin peak oxygenation is 80%

    macro_arterial_oxygenation = 100
    macro_venous_oxygenation = 70
    myoglobin_oxygenation = 100
    arterioles_oxygenation = 95
    venules_oxygenation = 70
    myoglobin_contribution = np.interp(100, [0, 100], [myoglobin_min_contribution, myoglobin_max_contribution])

    macrovasc_signal = (macrovasc_contribution / 100) * ((macro_arterial_oxygenation + macro_venous_oxygenation) / 2)
    myoglobin_signal = (myoglobin_contribution / 100) * myoglobin_oxygenation
    arterioles_signal = (arterioles_contribution / 100) * arterioles_oxygenation
    venules_signal = (venules_contribution / 100) * venules_oxygenation
    capillaries_contribution = 100 - (myoglobin_contribution + arterioles_contribution + venules_contribution)
    capillaries_signal = (capillaries_contribution / 100) * venules_oxygenation

    muscle_signal = macrovasc_signal + myoglobin_signal + arterioles_signal + venules_signal + capillaries_signal

    # Adding skin and adipose contributions
    skin_signal = (skin_contribution / 100) * skin_oxygenation_peak
    adipose_signal = (adipose_contribution / 100) * adipose_oxygenation

    total_signal = muscle_signal * (muscle_contribution / 100) + skin_signal + adipose_signal
    return min(total_signal, 100)

# Function to calculate minimum oxygenation (StO2_min)
def calculate_min_oxygenation(macrovasc_contribution, adipose_contribution, skin_contribution, myoglobin_min_contribution, myoglobin_max_contribution, arterioles_contribution, venules_contribution):
    muscle_contribution = 100 - (adipose_contribution + skin_contribution)  # Remaining contribution for muscle layer

    adipose_oxygenation = 70  # Adipose oxygenation is always 70%
    skin_oxygenation_min = 10  # Skin minimum oxygenation is 10%

    macro_arterial_oxygenation = 100
    macro_venous_oxygenation = 25
    myoglobin_oxygenation = 0
    arterioles_oxygenation = 100
    venules_oxygenation = 25
    myoglobin_contribution = np.interp(0, [0, 100], [myoglobin_min_contribution, myoglobin_max_contribution])

    macrovasc_signal = (macrovasc_contribution / 100) * ((macro_arterial_oxygenation + macro_venous_oxygenation) / 2)
    myoglobin_signal = (myoglobin_contribution / 100) * myoglobin_oxygenation
    arterioles_signal = (arterioles_contribution / 100) * arterioles_oxygenation
    venules_signal = (venules_contribution / 100) * venules_oxygenation
    capillaries_contribution = 100 - (myoglobin_contribution + arterioles_contribution + venules_contribution)
    capillaries_signal = (capillaries_contribution / 100) * venules_oxygenation

    muscle_signal = macrovasc_signal + myoglobin_signal + arterioles_signal + venules_signal + capillaries_signal

    # Adding skin and adipose contributions
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
        0, 50, 5, step=1,
        help="Skin contribution as a percentage of total signal."
    )

# Section: Adipose Layer
with st.expander("Adipose Layer"):
    adipose_contribution = st.slider(
        "Adipose Layer Contribution (%), oxygenation is set at 70'%':",
        0, 100, 5, step=1,
        help="Adipose tissue contribution as a percentage of total signal."
    )

# Section: Macrovasculature
with st.expander("Macrovasculature"):
    macrovasc_contribution = st.slider(
        "Macrovasculature signal Contribution (%):",
        0, 40, 0, step=1,
        help="Contribution from arteries (100%) and veins (70% at rest, 25% at end of occlusion)."
    )

# Section: Muscle Layer
with st.expander("Muscle Layer"):
    myoglobin_min_contribution = st.slider(
        "Myoglobin signal Contribution at end of occlusion (%), oxygenation set at 0%:",
        10, 80, 80, step=1,
        help="Oxygenation assumed 0% at end of occlusion."
    )
    myoglobin_max_contribution = st.slider(
        "Myoglobin signal Contribution at rest (%), oxygenation set at 100%:",
        10, 80, 30, step=1,
        help="Oxygenation assumed 100% at rest."
    )
    arterioles_contribution = st.slider(
        "Arterioles signal Contribution (%), oxygenation is set at 95%:",
        5, 30, 10, step=1,
        help="Signal contribution from arterioles."
    )
    venules_contribution = st.slider(
        "Venules signal Contribution (%), oxygenation is set at 70 at rest and end 25%:",
        5, 70, 10, step=1,
        help="Signal contribution from venules."
    )

# Calculate peak and minimum oxygenation
peak_oxygenation = calculate_peak_oxygenation(
    macrovasc_contribution, adipose_contribution, skin_contribution, myoglobin_min_contribution, myoglobin_max_contribution, arterioles_contribution, venules_contribution
)
min_oxygenation = calculate_min_oxygenation(
    macrovasc_contribution, adipose_contribution, skin_contribution, myoglobin_min_contribution, myoglobin_max_contribution, arterioles_contribution, venules_contribution
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
