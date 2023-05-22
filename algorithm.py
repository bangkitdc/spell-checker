import re

dictionary = []

with open('dataset/ind_wikipedia_2021_1M-words.txt', 'r', encoding='utf-8') as file:
    for line in file:
        data = line.split('\t')
        word = data[1].strip()
        number = data[2].strip()
        dictionary.append((word, number))

def spell_checker(input_string):
    words = re.findall(r'\w+|[^\w\s]', input_string)
    suggestions = []
    corrected_sentence = []
    index = 0

    for word in words:
        if word.isalpha() and not any(entry[0].lower() == word.lower() for entry in dictionary):
            closest_match = find_closest_match(word)
            similarity_ratio = calculate_similarity_ratio(word, closest_match)
            if similarity_ratio >= 0.75:
                corrected_sentence.append(closest_match)
                suggestions.append((closest_match, index))
            else:
                corrected_sentence.append(word)
        else:
            corrected_sentence.append(word)
        index += len(word) + 1

    return suggestions, ' '.join(corrected_sentence)

def calculate_similarity_ratio(word1, word2):
    max_length = max(len(word1), len(word2))
    distance = levenshtein_distance(word1, word2)
    similarity_ratio = (1.0 - distance / max_length) * 100
    return similarity_ratio

def find_closest_match(word):
    closest_match = None
    min_distance = float('inf')
    max_count = 0

    for dict_word, count in dictionary:
        if len(dict_word) == len(word):
            distance = levenshtein_distance(word, dict_word)
            if distance < min_distance:
                max_count = int(count)
                min_distance = distance
                closest_match = dict_word
            elif distance == min_distance and int(count) >= max_count:
                max_count = int(count)
                min_distance = distance
                closest_match = dict_word

    return closest_match if closest_match is not None else ''

def levenshtein_distance(word1, word2):
    m, n = len(word1), len(word2)
    if m == 0:
        return n
    if n == 0:
        return m

    dp = [[0] * (n+1) for _ in range(m+1)]

    for i in range(m+1):
        dp[i][0] = i
    for j in range(n+1):
        dp[0][j] = j

    for i in range(1, m+1):
        for j in range(1, n+1):
            cost = 0 if word1[i-1] == word2[j-1] else 1
            dp[i][j] = min(dp[i-1][j] + 1, dp[i][j-1] + 1, dp[i-1][j-1] + cost)

    return dp[m][n]