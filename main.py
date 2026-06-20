# -*- coding: utf-8 -*-
import os
from sys import exit
from rich import print

# 내부 모듈
from module.Nwebtoon import NWebtoon
from module.Headers import headers, image_headers
from module.Settings import Setting
from module.html_maker import HtmlMaker
from module.image_merger import ImageMerger
from module.input_validate import input_until_get_data, input_until_correct_download_range

# 콘솔창 타이틀 변경 (윈도우 전용)
WINDOW_TITLE = "NWebtoon Downloader v5.3-NEW"
if os.name == 'nt':
    import ctypes
    ctypes.windll.kernel32.SetConsoleTitleW(WINDOW_TITLE)

if __name__ == "__main__":
    s = Setting()
    while True:
        try:
            print("::[bold green]NWebtoon Downloader[/bold green]::")
            print('<모드를 선택해주세요>')
            print('[magenta]d[/magenta] : 다운로드')
            print('[magenta]o[/magenta] : 다운로드 폴더 열기')
            print('[magenta]m[/magenta] : 이미지 병합')
            print('[red]q[/red] : 프로그램 종료')
            # print('[magenta]h[/magenta] : HTML 생성')
            dialog = input('>>> ').strip().lower()

            if dialog == 'd':
                query = input_until_get_data(
                    default_prompt=">>> 정보를 입력해주세요(웹툰ID, URL, 웹툰제목) : ")
                webtoon = NWebtoon(query)

                print('-------------------------------')
                print(f"[bold green]웹툰명[/bold green] : {webtoon.title}")
                print(f"[bold green]총화수[/bold green] : {webtoon.number}화")
                print(f"[bold green]종류[/bold green] : {webtoon.wtype}")
                print(webtoon.content)
                print('-------------------------------')

                dialog = input_until_correct_download_range(
                    default_prompt='몇화부터 몇화까지 다운로드 받으시겠습니까? 예) 1-10 , 5: ',
                    error_prompt='>>> 다시 입력해주세요. 예) 1-10 , 5: ')

                if '-' not in dialog:
                    num = int(dialog)
                    webtoon.multi_download(num, num)
                else:
                    start, end = map(int, dialog.split('-'))
                    if end > webtoon.number:
                        input("최대화수를 초과했습니다")
                        continue
                    if end <= 0:
                        input("0 또는 음수는 입력할 수 없습니다.")
                        continue
                    webtoon.multi_download(start, end)
                input('다운로드가 완료되었습니다.')

            elif dialog == 'm':
                path = input("병합할 웹툰 경로를 입력해주세요 : ").strip()
                image = ImageMerger(path)
                image.print_lists()
                image.run()
                input('작업이 완료되었습니다.')

            elif dialog == 'h':
                print("히든 기능 발견! 해당 기능은 아직 개발중입니다. 버그 발생해도 책임지지 않습니다.")
                path = input("HTML을 생성할 웹툰 경로를 입력해주세요 : ").strip()
                html = HtmlMaker(path)
                html.print_lists()
                html.run()
                input('작업이 완료되었습니다.')

            elif dialog == 'o':
                path = os.path.realpath(s.download_path)
                os.startfile(path)
                print('다운로드 폴더를 열었습니다.')

            elif dialog == 'q':
                exit()

            else:
                input('올바르지 않은 입력입니다.')
                os.system('cls' if os.name == 'nt' else 'clear')

        except Exception as e:
            print(f"[red]오류 발생:[/red] {e}")
            input("엔터를 눌러 계속...")
