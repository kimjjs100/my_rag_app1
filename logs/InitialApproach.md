# Change Log History - Offline RAG System

이 문서는 추후 개발 세션을 위해 현재 프로젝트의 개발 내역, 주요 의사결정, 그리고 변경 사항을 기록합니다.

## Project Info
- **Project Name**: Offline Real-time Sensor RAG System (Shipboard)
- **Target Environment**: Offline Ship Network (No Internet)
- **Hardware Constraints**: 
  - CPU: Intel Xeon Gold 5218 (32 cores)
  - GPU: NVIDIA Quadro RTX 4000 (8GB VRAM) *[Changed from initial high-spec consumer GPU]*
  - RAM: 32GB

## Development Timeline & Changes

### 1. Initial Architecture Design
- **Goal**: 선내 센서 데이터 및 알람 발생 시, 기술 문서(PDF)를 참조하여 원인 분석 제공.
- **Pipeline**:
  - **Ingestion**: PDF 문서 Parsing -> Chunking -> Embedding -> ChromaDB 저장.
  - **RAG Engine**: 질문 -> 검색(Retriever) -> LLM(Llama 3.1) -> 답변 생성.
- **Tech Stack**: Python 3.10, LangChain, ChromaDB, Ollama.

### 2. Implementation Details
- **Structure**:
  - `src/config.py`: 모델 경로 및 파라미터 관리.
  - `src/utils/doc_loader.py`: `ParsingStrategy` 패턴 적용 (`fast_text` vs `table_heavy` vs `layout`).
  - `src/ingestion.py`: 문서 로드 및 벡터 DB 구축 (Ingestion Pipeline).
  - `src/rag_engine.py`: `RAGAnalyst` 클래스 구현 (Retrieval + Generation).
  - `main.py`: CLI (`ingest`, `analyze`) 인터페이스.
- **Dependency Management**: `.venv` 가상환경 및 `requirements.txt` 구성.

### 3. Key Adjustments (Hardware Adaptation)
- **Issue**: 초기 `BAAI/bge-m3` 임베딩 모델 사용 계획이었으나, 8GB VRAM 환경에서의 OOM(Out of Memory) 우려 및 LLM(Llama 3.1 8B)과의 동시 구동 부하 고려.
- **Change**: 
  - Embedding Model을 `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`로 변경.
  - 선정 사유: 한국어/영어 검색 지원이 가능하면서도 메모리 사용량이 적음 (약 470MB).
  - Config 파일(`src/config.py`) 반영 완료.

### 4. Verification
- **Ingestion Test**:
  - `test_manual.pdf` (Dummy data with Table) 생성 및 `table_heavy` 전략(PDFPlumber)으로 파싱 성공.
  - 실제 매뉴얼 PDF 4종 Ingestion 수행 완료 (총 1598 Chunks).
- **RAG Analysis Test**:
  - **Scenario**: `ALARM-001` (High Pressure) 상황 시뮬레이션.
  - **Result**: `test_manual.pdf`의 내용을 정확히 참조하여 한국어로 "고압 원인 및 밸브 확인 필요" 답변 생성 확인.
  - **Performance**: 응답 시간 약 4초, VRAM 8GB 내에서 안정적 동작 확인.

## Current System Status
- **Source Code**: `src/` 폴더 내 기능 구현 완료.
- **Knowledge Base**: `vector_store/`에 ChromaDB 데이터 구축됨.
- **Models**: `models/` 폴더 및 Ollama에 모델 준비됨.
- **Logs**: `logs/` 폴더에 실행 이력 저장.

## Future To-Do (Context for Next Session)
1. **Real Data Integration**: 실제 센서 수집 모듈(100ms/1s 주기)과의 인터페이스 연동.
2. **GUI Development**: PyQt 기반의 운용자 UI 개발 시 `RAGAnalyst` 클래스 활용.
3. **Prompt Tuning**: 선박 특화 용어 및 상황에 맞춘 프롬프트 고도화.
