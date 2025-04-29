from unittest.mock import patch, MagicMock
import pytest
from py4j.protocol import Py4JJavaError
from pyspark.sql import SparkSession, DataFrame
from thinknet_application_specific_exception import ApplicationSpecificException
from thinknet_airflow_dag_artifact.spark_utilities import read_from_s3_as_dataframe

@pytest.fixture(scope="session",name="spark_session")
def fixture_spark_session():
    spark = SparkSession.builder.appName("pytest-spark").master("local[*]").getOrCreate()
    yield spark
    spark.stop()

def test_read_from_s3_as_dataframe_success(spark_session, tmp_path):
    data = [("Alice", 1), ("Bob", 2)]
    columns = ["name", "id"]
    df = spark_session.createDataFrame(data, columns)

    output_path = str(tmp_path / "test.parquet")
    df.write.parquet(output_path)

    read_df = read_from_s3_as_dataframe(spark_session, f"file://{output_path}")
    assert isinstance(read_df, DataFrame)
    assert read_df.columns == columns
    assert read_df.count() == 2

def test_read_from_s3_as_dataframe_path_none(spark_session):
    with pytest.raises(ApplicationSpecificException) as excinfo:
        read_from_s3_as_dataframe(spark_session, None)
    assert excinfo.value.error_code == "UTT01"
    assert excinfo.value.input_params == {"value":None}

def test_read_from_s3_as_dataframe_path_non_str_type(spark_session):
    with pytest.raises(ApplicationSpecificException) as excinfo:
        read_from_s3_as_dataframe(spark_session, 12345)
    assert excinfo.value.error_code == "UTT01"
    assert excinfo.value.input_params == {"value":12345}

def test_read_from_s3_as_dataframe_file_not_found(spark_session):
    non_existent_path = "file:///tmp/non_existent.parquet"
    with pytest.raises(ApplicationSpecificException) as excinfo:
        read_from_s3_as_dataframe(spark_session, non_existent_path)
    assert excinfo.value.error_code == "ADAF01"
    assert excinfo.value.input_params == {"path_file":non_existent_path}

def test_read_from_s3_as_dataframe_accessdenied_mock(spark_session):
    path = "s3a://some-bucket/restricted.parquet"
    mock_java_exception = MagicMock(_target_id="_")
    mock_java_exception.__str__.return_value = "AccessDeniedException"
    mock_py4j_error = Py4JJavaError("_", java_exception=mock_java_exception)

    with patch("pyspark.sql.SparkSession.read") as mock_read:
        mock_read.parquet.side_effect = mock_py4j_error
        with pytest.raises(ApplicationSpecificException) as excinfo:
            read_from_s3_as_dataframe(spark_session, path)
        assert excinfo.value.error_code == "ADAP01"
        assert excinfo.value.input_params == {"path_file": path}

def test_read_from_s3_as_dataframe_nosuchbucket_mock(spark_session):
    path = "s3a://nonexistent-bucket/data.parquet"
    mock_java_exception = MagicMock(_target_id="_")
    mock_java_exception.__str__.return_value = "com.amazonaws.services.s3.model.NoSuchBucketException: The specified bucket does not exist"
    mock_py4j_error = Py4JJavaError("_", java_exception=mock_java_exception)

    with patch("pyspark.sql.SparkSession.read") as mock_read:
        mock_read.parquet.side_effect = mock_py4j_error
        with pytest.raises(ApplicationSpecificException) as excinfo:
            read_from_s3_as_dataframe(spark_session, path)
        assert excinfo.value.error_code == "ADAC01"
        assert excinfo.value.input_params == {"path_file": path}

def test_read_from_s3_as_dataframe_other_py4j_error_mock(spark_session):
    path = "s3a://some-bucket/corrupted.parquet"
    mock_java_exception = MagicMock(_target_id="_")
    mock_java_exception.__str__.return_value = "java.lang.RuntimeException: Unexpected error"
    mock_py4j_error = Py4JJavaError("_", java_exception=mock_java_exception)

    with patch("pyspark.sql.SparkSession.read") as mock_read:
        mock_read.parquet.side_effect = mock_py4j_error
        with pytest.raises(ApplicationSpecificException) as excinfo:
            read_from_s3_as_dataframe(spark_session, path)
        assert excinfo.value.error_code == "ADAE99"
        assert excinfo.value.input_params == {"path_file": path}