from matplotlib import pyplot as plt
import numpy as np




x_71 = [0, 0, 0, 0, 0, 0, 0, 0, 0]

x_5 = [1, 1, 1, 1, 1, 1, 1, 1, 1]

x_57 = [2, 2, 2, 2, 2, 2, 2, 2, 2]

x_577 = [3, 3, 3]




magnitudes_10x_dark = np.absolute([-1.7075, -2.0275, -2.085, -2.61, -1.3, -1.25, -1.3, -1.71, -2.9375])

magnitudes_100x_dark = np.absolute([-1.2375, -1.2525, -1.3175])

magnitudes_3x3_low_exp = np.absolute([ -0.815, -1.055,  -1.0125,  -0.968,  -1.4175,  -0.757,  -0.8375,  -1.13,  -1.24])

magnitudes_3x3_high_exp = np.absolute([-1.03,  -1.0975,  -0.722,  -1.0325,  -1.13,  -0.8975,  -1.0325,  -0.792,  -0.865])

magnitudes_3x3_half_high_exp = np.absolute([-0.9675,  -0.77,  -0.8775,  -1.025,  -1.1175,  -0.8275,  -0.93,  -0.817, -0.8, ])

magnitudes_3x3_half_low_exp = np.absolute([ -1.1025,  -1.07,  -0.86,  -0.90,  -1.2375,  -1.0475, -0.94,  -1.0725,  -1.1125])


plt.title("Exposure time vs Average Magnitudes (Dark_pf Corrected)")
plt.plot(x_71, magnitudes_3x3_low_exp, 'o', label="3x3 White Low Exposure")
plt.plot(x_5, magnitudes_3x3_high_exp, 'o', label="3x3 White High Exposure")
plt.plot(x_71, magnitudes_3x3_half_low_exp, 'o', label="3x3 0.5x White Low Exposure")
plt.plot(x_5, magnitudes_3x3_half_high_exp, 'o', label="3x3 0.5x White High Exposure")
plt.plot(x_57, magnitudes_10x_dark, 'o', label="10x")
plt.plot(x_577, magnitudes_100x_dark, 'o', label="100x")
plt.xticks([0,1,2,3], ['0.7124', '5.7479', '57.4899', '574.5897'])
plt.ylabel("Absolute Magnitude in Row Dimming")
plt.xlabel("Exposure Time (ms)")

plt.legend()
plt.show()