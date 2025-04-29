from unittest.mock import patch, MagicMock
import pytest
from py4j.protocol import Py4JJavaError
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import lit
from thinknet_application_specific_exception import ApplicationSpecificException
from thinknet_airflow_dag_artifact.spark_utilities import write_dataframe_to_s3

@pytest.fixture(scope="session",name="spark_session")
def fixture_spark_session():
    spark = SparkSession.builder.appName("pytest-spark").master("local[*]").getOrCreate()
    yield spark
    spark.stop()

def test_write_dataframe_to_s3_success(spark_session, tmp_path):
    data = [("Alice", 1), ("Bob", 2)]
    columns = ["name", "id"]
    df = spark_session.createDataFrame(data, columns)

    output_path = str(tmp_path / "test.parquet")
    write_dataframe_to_s3(df, f"file://{output_path}")

    read_df = spark_session.read.parquet(f"file://{output_path}")
    assert isinstance(read_df, DataFrame)
    assert read_df.columns == columns
    assert read_df.count() == 2

def test_write_dataframe_to_s3_path_none(spark_session):
    data = [("Alice", 1), ("Bob", 2)]
    columns = ["name", "id"]
    df = spark_session.createDataFrame(data, columns)

    with pytest.raises(ApplicationSpecificException) as excinfo:
        write_dataframe_to_s3(df, None)
    assert excinfo.value.error_code == "UTT01"
    assert excinfo.value.input_params == {"value":None}

def test_write_dataframe_to_s3_path_non_str_type(spark_session):
    data = [("Alice", 1), ("Bob", 2)]
    columns = ["name", "id"]
    df = spark_session.createDataFrame(data, columns)

    with pytest.raises(ApplicationSpecificException) as excinfo:
        write_dataframe_to_s3(df, 12345)
    assert excinfo.value.error_code == "UTT01"
    assert excinfo.value.input_params == {"value":12345}

def test_write_dataframe_to_s3_df_non_dataframe_type(tmp_path):
    output_path = str(tmp_path / "test.parquet")
    with pytest.raises(ApplicationSpecificException) as excinfo:
        write_dataframe_to_s3(123, f"file://{output_path}")
    assert excinfo.value.error_code == "ADAT01"
    assert excinfo.value.input_params == {"df": 123}

def test_write_dataframe_to_s3_unsupport_type(spark_session, tmp_path):
    data = [("Alice", 1), ("Bob", 2)]
    columns = ["name", "id"]
    df = spark_session.createDataFrame(data, columns)
    df = df.withColumn("empty_column", lit(None))

    output_path = str(tmp_path / "test.parquet")
    with pytest.raises(ApplicationSpecificException) as excinfo:
        write_dataframe_to_s3(df, f"file://{output_path}")
    assert excinfo.value.error_code == "ADAN01"
    assert excinfo.value.input_params == {"df": df,"path_file":f"file://{output_path}"}

def test_write_dataframe_to_s3_accessdenied_mock(spark_session, tmp_path):
    data = [("Alice", 1), ("Bob", 2)]
    columns = ["name", "id"]
    df = spark_session.createDataFrame(data, columns)

    output_path = str(tmp_path / "test_client_error.parquet")
    output_path = f"s3a://test-tn-spark-lib/{output_path}"

    mock_java_exception = MagicMock(_target_id="_")
    mock_java_exception.__str__.return_value = "AccessDeniedException"
    mock_py4j_error = Py4JJavaError("_", java_exception=mock_java_exception)

    with patch("pyspark.sql.DataFrameWriter.parquet", side_effect=mock_py4j_error):
        with pytest.raises(ApplicationSpecificException) as excinfo:
            write_dataframe_to_s3(df, output_path)
    assert excinfo.value.error_code == "ADAP02"
    assert excinfo.value.input_params == {"df": df,"path_file":output_path}

def test_write_dataframe_to_s3_nosuchbucket_mock(spark_session, tmp_path):
    data = [("Alice", 1), ("Bob", 2)]
    columns = ["name", "id"]
    df = spark_session.createDataFrame(data, columns)
    
    output_path = str(tmp_path / "test_bucket_error.parquet")
    output_path = f"s3a://test-tn-spark-lib/{output_path}"

    mock_java_exception = MagicMock(_target_id="_")
    mock_java_exception.__str__.return_value = "com.amazonaws.services.s3.model.NoSuchBucketException: The specified bucket does not exist"
    mock_py4j_error = Py4JJavaError("_", java_exception=mock_java_exception)

    with patch("pyspark.sql.DataFrameWriter.parquet", side_effect=mock_py4j_error):
        with pytest.raises(ApplicationSpecificException) as excinfo:
            write_dataframe_to_s3(df, output_path)
    assert excinfo.value.error_code == "ADAC01"
    assert excinfo.value.input_params == {"df": df,"path_file": output_path}

def test_write_dataframe_to_s3_other_py4j_error_mock(spark_session, tmp_path):
    data = [("Alice", 1), ("Bob", 2)]
    columns = ["name", "id"]
    df = spark_session.createDataFrame(data, columns)

    output_path = str(tmp_path / "test_bucket_error.parquet")
    output_path = f"s3a://test-tn-spark-lib/{output_path}"

    mock_java_exception = MagicMock(_target_id="_")
    mock_java_exception.__str__.return_value = "java.lang.RuntimeException: Unexpected error"
    mock_py4j_error = Py4JJavaError("_", java_exception=mock_java_exception)

    with patch("pyspark.sql.DataFrameWriter.parquet", side_effect=mock_py4j_error):
        with pytest.raises(ApplicationSpecificException) as excinfo:
            write_dataframe_to_s3(df, output_path)
    assert excinfo.value.error_code == "ADAE99"
    assert excinfo.value.input_params == {"df": df,"path_file": output_path}
