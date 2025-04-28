def union(set1, set2):
    return {key: max(set1.get(key, 0), set2.get(key, 0)) for key in set(set1) | set(set2)}

def intersection(set1, set2):
    return {key: min(set1.get(key, 0), set2.get(key, 0)) for key in set(set1) & set(set2)}

def complement(fuzzy_set):
    return {key: 1 - value for key, value in fuzzy_set.items()}

def main():
    fuzzy1 = {'a': 0.2, 'b': 0.5, 'c': 0.7}
    fuzzy2 = {'a': 0.4, 'b': 0.6, 'c': 0.3}
    fuzzy3 = {'a': 0.8, 'b': 0.1, 'c': 0.5}

    print("Union of fuzzy1 and fuzzy2:", union(fuzzy1, fuzzy2))
    print("Intersection of fuzzy1 and fuzzy2:", intersection(fuzzy1, fuzzy2))
    print("Complement of fuzzy1:", complement(fuzzy1))
    print("Complement of fuzzy2:", complement(fuzzy2))
    print("Complement of fuzzy3:", complement(fuzzy3))

if __name__ == "__main__":
    main()
