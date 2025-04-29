import json
from typing import Any
from thinknet_application_specific_exception import raise_error
from thinknet_variable_validator import validate_and_strip_str_variable
from thinknet_airflow_dag_artifact.error_data import ErrorData

def write_xcom_to_file(airflow_xcom_path: str, value: Any) -> None:
    validate_and_strip_str_variable(airflow_xcom_path)
    try:
        with open(airflow_xcom_path, "w", encoding="utf-8") as f:
            json.dump(value, f)
    except FileNotFoundError:
        raise_error(
            ErrorData.ADAF02,
            {"airflow_xcom_path": airflow_xcom_path, "value": value},
        )
    except PermissionError:
        raise_error(
            ErrorData.ADAP03,
            {"airflow_xcom_path": airflow_xcom_path, "value": value},
        )
    except TypeError:
        raise_error(
            ErrorData.ADAT02,
            {"airflow_xcom_path": airflow_xcom_path, "value": value},
        )
