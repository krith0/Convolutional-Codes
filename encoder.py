def v_xor(bit0, bit1):
    if bit0 == bit1:
        return "0"
    else:
        return "1"

def viterbi_encoder(inputs):
    s_reg = ["0", "0", "0"]
    encoded_output = []

    for t in range(0, len(inputs)):
        s_reg[2] = s_reg[1]
        s_reg[1] = s_reg[0]
        s_reg[0] = inputs[t]

        output1 = v_xor(v_xor(s_reg[0], s_reg[1]), s_reg[2])
        output2 = v_xor(s_reg[0], s_reg[2])

        encoded_output.append(output1 + output2)

    return encoded_output

# Read the input sequence from a text file
input_file_name = "binary_image_01.txt"
output_file_name = "encoded_output.txt"

try:
    with open(input_file_name, "r") as input_file:
        input_sequence = input_file.read().strip()
except FileNotFoundError:
    print(f"Input file '{input_file_name}' not found.")
    input_sequence = ""

if not input_sequence:
    print("No input sequence provided.")
else:
    # Ensure the length of encoded_output matches the length of the input sequence
    encoded_output = viterbi_encoder(input_sequence)

    # Save the encoded output to a file
    with open(output_file_name, "w") as output_file:
        for item in encoded_output:
            output_file.write(item + " ")

    print(f"Encoded output saved to {output_file_name}")
