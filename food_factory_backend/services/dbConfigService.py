from constants.queries import FETCH_DB_CONFIG_DATA, UPDATE_DB_CONFIG_DATA
from logger import LOGGER
import json

def fetch_db_config_data(db_connection, map_from):
    try:
        LOGGER.info("Inside fetch_db_config_data!")
        
        cursor = db_connection.cursor() 
        cursor.execute(FETCH_DB_CONFIG_DATA, (map_from,))
        configDetail = cursor.fetchone() 

        if configDetail:
            return configDetail[0]  
        else:
            return None
            
    except Exception as e:
        LOGGER.error(f"Error fetching config: {e}")
        return None
    finally:
        cursor.close()
    
def update_db_config_data(db_connection, request):
    try:
        LOGGER.info("Inside update_db_config_data!")
        
        data = json.loads(request.body)
        cursor = db_connection.cursor() 
        cursor.execute(UPDATE_DB_CONFIG_DATA, (
            data.get('mapTo'),
            data.get('mapFrom')
        ))
         
        db_connection.commit()
        return cursor.rowcount > 0
            
    except Exception as e:
        LOGGER.error(f"Error updating config: {e}")
        return None
    finally:
        cursor.close()