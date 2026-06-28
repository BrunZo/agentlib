from agentlib.coding.tasks import SYSTEM_PROMPT, refactor_function
from agentlib.completions.openrouter import Message, OpenRouterChat


def main():
    chat = OpenRouterChat()
    chat.append_message(Message(role="system", content=SYSTEM_PROMPT))

    while (target := _prompt_for_function()) is not None:
        refactor_function(chat, target)

    print(chat.transcript())


def _prompt_for_function() -> tuple[str, str] | None:
    payload = input("input [module]:[function] (blank to quit) ").strip()
    if not payload:
        return None
    module, function = payload.split(":")
    return module, function


if __name__ == "__main__":
    main()
