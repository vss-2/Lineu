split -l 1000000 sisvan_estado_nutricional_2021.csv x

for file in x*; do
  mv "$file" "$file.csv"
done

rm sisvan_estado_nutricional.csv
