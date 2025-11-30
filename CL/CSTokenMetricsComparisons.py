# load the excel data
import pandas as pd
import matplotlib.colors as mc # For the legend
import matplotlib.pyplot as plt
import matplotlib.colors
import numpy as np

class CSTokenMetricsComparisons:
  def __init__(self, data, n_languages=2, IU_tag_col_name="Clean Lang Tag", word_tag_col_name = "Words Lang Tag", text_col_name="IU no punctuation"):
    self.df = data
    self.IU_tag_col_name = IU_tag_col_name
    self.word_tag_col_name = word_tag_col_name
    self.text_col_name = text_col_name
    self.n_languages = n_languages
    self.IU_lang_visualizations = []
    """
    Dictionary storing all the ingo we will eventually populate. Entry examples include:
    - total_rows      : how many IUs are there in the transcript? (int)
    - IU_lang_rows    : language tags per IU after filtering non- S/E/L (list of strs)
    - L_count         : how many lone items are present? (list of ints, counting Ls per IU)
    - within-switch   : # of within IU CS (diff. based on the token) (int)
    - across-switch   : # of of across IU CS (int)
    - prosodic-switch : counting CS based on language and IU sentence (dict of SE/ES counts)
    """
    self.data_dict = {
        "IU"  : {
            "multi": {},
            "both" : {}
        },
        "word": {
            "multi": {},
            "both" : {}
        }
    }


  """
  This function should get called first, to populate the data_dict structure.
  """
  def process_raw_info(self, CS_type="multi", token_level="IU"):
    prev_letter = ""
    raw_counts = {
        "total_valid_rows": 0,    # rows counted after filtering for desired language tags
        "total_rows"      : 0,
        "lang_tag_counts" : {
                             "S": 0,
                             "E": 0,
                            },
        "L_count"         : [],   # how many IUs have Ls? (and how many?)
        "IU_lang_rows"    : [],   # language tag measurements after filtering out non- S/E/L
    }

    # get appropriate data column
    data_rows = None
    if token_level == "IU":
      data_rows = self.df[self.IU_tag_col_name].astype(str)
    elif token_level == "word":
      data_rows = self.df[self.word_tag_col_name].astype(str)
    else:
      raise Exception("Did not enter a valid token level. Please enter either 'IU' or 'word'.")

    # loop through every IU row in the transcript
    for i in range(len(data_rows)):
      # we want to filter out anything that isn't L or S or E (depending on our 'include_L' flag)
      curr_row = data_rows[i]
      curr_row = [x for x in curr_row if x in ["L", "S", "E"]]
      if len(curr_row) > 0:
        raw_counts["total_valid_rows"] += 1

      # count the Ls in the current IU row
      if CS_type == "both":
        L_count = curr_row.count("L")
        raw_counts["L_count"].append(L_count)

      # process every tag in the IU
      curr_tags = []
      for lang_idx, lang in enumerate(curr_row):

        # this will only happen once for each for loop / IU row;
        if (token_level == "IU" and lang_idx == 0) or token_level == "word":
          # properly increment the lang tag counts (currently for the IU)
          if lang == "S":
            raw_counts["lang_tag_counts"]["S"] += 1
          elif lang == "E":
            raw_counts["lang_tag_counts"]["E"] += 1

        # populate the filtered language tags properly; if L, switch it according to the second param!
        if lang == "L":
          if prev_letter == "E":
            if CS_type == "both": # it counts as CS, so we will switch it
              curr_tags.append("L")
            else:
              curr_tags.append("E")
          elif prev_letter == "S":
            if CS_type == "both":
              curr_tags.append("L")
            else:
              curr_tags.append("S")
        else:
          curr_tags.append(lang)

        prev_letter = lang

      raw_counts["IU_lang_rows"].append(curr_tags)

    raw_counts["total_rows"] = len(raw_counts["IU_lang_rows"])

    self.data_dict[token_level][CS_type] = raw_counts
    return raw_counts

  """
  NOTES:
  - This function does count the Ls.
  - Because of that, some IUs from the total_valid_rows number don't actually count (i.e.,
      if an IU starts with an L, for example).
  """
  def m_index(self, CS_type="multi", token_level="IU"):
    # add a check here that throws an error in case they haven't processed raw counts yet
    if len(self.data_dict[token_level][CS_type]) == 0:
      raise Exception("Data hasn't been processed! Please call process_raw_counts with the same parameters before calling this function.")

    lang_counts = self.data_dict[token_level][CS_type]["lang_tag_counts"]
    lang_counts = [lang_counts["E"], lang_counts["S"]]

    # NOTE: Different number than self.data_dict[token_level][CS_type]["total_valid_rows"], which will also count a row as valid if it starts with an L (which we don't count here in our total).
    total_rows = lang_counts[0] + lang_counts[1]

    for i in range(len(lang_counts)):
      lang_counts[i] /= total_rows
      lang_counts[i] = lang_counts[i] ** 2

    p_sum = lang_counts[0] + lang_counts[1]
    self.M_index = (1 - p_sum) / ((self.n_languages - 1) * p_sum)

    return self.M_index

  def across_IU(self, CS_type="multi", token_level="IU"):
    if len(self.data_dict[token_level][CS_type]) == 0:
      raise Exception("Data hasn't been processed! Please call process_raw_counts with the same parameters before calling this function.")

    tag_cols = self.data_dict[token_level][CS_type]["IU_lang_rows"]
    prev = ""
    total, switch_count = 0, 0
    for row in tag_cols:
      if len(row) > 0:
        total += 1
      for i, tag in enumerate(row):
        if i == 0 and prev != "" and prev != tag and prev != "L":
          switch_count += 1
        prev = tag
    self.data_dict[token_level][CS_type]["across-switch"] = switch_count

    return switch_count, total

  """
  Remember: this is a binary count that only counts once if a switch is present within the IU.
  """
  def within_IU(self, CS_type="multi", token_level="IU"):
    if len(self.data_dict[token_level][CS_type]) == 0:
      raise Exception("Data hasn't been processed! Please call process_raw_counts with the same parameters before calling this function.")

    tag_cols = self.data_dict[token_level][CS_type]["IU_lang_rows"]

    total, switch_count = 0, 0
    for row in tag_cols:
      if len(row) > 0:
        total += 1
        # the below is to ensure we don't double count, since an L will already be considerd as an across IU switch
        if row[0] == "L":
          row = row[1:]
        unique_tags = set("".join(row))
        if len(unique_tags) > 1:
          switch_count += 1
    self.data_dict[token_level][CS_type]["within-switch"] = switch_count

    return switch_count, total

  def i_index(self, CS_type="multi", token_level="IU"):
    if len(self.data_dict[token_level][CS_type]) == 0:
      raise Exception("Data hasn't been processed! Please call process_raw_counts with the same parameters before calling this function.")

    if token_level == "IU":
      return self.__iu_i_index__(CS_type, token_level)
    elif token_level == "word":
      return self.__word_i_index__(CS_type, token_level)
    raise Exception("Invalid token level. Pleaseuse either 'IU' or 'word'.")

  """
  This function calculates the normal I-Index using word tokens by going through
  the transcript in sequential order. We only print the result, and don't return.
  """
  def __word_i_index__(self, CS_type="multi", token_level="IU"):
    tag_cols = self.data_dict[token_level][CS_type]["IU_lang_rows"]

    prev = ""
    total, switch_count = 0, 0
    for row in tag_cols:
      for tag in row:
        total += 1
        # remember, we aren't counting switching out of a lone tag.
        if prev != "" and prev != tag and prev != "L":
          switch_count += 1
        prev = tag

    i_index = switch_count / (total - 1)

    self.data_dict[token_level][CS_type]["CS-count"] = switch_count
    self.data_dict[token_level][CS_type]["I-index"] = i_index
    return switch_count, i_index

  def __iu_i_index__(self, CS_type="multi", token_level="IU"):
    # within IU only
    within_count, within_total = self.within_IU(CS_type, token_level)
    across_count, across_total = self.across_IU(CS_type, token_level)

    numerator = across_count + within_count - (across_count * (within_count / within_total))
    i_index = numerator / max(within_total, across_total)

    self.data_dict[token_level][CS_type]["CS-count"] = numerator
    self.data_dict[token_level][CS_type]["I-Index"] = i_index
    return numerator, i_index

  def count_CS_prosodic(self, CS_type="multi", token_level="IU"):
    if len(self.data_dict[token_level][CS_type]) == 0:
      raise Exception("Data hasn't been processed! Please call process_raw_counts with the same parameters before calling this function.")

    tag_cols = self.data_dict[token_level][CS_type]["IU_lang_rows"]
    word_col = self.df[self.text_col_name].astype(str).tolist()

    prev = ""
    SE, ES, total = 0, 0, 0
    for i, tags in enumerate(tag_cols):
      for j, tag in enumerate(tags):
        if prev != "" and prev != tag: # there's a switch!
          # is it within the prosodic boundary?
          # the first condition checks if we're the 1st tag in our row AND the
          # previous character of the transcription line isn't the end of a prosodic
          # sentence. the second condition is if we're not the first tag in the IU.

          if (j == 0 and word_col[i - 1][-1] not in [".", "?"]) or j > 0:
              total += 1
              if prev == "E" and tag == "S":
                ES += 1
              elif prev == "S" and tag == "E":
                SE += 1
              elif tag == "L":
                if prev == "E":
                  ES += 1
                elif prev == "S":
                  SE += 1
              elif prev == "L":
                total -= 1
        prev = tag
    assert (total == SE + ES)

    self.data_dict[token_level][CS_type]['prosodic-CS'] = {
        "SE"    : SE,
        "ES"    : ES,
        "total" : total
    }
    return SE, ES

  def visualize_transcript(self, CS_type="multi", token_level="IU", cmap_colors=["#0a437a", "#ADD8E6"], filepath="", save=False):
    if len(self.data_dict[token_level][CS_type]) == 0:
      raise Exception("Data hasn't been processed! Please call process_raw_counts with the same parameters before calling this function.")

    tag_cols = self.data_dict[token_level][CS_type]["IU_lang_rows"]
    # tags_merged = [tag for tags in tag_cols for tag in tags if tag in ["S", "E"]]
    # tags_merged = np.asarray(tags_merged)
    # print(tags_merged)
    # lang_distr = np.where(tags_merged == "E", 0, 1)

    lang_distributions = []
    for tags in tag_cols:
      for tag in tags:
        if tag == "E":
          lang_distributions.append(0)
        elif tag == "S":
          lang_distributions.append(1)
    # print(lang_distr)
    lang_distributions = np.asarray(lang_distributions).reshape(1, len(list(lang_distributions)), order="F")
    fig, ax = plt.subplots(figsize=(8, 4))

    if len(cmap_colors) != self.n_languages:
      raise Exception(f"Number of colors for plot should match # of languages, i.e., {self.n_languages}.")

    cmap = matplotlib.colors.ListedColormap(cmap_colors)
    ax.pcolormesh(lang_distributions, cmap=cmap)
    ax.set_frame_on(False)
    plt.yticks([])
    ax.set_ylim(top=0.5)

    if save:
      plt.savefig(filepath)
    return