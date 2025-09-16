from langchain_aws.chat_models import ChatBedrock
from langchain_experimental.tools import PythonAstREPLTool
from langchain.agents import initialize_agent, AgentType, Tool

python_repl_tool = PythonAstREPLTool()
tools = [Tool(
    name="python_repl_ast",
    func=python_repl_tool.run,
    description="Executes Python code. Input should be valid Python code."
)]

def check_model_capability():
    model_arn = "arn:aws:bedrock:us-east-1:539772171138:inference-profile/us.anthropic.claude-3-7-sonnet-20250219-v1:0"

    print("\n===============================")
    print(f"Using inference profile: {model_arn}")
    print("===============================\n")

    llm = ChatBedrock(
        model=model_arn,
        provider="anthropic",           # ✅ REQUIRED when using ARN
        region="us-east-1"
    )

    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        max_iterations=5,
        handle_parsing_errors=True
    )

    try:
        question = (
            "Use the python tool to run len([1,2,3,4,5]) "
            "and return only the numeric result."
        )
        response = agent.invoke({"input": question})
        print(f"\n📝 Agent response:\n{response}\n")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    check_model_capability()
