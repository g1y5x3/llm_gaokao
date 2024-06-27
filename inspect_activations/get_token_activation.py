import torch, pickle, argparse
import matplotlib.pyplot as plt
import seaborn as sns
from transformers import AutoModelForCausalLM, AutoTokenizer

# Function to get activations
def get_activations(model, input_ids):
    activations = []
    
    # select only the last token's activation
    def hook_fn(module, input, output):
        activations.append(output[0].detach().to(torch.float32).squeeze(0)[-1].cpu().numpy())
    
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
    print(model)

    prompt = "Given the universal set $U=\{1,2,3,4,5\}$ and set $A=\{2,4\}$, find $\\bar{A}$?"
    # prompt = "设全集 $U=\{1,2,3,4,5\}$ ，集合 $A=\{2,4\}$ ，求 $\\bar{A}$ ？"
    messages = [{"role": "user",   "content": prompt}]
    input_ids = tokenizer.apply_chat_template(conversation=messages, tokenize=True, return_tensors='pt')

    # Generate response token by token
    generated = input_ids.to('cuda')
    token_activation_pairs = []
    for _ in range(max_length - len(generated[0])):
        activations = get_activations(model, generated)

        outputs = model(generated)
        next_token_logits = outputs.logits[:, -1, :]
        next_token = torch.argmax(next_token_logits, dim=-1).unsqueeze(0)

        print(tokenizer.decode(next_token[0], skip_special_tokens=True))
        decoded_token = tokenizer.decode(next_token[0], skip_special_tokens=True)
        token_activation_pairs.append((decoded_token, activations))

        generated = torch.cat([generated, next_token], dim=-1)
        if next_token.item() == tokenizer.eos_token_id: break

    with open("token_activations.pkl", "wb") as f:
        pickle.dump(token_activation_pairs, f)

    response = tokenizer.decode(generated[0][input_ids.shape[1]:], skip_special_tokens=True)

    print(f"Prompt: {prompt}\n")
    print(f"Response:\n{response}\n")

