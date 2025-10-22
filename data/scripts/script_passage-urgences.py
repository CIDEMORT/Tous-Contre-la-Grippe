import pandas as pd
import numpy as np


urgences = pd.read_csv('grippe-passages-aux-urgences-et-actes-sos-medecins-departement.csv', 
                       encoding='utf-8')
pauvrete = pd.read_csv('taux_de_pauvreté.csv', encoding='utf-8')
communes = pd.read_csv('communes-france-2025.csv', encoding='utf-8')


def normaliser_region(nom):
    """
    Fonction améliorée pour normaliser les noms de régions
    """
    if pd.isna(nom):
        return None
    
    nom = str(nom).strip()
    
    correspondances = {
        # Variations avec "et" vs "-"
        'Auvergne et Rhône-Alpes': 'Auvergne-Rhône-Alpes',
        'Auvergne-et-Rhône-Alpes': 'Auvergne-Rhône-Alpes',
        'Auvergne et Rhone-Alpes': 'Auvergne-Rhône-Alpes',
        'Bourgogne et Franche-Comté': 'Bourgogne-Franche-Comté',
        'Bourgogne-Franche-Comte': 'Bourgogne-Franche-Comté',
        
        # Variations avec espaces
        'Nouvelle Aquitaine': 'Nouvelle-Aquitaine',
        'Nouvelle aquitaine': 'Nouvelle-Aquitaine',
        
        # Variations avec accents
        "Provence-Alpes-Côte-d'Azur": "Provence-Alpes-Côte d'Azur",
        'Provence-Alpes-Cote-d\'Azur': "Provence-Alpes-Côte d'Azur",
        'Provence-Alpes-Cote d\'Azur': "Provence-Alpes-Côte d'Azur",
        
        # Variations Centre
        'Centre': 'Centre-Val de Loire',
        'Centre Val de Loire': 'Centre-Val de Loire',
        
        # Variations Île-de-France
        'Ile-de-France': 'Île-de-France',
        'Ile de France': 'Île-de-France',
        
        # La Réunion
        'Réunion': 'La Réunion',
        'Reunion': 'La Réunion',
        
        # Autres variations courantes
        'Pays de la Loire': 'Pays de la Loire',
        'Hauts-de-France': 'Hauts-de-France',
        'Grand Est': 'Grand Est',
        'Normandie': 'Normandie',
        'Bretagne': 'Bretagne',
        'Occitanie': 'Occitanie',
        'Corse': 'Corse',
        
        # DOM-TOM
        'Guadeloupe': 'Guadeloupe',
        'Martinique': 'Martinique',
        'Guyane': 'Guyane',
        'Mayotte': 'Mayotte',
    }
    
    return correspondances.get(nom, nom)

pauvrete['Region'] = pauvrete['Region'].apply(normaliser_region)
for reg in sorted(pauvrete['Region'].unique()):
    print(f"  - {reg}")


communes['reg_nom_clean'] = communes['reg_nom'].apply(normaliser_region)

pop_par_region = communes.groupby('reg_nom_clean')['population'].sum().reset_index()
pop_par_region.columns = ['Region', 'Population']

for reg in sorted(pop_par_region['Region'].unique()):
    pop = pop_par_region[pop_par_region['Region'] == reg]['Population'].values[0]
    print(f"  - {reg}: {pop:,} habitants")


urgences.columns = urgences.columns.str.strip()
urgences_tous_ages = urgences[urgences['Classe d\'âge'] == 'Tous âges'].copy()
urgences_tous_ages['Region_clean'] = urgences_tous_ages['Région'].apply(normaliser_region)

taux_par_region = urgences_tous_ages.groupby('Region_clean').agg({
    'Taux de passages aux urgences pour grippe': 'mean'
}).reset_index()

taux_par_region.columns = ['Region', 'Taux_moyen_passages_urgences']
df_avec_pop = taux_par_region.merge(pop_par_region, on='Region', how='left')

df_avec_pop['Passages_totaux_estimes'] = (
    df_avec_pop['Taux_moyen_passages_urgences'] * 
    df_avec_pop['Population'] / 100000
).round(0)

tableau_final = df_avec_pop.merge(
    pauvrete[['Region', 'Taux_pauvrete_pourcent']], 
    on='Region', 
    how='left'
)

tableau_final = tableau_final[[
    'Region',
    'Population',
    'Passages_totaux_estimes',
    'Taux_moyen_passages_urgences',
    'Taux_pauvrete_pourcent'
]]

tableau_final.columns = [
    'Région',
    'Population_totale',
    'Passages_urgences_total_estimé',
    'Taux_passages_pour_100k_hab',
    'Taux_pauvreté_%'
]

tableau_final['Passages_pour_1000_hab'] = (
    tableau_final['Passages_urgences_total_estimé'] / 
    tableau_final['Population_totale'] * 1000
).round(2)


for _, row in tableau_final.iterrows():
    missing = []
    if pd.isna(row['Population_totale']):
        missing.append('Population')
    if pd.isna(row['Taux_pauvreté_%']):
        missing.append('Taux pauvreté')
    if pd.isna(row['Taux_passages_pour_100k_hab']):
        missing.append('Taux passages')
    
    if missing:
        print(f"  - {row['Région']}: {', '.join(missing)}")

tableau_complet = tableau_final[
    tableau_final['Population_totale'].notna() & 
    tableau_final['Taux_pauvreté_%'].notna() & 
    tableau_final['Taux_passages_pour_100k_hab'].notna()
].copy()

dom_tom = ['Guadeloupe', 'Martinique', 'Guyane', 'La Réunion', 'Mayotte']
tableau_complet['Type'] = tableau_complet['Région'].apply(
    lambda x: 'DOM-TOM' if x in dom_tom else 'Métropole'
)



tableau_complet = tableau_complet.sort_values('Taux_pauvreté_%', ascending=False)

for _, row in tableau_complet.iterrows():
    print(f"{row['Région']} ({row['Type']})")
    print(f"  Population: {row['Population_totale']:,.0f} habitants")
    print(f"  Passages urgences: {row['Passages_urgences_total_estimé']:,.0f} ({row['Taux_passages_pour_100k_hab']:.1f}/100k hab)")
    print(f"  Taux pauvreté: {row['Taux_pauvreté_%']:.1f}%")
    print()


for i, (_, row) in enumerate(tableau_complet.nlargest(5, 'Taux_pauvreté_%').iterrows(), 1):
    print(f"{i}. {row['Région']}: {row['Taux_pauvreté_%']:.1f}% | Passages: {row['Taux_passages_pour_100k_hab']:.1f}/100k hab")

print("\n🔝 Top 5 - Plus de passages aux urgences:")
for i, (_, row) in enumerate(tableau_complet.nlargest(5, 'Taux_passages_pour_100k_hab').iterrows(), 1):
    print(f"{i}. {row['Région']}: {row['Taux_passages_pour_100k_hab']:.1f}/100k hab | Pauvreté: {row['Taux_pauvreté_%']:.1f}%")


tableau_final_save = tableau_complet.drop('Type', axis=1)

tableau_final_save.to_csv('tableau_pauvrete_urgences_population_complet.csv', 
                          index=False, encoding='utf-8')

tableau_metropole = tableau_complet[tableau_complet['Type'] == 'Métropole'].drop('Type', axis=1)
tableau_metropole.to_csv('tableau_pauvrete_urgences_METROPOLE.csv', 
                         index=False, encoding='utf-8')

if len(tableau_complet[tableau_complet['Type'] == 'DOM-TOM']) > 0:
    tableau_domtom = tableau_complet[tableau_complet['Type'] == 'DOM-TOM'].drop('Type', axis=1)
    tableau_domtom.to_csv('tableau_pauvrete_urgences_DOMTOM.csv', 
                          index=False, encoding='utf-8')