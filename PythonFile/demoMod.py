import modal


app = modal.App("app-demo")

image = modal.Image.debian_slim().pip_install("diffusers", "transformers", "accelerate").pip_install("peft", "fastapi[standard]", "uvicorn")

## Tells modal that these should only be imported when inside the remote  ConnectionAbortedError
with image.imports():
    from diffusers import AutoPipelineForText2Image
    import torch

    import io
    from fastapi import Response 

@app.cls(image=image, gpu="A10G")
class Model:

    @modal.method()
    def load_weights(self):
        self.pipe = AutoPipelineForText2Image.from_pretrained("stabilityai/sdxl-turbo", torch_dtype=torch.float16, variant="fp16")
        self.pipe.to("cuda")

    @modal.method()
    def load_lora_weights(self):
        
        self.pipe.load_lora_weights("nerijs/pixel-art-xl", adapter_names="pixel")
        self.pipe.set_adapters(["pixel"], adapter_weights=[1.2])
        
    @modal.web_endpoint()
    def generate(self, prompt = "A cinematic shot of a baby racoon wearing an intricate italian priest robe."):

        image = self.pipe(prompt=prompt, num_interface_steps=1, guidance_scale=0.0).images[0]
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG")
        return Response(content=buffer.getvalue(), media_type="image/jpeg")



