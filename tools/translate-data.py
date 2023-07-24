from csv import DictReader

start_year = 1960

years = []

for x in range(1960,2022):
    years.append(str(x))

# print(years)

csv_data = []

with open('./public_populations_export_2023-07-24_142322.csv', newline='') as csvfile:
    dict_reader = DictReader(csvfile)   
    csv_data = list(dict_reader)

new_dataset = []

for record in csv_data:
    for year in years:
        new_dataset.append(f"insert into populations (country, country_code, year, population) values ('{record['country']}', '{record['country_code']}', '{year}', {record[year]});")

# print(new_dataset)

file = open('insert_population_data.sql','w')
for record in new_dataset:
	file.write(record+"\n")
file.close()
    