# Code-Switching Metrics Using Intonation Units
This repository holds the code used for the EMNLP 2023 paper. It is meant to process transcripts where each row in a spreadsheet (e.g., Excel) represents a single Intonation Unit (IU).

| Speaker Type | IU no punctuation        | Clean Lag Tag |
| --------     | -------                  | ---           |
| Participant  | le decían el preprimer.  | SL            |
| ...          | ...                      |...            |

1. Speaker Type: Describes whether the utterance was spoken by the Interviewer or the Participant. We used this to select transcripts that were majority monological (majority spoken by Participant).
2. IU no punctuation: Represents an IU utterance after filtering out punctuation.
3. Clean Lag Tag: This is the most relevant column in our paper. It contains all relevant language tags for an IU, which for our analysis is some combination of E, S, or L. See the example above and in our paper.

