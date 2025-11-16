import gradio as gr

from typing import List
from sentence_generator import SentenceGenerator
from utils import get_nb_sentences, get_target_language

class AppUI:
    def __init__(self):
        self.sg = SentenceGenerator()
        self.target_sentences = ["" for _ in range(get_nb_sentences())]
        self.reference_sentences = ["" for _ in range(get_nb_sentences())]
    

    def generate_sentences(self)->List[str]:
        sentences = self.sg.generate_sentences()
        for i, s in enumerate(sentences):
            self.target_sentences[i] = s[get_target_language()]
            self.reference_sentences[i] = s["english"]
        return self.target_sentences

    def launch_ui(self)->None:
        sentences_markdowns = [gr.Markdown() for _ in range(get_nb_sentences())]
        sentences_answers = [gr.Textbox() for _ in range(get_nb_sentences())]

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
                gr.Button("Check Answers")

            return interface
        
        def results_ui()->gr.Blocks:
            with gr.Blocks() as interface:
                gr.Markdown("Here are your results!")
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