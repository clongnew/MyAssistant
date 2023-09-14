import gradio as gr
from io import StringIO
import contextlib
import sys
from main_functions import check_name, generate_name, memory_to_list, create_main_agent
from multiprocessing import Process, Queue
import multiprocessing
import traceback

gr_row = lambda scale: gr.Row(scale=scale)
main_agent = create_main_agent()
print('main_agent has been created: ', main_agent, '\n')


def capture_output_and_error(func):
    @contextlib.contextmanager
    def captured_output():
        new_out, new_err = StringIO(), StringIO()
        old_out, old_err = sys.stdout, sys.stderr
        try:
            sys.stdout, sys.stderr = new_out, new_err
            yield new_out, new_err
        finally:
            sys.stdout, sys.stderr = old_out, old_err

    def wrapper(*args, **kwargs):
        result = (None, )
        stdout = ""
        error_message = None

        with captured_output() as (out, err):
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                error_message = str(e)
                traceback_str = traceback.format_exc()
                error_message += "\n" + traceback_str

            stdout = out.getvalue()

        return *result, stdout, error_message

    return wrapper


def main_interface(dialogue_dic):
    with gr.Blocks() as demo:
        with gr.Row():
            # 1.组件函数

            @capture_output_and_error
            def ai_answer(query, current_dialogue, current_name):
                print(f'start_answer agent memory: {main_agent.memory} \n')
                answer = main_agent.run(query)
                if not current_name:
                    current_name = check_name(generate_name(query), dialogue_dic)
                    if current_name not in dialogue_list:
                        dialogue_list.append(current_name)
                hd_options = history_dropdown.update(choices=dialogue_list, value=current_name)
                dialogue_dic[current_name] = main_agent.memory
                current_dialogue.append((query, answer))
                # 清空输出栏，聊天记录，及时更新对话名称
                return "", current_dialogue, hd_options

            @capture_output_and_error
            def history_to_current(name):
                global main_agent
                print(dialogue_dic, '\n\n')
                memory = dialogue_dic[name]
                main_agent = create_main_agent(memory=memory)
                current_dialogue = memory_to_list(memory)
                return (current_dialogue,)

            def clear_memory():
                global main_agent
                main_agent = create_main_agent()

            # 布局设置
            with gr.Column(scale=1):
                with gr.Row():
                    # 定义组件
                    dialogue_list = [name for name in dialogue_dic]
                    history_dropdown = gr.Dropdown(choices=dialogue_list, label="Select A Conversation")
                gr.Markdown('Terminal Output')
                terminal_output = gr.Textbox(placeholder='Standard Output:')
                terminal_error = gr.Textbox(placeholder='Standard Error:')

                # # 定义组件
                # chatbot = gr.Chatbot()
                # query_input = gr.Textbox(placeholder='input your query here: ')
                # clear = gr.ClearButton([query_input, chatbot, history_dropdown])

            with gr.Column(scale=2):
                # gr.Markdown('Terminal Output')
                # terminal_output = gr.Textbox(placeholder='Standard Output:')
                # terminal_error = gr.Textbox(placeholder='Standard Error:')
                # 定义组件
                chatbot = gr.Chatbot()
                query_input = gr.Textbox(placeholder='input your query here: ')
                clear = gr.ClearButton([query_input, chatbot, history_dropdown, terminal_output, terminal_error])

            # 组件点击绑定函数
            query_input.submit(ai_answer, [query_input, chatbot, history_dropdown],
                               [query_input, chatbot, history_dropdown, terminal_output, terminal_error])
            history_dropdown.select(history_to_current, history_dropdown, [chatbot, terminal_output, terminal_error])
            clear.click(clear_memory)
    demo.launch(share=True)
