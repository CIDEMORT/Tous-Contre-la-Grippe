import pandas as pd

pharmacies = pd.read_csv('santefr-lieux-vaccination-grippe-pharmacie.csv', 
                         sep=';', encoding='utf-8')
communes = pd.read_csv('communes-france-2025.csv', encoding='utf-8')

pharmacies_par_cp = pharmacies.groupby('Adresse_codepostal').size().reset_index(name='nombre_pharmacies')

communes_expanded = communes.assign(
    code_postal=communes['codes_postaux'].str.split(', ')
).explode('code_postal')
communes_expanded['code_postal'] = pd.to_numeric(communes_expanded['code_postal'], errors='coerce')

communes_clean = communes_expanded[['code_postal', 'population']].dropna()

resultat = pharmacies_par_cp.merge(
    communes_clean, 
    left_on='Adresse_codepostal', 
    right_on='code_postal',
    how='left'
)

resultat = resultat.groupby('Adresse_codepostal').agg({
    'nombre_pharmacies': 'first',
    'population': 'sum'
}).reset_index()

resultat.columns = ['code_postal', 'nombre_pharmacies', 'population']


populations_villes = {
    'Paris': 2102650,
    'Marseille': 873076,
    'Lyon': 522969
}

paris_arr = resultat[(resultat['code_postal'] >= 75001) & (resultat['code_postal'] <= 75020)]
marseille_arr = resultat[(resultat['code_postal'] >= 13001) & (resultat['code_postal'] <= 13016)]
lyon_arr = resultat[(resultat['code_postal'] >= 69001) & (resultat['code_postal'] <= 69009)]

paris_regroupe = pd.DataFrame([{
    'code_postal': 75000,
    'nombre_pharmacies': paris_arr['nombre_pharmacies'].sum(),
    'population': populations_villes['Paris']
}])

marseille_regroupe = pd.DataFrame([{
    'code_postal': 13000,
    'nombre_pharmacies': marseille_arr['nombre_pharmacies'].sum(),
    'population': populations_villes['Marseille']
}])

lyon_regroupe = pd.DataFrame([{
    'code_postal': 69000,
    'nombre_pharmacies': lyon_arr['nombre_pharmacies'].sum(),
    'population': populations_villes['Lyon']
}])

resultat_filtre = resultat[~((resultat['code_postal'] >= 75001) & (resultat['code_postal'] <= 75020))]
resultat_filtre = resultat_filtre[~((resultat_filtre['code_postal'] >= 13001) & (resultat_filtre['code_postal'] <= 13016))]
resultat_filtre = resultat_filtre[~((resultat_filtre['code_postal'] >= 69001) & (resultat_filtre['code_postal'] <= 69009))]

resultat_final = pd.concat([resultat_filtre, paris_regroupe, marseille_regroupe, lyon_regroupe], ignore_index=True)

resultat_final = resultat_final.sort_values('code_postal').reset_index(drop=True)
villes = resultat_final[resultat_final['code_postal'].isin([75000, 13000, 69000])]

top10 = resultat_final.nlargest(10, 'nombre_pharmacies')[['code_postal', 'nombre_pharmacies', 'population']]

resultat_final.to_csv('pharmacies_par_code_postal_final.csv', index=False)
