from botocore.exceptions import ClientError
from thinknet_application_specific_exception import BaseErrorData

class ErrorData(BaseErrorData):
    ADAF01 = (111, FileNotFoundError, "A FileNotFoundError occurred while reading from S3.The file may not exist at the specified path.")
    ADAF02 = (112, FileNotFoundError, "A FileNotFoundError occured while writing xcom data to file. The file may not exist at the specified path.")
    ADAP01 = (121, PermissionError, "Read Data from S3 with Missing Permissions.")
    ADAP02 = (122, PermissionError, "Write Data to S3 with Missing Permissions.")
    ADAP03 = (123, PermissionError, "Write Data to Airflow Xcom Path with Missing Permissions.")
    ADAC01 = (131, ClientError, "The S3 bucket specified does not exist, please verify the bucket name or check your S3 configuration.")
    ADAN01 = (141, NotImplementedError, "Parquet does not support type in columns.")
    ADAT01 = (151, TypeError, "df to write to s3 is not DataFrame")
    ADAT02 = (152, TypeError, "Non serializable value when trying to write xcom to file")
    ADAE99 = (999, Exception, "Unspecified or unexpected errors.")