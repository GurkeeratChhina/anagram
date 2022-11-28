import time

primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41,
          43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101]
raw_input = 'mit_10000.txt'


def letter_to_prime(letter):
    """Encodes letters as prime numbers.

    Example usage: letter_to_prime("e") = 11
    """

    index = ord(letter) - ord('a')
    return primes[index]


def word_to_number(word):
    """Assigns a number to a word.

    Two words get the same number if and only if they have the same letters,
    but possibly in different orders.
    Example usage: word_to_number("hello") = 19*11*37*37*47 = 13447687
    """

    product = 1
    for letter in word:
        product = product * letter_to_prime(letter)
    return product

def word_anagrams(word, word_dict):
    """A wrapper function for finding anagrams of a given word
    
    Example usage: word_anagrams("aber", english_words) = ["bear", "bare"]
    """

    key = word_to_number(word)
    return word_dict[key]


def search_strings(list_of_strings, english_dict):
    """Find a list of possible sentences from anagramming each string.

    The output is a list of list of strings, where the first list of 
    strings indicates all options for the first word, the second list 
    of strings indicates all options for the second word, and so on.
    Example usage: search_strings(["a", "aber", "aet", "em"]) =
    [["a"], ["bear", "bare"], ["ate", "eta", "tea"], ["me"]]
    """

    list_of_sentences = []
    for string in list_of_strings:
        key = word_to_number(string)
        try:
            values = english_dict[key]
            list_of_sentences.append(values)
        except:
            return []
    return list_of_sentences


def search_ints(list_of_ints, english_dict):
    """Similar to search_strings, but the strings are represented by ints.

    The output is a list of list of strings, where the first list of 
    strings indicates all options for the first word, the second list 
    of strings indicates all options for the second word, and so on.
    Example usage: search_ints([2, 4026, 1562, 451]) =
    [["a"], ["bear", "bare"], ["ate", "eta", "tea"], ["me"]]
    """

    list_of_sentences = []
    for key in list_of_ints:
        try:
            values = english_dict[key]
            list_of_sentences.append(values)
        except:
            return []
    return list_of_sentences


# TODO: Look into representing factors as a dictionary or collections.counter instead of sorting

def reduce_factor_combinations(list_of_factor_combinations):
    """Compute a new list of factor combinations by combining pairs of factors.

    A factor_combination is a list of ints, named such because each 
    factor_combination in the list_of_factor_combinations has the same product.
    Furthermore, each factor_combination has the same number of factors as each
    other factor_combination in the list, and there should be no duplicates.
    For example, [2,2] and [1,4] are distinct factor_combinations of length two.
    An example of duplicate factor_combinations would be [1,4] and [4,1]
    Factor_combinations are sometimes referred to as just factors.

    Example usage: reduce_factor_combinations([[6, 7, 8], [11, 12, 13]]) =
    [ [42, 8], [48, 7], [6, 56], [132, 13], [143, 12], [11, 156] ]
    """

    output = set()
    for factors in list_of_factor_combinations:
        n = len(factors)
        for i in range(0, n):
            for j in range(i+1, n):
                new_list = [factors[x] for x in range(0,n) if x not in [i, j]]
                new_list += [factors[i] * factors[j]]
                output.add(tuple(sorted(new_list)))
    return [list(x) for x in output]


def sentence_anagrams(string):
    """Computes all sentence anagrams of a given string, inserting spaces as necessary.

    The output is a list of sentences, where a sentence is a list of lists of words.
    Each list of words in a sentence indicates all possible anagrams of a word that 
    are possible with a subset of letters. The output contains no duplicate sentences.
    For example, [["a"], ["bear", "bare"]] would be a sentence, 
    and [["bare", "bear"], ["a"]] would be a duplicate of that sentence.    
    """

    n = len(string)
    list_of_factors = [[letter_to_prime(letter) for letter in string]]
    lists_of_sentences = []
    while (n > 1):
        lists_of_sentences += [search_ints(factors, word_dict) 
                               for factors in list_of_factors 
                               if search_ints(factors, word_dict)]
        list_of_factors = reduce_factor_combinations(list_of_factors)
        n -= 1
    return lists_of_sentences


def import_raw_to_dict(file_name):
    """Import the raw list of english words to a dictionary.

    Dictionary format: {number: [list_of_words]}
    where word_to_number(word) = number for each word in [list_of_words]
    """

    word_dict = {}
    with open(file_name) as file:
        for line in file:
            value = line.strip().lower()
            key = word_to_number(value)
            word_dict[key] = word_dict.get(key, [])+[value]
    return word_dict


def time_function(fun, *args, n):
    """Determines how long it takes to run the given function n times."""

    start = time.perf_counter()
    for i in range(n):
        fun(*args)
    end = time.perf_counter()
    return end-start


# This is all basically manually testing xd
if __name__ == '__main__':
    print("Importing dictionary, please wait...")
    word_dict = import_raw_to_dict(raw_input)
    print("Finished importing!")

    while True:
        string = input("Enter a string to descramble: \n")
        try:
            key = word_to_number(string)
        except:
            print("Please make sure to only use letters a-z in your string!", end=" ")
            continue
        try:
            values = word_dict[key]
            print("Here is a list of possible words your string could be:", values)
        except:
            print("No words were found!")

        # TODO: Test the new sentence anagram code
        print("Searching sentences:")
        start = time.perf_counter()
        lists_of_sentences = sentence_anagrams(string)
        end = time.perf_counter()
        print("Sentences found:")
        for sentence in lists_of_sentences:
            print(sentence)
        print("Time elapsed:", end-start)
