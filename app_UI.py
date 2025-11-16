import gradio as gr

from typing import List
from difflib import Differ
from sentence_generator import SentenceGenerator
from utils import get_nb_sentences, get_target_language

class AppUI:
    def __init__(self):
        self.sg = SentenceGenerator()
        self.target_sentences = ["" for _ in range(get_nb_sentences())]
        self.reference_sentences = ["" for _ in range(get_nb_sentences())]
    

    def generate_sentences(self)->List[str]:
        sentences = self.sg.generate_sentences()
        for i in range(get_nb_sentences()):
            self.target_sentences[i] = sentences[i]["english"]
            self.reference_sentences[i] = sentences[i][get_target_language()]
        return self.target_sentences
    

    def compare_all_sentences(self, *answers):
        d = Differ()
        results = []

        for i, user_answer in enumerate(answers):
            reference = self.reference_sentences[i]
            diff = [
                (token[2:], token[0] if token[0] != " " else None)
                for token in d.compare(user_answer.split(), reference.split())
            ]
            diff = [d for d in diff if d[1] in [None, "+", "-"]]
            results.append(diff)

        return results


    def launch_ui(self)->None:
        sentences_markdowns = [gr.Markdown() for _ in range(get_nb_sentences())]
        sentences_answers = [gr.Textbox() for _ in range(get_nb_sentences())]
        results_highlight = [gr.HighlightedText(
            label="Your Answer",
            show_legend=True,
            color_map={
                "+": "green",
                "-": "red"
            }
        ) for _ in range(get_nb_sentences())]

        def menu_ui()->gr.Blocks:
            with gr.Blocks() as interface:
                generate_btn = gr.Button(f"Generate {get_nb_sentences()} Sentences")

                generate_btn.click(
                    fn=self.generate_sentences, 
                    outputs=sentences_markdowns
                )
            return interface
        
        def sentences_ui()->gr.Blocks:
            with gr.Blocks() as interface:
                gr.Markdown("# Translate The Sentences")
                with gr.Column():
                    for i in range(get_nb_sentences()):
                        with gr.Group():
                            gr.Markdown(f"## Sentence {i+1}")
                            sentences_markdowns[i].render()
                            sentences_answers[i].render()
                check_answers_btn = gr.Button("Check Answers")

                check_answers_btn.click(
                    fn=self.compare_all_sentences,
                    inputs=sentences_answers,
                    outputs=results_highlight
                )
            return interface
        
        def results_ui()->gr.Blocks:
            with gr.Blocks() as interface:
                gr.Markdown("Here are your results!")
                with gr.Column():
                    for i in range(get_nb_sentences()):
                        with gr.Group():
                            gr.Markdown(f"## Sentence {i+1}")
                            results_highlight[i].render()

            return interface
        

        ui = gr.TabbedInterface(
            [
                menu_ui(),
                sentences_ui(),
                results_ui()
            ],
            ["Menu", "Translate Sentences", "Results"],
        )
        ui.launch()