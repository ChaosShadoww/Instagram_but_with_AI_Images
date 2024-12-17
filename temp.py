import modal


stub = modal.Stub("stub-demo")

image = modal.Image.debian_slim().pip_install("diffusers", "transformers", "accelerate")

## Tells modal that these should only be imported when inside the remote  ConnectionAbortedError
with image.imports():
    from diffusers import AutoPipelineForText2Image
    import torch

    import io
    from fastapi import Response #to be able to get Fast API repsonse

@stub.cls(image=image, gpu="H100")## to tell the class to use the image and to give it a gpu
class Model:
    @modal.build()# to tell modal to run initialization code during the build
    @modal.enter()# to tell modal to run initialization code when the container starts up
    def load_weights(self):
        self.piper = AutoPipelineForText2Image.from_pretrained("stabilityai/sdxl-turbo", torch_dtype=torch.float16, variant="fp16")
        self.pipe.to("cuda")
        
    @modal.web_endpoint()
    def generate(self, prompt = "A cinematic shot of a baby racoon wearing an intricate italian priest robe."):
        image = pipe(prompt=prompt, num_interface_steps=1, guidance_scale=0.0).images[0]

        buffer = io.BytesIO()
        image.save(buffer, format="JPEG")# to save image in buffer
        return Response(content=buffer.getvalue(), media_type="image/jpeg")



