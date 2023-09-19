def read_input_bits(file_path):
    obs = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip().split()  # Split the line into bit pairs
            obs.extend(line)  # Add the bit pairs to the observations list
    return obs

# Specify the path to your input file
input_file_path = 'encoded_output.txt'
obs = read_input_bits(input_file_path)
start_metric = {'zero': 0, 'one': 0, 'two': 0, 'three': 0}
state_machine = {
    'zero': {'b1': {'out_b': "11", 'prev_st': 'one', 'input_b': 0},
             'b2': {'out_b': "00", 'prev_st': 'zero', 'input_b': 0}},
    'one': {'b1': {'out_b': "01", 'prev_st': 'three', 'input_b': 0},
            'b2': {'out_b': "10", 'prev_st': 'two', 'input_b': 0}},
    'two': {'b1': {'out_b': "11", 'prev_st': 'zero', 'input_b': 1},
            'b2': {'out_b': "00", 'prev_st': 'one', 'input_b': 1}},
    'three': {'b1': {'out_b': "10", 'prev_st': 'three', 'input_b': 1},
              'b2': {'out_b': "01", 'prev_st': 'two', 'input_b': 1}},
}


def bits_diff_num(num_1, num_2):
    count = 0
    for i in range(0, len(num_1), 1):
        if num_1[i] != num_2[i]:
            count = count + 1
    return count


def viterbi(obs, start_metric, state_machine):
    V = [{}]
    for st in state_machine:
        V[0][st] = {"metric": start_metric[st]}

    for t in range(1, len(obs) + 1):
        V.append({})
        for st in state_machine:
            prev_st = state_machine[st]['b1']['prev_st']
            first_b_metric = V[t - 1][prev_st]["metric"] + bits_diff_num(state_machine[st]['b1']['out_b'], obs[t - 1])
            prev_st = state_machine[st]['b2']['prev_st']
            second_b_metric = V[t - 1][prev_st]["metric"] + bits_diff_num(state_machine[st]['b2']['out_b'], obs[t - 1])

            if first_b_metric > second_b_metric:
                V[t][st] = {"metric": second_b_metric, "branch": 'b2'}
            else:
                V[t][st] = {"metric": first_b_metric, "branch": 'b1'}

    smaller = min(V[len(obs)][st]["metric"] for st in state_machine)

    for st in state_machine:
        if V[len(obs)][st]["metric"] == smaller:
            source_state = st
            output_bits = []
            for t in range(len(obs), 0, -1):
                branch = V[t][source_state]["branch"]
                output_bits.append(state_machine[source_state][branch]['input_b'])
                source_state = state_machine[source_state][branch]['prev_st']
            output_bits.reverse()
            with open('output_bits.txt', 'w') as output_file:
                output_file.write(''.join(map(str, output_bits)))
            break  # Exit the loop after finding the smallest metric

# Rest of your code remains unchanged

viterbi(obs, start_metric, state_machine)
