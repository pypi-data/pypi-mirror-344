def count_vowels_and_consonants(text):
    vowels = "aeiouAEIOU"
    v_count = c_count = 0
    for char in text:
        if char.isalpha():
            if char in vowels:
                v_count += 1
            else:
                c_count += 1
    return {"vowels": v_count, "consonants": c_count}
