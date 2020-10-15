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
    lst = sorted(glob.glob('data/1enc/*.wav'))
    lst1 = []
    lst2 = []
    comp = ['data/1enc', 'data/2enc', 'data/proposed']
    refdir = 'data/melgan'
    
    for f in lst:
        basename = os.path.basename(f)
        source = basename.split('.')[0].split('_to_')[0]
        target = basename.split('.')[0].split('_to_')[1]
        if source == target:
            continue
        lst1.append([basename, 1, target])
        lst2.append([basename, 2, target])
    
    # 100 - 30*2 = 40
    # 40 / 2 = 20
    lst = lst1 + lst2 + lst1[:20] + lst2[:20]

    ques = []

    for i in range(10):
        j = (form_id + i*10) % len(lst)
        basename, comp_id, target = lst[j]
        ref = os.path.join(refdir, target+'.wav')
        choice = [os.path.join(comp[0], basename), os.path.join(comp[comp_id], basename)]
        random.shuffle(choice)
        ques.append([ref, choice])

    random.shuffle(ques)
    for i, q in enumerate(ques):
        ref, choice = q
        ret.append(
            {
                "title": f"問題{i+1}",
                "ref_path": ref,
                "audio_paths": choice,
                "name": f"q{i+1}"
            }
        )
    return ret

def main():
    """Main function."""
    loader = FileSystemLoader(searchpath="./templates")
    env = Environment(loader=loader)
    template = env.get_template("sim.html.jinja2")

    args = get_args()
    questions = gen_questions(form_id=args.form_id)

    html = template.render(
        page_title=f"語者相似度實驗 {args.form_id}",
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
    # print(questions)
    print(html)


if __name__ == "__main__":
    random.seed(0)
    main()
