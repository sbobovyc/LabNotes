clear;

[stable_time, stable_data] = import_csv('shielded_differential/1plate_demo_stable.csv');
[loaded_time, loaded_data] = import_csv('shielded_differential/1plate_demo_acloaded.csv');
[cable_time, cable_data] = import_csv('shielded_differential/1plate_demo_cable_vibrate.csv');

[hand2plate_time, hand2plate_data] = import_csv('shielded_differential/1plate_demo_hand2plate.csv');
[hand2shield_time, hand2shield_data] = import_csv('shielded_differential/1plate_demo_hand2shield.csv');


figure; hold all; plot (stable_time, stable_data);
figure; hold all; plot (loaded_time, loaded_data);
figure; hold all; plot (cable_time, cable_data);

figure; hold all; plot (hand2plate_time, hand2plate_data, 'b');
 plot (hand2shield_time, hand2shield_data, 'r');

