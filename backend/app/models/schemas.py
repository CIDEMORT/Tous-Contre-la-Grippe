from sqlalchemy import Column, Integer, String, Float, Date, DateTime
from app.database import Base
from datetime import datetime

# ============================================
# GÉOGRAPHIE
# ============================================

class AccessibilitePharmacies(Base):
    """Accessibilité des centres de vaccination (pharmacies)"""
    __tablename__ = "accessibilite_pharmacies"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre_pharmacies = Column(Integer)
    population = Column(Integer)
    code_postal = Column(String(10), index=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class EvolutionActesAge(Base):
    """Évolution des actes par âge de 2021 à 2024 selon les régions"""
    __tablename__ = "evolution_actes_age"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    region = Column(String(100), index=True)
    actes_2021_65_plus = Column(Integer, name="2021_65_ans_et_plus")
    actes_2021_moins_65 = Column(Integer, name="2021_moins_de_65_ans")
    actes_2022_65_plus = Column(Integer, name="2022_65_ans_et_plus")
    actes_2022_moins_65 = Column(Integer, name="2022_moins_de_65_ans")
    actes_2023_65_plus = Column(Integer, name="2023_65_ans_et_plus")
    actes_2023_moins_65 = Column(Integer, name="2023_moins_de_65_ans")
    actes_2024_65_plus = Column(Integer, name="2024_65_ans_et_plus")
    actes_2024_moins_65 = Column(Integer, name="2024_moins_de_65_ans")
    created_at = Column(DateTime, default=datetime.utcnow)


class EvolutionDosesAge(Base):
    """Évolution des doses par âge de 2021 à 2024 selon les régions"""
    __tablename__ = "evolution_doses_age"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    region = Column(String(100), index=True)
    doses_2021_65_plus = Column(Integer, name="2021_65_ans_et_plus")
    doses_2021_moins_65 = Column(Integer, name="2021_moins_de_65_ans")
    doses_2022_65_plus = Column(Integer, name="2022_65_ans_et_plus")
    doses_2022_moins_65 = Column(Integer, name="2022_moins_de_65_ans")
    doses_2023_65_plus = Column(Integer, name="2023_65_ans_et_plus")
    doses_2023_moins_65 = Column(Integer, name="2023_moins_de_65_ans")
    doses_2024_65_plus = Column(Integer, name="2024_65_ans_et_plus")
    doses_2024_moins_65 = Column(Integer, name="2024_moins_de_65_ans")
    created_at = Column(DateTime, default=datetime.utcnow)


class EvolutionActesRegion(Base):
    """Évolution actes de vaccination contre la grippe de 2021 à 2024 par région"""
    __tablename__ = "evolution_actes_region"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    region = Column(String(100), index=True)
    code = Column(Integer)
    # Utiliser directement les noms avec majuscules comme dans le CSV
    Actes_2021 = Column(Integer)
    Actes_2022 = Column(Integer)
    Actes_2023 = Column(Integer)
    Actes_2024 = Column(Integer)
    Evolution_pct = Column(Float, name="Evolution_%")
    created_at = Column(DateTime, default=datetime.utcnow)

class EvolutionDosesRegion(Base):
    """Évolution doses de vaccination contre la grippe de 2021 à 2024 par région"""
    __tablename__ = "evolution_doses_region"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    region = Column(String(100), index=True)
    doses_2021 = Column(Integer, name="Doses_2021")
    doses_2022 = Column(Integer, name="Doses_2022")
    doses_2023 = Column(Integer, name="Doses_2023")
    doses_2024 = Column(Integer, name="Doses_2024")
    evolution_pct = Column(Float, name="Evolution_%")
    created_at = Column(DateTime, default=datetime.utcnow)


class RepartitionLieuVaccination(Base):
    """Répartition du lieu de vaccination selon la tranche d'âge"""
    __tablename__ = "repartition_lieu_vaccination"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    type_lieu_vaccination = Column(String(100), index=True)
    tranche_age = Column(String(50), index=True)
    created_at = Column(DateTime, default=datetime.utcnow)


# ============================================
# LOGISTIQUE
# ============================================

class ActesDosesRegion(Base):
    """Comparaison actes de vaccination vs doses distribuées par région"""
    __tablename__ = "actes_doses_region"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    region = Column(String(100), index=True)
    acte_vgp = Column(Integer)  # Nom Python simplifié
    doses_j07e1 = Column(Integer)  # Nom Python simplifié
    created_at = Column(DateTime, default=datetime.utcnow)

class NombrePharmaciesPeriode(Base):
    """Nombre de pharmacie sur une période/campagne de vaccination"""
    __tablename__ = "nombre_pharmacies_periode"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date = Column(Date, index=True)
    variable_pharmacie = Column(String(100))
    valeur = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)


# ============================================
# SAISONNALITÉ
# ============================================

class DonneesMeteo(Base):
    """Données météo pour analyse saisonnalité + grippe"""
    __tablename__ = "donnees_meteo"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    NOM_USUEL = Column(String(200), index=True)  # ← Majuscules pour matcher le CSV
    TNTXM = Column(Float)
    TNSOL = Column(Float)
    TMM = Column(Float)
    annees = Column(Integer, index=True)
    mois = Column(Integer, index=True)
    taux_grippe = Column(Float)
    incidence_sg_hebdo = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)