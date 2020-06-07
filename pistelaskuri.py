deadlines = [2.5, 2.75, 1.5, 4, 3]
pisteet = 0
deadline_6 = 4.5
alkupisteet = 67.25

for x in deadlines:
    pisteet = pisteet + x
    
print("Pisteitä on korotettu: " + str(pisteet))
print("Alkupisteet olivat: " + str(alkupisteet))
print("Viimeisen deadlinen täyttämisestä sai " + str(deadline_6))
print("Yhteispisteet ovat " + str(pisteet + deadline_6 + alkupisteet))