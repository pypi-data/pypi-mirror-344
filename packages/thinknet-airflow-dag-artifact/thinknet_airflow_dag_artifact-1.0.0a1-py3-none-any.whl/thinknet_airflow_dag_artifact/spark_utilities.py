from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.utils import AnalysisException
from py4j.protocol import Py4JJavaError
from thinknet_application_specific_exception import raise_error
from thinknet_variable_validator import validate_and_strip_str_variable
from thinknet_airflow_dag_artifact.error_data import ErrorData

def read_from_s3_as_dataframe(spark: SparkSession, path_file: str) -> DataFrame:
    validate_and_strip_str_variable(path_file)
    try:
        df = spark.read.parquet(path_file)
    except AnalysisException:
        raise_error(
            ErrorData.ADAF01,
            {"path_file": path_file},
        )
    except Py4JJavaError as e:
        java_exception = str(e.java_exception)
        if "NoSuchBucket" in java_exception:
            raise_error(
                ErrorData.ADAC01,
                {"path_file": path_file},
            )
        elif "AccessDeniedException" in java_exception:
            raise_error(
                ErrorData.ADAP01,
                {"path_file": path_file},
            )
        else:
            raise_error(
                ErrorData.ADAE99,
                {"path_file": path_file},
            )
    return df

def write_dataframe_to_s3(df: DataFrame, path_file: str) -> None:
    validate_and_strip_str_variable(path_file)
    if not isinstance(df, DataFrame):
        raise_error(
            ErrorData.ADAT01,
            {"df": df},
        )

    print(f"Start writing df to s3 at path: {path_file}")
    try:
        df.write.mode('overwrite').parquet(path_file)
    except AnalysisException:
        raise_error(
            ErrorData.ADAN01,
            {"df": df, "path_file": path_file},
        )
    except Py4JJavaError as e:
        java_exception = str(e.java_exception)
        if "NoSuchBucket" in java_exception:
            raise_error(
                ErrorData.ADAC01,
                {"df": df, "path_file": path_file},
            )
        elif "AccessDeniedException" in java_exception:
            raise_error(
                ErrorData.ADAP02,
                {"df": df, "path_file": path_file},
            )
        else:
            raise_error(
                ErrorData.ADAE99,
                {"df": df, "path_file": path_file},
            )
