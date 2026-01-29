# Change Log History

## 2026-01-29

- **[Plan]** 오프라인 RAG 시스템 아키텍처 설계: 선박 내 인터넷 차단 환경을 고려하여 Local LLM (Llama 3.1)과 ChromaDB를 활용한 RAG 시스템 초기 설계를 수립함. 구성 요소 다이어그램 및 데이터 흐름 정의. (affected code files: `implementation_plan.md`, `task.md`)
- **[Infra]** 환경 및 의존성 구성: Python 3.10 가상환경(`.venv`) 설정 및 핵심 라이브러리(`langchain`, `chromadb`, `ollama`, `torch`) 설치 완료. 시스템 로그 저장을 위한 `logs/` 디렉토리 생성. (affected code files: `requirements.txt`, `.gitignore`)
- **[Feature]** 설정 관리 시스템 구현: 임베딩 모델, 청크 크기, 경로 등을 중앙에서 관리하기 위한 `src/config.py` 구현. 파일 기반 디버그 로깅(`app.log`, `rag_debug.log`)을 위한 `src/utils/logger.py` 구현. (affected code files: `src/config.py`, `src/utils/logger.py`)
- **[Feature]** 고급 문서 데이터 적재(Ingestion) 구현: 사용자 피드백을 반영하여 문서 특성에 따른 파싱 전략 패턴(Strategy Pattern)을 `src/utils/doc_loader.py`에 구현 (`fast_text`: PyMuPDF, `table_heavy`: PDFPlumber, `layout`: PyMuPDF4LLM). PDF 매뉴얼을 처리하고 ChromaDB 벡터 인덱스를 구축하는 `src/ingestion.py` 개발. (affected code files: `src/utils/doc_loader.py`, `src/ingestion.py`)
- **[Feature]** 오프라인 RAG 엔진 개발: `OllamaLLM` (Llama 3.1)과 `HuggingFaceEmbeddings`를 결합하여 `src/rag_engine.py`의 `RAGAnalyst` 클래스 개발. 한국어 시스템 프롬프트를 적용하여 검색(Retrieval) 및 답변 생성(Generation) 파이프라인 구축. (affected code files: `src/rag_engine.py`)
- **[Feature]** CLI 인터페이스 구현: `ingest` (파싱 전략 선택 가능) 및 `analyze` (센서값 입력 지원) 명령어를 지원하는 `main.py` 엔트리 포인트 구현. (affected code files: `main.py`)
- **[Refactor]** 하드웨어 최적화 (8GB VRAM 대응): RTX 4000 그래픽카드 환경에서 대용량 임베딩 모델(`BAAI/bge-m3`) 사용 시 OOM(메모리 부족) 위험 감지. 한국어 지원이 가능하면서 메모리 효율이 좋은 `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` (약 470MB)로 모델 변경 및 설정 업데이트. (affected code files: `src/config.py`, `implementation_plan.md`)
- **[Verification]** 더미 데이터 테스트 수행: 특정 알람 코드("ALARM-001")가 포함된 `data/manuals/test_manual.pdf`를 생성하여 `table_heavy` 전략(PDFPlumber) 기반의 파싱 및 인덱싱 성공 검증. (affected code files: `main.py`)
- **[Verification]** 종단간(End-to-End) 분석 테스트: "ALARM-001" 발생 상황을 시뮬레이션하여 `analyze` 명령 실행. 매뉴얼에서 정확한 키/값 쌍을 검색하고 Llama 3.1이 한국어로 원인 및 해결책을 제시하는 것을 확인함. (affected code files: `logs/rag_debug.log`, `walkthrough.md`)
- **[Documentation]** 프로젝트 산출물 작성: 설치 및 실행 가이드를 포함한 `README.md`와 검증 결과를 정리한 `walkthrough.md` 작성. (affected code files: `README.md`, `walkthrough.md`)
