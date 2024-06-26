import torch, argparse
import matplotlib.pyplot as plt
import seaborn as sns
from transformers import AutoModelForCausalLM, AutoTokenizer

# Function to get activations
def get_activations(model, input_ids):
    activations = []
    
    def hook_fn(module, input, output):
        if isinstance(output, tuple):
            activations.append(output[0].detach())
        else:
            activations.append(output.detach())
    
    hooks = []
    for layer in model.model.layers:
        hooks.append(layer.register_forward_hook(hook_fn))
    
    with torch.no_grad():
        output = model(input_ids.to('cuda'))
    
    for hook in hooks:
        hook.remove()
    
    return activations

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a model on a CSV file and save the responses.")
    parser.add_argument("--model_name", default="01-ai/Yi-1.5-9B-Chat", type=str, required=False, help="Name of the model to use.")
    parser.add_argument("--max_length", default=4096, type=int, required=False, help="Maximum length for the generated response.")
    args = parser.parse_args()

    model_name = args.model_name
    max_length = args.max_length

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", torch_dtype="auto").eval()

    prompt = "设全集 $U=\{1,2,3,4,5\}$ ，集合 $A=\{2,4\}$ ，求 $\\bar{A}$ ？"
    messages = [{"role": "user",   "content": prompt}]
    input_ids = tokenizer.apply_chat_template(conversation=messages, tokenize=True, return_tensors='pt')

    # Generate response token by token
    generated = input_ids.to('cuda')
    for _ in range(max_length - len(generated[0])):
        activations = get_activations(model, generated)

        outputs = model(generated)
        next_token_logits = outputs.logits[:, -1, :]
        next_token = torch.argmax(next_token_logits, dim=-1).unsqueeze(0)

        generated = torch.cat([generated, next_token], dim=-1)

        if next_token.item() == tokenizer.eos_token_id:
            break
        
        # Visualize activations
        plt.figure(figsize=(15, 10))
        for i, activation in enumerate(activations):
            sns.heatmap(activation[0, -1, :].cpu().numpy().reshape(1, -1), cmap='viridis', ax=plt.subplot(len(activations), 1, i+1))
            plt.title(f"Layer {i+1} Activation")
        plt.tight_layout()
        plt.savefig(f"activation_step_{len(generated[0])}.png")
        plt.close()

    # output_ids = model.generate(input_ids.to('cuda'), eos_token_id=tokenizer.eos_token_id, max_length=max_length)
    response = tokenizer.decode(generated[0][input_ids.shape[1]:], skip_special_tokens=True)

    print(f"Prompt: {prompt}\n")
    print(f"Response:\n{response}\n")

    prompt = "Given the universal set $U=\{1,2,3,4,5\}$ and set $A=\{2,4\}$, find $\\bar{A}$?"
    messages = [{"role": "user",   "content": prompt}]

    input_ids = tokenizer.apply_chat_template(conversation=messages, tokenize=True, return_tensors='pt')
    output_ids = model.generate(input_ids.to('cuda'), eos_token_id=tokenizer.eos_token_id, max_length=max_length)
    response = tokenizer.decode(output_ids[0][input_ids.shape[1]:], skip_special_tokens=True)

    print(f"Prompt: {prompt}\n")
    print(f"Response:\n{response}\n")
