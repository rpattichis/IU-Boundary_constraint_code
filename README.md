# Intonation Unit (IU)-Boundary constraint

Official code for: 

- ["Code-Switching Metrics Using Intonation Units"](https://aclanthology.org/2023.emnlp-main.1047/) (EMNLP 2023)

We adapt two metrics, multilinguality and code-switching (CS) probability, and apply them to transcribed bilingual speech, for the first time putting forward Intonation Units (IUs) – prosodic speech segments – as basic tokens for NLP tasks. We calculate these two metrics separately for distinct mixing types: alternating-language multi-word strings and single-word incorporations from one language into another. Results indicate that there is a shared tendency among bilinguals for multi-word CS to occur across, rather than within, IU boundaries. 

- ["Re-evaluating the word token for bilingual speech processing: The case for Intonation Units"](https://direct.mit.edu/coli/article/doi/10.1162/COLI.a.580/134133) (_Computational Linguistics_ 2025)

Switch points are far more likely between words at IU boundaries than between words in the same IU. Here, we put forward an IU-based adaptation of a familiar metric of code-switching (CS) probability. We then compare the token levels on this metric. Our comparison shows that the currently standard two-significant-figure precision of the word-based metric is insufficient, as the token level compresses the range of values by inflating the universe of CS. 

This repo contains code to **process IU and word tokens for two code-switching (CS) metrics**, namely the Integration Index (I-Index) (Guzmán et al 2017) and the Multilingual Index (M-Index) (Barnett et al. 2000)**. 

For the IU token, we have two methods of processing its language tags for the I-Index:
1. Across-IU I-Index vs. Within-IU I-Index (EMNLP 2023):
2. Unified I-Index (_Computational Linguistics_ 2025):

## Contents

```bash
├── CL
│   ├── Language Distribution Graphs (word)/
│   ├── CL_Comparisons.ipynb
│   ├── CSTokenMetricsComparisons.py
├── EMNLP
│   ├── Language Distribution Graphs/
│   ├── EMNLP_IU_Boundary_code.ipynb
│   ├── IUBoundaryMetrics.py
├── README.md
```

## Data Formatting

This code is meant to process transcripts where each row in a spreadsheet (e.g., Excel) represents a single Intonation Unit (IU), as shown below.

| Speaker Type | IU no punctuation        | Clean Lang Tag | Words Lang Tag |
| --------     | -------                  | ---            |---             |
| Participant  | le decían el preprimer.  | SL             | SSSL           |
| ...          | ...                      |...             |...             |

Note that the last column, 'Words Lang Tag', is only a requirement when running the _CL_ code.

1. Speaker Type: Describes whether the utterance was spoken by the Interviewer or the Participant. We used this to select transcripts that were majority monological (majority spoken by Participant).
2. IU no punctuation: Represents an IU utterance filtering out special symbols (e.g., for vowel lengthening, laughter, vocal noises).
3. Clean Lag Tag: This is the most relevant column in the EMNLP paper. It contains all relevant language tags for an IU, which for our analysis is some combination of E, S, or L. See the example above and in our paper.
4. Words Lang Tag: This is the most relevant column in the _CL_ journal article. It contains all relevant language tags per IU at the word level, which for our analysis is some combination of E, S, or L. 

## Citations

If using the code from the ```EMNLP`` folder, please cite as:

```
@inproceedings{pattichis2023code,
  title={Code-switching metrics using intonation units},
  author={Pattichis, Rebecca and LaCasse, Dora and Trawick, Sonya and Cacoullos, Rena Torres},
  booktitle={Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing},
  pages={16840--16849},
  year={2023}
}
```

If using the code from the ```CL`` folder, please cite as:

```
@article{pattichis2025re,
  title={Re-evaluating the word token for bilingual speech processing: The case for Intonation Units},
  author={Pattichis, Rebecca and LaCasse, Dora and Torres Cacoullos, Rena},
  journal={Computational Linguistics},
  pages={1--22},
  year={2025},
  publisher={MIT Press 255 Main Street, 9th Floor, Cambridge, Massachusetts 02142, USA~…}
}
```