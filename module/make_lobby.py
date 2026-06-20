import os
import chardet
from jinja2 import Template
import natsort

def read_file_safe(path: str) -> str:
    """
    파일을 열어 인코딩을 자동으로 감지하고 안전하게 내용을 읽어옵니다.
    """
    try:
        with open(path, 'rb') as rb:
            rawdata = rb.read()
        result = chardet.detect(rawdata)
        enc = result['encoding'] or 'utf-8'

        with open(path, "r", encoding=enc, errors="replace") as f:
            return f.read()
    except Exception as e:
        print(f"⚠️ 파일을 읽는 중 오류 발생 ({path}): {e}")
        return ""

def generate_lobby_hub():
    # 1. 사용자로부터 경로 입력 받기
    user_path = input("경로: ").strip()
    
    if not os.path.isdir(user_path):
        print(f"❌ 입력하신 경로가 존재하지 않거나 폴더가 아닙니다: {user_path}")
        return

    print(f"\n{user_path} 위치에서 .html 파일을 탐색하여 로비 허브를 생성합니다...")

    lobby_output_name = "index.html"
    
    try:
        # 지정된 경로 직하의 파일/폴더 목록만 가져옴 (하위 폴더 내부 탐색 방지)
        all_files = os.listdir(user_path)
    except Exception as e:
        print(f"❌ 디렉토리 목록을 읽지 못했습니다: {e}")
        return

    webtoon_lst = []
    
    for file in all_files:
        try:
            # 서로게이트 인코딩 에러 방지를 위해 파일명 안전하게 정제
            safe_file = file.encode('utf-8', 'replace').decode('utf-8')
            full_file_path = os.path.join(user_path, safe_file)
            
            # 파일이 아니고 폴더이거나, .html 확장자가 아니면 제외
            if os.path.isdir(full_file_path) or not safe_file.lower().endswith('.html'):
                continue
                
            # 생성될 결과물(index.html) 및 원본 템플릿 파일 명칭들은 수집에서 제외
            if safe_file.lower() in [lobby_output_name, 'template.html', 'template2.html', 'template3.html']:
                continue

            # 파일 확장자(.html)를 제외한 순수 타이틀 추출
            pure_title = os.path.splitext(safe_file)[0]
            webtoon_lst.append((safe_file, pure_title))
            
        except Exception:
            continue  # 문제가 있는 파일명은 건너뜁니다.

    # 자연스러운 정렬(가나다/숫자순) 적용
    webtoon_lst = natsort.natsorted(webtoon_lst, key=lambda x: x[1])

    # 2. 템플릿3 로드 및 렌더링
    # 스크립트 실행 위치 기준으로 템플릿 경로 설정 (필요시 절대경로나 상대경로로 수정 가능)
    lobby_template_path = "./module/template/template3.html"
    
    if not os.path.exists(lobby_template_path):
        print(f"⚠️ 경고: 템플릿 스킨 파일({lobby_template_path})이 존재하지 않습니다.")
        return

    lobby_html_raw = read_file_safe(lobby_template_path)
    if not lobby_html_raw:
        print("❌ 템플릿 파일 내용이 비어있거나 읽을 수 없습니다.")
        return

    try:
        rendered_lobby = Template(lobby_html_raw).render(webtoon_lst=webtoon_lst)
        
        # 3. 사용자가 지정한 경로에 index.html 파일 생성 및 저장
        output_full_path = os.path.join(user_path, lobby_output_name)
        with open(output_full_path, 'w', encoding="UTF-8", errors="replace") as f:
            f.write(rendered_lobby)
            
        print(f"\n🎉 통합 중앙 로비 허브 빌드 완료!")
        print(f"📍 생성 위치: {os.path.abspath(output_full_path)}")
        print(f"📦 포함된 웹툰 개수: {len(webtoon_lst)}개")
        
    except Exception as e:
        print(f"❌ 로비 허브 파일 쓰기 중 오류 발생: {e}")

if __name__ == "__main__":
    generate_lobby_hub()