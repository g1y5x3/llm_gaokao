import numpy as np
import matplotlib.pyplot as plt
import pickle

"""
english
124 {
125 1
126 ,
127 3
128 ,
129 5
130 \
131 }$

chinese
95  {
96  1
97  ,
98  3
99  ,
100 5
101 \
102 }$
"""

with open("token_activations_chinese.pkl", "rb") as f:
    token_activation_pairs = pickle.load(f)

print(len(token_activation_pairs))
# Choose multiple token-activation pairs to visualize
num_tokens = 50  # Change this to the number of tokens you want to compare
# fig, axes = plt.subplots(num_tokens, 1, figsize=(12, 6*num_tokens), sharex=True)

for i in range(len(token_activation_pairs)):
    token, activations = token_activation_pairs[i]
    print(i, token)
#     activation_array = np.array(activations)
    
#     im = axes[i].imshow(activation_array, aspect='auto', cmap='viridis')
#     axes[i].set_title(f'Token: "{token}"')
#     axes[i].set_ylabel('Layer')
#     axes[i].set_yticks(range(len(activations)))
#     axes[i].set_yticklabels(range(1, len(activations) + 1))

#     # Add colorbar to each subplot
#     plt.colorbar(im, ax=axes[i], label='Activation Value')

# plt.xlabel('Hidden State Dimension')
# plt.suptitle('Activation Heatmaps for Multiple Tokens', fontsize=16)
# plt.tight_layout()

# # Save the figure
# plt.savefig('activation_heatmaps_multiple_tokens.png', dpi=300, bbox_inches='tight')
# plt.close()  # Close the figure to free up memory

# print("Figure saved as activation_heatmaps_multiple_tokens.png")
