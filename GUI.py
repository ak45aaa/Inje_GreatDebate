import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton
from audio import VoiceRecorder
from clova import return_text
from gpt_ import chat_with_gpt

recorder = VoiceRecorder('audio.wav')
prompt = """
    챗봇은 목표는 경쟁적인 토론이 아니다. 하나의 아이디어로 수렴하는 방향의 토의를 진행하는 것이다. (어휘에서는 "토론"대신 "토의"를 사용한다.)

    강조할 것은 미래지향적인 주제를 만드는 것이다. 공학적 토의 주제여야 한다. 피할 것은 민감한 주제이다. 고등학교에서 사용될 주제이므로 주의하도록 한다.

    해결 방안을 제시하지 마라. 해결 방안의 평가만 해라.

    이 지침을 바탕으로 대화 대상인 학생이 하나의 아이디어로 수렴할 수 있도록 돕는 것이 챗봇의 주요 역할이다.

    토의에서 주어진 주제에 대해 대한 해결방안을 입력하면, 그 해결방안에 대해 상세한 평가를 말하여라. 상세한 평가에는 실현 가능성, 미래 지향성, 장점, 단점 등 여러가지 평가가 포함하되, 맹목적으로 따를 필요는 없으며, 대화 주제에 대해 유동적으로 챗봇만의 생각이나, 평가 기준을 구축해도 된다.


    챗봇은 고등학생 친구끼리 대화하는 것처럼 친근하지만, 공식적인 자리에서 말하는 형식을 차려야한다.
    무조건 대화체이며, 무조건 경어체, 반말을 사용한다. (안녕하세요? (X), 안녕? (O)) 항상 세 문장 이하로 대답한다. 
    출력은 단락을 콜론이나 번호 순서를 나열하는 방식 대신에, 줄글 및 한 문단으로 작성해서 사람과 대화하는 것과 같이 출력한다. 출력은 항상 3줄 이하로 하고, 이해가 쉽게 고등학생 수준의 어휘로 출력하여라. 모든 상황에서 예시를 들 경우, 세 개 이하의 예시를 사용한다

    결론을 요청할 경우, 지금까지 대화했던 주제들에 대해 요약, 정리, 평가를 해라.

    대화는 고등학생 친구끼리 대화하는 것처럼 친근하지만, 공식적인 자리에서 말하는 형식을 차려야 합니다. 
    또한 응답은 무조건 대화체고, 무조건 경어체를 사용합니다. 단락을 콜론이나 번호 순서를 나열하는 방식 대신에, 줄글로 쭉 작성해서 사람과 대화하는 것처럼 작성하세요. 출력은 항상 3줄로 하고, 이해가 쉽게 고등학생 수준의 어휘로 출력하세요.

    "소재 화학 연구에서 AI 활용의 난관은 무엇인가에 대해 이야기하자"라는 질문을 받는다면 반드시 "소재 화학 연구에서 AI 활용의 난관은 무엇인가를 주제로 토의를 해보자는 거지? 소재 화학 연구에서 AI 활용의 난관은 무엇인가에 관한 주제를 기반으로 소재 화학 연구를 하는 과정에서 나타날 수 있는 여러 가지 문제점들에 대해 다루어보자." 라고만 대답해야 한다."""

conversation_history = [
    {"role":"system", 'content':prompt}]

class FourPanelApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('4분할 애플리케이션')
        self.setGeometry(100, 100, 600, 400)

        # 메인 레이아웃
        main_layout = QVBoxLayout()

        # 상단 레이아웃 (텍스트 출력창 2개)
        top_layout = QHBoxLayout()
        self.text_edit1 = QTextEdit()
        self.text_edit2 = QTextEdit()
        self.text_edit1.setReadOnly(True)
        self.text_edit2.setReadOnly(True)
        top_layout.addWidget(self.text_edit1)
        top_layout.addWidget(self.text_edit2)

        # 하단 레이아웃 (버튼 2개)
        bottom_layout = QHBoxLayout()
        self.button1 = QPushButton('녹음 시작')
        self.button2 = QPushButton('녹음 끝')
        bottom_layout.addWidget(self.button1)
        bottom_layout.addWidget(self.button2)

        # 메인 레이아웃에 상단과 하단 레이아웃 추가
        main_layout.addLayout(top_layout)
        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)

        # 버튼 클릭 이벤트 연결
        self.button1.clicked.connect(self.button1_clicked)
        self.button2.clicked.connect(self.button2_clicked)

    def button1_clicked(self):
        recorder.start_recording()

    def button2_clicked(self):
        global conversation_history
        recorder.stop_recording()
        rescode, response_json = return_text('audio.wav')
        if rescode == 200 and response_json is not None:
            user_say = response_json.get("text", "No text found")
            gpt_say, conversation_history = chat_with_gpt(user_say, conversation_history)
            self.text_edit1.append(user_say)
            self.text_edit2.append(gpt_say)
        else:
            self.text_edit2.append("Error occurred during speech recognition")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FourPanelApp()
    ex.show()
    sys.exit(app.exec_())