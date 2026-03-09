class Logging:
    def __init__(self, theme="default", text_color="white", log_text_color="black"):
        self.reset = "\x1b[0m"
        
        self.red = None
        self.blue = None
        self.green = None
        self.white = None
        self.black = None
        self.orange = None
        self.yellow = None
        self.magenta = None
        self.light_pink = "\x1b[38;2;255;182;193m"
        self.light_pink_bg = "\x1b[48;2;255;182;193m"
        self.theme = str(theme).lower()
        
        self.load_color_scheme()
        
        self.textcolor = (
            "\x1b[30m" if text_color.lower() == "black" else
            "\x1b[37m" if text_color.lower() == "white" else
            text_color
        )
        self.log_text_color = (
            self.black if log_text_color.lower() == "black" else
            self.white if log_text_color.lower() == "white" else
            log_text_color
        )
    
    def load_color_scheme(self):
        if self.theme == "default":
            self.red = "\x1b[41m"
            self.blue = "\x1b[44m"
            self.green = "\x1b[42m"
            self.white = "\x1b[37m"
            self.black = "\x1b[30m"
            self.orange = None
            self.yellow = "\x1b[43m"
            self.magenta = "\x1b[45m"
            
        elif self.theme in ["catppuccin", "catppuccin-mocha"]:
            self.red = "\x1b[48;2;243;139;168m"
            self.blue = "\x1b[48;2;137;180;250m"
            self.green = "\x1b[48;2;166;227;161m"
            self.white = "\x1b[38;2;205;214;244m"
            self.black = "\x1b[38;2;17;17;27m"
            self.orange = "\x1b[48;2;250;179;135m"
            self.yellow = "\x1b[48;2;249;226;175m"
            self.magenta = "\x1b[48;2;203;166;247m"
            
        else:
            self.theme = "default"
            self.load_color_scheme()
            self.info("Theme not supported yet! Switch to default theme.")
    
    def logger(self, text1: str, text: str) -> None:
        text1 = str(text1)
        text = str(text)
        print(f"{self.light_pink_bg}{self.black} {text1} {self.reset} {self.textcolor}{text}{self.reset}")
    
    def success(self, text: str) -> None:
        text = str(text)
        print(f"{self.green}{self.log_text_color}LOADDER COMMANDS {self.reset}{self.textcolor}{text}")

    def error(self, text: str) -> None:
        text = str(text)
        print(f"{self.red}{self.log_text_color}ERROR {self.reset}{self.textcolor}{text}")

    def prefixcmd(self, text: str) -> None:
        text = str(text)
        print(f"{self.green}{self.log_text_color}PREFIX COMMANDS BOT {self.reset}{self.textcolor}{text}")
    
    def warning(self, text: str) -> None:
        text = str(text)
        print(f"{self.orange or self.yellow}{self.log_text_color}WARN {self.reset}{self.textcolor}{text}")

    def restart(self, text: str) -> None:
        text = str(text)
        print(f"{self.green}{self.log_text_color}RESTART BOT {self.reset}{self.textcolor}{text}")

    def info(self, text: str) -> None:
        text = str(text)
        print(f"{self.blue}{self.log_text_color}DEBUG {self.reset}{self.textcolor}{text}")
