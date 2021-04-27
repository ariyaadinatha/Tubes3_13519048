kata_penting = ["Kuis", "Ujian", "Tucil", "Tubes", "Praktikum"]

def boyer_moore_string_matching(sentence, matcher):
    # Constructing bad match table
    bad_match_table = {}
    for i in range(len(matcher)):
        shift = max(1, len(matcher) - i - 1)
        bad_match_table[matcher[i]] = shift
    
    # Boyer moore 
    sentence_idx = 0
    while(sentence_idx <= len(sentence) - len(matcher)):
        matcher_idx = len(matcher) - 1
        # Loop through sentence, matching the pattern from behind
        while(matcher_idx >= 0):
            # If sentence doesn't match break the loop and shift until we don't meet that character again
            if (sentence[matcher_idx+sentence_idx] != matcher[matcher_idx]):
                # If current character in sentence is within bad_match_table we use that value to calculate shifting
                if (sentence[matcher_idx+sentence_idx] in bad_match_table):
                    sentence_idx += bad_match_table[sentence[matcher_idx+sentence_idx]] + matcher_idx - len(matcher) + 1
                # if current character in sentence not in bad_match_table, simply use matcher_idx to shift
                else :
                    sentence_idx += matcher_idx + 1
                break
            # If sentence match the matcher, decrement matcher_idx to check remaining character
            matcher_idx -= 1
        # If matcher_idx survive the loop without breaking, then the matcher is found in the sentence
        if (matcher_idx == -1) :
            return True
    return False

print(boyer_moore_string_matching("ZZZZZOLOLOLOLZZZZZZZZZZZZZLOLOLOL", "LOLOLOL"))
                                #       LOLOLOL


# For debugging:
# def boyer_moore_string_matching(sentence, matcher):
#     # Construction bad match table
#     bad_match_table = {}
#     for i in range(len(matcher)):
#         shift = max(1, len(matcher) - i - 1)
#         bad_match_table[matcher[i]] = shift
#     print(bad_match_table)
#     sentence_idx = 0
#     while(sentence_idx <= len(sentence) - len(matcher)):
#         matcher_idx = len(matcher) - 1
#         while(matcher_idx >= 0):
#             print("Curr Sentence: " + sentence[matcher_idx+sentence_idx] + " Curr Matcher:  " + matcher[matcher_idx])
#             if (sentence[matcher_idx+sentence_idx] != matcher[matcher_idx]):
#                 if (sentence[matcher_idx+sentence_idx] in bad_match_table):
#                     print("found")
#                     sentence_idx += bad_match_table[sentence[matcher_idx+sentence_idx]] + matcher_idx - len(matcher) + 1
#                 else :
#                     print("not found")
#                     sentence_idx += max(1, matcher_idx + 1)
#                 print("sentence_idx is " + str(sentence_idx))
#                 break
#             matcher_idx -= 1
#             print("sentence_idx is " + str(sentence_idx))
#         if (matcher_idx == -1) :
#             return True
#     return False


