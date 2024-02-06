import numpy as np
import psycopg2

TABLE_CREATE_COMMANDS = [
    """
    CREATE TABLE IF NOT EXISTS cameras (
        pk_c_id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        description VARCHAR(4000),
        resolution_height INTEGER,
        resolution_width INTEGER,
        base_url VARCHAR(4000) NOT NULL,
        port INTEGER NOT NULL,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        manufacturing_line VARCHAR(255) NOT NULL,
        in_use BOOL NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS models (
        pk_m_id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        description VARCHAR(4000),
        absolute_path VARCHAR(255) NOT NULL,
        format VARCHAR(255) NOT NULL,
        model_type VARCHAR(255),
        config VARCHAR(4000)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS event_types (
        pk_e_id SERIAL PRIMARY KEY,
        pk_m_id SERIAL REFERENCES models(pk_m_id),
        event_type VARCHAR(255) NOT NULL,
        severity INTEGER
    )
    """
]

def format_insert(metadata, table_name, n_samples=20):
    def get_values_str(values):
        return ", ".join([f"'{value}'" if isinstance(value, str) else value for value in values])
    values_np = np.array(list(metadata.values()))
    commands = []
    for i in range(0, n_samples):
        commands.append(f'INSERT INTO {table_name} ({", ".join(list(metadata.keys()))}) VALUES ({get_values_str(values_np[:, i])})')
    return commands


def create_responsibility():
    ...

def create_task_type():
    ...

def create_event_type():
    ...




def generate_hardware_stage(n_samples=20):
    metadata = {
        'pk_c_id': np.arange(0, n_samples),
        'name': [f'test_name_{index}' for index in range(0, n_samples)],
        'description': [f'test_description_{index}' for index in range(0, n_samples)],
        'resolution_height': [240] * n_samples,
        'resolution_width': [240] * n_samples,
        'base_url': [f'test_url_{index}' for index in range(0, n_samples)],
        'port': [8000] * n_samples,
        'username': [f'test_username_{index}' for index in range(0, n_samples)],
        'password': [f'test_password_{index}' for index in range(0, n_samples)],
        'manufacturing_line': [np.random.choice(['line_1', 'line_2']) for _ in range(0, n_samples)],
        'in_use': [np.random.choice([True, False]) for _ in range(0, n_samples)]
    }
    return metadata

def generate_model_stage(n_samples=4):
    metadata = {
        'pk_m_id': np.arange(0, n_samples),
        'name': [f'test_name_{index}' for index in range(0, n_samples)],
        'description': [f'test_description_{index}' for index in range(0, n_samples)],
        'absolute_path': [f'some/path/model_{index}.onnx' for index in range(0, n_samples)],
        'format': ['onnx'] * n_samples,
        'model_type': [np.random.choice(['yolov8', 'musc', 'ocr']) for _ in range(0, n_samples)],
        'config': ['{track: True}'] * n_samples
    }
    return metadata

def generate_hardware_record_stage():
    ...

def generate_event_stage():
    ...

def generate_auth_stage():
    ...

def generate_auth_audit_stage():
    ...



def run():
    try:
        with psycopg2.connect(dbname='postgres', user='root', password='password') as conn:
            with conn.cursor() as cursor:
                # --- cameras --- #
                cursor.execute('DROP TABLE IF EXISTS cameras;')
                cursor.execute(TABLE_CREATE_COMMANDS[0])
                insert_commands = format_insert(generate_hardware_stage(), 'cameras', n_samples=20)
                for command in insert_commands: cursor.execute(command)

                # --- models --- #
                cursor.execute('DROP TABLE IF EXISTS models;')
                cursor.execute(TABLE_CREATE_COMMANDS[1])
                insert_commands = format_insert(generate_model_stage(), 'models', n_samples=4)
                for command in insert_commands: cursor.execute(command)

                # --- event_types --- #
                cursor.execute('DROP TABLE IF EXISTS event_types')
                cursor.execute(TABLE_CREATE_COMMANDS[2])
                
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

if __name__ == '__main__':
    run()