import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QScrollArea, QLabel, QTextEdit, QPushButton
from PyQt5.QtCore import QTimer, Qt, QSize, QRect, QDateTime
from PyQt5.QtGui import QKeySequence, QFont, QColor, QPainter, QBrush, QFontMetrics, QFontDatabase, QPen, QPixmap, QPainterPath
from audio import VoiceRecorder
from clova import return_text
from gpt_ import chat_with_gpt
from tts_AI import tts

recorder = VoiceRecorder('audio.wav')
prompt_national = """
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

prompt_personal = """
"생성형 AI가 만든 창작물의 저작권을 인정해야 하는가?"에 대한 토론을 위해 설계됨.

모든 응답은 대화체로 구성한다. (단, 항상 존중과 예의를 유지한다.)

응답의 형식은 한 문단으로 한정한다.

토론에서의 모든 응답은 6줄 이내로 구성한다.

토론의 모든 과정에 첫째, 둘째 등과 같은 서수적 표현은 절대 사용하지 않는다.

토론 순서를 고려하여 응답의 마지막에 다음 순서를 언급한다.

교차 조사는 상대방의 주장 중 궁금한 부분을 찾아 질문하는 과정임.

교차 조사 시 무조건 하나의 질문만 질문한다.

입론 및 반론에 대한 답변은 하지 않는다.

입론 및 반론을 할 경우, 사용자와 GPT의 주장과 근거가 겹치지 않도록 한다. 

논리적인 주장과 신뢰성 있는 근거 자료를 제시한다. 

토론의 순서는 아래와 같다. 

1_찬성 측 입론 - GPT가 찬성 측 입장에서 입론 제시
2_반대 측 교차 조사 - 사용자가 먼저 GPT에게 교차 조사, 교차 조사에 대한 답변 제시(교차 조사는 질문과 답변으로 구성되며, 교차 조사를 2번 반복한다.)
3_반대 측 입론 - 사용자가 반대 측 입장에서 입론 제시(GPT는 답변하지 않고 4번으로.)
4_찬성 측 교차 조사 - GPT가 먼저 사용자에게 교차 조사, 이어서 사용자가 답변 제시(교차 조사는 질문과 답변으로 구성되며, 교차 조사를 2번 반복한다.)
5_찬성 측 최종 반론 - GPT가 반대 측 입론에 대한 최종 반론 제시, 이어서 GPT의 발언을 요약하여 명령의 마지막 한 줄로 제시하면서 반론을 마무리
6_반대 측 최종 반론
7_"찬성 측과 반대 측의 입장을 상호 교체하겠습니다. 이제 사용자가 찬성 측 입장에서 주장을 제시할 차례입니다."이라고 말한 후, 8번 순서로 넘어간다.
8_찬성 측 입론 - 사용자가 찬성 측 입장에서 주장 제시
9_반대 측 교차 조사 - GPT가 먼저 사용자에게 교차 조사, 교차 조사에 대한 답변 제시(교차 조사는 질문과 답변으로 구성되며, 교차 조사를 2번 반복한다.)
10_반대 측 입론 - GPT가 반대 측 입장에서 주장 제시
11_찬성 측 교차 조사 - 사용자가 먼저 GPT에게 교차 조사, 교차 조사에 대한 답변 제시(교차 조사는 질문과 답변으로 구성되며, 교차 조사를 2번 반복한다.)
12_찬성 측 최종 반론 - 사용자가 반대 측 주장에 대한 반론을 제시할 것이니, 사용자의 답변을 기다리고 답변이 입력되면 12번으로. (반론에 대한 답변은 입력하지 않는다.)
13_반대 측 최종 반론 - GPT가 찬성 측 주장에 대한 반론을 제시한 뒤, GPT는 반대 측의 입장을 한 줄로 요약하여 제시하고, 마지막에 토론의 마무리를 정중하게 알린다.
"""

prompt_ = "끝말잇기를 할거야"

conversation_history = [
    {"role":"system", 'content':prompt_}]

class BubbleLabel(QLabel):
    def __init__(self, text, user=True, time=None, name=None, min_width=0, max_width=None, base_font_size=10, custom_font=None):
        super().__init__(text)
        self.user = user
        self.time = time or QDateTime.currentDateTime().toString("ap h:mm").replace("AM", "오전").replace("PM", "오후")
        self.name = name
        self.setWordWrap(True)
        self.min_width = min_width
        self.max_width = max_width
        self.base_font_size = base_font_size
        self.current_font_size = base_font_size
        self.custom_font = custom_font if custom_font else QFont()
        self.custom_font.setPointSize(self.current_font_size)
        self.setFont(self.custom_font)
        self.update_size(1.0)

    def update_size(self, scale):
        self.current_font_size = int(self.base_font_size * scale)
        self.custom_font.setPointSize(self.current_font_size)
        self.setFont(self.custom_font)

        horizontal_margin = int(5 * scale)
        vertical_margin = int(2.5 * scale)
        self.setContentsMargins(horizontal_margin, vertical_margin, horizontal_margin, vertical_margin)

        fm = QFontMetrics(self.font())
        max_width = self.max_width - (horizontal_margin * 1) if self.max_width else fm.maxWidth() * 20

        text_rect = fm.boundingRect(
            QRect(0, 0, max_width, 0), 
            Qt.TextWordWrap, 
            self.text()
        )

        ideal_width = min(max(text_rect.width() + (horizontal_margin * 2), int(self.min_width * scale)), self.max_width)
        ideal_height = text_rect.height() + (vertical_margin * 2)

        self.setFixedSize(ideal_width, ideal_height)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        rect = self.rect()
        
        # Draw bubble
        painter.setBrush(QBrush(QColor("#FEE500" if self.user else "#FFFFFF")))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect, 10, 10)
        
        # Draw text
        painter.setPen(Qt.black)
        painter.setFont(self.font())
        margins = self.contentsMargins()
        text_rect = rect.adjusted(margins.left(), margins.top(), -margins.right(), -margins.bottom())
        painter.drawText(text_rect, Qt.TextWordWrap, self.text())

class FourPanelApp(QWidget):
    def __init__(self):
        super().__init__()        
        self.is_recording = False
        self.base_width = 600
        self.base_height = 500
        self.scale = 3.0
        self.base_font_size = 10
        self.time_font_size = 5  # 시간 텍스트의 기본 폰트 크기
        self.date_font_size = 50  # 날짜 텍스트의 기본 폰트 크기
        self.name_font_size = 9  # 이름 텍스트의 기본 폰트 크기        
        self.initUI()


    def initUI(self):
        self.setWindowTitle('KaKaoTalk 스타일 채팅')
        self.setGeometry(100, 100, self.base_width, self.base_height)
        self.setStyleSheet("background-color: #B2C7D9;")
        
        font_id = QFontDatabase.addApplicationFont(r"C:\Users\dlwns\Desktop\Study\AI_GreatDebate\Pretendard-Black.ttf")
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            self.custom_font = QFont(font_family)
        else:
            print("Error: Failed to load custom font.")
            self.custom_font = QFont()

        self.custom_font.setPointSize(self.base_font_size)

        # 메인 레이아웃
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.date_label = QLabel("인공지능 대토론회🤖")
        self.date_label.setAlignment(Qt.AlignCenter)
        date_font = QFont(self.custom_font)
        date_font.setPointSize(self.date_font_size)
        date_font.setBold(True)
        self.date_label.setFont(date_font)
        self.date_label.setStyleSheet("color: #292A2D; margin: 10px 0;")
        self.layout.addWidget(self.date_label)

        self.chat_area = QScrollArea()
        self.chat_widget = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_widget)
        self.chat_layout.addStretch()
        self.chat_area.setWidget(self.chat_widget)
        self.chat_area.setWidgetResizable(True)
        self.layout.addWidget(self.chat_area)

        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setStyleSheet("border: none; border-radius: 15px; padding: 10px; background-color: white;")
        self.input_field.setFont(self.custom_font)
        input_layout.addWidget(self.input_field)

        self.send_button = QPushButton('전송')
        self.send_button.setStyleSheet("background-color: #fee500; border: none; border-radius: 15px; padding: 10px 20px;")
        self.send_button.setFont(self.custom_font)
        input_layout.addWidget(self.send_button)

        self.layout.addLayout(input_layout)
        
        self.color_timer = QTimer(self)
        self.color_timer.timeout.connect(self.reset_button_color)
        
        self.temp = 0
        
    def add_message(self, message, user=True, name=None, time=None):
        message_layout = QVBoxLayout()
        row_layout = QHBoxLayout()
        
        if not user:
            name_label = QLabel(name)
            name_label.setStyleSheet("color: #000000; background-color: transparent;")
            name_font = QFont(self.custom_font)
            name_font.setPointSize(int(self.name_font_size * self.scale))
            name_label.setFont(name_font)
            message_layout.addWidget(name_label)

        max_bubble_width = int(self.width() * 0.75)  # 화면 너비의 75%
        bubble = BubbleLabel(message, user, time=time, name=name, custom_font=self.custom_font, base_font_size=self.base_font_size, max_width=max_bubble_width)
        bubble.update_size(self.scale)
        
        time_label = QLabel(bubble.time)
        time_label.setStyleSheet("color: #8C8C8C; background-color: transparent;")
        time_font = QFont(self.custom_font)
        time_font.setPointSize(int(self.time_font_size * self.scale))
        time_label.setFont(time_font)
        time_label.setAlignment(Qt.AlignBottom)
        
        if user:
            row_layout.addStretch()
            row_layout.addWidget(time_label)
            row_layout.addWidget(bubble)
        else:
            row_layout.addWidget(bubble)
            row_layout.addWidget(time_label)
            row_layout.addStretch()
    
        message_layout.addLayout(row_layout)
        self.chat_layout.insertLayout(self.chat_layout.count() - 1, message_layout)
        QApplication.processEvents()
        self.scroll_to_bottom()

    def scroll_to_bottom(self):
        QTimer.singleShot(50, lambda: self.chat_area.verticalScrollBar().setValue(
            self.chat_area.verticalScrollBar().maximum()
        ))

    def update_date_label(self):
        date_font = QFont(self.custom_font)
        date_font.setPointSize(int(self.date_font_size * self.scale))
        date_font.setBold(True)
        self.date_label.setFont(date_font)

    def update_all_bubbles(self):
        max_bubble_width = int(self.width() * 0.75)  # 화면 너비의 75%
        for i in range(self.chat_layout.count() - 1):
            item = self.chat_layout.itemAt(i)
            if isinstance(item, QVBoxLayout):
                message_layout = item
                for j in range(message_layout.count()):
                    widget = message_layout.itemAt(j).widget()
                    if isinstance(widget, QLabel) and not isinstance(widget, BubbleLabel):
                        # This is likely the name label
                        name_font = QFont(self.custom_font)
                        name_font.setPointSize(int(self.name_font_size * self.scale))
                        widget.setFont(name_font)
                    elif isinstance(widget, QHBoxLayout):
                        row_layout = widget
                        for k in range(row_layout.count()):
                            widget = row_layout.itemAt(k).widget()
                            if isinstance(widget, BubbleLabel):
                                widget.max_width = max_bubble_width
                                widget.update_size(self.scale)
                            elif isinstance(widget, QLabel) and widget.text().startswith("오"):
                                time_font = QFont(self.custom_font)
                                time_font.setPointSize(int(self.time_font_size * self.scale))
                                widget.setFont(time_font)
        self.chat_widget.adjustSize()
        self.chat_area.setWidgetResizable(True)
        self.scroll_to_bottom()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_all_bubbles()
        
    def toggle_recording(self):
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        self.is_recording = True
        recorder.start_recording()
        self.send_button.setStyleSheet("background-color: green")
        self.color_timer.start(100)  # 1초 후 노란색으로 변경

    def stop_recording(self):
        global conversation_history
        self.is_recording = False
        recorder.stop_recording()
        self.send_button.setStyleSheet("background-color: red")
        self.color_timer.start(100)  # 1초 후 기본 색상으로 리셋

        rescode, response_json = return_text('audio.wav')
        if rescode == 200 and response_json is not None:
            user_say = response_json.get("text", "No text found")
            gpt_say, conversation_history = chat_with_gpt(user_say, conversation_history)
            self.add_message(user_say)
            self.add_message(gpt_say, False, name='GPT')
            self.temp += 1
            print(self.temp)
            tts(gpt_say, file_name="test{}.wav".format(self.temp))

        else:
            self.add_message("Error occurred during speech recognition")
            tts("Error occurred during speech recognition")

    def reset_button_color(self):
        if self.is_recording:
            self.send_button.setStyleSheet("background-color: yellow")  # 녹음 중일 때 노란색으로 변경
        else:
            self.send_button.setStyleSheet("")  # 녹음 중이 아닐 때 기본 스타일로 리셋
        self.color_timer.stop()
    
    def toggleFullScreen(self):
        if self.isFullScreen:
            self.showNormal()
        else:
            self.showFullScreen()
        self.isFullScreen = not self.isFullScreen
        self.update_all_bubbles()  # 화면 크기 변경에 따른 업데이트

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            self.toggle_recording()
        elif event.key() == Qt.Key_F11:
            self.toggleFullScreen()
        else:
            super().keyPressEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FourPanelApp()
    ex.show()
    sys.exit(app.exec_())