import random
import re
from bs4 import BeautifulSoup
import requests
from django import shortcuts
from datetime import datetime

class Religion:

    def get_bs(self, url) -> BeautifulSoup:
        return BeautifulSoup(requests.get(url).content, features="html.parser")


class Christianity(Religion):

    def __init__(self, request):
        super().__init__()
        self.request = request

    def bible(self) -> shortcuts.render:
        data = {}

        # Book
        books = self.get_bs("https://www.biblestudytools.com/niv/").find_all("a", {"class": "text-center text-xl mr-2 mb-2 bg-gray-100 inline-block hover:bg-yellow-400 hover:text-yellow-800 text-black w-64 p-5 border w-full rounded-md"})
        data["book"] = random.choice(books).string.strip()

        # Chapter
        chapter_url = f"https://www.biblestudytools.com/{data['book'].lower().replace(' ', '-')}/"
        total_chapters = self.get_bs(chapter_url).find_all("a", {"class": "text-center rounded-md text-2xl font-bold mr-2 mb-2 bg-gray-100 inline-block hover:bg-yellow-500 hover:text-yellow-800 text-black w-24 p-5 border"})[-1].find("span").string
        data["chapter"] = random.randint(1, int(total_chapters))
        data["sources"] = [f"{chapter_url}{data['chapter']}.html"]

        # Verses
        data["verses"] = []
        verses = self.get_bs(f"{chapter_url}{data['chapter']}.html").find_all("div", {"class": "p-1 px-2 md:px-3 leading-8 transition-colors rounded my-1"})
        data["num_verses"] = len(verses)
        for num_verse, verse in enumerate(verses):

            start = 1
            title = verse.find("h3")
            if title:
                data["verses"].append(("", "title_" + title.string.strip()))
                start = 2

            data["verses"].append((num_verse + 1, "".join(verse.find_all(text=True, recursive=False)[start:]).strip()))
                
        return shortcuts.render(self.request, "bible_reader.html", context=data)

class Islam(Religion):

    def __init__(self, request):
        super().__init__()
        self.request = request

    def quran(self) -> shortcuts.render:
        data = {}

        # Number of the chapter
        num_chapter = random.randint(1, 114)

        # Chapter data
        keys = iter(["name", "transcription", "translation", "num_verses"])
        vals = self.get_bs("https://www.quran-online.com/").find("span", attrs={"class": "transcription"}, string=re.compile(f"{num_chapter}. ")).parent.children

        for val in vals:
            if val != "\n":
                data[next(keys)] = val.text

        # Verses
        data["sources"] = []
        ar_bs = self.get_bs(f"https://www.quran-online.com/quran-arabic/surah-{data['transcription'].split()[1]}-arabic-{num_chapter}.html")
        ar_verses = ar_bs.find_all("span", {"class": "verset_en_arabe"})
        data["sources"].append(f"https://www.quran-online.com/quran-arabic/surah-{data['transcription'].split()[1]}-arabic-{num_chapter}.html")

        en_bs = self.get_bs(f"https://www.quran-online.com/quran-english/surah-{data['transcription'].split()[1]}-english-{num_chapter}.html")
        en_verses = en_bs.find_all("div", {"class": "texte_verset"})
        data["sources"].append(f"https://www.quran-online.com/quran-english/surah-{data['transcription'].split()[1]}-english-{num_chapter}.html")

        data["quran_verses"] = []
        for ar_verse, en_verse in zip(ar_verses, en_verses):
            data["quran_verses"].append((ar_verse.text.strip(), en_verse.find_all(text=True, recursive=True)[2].strip()))

        return shortcuts.render(self.request, "quran_reader.html", context=data)


class Sikhism(Religion):

    def __init__(self, request):
        super().__init__()
        self.request = request

    def sri_guru_granth_sahib(self) -> shortcuts.render:
        data = {}
        data["chapter"] = 1
        data["verses"] = []

        # Gurmukhi verses and their translation
        srigranth = self.get_bs(f"https://www.srigranth.org/servlet/gurbani.gurbani?Action=Page&Param={data['chapter']}")
        gurmukhi_verses = srigranth.find_all("font", {"face": "AnmolUniPr"})
        translations = srigranth.find_all("font", {"color": "#000080"})

        for gv, trans in zip(gurmukhi_verses, translations):
            data["verses"].append({
                "gurmukhi": " ".join(gv.find_all(text=True, recursive=True)),
                "translation": trans.string.strip()
            })

        # TODO Transcriptions and print in the web (and remove the call from the index)
        transcriptions = self.get_bs(f"https://www.srigurugranth.org/{data['chapter']:04d}.html").find_all("font", {"face": "Tahoma"})
        print(f"https://www.srigurugranth.org/{data['chapter']:04d}.html")
        for verse, transcription in zip(data["verses"], transcriptions):
            verse["transcription"] = " ".join(transcription.find_all(text=True, recursive=False))

        print(data, len(data["verses"]))
        