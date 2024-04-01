mass = ['M500','M750','M1000','M1250','M1500','M1750','M2000','M2500','M3000','M4000']
mass_err = ['M750','M4000']
Xmass = [500, 750, 1000, 1250, 1500, 1750, 2000, 2500, 3000, 4000]

new_Xmass = Xmass[:]

for err in mass_err:
    index = mass.index(err)
    new_Xmass.remove(Xmass[index])

print("Original Xmass:", Xmass)
print("New Xmass:", new_Xmass)

