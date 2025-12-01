# Intonation Unit (IU)-Boundary constraint

This repository holds the code for the EMNLP 2023 paper titled ["Code-Switching Metrics Using Intonation Units"](https://aclanthology.org/2023.emnlp-main.1047/) and the 2025 _Computational Linguistics_ journal article titled ["Re-evaluating the word token for bilingual speech processing: The case for Intonation Units"](https://direct.mit.edu/coli/article/doi/10.1162/COLI.a.580/134133).

```bash
├── CL
│   ├── CL_Comparisons.ipynb
│   ├── CSTokenMetricsComparisons.py
├── EMNLP
│   ├── Language Distribution Graphs/
│   ├── EMNLP_IU_Boundary_code.ipynb
├── README.md
├── requirements.txt
```

# Data Formatting

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

# Citations

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