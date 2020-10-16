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
    types = {
        'melgan': 0,
        '1enc': 1,
        '2enc': 2,
        'proposed': 3
    }
    # 180 - 36*3 - 12 = 60
    # 60 / 3 = 20
    lst = lst1 + lst2 + lst3 + lst4 + lst4 + lst1[:20] + lst2[:20] + lst3[:20]

    for i in range(18):
        j = (form_id + i*10) % len(lst)
        files.append(lst[j])

    random.shuffle(files)

    for i, f in enumerate(files):
        method = os.path.basename(os.path.dirname(f))
        basename = os.path.basename(f)
        typ = types[method]
        ret.append(
            {
                "title": f"問題{i+1}",
                "audio_path": f,
                "name": f"q{i+1}",
                "type": typ
            }
        )
    return ret

def main():
    """Main function."""
    loader = FileSystemLoader(searchpath="./templates")
    env = Environment(loader=loader)
    template = env.get_template("mos.html.jinja2")

    args = get_args()
    random.seed(args.form_id)
    questions = gen_questions(form_id=args.form_id)


    html = template.render(
        page_title=f"語音品質實驗 {args.form_id}",
        form_url="https://script.google.com/macros/s/AKfycbxpNFr1U6Jdy6BB10fwVR5Idy_wAdVSxgCs38oT00AAcg4WGvco/exec",
        form_id=args.form_id,
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
    with open(f'mos_{args.form_id}', 'w') as f:
        for q in questions:
            f.write(f'{q["type"]}\t')
    print(html)

if __name__ == "__main__":
    main()
