import boto3, re
import pandas as pd
from io import BytesIO
from langchain_aws.chat_models import ChatBedrock
from langchain_experimental.agents import create_pandas_dataframe_agent

# Load csv from S3 bucket
def load_csv_from_s3(bucket_name, object_key, region_name='us-east-1'):
    s3_client = boto3.client('s3', region_name=region_name)
    obj = s3_client.get_object(Bucket=bucket_name, Key=object_key)
    csv_data = pd.read_csv(BytesIO(obj['Body'].read()))
    return csv_data

# Interactive agent to query the dataframe
def interactive_csv_agent(df):
    # Use Claude 3.7 Sonnet via system-defined inference profile ARN
    llm = ChatBedrock(
        model="arn:aws:bedrock:us-east-1:539772171138:inference-profile/us.anthropic.claude-3-7-sonnet-20250219-v1:0",
        provider="anthropic",
        region="us-east-1",
        temperature=0.0,
    )

    # Step 1-3 : Ask LLM to generate code
    prompt = f""" You are a data analyst. You are given a pandas dataframe with stock data that
    contains these columns: {', '.join(df.columns)}.
    Write python code using pandas to answer the following question:
    
    {user_input}

    Rules:
    - Use only the dataframe named 'df'
    - The questions are always about data within the dataframe, please write code and answer accordingly
    - Only output pure Python code (no text, no explanation, no comments, no markdown)
    - execute the code and store the final answer in a variable named 'result''
    - The code must be syntactically correct and runnable as-is
    - The code must produce only the minimal correct answer (no extra words or sentences)
    - Do not print, describe, or format the answer
    """
    
    raw= llm.invoke(prompt).content.strip()
    print("Raw LLM output:\n", raw)

    # Remove any markdown formatting if present
    code = re.sub(r"^```(?:python)?\s*", "", raw, flags=re.MULTILINE)
    code = re.sub(r"\s*```.*$", "", code, flags=re.MULTILINE)
    # code = re.sub(r'\\\n', '', code)       # remove accidental line continuations
    # code = re.sub(r'\n\s+', ' ', code)     # flatten broken f-strings into one line

    print("Cleaned code:\n", code)

    # Step 4: Execute the generated code
    local_scope = {"df": df}
    exec(code, {}, local_scope)
    ## Assuming the result is stored in a variable named 'result' in the generated code
    result=local_scope.get("result", "See printed output above.")
    print("Execution Result:\n", result) 

    # Step 5: Ask LLM to interpret the result
    summary_prompt = f"Answer: {result}\nAnswer in 1 sentence.\nJust format the input as a concise summary.No other text"
    answer = llm.invoke(summary_prompt).content.strip()
    print("Summary answer:\n", answer)
    return answer

# Main execution
if __name__ == "__main__":
        bucket_name = 'pathikrith-stock-data-bucket-1'
        object_key = 'StockData.csv'

        df = load_csv_from_s3(bucket_name, object_key)
        print("shape of df:", df.shape)
        print("CSV loaded. Ask me anything. Type 'exit' to quit.\n")
        while True:
            user_input = input("Your question: ")
            if user_input.lower().strip() == 'exit':
                break
            try:
                answer = interactive_csv_agent(df)
                print("\nAgent answer:", answer, "\n")
            except Exception as e:
                print("\nError:", e, "\n")