import json
import os
import pytest
from thinknet_application_specific_exception import ApplicationSpecificException
from thinknet_airflow_dag_artifact.xcom_utilities import write_xcom_to_file

def test_xcom_push_success(tmp_path):
    file_path = str(tmp_path / "empty_xcom.json")
    value = "Mock"
    write_xcom_to_file(file_path, value)
    with open(file_path, "r", encoding="utf-8") as f:
        assert json.load(f) == value

def test_xcom_push_undefined_path():
    xcom_path = None
    value = "Mock"
    with pytest.raises(ApplicationSpecificException) as excinfo:
        write_xcom_to_file(xcom_path, value)
    assert excinfo.value.error_code == "UTT01"
    assert excinfo.value.input_params == {"value": xcom_path}

def test_xcom_push_non_str_path():
    xcom_path = 123456
    value = "Mock"
    with pytest.raises(ApplicationSpecificException) as excinfo:
        write_xcom_to_file(xcom_path, value)
    assert excinfo.value.error_code == "UTT01"
    assert excinfo.value.input_params == {"value": xcom_path}

def test_xcom_push_non_existent_directory_raises_error(tmp_path):
    invalid_path = str(tmp_path / "non_existent_dir" / "xcom.json")
    value = "Mock"
    with pytest.raises(ApplicationSpecificException) as excinfo:
        write_xcom_to_file(invalid_path, value)
    assert excinfo.value.error_code == "ADAF02"
    assert excinfo.value.input_params == {"airflow_xcom_path": invalid_path, "value": value}

def test_xcom_push_permission_error_raises_error(tmp_path):
    file_path = str(tmp_path / "readonly_xcom.json")
    with open(file_path, "w",encoding="utf-8"):
        pass
    os.chmod(file_path, 0o444)  # Make file read-only
    value = {"key": "value"}
    try:
        with pytest.raises(ApplicationSpecificException) as excinfo:
            write_xcom_to_file(file_path, value)
        assert excinfo.value.error_code == "ADAP03"
        assert excinfo.value.input_params == {"airflow_xcom_path": file_path, "value": value}
    finally:
        os.chmod(file_path, 0o666)

def test_xcom_push_non_serializable_value_raises_error(tmp_path):
    file_path = str(tmp_path / "nonserializable_xcom.json")
    value = {"key": object()}  # Object is not JSON serializable
    with pytest.raises(ApplicationSpecificException) as excinfo:
        write_xcom_to_file(file_path, value)
    assert excinfo.value.error_code == "ADAT02"
    assert excinfo.value.input_params == {"airflow_xcom_path": file_path, "value": value}
