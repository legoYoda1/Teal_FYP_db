
import random

singapore_roads_abbr = [
    "O",      # Orchard Road -> O
    "BT",     # Bukit Timah Road -> B T
    "H",      # Holland Road -> H
    "S",      # Serangoon Road -> S
    "T",      # Tampines Avenue 5 -> T
    "C",      # Cecil Street -> C
    "JW",     # Jurong West Street 91 -> J W
    "SEM",      # Sembawang Road -> S
    "UT",     # Upper Thomson Road -> U T
    "CH"       # Changi Road -> C
]

singapore_roads = [
"Orchard Road",
"Bukit Timah Road",
"Holland Road",
"Serangoon Road",
"Tampines Avenue 5",
"Cecil Street",
"Jurong West Street 91",
"Sembawang Road",
"Upper Thomson Road",
"Changi Road"
]

# INSERT INTO location_dim (location_id, location, zone, lamppost_id, road_type) VALUES
s = ''
s += 'INSERT INTO location_dim (location_id, location, zone, lamppost_id, road_type) VALUES \n'
    
letters = ['A', 'B', 'C', 'D', 'E', 'F']
for x in range(len(singapore_roads_abbr)):
    for i in range(1, 21):
        for j in range(len(letters)):
            landmark_id = f'{str(i).zfill(3)}{letters[j]}'
            road_type = ''
            if singapore_roads[x].__contains__('Road'):
                road_type = 'Road'
            if singapore_roads[x].__contains__('Street'):
                road_type = 'Street'
            if singapore_roads[x].__contains__('Ave'):
                road_type = 'Ave'
            
            s += f"('{singapore_roads_abbr[x]}{landmark_id}', '{singapore_roads[x]}', 0, '{landmark_id}', '{road_type}'), \n"
    
with open('filename.txt', 'w') as file:
    file.write(s)