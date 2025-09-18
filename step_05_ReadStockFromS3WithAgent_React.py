import boto3
import pandas as pd
from io import BytesIO
from langchain_aws.chat_models import ChatBedrock
from langchain_experimental.agents import create_pandas_dataframe_agent

# -----------------------
# Load CSV from S3
# -----------------------
def load_csv_from_s3(bucket_name, object_key, region_name='us-east-1'):
    s3_client = boto3.client('s3', region_name=region_name)
    obj = s3_client.get_object(Bucket=bucket_name, Key=object_key)
    csv_data = pd.read_csv(BytesIO(obj['Body'].read()))
    return csv_data

# -----------------------
# Interactive Agent
# -----------------------
def interactive_csv_agent(df):
    # ✅ Use Claude 3.7 Sonnet via system-defined inference profile ARN
    llm = ChatBedrock(
        model="arn:aws:bedrock:us-east-1:539772171138:inference-profile/us.anthropic.claude-3-7-sonnet-20250219-v1:0",
        provider="anthropic",
        region="us-east-1"
    )

    agent = create_pandas_dataframe_agent(
        llm,
        df,
        verbose=True,
        allow_dangerous_code=True,
        max_iterations=10
    )

    print("CSV loaded. Ask me anything. Type 'exit' to quit.\n")
    while True:
        user_input = input("Your question: ")
        if user_input.lower().strip() == 'exit':
            break
        try:
            result = agent.invoke(user_input)
            print("\nAgent answer:", result["output"], "\n")
        except Exception as e:
            print("\nError:", e, "\n")

# -----------------------
# Main
# -----------------------
if __name__ == "__main__":
    bucket_name = 'pathikrith-stock-data-bucket-1'
    object_key = 'StockData.csv'

    df = load_csv_from_s3(bucket_name, object_key)
    print("shape of df:", df.shape)
    interactive_csv_agent(df)
