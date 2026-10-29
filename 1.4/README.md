# 1.4 Ar dokumentas yra CV? TensorFlow CNN

1.4 užduotis: suprasti dėstytojo Colab užrašus ir perdaryti juos su savo vaizdų duomenimis.
Užrašo tekstai anglų kalba, šis aprašas lietuvių.

| Užrašas | Failas | Originalas |
| --- | --- | --- |
| CNN + filtrai + MLP | [`1_4_documents_cnn.ipynb`](1_4_documents_cnn.ipynb) | [Colab CNN](https://colab.research.google.com/drive/1wx-OBEcjPhAfv8AZ5Fl59mp7RY5Hm0Ql) |

## Kaip veikia originalas

CIFAR-10 (32×32 RGB, 10 klasių, įkeliama iš Hugging Face) → normalizavimas `/255` → 100 nuotraukų tinklelis
→ CNN (`Conv2D 32 → Pool → Conv2D 64 → Pool → Conv2D 64 → Flatten → Dense 64 → Dense 10`) → `adam` + `SparseCategoricalCrossentropy(from_logits=True)` → 20 epochų, testas ~70 %.
2 dalis: pirmo sluoksnio filtrai, požymių žemėlapiai ir konvoliucija ranka su `numpy`, kuri sutampa su Keras.
3 dalis: MLP (`Flatten → Dense 32 → 64 → 64 → 10`), ~43 %.

## Duomenų rinkinys ir šaltinis

CVMatch AI gauna CV, bet žmonės gali įkelti ir kitus dokumentus. Todėl modelis mokomas atskirti CV nuo kitų dokumentų, kurie būna pridedami prie darbo paraiškos.

| | |
| --- | --- |
| Klasės | `resume` (CV), `letter`, `email`, `form` |
| Apimtis | 4000 skenų: 2800 mokymo, 600 validacijos, 600 testo (700 / 150 / 150 kiekvienai klasei) |
| Dydis | 128×128, pilki (įkeliami kaip 3 kanalai) |
| Šaltinis | RVL-CDIP (Harley ir kt., 2015), Hugging Face `chainyo/rvl-cdip` |
| Failai | [`../data/documents/`](../data/documents/), sudaryta su [`../scripts/prepare_documents_dataset.py`](../scripts/prepare_documents_dataset.py) |

## CIFAR-10 → dokumentai

| Originalas (CIFAR-10) | Ši versija | Pastaba |
| --- | --- | --- |
| 10 objektų klasių | 4 dokumentų klasės | |
| 32×32 RGB | 128×128, pilki kaip 3 kanalai | 2 dalies trijų kanalų filtrų kodas lieka toks pat |
| `Dense(10)` | `Dense(4)` | |
| testas naudojamas ir validacijai | atskira validacijos aibė | testas paliekamas galutiniam įvertinimui |
| HF `uoft-cs/cifar10` | aplankas su JPEG failais | Colab'e saugykla nusiklonuojama |

Nepakeista: sluoksniai, epochos (CNN 20, MLP 15), optimizatorius, 2 ir 3 dalys.

## Rezultatai

| Modelis | Testo tikslumas |
| --- | --- |
| MLP | 0,25 (atsitiktinis spėjimas) |
| **CNN** | **0,813** |

- CNN gerokai geresnis už MLP. Dokumentams svarbiausia išdėstymas, o MLP po `Flatten` nebežino, kurie pikseliai yra greta.
- Į klausimą „CV ar ne CV?" CNN teisingai atsako 92 % atvejų. Dažniausiai painiojami laiškai su formomis.
- Modelis persimoko: mokymo tikslumas 100 %, validacijos ~0,80.
- Konvoliucija ranka su `numpy` duoda tą patį rezultatą kaip Keras.

## Kaip paleisti

Atidaryti Colab (ženkliukas užrašo viršuje) → *Runtime → Run all*. Mano kompiuteryje (be GPU) visas užrašas trunka ~4 min.
