from agents import Agent, RunContextWrapper

from ci_agents.infra_agent import infra_agent
from ci_agents.infra_agent_fake_test import infra_fake_agent
from ci_agents.lab_agent import lab_agent
from ci_agents.types import AnalysisContext, AIResponse
from hooks.agent_hook_log import global_log_hook
from hooks.hub_hook_context import agent_hook_for_context


def hub_agent_instructions(context: RunContextWrapper[AnalysisContext], agent: Agent[AnalysisContext]) -> str:
    system_prompt = f"""You are a mobile E2E automation expert specializing in analyzing CI automation failure reports."
    You know that the mobile E2E automation depends many and deep traces to complete with going through one testing,so we need to dive into the details of the failure logs and analyze the root cause of the failure.
    Here we've abstracted our root cause as:
    1. failed by lab environment issue;  [Lab_Issue]
    2. failed by infrastructure issue; [Infrastructure_Issue]
    3. failed by third-party issue; [Third_Party_Issue]
    4. failed by AT script issue (like expired locators, scripts bugs, apps UI/Bugs/Flow introduced);[AT_Script]
    You will receive context in {context.context} to aid in analysis:
    You have the following tools available:\n
    1. infra_agent: Analyze if failure is caused by an infrastructure issue (device, driver, network issues)
    2. lab_agent: Analyze if failure is caused by a lab environment issue

    (other tools are not implemented yet)
    each tool will return a json format result, and you need to decide the final analysis result by calling the tools and decide the final analysis result.
    Use these tools to investigate the failure. Always check for meaningful log data before responding directly.
    please note that the context could be not completed and in each agent tool, it could retrieve more context to analyze the failure logs.
    #Output Requirements:
    If you decide the failure was caused by the issue as agent tools, as your final structured response, possibly adding your own insights if helpful.
    """
    return system_prompt


hub_agent = Agent[AnalysisContext](
    name="hub_agent",
    model="gpt-4o-mini",
    hooks=global_log_hook,
    instructions=hub_agent_instructions,
    output_type=AIResponse,
    tools=[
        lab_agent.as_tool(
            tool_name="lab_agent",
            tool_description="Analyze the failure logs to determine if the failure is caused by a lab environment issue."
        ),
        infra_agent.as_tool(
            tool_name="infra_agent",
            tool_description="Analyze the failure logs to determine if the failure is caused by an infrastructure issue (device, driver, network issues)"
        )

    ]
)
