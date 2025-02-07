from constants.queries import FETCH_DB_CONFIG_DATA

def fetch_db_config_data(db_connection, map_from):
    try:
        cursor = db_connection.cursor() 
        cursor.execute(FETCH_DB_CONFIG_DATA, (map_from,))
        configDetail = cursor.fetchone() 

        if configDetail:
            return configDetail[0]  
        else:
            return None
            
    except Exception as e:
        print(f"Error fetching config: {e}")
        return None
    finally:
        cursor.close()