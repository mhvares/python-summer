import tkinter
from threading import Thread

from client import ChatClient


class ChatClientGUI:
    def __init__(self, server_name, server_port):
        self.__engine = ChatClient(server_name, server_port)

        self.root = tkinter.Tk()
        self.root.title('Chat: %s' % str(self.__engine.get_name()))

        width = 400
        height = 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry("{width}x{height}+{x}+{y}".format(width=width,
                                                             height=height,
                                                             x=int((screen_width - width) / 2),
                                                             y=int((screen_height - height - 50) / 2)))

        label_frame_new_message_height = 50
        margin = 5
        self.text_messages = tkinter.Text(self.root)
        self.text_messages.config(state=tkinter.DISABLED)
        self.text_messages.place(width=-2 * margin,
                                 height=-3 * margin - label_frame_new_message_height,
                                 relwidth=1,
                                 relheight=1,
                                 x=margin,
                                 y=margin,
                                 relx=0,
                                 rely=0)

        label_frame_new_message = tkinter.LabelFrame(self.root, text='New Message')
        label_frame_new_message.place(width=-2 * margin,
                                      height=label_frame_new_message_height,
                                      x=margin,
                                      y=-label_frame_new_message_height - margin,
                                      relwidth=1,
                                      relheight=0,
                                      relx=0,
                                      rely=1)

        button_send_width = 37
        self.__button_send = tkinter.Button(label_frame_new_message,
                                            text='Send',
                                            command=self.__send_message)
        self.__button_send.place(x=-button_send_width - margin,
                                 y=0,
                                 relx=1)

        self.__entry_message = tkinter.Entry(label_frame_new_message)
        self.__entry_message.focus()
        self.__entry_message.bind('<Return>', lambda x: self.__send_message())
        self.__entry_message.place(width=-button_send_width - 3*margin,
                                   x=margin,
                                   y=margin,
                                   relwidth=1)

        receive_message_thread = Thread(target=self.__received_message)
        receive_message_thread.start()

        self.root.mainloop()

    def __received_message(self):
        while True:
            message = self.__engine.receive_message()
            print(message)
            if message is None:
                break
            self.text_messages.config(state=tkinter.NORMAL)
            self.text_messages.insert(tkinter.END, message.decode('utf-8') + '\n')
            self.text_messages.config(state=tkinter.DISABLED)

    def __send_message(self):
        print('send')
        message = self.__entry_message.get()
        self.__engine.send_message(message.encode('ascii'))
        self.__entry_message.delete(0, tkinter.END)

    def __close(self):
        self.root.quit()
        self.__engine.close()

if __name__ == '__main__':
    sn = 'localhost'
    sp = 31066
    ChatClientGUI(sn, sp)
