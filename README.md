# CVMatch AI — CV and job ad matching with Gemini

**CVMatch AI** is an information system that uses generative AI (Google Gemini API) to evaluate how well a
candidate's CV matches a job advertisement. It returns structured JSON: a match score, a verdict,
matched and missing skills, and concrete recommendations for improving the CV.

| Input `X` | Output `y` |
| --- | --- |
| `cv` — CV text<br>`job_ad` — job advertisement text | `match_score` (0–100), `verdict`, `matched_skills`, `missing_skills`, `recommendations` |

## Repository structure

```
cvmatch/
├── data/examples.json            # (X, y) pairs — 4 end-to-end examples
├── prompts/
│   └── prompt.json               # test prompt: system prompt + user template (used by Colab and for GPT testing)
├── diagrams/                     # PlantUML (.puml) and Mermaid (.mmd) sources + PNG
└── notebooks/cvmatch_ai_gemini.ipynb   # Google Colab prototype with the Gemini API
```

## Data

| File | Description |
| --- | --- |
| [`data/examples.json`](data/examples.json) | 4 `(X, y)` pairs: `{ "id", "scenario", "X": { "cv", "job_ad" }, "y": { ... } }` |

The examples cover different cases:

| Example | Scenario | `y.match_score` | `y.verdict` |
| --- | --- | --- | --- |
| `example_01` | Python developer → Python backend role | 85 | Strong match |
| `example_02` | Junior Java developer → full-stack role | 52 | Partial match |
| `example_03` | Accountant → DevOps engineer role | 5 | No match |
| `example_04` | Very short CV → junior QA tester role | 30 | Weak match |

All people and companies in the examples are fictional.

## Prompts

- [`prompts/prompt.json`](prompts/prompt.json) — the test prompt. `system_prompt` sets the recruiter role and scoring
  rules, `user_prompt_template` holds the CV and job ad (`{{cv}}`, `{{job_ad}}`) and the JSON structure to return.
  Give it to a GPT agent with `X` from any example and it answers in the `y` format; the Colab notebook sends the
  same prompt to the Gemini API.

## UMLs

### PlantUML Component diagram

```plantuml
@startuml
actor "Job Seeker / Recruiter" as User

rectangle "CVMatch AI" {

    component "REST API\nPOST /match" as API

    component "Input Processor" as Input

    component "Prompt Builder" as Prompt

    component "Gemini API" as Gemini

    component "Result Validator" as Validator
}

file "Prompt Template\n(prompt.json)" as Template

cloud "GitHub Repository" as GitHub


User --> API : CV text +\njob ad text

API --> Input : Validate & clean\ninput

Input --> Prompt : Clean CV +\njob ad

Template --> Prompt : System prompt +\nuser template

Prompt --> Gemini : Filled prompt +\nJSON schema

Gemini --> Validator : Score + skills +\nrecommendations + verdict

Validator --> API : Validated result

API --> User : JSON response

GitHub --> Template : Prompt file
@enduml
```

![PlantUML component diagram](diagrams/component.png)

### Mermaid Component diagram

```mermaid
flowchart LR

    User["Job Seeker / Recruiter"]

    subgraph CVMatch["CVMatch AI"]
        API["REST API<br/>POST /match"]
        Input["Input Processor"]
        Prompt["Prompt Builder"]
        Gemini["Gemini API"]
        Validator["Result Validator"]
    end

    Template[/"Prompt Template<br/>(prompt.json)"/]
    GitHub["GitHub Repository"]

    User -->|"CV text +<br/>job ad text"| API

    API -->|"Validate & clean<br/>input"| Input

    Input -->|"Clean CV +<br/>job ad"| Prompt

    Template -->|"System prompt +<br/>user template"| Prompt

    Prompt -->|"Filled prompt +<br/>JSON schema"| Gemini

    Gemini -->|"Score + skills +<br/>recommendations + verdict"| Validator

    Validator -->|"Validated result"| API

    API -->|"JSON response"| User

    GitHub -->|"Prompt file"| Template
```

### PlantUML Sequence diagram

```plantuml
@startuml
actor "Job Seeker / Recruiter" as User

participant "REST API\n/match" as API
participant "Input Processor" as Input
participant "Prompt Builder" as Prompt
participant "Gemini API" as Gemini
participant "Result Validator" as Validator

User -> API : POST /match\n{cv, job_ad}
API -> Input : Validate & clean texts
Input --> API : Clean CV + job ad + warnings

API -> Prompt : CV + job ad
Prompt -> Prompt : Fill prompt.json template
Prompt --> API : System prompt + user prompt

API -> Gemini : generate_content(prompt, response_schema)
alt Gemini answered
    Gemini --> Validator : JSON answer
else No API key / API error
    API -> Validator : Keyword-overlap fallback result
end

Validator -> Validator : Check fields, clamp score,\nmatch verdict to score
Validator --> API : Validated result

API --> User : JSON response\n{match_score, verdict, matched_skills,\nmissing_skills, recommendations}
@enduml
```

![PlantUML sequence diagram](diagrams/sequence.png)

### Mermaid Sequence diagram

```mermaid
sequenceDiagram
    actor User as Job Seeker / Recruiter
    participant API as REST API /match
    participant Input as Input Processor
    participant Prompt as Prompt Builder
    participant Gemini as Gemini API
    participant Validator as Result Validator

    User->>API: POST /match<br/>{cv, job_ad}
    API->>Input: Validate & clean texts
    Input-->>API: Clean CV + job ad + warnings

    API->>Prompt: CV + job ad
    Prompt->>Prompt: Fill prompt.json template
    Prompt-->>API: System prompt + user prompt

    API->>Gemini: generate_content(prompt, response_schema)
    alt Gemini answered
        Gemini-->>Validator: JSON answer
    else No API key / API error
        API->>Validator: Keyword-overlap fallback result
    end

    Validator->>Validator: Check fields, clamp score,<br/>match verdict to score
    Validator-->>API: Validated result

    API-->>User: JSON response<br/>{match_score, verdict, matched_skills,<br/>missing_skills, recommendations}
```

## Google Colab demo

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/jauniusc/cvmatch/blob/main/notebooks/cvmatch_ai_gemini.ipynb)

The working prototype is [`notebooks/cvmatch_ai_gemini.ipynb`](notebooks/cvmatch_ai_gemini.ipynb). It walks through the
same steps as the sequence diagram: it loads `prompt.json` and `examples.json` from this repository, cleans the CV and
the job ad, fills in the prompt, asks Gemini for a JSON answer and checks that answer. The function
`post_match(cv, job_ad)` joins these steps together, just like the `POST /match` endpoint would.

In the last part every example is sent through the pipeline and the answer is compared with the expected `y`:

- the score difference for each example and the average error;
- whether the verdict is the same;
- a bar chart and a short report for each CV.

There is also a cell where you can paste your own CV and job ad.

**Running it**

1. Create an API key in [Google AI Studio](https://aistudio.google.com/apikey).
2. In Colab open 🔑 Secrets, add `GEMINI_API_KEY` and allow notebook access.
3. Choose Runtime → Run all.

If no key is set, Gemini is not called and a basic keyword comparison fills in the answer instead, so every cell still
runs, but the results are much less accurate.
