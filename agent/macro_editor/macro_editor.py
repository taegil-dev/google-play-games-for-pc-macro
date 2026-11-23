import json
from os import name
import sys
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, QAbstractItemView, QComboBox, QFileDialog, QHBoxLayout,
    QInputDialog, QLabel, QListWidget, QListWidgetItem, QMainWindow,
    QMessageBox, QPushButton, QSplitter, QTabWidget, QVBoxLayout, QWidget,
)
from PySide6.QtGui import QShortcut, QKeySequence

import ef2.pos as p

BASE_DIR = Path(__file__).resolve().parent


def read_json(name):
    path = BASE_DIR / name
    with path.open('r', encoding='utf-8') as f:
        return json.load(f)


def write_json(name, data):
    path = BASE_DIR / name
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    tmp.replace(path)


class Editor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('매크로 에디터')
        self.resize(1600, 900)
        self.color = Qt.black

        # 파일 로드
        self.data = read_json('data.json')
        self.positions = read_json('positions.json')
        self.delays = read_json('delays.json')
        self.changed = False

        # 루트
        root = QWidget()
        # vertical layout
        layout = QVBoxLayout(root)
        # 화면 생성
        self.init_screen(root, layout)

        # horizontal layout
        bottom = QHBoxLayout()
        self.status = QLabel('기존 JSON 데이터를 불러왔습니다.')
        bottom.addWidget(self.status, 1)
        save_btn = QPushButton('JSON 저장 (Ctrl+S)')
        save_btn.clicked.connect(self.save)
        bottom.addWidget(save_btn)
        layout.addLayout(bottom)
        QShortcut(QKeySequence.Save, self, activated=self.save)
        self.refresh_data("sequences")
        self.refresh_data("macros")

    def init_screen(self, root: QWidget, layout: QVBoxLayout):
        # 상단 탭
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        self.setCentralWidget(root)
        
        self.multi_macro_tab = QWidget()
        self.macro_tab = QWidget()
        self.sequence_tab = QWidget()
        self.tabs.addTab(self.multi_macro_tab, '다중 매크로 편집')
        self.tabs.addTab(self.macro_tab, '매크로 편집')
        self.tabs.addTab(self.sequence_tab, '시퀀스 편집')

        # 내부 레이아웃
        multi_macro_layout = QHBoxLayout(self.multi_macro_tab)
        macro_layout = QHBoxLayout(self.macro_tab)
        sequence_layout = QHBoxLayout(self.sequence_tab)

        # 목록 생성
        self.data_list: dict[str, QListWidget] = {"multi_macros": None, "macros": None, "sequences": None}
        self.draw_data_list(multi_macro_layout, "다중 매크로", "multi_macros")
        self.draw_data_list(macro_layout, "매크로", "macros")
        self.draw_data_list(sequence_layout, "시퀀스", "sequences")
        # 실행 순서 표시
        self.data_steps: dict[str, QListWidget] = {"multi_macros": None, "macros": None, "sequences": None}
        self.draw_data_steps(multi_macro_layout, "다중 매크로", "multi_macros")
        self.draw_data_steps(macro_layout, "매크로", "macros")
        self.draw_data_steps(sequence_layout, "시퀀스", "sequences")
        # 동작 목록 표시
        self.draw_base_list(macro_layout, "macros")
        self.draw_base_list(sequence_layout, "sequences")



    def draw_data_list(self, layout, label, type):
        # 왼쪽 컨테이너
        left = QVBoxLayout()
        left.addWidget(QLabel(f'{label} 목록'))

        # 데이터 목록
        self.data_list[type] = QListWidget()
        self.data_list[type].currentTextChanged.connect(lambda name: self.show_data(name, type))
        left.addWidget(self.data_list[type])

        # 하단 버튼
        bottom_row = QHBoxLayout()
        self.button('추가', lambda: self.add_data(label, type), bottom_row)
        self.button('이름 변경', lambda: self.rename_data(label, type), bottom_row)
        self.button('삭제', lambda: self.delete_data(label, type), bottom_row)
        left.addLayout(bottom_row)

        # 왼쪽 컨테이너 추가
        layout.addLayout(left, 2)


    def add_data(self, label, type):
        name, ok = QInputDialog.getText(self, f'새 {label}', f'{label} 이름:')
        name = name.strip()
        if not ok or not name:
            return
        
        if name in self.data[type]:
            QMessageBox.warning(self, '중복', f'이미 존재하는 {label}입니다.')
            return
        
        self.data[type][name] = []
        self.mark()
        self.refresh_data(type, select=name)


    def rename_data(self, label, type):
        old = self.selected_data(type)
        if not old: 
            return
        
        name, ok = QInputDialog.getText(self, '이름 변경', '새 이름:', text=old)
        name = name.strip()
        if not ok or not name or name == old: 
            return
        
        if name in self.data[type]:
            QMessageBox.warning(self, '중복', f'이미 존재하는 {label}입니다.')
            return
        
        self.data[type] = {(name if name == old else value) : value for name, value in self.data[type].items()}
        if type == "sequences":
            for blocks in self.data["macros"].values():
                for block in blocks:
                    if block['sequence'] == old: block['sequence'] = name

        self.mark()
        self.refresh_data(type, select=name)

        # 매크로에 들어가는 시퀀스 이름 새로고침
        if type == "sequences":
            self.refresh_data("macros")


    def delete_data(self, label, type):
        name = self.selected_data(type)
        if not name: 
            return

        if type == "sequences":
            used = [k for k, blocks in self.data["macros"].items() if any(b['sequence'] == name for b in blocks)]
            if used:
                QMessageBox.warning(self, '삭제 불가', '다음 매크로에서 사용 중입니다: ' + ', '.join(used))
                return
        
        if QMessageBox.question(self, '삭제', f'"{name}" {label}를 삭제할까요?') != QMessageBox.Yes: 
            return
        
        del self.data[type][name]

        self.mark()
        self.refresh_data(type)


    def refresh_data(self, type, select = None):
        current = select or self.data_list[type].currentItem() and self.data_list[type].currentItem().text()

        self.data_list[type].blockSignals(True)
        self.data_list[type].clear()
        self.data_list[type].addItems(list(self.data[type]))
        self.data_list[type].blockSignals(False)

        if current in self.data[type]:
            self.data_list[type].setCurrentRow(list(self.data[type]).index(current))
        elif self.data[type]:
            self.data_list[type].setCurrentRow(0)
        else:
            self.data_steps[type].clear()

        if type == "sequences":
            self.refresh_available_sequences()



    def refresh_available_sequences(self):
        self.available_sequences.clear()
        self.available_sequences.addItems(list(self.data["sequences"]))


    # 시퀀스 선택 시 해당 시퀀스 순서 표시
    def show_data(self, name, type):
        self.data_steps[type].clear()
        if type == "macros":
            for block in self.data[type].get(name, []):
                self.data_steps[type].addItem(f"{block['name']}  →  {block['sequence']}")
        elif type == "sequences":
            for step in self.data[type].get(name, []):
                if step['type'] == 'custom_delay':
                    label = f"딜레이 {step['seconds']}초"
                else:
                    label = f"{step['type'].upper()}  |  {step['name']}"
                self.data_steps[type].addItem(label)


    def draw_data_steps(self, layout, label, type):
        # 중앙 컨테이너
        center = QVBoxLayout()
        center.addWidget(QLabel(f'선택한 {label}의 실행 순서'))
        # 순서 목록
        self.data_steps[type] = QListWidget()
        if type == "sequences":
            self.data_steps[type].setSelectionMode(QAbstractItemView.SingleSelection)

        center.addWidget(self.data_steps[type])

        # 하단 버튼
        bottom_row = QHBoxLayout()
        self.button('↑ 위로', lambda: self.move_step(-1, type), bottom_row)
        self.button('↓ 아래로', lambda: self.move_step(1, type), bottom_row)
        self.button('제거', lambda: self.remove_step(type), bottom_row)
        center.addLayout(bottom_row)

        # 중앙 컨테이너 추가
        layout.addLayout(center, 3)


    def move_step(self, delta, type):
        # 현재 선택한 작업 찾기
        name = self.selected_data(type)
        if not name:
            return
        
        current_step = self.data_steps[type].currentRow()
        result_step = current_step + delta
        # 예외 처리
        if current_step < 0 or result_step < 0 or result_step >= len(self.data[type][name]): 
            return

        # 스왑
        steps = self.data[type][name]
        steps[current_step], steps[result_step] = steps[result_step], steps[current_step]
        
        self.mark()
        self.show_data(name, type)
        self.data_steps[type].setCurrentRow(result_step)


    def remove_step(self, type):
        # 현재 선택한 작업 찾기
        name = self.selected_data(type)

        current_step = self.data_steps[type].currentRow()
        if not name or current_step < 0: 
            return
        
        del self.data[type][name][current_step]

        self.mark()
        self.show_data(name, type)
        self.data_steps[type].setCurrentRow(min(current_step, self.data_steps[type].count() - 1))


    def selected_data(self, type):
        item = self.data_list[type].currentItem()
        return item.text() if item else None


    def draw_base_list(self, layout, type):
        # 오른쪽 컨테이너
        right = QVBoxLayout()
        if type == "sequences":
            right.addWidget(QLabel('미리 정의된 동작'))
        elif type == "macros":
            right.addWidget(QLabel('사용할 시퀀스'))

        if type == "sequences":
            # 동작 종류 선택 박스
            self.action_kind = QComboBox()
            self.action_kind.addItems(['POS', 'DELAY'])
            self.action_kind.currentIndexChanged.connect(self.refresh_actions)
            right.addWidget(self.action_kind)

            # 동작 검색
            self.action_filter = QComboBox()
            self.action_filter.setEditable(True)
            self.action_filter.setInsertPolicy(QComboBox.NoInsert)
            self.action_filter.lineEdit().setPlaceholderText('목록에서 선택하거나 검색')
            right.addWidget(self.action_filter)

            # 동작 리스트
            self.action_list = QListWidget()
            self.action_list.itemDoubleClicked.connect(lambda _: self.add_step(type))
            right.addWidget(self.action_list)

            self.action_filter.lineEdit().textEdited.connect(self.filter_actions)
            self.refresh_actions()
        elif type == "macros":
            # 사용할 시퀀스 목록
            self.available_sequences = QListWidget()
            self.available_sequences.itemDoubleClicked.connect(lambda _: self.add_step(type))
            right.addWidget(self.available_sequences)

        self.button('선택한 동작 추가 →', lambda: self.add_step(type), right)
        layout.addLayout(right, 2)


    def add_step(self, type):
        name = self.selected_data(type)
        if type == "sequences":
            item = self.action_list.currentItem()
        elif type == "macros":
            item = self.available_sequences.currentItem()

        if not name or not item: 
            return

        if type == "sequences":
            kind = 'pos' if self.action_kind.currentText() == 'POS' else 'delay'
        elif type == "macros":
            kind = item.text()
        index = self.data_steps[type].currentRow()
        at = index + 1 if index >= 0 else len(self.data[type][name])
        if type == "sequences":
            self.data[type][name].insert(at, {'type': kind, 'name': item.text()})
        elif type == "macros":
            self.data[type][name].insert(at, {'name': kind, 'sequence': kind})

        self.mark()
        self.show_data(name, type)
        self.data_steps[type].setCurrentRow(at)


    # 동작 검색
    def filter_actions(self, query):
        for i in range(self.action_list.count()):
            item = self.action_list.item(i)
            item.setHidden(query.casefold() not in item.text().casefold())


    def refresh_actions(self):
        self.action_filter.blockSignals(True)
        self.action_filter.clear()
        self.action_filter.blockSignals(False)
        self.action_list.clear()
        values = self.positions if self.action_kind.currentText() == 'POS' else self.delays
        self.action_list.addItems(list(values))



    def button(self, text, callback, parent_layout):
        b = QPushButton(text)
        b.clicked.connect(callback)
        parent_layout.addWidget(b)
        return b
    

    def mark(self):
        self.changed = True
        self.status.setText('저장되지 않은 변경사항이 있습니다.')
        self.setWindowTitle('Macro Sequence Editor *')


    def save(self):
        try:
            write_json('data.json', self.data)
        except Exception as e:
            QMessageBox.critical(self, '저장 실패', str(e))
            return
        self.changed = False
        self.setWindowTitle('Macro Sequence Editor')
        self.status.setText('data.json 저장 완료')

    def closeEvent(self, event):
        if self.changed:
            answer = QMessageBox.question(self, '저장되지 않은 변경사항', '변경사항을 저장할까요?', QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel, QMessageBox.Save)
            if answer == QMessageBox.Cancel:
                event.ignore(); return
            if answer == QMessageBox.Save:
                self.save()
                if self.changed:
                    event.ignore(); return
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet("""
        QWidget {
            background-color: #18181b;
            color: #e4e4e7;
            font-size: 13px;
        }

        QMainWindow, QDialog {
            background-color: #18181b;
        }

        QTreeWidget, QListWidget, QTableWidget {
            background-color: #27272a;
            color: #e4e4e7;
            border: 1px solid #3f3f46;
            border-radius: 6px;
            outline: none;
        }

        QTreeWidget::item, QListWidget::item {
            padding: 6px;
        }

        QTreeWidget::item:selected,
        QListWidget::item:selected,
        QTableWidget::item:selected {
            background-color: #3b4260;
            color: #ffffff;
        }

        QPushButton {
            background-color: #3f3f46;
            color: #f4f4f5;
            border: 1px solid #52525b;
            border-radius: 6px;
            padding: 7px 12px;
        }

        QPushButton:hover {
            background-color: #52525b;
        }

        QPushButton:pressed {
            background-color: #6366f1;
        }

        QPushButton:disabled {
            background-color: #27272a;
            color: #71717a;
        }

        QLineEdit, QSpinBox, QDoubleSpinBox,
        QComboBox, QTextEdit {
            background-color: #27272a;
            color: #f4f4f5;
            border: 1px solid #52525b;
            border-radius: 5px;
            padding: 5px;
            selection-background-color: #4f46e5;
        }

        QLineEdit:focus, QSpinBox:focus,
        QDoubleSpinBox:focus, QComboBox:focus {
            border: 1px solid #818cf8;
        }

        QComboBox QAbstractItemView {
            background-color: #27272a;
            color: #f4f4f5;
            selection-background-color: #3b4260;
        }

        QTabWidget::pane {
            border: 1px solid #3f3f46;
            background-color: #18181b;
        }

        QTabBar::tab {
            background-color: #27272a;
            color: #a1a1aa;
            padding: 9px 18px;
            border: 1px solid #3f3f46;
        }

        QTabBar::tab:selected {
            background-color: #3f3f46;
            color: #ffffff;
        }

        QHeaderView::section {
            background-color: #27272a;
            color: #e4e4e7;
            padding: 6px;
            border: 1px solid #3f3f46;
        }

        QMenuBar, QMenu {
            background-color: #27272a;
            color: #e4e4e7;
        }

        QMenu::item:selected {
            background-color: #3f3f46;
        }

        QScrollBar:vertical {
            background-color: #18181b;
            width: 10px;
        }

        QScrollBar::handle:vertical {
            background-color: #52525b;
            border-radius: 5px;
            min-height: 20px;
        }

        QScrollBar::add-line, QScrollBar::sub-line {
            height: 0px;
            width: 0px;
        }

        QSplitter::handle {
            background-color: #3f3f46;
        }
    """)

    window = Editor()
    window.show()
    sys.exit(app.exec())
