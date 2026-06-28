"""Tests for the Chat ABC, portraying a real chat between two people.

Run with either:
    python -m pytest tests/test_chat.py
    python -m unittest tests.test_chat
from the repository root.
"""

import unittest
from dataclasses import dataclass

from agentlib.completions.chat import Chat


@dataclass
class Message:
    author: str
    content: str

    def __str__(self):
        return f"{self.author}: {self.content}"


def make_conversation() -> Chat:
    """A short back-and-forth between Alice and Bob, like a real chat."""
    chat = Chat()
    chat.append_message(Message("Alice", "Hey Bob, are we still on for lunch?"))
    chat.append_message(Message("Bob", "Hi Alice! Yes, noon works for me."))
    chat.append_message(Message("Alice", "Great. The usual place?"))
    chat.append_message(Message("Bob", "Sounds good. See you there."))
    chat.append_message(Message("Alice", "See you 🙂"))
    return chat


class TestChat(unittest.TestCase):
    def setUp(self):
        self.chat = make_conversation()

    def test_starts_empty(self):
        self.assertEqual(len(Chat()), 0)

    def test_length_tracks_messages(self):
        self.assertEqual(len(self.chat), 5)

    def test_append_returns_the_message(self):
        chat = Chat()
        msg = Message("Alice", "Hello?")
        self.assertIs(chat.append_message(msg), msg)
        self.assertEqual(len(chat), 1)

    def test_messages_preserve_order(self):
        contents = [m.content for m in self.chat]
        self.assertEqual(
            contents,
            [
                "Hey Bob, are we still on for lunch?",
                "Hi Alice! Yes, noon works for me.",
                "Great. The usual place?",
                "Sounds good. See you there.",
                "See you 🙂",
            ],
        )

    def test_indexing(self):
        self.assertEqual(self.chat[0].author, "Alice")
        self.assertEqual(self.chat[1].author, "Bob")
        self.assertEqual(self.chat[-1].content, "See you 🙂")

    def test_authors_alternate(self):
        authors = [m.author for m in self.chat]
        self.assertEqual(authors, ["Alice", "Bob", "Alice", "Bob", "Alice"])

    def test_iteration_is_repeatable(self):
        # Sequence iteration must not exhaust the chat.
        first = [m.content for m in self.chat]
        second = [m.content for m in self.chat]
        self.assertEqual(first, second)

    def test_membership(self):
        opener = Message("Alice", "Hey Bob, are we still on for lunch?")
        self.assertIn(opener, self.chat)
        self.assertNotIn(Message("Carol", "hi"), self.chat)

    def test_reversed(self):
        last = list(reversed(self.chat))[0]
        self.assertEqual(last.author, "Alice")
        self.assertEqual(last.content, "See you 🙂")

    def test_transcript_rendering(self):
        self.assertEqual(
            self.chat.transcript(),
            "Alice: Hey Bob, are we still on for lunch?\n"
            "Bob: Hi Alice! Yes, noon works for me.\n"
            "Alice: Great. The usual place?\n"
            "Bob: Sounds good. See you there.\n"
            "Alice: See you 🙂",
        )

    def test_subclass_can_override_storage(self):
        # Chat is an ABC; a subclass inherits the shared behavior and may
        # override pieces of it. Here we cap the history at the last N messages.
        class RollingChat(Chat):
            def __init__(self, limit: int):
                super().__init__()
                self.limit = limit

            def append_message(self, message: Message) -> Message:
                super().append_message(message)
                self.messages = self.messages[-self.limit :]
                return message

        chat = RollingChat(limit=2)
        for author, content in [("Alice", "1"), ("Bob", "2"), ("Alice", "3")]:
            chat.append_message(Message(author, content))
        # inherited transcript() works on the overridden storage
        self.assertEqual(chat.transcript(), "Bob: 2\nAlice: 3")

    def test_seed_with_existing_messages(self):
        seed = [Message("Bob", "first"), Message("Alice", "second")]
        chat = Chat(seed)
        self.assertEqual(len(chat), 2)
        # Defensive copy: mutating the original list must not affect the chat.
        seed.append(Message("Bob", "third"))
        self.assertEqual(len(chat), 2)


if __name__ == "__main__":
    unittest.main()
