from django.shortcuts import render
from django.http import HttpResponse, Http404
import json

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch


model_name = "microsoft/DialoGPT-medium"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)



def index(request):
    return render(request, "chat/index.html")


def get_answer(request):
    if request.method == "POST":
        data = request.body.decode('utf-8')[1:-1]
        if "history" in request.session:
            history = torch.Tensor(request.session["history"]).int()
        else:
            history = ""

        new_massage = data[data.find(":")+2:-1]
        input_ids = tokenizer.encode(new_massage + tokenizer.eos_token, return_tensors="pt")

        bot_input_ids = input_ids

        history = model.generate(
            bot_input_ids,
            min_length=20,
            max_length=1000,
            do_sample=True,
            top_p=0.95,
            top_k=0,
            temperature=0.75
        )
        request.session["history"] = history.tolist()
        output = tokenizer.decode(history[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
        content = {"ans": output}
        return HttpResponse(json.dumps(content), content_type="application/json")
    raise Http404()
