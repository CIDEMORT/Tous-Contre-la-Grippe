from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from typing import Optional

router = APIRouter()

# ============================================
# LOGISTIQUE - Routes spécifiques
# ============================================

@router.get("/actes-doses-region")
async def get_actes_doses_region(
    db: Session = Depends(get_db),
    region: Optional[str] = Query(None, description="Filtrer par région"),
    variable_stock: Optional[str] = Query(None, description="Filtrer par variable: actes ou doses")
):
    """
    Actes/Doses de vaccination par région
    
    Graphique: Bar chart comparatif
    """
    query = "SELECT * FROM actes_doses_region WHERE 1=1"
    
    if region:
        query += f" AND region = '{region}'"
    if variable_stock:
        query += f" AND variable_stock = '{variable_stock}'"
    
    results = db.execute(text(query)).fetchall()
    
    data = []
    for row in results:
        data.append({
            "region": row[1],
            "variable_stock": row[2],
            "valeur": row[3]
        })
    
    # Regrouper par région
    regions = list(set([d["region"] for d in data]))
    
    # Séparer actes et doses
    actes_data = [d["valeur"] for d in data if d["variable_stock"] == "actes"]
    doses_data = [d["valeur"] for d in data if d["variable_stock"] == "doses"]
    
    # Format Chart.js (Grouped bar chart)
    chartjs_format = {
        "type": "bar",
        "data": {
            "labels": regions,
            "datasets": [
                {
                    "label": "Actes",
                    "data": actes_data,
                    "backgroundColor": "rgba(255, 99, 132, 0.5)",
                    "borderColor": "rgba(255, 99, 132, 1)",
                    "borderWidth": 1
                },
                {
                    "label": "Doses",
                    "data": doses_data,
                    "backgroundColor": "rgba(54, 162, 235, 0.5)",
                    "borderColor": "rgba(54, 162, 235, 1)",
                    "borderWidth": 1
                }
            ]
        },
        "options": {
            "responsive": True,
            "plugins": {
                "title": {
                    "display": True,
                    "text": "Actes et Doses de vaccination par région"
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
    
    return {
        "question": "Actes/Doses de vaccination par région",
        "graphique": "Bar chart",
        "data": data,
        "total": len(data),
        "chartjs": chartjs_format
    }


@router.get("/nombre-pharmacies-periode")
async def get_nombre_pharmacies_periode(
    db: Session = Depends(get_db),
    date_debut: Optional[str] = Query(None, description="Date de début (YYYY-MM-DD)"),
    date_fin: Optional[str] = Query(None, description="Date de fin (YYYY-MM-DD)"),
    variable_pharmacie: Optional[str] = Query(None, description="Variable spécifique")
):
    """
    Nombre de pharmacie sur une période/campagne de vaccination
    
    Graphique: Line chart (évolution temporelle)
    """
    query = "SELECT * FROM nombre_pharmacies_periode WHERE 1=1"
    
    if date_debut:
        query += f" AND date >= '{date_debut}'"
    if date_fin:
        query += f" AND date <= '{date_fin}'"
    if variable_pharmacie:
        query += f" AND variable_pharmacie = '{variable_pharmacie}'"
    
    query += " ORDER BY date ASC"
    
    results = db.execute(text(query)).fetchall()
    
    data = []
    for row in results:
        data.append({
            "date": str(row[1]),
            "variable_pharmacie": row[2],
            "valeur": row[3]
        })
    
    # Format Chart.js (Line chart)
    chartjs_format = {
        "type": "line",
        "data": {
            "labels": [d["date"] for d in data],
            "datasets": [{
                "label": "Nombre de pharmacies",
                "data": [d["valeur"] for d in data],
                "borderColor": "rgba(75, 192, 192, 1)",
                "backgroundColor": "rgba(75, 192, 192, 0.2)",
                "tension": 0.4,
                "fill": True
            }]
        },
        "options": {
            "responsive": True,
            "plugins": {
                "title": {
                    "display": True,
                    "text": "Évolution du nombre de pharmacies"
                }
            },
            "scales": {
                "y": {
                    "beginAtZero": True
                },
                "x": {
                    "type": "time",
                    "time": {
                        "unit": "day"
                    }
                }
            }
        }
    }
    
    return {
        "question": "Nombre de pharmacie sur une période/campagne de vaccination",
        "graphique": "Line chart",
        "data": data,
        "total": len(data),
        "chartjs": chartjs_format
    }