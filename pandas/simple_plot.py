import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("2016_10_05_Left.csv", sep=",")

plt.plot(df["RemLogic_Relative_Time_sec"], df["Capacitor_1"])
plt.plot(df["RemLogic_Relative_Time_sec"], df["Capacitor_2"])
plt.plot(df["RemLogic_Relative_Time_sec"], df["Capacitor_3"])
plt.plot(df["RemLogic_Relative_Time_sec"], df["Acc_X"])
plt.plot(df["RemLogic_Relative_Time_sec"], df["Acc_Y"])
plt.plot(df["RemLogic_Relative_Time_sec"], df["Acc_Z"])

plt.legend()
plt.grid(True)
plt.show()


