from cmath import pi
from typing import Iterable
import argparse
from bs4 import BeautifulSoup
import sys
import json
import requests
import jieba
import jieba.posseg as pseg
from tqdm import tqdm
from pathlib import Path
from options import WebscrapperAnkiOptions
import utils

class YoudaoTranslate:
    known_words = []
    deck_name = "中文"
    model_name = "Chinese (Basic)"
    waiting_for_review = []
    file = None

    def __to_data__(self,hanzi,translation, pinyin, examples, ex_tr):
        return { "Hanzi": hanzi ,
                        "Examples":"<hr />".join(examples),
                        "Color": hanzi,
                        "Pinyin": pinyin,
                        "English": "<hr / >".join(translation),
                        "ExamplesTrans": "<hr / >".join(ex_tr),
                        "Sound": "",
                    }


    def __init__(self ) -> None:
        # self.n = n
        # self.depth = depth
        # self.bar = tqdm(total=self.n)
        self.f = Path("../../known_words.txt")
        if self.f.is_file():
            self.known_words = self.__read_from_fs__()
            # print(self.known_words)
        pass

    def run(self,argv,add_examples_words):
        if argv[0] in self.known_words:
            return
        self.known_words.append(argv[0])

        args = self.translate(argv)
        data = utils.add_note(self.deck_name,self.model_name,self.__to_data__(*args ) )

        if data != None:
            self.waiting_for_review.append(data)


        if add_examples_words:
            for e in args[-2]:
                words = pseg.cut(e, use_paddle=True)
                for word, flag in words:
                    if (
                        flag != "r"
                        and flag != "q"
                        and flag != "ul"
                        and flag != "x"
                        and flag != "uj"
                        and flag != "d"
                        and flag != "ud"
                        and word  != argv[0]
                        and word not in self.known_words
                    ):
                        argse = self.translate([word])
                        if argse[0] == None:
                            continue
                        self.known_words.append(word)
                        # data = utils.can_send_anki(han,trans,pin,ex,tr_ex)
                        data = utils.add_note(self.deck_name,self.model_name,self.__to_data__(*argse))
                        if data != None:
                            self.waiting_for_review.append(data)

        already_known = self.__read_from_fs__()
        self.__write_to_fs__([w for w in self.known_words if w not in already_known])
        self.known_words = self.__read_from_fs__()




        # if len(self.waiting_for_review) == self.n :
        # print(self.waiting_for_review)

        # for_send = []
        # for data in self.waiting_for_review:
        #     print(data["params"]["notes"][0]["fields"])
        #     inp = input("want this ? Y/N ")
        #     if inp == "Y" or inp == "y":
        #         for_send.append(data)
        # self.waiting_for_review = []
        # if len(for_send) > 0:
        #     for_send[0]["params"]["notes"] = [data["params"]["notes"][0] for data in for_send]
        #     self.add_to_anki(for_send[0])

    def translate(self, argv):
        try:
            hex_q = (
                repr(argv[0].encode("utf-8"))[2:-1]
                .replace("\\", "%")
                .replace("x", "")
                .upper()
            )
            url = f"https://www.youdao.com/result?word={hex_q}&lang=en"
            result = requests.get(url, timeout=10)
            a = BeautifulSoup(result.content, "html5lib")
            # print(a)
            b = [
                div.get_text()
                for div in a.find_all("div")
                if len(div.find_all("b")) > 0 and len(div.find_all("div")) == 0
            ]
            pinyin = [
                div.get_text() for div in a.find_all("span", {"class": "phonetic"})
            ][0]
            translation = [
                div.get_text() for div in a.find_all("div", {"class": "trans-ce"})
            ]
            examples_tran = [
                div.get_text() for div in a.find_all("div", {"class": "sen-ch"})
            ]
            # print(examples_tran)
            examples = []
            pinyin = pinyin.split("/")[1]
            for i in range(len(b)):
                c = b[i]
                if len(c.split("\xa0")) == 1 and len(argv[0]) > 1:
                    examples.append(c)

            if len(translation) > 1:
                translation = translation[:2]
            return (argv[0], translation, pinyin, examples,examples_tran)
        except Exception as e:
            print(e)
            return (None,None,None,None,None)

    def add_to_anki(self, datas):
            results = requests.post("http://127.0.0.1:8765", data=json.dumps(datas))
            print(results.content)


    def __write_to_fs__(self, batch_known:Iterable[str]):
        # print(batch_known)
        self.file = open(self.f, "a")
        for a in [f",${word}," for word in batch_known]:
            self.file.write(a)
        self.file.close()

    def __read_from_fs__(self) -> Iterable[str]:
        self.file = open(self.f, "r")
        self.file.seek(0)
        a = [w[1:] for w in self.file.readlines()[0].split(",")]
        self.file.close()
        return a


if __name__ == "__main__":
    opts = WebscrapperAnkiOptions().parse()
    words = None
    if opts.inline is not None:
        words = opts.inline
    if opts.file is not None:
        f = open(opts.file,'r')
        words = [l[:-1] for l in f.readlines() ]
        f.close()
        # print(words)
    for word in words:
        try:
            YoudaoTranslate().run([word],opts.examples_words)
        except Exception as e:
            print(e)
            pass
