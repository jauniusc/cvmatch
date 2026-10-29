# 1.5 Iš anksto apmokyti modeliai ir transfer learning

1.5 užduotis: suprasti dėstytojo Colab užrašus ir perdaryti juos su savo duomenimis.
Užrašų tekstai anglų kalba, šis aprašas lietuvių.

| Užrašas | Failas | Originalas |
| --- | --- | --- |
| Klasifikacija, objektų aptikimas, segmentacija su viena nuotrauka | [`1_5_one_image_workplace.ipynb`](1_5_one_image_workplace.ipynb) | [Colab One Image](https://colab.research.google.com/drive/1h7GEPDd4ldfEa0J2dJiFO2d2bQATAqsp) |
| Transfer learning | [`1_5_transfer_learning_documents.ipynb`](1_5_transfer_learning_documents.ipynb) | [Colab Transfer learning](https://colab.research.google.com/drive/1uDCip2CIMQN8bg859EZlOR_uWhHaLQNg) |

## Kaip veikia originalai

**Viena nuotrauka.** Nieko nemokoma, naudojami TF Hub modeliai: du EfficientNetV2-S klasifikatoriai (ImageNet-21k ir ImageNet-1k, 384×384, top-4 klasės),
iškirpta nuotraukos dalis, SSD MobileNetV2 objektų aptikimas (Open Images, 600 klasių) ir HRNet segmentacija (ADE20K, 150 klasių).

**Transfer learning.** CIFAR-10 → `Resizing(240)` → užšaldytas EfficientNetV2-B1 (`hub.KerasLayer`, `tf_keras`) → `Dense(10)`.
3 epochos, testas ~88,5 %. Tada modelis įkeliamas iš naujo, mažinamas learning rate, atšildomas, mokomas su augmentacija (3 iteracijos), ~87,6 %.

## Duomenys

| Užrašas | Duomenys |
| --- | --- |
| Viena nuotrauka | 4 darbo vietų nuotraukos iš Wikimedia Commons ([`../data/photos/`](../data/photos/), su autoriais ir licencijomis) ir vienas CV skenas |
| Transfer learning | tas pats CV / laiškų / el. laiškų / formų rinkinys kaip 1.4 ([`../data/documents/`](../data/documents/)) |

## Originalas → ši versija

| Originalas | Ši versija | Pastaba |
| --- | --- | --- |
| Vilniaus, Paryžiaus ir kt. nuotraukos | darbo vietos ir CV skenas | susiję su CVMatch tema |
| viena nuotrauka per kartą | visos nuotraukos klasifikuojamos cikle | |
| segmentacijoje fiksuoti kaukių numeriai | 4 klasės, užimančios daugiausia ploto | numeriai originale parinkti jo nuotraukai |
| CIFAR-10, `Dense(10)` | dokumentai, `Dense(4)` | |
| testas naudojamas ir validacijai | atskira validacijos aibė | |
| augmentacija su horizontaliu apvertimu | be apvertimo, mažesnis pasukimas (0,02) ir poslinkis (0,05) | apverstas dokumentas neatrodo kaip tikras |
| learning rate ×0,1, paketas 64 | `Adam(1e-5)`, paketas 32 | mažiau atminties |
| `model.trainable = True` | tas pats + EfficientNet kviečiamas su `training=False` | BatchNorm lieka su ImageNet statistika, kaip rekomenduoja Keras |

## Rezultatai

**Viena nuotrauka:** biurus modeliai atpažįsta gerai („office", „desk", „workstation"), pokalbio nuotraukoje randa žmones, kostiumą ir stalą,
o segmentacija išskiria lubas, grindis, sienas ir kėdes. CV skeną modeliai vadina „web site" arba „menu", nes ImageNet neturi CV klasės.
Dėl to antrame užraše reikia transfer learning.

**Transfer learning:**

| Modelis | Mokomi parametrai | Testo tikslumas |
| --- | --- | --- |
| Mano CNN nuo nulio (1.4) | 3 267 908 | 0,813 |
| **Užšaldytas EfficientNetV2-B1 + Dense** | **5 124** | **0,855** |
| Po fine-tuning su augmentacija | 6 865 176 | 0,847 |

- Transfer learning lenkia mano CNN, nors mokoma 600 kartų mažiau parametrų ir tik 3 epochas.
- Fine-tuning rezultato nepagerino, kaip ir originale.
- Į klausimą „CV ar ne CV?" modelis teisingai atsako 92,8 % atvejų.

## Kaip paleisti

Atidaryti Colab (ženkliukas užrašo viršuje) → *Runtime → Run all*. Transfer learning užrašui geriau įjungti GPU (*Runtime → Change runtime type → T4 GPU*), nes mano kompiuteryje be GPU fine-tuning truko ~15 min.
