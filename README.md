# cvmatch

CVMatch compares a candidate's CV with a job posting using the Gemini API. It returns a match score (0–100), matched and missing skills, the candidate's strengths, recommendations for improving the CV, and a verdict.

## Project structure

```
cvmatch/
├── prompts/
│   └── prompt.json          # system prompt, user prompt template, output format
├── data/
│   └── example_01–06.json   # example inputs (X) and expected outputs (y)
└── diagrams/
    ├── mermaid/             # component and sequence diagrams (Mermaid)
    └── plantuml/            # the same diagrams (PlantUML)
```

## Prompt

[`prompts/prompt.json`](prompts/prompt.json) contains the system prompt and a user prompt template with `{{cv}}` and `{{job_ad}}` placeholders. The model must return JSON with these fields:

| Field | Type | Description |
|---|---|---|
| `match_score` | number | Match score from 0 to 100 (mandatory requirements 70%, nice-to-haves 30%) |
| `matched_skills` | string[] | Requirements the candidate meets |
| `missing_skills` | string[] | Requirements the candidate is missing |
| `strengths` | string[] | 2–3 strengths for this position |
| `recommendations` | string[] | 2–4 specific CV improvement suggestions |
| `verdict` | string | `Strong match` (80–100), `Partial match` (50–79), `Weak match` (20–49), `Not a match` (0–19) |

## Examples

Each file in [`data/`](data/) contains an input `X` (`cv`, `job_ad`) and the expected output `y`.

| File | Scenario | Score | Verdict |
|---|---|---|---|
| [example_01](data/example_01.json) | Python developer -> Python backend position | 85 | Strong match |
| [example_02](data/example_02.json) | Junior Java developer -> Full-stack position | 52 | Partial match |
| [example_03](data/example_03.json) | Accountant -> DevOps engineer position | 5 | Not a match |
| [example_04](data/example_04.json) | Data analyst with e-commerce experience -> data analyst position | 82 | Strong match |
| [example_05](data/example_05.json) | Marketing specialist -> digital marketing manager (lacks management experience) | 62 | Partial match |
| [example_06](data/example_06.json) | Very short CV with little information -> QA tester position | 30 | Weak match |

## Diagrams

### Component diagram

Mermaid source: [`diagrams/mermaid/2-component.mmd`](diagrams/mermaid/2-component.mmd)

```mermaid
flowchart TB
    User["User"]

    subgraph CVMatch
        UI["User Interface (UI)"]

        IPrep(("IDataPreparation"))
        IPrompt(("IPromptGeneration"))
        IVal(("IResponseValidation"))
        IViz(("IResultsVisualization"))

        Prep["Data Preparation Module"]
        PromptGen["Prompt Generator"]
        Validator["Response Validator"]
        Viz["Results Visualization"]
    end

    IGemini(("generateContent<br/>(REST / JSON)"))

    subgraph GoogleCloud["Google Cloud"]
        Gemini["Gemini API"]
    end

    User -->|"CV file,<br/>job posting text"| UI

    UI -.->|"1. prepare(cv, jobPosting)"| IPrep
    UI -.->|"2. generate(data)"| IPrompt
    UI -..->|"3. send(prompt)"| IGemini
    UI -.->|"4. validate(response)"| IVal
    UI -.->|"5. render(result)"| IViz

    IPrep --- Prep
    IPrompt --- PromptGen
    IGemini --- Gemini
    IVal --- Validator
    IViz --- Viz
```

PlantUML version ([`diagrams/plantuml/2-component.puml`](diagrams/plantuml/2-component.puml)):

![Component diagram (PlantUML)](diagrams/plantuml/2-component.png)

<details>
<summary>PlantUML source</summary>

```plantuml
@startuml CVMatch_Component
skinparam componentStyle rectangle

actor "User" as User

package "CVMatch" {
  [User Interface (UI)] as UI

  interface "IDataPreparation" as IPrep
  interface "IPromptGeneration" as IPrompt
  interface "IResponseValidation" as IVal
  interface "IResultsVisualization" as IViz

  [Data Preparation Module] as Prep
  [Prompt Generator] as PromptGen
  [Response Validator] as Validator
  [Results Visualization] as Viz
}

interface "generateContent\n(REST / JSON)" as IGemini

cloud "Google Cloud" {
  [Gemini API] as Gemini
}

User --> UI : CV file,\njob posting text

UI ..> IPrep : 1. prepare(cv, jobPosting)
UI ..> IPrompt : 2. generate(data)
UI ..> IGemini : 3. send(prompt)
UI ..> IVal : 4. validate(response)
UI ..> IViz : 5. render(result)

IPrep -- Prep
IPrompt -- PromptGen
IGemini -- Gemini
IVal -- Validator
IViz -- Viz
@enduml
```

</details>

### Sequence diagram

Mermaid source: [`diagrams/mermaid/3-sequence.mmd`](diagrams/mermaid/3-sequence.mmd)

```mermaid
sequenceDiagram
    actor User as User
    participant UI as User Interface (UI)
    participant Prep as Data Preparation<br/>Module
    participant PromptGen as Prompt<br/>Generator
    participant Gemini as Gemini API
    participant Validator as Response<br/>Validator
    participant Viz as Results<br/>Visualization

    User->>UI: Uploads CV file
    User->>UI: Enters job posting text
    User->>UI: Clicks "Analyze"
    activate UI

    UI->>Prep: prepare(cvFile, jobPostingText)
    activate Prep
    Prep->>Prep: extract text from PDF / DOCX
    Prep->>Prep: clean and normalize text
    Prep->>Prep: check that both texts are non-empty
    Prep-->>UI: PreparedData {cvText, jobPostingText}
    deactivate Prep

    UI->>PromptGen: generate(preparedData)
    activate PromptGen
    PromptGen->>PromptGen: fill in prompt template
    PromptGen->>PromptGen: add JSON schema and instructions
    PromptGen-->>UI: prompt
    deactivate PromptGen

    UI->>Gemini: POST generateContent(prompt,<br/>responseMimeType = "application/json")
    activate Gemini
    Gemini-->>UI: 200 OK, response text (JSON)
    deactivate Gemini

    UI->>Validator: validate(responseText)
    activate Validator
    Validator->>Validator: parse JSON
    Validator->>Validator: check schema<br/>(score 0–100, required fields)
    Validator-->>UI: AnalysisResult
    deactivate Validator

    UI->>Viz: render(result)
    activate Viz
    Viz->>Viz: build score indicator,<br/>skill lists, recommendations
    Viz-->>UI: results view
    deactivate Viz

    UI-->>User: Shows match score, skills,<br/>strengths and recommendations
    deactivate UI
```

PlantUML version ([`diagrams/plantuml/3-sequence.puml`](diagrams/plantuml/3-sequence.puml)):

![Sequence diagram (PlantUML)](diagrams/plantuml/3-sequence.png)

<details>
<summary>PlantUML source</summary>

```plantuml
@startuml CVMatch_Sequence
actor "User" as User
participant "User Interface (UI)" as UI
participant "Data Preparation\nModule" as Prep
participant "Prompt\nGenerator" as PromptGen
participant "Gemini API" as Gemini
participant "Response\nValidator" as Validator
participant "Results\nVisualization" as Viz

User -> UI : Uploads CV file
User -> UI : Enters job posting text
User -> UI : Clicks "Analyze"
activate UI

UI -> Prep : prepare(cvFile, jobPostingText)
activate Prep
Prep -> Prep : extract text from PDF / DOCX
Prep -> Prep : clean and normalize text
Prep -> Prep : check that both texts are non-empty
Prep --> UI : PreparedData {cvText, jobPostingText}
deactivate Prep

UI -> PromptGen : generate(preparedData)
activate PromptGen
PromptGen -> PromptGen : fill in prompt template
PromptGen -> PromptGen : add JSON schema and instructions
PromptGen --> UI : prompt
deactivate PromptGen

UI -> Gemini : POST generateContent(prompt,\nresponseMimeType = "application/json")
activate Gemini
Gemini --> UI : 200 OK, response text (JSON)
deactivate Gemini

UI -> Validator : validate(responseText)
activate Validator
Validator -> Validator : parse JSON
Validator -> Validator : check schema\n(score 0–100, required fields)
Validator --> UI : AnalysisResult
deactivate Validator

UI -> Viz : render(result)
activate Viz
Viz -> Viz : build score indicator,\nskill lists, recommendations
Viz --> UI : results view
deactivate Viz

UI --> User : Shows match score, skills,\nstrengths and recommendations
deactivate UI
@enduml
```

</details>
