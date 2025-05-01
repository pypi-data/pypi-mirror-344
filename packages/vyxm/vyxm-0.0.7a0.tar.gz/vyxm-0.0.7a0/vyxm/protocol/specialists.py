from transformers import pipeline
import subprocess

# Transformers LLM Executor
class TransformersLLMExecutor:
    def __init__(self, model_name="gpt2"):
        self.generator = pipeline("text-generation", model=model_name)

    def Run(self, query):
        result = self.generator(query)
        return result[0]["generated_text"]


# Ollama Executor
class OllamaExecutor:
    def __init__(self, model_name="llama2"):
        self.model_name = model_name

    def Run(self, query):
        result = subprocess.run(
            ["ollama", "run", self.model_name, query],
            capture_output=True,
            text=True
        )
        return result.stdout.strip()


# Llama.cpp Executor
class LlamaCppExecutor:
    def __init__(self, model_path="models/llama.bin"):
        self.model_path = model_path

    def Run(self, query):
        result = subprocess.run(
            ["llama", "-m", self.model_path, "-p", query],
            capture_output=True,
            text=True
        )
        return result.stdout.strip()


# Diffusers Image Generation Executor
class DiffusersImageGenExecutor:
    def __init__(self, model_id="CompVis/stable-diffusion-v1-4"):
        from diffusers import StableDiffusionPipeline
        import torch

        self.pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
        self.pipe.to("cuda" if torch.cuda.is_available() else "cpu")

    def Run(self, prompt):
        image = self.pipe(prompt).images[0]
        image.save("output.png")
        return "Image saved as output.png"
