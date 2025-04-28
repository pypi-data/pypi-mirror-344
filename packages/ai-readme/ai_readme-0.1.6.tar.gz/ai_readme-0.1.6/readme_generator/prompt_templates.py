def get_prompt(lang: str, content_summary: str) -> str:
    if lang == "en":
        return (
            "You are an expert technical writer and software engineer.\n"
            "Generate a highly professional, detailed, and well-structured README.md for the project based on the following source files.\n\n"
            "Guidelines:\n"
            "- Start with a clear and concise project title.\n"
            "- Write a one-paragraph overview describing the project's purpose, key features, and target users.\n"
            "- Create a detailed Installation section, including dependencies, environment setup, and installation steps.\n"
            "- Create a detailed Usage section with examples of typical usage.\n"
            "- If applicable, include a Configuration section (such as environment variables).\n"
            "- Add a Features section listing key capabilities of the project.\n"
            "- Add a License section specifying the license type.\n"
            "- If necessary, create a Contributing section briefly explaining how to contribute.\n"
            "- If the source files imply workflows (e.g., API flows, component interactions), illustrate them using mermaid diagrams (e.g., `sequenceDiagram`, `flowchart`).\n"
            "- Use mermaid syntax only if meaningful and helpful.\n"
            "- If any information is missing, intelligently assume reasonable values or mark with [TODO].\n\n"
            "Here are the project files:\n"
            f"{content_summary}"
        )
    elif lang == "ko":
        return (
            "당신은 숙련된 기술 문서 작성자이자 소프트웨어 엔지니어입니다.\n"
            "아래 제공된 프로젝트 파일들을 기반으로 전문적이고, 세부적이며, 잘 구조화된 README.md 파일을 작성해 주세요.\n\n"
            "작성 가이드라인:\n"
            "- 명확하고 간결한 프로젝트 제목을 추가하세요.\n"
            "- 프로젝트 목적, 주요 기능, 타겟 사용자를 설명하는 한 단락짜리 개요를 작성하세요.\n"
            "- 의존성, 환경 설정, 설치 과정을 포함하는 상세한 설치 방법(Installation) 섹션을 작성하세요.\n"
            "- 일반적인 사용 예시를 포함하는 Usage 섹션을 작성하세요.\n"
            "- 필요 시 환경 변수나 설정 방법을 설명하는 Configuration 섹션을 추가하세요.\n"
            "- 프로젝트의 주요 기능들을 나열하는 Features 섹션을 추가하세요.\n"
            "- 라이선스 종류를 명시하는 License 섹션을 작성하세요.\n"
            "- 필요 시 기여 방법을 안내하는 Contributing 섹션을 작성하세요.\n"
            "- 소스 파일에서 API 흐름이나 컴포넌트 간 상호작용이 유추된다면 mermaid 다이어그램(`sequenceDiagram`, `flowchart` 등)을 추가해 시각화하세요.\n"
            "- mermaid 다이어그램은 의미 있고 도움이 되는 경우에만 사용하세요.\n"
            "- 정보가 부족한 경우 합리적으로 추정하거나 [작성 필요]로 표기하세요.\n\n"
            "다음은 프로젝트 파일 내용입니다:\n"
            f"{content_summary}"
        )
    else:
        raise ValueError(f"Unsupported language: {lang}")
