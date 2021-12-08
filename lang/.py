# -*- coding = utf-8 -*-
# encoding: utf-8
# @Time : 2021.7.28 00:51
# @Author : Synthesis 杜品赫
# @File : DatabaseDebug.py
# @Software : PyCharm
# https://github.com/SynthesisDu/SE_Trandict

# pip install pySide2
# from PySide2.QtGui import *
# from PySide2.QtWidgets import *
# from PySide2.QtCore import *
# from PySide2.QtWidgets import QApplication
# from PySide2.QtUiTools import QUiLoader
# from PySide2.QtCore import QFile
# from PySide2.QtGui import QPalette
# from PySide2 import QtGui
# from PySide2.QtOpenGL import QGLWidget
# from PySide2 import QtCore, QtWidgets, QtOpenGL

# pyinstaller -i icon.ico -w main.py

from PySide2.QtWidgets import QApplication
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
from PySide2 import QtCore
import sqlite3
import time as tm
# pyside2-rcc [.qrc] -o [.py]
import icon_Trandict


# Main window
class UiMain:
    def __init__(self, connect):
        self.connect = connect
        self.cur = self.connect.cursor()
        #####################################################################
        qfileStats = QFile(self.GetUI())
        qfileStats.open(QFile.ReadOnly)
        qfileStats.close()
        self.qMainWindow = QUiLoader().load(qfileStats)
        self.qMainWindow.setStyleSheet('color:black')

        #####################################################################
        # 文件(&F)
        # 文件(&F) > 导入(&I)
        self.qMainWindow.qqqF_I_W.triggered.connect(self.Action404)
        self.qMainWindow.qqqF_I_H.triggered.connect(self.Action404)
        self.qMainWindow.qqqF_I_N.triggered.connect(self.Action404)
        self.qMainWindow.qqqF_I_D.triggered.connect(self.Action404)
        # 文件(&F) > 导出(&E)
        self.qMainWindow.qqqF_E_W.triggered.connect(self.Action404)
        self.qMainWindow.qqqF_E_H.triggered.connect(self.Action404)
        self.qMainWindow.qqqF_E_N.triggered.connect(self.Action404)
        self.qMainWindow.qqqF_E_D.triggered.connect(self.Action404)
        # 文件(&F) > 退出(&Q)
        self.qMainWindow.qqqF_Q.triggered.connect(self.ActionFQ)
        # -------------------------------------------------------------------
        # 编辑(&E)
        # 编辑(&E) > 词性/词意(&A)
        self.qMainWindow.qqqE_A.triggered.connect(self.ActionEA)
        # -------------------------------------------------------------------
        # 查看(&V)
        # 查看(&V) > 历史(&H)
        self.qMainWindow.qqqV_H.triggered.connect(self.Action404)
        self.qMainWindow.qqqButtonHis.clicked.connect(self.Action404)
        # 查看(&V) > 统计图(&G)
        self.qMainWindow.qqqV_G.triggered.connect(self.Action404)
        self.qMainWindow.qqqButtonGra.clicked.connect(self.Action404)
        # -------------------------------------------------------------------
        # 窗口(&W)
        # 窗口(&W) > 主题(&T)
        self.qMainWindow.qqqW_T_O.triggered.connect(self.ActionWTO)
        self.qMainWindow.qqqW_O.triggered.connect(self.ActionWTO)
        self.qMainWindow.qqqW_T_D.triggered.connect(self.ActionWTD)
        self.qMainWindow.qqqW_D.triggered.connect(self.ActionWTD)
        self.qMainWindow.qqqW_T_C.triggered.connect(self.Action404)
        # 窗口(&W) > 语言(&L)
        # 帮助(&H) > 语言(&L)
        self.qMainWindow.qqqW_L_C.triggered.connect(self.ActionChinese)
        self.qMainWindow.qqqH_L_C.triggered.connect(self.ActionChinese)
        self.qMainWindow.qqqW_L_E.triggered.connect(self.ActionEnglish)
        self.qMainWindow.qqqH_L_E.triggered.connect(self.ActionEnglish)
        # -------------------------------------------------------------------
        # 帮助(&H)
        # 帮助(&H) > 关于(&A)
        self.qMainWindow.qqqH_A.triggered.connect(self.ActionHA)
        #####################################################################
        self.qMainWindow.qqqVocIn.textChanged.connect(self.VocIn)
        self.qMainWindow.qqqVocIn.returnPressed.connect(self.VocInR)
        self.qMainWindow.qqqCheckBoxStar.clicked.connect(lambda: self.BoxChangeStar(self.qMainWindow.qqqCheckBoxStar))
        self.qMainWindow.qqqCheckBoxDone.clicked.connect(lambda: self.BoxChangeDone(self.qMainWindow.qqqCheckBoxDone))
        #####################################################################
        # Star Done Vocab
        self.check = [0, 0, '']

    # 用于eng子类继承后覆写另外的ui文件
    def GetUI(self):
        return 'cn_Main.ui'

    def HistoryAdd(self, vocab, info):
        # sqlite查询 + 数据处理
        try:
            self.cur.execute("SELECT id FROM vocab WHERE vocab == '%s';" % vocab)
            inp = int(self.cur.fetchall()[0][0])
            vocab_id = inp
            time = str(tm.strftime("%Y-%m-%d %H:%M:%S", tm.localtime()))
            self.cur.execute("INSERT INTO history(time, vocab_id, info) VALUES ('%s', %d, '%s');" % (time, vocab_id, info))
            self.connect.commit()
            self.HistoryPrint(vocab)
        except Exception as e:
            pass

    def HistoryPrint(self, vocab):
        self.qMainWindow.qqqDate.clear()
        try:
            self.cur.execute("SELECT id FROM vocab WHERE vocab == '%s';" % vocab)
            inp = int(self.cur.fetchall()[0][0])
            vocab_id = inp
            self.cur.execute("SELECT time, info FROM history WHERE vocab_id == '%d';" % vocab_id)
            for i in self.cur.fetchall():
                self.qMainWindow.qqqDate.append(str(i).replace("('", '').replace("')", '').replace("', '", ' '))
        except Exception as e:
            print(e)

    def BoxPrint(self, vocab):
        # sqlite查询 + 数据处理
        try:
            self.cur.execute("SELECT star, done FROM vocab WHERE vocab == '%s';" % vocab)
            inp = str(self.cur.fetchall()[0])
            star = inp[:inp.find(',')]
            done = inp[inp.find(','):]
            self.check[2] = vocab
            if '0' in star or 'No' in star:
                self.qMainWindow.qqqCheckBoxStar.setChecked(False)
                self.check[0] = 0
            else:
                self.qMainWindow.qqqCheckBoxStar.setChecked(True)
                self.check[0] = 1
            if '0' in done or 'No' in done:
                self.qMainWindow.qqqCheckBoxDone.setChecked(False)
                self.check[1] = 0
            else:
                self.qMainWindow.qqqCheckBoxDone.setChecked(True)
                self.check[1] = 1
        except Exception:
            self.qMainWindow.qqqCheckBoxStar.setChecked(False)
            self.qMainWindow.qqqCheckBoxDone.setChecked(False)

    def BoxChangeStar(self, btn):
        vocab = str(self.qMainWindow.qqqVocIn.text())
        vocab = vocab.lower()
        checkBox = str(btn.checkState())
        check = 0
        if 'Checked' in checkBox:
            check = 1
            if self.check[0] != 1:
                self.HistoryAdd(vocab, 'Search & Star')
                self.check[0] = 1
        elif 'Unchecked' in checkBox:
            check = 0
            if self.check[0] != 0:
                self.HistoryAdd(vocab, 'Search & UnStar')
                self.check[0] = 0
        if vocab != '' and vocab is not None:
            try:
                self.cur.execute('UPDATE vocab SET star = %d WHERE vocab = "%s";' % (check, vocab))
                self.connect.commit()
            except Exception:
                pass
        self.HistoryPrint(vocab)

    def BoxChangeDone(self, btn):
        vocab = str(self.qMainWindow.qqqVocIn.text())
        vocab = vocab.lower()
        checkBox = str(btn.checkState())
        check = 0
        if 'Checked' in checkBox:
            check = 1
            if self.check[1] != 1:
                self.HistoryAdd(vocab, 'Search & Done')
                self.check[1] = 1
        elif 'Unchecked' in checkBox:
            check = 0
            if self.check[1] != 0:
                self.HistoryAdd(vocab, 'Search & UnDone')
                self.check[1] = 0
        if vocab != '' and vocab is not None:
            try:
                self.cur.execute('UPDATE vocab SET done = %d WHERE vocab = "%s";' % (check, vocab))
                self.connect.commit()
            except Exception:
                pass
        self.HistoryPrint(vocab)

    def Action404(self):
        cn_Undone.qMainWindow.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        cn_Undone.qMainWindow.show()

    def ActionChinese(self):
        pass

    def ActionEnglish(self):
        self.qMainWindow.close()
        eng_Main.qMainWindow.show()

    def ActionWTO(self):
        self.qMainWindow.setStyleSheet('color:black')
        cn_EA.qMainWindow.setStyleSheet('color:black')
        cn_About.qMainWindow.setStyleSheet('color:black')
        cn_Undone.qMainWindow.setStyleSheet('color:black')

    def ActionWTD(self):
        self.qMainWindow.setStyleSheet('background-color:rgba(130, 130, 130, 50); color:white')
        cn_EA.qMainWindow.setStyleSheet('background-color:rgba(130, 130, 130, 50); color:white')
        cn_About.qMainWindow.setStyleSheet('background-color:rgba(130, 130, 130, 50); color:white')
        cn_Undone.qMainWindow.setStyleSheet('background-color:rgba(130, 130, 130, 50); color:white')

    def ActionFQ(self):
        self.qMainWindow.close()

    def ActionEA(self):
        cn_EA.Load()
        cn_EA.qMainWindow.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        cn_EA.qMainWindow.show()

    def ActionHA(self):
        cn_About.qMainWindow.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        cn_About.qMainWindow.show()

    def VocIn(self):
        # 刷新
        self.qMainWindow.qqqVocList.clear()
        self.qMainWindow.qqqVocTitle.clear()
        self.qMainWindow.qqqVocCharacter.clear()
        self.qMainWindow.qqqVocWY.clear()
        self.qMainWindow.qqqDate.clear()
        # 新输入
        info = str(self.qMainWindow.qqqVocIn.text())
        self.qMainWindow.qqqVocTitle.append(info)
        # 备加载E_A编辑窗口
        cn_EA.qMainWindow.qqqVocab.clear()
        cn_EA.qMainWindow.qqqVocab.append(info)
        cn_EA.word = info
        # 一律小写
        info = info.lower()
        # 加载详情组件
        self.BoxPrint(info)
        self.HistoryPrint(info)
        if info != '':
            re = []
            self.cur.execute("SELECT vocab FROM vocab WHERE vocab LIKE '%s%%';" % info)
            re = re + self.cur.fetchall()
            reS = ''
            try:
                i = 0
                for reR in re:
                    reS += str(reR).replace('(', '').replace("'", '').replace(',', '').replace(')', '').replace(' ', '') + '\n'
                    if i > 20:
                        break
                    i += 1
            except Exception:
                reS = '<font color=red>没有匹配的单词</font>'
            self.qMainWindow.qqqVocList.append(reS)
        # sqlite查询 + 数据处理
        try:
            self.cur.execute("SELECT noun, pronoun, adjective, adverb, verb, intransitive_verb, transitive_verb, "
                             "auxiliary_verb, numeral, article, preposition, conjunction, interjection, abbreviation FROM vocab WHERE vocab == '%s';" % info)
            inp = str(self.cur.fetchall()[0])
            noun = inp[:inp.find(',')].replace("'", '').replace('(', '', 1).replace(',', '')
            inp = inp[inp.find(',') + 1:]
            pronoun = inp[1:inp.find(',')].replace("'", '').replace(',', '')
            inp = inp[inp.find(',') + 1:]
            adjective = inp[1:inp.find(',')].replace("'", '').replace(',', '')
            inp = inp[inp.find(',') + 1:]
            adverb = inp[1:inp.find(',')].replace("'", '').replace(',', '')
            inp = inp[inp.find(',') + 1:]
            verb = inp[1:inp.find(',')].replace("'", '').replace(',', '')
            inp = inp[inp.find(',') + 1:]
            intransitive_verb = inp[1:inp.find(',')].replace("'", '').replace(',', '')
            inp = inp[inp.find(',') + 1:]
            transitive_verb = inp[1:inp.find(',')].replace("'", '').replace(',', '')
            inp = inp[inp.find(',') + 1:]
            auxiliary_verb = inp[1:inp.find(',')].replace("'", '').replace(',', '')
            inp = inp[inp.find(',') + 1:]
            numeral = inp[1:inp.find(',')].replace("'", '').replace(',', '')
            inp = inp[inp.find(',') + 1:]
            article = inp[1:inp.find(',')].replace("'", '').replace(',', '')
            inp = inp[inp.find(',') + 1:]
            preposition = inp[1:inp.find(',')].replace("'", '').replace(',', '')
            inp = inp[inp.find(',') + 1:]
            conjunction = inp[1:inp.find(',')].replace("'", '').replace(',', '')
            inp = inp[inp.find(',') + 1:]
            interjection = inp[1:inp.find(',')].replace("'", '').replace(',', '')
            inp = inp[inp.find(',') + 1:]
            if inp.find(',') == -1:
                abbreviation = inp.replace("'", '').replace('(', '').replace(',', '').replace(')', '')
            else:
                abbreviation = inp[:inp.find(',')].replace("'", '').replace('(', '').replace(',', '').replace(')',
                                                                                                              '')
            re = ''
            if noun != '' and noun != 'None' and noun != ' ':
                re += 'n.' + noun + '\n'
            if pronoun != '' and pronoun != 'None' and pronoun != ' ':
                re += 'porn.' + pronoun + '\n'
            if adjective != '' and adjective != 'None' and adjective != ' ':
                re += 'adj.' + adjective + '\n'
            if adverb != '' and adverb != 'None' and adverb != ' ':
                re += 'adv.' + adverb + '\n'
            if verb != '' and verb != 'None' and verb != ' ':
                re += 'v.' + verb + '\n'
            if intransitive_verb != '' and intransitive_verb != 'None' and intransitive_verb != ' ':
                re += 'vi.' + intransitive_verb + '\n'
            if transitive_verb != '' and transitive_verb != 'None' and transitive_verb != ' ':
                re += 'vt.' + transitive_verb + '\n'
            if auxiliary_verb != '' and auxiliary_verb != 'None' and auxiliary_verb != ' ':
                re += 'aux.' + auxiliary_verb + '\n'
            if numeral != '' and numeral != 'None' and numeral != ' ':
                re += 'num.' + numeral + '\n'
            if article != '' and article != 'None' and article != ' ':
                re += 'art.' + article + '\n'
            if preposition != '' and preposition != 'None' and preposition != ' ':
                re += 'prep.' + preposition + '\n'
            if conjunction != '' and conjunction != 'None' and conjunction != ' ':
                re += 'conj.' + conjunction + '\n'
            if interjection != '' and interjection != 'None' and interjection != ' ':
                re += 'int.' + interjection + '\n'
            if abbreviation != '' and abbreviation != 'None' and abbreviation != ' ':
                re += 'abbr.' + abbreviation + '\n'
            self.qMainWindow.qqqVocCharacter.append(re)
            self.cur.execute("SELECT wyy_additional FROM vocab WHERE vocab == '%s';" % info)
            inp = str(self.cur.fetchall()[0]).replace('(', '', 1).replace(',)', '')[1:-1]
            if inp != '' and inp != 'on':
                self.qMainWindow.qqqVocWY.append(inp)
        except Exception:
            pass

    def VocInR(self):
        # 刷新
        self.qMainWindow.qqqVocTitle.clear()
        info = str(self.qMainWindow.qqqVocIn.text())
        self.qMainWindow.qqqVocTitle.append(info)
        self.HistoryAdd(info, 'Search & Return')

# &E&A window
class UiEA:
    def __init__(self, connect):
        self.connect = connect
        self.cur = self.connect.cursor()
        #####################################################################
        qfileStats = QFile('cn_EA.ui')
        qfileStats.open(QFile.ReadOnly)
        qfileStats.close()
        self.qMainWindow = QUiLoader().load(qfileStats)
        #####################################################################
        self.word = ''
        #####################################################################
        self.qMainWindow.qqqButtonC.clicked.connect(self.ButtonEA_C)
        self.qMainWindow.qqqButtonOK.clicked.connect(self.ButtonEA_OK)

    def Load(self):
        self.cur.execute("SELECT noun FROM vocab WHERE vocab = '%s';" % self.word)
        try:
            noun = str(self.cur.fetchall()).replace("[('", '').replace(",)]", '')[:-1]
            if noun == '[':
                noun = ''
            self.qMainWindow.qqqN.setText(noun)
        except Exception:
            pass
        self.cur.execute("SELECT pronoun FROM vocab WHERE vocab = '%s';" % self.word)
        try:
            pronoun = str(self.cur.fetchall()).replace("[('", '').replace(",)]", '')[:-1]
            if pronoun == '[':
                pronoun = ''
            self.qMainWindow.qqqPron.setText(pronoun)
        except Exception:
            pass
        self.cur.execute("SELECT adjective FROM vocab WHERE vocab = '%s';" % self.word)
        try:
            adjective = str(self.cur.fetchall()).replace("[('", '').replace(",)]", '')[:-1]
            if adjective == '[':
                adjective = ''
            self.qMainWindow.qqqAdj.setText(adjective)
        except Exception:
            pass
        self.cur.execute("SELECT adverb FROM vocab WHERE vocab = '%s';" % self.word)
        try:
            adverb = str(self.cur.fetchall()).replace("[('", '').replace(",)]", '')[:-1]
            if adverb == '[':
                adverb = ''
            self.qMainWindow.qqqAdv.setText(adverb)
        except Exception:
            pass
        self.cur.execute("SELECT verb FROM vocab WHERE vocab = '%s';" % self.word)
        try:
            verb = str(self.cur.fetchall()).replace("[('", '').replace(",)]", '')[:-1]
            if verb == '[':
                verb = ''
            self.qMainWindow.qqqV.setText(verb)
        except Exception:
            pass
        self.cur.execute("SELECT intransitive_verb FROM vocab WHERE vocab = '%s';" % self.word)
        try:
            intransitive_verb = str(self.cur.fetchall()).replace("[('", '').replace(",)]", '')[:-1]
            if intransitive_verb == '[':
                intransitive_verb = ''
            self.qMainWindow.qqqVi.setText(intransitive_verb)
        except Exception:
            pass
        self.cur.execute("SELECT transitive_verb FROM vocab WHERE vocab = '%s';" % self.word)
        try:
            transitive_verb = str(self.cur.fetchall()).replace("[('", '').replace(",)]", '')[:-1]
            if transitive_verb == '[':
                transitive_verb = ''
            self.qMainWindow.qqqVt.setText(transitive_verb)
        except Exception:
            pass
        self.cur.execute("SELECT auxiliary_verb FROM vocab WHERE vocab = '%s';" % self.word)
        try:
            auxiliary_verb = str(self.cur.fetchall()).replace("[('", '').replace(",)]", '')[:-1]
            if auxiliary_verb == '[':
                auxiliary_verb = ''
            self.qMainWindow.qqqAux.setText(auxiliary_verb)
        except Exception:
            pass
        self.cur.execute("SELECT numeral FROM vocab WHERE vocab = '%s';" % self.word)
        try:
            numeral = str(self.cur.fetchall()).replace("[('", '').replace(",)]", '')[:-1]
            if numeral == '[':
                numeral = ''
            self.qMainWindow.qqqNum.setText(numeral)
        except Exception:
            pass
        self.cur.execute("SELECT article FROM vocab WHERE vocab = '%s';" % self.word)
        try:
            article = str(self.cur.fetchall()).replace("[('", '').replace(",)]", '')[:-1]
            if article == '[':
                article = ''
            self.qMainWindow.qqqArt.setText(article)
        except Exception:
            pass
        self.cur.execute("SELECT preposition FROM vocab WHERE vocab = '%s';" % self.word)
        try:
            preposition = str(self.cur.fetchall()).replace("[('", '').replace(",)]", '')[:-1]
            if preposition == '[':
                preposition = ''
            self.qMainWindow.qqqPrep.setText(preposition)
        except Exception:
            pass
        self.cur.execute("SELECT conjunction FROM vocab WHERE vocab = '%s';" % self.word)
        try:
            conjunction = str(self.cur.fetchall()).replace("[('", '').replace(",)]", '')[:-1]
            if conjunction == '[':
                conjunction = ''
            self.qMainWindow.qqqConj.setText(conjunction)
        except Exception:
            pass
        self.cur.execute("SELECT interjection FROM vocab WHERE vocab = '%s';" % self.word)
        try:
            interjection = str(self.cur.fetchall()).replace("[('", '').replace(",)]", '')[:-1]
            if interjection == '[':
                interjection = ''
            self.qMainWindow.qqqInt.setText(interjection)
        except Exception:
            pass
        self.cur.execute("SELECT abbreviation FROM vocab WHERE vocab = '%s';" % self.word)
        try:
            abbreviation = str(self.cur.fetchall()).replace("[('", '').replace(",)]", '')[:-1]
            if abbreviation == '[':
                abbreviation = ''
            self.qMainWindow.qqqAbb.setText(abbreviation)
        except Exception:
            pass

    def ButtonEA_C(self):
        self.qMainWindow.close()

    def ButtonEA_OK(self):
        try:
            n = self.qMainWindow.qqqN.text()
            self.cur.execute('UPDATE vocab SET noun = "%s" WHERE vocab = "%s";' % (n, self.word))
            pron = self.qMainWindow.qqqPron.text()
            self.cur.execute('UPDATE vocab SET pronoun = "%s" WHERE vocab = "%s";' % (pron, self.word))
            adj = self.qMainWindow.qqqAdj.text()
            self.cur.execute('UPDATE vocab SET adjective = "%s" WHERE vocab = "%s";' % (adj, self.word))
            adv = self.qMainWindow.qqqAdv.text()
            self.cur.execute('UPDATE vocab SET adverb = "%s" WHERE vocab = "%s";' % (adv, self.word))
            v = self.qMainWindow.qqqV.text()
            self.cur.execute('UPDATE vocab SET verb = "%s" WHERE vocab = "%s";' % (v, self.word))
            vi = self.qMainWindow.qqqVi.text()
            self.cur.execute('UPDATE vocab SET intransitive_verb = "%s" WHERE vocab = "%s";' % (vi, self.word))
            vt = self.qMainWindow.qqqVt.text()
            self.cur.execute('UPDATE vocab SET transitive_verb = "%s" WHERE vocab = "%s";' % (vt, self.word))
            aux = self.qMainWindow.qqqAux.text()
            self.cur.execute('UPDATE vocab SET auxiliary_verb = "%s" WHERE vocab = "%s";' % (aux, self.word))
            num = self.qMainWindow.qqqNum.text()
            self.cur.execute('UPDATE vocab SET numeral = "%s" WHERE vocab = "%s";' % (num, self.word))
            art = self.qMainWindow.qqqArt.text()
            self.cur.execute('UPDATE vocab SET article = "%s" WHERE vocab = "%s";' % (art, self.word))
            prep = self.qMainWindow.qqqPrep.text()
            self.cur.execute('UPDATE vocab SET preposition = "%s" WHERE vocab = "%s";' % (prep, self.word))
            conj = self.qMainWindow.qqqConj.text()
            self.cur.execute('UPDATE vocab SET conjunction = "%s" WHERE vocab = "%s";' % (conj, self.word))
            intv = self.qMainWindow.qqqInt.text()
            self.cur.execute('UPDATE vocab SET interjection = "%s" WHERE vocab = "%s";' % (intv, self.word))
            abb = self.qMainWindow.qqqAbb.text()
            self.cur.execute('UPDATE vocab SET abbreviation = "%s" WHERE vocab = "%s";' % (abb, self.word))
            self.connect.commit()
        except Exception as e:
            pass
        cn_Main.qMainWindow.qqqVocCharacter.clear()
        cn_Main.qMainWindow.qqqVocTitle.clear()
        cn_Main.VocInR()
        self.qMainWindow.close()
        self.qMainWindow.qqqVocab.clear()

# &H&A window
class UiAbout:
    def __init__(self, connect):
        self.connect = connect
        self.cur = self.connect.cursor()
        #####################################################################
        qfileStats = QFile('cn_About.ui')
        qfileStats.open(QFile.ReadOnly)
        qfileStats.close()
        self.qMainWindow = QUiLoader().load(qfileStats)
        #####################################################################

# 404 window
class UiUndone:
    def __init__(self, connect):
        self.connect = connect
        self.cur = self.connect.cursor()
        #####################################################################
        qfileStats = QFile('cn_Undone.ui')
        qfileStats.open(QFile.ReadOnly)
        qfileStats.close()
        self.qMainWindow = QUiLoader().load(qfileStats)
        #####################################################################

class UiMainEng(UiMain):
    def GetUI(self):
        return 'eng_Main.ui'

    def ActionChinese(self):
        self.qMainWindow.close()
        cn_Main.qMainWindow.show()

    def ActionEnglish(self):
        pass

if __name__ == '__main__':
    icon_Trandict.check()
    con = sqlite3.connect('Database.db')
    app = QApplication([])
    cn_Main = UiMain(connect = con)
    cn_EA = UiEA(connect = con)
    cn_About = UiAbout(connect = con)
    cn_Undone = UiUndone(connect = con)
    eng_Main = UiMainEng(connect=con)
    cn_Main.qMainWindow.show()
    app.exec_()
    con.close()

# -*- coding = utf-8 -*-
# encoding: utf-8
# @Time : 2021.7.28 00:51
# @Author : Synthesis 杜品赫
# @File : DatabaseDebug.py
# @Software : PyCharm
# https://github.com/SynthesisDu/SE_Trandict

# pip install pySide2
# from PySide2.QtGui import *
# from PySide2.QtWidgets import *
# from PySide2.QtCore import *
# from PySide2.QtWidgets import QApplication
# from PySide2.QtUiTools import QUiLoader
# from PySide2.QtCore import QFile
# from PySide2.QtGui import QPalette
# from PySide2 import QtGui
# from PySide2.QtOpenGL import QGLWidget
# from PySide2 import QtCore, QtWidgets, QtOpenGL

# pyinstaller -i icon.ico -w main.py

from PySide2.QtWidgets import QApplication
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
from PySide2 import QtCore
import sqlite3
import time as tm
# pyside2-rcc [.qrc] -o [.py]
import icon_Trandict


# Main window
class UiMain:
    def __init__(self, connect):
        self.connect = connect
        self.cur = self.connect.cursor()
        #####################################################################
        qfileStats = QFile(self.GetUI())
        qfileStats.open(QFile.ReadOnly)
        qfileStats.close()
        self.qMainWindow = QUiLoader().load(qfileStats)
        self.qMainWindow.setStyleSheet('color:black')

        #####################################################################
        # 文件(&F)
        # 文件(&F) > 导入(&I)
        self.qMainWindow.qqqF_I_W.triggered.connect(self.Action404)
        self.qMainWindow.qqqF_I_H.triggered.connect(self.Action404)
        self.qMainWindow.qqqF_I_N.triggered.connect(self.Action404)
        self.qMainWindow.qqqF_I_D.triggered.connect(self.Action404)
        # 文件(&F) > 导出(&E)
        self.qMainWindow.qqqF_E_W.triggered.connect(self.Action404)
        self.qMainWindow.qqqF_E_H.triggered.connect(self.Action404)
        self.qMainWindow.qqqF_E_N.triggered.connect(self.Action404)
        self.qMainWindow.qqqF_E_D.triggered.connect(self.Action404)
        # 文件(&F) > 退出(&Q)
        self.qMainWindow.qqqF_Q.triggered.connect(self.ActionFQ)
        # -------------------------------------------------------------------
        # 编辑(&E)
        # 编辑(&E) > 词性/词意(&A)
        self.qMainWindow.qqqE_A.triggered.connect(self.ActionEA)
        # -------------------------------------------------------------------
        # 查看(&V)
        # 查看(&V) > 历史(&H)
        self.qMainWindow.qqqV_H.triggered.connect(self.Action404)
        self.qMainWindow.qqqButtonHis.clicked.connect(self.Action404)
        # 查看(&V) > 统计图(&G)
        self.qMainWindow.qqqV_G.triggered.connect(self.Action404)
        self.qMainWindow.qqqButtonGra.clicked.connect(self.Action404)
        # -------------------------------------------------------------------
        # 窗口(&W)
        # 窗口(&W) > 主题(&T)
        self.qMainWindow.qqqW_T_O.triggered.connect(self.ActionWTO)
        self.qMainWindow.qqqW_O.triggered.connect(self.ActionWTO)
        self.qMainWindow.qqqW_T_D.triggered.connect(self.ActionWTD)
        self.qMainWindow.qqqW_D.triggered.connect(self.ActionWTD)
        self.qMainWindow.qqqW_T_C.triggered.connect(self.Action404)
        # 窗口(&W) > 语言(&L)
        # 帮助(&H) > 语言(&L)
        self.qMainWindow.qqqW_L_C.triggered.connect(self.ActionChinese)
        self.qMainWindow.qqqH_L_C.triggered.connect(self.ActionChinese)
        self.qMainWindow.qqqW_L_E.triggered.connect(self.ActionEnglish)
        self.qMainWindow.qqqH_L_E.triggered.connect(self.ActionEnglish)
        # -------------------------------------------------------------------
        # 帮助(&H)
        # 帮助(&H) > 关于(&A)
        self.qMainWindow.qqqH_A.triggered.connect(self.ActionHA)
        #####################################################################
        self.qMainWindow.qqqVocIn.textChanged.connect(self.VocIn)
        self.qMainWindow.qqqVocIn.returnPressed.connect(self.VocInR)
        self.qMainWindow.qqqCheckBoxStar.clicked.connect(lambda: self.BoxChangeStar(self.qMainWindow.qqqCheckBoxStar))
        self.qMainWindow.qqqCheckBoxDone.clicked.connect(lambda: self.BoxChangeDone(self.qMainWindow.qqqCheckBoxDone))
        #####################################################################
        # Star Done Vocab
        self.check = [0, 0, '']

    # 用于eng子类继承后覆写另外的ui文件
    def GetUI(self):
        return 'cn_Main.ui'

    def HistoryAdd(self, vocab, info):
        # sqlite查询 + 数据处理
        try:
            self.cur.execute("SELECT id FROM vocab WHERE vocab == '%s';" % vocab)
            inp = int(self.cur.fetchall()[0][0])
            vocab_id = inp
            time = str(tm.strftime("%Y-%m-%d %H:%M:%S", tm.localtime()))
            self.cur.execute("INSERT INTO history(time, vocab_id, info) VALUES ('%s', %d, '%s');" % (time, vocab_id, info))
            self.connect.commit()
            self.HistoryPrint(vocab)
        except Exception as e:
            pass

    def HistoryPrint(self, vocab):
        self.qMainWindow.qqqDate.clear()
        try:
            self.cur.execute("SELECT id FROM vocab WHERE vocab == '%s';" % vocab)
            inp = int(self.cur.fetchall()[0][0])
            vocab_id = inp
            self.cur.execute("SELECT time, info FROM history WHERE vocab_id == '%d';" % vocab_id)
            for i in self.cur.fetchall():
                self.qMainWindow.qqqDate.append(str(i).replace("('", '').replace("')", '').replace("', '", ' '))
        except Exception as e:
            print(e)

    def BoxPrint(self, vocab):
        # sqlite查询 + 数据处理
        try:
            self.cur.execute("SELECT star, done FROM vocab WHERE vocab == '%s';" % vocab)
            inp = str(self.cur.fetchall()[0])
            star = inp[:inp.find(',')]
            done = inp[inp.find(','):]
            self.check[2] = vocab
            if '0' in star or 'No' in star:
                self.qMainWindow.qqqCheckBoxStar.setChecked(False)
                self.check[0] = 0
            else:
                self.qMainWindow.qqqCheckBoxStar.setChecked(True)
                self.check[0] = 1
            if '0' in done or 'No' in done:
                self.qMainWindow.qqqCheckBoxDone.setChecked(False)
                self.check[1] = 0
            else:
                self.qMainWindow.qqqCheckBoxDone.setChecked(True)
                self.check[1] = 1
        except Exception:
            self.qMainWindow.qqqCheckBoxStar.setChecked(False)
            self.qMainWindow.qqqCheckBoxDone.setChecked(False)

    def BoxChangeStar(self, btn):
        vocab = str(self.qMainWindow.qqqVocIn.text())
        vocab = vocab.lower()
        checkBox = str(btn.checkState())
        check = 0
        if 'Checked' in checkBox:
            check = 1
            if self.check[0] != 1:
                self.HistoryAdd(vocab, 'Search & Star')
                self.check[0] = 1
        elif 'Unchecked' in checkBox:
            check = 0
            if self.check[0] != 0:
                self.HistoryAdd(vocab, 'Search & UnStar')
                self.check[0] = 0
        if vocab != '' and vocab is not None:
            try:
                self.cur.execute('UPDATE vocab SET star = %d WHERE vocab = "%s";' % (check, vocab))
                self.connect.commit()
            except Exception:
                pass
        self.HistoryPrint(vocab)

    def BoxChangeDone(self, btn):
        vocab = str(self.qMainWindow.qqqVocIn.text())
        vocab = vocab.lower()
        checkBox = str(btn.checkState())
        check = 0
        if 'Checked' in checkBox:
            check = 1
            if self.check[1] != 1:
                self.HistoryAdd(vocab, 'Search & Done')
                self.check[1] = 1
        elif 'Unchecked' in checkBox:
            check = 0
            if self.check[1] != 0:
                self.HistoryAdd(vocab, 'Search & UnDone')
                self.check[1] = 0
        if vocab != '' and vocab is not None:
            try:
                self.cur.execute('UPDATE vocab SET done = %d WHERE vocab = "%s";' % (check, vocab))
                self.connect.commit()
            except Exception:
                pass
        self.HistoryPrint(vocab)

    def Action404(self):
        cn_Undone.qMainWindow.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        cn_Undone.qMainWindow.show()

    def ActionChinese(self):
        pass

    def ActionEnglish(self):
        self.qMainWindow.close()
        eng_Main.qMainWindow.show()

    def ActionWTO(self):
        self.qMainWindow.setStyleSheet('color:black')
        cn_EA.qMainWindow.setStyleSheet('color:black')
        cn_About.qMainWindow.setStyleSheet('color:black')
        cn_Undone.qMainWindow.setStyleSheet('color:black')

    def ActionWTD(self):
        self.qMainWindow.setStyleSheet('background-color:rgba(130, 130, 130, 50); color:white')
        cn_EA.qMainWindow.setStyleSheet('background-color:rgba(130, 130, 130, 50); color:white')
        cn_About.qMainWindow.setStyleSheet('background-color:rgba(130, 130, 130, 50); color:white')
        cn_Undone.qMainWindow.setStyleSheet('background-color:rgba(130, 130, 130, 50); color:white')

    def ActionFQ(self):
        self.qMainWindow.close()

    def ActionEA(self):
        cn_EA.Load()
        cn_EA.qMainWindow.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        cn_EA.qMainWindow.show()

    def ActionHA(self):
        cn_About.qMainWindow.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        cn_About.qMainWindow.show()

    def VocIn(self):
        # 刷新
        self.qMainWindow.qqqVocList.clear()
        self.qMainWindow.qqqVocTitle.clear()
        self.qMainWindow.qqqVocCharacter.clear()
        self.qMainWindow.qqqVocWY.clear()
        self.qMainWindow.qqqDate.clear()
        # 新输入
        info = str(self.qMainWindow.qqqVocIn.text())
        self.qMainWindow.qqqVocTitle.append(info)
        # 备加载E_A编辑窗口
        cn_EA.qMainWindow.qqqVocab.clear()
        cn_EA.qMainWindow.qqqVocab.append(info)
        cn_EA.word = info
        # 一律小写
        info = info.lower()
        # 加载详情组件
        self.BoxPrint(info)
        self.HistoryPrint(info)
        if info != '':
            re = []
            self.cur.execute("SELECT vocab FROM vocab WHERE vocab LIKE '%s%%';" % info)
            re = re + self.cur.fetchall()
            reS = ''
            try:
                i = 0
                for reR in re:
                    reS += str(reR).replace('(', '').replace("'", '').replace(',', '').replace(')', '').replace(' ', '') + '\n'
                    if i > 20:
                        break
                    i += 1
            except Exception:
                reS = '<font color=red>没有匹配的单词</font>'
            self.qMainWindow.qqqVocList.append(reS)
        # sqlite查询 + 数据处理
        try:
            self.cur.execute("SELECT noun, pronoun, adjective, adverb, verb, intransitive_verb, transitive_verb, "
                             "auxiliary_verb, numeral, article, preposition, conjunction, interjection, abbreviation FROM vocab WHERE vocab == '%s';" % info)
            inp = str(self.cur.fetchall()[0])
            noun = inp[:inp.find(',')].replace("'", '').replace('(', '', 1).replace(',', '')
            inp = inp[inp.find(',') + 1:]
            pronoun = inp[1:inp.find(',')].replace("'", '').replace(',', '')
            inp = inp[inp.find(',') + 1:]
            adjective = inp[1:inp.find(',')].replace("'", '').replace(',', '')
            inp = inp[inp.find(',') + 1:]
            adverb = inp[1:inp.find(',')].replace("'", '').replace(',', '')
            inp = inp[inp.find(',') + 1:]
            verb = inp[1:inp.find(',')].replace("'", '').replace(',', '')
            inp = inp[inp.find(',') + 1:]
            intransitive_verb = inp[1:inp.find(',')].replace("'", '').replace(',', '')
            inp = inp[inp.find(',') + 1:]
            transitive_verb = inp[1:inp.find(',')].replace("'", '').replace(',', '')
            inp = inp[inp.find(',') + 1:]
            auxiliary_verb = inp[1:inp.find(',')].replace("'", '').replace(',', '')
            inp = inp[inp.find(',') + 1:]
            numeral = inp[1:inp.find(',')].replace("'", '').replace(',', '')
            inp = inp[inp.find(',') + 1:]
            article = inp[1:inp.find(',')].replace("'", '').replace(',', '')
            inp = inp[inp.find(',') + 1:]
            preposition = inp[1:inp.find(',')].replace("'", '').replace(',', '')
            inp = inp[inp.find(',') + 1:]
            conjunction = inp[1:inp.find(',')].replace("'", '').replace(',', '')
            inp = inp[inp.find(',') + 1:]
            interjection = inp[1:inp.find(',')].replace("'", '').replace(',', '')
            inp = inp[inp.find(',') + 1:]
            if inp.find(',') == -1:
                abbreviation = inp.replace("'", '').replace('(', '').replace(',', '').replace(')', '')
            else:
                abbreviation = inp[:inp.find(',')].replace("'", '').replace('(', '').replace(',', '').replace(')',
                                                                                                              '')
            re = ''
            if noun != '' and noun != 'None' and noun != ' ':
                re += 'n.' + noun + '\n'
            if pronoun != '' and pronoun != 'None' and pronoun != ' ':
                re += 'porn.' + pronoun + '\n'
            if adjective != '' and adjective != 'None' and adjective != ' ':
                re += 'adj.' + adjective + '\n'
            if adverb != '' and adverb != 'None' and adverb != ' ':
                re += 'adv.' + adverb + '\n'
            if verb != '' and verb != 'None' and verb != ' ':
                re += 'v.' + verb + '\n'
            if intransitive_verb != '' and intransitive_verb != 'None' and intransitive_verb != ' ':
                re += 'vi.' + intransitive_verb + '\n'
            if transitive_verb != '' and transitive_verb != 'None' and transitive_verb != ' ':
                re += 'vt.' + transitive_verb + '\n'
            if auxiliary_verb != '' and auxiliary_verb != 'None' and auxiliary_verb != ' ':
                re += 'aux.' + auxiliary_verb + '\n'
            if numeral != '' and numeral != 'None' and numeral != ' ':
                re += 'num.' + numeral + '\n'
            if article != '' and article != 'None' and article != ' ':
                re += 'art.' + article + '\n'
            if preposition != '' and preposition != 'None' and preposition != ' ':
                re += 'prep.' + preposition + '\n'
            if conjunction != '' and conjunction != 'None' and conjunction != ' ':
                re += 'conj.' + conjunction + '\n'
            if interjection != '' and interjection != 'None' and interjection != ' ':
                re += 'int.' + interjection + '\n'
            if abbreviation != '' and abbreviation != 'None' and abbreviation != ' ':
                re += 'abbr.' + abbreviation + '\n'
            self.qMainWindow.qqqVocCharacter.append(re)
            self.cur.execute("SELECT wyy_additional FROM vocab WHERE vocab == '%s';" % info)
            inp = str(self.cur.fetchall()[0]).replace('(', '', 1).replace(',)', '')[1:-1]
            if inp != '' and inp != 'on':
                self.qMainWindow.qqqVocWY.append(inp)
        except Exception:
            pass

    def VocInR(self):
        # 刷新
        self.qMainWindow.qqqVocTitle.clear()
        info = str(self.qMainWindow.qqqVocIn.text())
        self.qMainWindow.qqqVocTitle.append(info)
        self.HistoryAdd(info, 'Search & Return')

# &E&A window
class UiEA:
    def __init__(self, connect):
        self.connect = connect
        self.cur = self.connect.cursor()
        #####################################################################
        qfileStats = QFile('cn_EA.ui')
        qfileStats.open(QFile.ReadOnly)
        qfileStats.close()
        self.qMainWindow = QUiLoader().load(qfileStats)
        #####################################################################
        self.word = ''
        #####################################################################
        self.qMainWindow.qqqButtonC.clicked.connect(self.ButtonEA_C)
        self.qMainWindow.qqqButtonOK.clicked.connect(self.ButtonEA_OK)

    def Load(self):
        self.cur.execute("SELECT noun FROM vocab WHERE vocab = '%s';" % self.word)
        try:
            noun = str(self.cur.fetchall()).replace("[('", '').replace(",)]", '')[:-1]
            if noun == '[':
                noun = ''
            self.qMainWindow.qqqN.setText(noun)
        except Exception:
            pass
        self.cur.execute("SELECT pronoun FROM vocab WHERE vocab = '%s';" % self.word)
        try:
            pronoun = str(self.cur.fetchall()).replace("[('", '').replace(",)]", '')[:-1]
            if pronoun == '[':
                pronoun = ''
            self.qMainWindow.qqqPron.setText(pronoun)
        except Exception:
            pass
        self.cur.execute("SELECT adjective FROM vocab WHERE vocab = '%s';" % self.word)
        try:
            adjective = str(self.cur.fetchall()).replace("[('", '').replace(",)]", '')[:-1]
            if adjective == '[':
                adjective = ''
            self.qMainWindow.qqqAdj.setText(adjective)
        except Exception:
            pass
        self.cur.execute("SELECT adverb FROM vocab WHERE vocab = '%s';" % self.word)
        try:
            adverb = str(self.cur.fetchall()).replace("[('", '').replace(",)]", '')[:-1]
            if adverb == '[':
                adverb = ''
            self.qMainWindow.qqqAdv.setText(adverb)
        except Exception:
            pass
        self.cur.execute("SELECT verb FROM vocab WHERE vocab = '%s';" % self.word)
        try:
            verb = str(self.cur.fetchall()).replace("[('", '').replace(",)]", '')[:-1]
            if verb == '[':
                verb = ''
            self.qMainWindow.qqqV.setText(verb)
        except Exception:
            pass
        self.cur.execute("SELECT intransitive_verb FROM vocab WHERE vocab = '%s';" % self.word)
        try:
            intransitive_verb = str(self.cur.fetchall()).replace("[('", '').replace(",)]", '')[:-1]
            if intransitive_verb == '[':
                intransitive_verb = ''
            self.qMainWindow.qqqVi.setText(intransitive_verb)
        except Exception:
            pass
        self.cur.execute("SELECT transitive_verb FROM vocab WHERE vocab = '%s';" % self.word)
        try:
            transitive_verb = str(self.cur.fetchall()).replace("[('", '').replace(",)]", '')[:-1]
            if transitive_verb == '[':
                transitive_verb = ''
            self.qMainWindow.qqqVt.setText(transitive_verb)
        except Exception:
            pass
        self.cur.execute("SELECT auxiliary_verb FROM vocab WHERE vocab = '%s';" % self.word)
        try:
            auxiliary_verb = str(self.cur.fetchall()).replace("[('", '').replace(",)]", '')[:-1]
            if auxiliary_verb == '[':
                auxiliary_verb = ''
            self.qMainWindow.qqqAux.setText(auxiliary_verb)
        except Exception:
            pass
        self.cur.execute("SELECT numeral FROM vocab WHERE vocab = '%s';" % self.word)
        try:
            numeral = str(self.cur.fetchall()).replace("[('", '').replace(",)]", '')[:-1]
            if numeral == '[':
                numeral = ''
            self.qMainWindow.qqqNum.setText(numeral)
        except Exception:
            pass
        self.cur.execute("SELECT article FROM vocab WHERE vocab = '%s';" % self.word)
        try:
            article = str(self.cur.fetchall()).replace("[('", '').replace(",)]", '')[:-1]
            if article == '[':
                article = ''
            self.qMainWindow.qqqArt.setText(article)
        except Exception:
            pass
        self.cur.execute("SELECT preposition FROM vocab WHERE vocab = '%s';" % self.word)
        try:
            preposition = str(self.cur.fetchall()).replace("[('", '').replace(",)]", '')[:-1]
            if preposition == '[':
                preposition = ''
            self.qMainWindow.qqqPrep.setText(preposition)
        except Exception:
            pass
        self.cur.execute("SELECT conjunction FROM vocab WHERE vocab = '%s';" % self.word)
        try:
            conjunction = str(self.cur.fetchall()).replace("[('", '').replace(",)]", '')[:-1]
            if conjunction == '[':
                conjunction = ''
            self.qMainWindow.qqqConj.setText(conjunction)
        except Exception:
            pass
        self.cur.execute("SELECT interjection FROM vocab WHERE vocab = '%s';" % self.word)
        try:
            interjection = str(self.cur.fetchall()).replace("[('", '').replace(",)]", '')[:-1]
            if interjection == '[':
                interjection = ''
            self.qMainWindow.qqqInt.setText(interjection)
        except Exception:
            pass
        self.cur.execute("SELECT abbreviation FROM vocab WHERE vocab = '%s';" % self.word)
        try:
            abbreviation = str(self.cur.fetchall()).replace("[('", '').replace(",)]", '')[:-1]
            if abbreviation == '[':
                abbreviation = ''
            self.qMainWindow.qqqAbb.setText(abbreviation)
        except Exception:
            pass

    def ButtonEA_C(self):
        self.qMainWindow.close()

    def ButtonEA_OK(self):
        try:
            n = self.qMainWindow.qqqN.text()
            self.cur.execute('UPDATE vocab SET noun = "%s" WHERE vocab = "%s";' % (n, self.word))
            pron = self.qMainWindow.qqqPron.text()
            self.cur.execute('UPDATE vocab SET pronoun = "%s" WHERE vocab = "%s";' % (pron, self.word))
            adj = self.qMainWindow.qqqAdj.text()
            self.cur.execute('UPDATE vocab SET adjective = "%s" WHERE vocab = "%s";' % (adj, self.word))
            adv = self.qMainWindow.qqqAdv.text()
            self.cur.execute('UPDATE vocab SET adverb = "%s" WHERE vocab = "%s";' % (adv, self.word))
            v = self.qMainWindow.qqqV.text()
            self.cur.execute('UPDATE vocab SET verb = "%s" WHERE vocab = "%s";' % (v, self.word))
            vi = self.qMainWindow.qqqVi.text()
            self.cur.execute('UPDATE vocab SET intransitive_verb = "%s" WHERE vocab = "%s";' % (vi, self.word))
            vt = self.qMainWindow.qqqVt.text()
            self.cur.execute('UPDATE vocab SET transitive_verb = "%s" WHERE vocab = "%s";' % (vt, self.word))
            aux = self.qMainWindow.qqqAux.text()
            self.cur.execute('UPDATE vocab SET auxiliary_verb = "%s" WHERE vocab = "%s";' % (aux, self.word))
            num = self.qMainWindow.qqqNum.text()
            self.cur.execute('UPDATE vocab SET numeral = "%s" WHERE vocab = "%s";' % (num, self.word))
            art = self.qMainWindow.qqqArt.text()
            self.cur.execute('UPDATE vocab SET article = "%s" WHERE vocab = "%s";' % (art, self.word))
            prep = self.qMainWindow.qqqPrep.text()
            self.cur.execute('UPDATE vocab SET preposition = "%s" WHERE vocab = "%s";' % (prep, self.word))
            conj = self.qMainWindow.qqqConj.text()
            self.cur.execute('UPDATE vocab SET conjunction = "%s" WHERE vocab = "%s";' % (conj, self.word))
            intv = self.qMainWindow.qqqInt.text()
            self.cur.execute('UPDATE vocab SET interjection = "%s" WHERE vocab = "%s";' % (intv, self.word))
            abb = self.qMainWindow.qqqAbb.text()
            self.cur.execute('UPDATE vocab SET abbreviation = "%s" WHERE vocab = "%s";' % (abb, self.word))
            self.connect.commit()
        except Exception as e:
            pass
        cn_Main.qMainWindow.qqqVocCharacter.clear()
        cn_Main.qMainWindow.qqqVocTitle.clear()
        cn_Main.VocInR()
        self.qMainWindow.close()
        self.qMainWindow.qqqVocab.clear()

# &H&A window
class UiAbout:
    def __init__(self, connect):
        self.connect = connect
        self.cur = self.connect.cursor()
        #####################################################################
        qfileStats = QFile('cn_About.ui')
        qfileStats.open(QFile.ReadOnly)
        qfileStats.close()
        self.qMainWindow = QUiLoader().load(qfileStats)
        #####################################################################

# 404 window
class UiUndone:
    def __init__(self, connect):
        self.connect = connect
        self.cur = self.connect.cursor()
        #####################################################################
        qfileStats = QFile('cn_Undone.ui')
        qfileStats.open(QFile.ReadOnly)
        qfileStats.close()
        self.qMainWindow = QUiLoader().load(qfileStats)
        #####################################################################

class UiMainEng(UiMain):
    def GetUI(self):
        return 'eng_Main.ui'

    def ActionChinese(self):
        self.qMainWindow.close()
        cn_Main.qMainWindow.show()

    def ActionEnglish(self):
        pass

if __name__ == '__main__':
    icon_Trandict.check()
    con = sqlite3.connect('Database.db')
    app = QApplication([])
    cn_Main = UiMain(connect = con)
    cn_EA = UiEA(connect = con)
    cn_About = UiAbout(connect = con)
    cn_Undone = UiUndone(connect = con)
    eng_Main = UiMainEng(connect=con)
    cn_Main.qMainWindow.show()
    app.exec_()
    con.close()

# -*- coding = utf-8 -*-
# encoding: utf-8
# @Time : 2021.7.28 00:51
# @Author : Synthesis 杜品赫
# @File : DatabaseDebug.py
# @Software : PyCharm
# https://github.com/SynthesisDu/SE_Trandict

# pip install pySide2
# from PySide2.QtGui import *
# from PySide2.QtWidgets import *
# from PySide2.QtCore import *
# from PySide2.QtWidgets import QApplication
# from PySide2.QtUiTools import QUiLoader
# from PySide2.QtCore import QFile
# from PySide2.QtGui import QPalette
# from PySide2 import QtGui
# from PySide2.QtOpenGL import QGLWidget
# from PySide2 import QtCore, QtWidgets, QtOpenGL

# pyinstaller -i icon.ico -w main.py

from PySide2.QtWidgets import QApplication
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
from PySide2 import QtCore
import sqlite3
import time as tm
# pyside2-rcc [.qrc] -o [.py]
import icon_Trandict


# Main window
class UiMain:
    def __init__(self, connect):
        self.connect = connect
        self.cur = self.connect.cursor()
        #####################################################################
        qfileStats = QFile(self.GetUI())
        qfileStats.open(QFile.ReadOnly)
        qfileStats.close()
        self.qMainWindow = QUiLoader().load(qfileStats)
        self.qMainWindow.setStyleSheet('color:black')

        #####################################################################
        # 文件(&F)
        # 文件(&F) > 导入(&I)
        self.qMainWindow.qqqF_I_W.triggered.connect(self.Action404)
        self.qMainWindow.qqqF_I_H.triggered.connect(self.Action404)
        self.qMainWindow.qqqF_I_N.triggered.connect(self.Action404)
        self.qMainWindow.qqqF_I_D.triggered.connect(self.Action404)
        # 文件(&F) > 导出(&E)
        self.qMainWindow.qqqF_E_W.triggered.connect(self.Action404)
        self.qMainWindow.qqqF_E_H.triggered.connect(self.Action404)
        self.qMainWindow.qqqF_E_N.triggered.connect(self.Action404)
        self.qMainWindow.qqqF_E_D.triggered.connect(self.Action404)
        # 文件(&F) > 退出(&Q)
        self.qMainWindow.qqqF_Q.triggered.connect(self.ActionFQ)
        # -------------------------------------------------------------------
        # 编辑(&E)
        # 编辑(&E) > 词性/词意(&A)
        self.qMainWindow.qqqE_A.triggered.connect(self.ActionEA)
        # -------------------------------------------------------------------
        # 查看(&V)
        # 查看(&V) > 历史(&H)
        self.qMainWindow.qqqV_H.triggered.connect(self.Action404)
        self.qMainWindow.qqqButtonHis.clicked.connect(self.Action404)
        # 查看(&V) > 统计图(&G)
        self.qMainWindow.qqqV_G.triggered.connect(self.Action404)
        self.qMainWindow.qqqButtonGra.clicked.connect(self.Action404)
        # -------------------------------------------------------------------
        # 窗口(&W)
        # 窗口(&W) > 主题(&T)
        self.qMainWindow.qqqW_T_O.triggered.connect(self.ActionWTO)
        self.qMainWindow.qqqW_O.triggered.connect(self.ActionWTO)
        self.qMainWindow.qqqW_T_D.triggered.connect(self.ActionWTD)
        self.qMainWindow.qqqW_D.triggered.connect(self.ActionWTD)
        self.qMainWindow.qqqW_T_C.triggered.connect(self.Action404)
        # 窗口(&W) > 语言(&L)
        # 帮助(&H) > 语言(&L)
        self.qMainWindow.qqqW_L_C.triggered.connect(self.ActionChinese)
        self.qMainWindow.qqqH_L_C.triggered.connect(self.ActionChinese)
        self.qMainWindow.qqqW_L_E.triggered.connect(self.ActionEnglish)
        self.qMainWindow.qqqH_L_E.triggered.connect(self.ActionEnglish)
        # -------------------------------------------------------------------
        # 帮助(&H)
        # 帮助(&H) > 关于(&A)
        self.qMainWindow.qqqH_A.triggered.connect(self.ActionHA)
        #####################################################################
        self.qMainWindow.qqqVocIn.textChanged.connect(self.VocIn)
        self.qMainWindow.qqqVocIn.returnPressed.connect(self.VocInR)
        self.qMainWindow.qqqCheckBoxStar.clicked.connect(lambda: self.BoxChangeStar(self.qMainWindow.qqqCheckBoxStar))
        self.qMainWindow.qqqCheckBoxDone.clicked.connect(lambda: self.BoxChangeDone(self.qMainWindow.qqqCheckBoxDone))
        #####################################################################
        # Star Done Vocab
        self.check = [0, 0, '']

    # 用于eng子类继承后覆写另外的ui文件
    def GetUI(self):
        return 'cn_Main.ui'

    def HistoryAdd(self, vocab, info):
        # sqlite查询 + 数据处理
        try:
            self.cur.execute("SELECT id FROM vocab WHERE vocab == '%s';" % vocab)
            inp = int(self.cur.fetchall()[0][0])
            vocab_id = inp
            time = str(tm.strftime("%Y-%m-%d %H:%M:%S", tm.localtime()))
            self.cur.execute("INSERT INTO history(time, vocab_id, info) VALUES ('%s', %d, '%s');" % (time, vocab_id, info))
            self.connect.commit()
            self.HistoryPrint(vocab)
        except Exception as e:
            pass

    def HistoryPrint(self, vocab):
        self.qMainWindow.qqqDate.clear()
        try:
            self.cur.execute("SELECT id FROM vocab WHERE vocab == '%s';" % vocab)
            inp = int(self.cur.fetchall()[0][0])
            vocab_id = inp
            self.cur.execute("SELECT time, info FROM history WHERE vocab_id == '%d';" % vocab_id)
            for i in self.cur.fetchall():
                self.qMainWindow.qqqDate.append(str(i).replace("('", '').replace("')", '').replace("', '", ' '))
        except Exception as e:
            print(e)

    def BoxPrint(self, vocab):
        # sqlite查询 + 数据处理
        try:
            self.cur.execute("SELECT star, done FROM vocab WHERE vocab == '%s';" % vocab)
            inp = str(self.cur.fetchall()[0])
            star = inp[:inp.find(',')]
            done = inp[inp.find(','):]
            self.check[2] = vocab
            if '0' in star or 'No' in star:
                self.qMainWindow.qqqCheckBoxStar.setChecked(False)
                self.check[0] = 0
            else:
                self.qMainWindow.qqqCheckBoxStar.setChecked(True)
                self.check[0] = 1
            if '0' in done or 'No' in done:
                self.qMainWindow.qqqCheckBoxDone.setChecked(False)
                self.check[1] = 0
            else:
                self.qMainWindow.qqqCheckBoxDone.setChecked(True)
                self.check[1] = 1
        except Exception:
            self.qMainWindow.qqqCheckBoxStar.setChecked(False)
            self.qMainWindow.qqqCheckBoxDone.setChecked(False)

    def BoxChangeStar(self, btn):
        vocab = str(self.qMainWindow.qqqVocIn.text())
        vocab = vocab.lower()
        checkBox = str(btn.checkState())
        check = 0
        if 'Checked' in checkBox:
            check = 1
            if self.check[0] != 1:
                self.HistoryAdd(vocab, 'Search & Star')
                self.check[0] = 1
        elif 'Unchecked' in checkBox:
            check = 0
            if self.check[0] != 0:
                self.HistoryAdd(vocab, 'Search & UnStar')
                self.check[0] = 0
        if vocab != '' and vocab is not None:
            try:
                self.cur.execute('UPDATE vocab SET star = %d WHERE vocab = "%s";' % (check, vocab))
                self.connect.commit()
            except Exception:
                pass
        self.HistoryPrint(vocab)

    def BoxChangeDone(self, btn):
        vocab = str(self.qMainWindow.qqqVocIn.text())
        vocab = vocab.lower()
        checkBox = str(btn.checkState())
        check = 0
        if 'Checked' in checkBox:
            check = 1
            if self.check[1] != 1:
                self.HistoryAdd(vocab, 'Search & Done')
                self.check[1] = 1
        elif 'Unchecked' in checkBox:
            check = 0
            if self.check[1] != 0:
                self.HistoryAdd(vocab, 'Search & UnDone')
                self.check[1] = 0
        if vocab != '' and vocab is not None:
            try:
                self.cur.execute('UPDATE vocab SET done = %d WHERE vocab = "%s";' % (check, vocab))
                self.connect.commit()
            except Exception:
                pass
        self.HistoryPrint(vocab)

    def Action404(self):
        cn_Undone.qMainWindow.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        cn_Undone.qMainWindow.show()

    def ActionChinese(self):
        pass

    def ActionEnglish(self):
        self.qMainWindow.close()
        eng_Main.qMainWindow.show()

    def ActionWTO(self):
        self.qMainWindow.setStyleSheet('color:black')
        cn_EA.qMainWindow.setStyleSheet('color:black')
        cn_About.qMainWindow.setStyleSheet('color:black')
        cn_Undone.qMainWindow.setStyleSheet('color:black')

    def ActionWTD(self):
        self.qMainWindow.setStyleSheet('background-color:rgba(130, 130, 130, 50); color:white')
        cn_EA.qMainWindow.setStyleSheet('background-color:rgba(130, 130, 130, 50); color:white')
        cn_About.qMainWindow.setStyleSheet('background-color:rgba(130, 130, 130, 50); color:white')
        cn_Undone.qMainWindow.setStyleSheet('background-color:rgba(130, 130, 130, 50); color:white')

    def ActionFQ(self):
        self.qMainWindow.close()

    def ActionEA(self):
        cn_EA.Load()
        cn_EA.qMainWindow.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        cn_EA.qMainWindow.show()

    def ActionHA(self):
        cn_About.qMainWindow.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        cn_About.qMainWindow.show()

    def VocIn(self):
        # 刷新
        self.qMainWindow.qqqVocList.clear()
        self.qMainWindow.qqqVocTitle.clear()
        self.qMainWindow.qqqVocCharacter.clear()
        self.qMainWindow.qqqVocWY.clear()
        self.qMainWindow.qqqDate.clear()
        # 新输入
        info = str(self.qMainWindow.qqqVocIn.text())
        self.qMainWindow.qqqVocTitle.append(info)
        # 备加载E_A编辑窗口
        cn_EA.qMainWindow.qqqVocab.clear()
        cn_EA.qMainWindow.qqqVocab.append(info)
        cn_EA.word = info
        # 一律小写
        info = info.lower()
        # 加载详情组件
        self.BoxPrint(info)
        self.HistoryPrint(info)
        if info != '':
            re = []
            self.cur.execute("SELECT vocab FROM vocab WHERE vocab LIKE '%s%%';" % info)
            re = re + self.cur.fetchall()
            reS = ''
            try:
                i = 0
                for reR in re:
                    reS += str(reR).replace('(', '').replace("'", '').replace(',', '').replace(')', '').replace(' ', '') + '\n'
                    if i > 20:
                        break
                    i += 1
            except Exception:
                reS = '<font color=red>没有匹配的单词</font>'
            self.qMainWindow.qqqVocList.append(reS)
        # sqlite查询 + 数据处理
        try:
            self.cur.execute("SELECT noun, pronoun, adjective, adverb, verb, intransitive_verb, transitive_verb, "
                             "auxiliary_verb, numeral, article, preposition, conjunction, interjection, abbreviation FROM vocab WHERE vocab == '%s';" % info)
            inp = str(self.cur.fetchall()[0])
            noun = inp[:inp.find(',')].replace("'", '').replace('(', '', 1).replace(',', '')
            inp = inp[inp.find(',') + 1:]
            pronoun = inp[1:inp.find(',')].replace("'", '').replace(',', '')
            inp = inp[inp.find(',') + 1:]
            adjective = inp[1:inp.find(',')].replace("'", '').replace(',', '')
            inp = inp[inp.find(',') + 1:]
            adverb = inp[1:inp.find(',')].replace("'", '').replace(',', '')
            inp = inp[inp.find(',') + 1:]
            verb = inp[1:inp.find(',')].replace("'", '').replace(',', '')
            inp = inp[inp.find(',') + 1:]
            intransitive_verb = inp[1:inp.find(',')].replace("'", '').replace(',', '')
            inp = inp[inp.find(',') + 1:]
            transitive_verb = inp[1:inp.find(',')].replace("'", '').replace(',', '')
            inp = inp[inp.find(',') + 1:]
            auxiliary_verb = inp[1:inp.find(',')].replace("'", '').replace(',', '')
            inp = inp[inp.find(',') + 1:]
            numeral = inp[1:inp.find(',')].replace("'", '').replace(',', '')
            inp = inp[inp.find(',') + 1:]
            article = inp[1:inp.find(',')].replace("'", '').replace(',', '')
            inp = inp[inp.find(',') + 1:]
            preposition = inp[1:inp.find(',')].replace("'", '').replace(',', '')
            inp = inp[inp.find(',') + 1:]
            conjunction = inp[1:inp.find(',')].replace("'", '').replace(',', '')
            inp = inp[inp.find(',') + 1:]
            interjection = inp[1:inp.find(',')].replace("'", '').replace(',', '')
            inp = inp[inp.find(',') + 1:]
            if inp.find(',') == -1:
                abbreviation = inp.replace("'", '').replace('(', '').replace(',', '').replace(')', '')
            else:
                abbreviation = inp[:inp.find(',')].replace("'", '').replace('(', '').replace(',', '').replace(')',
                                                                                                              '')
            re = ''
            if noun != '' and noun != 'None' and noun != ' ':
                re += 'n.' + noun + '\n'
            if pronoun != '' and pronoun != 'None' and pronoun != ' ':
                re += 'porn.' + pronoun + '\n'
            if adjective != '' and adjective != 'None' and adjective != ' ':
                re += 'adj.' + adjective + '\n'
            if adverb != '' and adverb != 'None' and adverb != ' ':
                re += 'adv.' + adverb + '\n'
            if verb != '' and verb != 'None' and verb != ' ':
                re += 'v.' + verb + '\n'
            if intransitive_verb != '' and intransitive_verb != 'None' and intransitive_verb != ' ':
                re += 'vi.' + intransitive_verb + '\n'
            if transitive_verb != '' and transitive_verb != 'None' and transitive_verb != ' ':
                re += 'vt.' + transitive_verb + '\n'
            if auxiliary_verb != '' and auxiliary_verb != 'None' and auxiliary_verb != ' ':
                re += 'aux.' + auxiliary_verb + '\n'
            if numeral != '' and numeral != 'None' and numeral != ' ':
                re += 'num.' + numeral + '\n'
            if article != '' and article != 'None' and article != ' ':
                re += 'art.' + article + '\n'
            if preposition != '' and preposition != 'None' and preposition != ' ':
                re += 'prep.' + preposition + '\n'
            if conjunction != '' and conjunction != 'None' and conjunction != ' ':
                re += 'conj.' + conjunction + '\n'
            if interjection != '' and interjection != 'None' and interjection != ' ':
                re += 'int.' + interjection + '\n'
            if abbreviation != '' and abbreviation != 'None' and abbreviation != ' ':
                re += 'abbr.' + abbreviation + '\n'
            self.qMainWindow.qqqVocCharacter.append(re)
            self.cur.execute("SELECT wyy_additional FROM vocab WHERE vocab == '%s';" % info)
            inp = str(self.cur.fetchall()[0]).replace('(', '', 1).replace(',)', '')[1:-1]
            if inp != '' and inp != 'on':
                self.qMainWindow.qqqVocWY.append(inp)
        except Exception:
            pass

    def VocInR(self):
        # 刷新
        self.qMainWindow.qqqVocTitle.clear()
        info = str(self.qMainWindow.qqqVocIn.text())
        self.qMainWindow.qqqVocTitle.append(info)
        self.HistoryAdd(info, 'Search & Return')

# &E&A window
class UiEA:
    def __init__(self, connect):
        self.connect = connect
        self.cur = self.connect.cursor()
        #####################################################################
        qfileStats = QFile('cn_EA.ui')
        qfileStats.open(QFile.ReadOnly)
        qfileStats.close()
        self.qMainWindow = QUiLoader().load(qfileStats)
        #####################################################################
        self.word = ''
        #####################################################################
        self.qMainWindow.qqqButtonC.clicked.connect(self.ButtonEA_C)
        self.qMainWindow.qqqButtonOK.clicked.connect(self.ButtonEA_OK)

    def Load(self):
        self.cur.execute("SELECT noun FROM vocab WHERE vocab = '%s';" % self.word)
        try:
            noun = str(self.cur.fetchall()).replace("[('", '').replace(",)]", '')[:-1]
            if noun == '[':
                noun = ''
            self.qMainWindow.qqqN.setText(noun)
        except Exception:
            pass
        self.cur.execute("SELECT pronoun FROM vocab WHERE vocab = '%s';" % self.word)
        try:
            pronoun = str(self.cur.fetchall()).replace("[('", '').replace(",)]", '')[:-1]
            if pronoun == '[':
                pronoun = ''
            self.qMainWindow.qqqPron.setText(pronoun)
        except Exception:
            pass
        self.cur.execute("SELECT adjective FROM vocab WHERE vocab = '%s';" % self.word)
        try:
            adjective = str(self.cur.fetchall()).replace("[('", '').replace(",)]", '')[:-1]
            if adjective == '[':
                adjective = ''
            self.qMainWindow.qqqAdj.setText(adjective)
        except Exception:
            pass
        self.cur.execute("SELECT adverb FROM vocab WHERE vocab = '%s';" % self.word)
        try:
            adverb = str(self.cur.fetchall()).replace("[('", '').replace(",)]", '')[:-1]
            if adverb == '[':
                adverb = ''
            self.qMainWindow.qqqAdv.setText(adverb)
        except Exception:
            pass
        self.cur.execute("SELECT verb FROM vocab WHERE vocab = '%s';" % self.word)
        try:
            verb = str(self.cur.fetchall()).replace("[('", '').replace(",)]", '')[:-1]
            if verb == '[':
                verb = ''
            self.qMainWindow.qqqV.setText(verb)
        except Exception:
            pass
        self.cur.execute("SELECT intransitive_verb FROM vocab WHERE vocab = '%s';" % self.word)
        try:
            intransitive_verb = str(self.cur.fetchall()).replace("[('", '').replace(",)]", '')[:-1]
            if intransitive_verb == '[':
                intransitive_verb = ''
            self.qMainWindow.qqqVi.setText(intransitive_verb)
        except Exception:
            pass
        self.cur.execute("SELECT transitive_verb FROM vocab WHERE vocab = '%s';" % self.word)
        try:
            transitive_verb = str(self.cur.fetchall()).replace("[('", '').replace(",)]", '')[:-1]
            if transitive_verb == '[':
                transitive_verb = ''
            self.qMainWindow.qqqVt.setText(transitive_verb)
        except Exception:
            pass
        self.cur.execute("SELECT auxiliary_verb FROM vocab WHERE vocab = '%s';" % self.word)
        try:
            auxiliary_verb = str(self.cur.fetchall()).replace("[('", '').replace(",)]", '')[:-1]
            if auxiliary_verb == '[':
                auxiliary_verb = ''
            self.qMainWindow.qqqAux.setText(auxiliary_verb)
        except Exception:
            pass
        self.cur.execute("SELECT numeral FROM vocab WHERE vocab = '%s';" % self.word)
        try:
            numeral = str(self.cur.fetchall()).replace("[('", '').replace(",)]", '')[:-1]
            if numeral == '[':
                numeral = ''
            self.qMainWindow.qqqNum.setText(numeral)
        except Exception:
            pass
        self.cur.execute("SELECT article FROM vocab WHERE vocab = '%s';" % self.word)
        try:
            article = str(self.cur.fetchall()).replace("[('", '').replace(",)]", '')[:-1]
            if article == '[':
                article = ''
            self.qMainWindow.qqqArt.setText(article)
        except Exception:
            pass
        self.cur.execute("SELECT preposition FROM vocab WHERE vocab = '%s';" % self.word)
        try:
            preposition = str(self.cur.fetchall()).replace("[('", '').replace(",)]", '')[:-1]
            if preposition == '[':
                preposition = ''
            self.qMainWindow.qqqPrep.setText(preposition)
        except Exception:
            pass
        self.cur.execute("SELECT conjunction FROM vocab WHERE vocab = '%s';" % self.word)
        try:
            conjunction = str(self.cur.fetchall()).replace("[('", '').replace(",)]", '')[:-1]
            if conjunction == '[':
                conjunction = ''
            self.qMainWindow.qqqConj.setText(conjunction)
        except Exception:
            pass
        self.cur.execute("SELECT interjection FROM vocab WHERE vocab = '%s';" % self.word)
        try:
            interjection = str(self.cur.fetchall()).replace("[('", '').replace(",)]", '')[:-1]
            if interjection == '[':
                interjection = ''
            self.qMainWindow.qqqInt.setText(interjection)
        except Exception:
            pass
        self.cur.execute("SELECT abbreviation FROM vocab WHERE vocab = '%s';" % self.word)
        try:
            abbreviation = str(self.cur.fetchall()).replace("[('", '').replace(",)]", '')[:-1]
            if abbreviation == '[':
                abbreviation = ''
            self.qMainWindow.qqqAbb.setText(abbreviation)
        except Exception:
            pass

    def ButtonEA_C(self):
        self.qMainWindow.close()

    def ButtonEA_OK(self):
        try:
            n = self.qMainWindow.qqqN.text()
            self.cur.execute('UPDATE vocab SET noun = "%s" WHERE vocab = "%s";' % (n, self.word))
            pron = self.qMainWindow.qqqPron.text()
            self.cur.execute('UPDATE vocab SET pronoun = "%s" WHERE vocab = "%s";' % (pron, self.word))
            adj = self.qMainWindow.qqqAdj.text()
            self.cur.execute('UPDATE vocab SET adjective = "%s" WHERE vocab = "%s";' % (adj, self.word))
            adv = self.qMainWindow.qqqAdv.text()
            self.cur.execute('UPDATE vocab SET adverb = "%s" WHERE vocab = "%s";' % (adv, self.word))
            v = self.qMainWindow.qqqV.text()
            self.cur.execute('UPDATE vocab SET verb = "%s" WHERE vocab = "%s";' % (v, self.word))
            vi = self.qMainWindow.qqqVi.text()
            self.cur.execute('UPDATE vocab SET intransitive_verb = "%s" WHERE vocab = "%s";' % (vi, self.word))
            vt = self.qMainWindow.qqqVt.text()
            self.cur.execute('UPDATE vocab SET transitive_verb = "%s" WHERE vocab = "%s";' % (vt, self.word))
            aux = self.qMainWindow.qqqAux.text()
            self.cur.execute('UPDATE vocab SET auxiliary_verb = "%s" WHERE vocab = "%s";' % (aux, self.word))
            num = self.qMainWindow.qqqNum.text()
            self.cur.execute('UPDATE vocab SET numeral = "%s" WHERE vocab = "%s";' % (num, self.word))
            art = self.qMainWindow.qqqArt.text()
            self.cur.execute('UPDATE vocab SET article = "%s" WHERE vocab = "%s";' % (art, self.word))
            prep = self.qMainWindow.qqqPrep.text()
            self.cur.execute('UPDATE vocab SET preposition = "%s" WHERE vocab = "%s";' % (prep, self.word))
            conj = self.qMainWindow.qqqConj.text()
            self.cur.execute('UPDATE vocab SET conjunction = "%s" WHERE vocab = "%s";' % (conj, self.word))
            intv = self.qMainWindow.qqqInt.text()
            self.cur.execute('UPDATE vocab SET interjection = "%s" WHERE vocab = "%s";' % (intv, self.word))
            abb = self.qMainWindow.qqqAbb.text()
            self.cur.execute('UPDATE vocab SET abbreviation = "%s" WHERE vocab = "%s";' % (abb, self.word))
            self.connect.commit()
        except Exception as e:
            pass
        cn_Main.qMainWindow.qqqVocCharacter.clear()
        cn_Main.qMainWindow.qqqVocTitle.clear()
        cn_Main.VocInR()
        self.qMainWindow.close()
        self.qMainWindow.qqqVocab.clear()

# &H&A window
class UiAbout:
    def __init__(self, connect):
        self.connect = connect
        self.cur = self.connect.cursor()
        #####################################################################
        qfileStats = QFile('cn_About.ui')
        qfileStats.open(QFile.ReadOnly)
        qfileStats.close()
        self.qMainWindow = QUiLoader().load(qfileStats)
        #####################################################################

# 404 window
class UiUndone:
    def __init__(self, connect):
        self.connect = connect
        self.cur = self.connect.cursor()
        #####################################################################
        qfileStats = QFile('cn_Undone.ui')
        qfileStats.open(QFile.ReadOnly)
        qfileStats.close()
        self.qMainWindow = QUiLoader().load(qfileStats)
        #####################################################################

class UiMainEng(UiMain):
    def GetUI(self):
        return 'eng_Main.ui'

    def ActionChinese(self):
        self.qMainWindow.close()
        cn_Main.qMainWindow.show()

    def ActionEnglish(self):
        pass

if __name__ == '__main__':
    icon_Trandict.check()
    con = sqlite3.connect('Database.db')
    app = QApplication([])
    cn_Main = UiMain(connect = con)
    cn_EA = UiEA(connect = con)
    cn_About = UiAbout(connect = con)
    cn_Undone = UiUndone(connect = con)
    eng_Main = UiMainEng(connect=con)
    cn_Main.qMainWindow.show()
    app.exec_()
    con.close()

