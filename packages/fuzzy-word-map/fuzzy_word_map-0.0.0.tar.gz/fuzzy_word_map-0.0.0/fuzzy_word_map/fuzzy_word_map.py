# 너그러운 단어 검색기
# 한글은 자모 분해 지원
from functools import reduce

import Levenshtein
import jamo

class WordMap:
    def __init__(self):
        self.words: list[str] = []
        self.letter_to_word_set: dict[str, set[str]] = {}

    def add(self, word: str):
        letters = divide_jamo(word)
        self.words.append(word)
        for letter in letters:
            if letter not in self.letter_to_word_set:
                self.letter_to_word_set[letter] = set([word])
            else:
                self.letter_to_word_set[letter].add(word)

    def remove(self, word: str):
        letters = divide_jamo(word)
        self.words.remove(word)
        word_sets = (self.letter_to_word_set[letter] for letter in letters
                     if letter in self.letter_to_word_set)
        for word_set in word_sets:
            word_set.discard(word)

    def find(self, word: str):
        # letters = set(divide_jamo(word)) & set(self.letter_to_word_set.keys())
        # sets = [self.letter_to_word_set[letter] for letter in letters]
        sets = [self.letter_to_word_set[letter] for letter in set(divide_jamo(word))
                if letter in self.letter_to_word_set]
        candidates = reduce(lambda a, b: a & b, sets) if sets else set()

        def similarity_score(a: str, b: str) -> float:
            dist = Levenshtein.distance(a, b)
            max_len = max(len(a), len(b))
            return 1 - dist / max_len if max_len > 0 else 1.0

        # 갯수 제한하고 싶지만 정렬을 하려면 제한할 수가 없다.
        # 물론 정렬 한 후에 일부만 취하는 것도 의미는 있다.
        sorted_word_weight_tuples = sorted(
            ((w, similarity_score(word, w)) for w in candidates),
            key=lambda x: x[1],
            reverse=True
        )
        more_fuzzy_list = one_miss_intersections_union(sets)
        sorted_words = [x[0] for x in sorted_word_weight_tuples]
        return sorted_words + list(more_fuzzy_list - set(sorted_words))

def divide_jamo(word:str):
    return jamo.j2hcj(jamo.h2j(word))

# 철자 하나 무시하고 유사 문자열 찾기
def one_miss_intersections_union(sets: list[set]) -> set:
    n = len(sets)
    if n <= 1:
        return set()

    # 누적 왼쪽, 오른쪽 교집합
    left = [None] * n
    right = [None] * n

    left[0] = sets[0]
    for i in range(1, n):
        left[i] = left[i - 1] & sets[i]

    right[-1] = sets[-1]
    for i in range(n - 2, -1, -1):
        right[i] = right[i + 1] & sets[i]

    result = set()
    for i in range(n):
        if i == 0:
            inter = right[1]
        elif i == n - 1:
            inter = left[n - 2]
        else:
            inter = left[i - 1] & right[i + 1]
        result.update(inter)

    return result

if __name__ == '__main__':
    words = WordMap()
    words.add("asd")
    words.add("박현영")
    words.add("현영")

    print(words.find("a바"))
    print(words.find("aㅂ"))
    print(words.find("ㅂ혀영"))
    print(words.find("박현영"))
    print(words.find("ㅎ영"))
