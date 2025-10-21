"""
Constantes et configurations statiques de l'application
"""

THEMATIQUES = [
    {
        "nom": "Logistique",
        "endpoint": "/api/logistique",
        "description": "Distribution vaccins, stocks, actes"
    },
    {
        "nom": "Géographique", 
        "endpoint": "/api/geographique",
        "description": "Accès aux soins (pharmacies, médecins)"
    },
    {
        "nom": "Saisonnalité",
        "endpoint": "/api/saisonnalite", 
        "description": "Virus grippal hiver vs été"
    }
]