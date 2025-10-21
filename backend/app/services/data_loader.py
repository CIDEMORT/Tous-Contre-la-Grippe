import pandas as pd
from pathlib import Path
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Text, Boolean
from sqlalchemy.types import TypeDecorator
from app.config import get_settings
from app.database import SessionLocal, Base, engine
from datetime import datetime
import logging

settings = get_settings()
logger = logging.getLogger(__name__)

# Mapping des types pandas vers SQLAlchemy
PANDAS_TO_SQL_TYPES = {
    'int64': Integer,
    'int32': Integer,
    'float64': Float,
    'float32': Float,
    'object': String(500),  # String par défaut
    'bool': Boolean,
    'datetime64[ns]': DateTime,
}

def clean_column_name(col_name: str) -> str:
    """
    Nettoie les noms de colonnes pour SQLite
    - Enlève les espaces
    - Remplace les caractères spéciaux
    - Met en lowercase
    """
    col_name = col_name.strip().lower()
    col_name = col_name.replace(' ', '_')
    col_name = col_name.replace('-', '_')
    col_name = col_name.replace('(', '').replace(')', '')
    col_name = col_name.replace('/', '_')
    col_name = col_name.replace('é', 'e').replace('è', 'e').replace('ê', 'e')
    col_name = col_name.replace('à', 'a').replace('â', 'a')
    col_name = col_name.replace('ô', 'o')
    col_name = col_name.replace('ù', 'u').replace('û', 'u')
    col_name = col_name.replace('ç', 'c')
    return col_name

def infer_sql_type(dtype, sample_values):
    """
    Infère le type SQL à partir du type pandas et des valeurs
    """
    dtype_str = str(dtype)
    
    # Détection de dates
    if 'date' in dtype_str.lower():
        return DateTime
    
    # Essayer de détecter les dates dans les strings
    if dtype_str == 'object' and sample_values is not None:
        try:
            pd.to_datetime(sample_values.dropna().head(5))
            return DateTime
        except:
            pass
    
    # Type par défaut selon pandas
    return PANDAS_TO_SQL_TYPES.get(dtype_str, String(500))

def create_table_from_csv(csv_path: Path, table_name: str = None):
    """
    Crée une table dynamiquement à partir d'un CSV
    """
    logger.info(f"📄 Analyse du fichier: {csv_path.name}")
    
    # Lire le CSV avec pandas
    try:
        df = pd.read_csv(csv_path, nrows=100)  # Lire seulement 100 lignes pour l'analyse
    except Exception as e:
        logger.error(f"❌ Erreur lecture CSV {csv_path.name}: {e}")
        return None
    
    # Nettoyer les noms de colonnes
    df.columns = [clean_column_name(col) for col in df.columns]
    
    # Nom de la table (utilise le nom du fichier si non spécifié)
    if table_name is None:
        table_name = clean_column_name(csv_path.stem)
    
    logger.info(f"📊 Table: {table_name}")
    logger.info(f"📋 Colonnes détectées: {', '.join(df.columns)}")
    
    # Créer la classe dynamiquement
    attrs = {
        '__tablename__': table_name,
        'id': Column(Integer, primary_key=True, index=True, autoincrement=True),
        'created_at': Column(DateTime, default=datetime.utcnow),
    }
    
    # Ajouter les colonnes détectées
    for col in df.columns:
        sql_type = infer_sql_type(df[col].dtype, df[col])
        attrs[col] = Column(sql_type, nullable=True)
    
    # Créer la classe de modèle
    table_class = type(table_name.capitalize() + 'Model', (Base,), attrs)
    
    return table_class, df.columns.tolist()

def load_csv_to_table(csv_path: Path, table_class, columns: list):
    """
    Charge les données d'un CSV dans la table
    """
    logger.info(f"📥 Chargement des données de {csv_path.name}...")
    
    # Lire tout le CSV
    try:
        df = pd.read_csv(csv_path)
        df.columns = [clean_column_name(col) for col in df.columns]
    except Exception as e:
        logger.error(f"❌ Erreur lecture complète du CSV: {e}")
        return 0
    
    # Convertir en dictionnaires
    records = df.to_dict('records')
    
    # Insérer dans la DB
    db = SessionLocal()
    try:
        # Insertion par batch de 1000
        batch_size = 1000
        total_inserted = 0
        
        for i in range(0, len(records), batch_size):
            batch = records[i:i+batch_size]
            db.bulk_insert_mappings(table_class, batch)
            db.commit()
            total_inserted += len(batch)
            logger.info(f"   ✅ {total_inserted}/{len(records)} lignes insérées")
        
        logger.info(f"✅ {total_inserted} lignes chargées avec succès")
        return total_inserted
        
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Erreur lors de l'insertion: {e}")
        return 0
    finally:
        db.close()

def load_all_csv_data():
    """
    Charge tous les fichiers CSV du dossier data/raw
    """
    csv_path = Path(settings.csv_data_path)
    
    if not csv_path.exists():
        logger.warning(f"⚠️  Dossier CSV non trouvé: {csv_path}")
        logger.info(f"💡 Créez le dossier et ajoutez vos fichiers CSV")
        csv_path.mkdir(parents=True, exist_ok=True)
        return
    
    logger.info(f"📁 Recherche de CSV dans: {csv_path}")
    csv_files = list(csv_path.glob("*.csv"))
    
    if not csv_files:
        logger.warning("⚠️  Aucun fichier CSV trouvé")
        logger.info(f"💡 Ajoutez vos fichiers CSV dans {csv_path}")
        return
    
    logger.info(f"📊 {len(csv_files)} fichiers CSV trouvés")
    
    # Liste des tables qui ont déjà un modèle défini dans schemas.py
    PREDEFINED_TABLES = [
        "accessibilite_pharmacies",
        "evolution_actes_age",
        "evolution_doses_age",
        "evolution_actes_region",
        "evolution_doses_region",
        "repartition_lieu_vaccination",
        "actes_doses_region",
        "nombre_pharmacies_periode",
        "donnees_meteo"
    ]
    
    total_loaded = 0
    
    for csv_file in csv_files:
        try:
            table_name = clean_column_name(csv_file.stem)
            
            # Si la table a déjà un modèle défini, utiliser le chargement direct
            if table_name in PREDEFINED_TABLES:
                logger.info(f"📄 Chargement du CSV prédéfini: {csv_file.name} → {table_name}")
                rows_loaded = load_predefined_csv(csv_file, table_name)
                total_loaded += rows_loaded
                logger.info(f"✅ {csv_file.name} → {rows_loaded} lignes chargées")
            else:
                # Sinon, créer la table dynamiquement (pour les CSV non prévus)
                logger.info(f"📄 Analyse du fichier: {csv_file.name}")
                result = create_table_from_csv(csv_file)
                if result is None:
                    continue
                    
                table_class, columns = result
                
                # Créer la table dans la DB
                Base.metadata.create_all(bind=engine, tables=[table_class.__table__])
                
                # Charger les données
                rows_loaded = load_csv_to_table(csv_file, table_class, columns)
                total_loaded += rows_loaded
                
                logger.info(f"✅ {csv_file.name} → Table '{table_class.__tablename__}' créée et remplie")
            
        except Exception as e:
            logger.error(f"❌ Erreur avec {csv_file.name}: {e}")
            continue
    

    logger.info(f"🎉 Chargement terminé ! {total_loaded} lignes totales chargées")

def load_predefined_csv(csv_path: Path, table_name: str):
    """
    Charge un CSV dans une table qui a déjà un modèle SQLAlchemy défini
    """
    from app.models import schemas
    from sqlalchemy import inspect
    
    # Mapping des noms de tables vers les classes de modèles
    MODEL_MAPPING = {
        "accessibilite_pharmacies": schemas.AccessibilitePharmacies,
        "evolution_actes_age": schemas.EvolutionActesAge,
        "evolution_doses_age": schemas.EvolutionDosesAge,
        "evolution_actes_region": schemas.EvolutionActesRegion,
        "evolution_doses_region": schemas.EvolutionDosesRegion,
        "repartition_lieu_vaccination": schemas.RepartitionLieuVaccination,
        "actes_doses_region": schemas.ActesDosesRegion,
        "nombre_pharmacies_periode": schemas.NombrePharmaciesPeriode,
        "donnees_meteo": schemas.DonneesMeteo,
    }
    
    model_class = MODEL_MAPPING.get(table_name)
    if not model_class:
        logger.error(f"❌ Modèle introuvable pour la table: {table_name}")
        return 0
    
    # Lire le CSV SANS modifier les noms de colonnes
    try:
        df = pd.read_csv(csv_path, sep=None, engine='python')
        df.columns = df.columns.str.replace('\ufeff', '', regex=False)
        df.columns = df.columns.str.replace('(', '_', regex=False)
        df.columns = df.columns.str.replace(')', '', regex=False)

    except Exception as e:
        logger.error(f"❌ Erreur lecture du CSV: {e}")
        return 0
    
    logger.info(f"📋 Colonnes du CSV: {list(df.columns)}")
    
    # Utiliser l'inspecteur pour avoir les VRAIS noms de colonnes dans la DB
    inspector = inspect(engine)
    db_columns = {}
    for col in inspector.get_columns(table_name):
        db_columns[col['name']] = col
    
    logger.info(f"📋 Colonnes dans la DB: {list(db_columns.keys())}")
    
    # Créer un mapping CSV → Attribut Python du modèle
    csv_to_python_attr = {}
    for csv_col in df.columns:
        # Trouver l'attribut Python qui correspond à cette colonne CSV
        for attr_name in dir(model_class):
            if attr_name.startswith('_'):
                continue
            try:
                attr = getattr(model_class, attr_name)
                if hasattr(attr, 'expression'):
                    # C'est une colonne SQLAlchemy
                    col_name = attr.expression.name
                    if col_name == csv_col:
                        csv_to_python_attr[csv_col] = attr_name
                        logger.info(f"  Mapping: CSV '{csv_col}' → Python '{attr_name}' → DB '{col_name}'")
                        break
            except:
                continue
    
    # Convertir en dictionnaires
    records = df.to_dict('records')
    
    # Insérer dans la DB
    db = SessionLocal()
    try:
        # Vider la table d'abord
        db.query(model_class).delete()
        db.commit()
        
        # Insertion par batch
        batch_size = 1000
        total_inserted = 0
        
        for i in range(0, len(records), batch_size):
            batch = records[i:i+batch_size]
            
            objects_to_insert = []
            for record in batch:
                obj = model_class()
                
                # Utiliser le mapping qu'on a créé
                for csv_col, value in record.items():
                    if csv_col in csv_to_python_attr:
                        python_attr = csv_to_python_attr[csv_col]
                        setattr(obj, python_attr, value)
                    elif csv_col in db_columns:
                        # Essai direct si la colonne existe dans la DB
                        setattr(obj, csv_col, value)
                
                objects_to_insert.append(obj)
            
            db.add_all(objects_to_insert)
            db.commit()
            total_inserted += len(objects_to_insert)
            logger.info(f"   ✅ {total_inserted}/{len(records)} lignes insérées")
        
        logger.info(f"✅ {total_inserted} lignes chargées avec succès dans {table_name}")
        return total_inserted
        
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Erreur lors de l'insertion dans {table_name}: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return 0
    finally:
        db.close()