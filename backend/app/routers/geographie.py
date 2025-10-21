from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from typing import Optional
from app.models.response_models import (
    AccessibilitePharmaciesResponse,
    EvolutionActesAgeResponse,
    EvolutionActesRegionResponse,
    EvolutionDosesAgeResponse,        # ← AJOUTER
    EvolutionDosesRegionResponse,     # ← AJOUTER
    RepartitionLieuVaccinationResponse # ← AJOUTER
)

router = APIRouter()

# ============================================
# GÉOGRAPHIE - Routes spécifiques
# ============================================

@router.get("/accessibilite-pharmacies", response_model=AccessibilitePharmaciesResponse)
async def get_accessibilite_pharmacies(
    db: Session = Depends(get_db),
    code_postal: Optional[str] = Query(None, description="Filtrer par code postal"),
    limit: int = Query(100, ge=1, le=1000)
):
    # ... ton code existant
    """
    Accessibilité des centres de vaccination (pharmacies uniquement) selon la population
    
    Graphique: Barème
    Format Chart.js: Gauge / Bar chart
    """
    query = "SELECT * FROM accessibilite_pharmacies WHERE 1=1"
    
    if code_postal:
        query += f" AND code_postal = '{code_postal}'"
    
    query += f" LIMIT {limit}"
    
    results = db.execute(text(query)).fetchall()
    
    # Conversion en dictionnaires
    data = []
    for row in results:
        data.append({
            "nombre_pharmacies": row[1],
            "population": row[2],
            "code_postal": row[3],
            "ratio": round(row[2] / row[1], 2) if row[1] > 0 else 0  # population par pharmacie
        })
    
    # Format pour Chart.js (Bar chart horizontal)
    chartjs_format = {
        "type": "bar",
        "data": {
            "labels": [d["code_postal"] for d in data],
            "datasets": [{
                "label": "Population par pharmacie",
                "data": [d["ratio"] for d in data],
                "backgroundColor": "rgba(54, 162, 235, 0.5)",
                "borderColor": "rgba(54, 162, 235, 1)",
                "borderWidth": 1
            }]
        },
        "options": {
            "indexAxis": "y",  # Horizontal bars
            "responsive": True,
            "plugins": {
                "title": {
                    "display": True,
                    "text": "Accessibilité des pharmacies par code postal"
                }
            }
        }
    }
    
    return {
        "question": "Accessibilité des centres de vaccination (pharmacies uniquement) selon la population",
        "graphique": "Barème",
        "data": data,
        "total": len(data),
        "chartjs": chartjs_format
    }


@router.get("/evolution-actes-age", response_model=EvolutionActesAgeResponse)
async def get_evolution_actes_age(
    db: Session = Depends(get_db),
    region: Optional[str] = Query(None, description="Filtrer par région")
):
    """
    Évolution des actes par âge de 2021 à 2024 selon les régions
    
    Graphique: Courbes
    Format Chart.js: Line chart avec 2 lignes (65+ et -65)
    """
    query = "SELECT * FROM evolution_actes_age WHERE 1=1"
    
    if region:
        query += f" AND region = '{region}'"
    
    results = db.execute(text(query)).fetchall()
    
    # Préparer les données pour Chart.js
    regions_data = []
    for row in results:
        regions_data.append({
            "region": row[1],
            "2021_65_plus": row[2],
            "2021_moins_65": row[3],
            "2022_65_plus": row[4],
            "2022_moins_65": row[5],
            "2023_65_plus": row[6],
            "2023_moins_65": row[7],
            "2024_65_plus": row[8],
            "2024_moins_65": row[9]
        })
    
    # Format Chart.js (Line chart)
    chartjs_format = {
        "type": "line",
        "data": {
            "labels": ["2021", "2022", "2023", "2024"],
            "datasets": []
        },
        "options": {
            "responsive": True,
            "plugins": {
                "title": {
                    "display": True,
                    "text": "Évolution des actes de vaccination par âge"
                },
                "legend": {
                    "display": True
                }
            },
            "scales": {
                "y": {
                    "beginAtZero": True
                }
            }
        }
    }
    
    # Ajouter une ligne par région
    for region_data in regions_data:
        # Ligne pour 65+
        chartjs_format["data"]["datasets"].append({
            "label": f"{region_data['region']} - 65 ans et plus",
            "data": [
                region_data["2021_65_plus"],
                region_data["2022_65_plus"],
                region_data["2023_65_plus"],
                region_data["2024_65_plus"]
            ],
            "borderColor": "rgba(255, 99, 132, 1)",
            "backgroundColor": "rgba(255, 99, 132, 0.2)",
            "tension": 0.4
        })
        
        # Ligne pour moins de 65
        chartjs_format["data"]["datasets"].append({
            "label": f"{region_data['region']} - Moins de 65 ans",
            "data": [
                region_data["2021_moins_65"],
                region_data["2022_moins_65"],
                region_data["2023_moins_65"],
                region_data["2024_moins_65"]
            ],
            "borderColor": "rgba(54, 162, 235, 1)",
            "backgroundColor": "rgba(54, 162, 235, 0.2)",
            "tension": 0.4
        })
    
    return {
        "question": "Évolution des actes par âge de 2021 à 2024 selon les régions",
        "graphique": "Courbes",
        "data": regions_data,
        "total": len(regions_data),
        "chartjs": chartjs_format
    }


@router.get("/evolution-doses-age", response_model=EvolutionDosesAgeResponse)
async def get_evolution_doses_age(
    db: Session = Depends(get_db),
    region: Optional[str] = Query(None, description="Filtrer par région")
):
    """
    Évolution des doses par âge de 2021 à 2024 selon les régions
    
    Graphique: Courbes
    Format Chart.js: Line chart
    """
    query = "SELECT * FROM evolution_doses_age WHERE 1=1"
    
    if region:
        query += f" AND region = '{region}'"
    
    results = db.execute(text(query)).fetchall()
    
    regions_data = []
    for row in results:
        regions_data.append({
            "region": row[1],
            "2021_65_plus": row[2],
            "2021_moins_65": row[3],
            "2022_65_plus": row[4],
            "2022_moins_65": row[5],
            "2023_65_plus": row[6],
            "2023_moins_65": row[7],
            "2024_65_plus": row[8],
            "2024_moins_65": row[9]
        })
    
    # Même format que evolution-actes-age
    chartjs_format = {
        "type": "line",
        "data": {
            "labels": ["2021", "2022", "2023", "2024"],
            "datasets": []
        },
        "options": {
            "responsive": True,
            "plugins": {
                "title": {
                    "display": True,
                    "text": "Évolution des doses de vaccination par âge"
                }
            },
            "scales": {
                "y": {
                    "beginAtZero": True
                }
            }
        }
    }
    
    for region_data in regions_data:
        chartjs_format["data"]["datasets"].append({
            "label": f"{region_data['region']} - 65 ans et plus",
            "data": [
                region_data["2021_65_plus"],
                region_data["2022_65_plus"],
                region_data["2023_65_plus"],
                region_data["2024_65_plus"]
            ],
            "borderColor": "rgba(255, 99, 132, 1)",
            "backgroundColor": "rgba(255, 99, 132, 0.2)",
            "tension": 0.4
        })
        
        chartjs_format["data"]["datasets"].append({
            "label": f"{region_data['region']} - Moins de 65 ans",
            "data": [
                region_data["2021_moins_65"],
                region_data["2022_moins_65"],
                region_data["2023_moins_65"],
                region_data["2024_moins_65"]
            ],
            "borderColor": "rgba(54, 162, 235, 1)",
            "backgroundColor": "rgba(54, 162, 235, 0.2)",
            "tension": 0.4
        })
    
    return {
        "question": "Évolution des doses par âge de 2021 à 2024 selon les régions",
        "graphique": "Courbes",
        "data": regions_data,
        "total": len(regions_data),
        "chartjs": chartjs_format
    }


@router.get("/evolution-actes-region", response_model=EvolutionActesRegionResponse)
async def get_evolution_actes_region(
    db: Session = Depends(get_db),
    region: Optional[str] = Query(None, description="Filtrer par région")
):
    """
    Évolution actes de vaccination contre la grippe de 2021 à 2024 par région
    
    Graphique: Graph batons (Bar chart)
    """
    from app.models.schemas import EvolutionActesRegion
    
    query = db.query(EvolutionActesRegion)
    
    if region:
        query = query.filter(EvolutionActesRegion.region.like(f"%{region}%"))
    
    results = query.all()
    
    data = []
    for row in results:
        data.append({
            "region": row.region,
            "actes_2021": row.Actes_2021,  # ← Majuscule !
            "actes_2022": row.Actes_2022,  # ← Majuscule !
            "actes_2023": row.Actes_2023,  # ← Majuscule !
            "actes_2024": row.Actes_2024,  # ← Majuscule !
            "evolution_pct": row.Evolution_pct  # ← Majuscule !
        })
    
    # Le reste identique...
    chartjs_format = {
        "type": "bar",
        "data": {
            "labels": [d["region"] for d in data],
            "datasets": [
                {
                    "label": "2021",
                    "data": [d["actes_2021"] for d in data],
                    "backgroundColor": "rgba(255, 99, 132, 0.5)"
                },
                {
                    "label": "2022",
                    "data": [d["actes_2022"] for d in data],
                    "backgroundColor": "rgba(54, 162, 235, 0.5)"
                },
                {
                    "label": "2023",
                    "data": [d["actes_2023"] for d in data],
                    "backgroundColor": "rgba(255, 206, 86, 0.5)"
                },
                {
                    "label": "2024",
                    "data": [d["actes_2024"] for d in data],
                    "backgroundColor": "rgba(75, 192, 192, 0.5)"
                }
            ]
        },
        "options": {
            "responsive": True,
            "plugins": {
                "title": {
                    "display": True,
                    "text": "Évolution des actes de vaccination par région (2021-2024)"
                }
            },
            "scales": {
                "y": {
                    "beginAtZero": True
                }
            }
        }
    }
    
    return {
        "question": "Évolution actes de vaccination contre la grippe de 2021 à 2024 par région",
        "graphique": "Graph batons",
        "data": data,
        "total": len(data),
        "chartjs": chartjs_format
    }

@router.get("/evolution-doses-region", response_model=EvolutionDosesRegionResponse)
async def get_evolution_doses_region(
    db: Session = Depends(get_db),
    region: Optional[str] = Query(None, description="Filtrer par région")
):
    """
    Évolution doses de vaccination contre la grippe de 2021 à 2024 par région
    
    Graphique: Graph batons (Bar chart)
    """
    query = "SELECT * FROM evolution_doses_region WHERE 1=1"
    
    if region:
        query += f" AND region = '{region}'"
    
    results = db.execute(text(query)).fetchall()
    
    data = []
    for row in results:
        data.append({
            "region": row[1],
            "doses_2021": row[2],
            "doses_2022": row[3],
            "doses_2023": row[4],
            "doses_2024": row[5],
            "evolution_pct": row[6]
        })
    
    # Même format que evolution-actes-region
    chartjs_format = {
        "type": "bar",
        "data": {
            "labels": [d["region"] for d in data],
            "datasets": [
                {
                    "label": "2021",
                    "data": [d["doses_2021"] for d in data],
                    "backgroundColor": "rgba(255, 99, 132, 0.5)"
                },
                {
                    "label": "2022",
                    "data": [d["doses_2022"] for d in data],
                    "backgroundColor": "rgba(54, 162, 235, 0.5)"
                },
                {
                    "label": "2023",
                    "data": [d["doses_2023"] for d in data],
                    "backgroundColor": "rgba(255, 206, 86, 0.5)"
                },
                {
                    "label": "2024",
                    "data": [d["doses_2024"] for d in data],
                    "backgroundColor": "rgba(75, 192, 192, 0.5)"
                }
            ]
        },
        "options": {
            "responsive": True,
            "plugins": {
                "title": {
                    "display": True,
                    "text": "Évolution des doses de vaccination par région (2021-2024)"
                }
            },
            "scales": {
                "y": {
                    "beginAtZero": True
                }
            }
        }
    }
    
    return {
        "question": "Évolution doses de vaccination contre la grippe de 2021 à 2024 par région",
        "graphique": "Graph batons",
        "data": data,
        "total": len(data),
        "chartjs": chartjs_format
    }


@router.get("/repartition-lieu-vaccination", response_model=RepartitionLieuVaccinationResponse)
async def get_repartition_lieu_vaccination(
    db: Session = Depends(get_db),
    type_lieu: Optional[str] = Query(None, description="Filtrer par type de lieu"),
    tranche_age: Optional[str] = Query(None, description="Filtrer par tranche d'âge")
):
    """
    Répartition du lieu de vaccination selon la tranche d'âge
    
    Graphique: Courbe à barres (Stacked bar chart)
    """
    query = "SELECT * FROM repartition_lieu_vaccination WHERE 1=1"
    
    if type_lieu:
        query += f" AND type_lieu_vaccination = '{type_lieu}'"
    if tranche_age:
        query += f" AND tranche_age = '{tranche_age}'"
    
    results = db.execute(text(query)).fetchall()
    
    data = []
    for row in results:
        data.append({
            "type_lieu_vaccination": row[1],
            "tranche_age": row[2]
        })
    
    # Regrouper par tranche d'âge
    tranches = list(set([d["tranche_age"] for d in data]))
    lieux = list(set([d["type_lieu_vaccination"] for d in data]))
    
    # Format Chart.js (Stacked bar chart)
    chartjs_format = {
        "type": "bar",
        "data": {
            "labels": tranches,
            "datasets": []
        },
        "options": {
            "responsive": True,
            "plugins": {
                "title": {
                    "display": True,
                    "text": "Répartition du lieu de vaccination par tranche d'âge"
                }
            },
            "scales": {
                "x": {
                    "stacked": True
                },
                "y": {
                    "stacked": True,
                    "beginAtZero": True
                }
            }
        }
    }
@router.get("/debug-actes-region")
async def debug_actes_region(db: Session = Depends(get_db)):
    """Endpoint de debug pour voir les données brutes"""
    from app.models.schemas import EvolutionActesRegion
    
    results = db.query(EvolutionActesRegion).all()
    
    debug_data = []
    for row in results:
        debug_data.append({
            "region": row.region,
            "has_Actes_2021_attr": hasattr(row, 'Actes_2021'),
            "has_actes_2021_attr": hasattr(row, 'actes_2021'),
            "all_attributes": [attr for attr in dir(row) if not attr.startswith('_')],
            "try_Actes_2021": getattr(row, 'Actes_2021', 'NOT_FOUND'),
            "try_actes_2021": getattr(row, 'actes_2021', 'NOT_FOUND'),
        })
    
    return {
        "total_rows": len(results),
        "debug_data": debug_data[:3]  # Juste les 3 premières lignes
    }
    
    # TODO: Compter les occurrences par lieu et tranche d'âge
    
    return {
        "question": "Répartition du lieu de vaccination selon la tranche d'âge",
        "graphique": "Courbe à barres",
        "data": data,
        "total": len(data),
        "chartjs": chartjs_format
    }