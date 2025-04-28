def get_prompt(lang: str, content_summary: str) -> str:
    if lang == "en":
        return (
            f"Generate a professional, detailed README.md for a project based on the following source files:\n\n"
            f"- Include a project title\n"
            f"- Add a one-paragraph description\n"
            f"- Installation instructions\n"
            f"- Usage instructions\n"
            f"- License section\n"
            f"If information is missing, intelligently guess or indicate [TODO].\n"
            f"\nHere are the project files:\n{content_summary}"
        )
    elif lang == "ko":
        return (
            f"다음 소스 파일을 기반으로 전문적이고 상세한 README.md를 생성해 주세요:\n\n"
            f"- 프로젝트 제목 추가\n"
            f"- 한 문단 분량의 설명\n"
            f"- 설치 방법\n"
            f"- 사용 방법\n"
            f"- 라이선스 섹션\n"
            f"정보가 부족할 경우 [작성 필요]로 표기하세요.\n"
            f"\n프로젝트 파일 내용:\n{content_summary}"
        )
    else:
        raise ValueError(f"Unsupported language: {lang}")