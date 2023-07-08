def find_closing_bracket(text, start_index, start_bracket="[", end_bracket="]"):
    end_index = start_index
    acc = 0
    while end_index < len(text):
        cur = text[end_index]
        if cur == start_bracket:
            acc += 1
        elif cur == end_bracket:
            acc -= 1
        if acc == 0:
            break
        end_index += 1
    return end_index
