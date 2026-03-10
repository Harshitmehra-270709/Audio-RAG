import os

all_files = os.listdir('.')
print(all_files)

mp3_files = []
for file in all_files:
    if file.endswith('.mp3'):
        mp3_files.append(file)
counter = 1
for old_name in mp3_files:
    new_name = str(counter)+". "+old_name+ ".mp3"
    
    os.rename(old_name, new_name)
    
    print("Renamed", old_name, "to", new_name)
    
    counter = counter + 1