import functions


dipoles = functions.create_system(5)
print(dipoles)
de = functions.calc_energy(1, 2, dipoles)
print('de', de)
a = functions.flip_spin(1, 1, de, 2.5, dipoles)
print(a)
