from agents import Agent, InputGuardrail, GuardrailFunctionOutput, Runner
from dotenv import load_dotenv
from pydantic import BaseModel
import asyncio


# https://platform.openai.com/traces
# https://openai.github.io/openai-agents-python/quickstart/
class HomeworkOutput(BaseModel):
    is_homework: bool
    reasoning: str


guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the user is asking about homework.",
    model="gpt-4o-mini",
    output_type=HomeworkOutput,
)

math_tutor_agent = Agent(
    name="Math Tutor",
    handoff_description="Specialist agent for math questions",
    model="gpt-4o-mini",
    instructions="You provide help with math problems. Explain your reasoning at each step and include examples",
)

history_tutor_agent = Agent(
    name="History Tutor",
    handoff_description="Specialist agent for historical questions",
    model="gpt-4o-mini",
    instructions="You provide assistance with historical queries. Explain important events and context clearly.",
)


async def homework_guardrail(ctx, agent, input_data):
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_output_as(HomeworkOutput)
    return GuardrailFunctionOutput(
        output_info=final_output,
        # tripwire_triggered=not final_output.is_homework,
        tripwire_triggered=False,
    )


triage_agent = Agent(
    name="Triage Agent",
    instructions="You determine which agent to use based on the user's homework question",
    handoffs=[history_tutor_agent, math_tutor_agent],
    model="gpt-4o-mini",
    input_guardrails=[
        InputGuardrail(guardrail_function=homework_guardrail),
    ],
)


async def main():
    result = await Runner.run(triage_agent, "who was the first president of the united states?")
    print(result.final_output)
    print("===========")

    # result = await Runner.run(triage_agent, "what is life")  # not a homework question
    # print(result.final_output)


if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())
