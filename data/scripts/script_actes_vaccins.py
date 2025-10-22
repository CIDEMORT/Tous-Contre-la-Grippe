import pandas as pd
import numpy as np

couv_2021 = pd.read_csv('couverture-2021.csv', encoding='utf-8')
couv_2022 = pd.read_csv('couverture-2022.csv', encoding='utf-8')
couv_2023 = pd.read_csv('couverture-2023.csv', encoding='utf-8')
couv_2024 = pd.read_csv('couverture-2024.csv', encoding='utf-8')

couv_2021['annee'] = 2021
couv_2022['annee'] = 2022
couv_2023['annee'] = 2023
couv_2024['annee'] = 2024

df_complet = pd.concat([couv_2021, couv_2022, couv_2023, couv_2024], ignore_index=True)


df_actes = df_complet[df_complet['variable'] == 'ACTE(VGP)'].copy()

actes_total = df_actes.groupby(['region', 'code', 'annee'])['valeur'].sum().reset_index()
tableau_actes = actes_total.pivot(index=['region', 'code'], 
                                   columns='annee', 
                                   values='valeur').reset_index()

tableau_actes.columns.name = None
tableau_actes = tableau_actes.rename(columns={
    2021: 'Actes_2021',
    2022: 'Actes_2022',
    2023: 'Actes_2023',
    2024: 'Actes_2024'
})

tableau_actes['Evolution_2021-2024'] = (
    tableau_actes['Actes_2024'] - tableau_actes['Actes_2021']
)
tableau_actes['Evolution_%'] = (
    (tableau_actes['Actes_2024'] - tableau_actes['Actes_2021']) / 
    tableau_actes['Actes_2021'] * 100
).round(2)

actes_par_age = df_actes.pivot_table(
    index=['region', 'code'], 
    columns=['annee', 'groupe'], 
    values='valeur'
).reset_index()

actes_par_age.columns = ['_'.join(map(str, col)).strip('_') if isinstance(col, tuple) else col 
                         for col in actes_par_age.columns]

tableau_actes = tableau_actes.sort_values('code')
actes_par_age = actes_par_age.sort_values('code')

df_doses = df_complet[df_complet['variable'] == 'DOSES(J07E1)'].copy()

doses_total = df_doses.groupby(['region', 'code', 'annee'])['valeur'].sum().reset_index()
tableau_doses = doses_total.pivot(index=['region', 'code'], 
                                   columns='annee', 
                                   values='valeur').reset_index()

tableau_doses.columns.name = None
tableau_doses = tableau_doses.rename(columns={
    2021: 'Doses_2021',
    2022: 'Doses_2022',
    2023: 'Doses_2023',
    2024: 'Doses_2024'
})

tableau_doses['Evolution_2021-2024'] = (
    tableau_doses['Doses_2024'] - tableau_doses['Doses_2021']
)
tableau_doses['Evolution_%'] = (
    (tableau_doses['Doses_2024'] - tableau_doses['Doses_2021']) / 
    tableau_doses['Doses_2021'] * 100
).round(2)

doses_par_age = df_doses.pivot_table(
    index=['region', 'code'], 
    columns=['annee', 'groupe'], 
    values='valeur'
).reset_index()

doses_par_age.columns = ['_'.join(map(str, col)).strip('_') if isinstance(col, tuple) else col 
                         for col in doses_par_age.columns]

tableau_doses = tableau_doses.sort_values('code')
doses_par_age = doses_par_age.sort_values('code')


tableau_comparatif = tableau_actes[['region', 'code', 'Actes_2021', 'Actes_2022', 'Actes_2023', 'Actes_2024']].merge(
    tableau_doses[['region', 'code', 'Doses_2021', 'Doses_2022', 'Doses_2023', 'Doses_2024']],
    on=['region', 'code']
)

tableau_comparatif['Ratio_2021'] = (tableau_comparatif['Doses_2021'] / tableau_comparatif['Actes_2021']).round(2)
tableau_comparatif['Ratio_2022'] = (tableau_comparatif['Doses_2022'] / tableau_comparatif['Actes_2022']).round(2)
tableau_comparatif['Ratio_2023'] = (tableau_comparatif['Doses_2023'] / tableau_comparatif['Actes_2023']).round(2)
tableau_comparatif['Ratio_2024'] = (tableau_comparatif['Doses_2024'] / tableau_comparatif['Actes_2024']).round(2)


tableau_actes.to_csv('evolution_ACTES_vaccination_2021-2024.csv', index=False, encoding='utf-8')

tableau_doses.to_csv('evolution_DOSES_vaccination_2021-2024.csv', index=False, encoding='utf-8')

actes_par_age.to_csv('evolution_ACTES_par_age_2021-2024.csv', index=False, encoding='utf-8')

doses_par_age.to_csv('evolution_DOSES_par_age_2021-2024.csv', index=False, encoding='utf-8')

tableau_comparatif.to_csv('comparatif_ACTES_vs_DOSES_2021-2024.csv', index=False, encoding='utf-8')

top_hausse_actes = tableau_actes.nlargest(5, 'Evolution_%')[['region', 'Actes_2021', 'Actes_2024', 'Evolution_%']]

top_baisse_actes = tableau_actes.nsmallest(5, 'Evolution_%')[['region', 'Actes_2021', 'Actes_2024', 'Evolution_%']]
evolution_actes = ((tableau_actes['Actes_2024'].sum() - tableau_actes['Actes_2021'].sum()) / 
                   tableau_actes['Actes_2021'].sum() * 100)

top_hausse_doses = tableau_doses.nlargest(5, 'Evolution_%')[['region', 'Doses_2021', 'Doses_2024', 'Evolution_%']]

top_baisse_doses = tableau_doses.nsmallest(5, 'Evolution_%')[['region', 'Doses_2021', 'Doses_2024', 'Evolution_%']]

evolution_doses = ((tableau_doses['Doses_2024'].sum() - tableau_doses['Doses_2021'].sum()) / 
                   tableau_doses['Doses_2021'].sum() * 100)
