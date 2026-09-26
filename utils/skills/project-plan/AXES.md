# Task classification

You should classify each task (see definitions.md) into two axes:

Originality: 
- 1 = Saturated commodity
- 10 = Uncharted territory

Cognitive return: 
- 1 = Boring chore
- 10 = Profound technical challenge

Be brutally honest. Humans tend to regards their ideas as more interesting than they actually are. You can web search for similar projects to produce your answer.


## Examples

```
User Input: "Build an OS from scratch that sticks to a minimalist design"
Output: {"originality": 4, "cognitive": 10}
```

```
User Input: "Migrate my personal blog frontend from Next.js to a Vite + React setup."
Output: {"originality": 2, "cognitive": 2}
```

```
User Input: "Write a local python script to parse PDF filenames of sheet music, scrape the Henle difficulty level from their website, and rename the files."
Output: {"originality": 6, "cognitive": 4}
```

```
User Input: "Organize local directory with my math books"
Output: {"originality": 1, "cognitive": 1}
```

```
User Input: "Write my Math thesis about analytical number theory"
Output: {"originality": 8, "cognitive": 10}
```

```
User Input: "Build an agent that scrapes news following my investment"
Output: {"originality": 3, "cognitive": 6}
```

## Current input

User Input: "{input\_text}"


Your output must conform to the format:

```json
{"originality": [int], "cognitive": [int]}
```

where each [int] should be replaced with an integer between 1 and 10 inclusive. Do not add \`\`\`json tags. Your output should be processable by json.loads(your\_output)

