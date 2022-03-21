from typing import Iterable
from bs4 import BeautifulSoup
import sys
import json
import requests
import jieba
import jieba.posseg as pseg
from tqdm import tqdm
from pathlib import Path


class YoudaoTranslate:
    known_words = []
    waiting_for_review = []
    file = None

    def __init__(self, n) -> None:
        self.n = n
        self.bar = tqdm(total=self.n)
        self.f = Path("../known_words.txt")
        if self.f.is_file():
            self.known_words = self.__read_from_fs__()
        pass

    def translate(self, argv):
        try:
            if argv[0] not in self.known_words:
                self.known_words.append(argv[0])
            else:
                return
            hex_q = (
                repr(argv[0].encode("utf-8"))[2:-1]
                .replace("\\", "%")
                .replace("x", "")
                .upper()
            )
            url = f"https://www.youdao.com/result?word={hex_q}&lang=en"
            # print(argv[0])
            result = requests.get(url, timeout=10)
            a = BeautifulSoup(result.content, "html5lib")
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
            examples = []
            pinyin = pinyin.split("/")[1]
            for i in range(len(b)):
                c = b[i]
                if len(c.split("\xa0")) == 1 and len(argv[0]) > 1:
                    examples.append(c)

                # else:
                #     if len(c.split("\xa0")) > 1:
                #         c = c.split("\xa0")[1]
                #         c = c.split(
                #             [char for char in c if char > "\u4e00" and char < "\u9fff"][0]
                #         )[0]
                #     if len(translation) == 0:
                #         translation.append(c)

            if len(translation) > 1:
                translation = translation[:2]
            # if argv[0] not in self.known_words:
            self.add_to_anki(argv[0], translation, pinyin, examples)
            for e in examples:
                words = pseg.cut(c, use_paddle=True)
                for word, flag in words:
                    if (
                        flag != "r"
                        and flag != "q"
                        and flag != "ul"
                        and flag != "x"
                        and flag != "uj"
                        and flag != "d"
                        and flag != "ud"
                    ):
                        # print("%s %s" % (word, flag))
                        self.translate([word])
            if len(argv[0]) > 1:
                for char in argv[0]:
                    self.translate([char])
        except Exception as e:
            print(e)
            pass

    def add_to_anki(self, hanzi, translation, pinyin, examples):
        data = {
            "params": {
                "notes": [
                    {
                        "deckName": "中文",
                        "modelName": "Chinese (Basic)",
                        "fields": {
                            "Hanzi": hanzi,
                            "Color": hanzi,
                            "Pinyin": pinyin,
                            "English": "<hr / >".join(translation)
                            + "<hr / >"
                            + "<hr />".join(examples),
                            "Sound": "",
                        },
                    }
                ]
            },
        }
        data["action"] = "canAddNotes"
        results = requests.post("http://127.0.0.1:8765", data=json.dumps(data))
        # print(data["params"]["notes"][0]["fields"])
        if (results.content)[1:-1] == b"true":
            data["action"] = "addNotes"
            self.waiting_for_review.append(data)
            self.bar.update(1)
            if len(self.waiting_for_review) == self.n:
                for_send = []
                for data in self.waiting_for_review:
                    print(data["params"]["notes"][0]["fields"])
                    inp = input("want this ? Y/N ")
                    if inp == "Y" or inp == "y":
                        for_send.append(data)
                if len(for_send) > 0:
                    for_send[0]["params"]["notes"] = [
                        data["params"]["notes"][0] for data in for_send
                    ]
                    results = requests.post(
                        "http://127.0.0.1:8765", data=json.dumps(for_send[0])
                    )
                self.waiting_for_review = []
                self.bar.refresh()
                self.bar.reset(total=self.n)
                already_known = self.__read_from_fs__()
                self.__write_to_fs__([w for w in self.known_words if w not in already_known])
                self.known_words = self.__read_from_fs__()
                print(results.content)

    def __write_to_fs__(self, batch_known:Iterable[str]):
        self.file = open(self.f, "a")
        for a in [f"${word}," for word in batch_known]:
            self.file.write(a)
        self.file.close()

    def __read_from_fs__(self) -> Iterable[str]:
        print("found fs cache")
        self.file = open(self.f, "r")
        self.file.seek(0)
        a = [w[1:] for w in self.file.readlines()[0].split(",")]
        self.file.close()
        print(a)
        return a


if __name__ == "__main__":
    YoudaoTranslate(int(sys.argv[2])).translate(sys.argv[1:])
