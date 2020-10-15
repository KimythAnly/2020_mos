#!/usr/bin/env python3
"""Generate forms for human evaluation."""

from jinja2 import FileSystemLoader, Environment

import glob
def gen_questions():

    return {}

def main():
    """Main function."""
    loader = FileSystemLoader(searchpath="./templates")
    env = Environment(loader=loader)
    template = env.get_template("mos.html.jinja2")

    questions = gen_question()

    html = template.render(
        page_title="語音品質實驗 0",
        form_url="http://localhost:5488",
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
