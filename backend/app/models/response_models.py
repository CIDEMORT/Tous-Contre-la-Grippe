from pydantic import BaseModel
from typing import List, Dict, Any, Optional

# ============================================
# Modèles de réponse génériques
# ============================================

class ChartJSDataset(BaseModel):
    label: str
    data: List[Any]
    backgroundColor: Optional[str] = None
    borderColor: Optional[str] = None
    borderWidth: Optional[int] = None
    fill: Optional[bool] = None
    tension: Optional[float] = None

class ChartJSData(BaseModel):
    labels: List[str]
    datasets: List[ChartJSDataset]

class ChartJSOptions(BaseModel):
    responsive: bool = True
    plugins: Dict[str, Any] = {}
    scales: Optional[Dict[str, Any]] = None

class ChartJSFormat(BaseModel):
    type: str
    data: ChartJSData
    options: Optional[ChartJSOptions] = None

class BaseAPIResponse(BaseModel):
    question: str
    graphique: str
    data: List[Dict[str, Any]]
    total: int
    chartjs: ChartJSFormat

# ============================================
# Modèles spécifiques par endpoint
# ============================================

class AccessibilitePharmaciesData(BaseModel):
    nombre_pharmacies: int
    population: int
    code_postal: str
    ratio: float

class AccessibilitePharmaciesResponse(BaseModel):
    question: str
    graphique: str
    data: List[AccessibilitePharmaciesData]
    total: int
    chartjs: ChartJSFormat

class EvolutionActesAgeData(BaseModel):
    region: str
    actes_2021_65_plus: Optional[int] = None
    actes_2021_moins_65: Optional[int] = None
    actes_2022_65_plus: Optional[int] = None
    actes_2022_moins_65: Optional[int] = None
    actes_2023_65_plus: Optional[int] = None
    actes_2023_moins_65: Optional[int] = None
    actes_2024_65_plus: Optional[int] = None
    actes_2024_moins_65: Optional[int] = None

class EvolutionActesAgeResponse(BaseModel):
    question: str
    graphique: str
    data: List[EvolutionActesAgeData]
    total: int
    chartjs: ChartJSFormat

class EvolutionActesRegionData(BaseModel):
    region: str
    actes_2021: Optional[int] = None
    actes_2022: Optional[int] = None
    actes_2023: Optional[int] = None
    actes_2024: Optional[int] = None
    evolution_pct: Optional[float] = None

class EvolutionActesRegionResponse(BaseModel):
    question: str
    graphique: str
    data: List[EvolutionActesRegionData]
    total: int
    chartjs: ChartJSFormat

class DonneesMeteoData(BaseModel):
    NOM_USUEL: str
    TNTXM: Optional[float] = None
    TNSOL: Optional[float] = None
    TMM: Optional[float] = None
    annees: Optional[int] = None
    mois: Optional[int] = None
    taux_grippe: Optional[float] = None
    incidence_sg_hebdo: Optional[float] = None

class DonneesMeteoResponse(BaseModel):
    question: str
    graphique: str
    data: List[DonneesMeteoData]
    total: int
    chartjs: ChartJSFormat
    
# ============================================
# Admin
# ============================================

class TableInfo(BaseModel):
    columns: List[str]
    row_count: int

class AdminTablesResponse(BaseModel):
    total_tables: int
    tables: Dict[str, TableInfo]


# ============================================
# Évolution doses par âge
# ============================================

class EvolutionDosesAgeData(BaseModel):
    region: str
    doses_2021_65_plus: Optional[int] = None
    doses_2021_moins_65: Optional[int] = None
    doses_2022_65_plus: Optional[int] = None
    doses_2022_moins_65: Optional[int] = None
    doses_2023_65_plus: Optional[int] = None
    doses_2023_moins_65: Optional[int] = None
    doses_2024_65_plus: Optional[int] = None
    doses_2024_moins_65: Optional[int] = None

class EvolutionDosesAgeResponse(BaseModel):
    question: str
    graphique: str
    data: List[EvolutionDosesAgeData]
    total: int
    chartjs: ChartJSFormat

# ============================================
# Évolution doses par région
# ============================================

class EvolutionDosesRegionData(BaseModel):
    region: str
    doses_2021: Optional[int] = None
    doses_2022: Optional[int] = None
    doses_2023: Optional[int] = None
    doses_2024: Optional[int] = None
    evolution_pct: Optional[float] = None

class EvolutionDosesRegionResponse(BaseModel):
    question: str
    graphique: str
    data: List[EvolutionDosesRegionData]
    total: int
    chartjs: ChartJSFormat

# ============================================
# Répartition lieu de vaccination
# ============================================

class RepartitionLieuVaccinationData(BaseModel):
    type_lieu_vaccination: str
    tranche_age: str

class RepartitionLieuVaccinationResponse(BaseModel):
    question: str
    graphique: str
    data: List[RepartitionLieuVaccinationData]
    total: int
    chartjs: ChartJSFormat

# ============================================
# Logistique
# ============================================

class ActesDosesRegionData(BaseModel):
    region: str
    variable_stock: str
    valeur: int

class ActesDosesRegionResponse(BaseModel):
    question: str
    data: List[ActesDosesRegionData]
    chartjs: ChartJSFormat

class NombrePharmaciesPeriodeData(BaseModel):
    date: str
    variable_pharmacie: str
    valeur: int

class NombrePharmaciesPeriodeResponse(BaseModel):
    question: str
    data: List[NombrePharmaciesPeriodeData]
    chartjs: ChartJSFormat