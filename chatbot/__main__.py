from chatbot.speakeasy.app import App


def main():
    app = App()
    app.login()
    app.start_chat()


if __name__ == "__main__":
    main()
