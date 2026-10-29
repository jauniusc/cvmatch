# 1.3 HR Job Change: neuroninis tinklas ir Decision Forests

1.3 užduotis: suprasti dėstytojo Colab užrašus ir perdaryti juos su verslo duomenimis iš Kaggle.
Užrašų tekstai anglų kalba, šis aprašas lietuvių.

| Užrašas | Failas | Originalas |
| --- | --- | --- |
| Neuroninis tinklas | [`1_3_hr_job_change_nn.ipynb`](1_3_hr_job_change_nn.ipynb) | [AdventureWorks DW using TensorFlow Neural Network](https://colab.research.google.com/drive/1LLFM2Ba5jAZSna8JnS44frwSLW9mx5As) |
| Decision Forests | [`1_3_hr_job_change_decision_forests.ipynb`](1_3_hr_job_change_decision_forests.ipynb) | [AdventureWorks DW using TensorFlow Decision Forests](https://colab.research.google.com/drive/1zE7b6UlSOreWsgD7lGQOVfEki_xTRDAX) |

## Kaip veikia originalai

**Neuroninis tinklas.** AdventureWorks klientai (`vTargetMail.csv`, 18 484 eilutės), reikia nuspėti `BikeBuyer` (ar nupirks dviratį).
CSV → ID ir asmeninių stulpelių išmetimas → `BikeBuyer` pervadinamas į `target` → padalijimas 80:10:10 → `df_to_dataset` (`tf.data`, paketas 256)
→ `StringLookup` / `IntegerLookup` + `CategoryEncoding` tekstui ir `Normalization` skaičiams → `Dense(64)` → `Dropout` → `Dense(32)` → `Dropout` → `Dense(1)`
→ `adam` + `BinaryCrossentropy(from_logits=True)` → 30 epochų → testas (~0,75) → išsaugojimas ir vieno kliento prognozė.

**Decision Forests.** Tie patys duomenys, padalijimas 90:10, `RandomForestModel(num_trees=10, max_depth=15)`.
Medžiams nereikia nei normalizavimo, nei one-hot, o vertinti juos galima per out-of-bag duomenis. Testo tikslumas ~0,81, nubraižomas vienas medis.

## Duomenų rinkinys ir šaltinis

| | |
| --- | --- |
| Rinkinys | [HR Analytics: Job Change of Data Scientists](https://www.kaggle.com/datasets/arashnic/hr-analytics-job-change-of-data-scientists) (CC0) |
| Failas | [`../data/hr_job_change/aug_train.csv`](../data/hr_job_change/) (19 158 eilučių) |
| Tikslas | `target = 1`, jei kandidatas ieško naujo darbo (25 % kandidatų) |
| Ryšys su CVMatch | tie patys objektai: kandidatai ir darbo pasiūlymai |

## AdventureWorks → HR Job Change

| AdventureWorks | HR Job Change | Pastaba |
| --- | --- | --- |
| `BikeBuyer` → `target` | `target` | ar ieško naujo darbo |
| `Gender`, `MaritalStatus` | `gender` | |
| `EnglishEducation` | `education_level`, `major_discipline` | |
| `EnglishOccupation` | `relevent_experience`, `experience` | `experience` turi reikšmes `<1`, `>20`, todėl paliekama kaip kategorija |
| `CommuteDistance` | `company_size`, `company_type`, `last_new_job` | tekstinės kategorijos |
| `YearlyIncome`, `Age` ir kt. | `city_development_index`, `training_hours` | skaitiniai, normalizuojami |
| `Region` | `city` → išmetama | miestą jau aprašo `city_development_index` |
| ID stulpeliai | `enrollee_id` → išmetama | |
| `tensorflow_decision_forests` | `ydf` | TF-DF neturi paketų Colab naudojamam Python 3.13; YDF yra biblioteka, ant kurios TF-DF pastatytas |

Neuroniniam tinklui trūkstamos tekstinės reikšmės pakeičiamos į `Unknown`. Medžiai trūkstamas reikšmes apdoroja patys.

## Rezultatai

| Modelis | Testo tikslumas | AUC |
| --- | --- | --- |
| Visada „ne" | 0,752 | 0,5 |
| Neuroninis tinklas | 0,765 | 0,794 |
| Random Forest, 10 medžių | 0,785 | 0,788 |
| **Random Forest, 300 medžių** | **0,792** | **0,803** |

- Kadangi naujo darbo ieško tik 25 % kandidatų, tikslumas yra tik šiek tiek didesnis už „visada ne". Todėl modelius lyginu pagal AUC.
- Medžiai šiek tiek geresni už neuroninį tinklą, kaip ir originale.
- Prognozės logiškos: studijuojantis jaunesnysis specialistas 58–67 %, patyręs specialistas didelėje įmonėje 4–9 %.

## Kaip paleisti

Atidaryti Colab (ženkliukas užrašo viršuje) → *Runtime → Run all*. API rakto nereikia, duomenys skaitomi iš šios saugyklos.
