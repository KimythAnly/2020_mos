#!/usr/bin/env python3
"""Generate forms for human evaluation."""

from jinja2 import FileSystemLoader, Environment

import argparse
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--form_id", "-i", required=True, type=int)
    args = parser.parse_args()
    return args

import os
import glob
import random
def gen_questions(form_id=0):
    ret = []
    files = []
    lst1 = sorted(glob.glob('data/1enc/*.wav'))
    lst2 = sorted(glob.glob('data/2enc/*.wav'))
    lst3 = sorted(glob.glob('data/proposed/*.wav'))
    lst4 = sorted(glob.glob('data/melgan/*.wav'))
    lst = lst1 + lst2 + lst3 + lst4
    for i in range(18):
        j = (form_id + i*36) % len(lst)
        files.append(lst[j])
    random.shuffle(files)
    for i, f in enumerate(files):
        method = os.path.dirname(f)
        basename = os.path.basename(f)
        ret.append(
            {
                "title": f"問題{i+1}",
                "audio_path": f,
                # "name": f"{form_id}_{i+1}_{method}_{basename}"
                "name": f"q{i+1}"
            }
        )    
    return ret

def main():
    """Main function."""
    loader = FileSystemLoader(searchpath="./templates")
    env = Environment(loader=loader)
    template = env.get_template("mos.html.jinja2")

    args = get_args()
    questions = gen_questions(form_id=args.form_id)

    html = template.render(
        page_title=f"語音品質實驗 {args.form_id}",
        form_url="https://script.google.com/macros/s/AKfycbxpNFr1U6Jdy6BB10fwVR5Idy_wAdVSxgCs38oT00AAcg4WGvco/exec",
        form_id=0,
        # questions=[
        #     {
        #         "title": "問題 1",
        #         "audio_path": "wavs/test1.wav",
        #         "name": "q1"
        #     },
        #     {
        #         "title": "問題 2",
        #         "audio_path": "wavs/test2.wav",
        #         "name": "q2"
        #     },
        # ]
        questions=questions
    )
    print(html)


if __name__ == "__main__":
    main()
